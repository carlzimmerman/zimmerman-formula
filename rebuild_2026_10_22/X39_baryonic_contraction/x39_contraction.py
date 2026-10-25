#!/usr/bin/env python3
"""X39_baryonic_contraction: X38's a0-cored cold dark energy halos, adiabatically contracted by baryons, on SPARC and clusters.

Frozen criteria: FROZEN_CRITERIA.md (b75acfc767). EM1's SPARC machinery and X30's cluster machinery executed read-only
(as X38); CFG922 BCG masses matched as X21. One thread.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x39_contraction.py            -> .out, _results.json
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x39_contraction.py --mutate   -> (1 - F) in the contraction (K1 must fail)
"""
import os, sys, json, math, time, resource, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
os.environ.pop("X30_MUTATE", None)
import numpy as np
from scipy.optimize import brentq, minimize_scalar

T0 = time.time()
MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
SGN = -1.0 if MUTATE else 1.0                                                  # (1 + F) vs (1 - F)

# ------------------------------------------------------------------ EM1 + X30 read-only (as X38)
EM1SRC = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); TE = open(EM1SRC).read()
NE = {"__file__": EM1SRC, "__name__": "em1_ro"}; argv0 = sys.argv; sys.argv = [EM1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(TE[:TE.index("# ---------------- backgrounds")], EM1SRC, "exec"), NE)
GALS, fit_one, pooled, line, UPS, LAW, A0 = (NE[k] for k in ("GALS", "fit_one", "pooled", "line", "UPS", "LAW", "A0"))
GE, MSUNE, MPCE = NE["G"], NE["MSUN"], NE["MPC"]
X30SRC = os.path.join(REB, "X30_sheet_cluster_profile", "x30_sheet_cluster_profile.py"); TX = open(X30SRC).read()
codeX = TX[:TX.index("# ============================================================== STEP 0")]
old = 'OUTF = open(os.path.join(HERE, f"x30_sheet_cluster_profile{TAG}.out"), "w")'; assert codeX.count(old) == 1
codeX = codeX.replace(old, f'OUTF = open({os.path.join(HERE, "x39_x30_machinery" + TAG + ".log")!r}, "w")')
NX = {"__file__": X30SRC, "__name__": "x30_ro"}; sys.argv = [X30SRC]
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    exec(compile(codeX, X30SRC, "exec"), NX)
sys.argv = argv0
FEET, HK, BN, M, DC, I, TID, T3M, ALLI, N, X1m, wls1, bsum, prep, PREP, RG, RM, X7J, MY = (NX[k] for k in (
    "FEET", "HK", "BN", "M", "DC", "I", "TID", "T3M", "ALLI", "N", "X1m", "wls1", "bsum", "prep", "PREP", "RG", "RM", "X7J", "MY"))
O_, P_, A_, DS_, KG, RF, SB, DAT = (NX[k] for k in ("offset_floor", "project_floor", "at_bins", "dsig_from_sig", "KG_PC2", "redfac", "sig_bins", "DAT"))
P(f"X39_baryonic_contraction  {'MUTATE run ((1 - F))' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; route E (Newtonian), a0-cored cold dark energy halos + adiabatic contraction; not theory closed")
P(f"EM1 and X30 machinery executed read-only [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

# ------------------------------------------------------------------ Burkert at fixed Sigma (X38 + A1, verbatim logic)
def B(x):
    x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
def solve_r0(Mtot, Rout, Sig):
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(B(Rout / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10})
    lpk = float(pk.x)
    if lm(lpk) < math.log(Mtot): return math.exp(lpk)
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), lpk, xtol=1e-14))
SIG = {f: A0[f] / (2 * math.pi * GE) for f in FEET}

# ------------------------------------------------------------------ contraction
def contract(r, Mb, M0, F, gnedin=None):
    """Blumenthal (or Gnedin with gnedin=(A, w, rvir)): returns M_cde,f on r. r ascending (m); Mb, M0 cumulative on r."""
    lr = np.log(r)
    def Mb_at(x): return np.interp(np.log(np.maximum(x, r[0])), lr, Mb, left=Mb[0], right=Mb[-1])
    def M0_at(x): return np.interp(np.log(np.maximum(x, r[0])), lr, M0, left=M0[0], right=M0[-1])
    if gnedin is None:
        rb = lambda x: x
    else:
        A, w, rv = gnedin; rb = lambda x: A * rv * (np.maximum(x, 1e-300) / rv) ** w
    Mi0 = M0_at(rb(r))
    rf = r.copy()
    for _ in range(100):
        rf_new = r * Mi0 * (1 + SGN * F) / np.maximum(Mb_at(rb(rf)) + Mi0, 1e-300)
        rf = 0.5 * rf + 0.5 * rf_new
    conv = float(np.max(np.abs(rf_new / rf - 1)))
    order = np.maximum.accumulate(rf); cross = int(np.sum(rf < order - 1e-12 * order))
    Mf = np.interp(np.log(r), np.log(order), M0, left=0.0, right=M0[-1])
    return Mf, conv, cross

