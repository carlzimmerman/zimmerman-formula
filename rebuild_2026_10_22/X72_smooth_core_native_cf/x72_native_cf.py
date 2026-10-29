#!/usr/bin/env python3
"""X72_smooth_core_native_cf: X71's script (smooth core + uniform f* injection) with eta(M) = (4/(3 B_S(1))) c_f(M)^(5/4)
from X48's native c_f table (lg-M interpolation, flat outside, as x48_regrade.py).
Frozen criteria: FROZEN_CRITERIA.md (ba337e221c). One thread.

    X72_CF=const4 X71_FSTAR=0.034 python3 x72_native_cf.py                       # K1 identity (must equal X71)
    X72_CF=../X48_native_cf_zoom/x48_analyze_results_ng64_A4.json X71_FSTAR=0.034 python3 x72_native_cf.py
    add X72_CFMULT=2 for MUTATE
"""
import os, sys, json, math, time, resource, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
os.environ.pop("X30_MUTATE", None)
import numpy as np
FSTAR = float(os.environ.get("X71_FSTAR", "0.20")); SHAPEREQ = os.environ.get("X71_SHAPE", "S")
CFSRC = os.environ.get("X72_CF", "const4"); CFMULT = float(os.environ.get("X72_CFMULT", "1"))
if CFSRC == "const4":
    CFLM, CFV = np.array([12.0, 14.0]), np.array([4.0, 4.0])
else:
    _t = {float(k): v for k, v in json.load(open(CFSRC))["cf_by_mass"].items() if v is not None}
    if not all(any(abs(math.log10(m) - l) < 1e-6 for m in _t) for l in (12, 13, 14)): raise SystemExit("UNDECIDED: A4 table lacks 1e12/1e13/1e14")
    CFLM = np.array(sorted(math.log10(m) for m in _t)); CFV = np.array([_t[min(_t, key=lambda m: abs(math.log10(m) - l))] for l in CFLM])
CFV = CFV * CFMULT
def cf_of(M): return float(np.interp(math.log10(M), CFLM, CFV))
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
codeE = TE[:TE.index("# ---------------- halo profiles")]   # X41: includes EM1 backgrounds (CLASS)
NE = {"__file__": EM1SRC, "__name__": "em1_ro"}; argv0 = sys.argv; sys.argv = [EM1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(codeE, EM1SRC, "exec"), NE)
sys.argv = argv0
GALS, fit_one, pooled, line, UPS, LAW, NEWT, A0, BGSE = (NE[k] for k in ("GALS", "fit_one", "pooled", "line", "UPS", "LAW", "NEWT", "A0", "BGS"))
GE, MSUNE, MPCE = NE["G"], NE["MSUN"], NE["MPC"]
# ------------------------------------------------------------------ X30 (read-only, up to STEP 0)
X30SRC = os.path.join(REB, "X30_sheet_cluster_profile", "x30_sheet_cluster_profile.py"); TX = open(X30SRC).read()
codeX = TX[:TX.index("# ============================================================== STEP 0")]
old = 'OUTF = open(os.path.join(HERE, f"x30_sheet_cluster_profile{TAG}.out"), "w")'; assert codeX.count(old) == 1
codeX = codeX.replace(old, f'OUTF = open({os.path.join(HERE, "x72_x30_machinery" + TAG + ".log")!r}, "w")')
INJ = 'Mb = Mg*(1 + 0.20)'; assert codeX.count(INJ) == 1; codeX = codeX.replace(INJ, 'Mb = Mg*(1 + FSTAR_INJ)')
NX = {"__file__": X30SRC, "__name__": "x30_ro", "FSTAR_INJ": FSTAR}; sys.argv = [X30SRC]
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    exec(compile(codeX, X30SRC, "exec"), NX)
sys.argv = argv0
FEET, HK, BN, M, DC, I, TID, T3M, ALLI, N, X1m, wls1, bsum, prep, PREP, RG, RM, X7J = (NX[k] for k in (
    "FEET", "HK", "BN", "M", "DC", "I", "TID", "T3M", "ALLI", "N", "X1m", "wls1", "bsum", "prep", "PREP", "RG", "RM", "X7J"))
