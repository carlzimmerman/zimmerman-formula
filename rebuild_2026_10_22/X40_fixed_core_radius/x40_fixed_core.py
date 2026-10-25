#!/usr/bin/env python3
"""X40_fixed_core_radius: route-E cold dark energy halos with a Burkert core of FIXED size r_c (calibrated on SPARC only), on clusters.

Frozen criteria: FROZEN_CRITERIA.md (b37983a0f7). Built from X38's committed script (SD functions kept for K0). EM1's SPARC machinery (up to its backgrounds block) and X30's cluster
machinery (up to its STEP 0) are executed read-only in separate namespaces; X30's log is redirected here. One thread.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x38_sd_halos.py            -> .out, _results.json
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x38_sd_halos.py --mutate   -> +2 arctan in B(x) (K1 must fail)
"""
import os, sys, json, math, time, resource, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
os.environ.pop("X30_MUTATE", None)
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

T0 = time.time()
MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)

# ------------------------------------------------------------------ EM1 (read-only, up to backgrounds)
EM1SRC = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); TE = open(EM1SRC).read()
codeE = TE[:TE.index("# ---------------- backgrounds")]
NE = {"__file__": EM1SRC, "__name__": "em1_ro"}; argv0 = sys.argv; sys.argv = [EM1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(codeE, EM1SRC, "exec"), NE)
sys.argv = argv0
GALS, fit_one, pooled, line, UPS, LAW, NEWT, A0 = (NE[k] for k in ("GALS", "fit_one", "pooled", "line", "UPS", "LAW", "NEWT", "A0"))
GE, MSUNE, MPCE = NE["G"], NE["MSUN"], NE["MPC"]
# ------------------------------------------------------------------ X30 (read-only, up to STEP 0)
X30SRC = os.path.join(REB, "X30_sheet_cluster_profile", "x30_sheet_cluster_profile.py"); TX = open(X30SRC).read()
codeX = TX[:TX.index("# ============================================================== STEP 0")]
old = 'OUTF = open(os.path.join(HERE, f"x30_sheet_cluster_profile{TAG}.out"), "w")'; assert codeX.count(old) == 1
codeX = codeX.replace(old, f'OUTF = open({os.path.join(HERE, "x40_x30_machinery" + TAG + ".log")!r}, "w")')
NX = {"__file__": X30SRC, "__name__": "x30_ro"}; sys.argv = [X30SRC]
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    exec(compile(codeX, X30SRC, "exec"), NX)
sys.argv = argv0
FEET, HK, BN, M, DC, I, TID, T3M, ALLI, N, X1m, wls1, bsum, prep, PREP, RG, RM, X7J = (NX[k] for k in (
    "FEET", "HK", "BN", "M", "DC", "I", "TID", "T3M", "ALLI", "N", "X1m", "wls1", "bsum", "prep", "PREP", "RG", "RM", "X7J"))
GX = NX["G"]
P(f"X40_fixed_core_radius  {'MUTATE run (+2 arctan in B)' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; route E (Newtonian, no law force), cold dark energy halos with a fixed core size r_c (SPARC-calibrated); not theory closed")
P(f"EM1 and X30 machinery executed read-only [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

# ------------------------------------------------------------------ Burkert at fixed surface density
def B(x):
    x = np.asarray(x, float)
    return np.log1p(x * x) + 2 * np.log1p(x) + (2 if MUTATE else -2) * np.arctan(x)
SAT = {"n": 0}
def solve_r0(Mtot, Rout, Sig):
    """A1: compact root (r0 <= r0_pk); if Mtot > M_max(R) the halo is SATURATED at r0_pk (counted)."""
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(B(Rout / math.exp(lr))))
    from scipy.optimize import minimize_scalar
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10})
    lpk = float(pk.x)
    if lm(lpk) < math.log(Mtot):
        SAT["n"] += 1; return math.exp(lpk)
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), lpk, xtol=1e-14))
SIG = {f: A0[f] / (2 * math.pi * GE) for f in FEET}                          # kg/m^2
SIG_PC = {f: SIG[f] * (3.0857e16) ** 2 / MSUNE for f in FEET}
P(f"Sigma_a0 = a0/(2 pi G): canonical {SIG_PC['canonical']:.1f}, alt {SIG_PC['alt']:.1f} Msun/pc^2 (SECOND_LAW_HUNT: 107 / 129; Li+2020 Burkert median 177, context only)")
RES = dict(frozen="b37983a0f7", mutate=MUTATE, Sigma_Msun_pc2=SIG_PC, footings={}, checks={}); checks = []