P("\n=== checks")
RES = dict(frozen="b75acfc767", mutate=MUTATE, checks={}, footings={}); checks = []
rr = np.geomspace(1e18, 1e22, 40000); k_ = 1e20   # A1: fine test grid (interpolation error ~1e-4 at 400 points)
rf0 = None
Mz, c0z, _ = contract(rr, np.zeros_like(rr), k_ * rr, 0.0); k1a = float(np.max(np.abs(Mz / (k_ * rr) - 1)[5:-5])) < 1e-6
Mp, F_ = 5e40, 0.2
# point-mass baryons + SIS halo: r_f = k(1+F) r_i^2 / (k r_i + M_p)
Mt, ct, _ = contract(rr, np.full_like(rr, Mp), k_ * rr, F_)
rfa_all = k_ * (1 + F_) * rr ** 2 / (k_ * rr + Mp)                     # A1: test only shells whose r_f lies on the grid
sel = (rfa_all > rr[0] * 1.01) & (rr < rr[-1] / 1.5)
ri = rr[sel]; rfa = rfa_all[sel]
Mpred = np.interp(np.log(rfa), np.log(rr), Mt)
k1b = float(np.max(np.abs(Mpred / (k_ * ri) - 1))) < 1e-6
k1 = k1a and k1b
P(f"K1 Blumenthal: M_b = 0, F = 0 identity ({k1a}); point mass + SIS closed form max rel {float(np.max(np.abs(Mpred / (k_ * ri) - 1))):.2e} ({k1b}); convergence {ct:.1e}: {'PASS' if k1 else 'FAIL'}")
checks.append(("K1", k1))

# ------------------------------------------------------------------ CFG922 BCG masses, matched as X21
LANES = os.path.join(REPO, "campaign_fresh_gravity")
P687 = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
CEN = json.load(open(os.path.join(LANES, "CFG922_cluster_core_baryon_recheck", "cfg922_census_A1.json")))["eRASS1"]
J9 = np.full(N, -1)
for i in range(N):
    dd = np.hypot((P687["ra"] - MY["ra"][i]) * np.cos(np.radians(MY["dec"][i])), P687["dec"] - MY["dec"][i]) * 3600; j = int(np.argmin(dd))
    if dd[j] < 5 and abs(P687["z"][j] - MY["z"][i]) < 1e-3: J9[i] = j
meas = np.array([j >= 0 and not CEN[j].get("not_measured", False) for j in J9])
bcg = np.array([float(CEN[j]["bcg_med"]) if j >= 0 else np.nan for j in J9])
BCG = np.where(meas & (bcg > 0), bcg, np.nan)
nb = int(np.isfinite(BCG).sum()); k2 = nb == 190
fill = BCG.copy()
for t in range(3):
    m = T3M == t; med = float(np.nanmedian(BCG[m])); fill[m & ~np.isfinite(BCG)] = med
P(f"K2 CFG922 BCG matched {nb} (X21 'BCG>0 190'): {'PASS' if k2 else 'FAIL'}; filled {int((~np.isfinite(BCG)).sum())} by MGAS500-tercile median; "
  f"median BCG {np.nanmedian(BCG):.3g} Msun")
checks.append(("K2", k2))
KPC = 3.0857e19

# ------------------------------------------------------------------ clusters
def dvecN(i, foot, hk, Msrc):
    pp = prep(i, foot, hk); rho = np.gradient(Msrc, RM) / (4 * np.pi * RM ** 2)
    So = O_(P_(rho), pp["dmpc"]); Pp = A_(DS_(So)) / KG; fr, _ = RF(hk, i, SB(So)); return DAT[hk]["W"][i] * (Pp * fr)