GX = NX["G"]
P(f"X70_smooth_core_shape  {'MUTATE run (Burkert kept)' if MUTATE else 'normal run'}  [c_f EXTERNAL]")
P("kappa = 1/2 FITTED; footings never pooled; route E (Newtonian, no law force), core Sigma = max(a0/(2 pi G), eta x EPS collapse Sigma), eta from self-similar infall, c_f = 4 EXTERNAL; not theory closed")
P(f"EM1 and X30 machinery executed read-only [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

# ------------------------------------------------------------------ Burkert at fixed surface density
SHAPE = {"s": "B"}
def B(x):
    x = np.asarray(x, float)
    if SHAPE["s"] == "S": return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))
    return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
def rho_shape(r, r0, rho0):
    if SHAPE["s"] == "S": return rho0 * r0 ** 3 / (r * r + r0 * r0) ** 1.5
    return rho0 * r0 ** 3 / ((r + r0) * (r * r + r0 * r0))
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
RES = dict(frozen="190df89a83", mutate=MUTATE, Sigma_Msun_pc2=SIG_PC, footings={}, checks={}); checks = []

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

# ------------------------------------------------------------------ EPS formation (frozen section 1)
DC, OMEGA, DELTA = 1.686, 0.974, 18 * math.pi ** 2
B1 = 3 * math.log(2) - math.pi / 2; CF = 4.0; GAM = 2.25
def eta_of(cf, gam=None): return 4.0 / (3.0 * float(B(1.0))) * cf ** ((GAM if gam is None else gam) - 1.0)
ETA = eta_of(CF)
PC2 = (3.0857e16) ** 2
EPS = {}
for tag, bg in BGSE.items():
    cc = bg["c"]; h = bg["h"]; Om = float(cc.Omega_m()); rhom0 = Om * 2.775e11 * h ** 2              # Msun / Mpc^3
    zg = np.linspace(0, 30, 3001); Dg = np.array([cc.scale_independent_growth_factor(z) for z in zg]); Dg /= Dg[0]
    lMg = np.linspace(7.0, 16.5, 191); sigf = bg["cB"].__defaults__[1]                                      # EM1 stores sigma(M) as cB's default argument
    s2 = np.array([float(sigf(10 ** l)[0]) ** 2 for l in lMg])
    EPS[tag] = dict(rhom0=rhom0, zg=zg, Dg=Dg, lMg=lMg, s2=s2, h=h, s8=bg["s8"], s8F3=bg["s8_F3"])
def zform(tag, M):
    e = EPS[tag]; s2 = lambda l: float(np.interp(l, e["lMg"], e["s2"]))
    S = math.sqrt(max(s2(math.log10(M / 2)) - s2(math.log10(M)), 0.0)); Df = DC / (DC + OMEGA * S)
    if Df >= 1.0: return 0.0, Df
    return float(np.interp(-Df, -e["Dg"], e["zg"])), Df
def sigma_coll(tag, M):
    """Msun/pc^2: Delta rho_m(z_f) r_f for the half-mass object (frozen convention)."""
    zf, Df = zform(tag, M); e = EPS[tag]; rho = DELTA * e["rhom0"] * (1 + zf) ** 3          # Msun/Mpc^3
    rf = (3 * (M / 2) / (4 * math.pi * rho)) ** (1 / 3)                                      # Mpc
    return rho * rf / 1e12, zf, Df                                                          # Msun/Mpc^2 -> Msun/pc^2