# K0
k0a = all(abs(LAW[f]["rms"] - r) < 1e-4 for f, r in (("canonical", 0.0541), ("alt", 0.0537)))
o = M["canonical|h0672"]; k0b = abs(o["KT_all|OUTER"]["A"] - 0.716) < 6e-4 and abs(o["KT_all|MID"]["A"] - 1.668) < 6e-4
k0 = k0a and k0b
P(f"K0 EM1 law rms {LAW['canonical']['rms']:.4f} / {LAW['alt']['rms']:.4f}; X30 OUTER / MID {o['KT_all|OUTER']['A']:.4f} / {o['KT_all|MID']['A']:.4f}: {'PASS' if k0 else 'FAIL'}")
checks.append(("K0", k0))
# K1
r0t, Rt, St = 3.0857e19, 10 * 3.0857e19, SIG["canonical"]
rho0 = St / r0t
quadM = quad(lambda r: 4 * math.pi * r * r * rho0 * r0t ** 3 / ((r + r0t) * (r * r + r0t * r0t)), 0, Rt, epsabs=0, epsrel=1e-12, limit=400)[0]
cfM = math.pi * St * r0t ** 2 * float(B(Rt / r0t))
Mt = 1e11 * MSUNE; R2 = 3.0e21; r0s = solve_r0(Mt, R2, St)   # A1: feasible test mass
k1 = abs(cfM / quadM - 1) < 1e-6 and abs(math.pi * St * r0s ** 2 * float(B(R2 / r0s)) / Mt - 1) < 1e-8
P(f"K1 Burkert closed form vs quadrature {cfM / quadM - 1:+.2e}; solved r0 returns M {math.pi * St * r0s ** 2 * float(B(R2 / r0s)) / Mt - 1:+.2e}: {'PASS' if k1 else 'FAIL'}")
checks.append(("K1", k1))

# ------------------------------------------------------------------ SPARC
EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
F3 = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
BGS = {t: dict(a=EM1J["rows"][t]["R1"]["a"], b=EM1J["rows"][t]["R1"]["b"], h=F3[t]["params"]["h"]) for t in ("A_c2b_refit", "B_cfg886_bg")}
KPCm = 3.0857e19
def Bfix(x): return B(x)
def sparc(a, b, h, rc_kpc=None, sd_f=None):
    """rc_kpc: fixed core (FC); sd_f: X38's SD halo on footing sd_f (K0)."""
    rc = 3 * (100 * h * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); rows = []
    for q in GALS:
        lM = a + b * (q["lMb"] - 10); M200 = 10 ** lM * MSUNE; R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
        if sd_f is not None:
            r0 = solve_r0(M200, R200, SIG[sd_f]); Mh = math.pi * SIG[sd_f] * r0 ** 2 * B(q["Rm"] / r0)
        else:
            r0 = rc_kpc * KPCm; Mh = M200 * Bfix(q["Rm"] / r0) / float(Bfix(R200 / r0))
        rows.append(fit_one(q, np.log10(np.maximum(q["GB"] + (GE * Mh / q["Rm"] ** 2)[:, None], 1e-300))))
    return pooled([r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows])
st38 = sparc(BGS["A_c2b_refit"]["a"], BGS["A_c2b_refit"]["b"], BGS["A_c2b_refit"]["h"], sd_f="canonical")
# ------------------------------------------------------------------ clusters
O_, P_, A_, DS_, KG, RF, SB, DAT = (NX[k] for k in ("offset_floor", "project_floor", "at_bins", "dsig_from_sig", "KG_PC2", "redfac", "sig_bins", "DAT"))
def dvecN(i, foot, hk, Msrc):
    pp = prep(i, foot, hk); rho = np.gradient(Msrc, RM) / (4 * np.pi * RM ** 2)
    So = O_(P_(rho), pp["dmpc"]); Pp = A_(DS_(So)) / KG; fr, _ = RF(hk, i, SB(So)); return DAT[hk]["W"][i] * (Pp * fr)
def halo(i, foot, hk, rc_kpc=None):
    pp = prep(i, foot, hk); rta = pp["rta"]
    if rc_kpc is None:
        r0 = solve_r0(pp["Mfair"], rta, SIG[foot]); return math.pi * SIG[foot] * r0 ** 2 * B(np.minimum(RM, rta) / r0)
    r0 = rc_kpc * KPCm; return pp["Mfair"] * Bfix(np.minimum(RM, rta) / r0) / float(Bfix(rta / r0))