def cluster_masses(i, foot, hk, mode):
    pp = prep(i, foot, hk); rta = pp["rta"]; r0 = solve_r0(pp["Mfair"], rta, SIG[foot])
    M0 = math.pi * SIG[foot] * r0 ** 2 * B(np.minimum(RM, rta) / r0)
    a = {"none": None, "a10": 10, "a5": 5, "a20": 20, "gnedin": 10}.get(mode, 10)
    Mbcg = np.zeros_like(RM) if (mode == "none" or a is None) else fill[i] * MSUNE * RM ** 2 / (RM + a * KPC) ** 2
    Mbf = pp["Mb"] + Mbcg
    if mode == "off": return pp["Mb"] + M0
    F = float(np.interp(rta, RM, Mbf)) / pp["Mfair"]
    g = (0.85, 0.8, rta) if mode == "gnedin" else None
    Mf, conv, cross = contract(RM, Mbf, M0, F, gnedin=g)
    return Mbf + Mf
def grade_clusters(foot, mode):
    out = {}
    for hk in HK:
        V = np.zeros((N, 8))
        for i in ALLI:
            V[i] = dvecN(int(i), foot, hk, cluster_masses(int(i), foot, hk, mode))
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
        out[hk + "_MIDall"] = float(kt[:, 1].sum() / ktC[:, 1].sum())
    keys = list(out["h0672"])
    ok = {k: all(abs(out[hk][k]["Z"]) <= 2 for hk in HK) for k in keys}
    bad = [k for k in keys if not ok[k]]
    sgn = {k: ("OVER" if out["h0672"][k]["pred"] > out["h0672"][k]["meas"] else "UNDER") for k in bad}
    return dict(cells=out, ok=ok, fails=[f"{k} ({sgn[k]})" for k in bad])