k2 = all(abs(EPS[t]["s8"] - EPS[t]["s8F3"]) <= 1e-3 for t in EPS)
P(f"K2 EM1 sigma8 own vs F3: " + ", ".join(f"{t} {EPS[t]['s8']:.5f}/{EPS[t]['s8F3']:.5f}" for t in EPS) + f": {'PASS' if k2 else 'FAIL'}"); checks.append(("K2", k2))
# K1 EPS
Mt = 1e12; zt, Dt = zform("A_c2b_refit", Mt); e = EPS["A_c2b_refit"]
S = math.sqrt(float(np.interp(math.log10(Mt / 2), e["lMg"], e["s2"])) - float(np.interp(math.log10(Mt), e["lMg"], e["s2"])))
resid = abs(DC / float(np.interp(zt, e["zg"], e["Dg"])) - (DC + OMEGA * S)) if Dt < 1 else float("inf")
k1e = (0 < Dt <= 1.0) and resid < 1e-3
P(f"K1 EPS: M 1e12 -> z_f {zt:.3f}, D(z_f) {Dt:.4f} (in (0,1]: {0 < Dt <= 1}), equation residual {resid:.2e}: {'PASS' if k1e else 'FAIL'}")
checks[[c[0] for c in checks].index("K1")] = ("K1", dict(checks)["K1"] and k1e)
# K1 eta + mass match
k1a = abs(ETA - 14.83) < 1e-2
Mf_, rf_ = 1.0, 1.0; x0 = 1 / CF; r0_ = rf_ * x0; rho0r0 = ETA * 3 * Mf_ / (4 * math.pi * rf_ ** 2)
Mburk = math.pi * (rho0r0 / r0_) * r0_ ** 3 * B1; Minf = Mf_ * x0 ** (3 - GAM)
k1b = abs(Mburk / Minf - 1) < 1e-10
P(f"K1 eta = {ETA:.4f} (14.83: {k1a}); Burkert vs infall mass at r0 = r_f/c_f: {Mburk / Minf - 1:+.2e} ({k1b})")
checks[[c[0] for c in checks].index("K1")] = ("K1", dict(checks)["K1"] and k1a and k1b)
P("Sigma_coll table (bg A): " + "; ".join(f"M 1e{l}: {sigma_coll('A_c2b_refit', 10.0 ** l)[0]:.1f} Msun/pc^2 (z_f {sigma_coll('A_c2b_refit', 10.0 ** l)[1]:.2f})" for l in (11, 12, 13, 14, 15)))
ls_ = [math.log10(sigma_coll("A_c2b_refit", 10.0 ** l)[0]) for l in (13, 15)]
P(f"  log slope dlnSigma_coll/dlnM over 1e13-1e15: {(ls_[1] - ls_[0]) / 2:.3f} (X40b requires 0.25-0.30)")
k2t = abs(sigma_coll("A_c2b_refit", 1e12)[0] - 6.8) < 0.06
P(f"K2b X41 table reproduced (1e12 -> {sigma_coll('A_c2b_refit', 1e12)[0]:.2f}, X41 6.8): {'PASS' if k2t else 'FAIL'}"); checks.append(("K2b", k2t))
for f_ in ("canonical", "alt"):
    lx = brentq(lambda l: ETA * sigma_coll("A_c2b_refit", 10 ** l)[0] - SIG_PC[f_], 9.0, 16.0)
    P(f"  crossover eta Sigma_coll = Sigma_a0 [{f_}]: M = 10^{lx:.2f} Msun")
RES["sigma_coll_table"] = {f"1e{l}": sigma_coll("A_c2b_refit", 10.0 ** l)[:2] for l in (11, 12, 13, 14, 15)}

# ------------------------------------------------------------------ SPARC
EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
F3 = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
BGS = {t: dict(a=EM1J["rows"][t]["R1"]["a"], b=EM1J["rows"][t]["R1"]["b"], h=F3[t]["params"]["h"]) for t in ("A_c2b_refit", "B_cfg886_bg")}
ETA_USE = {'v': ETA}
def sig_core(f, tag, M, rule=True):
    s = SIG[f]
    if not rule: return s, False
    sc = ((4.0 / (3.0 * float(B(1.0))) * cf_of(M) ** 1.25) if ETA_USE["v"] == ETA else ETA_USE["v"]) * sigma_coll(tag, M)[0] * MSUNE / PC2
    return max(s, sc), sc > s