def grade_clusters(foot, rc_kpc=None):
    out = {}
    for hk in HK:
        V = np.zeros((N, 8))
        for i in ALLI:
            V[i] = dvecN(int(i), foot, hk, prep(int(i), foot, hk)["Mb"] + halo(int(i), foot, hk, rc_kpc))
        PREP.clear()
        cl = f"{foot}|{hk}"; o = M[cl]; vB = bsum(V); vC = bsum(DC[(foot, hk)]); kt, ktC = vB[I], vC[I]; g = {}
        for bi, b in enumerate(BN):
            At = [float(kt[TID == t, bi].sum() / ktC[TID == t, bi].sum()) for t in range(3)]; Aa = float(kt[:, bi].sum() / ktC[:, bi].sum())
            bp = float(wls1(kt[:, bi], ktC[:, bi], X1m)[1])
            if b == "MID":
                for t in range(3): g[f"G-MID-T{t+1}"] = (o["KT_terc|MID"][t]["A"], o["KT_terc|MID"][t]["s"], At[t])
                g["G-MID-b"] = (o["KT_b|MID"]["b"], o["KT_b|MID"]["s_b"], bp)
            if b == "OUTER":
                g["G-OUT-all"] = (o["KT_all|OUTER"]["A"], o["KT_all|OUTER"]["s"], Aa)
                for t in range(3): g[f"G-OUT-T{t+1}"] = (o["KT_terc|OUTER"][t]["A"], o["KT_terc|OUTER"][t]["s"], At[t])
                g["G-OUT-b"] = (o["KT_b|OUTER"]["b"], o["KT_b|OUTER"]["s_b"], bp)
            if b == "INNER":
                g["G-IN-all"] = (o["KT_all|INNER"]["A"], o["KT_all|INNER"]["s_IN"], Aa)
        r7 = X7J["bins"][f"terciles|{cl}"]; a7 = X7J["all"][f"C*|boost|{cl}"]
        Am = [[float(vB[T3M == t, bi].sum() / vC[T3M == t, bi].sum()) for t in range(3)] for bi in range(3)]
        Aall = [float(vB[:, bi].sum() / vC[:, bi].sum()) for bi in range(3)]
        g["G-OUT-Mall"] = (a7["OUTER"]["A_CAL"], a7["OUTER"]["s_CAL"], Aall[2])
        for t in range(3): g[f"G-OUT-M{t+1}"] = (r7[t]["OUTER"]["A_CAL"], r7[t]["OUTER"]["s_CAL"], Am[2][t])
        g["G-IN-Mall"] = (o["M_all|INNER"]["A"], o["M_all|INNER"]["s_IN"], Aall[0])
        out[hk] = {k: dict(meas=v[0], s=v[1], pred=v[2], Z=(v[0] - v[2]) / v[1]) for k, v in g.items()}
    keys = list(out["h0672"])
    ok = {k: all(abs(out[hk][k]["Z"]) <= 2 for hk in HK) for k in keys}
    bad = [k for k in keys if not ok[k]]
    sgn = {k: ("OVER" if out["h0672"][k]["pred"] > out["h0672"][k]["meas"] else "UNDER") for k in bad}
    return dict(cells=out, ok=ok, fails=[f"{k} ({sgn[k]})" for k in bad])
g38 = grade_clusters("canonical")
k0 = abs(st38["rms"] - 0.0795) < 1e-4 and abs(g38["cells"]["h0672"]["G-OUT-all"]["pred"] - 0.697) < 1e-3
P(f"K0 X38 SD reproduced: SPARC rms {st38['rms']:.4f} (0.0795); OUTER all pred {g38['cells']['h0672']['G-OUT-all']['pred']:.3f} (0.697): {'PASS' if k0 else 'FAIL'}")
checks.append(("K0", k0))
# K1 fixed-r_c normalisation
pp = prep(0, "canonical", "h0672"); Mh = halo(0, "canonical", "h0672", 5.0); PREP.clear()
k1a = abs(float(pp["Mfair"] * Bfix(pp["rta"] / (5.0 * KPCm)) / float(Bfix(pp["rta"] / (5.0 * KPCm)))) / pp["Mfair"] - 1) < 1e-10 and abs(float(Mh[-1]) / pp["Mfair"] - 1) < 1e-10   # A1: evaluate at r_ta exactly, not by grid interpolation
k1 = k1 and k1a
P(f"K1 (with the fixed-r_c normalisation, fair share at r_ta: {k1a}): {'PASS' if k1 else 'FAIL'}"); checks[[c[0] for c in checks].index("K1")] = ("K1", k1)
# calibration
GRID = np.geomspace(0.5, 30.0, 41); bA = BGS["A_c2b_refit"]
rmsA = []
for rc_ in GRID:
    st = sparc(bA["a"], bA["b"], bA["h"], rc_kpc=float(rc_)); rmsA.append((float(rc_), st["rms"], st["U_median"]))