# ------------------------------------------------------------------ SPARC
EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
F3 = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
BGS = {t: dict(a=EM1J["rows"][t]["R1"]["a"], b=EM1J["rows"][t]["R1"]["b"], h=F3[t]["params"]["h"]) for t in ("A_c2b_refit", "B_cfg886_bg")}
def sparc(f, a, b, h, mode="blumenthal"):
    rc = 3 * (100 * h * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); rows = []; uprs = []
    for q in GALS:
        lM = a + b * (q["lMb"] - 10); M200 = 10 ** lM * MSUNE; R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
        r0 = solve_r0(M200, R200, SIG[f]); R = q["Rm"]
        if mode == "off":
            gh = (GE * math.pi * SIG[f] * r0 ** 2 * B(R / r0) / R ** 2)[:, None] * np.ones((1, len(UPS)))
        else:
            rg = np.geomspace(R[0] * 0.05, R200, 300); M0 = math.pi * SIG[f] * r0 ** 2 * B(rg / r0)
            gh = np.zeros((len(R), len(UPS)))
            for iu, U in enumerate(UPS):
                Mbk = np.maximum.accumulate(np.maximum(q["GB"][:, iu] * R ** 2 / GE, 0.0))
                Mtot = max(float(Mbk[-1]), (U * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9 * MSUNE)
                Mbg = np.where(rg < R[0], Mbk[0] * (rg / R[0]) ** 2, np.interp(np.log(rg), np.log(R), Mbk))
                out = rg > R[-1]
                if out.any():
                    t = np.clip(np.log(rg[out] / R[-1]) / math.log(3.0), 0, 1); Mbg[out] = np.exp(np.log(max(Mbk[-1], 1e-300)) * (1 - t) + np.log(Mtot) * t)
                Mbg = np.maximum.accumulate(Mbg)
                F = Mtot / M200
                g_ = (0.85, 0.8, R200) if mode == "gnedin" else None
                Mf, _, _ = contract(rg, Mbg, M0, F, gnedin=g_)
                gh[:, iu] = GE * np.interp(np.log(R), np.log(rg), Mf) / R ** 2
        rows.append(fit_one(q, np.log10(np.maximum(q["GB"] + gh, 1e-300))))
    return pooled([r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows])

# K0: contraction off reproduces X38
s_off = sparc("canonical", BGS["A_c2b_refit"]["a"], BGS["A_c2b_refit"]["b"], BGS["A_c2b_refit"]["h"], mode="off")
g_off = grade_clusters("canonical", "off")
k0 = abs(s_off["rms"] - 0.0795) < 1e-4 and abs(g_off["cells"]["h0672"]["G-OUT-all"]["pred"] - 0.697) < 1e-3
P(f"K0 contraction off: SPARC rms {s_off['rms']:.4f} (X38 0.0795), OUTER all pred {g_off['cells']['h0672']['G-OUT-all']['pred']:.3f} (X38 0.697): {'PASS' if k0 else 'FAIL'}")
checks.append(("K0", k0)); P(f"  [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

X38J = json.load(open(os.path.join(REB, "X38_a0_surface_density_halos", "x38_sd_halos_results.json")))
for f in FEET:
    P(f"\n=== [{f}]")
    sp_ = {}
    for t, bg in BGS.items():
        st = sparc(f, bg["a"], bg["b"], bg["h"]); sp_[t] = dict(st, line=line(st))
        x38 = X38J["footings"][f]["sparc"][t]
        P(f"  SPARC [{t}] SD + AC: rms {st['rms']:.4f}, median U {st['U_median']:.2f} -> line {'PASS' if line(st) else 'FAIL'}   (X38 no contraction {x38['rms']:.4f}@{x38['U_median']:.2f})")
    gc = grade_clusters(f, "a10")
    c0, c1 = gc["cells"]["h0672"], gc["cells"]["h0686"]; x38c = X38J["footings"][f]["clusters"]["cells"]["h0672"]
    for k in [kk for kk in c0 if kk.startswith("G-")]:
        P(f"     {k:10s} meas {c0[k]['meas']:+.3f}+-{c0[k]['s']:.3f} pred {c0[k]['pred']:+.3f} Z {c0[k]['Z']:+.2f} (X38 {x38c[k]['pred']:+.3f}, Z {x38c[k]['Z']:+.2f}) | h0.686 Z {c1[k]['Z']:+.2f}"
          + ("" if gc["ok"][k] else "  FAIL"))
    P(f"     MID all-KT pred {c0['h0672_MIDall'] if 'h0672_MIDall' in c0 else gc['cells']['h0672_MIDall']:.3f} (meas {M[f'{f}|h0672']['KT_all|MID']['A']:.3f})")
    rep = {}
    for mode in ("none", "a5", "a20", "gnedin"):
        g2 = grade_clusters(f, mode); rep[mode] = dict(fails=g2["fails"], MID_T3=g2["cells"]["h0672"]["G-MID-T3"]["pred"], MIDb=g2["cells"]["h0672"]["G-MID-b"]["pred"],
                                                      OUT_all=g2["cells"]["h0672"]["G-OUT-all"]["pred"], M3=g2["cells"]["h0672"]["G-OUT-M3"]["pred"])
        P(f"  (reported) clusters {mode}: fails {g2['fails'] or 'none'}; MID T3 {rep[mode]['MID_T3']:.3f}, MID b {rep[mode]['MIDb']:+.3f}, OUTER all {rep[mode]['OUT_all']:.3f}, MGAS T3 OUTER {rep[mode]['M3']:.3f}")
    sg = sparc(f, BGS["A_c2b_refit"]["a"], BGS["A_c2b_refit"]["b"], BGS["A_c2b_refit"]["h"], mode="gnedin")
    P(f"  (reported, EXTERNALLY CALIBRATED) SPARC Gnedin (bg A): rms {sg['rms']:.4f}, median U {sg['U_median']:.2f}, line {'PASS' if line(sg) else 'FAIL'}")
    spass = all(v["line"] for v in sp_.values()); cpass = not gc["fails"]
    v = ("SD + AC PASSES" if spass and cpass else "SD + AC PASSES SPARC ONLY" if spass else "SD + AC PASSES CLUSTERS ONLY" if cpass else "SD + AC FAILS")
    det = ([] if spass else ["SPARC line"]) + gc["fails"]
    RES["footings"][f] = dict(sparc=sp_, sparc_gnedin=sg, clusters=gc, clusters_reported=rep, verdict=v, failing=det)
    P(f"  VERDICT [{f}]: {v}" + (f"  (failing: {', '.join(det)})" if det else "") + f"   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

V = {f: RES["footings"][f]["verdict"] for f in FEET}
RES["verdict"] = V["canonical"] if V["canonical"] == V["alt"] else f"UNDECIDED (footings disagree: {V})"
P(f"\n=== VERDICT (both footings): {RES['verdict']}")
checks.append(("K3", rss() < 2.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(ok for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
open(os.path.join(HERE, f"x39_contraction{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x39_contraction_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if n == len(checks) else 1)