def sparc(f, tag, rule=True):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); rows = []; act = 0
    for q in GALS:
        lM = bg["a"] + bg["b"] * (q["lMb"] - 10); M200 = 10 ** lM; R200 = (3 * M200 * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)
        s, a_ = sig_core(f, tag, M200, rule); act += a_
        r0 = solve_r0(M200 * MSUNE, R200, s); Mh = math.pi * s * r0 ** 2 * B(q["Rm"] / r0)
        rows.append(fit_one(q, np.log10(np.maximum(q["GB"] + (GE * Mh / q["Rm"] ** 2)[:, None], 1e-300))))
    st = pooled([r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows]); st["n_active"] = int(act); return st
O_, P_, A_, DS_, KG, RF, SB, DAT = (NX[k] for k in ("offset_floor", "project_floor", "at_bins", "dsig_from_sig", "KG_PC2", "redfac", "sig_bins", "DAT"))
def dvecN(i, foot, hk, Msrc):
    pp = prep(i, foot, hk); rho = np.gradient(Msrc, RM) / (4 * np.pi * RM ** 2)
    So = O_(P_(rho), pp["dmpc"]); Pp = A_(DS_(So)) / KG; fr, _ = RF(hk, i, SB(So)); return DAT[hk]["W"][i] * (Pp * fr)
def grade_clusters(foot, rule=True, tag="A_c2b_refit"):
    out = {}; act = 0; ratios = []
    for hk in HK:
        V = np.zeros((N, 8))
        for i in ALLI:
            pp = prep(int(i), foot, hk); Mtot = (pp["Mfair"] + float(pp["Mb"][-1])) / MSUNE
            s, a_ = sig_core(foot, tag, Mtot, rule); act += a_; ratios.append(sigma_coll(tag, Mtot)[0] * MSUNE / PC2 / SIG[foot])
            r0 = solve_r0(pp["Mfair"], pp["rta"], s); Mh = math.pi * s * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0)
            V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)
        PREP.clear()
        cl = f"{foot}|{hk}"; o = M[cl]; vB = bsum(V); vC = bsum(DC_[(foot, hk)]); kt, ktC = vB[I], vC[I]; g = {}
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
    keys = list(out["h0672"]); ok = {k: all(abs(out[hk][k]["Z"]) <= 2 for hk in HK) for k in keys}
    bad = [k for k in keys if not ok[k]]
    sgn = {k: ("OVER" if out["h0672"][k]["pred"] > out["h0672"][k]["meas"] else "UNDER") for k in bad}
    return dict(cells=out, ok=ok, fails=[f"{k} ({sgn[k]})" for k in bad], n_active=int(act), ratio_median=float(np.median(ratios)), ratio_max=float(np.max(ratios)))
DC_ = NX["DC"]
st0 = sparc("canonical", "A_c2b_refit", rule=False); g0 = grade_clusters("canonical", rule=False)
k0 = abs(st0["rms"] - 0.0795) < 1e-4 and abs(g0["cells"]["h0672"]["G-OUT-all"]["pred"] - 0.697) < 1e-3
P(f"K0 rule forced to Sigma_a0 reproduces X38: SPARC {st0['rms']:.4f} (0.0795), OUTER {g0['cells']['h0672']['G-OUT-all']['pred']:.3f} (0.697): {'PASS' if k0 else 'FAIL'}")
checks.append(("K0x38", k0))
# ------------------------------------------------------------------ groups (P4 T3's estimator, read-only, as X40b)
REPO = os.path.dirname(REB)
P4SRC = open(os.path.join(REB, "P4_v3_galaxy_tiles", "p4_v3_galaxy_tiles.py")).read()
NSG = {"np": np, "math": math}
exec(P4SRC[P4SRC.index("G540, MSUN540, KPC540 = "):P4SRC.index('if want("T3")')], NSG)
G540, MS540, KP540, HERN_RE, XG, LXG, RHO_H, M_H = (NSG[k] for k in ("G540", "MSUN540", "KPC540", "HERN_RE", "XG", "LXG", "RHO_H", "M_H"))
TIAN = os.path.join(os.path.dirname(REPO), "_external_data", "vizier2026", "J_A_A_710_L39.tsv")
GROUPS = []
for l in open(TIAN):
    if l.startswith("#"): continue
    r = l.rstrip("\n").split("\t")
    if len(r) < 13 or not r[0].strip().isdigit() or r[1].strip() != "Galaxy group": continue
    GROUPS.append(dict(id=r[2].strip(), ls=float(r[5]), els=float(r[6]), lM=float(r[7]), elM=float(r[8]), Re=float(r[10])))