ib = int(np.argmin([r[1] for r in rmsA])); RC = rmsA[ib][0]
P(f"\nSPARC calibration (bg A): r_c = {RC:.3f} kpc (rms {rmsA[ib][1]:.4f}, median U {rmsA[ib][2]:.2f})")
P("  grid (r_c kpc: rms / U): " + "; ".join(f"{r:.2f}: {s:.4f}/{u:.2f}" for r, s, u in rmsA[::4]))
near = [r for r in rmsA if r[1] - rmsA[ib][1] <= 0.002]
P(f"  r_c within drms 0.002: {near[0][0]:.2f} - {near[-1][0]:.2f} kpc; L* (21.7 / 22.9 pc) stated for comparison")
st0 = sparc(bA["a"], bA["b"], bA["h"], rc_kpc=1e-4)
k2 = st0["U_median"] < 0.77
P(f"K2 r_c -> 0 approaches a cusp: median U {st0['U_median']:.2f} (< X38 0.77): {'PASS' if k2 else 'FAIL'}"); checks.append(("K2", k2))
sp_ = {}
for t, bg in BGS.items():
    st = sparc(bg["a"], bg["b"], bg["h"], rc_kpc=RC); sp_[t] = dict(st, line=line(st))
    P(f"  SPARC [{t}] at r_c {RC:.2f} kpc: rms {st['rms']:.4f}, median U {st['U_median']:.2f} -> line {'PASS' if line(st) else 'FAIL'}")
spass = all(v["line"] for v in sp_.values())
RES["r_c_kpc"] = RC; RES["calibration"] = rmsA; RES["sparc"] = sp_
X38J = json.load(open(os.path.join(REB, "X38_a0_surface_density_halos", "x38_sd_halos_results.json")))
for f in FEET:
    P(f"\n=== [{f}] r_c = {RC:.3f} kpc")
    gc = grade_clusters(f, RC); c0, c1 = gc["cells"]["h0672"], gc["cells"]["h0686"]; x = X38J["footings"][f]["clusters"]["cells"]["h0672"]
    for k in c0:
        P(f"     {k:10s} meas {c0[k]['meas']:+.3f}+-{c0[k]['s']:.3f} pred {c0[k]['pred']:+.3f} Z {c0[k]['Z']:+.2f} (X38 Z {x[k]['Z']:+.2f}) | h0.686 Z {c1[k]['Z']:+.2f}"
          + ("" if gc["ok"][k] else "  FAIL"))
    rep = {}
    for rn in (near[0][0], near[-1][0]):
        g2 = grade_clusters(f, rn); rep[f"{rn:.2f}"] = g2["fails"]
        P(f"  (reported) clusters at r_c {rn:.2f} kpc: fails {g2['fails'] or 'none'}")
    cpass = not gc["fails"]
    v = ("FC PASSES" if spass and cpass else "FC PASSES SPARC ONLY" if spass else "FC PASSES CLUSTERS ONLY" if cpass else "FC FAILS")
    det = ([] if spass else ["SPARC line"]) + gc["fails"]
    RES["footings"][f] = dict(clusters=gc, reported_neighbours=rep, verdict=v, failing=det)
    P(f"  VERDICT [{f}]: {v}" + (f"  (failing: {', '.join(det)})" if det else "") + f"   [{time.time() - T0:.0f} s]")

V = {f: RES["footings"][f]["verdict"] for f in FEET}
RES["verdict"] = V["canonical"] if V["canonical"] == V["alt"] else f"UNDECIDED (footings disagree: {V})"
P(f"\n=== VERDICT (both footings): {RES['verdict']}")
checks.append(("K3", rss() < 2.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(ok for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
open(os.path.join(HERE, f"x40_fixed_core{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x40_fixed_core_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if n == len(checks) else 1)