def group_logsig(o, foot, dlM=0.0, halo=True, ret_a=False):
    lMb = o["lM"] + dlM; Mb = 10 ** lMb * MS540; a = o["Re"] * KP540 / HERN_RE
    bg = BGS["A_c2b_refit"]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * G540)
    M200 = 10 ** (bg["a"] + bg["b"] * (lMb - 10)) * MS540; R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
    gN = M_H / XG ** 2; act = False
    if halo:
        sc, act = sig_core(foot, "A_c2b_refit", M200 / MSUNE)
        r0 = solve_r0(M200, R200, sc); rr = XG * a
        Mh = math.pi * sc * r0 ** 2 * B(np.minimum(rr, R200) / r0); gN = gN + Mh / Mb / XG ** 2
    s2 = float(np.trapz(4 * np.pi * XG ** 2 * RHO_H * XG * gN * XG, LXG) / 3.0) * G540 * Mb / a
    v = 0.5 * math.log10(s2) - 3.0
    return (v, act) if ret_a else v
def grade_groups(foot):
    d, sl, na = [], [], 0
    for o in GROUPS:
        v, a_ = group_logsig(o, foot, ret_a=True); na += a_
        sp = (group_logsig(o, foot, 0.01) - group_logsig(o, foot, -0.01)) / 0.02
        d.append(o["ls"] - v); sl.append(sp)
    st = NSG["class_stats"](d, sl); st["PASS"] = st["verdict"] == "CONSISTENT"; st["n_active"] = int(na); return st
k4n = max(abs(group_logsig(o, "canonical", halo=False) - NSG["group_logsig"](o, A0["canonical"], lambda y: np.ones_like(np.asarray(y, float)))) for o in GROUPS)
k4 = len(GROUPS) == 63 and k4n < 1e-4
P(f"K4 groups: {len(GROUPS)} rows; no-halo integrator vs P4 (nu = 1) max |d| {k4n:.1e} dex: {'PASS' if k4 else 'FAIL'}"); checks.append(("K4", k4))
ETA_USE["v"] = 0.0; g38 = grade_groups("canonical"); ETA_USE["v"] = ETA
X43J = json.load(open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core_results.json")))
def x43_diff():
    d = 0.0
    for f_ in FEET:
        xf = X43J["footings"][f_]
        for t_ in BGS: d = max(d, abs(sparc(f_, t_)["rms"] - xf["sparc"][t_]["rms"]))
        d = max(d, abs(grade_groups(f_)["Z"] - xf["groups"]["Z"]))
        gcx = grade_clusters(f_)
        for hk_ in HK:
            for k_, c_ in gcx["cells"][hk_].items(): d = max(d, abs(c_["pred"] - xf["clusters"]["cells"][hk_][k_]["pred"]))
    return d
dk0 = x43_diff() if FSTAR == 0.20 else 0.0; k0x43 = dk0 < 1e-6
P(f"K0x43 Burkert shape reproduces X43 (SPARC, groups, all cluster preds, both footings): max |d| {dk0:.1e}: {'PASS' if k0x43 else 'FAIL'}")
checks.append(("K0x43", k0x43))
if not MUTATE and SHAPEREQ == "S":
    SHAPE["s"] = "S"
    BS1 = float(B(1.0)); ETA = eta_of(CF); ETA_USE["v"] = ETA
    r0t, Rt, St = 3.0857e19, 10 * 3.0857e19, SIG["canonical"]
    qM = quad(lambda r: 4 * math.pi * r * r * rho_shape(r, r0t, St / r0t), 0, Rt, epsabs=0, epsrel=1e-12, limit=400)[0]
    cM = math.pi * St * r0t ** 2 * float(B(Rt / r0t))
    Mt_, R2_ = 1e11 * MSUNE, 3.0e21; r0s_ = solve_r0(Mt_, R2_, St)
    k1s = abs(cM / qM - 1) < 1e-6 and abs(math.pi * St * r0s_ ** 2 * float(B(R2_ / r0s_)) / Mt_ - 1) < 1e-8 and abs(ETA - 14.8286 * B1 / BS1) < 1e-3 * 14.8 and abs(BS1 - 0.69707) < 1e-5
    P(f"K1 smooth shape: B_S vs quadrature {cM / qM - 1:+.1e}; solved r0 mass {math.pi * St * r0s_ ** 2 * float(B(R2_ / r0s_)) / Mt_ - 1:+.1e}; B_S(1) {BS1:.5f}; eta_S {ETA:.4f}: {'PASS' if k1s else 'FAIL'}")
    checks.append(("K1smooth", k1s))
else:
    P("MUTATE: Burkert shape kept for the graded run (must equal X43)")
P(f"  X38 groups (eta = 0) canonical: mean {g38['mean']:+.4f} Z {g38['Z']:+.2f} (X40b: +0.097, +2.48)")

for f in FEET:
    P(f"\n=== [{f}] Sigma_a0 {SIG_PC[f]:.1f} Msun/pc^2")
    sp_ = {t: sparc(f, t) for t in BGS}
    for t, st in sp_.items():
        st["line"] = line(st)
        P(f"  SPARC [{t}]: rms {st['rms']:.4f}, median U {st['U_median']:.2f}, line {'PASS' if st['line'] else 'FAIL'}; rule active in {st['n_active']}/{len(GALS)} galaxies")
    gr = grade_groups(f)
    P(f"  groups (63, P4 estimator): mean {gr['mean']:+.4f} Z {gr['Z']:+.2f} -> {gr['verdict']}; rule active in {gr['n_active']}/63 (X38: mean +0.097, Z +2.48)")
    gc = grade_clusters(f)
    P(f"  clusters: rule active in {gc['n_active']}/{2 * N} cluster-cells; Sigma_coll/Sigma_a0 median {gc['ratio_median']:.3f}, max {gc['ratio_max']:.3f}")
    c0 = gc["cells"]["h0672"]
    for k in c0:
        P(f"     {k:10s} meas {c0[k]['meas']:+.3f}+-{c0[k]['s']:.3f} pred {c0[k]['pred']:+.3f} Z {c0[k]['Z']:+.2f}" + ("" if gc["ok"][k] else "  FAIL"))
    spass = all(st["line"] for st in sp_.values()); cpass = not gc["fails"]; gpass = gr["PASS"]
    det = ([] if spass else ["SPARC line"]) + ([] if gpass else [f"groups ({gr['verdict']}, Z {gr['Z']:+.2f})"]) + gc["fails"]
    v = ("SC PASSES" if not det else "SC FAILS") + " [c_f EXTERNAL]"
    rep = {}
    xf = X43J["footings"][f]["clusters"]["cells"]["h0672"]
    for k in c0: P(f"     vs X43 {k:10s} Z {xf[k]['Z']:+.2f} -> {c0[k]['Z']:+.2f}")
    P(f"  vs X43 groups Z {X43J['footings'][f]['groups']['Z']:+.2f} -> {gr['Z']:+.2f}")
    if False:
        ETA_USE["v"] = 14.8286; s3 = sparc(f, "A_c2b_refit"); g3 = grade_groups(f); c3 = grade_clusters(f); ETA_USE["v"] = ETA
        rep["eta_14.83"] = dict(sparc=dict(rms=s3["rms"], line=line(s3)), groups=dict(Z=g3["Z"], verdict=g3["verdict"]), cluster_fails=c3["fails"])
        P(f"  (reported) smooth shape with eta 14.83: SPARC {s3['rms']:.4f} line {'PASS' if line(s3) else 'FAIL'}; groups Z {g3['Z']:+.2f} {g3['verdict']}; clusters fail {c3['fails'] or 'none'}")
    RES["footings"][f] = dict(sparc=sp_, groups=gr, clusters=gc, verdict=v, failing=det, reported=rep)
    P(f"  VERDICT [{f}]: {v}" + (f"  (failing: {', '.join(det)})" if det else "") + f"   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
V = {f: RES["footings"][f]["verdict"] for f in FEET}
RES["verdict"] = V["canonical"] if V["canonical"] == V["alt"] else f"UNDECIDED (footings disagree: {V})"
P(f"\n=== VERDICT (both footings): {RES['verdict']}")
checks.append(("K3", rss() < 2.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(bool(ok) for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
P(f"f* = {FSTAR}, shape {SHAPE['s']}")
for f_ in FEET:
    for hk_ in HK:
        c_ = RES["footings"][f_]["clusters"]["cells"][hk_]
        P(f"  [{f_} {hk_}] G-OUT-M3 Z {c_['G-OUT-M3']['Z']:+.2f}, G-IN-Mall Z {c_['G-IN-Mall']['Z']:+.2f}, max |Z| {max(abs(v['Z']) for v in c_.values()):.2f}, fails {[k for k, v in c_.items() if abs(v['Z']) > 2]}")
if FSTAR == 0.20 and SHAPE["s"] == "S":
    XJ = json.load(open(os.path.join(REB, "X70_smooth_core_shape", "x70_smooth_core_results.json")))
    did = max(abs(RES["footings"][f_]["clusters"]["cells"][hk_][k_]["pred"] - XJ["footings"][f_]["clusters"]["cells"][hk_][k_]["pred"])
              for f_ in FEET for hk_ in HK for k_ in XJ["footings"][f_]["clusters"]["cells"][hk_])
    P(f"K1 identity f* 0.20 reproduces X70 cluster preds: max |d| {did:.1e}: {'PASS' if did <= 1e-9 else 'FAIL'}"); RES["K1_identity"] = did
tagf = f"_{'const4' if CFSRC == 'const4' else 'A4'}{'_MUT' if CFMULT != 1 else ''}_fs{FSTAR:g}"
P("c_f table: " + ", ".join(f"1e{l:.0f}: {c:.3f}" for l, c in zip(CFLM, CFV)) + "; eta(M) at 1e12/13/14/15: " + ", ".join(f"{4.0 / (3.0 * float(B(1.0))) * cf_of(10 ** l) ** 1.25:.3f}" for l in (12, 13, 14, 15)))
if CFSRC == "const4" and CFMULT == 1 and SHAPE["s"] == "S":
    XJ = json.load(open(os.path.join(REB, "X71_smooth_core_measured_fstar", f"x71_results_fs{FSTAR:g}_S.json")))
    dd = max(abs(RES["footings"][f_]["clusters"]["cells"][hk_][k_]["pred"] - XJ["footings"][f_]["clusters"]["cells"][hk_][k_]["pred"]) for f_ in FEET for hk_ in HK for k_ in XJ["footings"][f_]["clusters"]["cells"][hk_])
    for f_ in FEET:
        dd = max(dd, abs(RES["footings"][f_]["groups"]["Z"] - XJ["footings"][f_]["groups"]["Z"]))
        for t_ in RES["footings"][f_]["sparc"]: dd = max(dd, abs(RES["footings"][f_]["sparc"][t_]["rms"] - XJ["footings"][f_]["sparc"][t_]["rms"]))
    P(f"K1 identity (c_f == 4) reproduces X71 f* {FSTAR:g} (cluster preds, groups Z, SPARC rms): max |d| {dd:.1e}: {'PASS' if dd <= 1e-9 else 'FAIL'}"); RES["K1_identity"] = dd
open(os.path.join(HERE, f"x72{tagf}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x72_results{tagf}.json"), "w"), indent=1, default=float)
sys.exit(0 if n == len(checks) else 1)
