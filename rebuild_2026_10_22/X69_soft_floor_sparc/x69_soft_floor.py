#!/usr/bin/env python3
"""X69_soft_floor_sparc: X43's SPARC grade with the floor softened by the galaxy's own peak baryonic acceleration,
Sigma_core = max(Sigma_M F(X0), eta Sigma_coll), F = 4X0/sqrt(1+16X0^2), X0 = max g_bar(Y=0.5)/a0.
Built from X43's committed script (its preamble, EM1 + X30 machinery read-only, up to the SPARC section) plus the SF grade.
Frozen criteria: FROZEN_CRITERIA.md (6c4f4537e0). One thread.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x69_soft_floor.py
    X69_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x69_soft_floor.py     # F uses 2 X0
"""
import os, sys, json, math, time, resource, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
os.environ.pop("X30_MUTATE", None)
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

T0 = time.time()
MUTATE = os.environ.get("X69_MUTATE") == "1"
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
codeX = codeX.replace(old, f'OUTF = open({os.path.join(HERE, "x69_x30_machinery" + TAG + ".log")!r}, "w")')
NX = {"__file__": X30SRC, "__name__": "x30_ro"}; sys.argv = [X30SRC]
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    exec(compile(codeX, X30SRC, "exec"), NX)
sys.argv = argv0
FEET, HK, BN, M, DC, I, TID, T3M, ALLI, N, X1m, wls1, bsum, prep, PREP, RG, RM, X7J = (NX[k] for k in (
    "FEET", "HK", "BN", "M", "DC", "I", "TID", "T3M", "ALLI", "N", "X1m", "wls1", "bsum", "prep", "PREP", "RG", "RM", "X7J"))
GX = NX["G"]
P(f"X69_soft_floor_sparc  {'MUTATE run (F uses 2 X0)' if MUTATE else 'normal run'}  [c_f EXTERNAL]")
P("kappa = 1/2 FITTED; footings never pooled; route E (Newtonian, no law force), core Sigma = max(a0/(2 pi G), eta x EPS collapse Sigma), eta from self-similar infall, c_f = 4 EXTERNAL; not theory closed")
P(f"EM1 and X30 machinery executed read-only [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

# ------------------------------------------------------------------ Burkert at fixed surface density
def B(x):
    x = np.asarray(x, float)
    return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
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
RES = dict(frozen="6c4f4537e0", mutate=MUTATE, Sigma_Msun_pc2=SIG_PC, footings={}, checks={}); checks = []

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
def eta_of(cf, gam=None): return 4.0 / (3.0 * B1) * cf ** ((GAM if gam is None else gam) - 1.0)
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
    sc = ETA_USE["v"] * sigma_coll(tag, M)[0] * MSUNE / PC2
    return max(s, sc), sc > s
def sparc(f, tag, rule=True):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); rows = []; act = 0
    for q in GALS:
        lM = bg["a"] + bg["b"] * (q["lMb"] - 10); M200 = 10 ** lM; R200 = (3 * M200 * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)
        s, a_ = sig_core(f, tag, M200, rule); act += a_
        r0 = solve_r0(M200 * MSUNE, R200, s); Mh = math.pi * s * r0 ** 2 * B(q["Rm"] / r0)
        rows.append(fit_one(q, np.log10(np.maximum(q["GB"] + (GE * Mh / q["Rm"] ** 2)[:, None], 1e-300))))
    st = pooled([r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows]); st["n_active"] = int(act); return st

# ------------------------------------------------------------------ X69: soft floor on SPARC
KF = 2.0 if MUTATE else 4.0
def Ff(X): X = np.asarray(X, float); return KF * X / np.sqrt(1 + (KF * X) ** 2)
IU5 = int(np.argmin(abs(UPS - 0.50))); assert abs(UPS[IU5] - 0.50) < 1e-9
def X0(q, f):
    g = q["GB"][:, IU5]; g = g[np.isfinite(g) & (g > 0)]
    return float(g.max() / A0[f]) if g.size else 0.0
def sparc_rows(f, tag, soft):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); rows = []
    for q in GALS:
        lM = bg["a"] + bg["b"] * (q["lMb"] - 10); M200 = 10 ** lM; R200 = (3 * M200 * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)
        sfl = SIG[f] * (float(Ff(X0(q, f))) if soft else 1.0)
        s = max(sfl, ETA * sigma_coll(tag, M200)[0] * MSUNE / PC2)
        r0 = solve_r0(M200 * MSUNE, R200, s); Mh = math.pi * s * r0 ** 2 * B(q["Rm"] / r0)
        rows.append(fit_one(q, np.log10(np.maximum(q["GB"] + (GE * Mh / q["Rm"] ** 2)[:, None], 1e-300))))
    return rows
def pool(rows, idx):
    return pooled([rows[i][0] for i in idx], [rows[i][1] for i in idx], [rows[i][2] for i in idx])
X43J = json.load(open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core_results.json")))
dk0 = 0.0; HARD = {}
for f in FEET:
    for t in BGS:
        HARD[(f, t)] = sparc_rows(f, t, False)
        dk0 = max(dk0, abs(pool(HARD[(f, t)], range(len(GALS)))["rms"] - X43J["footings"][f]["sparc"][t]["rms"]))
k0 = dk0 < 1e-6
P(f"K0 F == 1 reproduces X43 SPARC rms (both footings, both backgrounds): max |d| {dk0:.1e}: {'PASS' if k0 else 'FAIL'}")
k1 = abs(4 * 0.08 / math.sqrt(1 + 16 * 0.08 ** 2) - 0.305) < 1e-3 and abs(4 * 1e6 / math.sqrt(1 + 16e12) - 1) < 1e-9
P(f"K1 F(0.08) = {4 * 0.08 / math.sqrt(1 + 16 * 0.08 ** 2):.4f} (0.305), F(inf) -> 1: {'PASS' if k1 else 'FAIL'}")
checks = [("K0", k0), ("K1", k1)]
names = [q["name"] for q in GALS]
for f in FEET:
    xs = np.array([X0(q, f) for q in GALS]); LOW = [i for i in range(len(GALS)) if xs[i] < 0.32]; REST = [i for i in range(len(GALS)) if xs[i] >= 0.32]
    P(f"\n=== [{f}] X0 = peak g_bar(Y=0.5)/a0: median {np.median(xs):.2f}; LOW (X0 < 0.32) n = {len(LOW)}, REST n = {len(REST)}")
    P("  LOW galaxies: " + ", ".join(f"{names[i]}({xs[i]:.2f})" for i in sorted(LOW, key=lambda i: xs[i])))
    fv = {}
    for t in BGS:
        soft = sparc_rows(f, t, True); hard = HARD[(f, t)]
        A_ = pool(soft, range(len(GALS))); lh, ls = pool(hard, LOW)["rms"], pool(soft, LOW)["rms"]; rh, rs_ = pool(hard, REST)["rms"], pool(soft, REST)["rms"]
        dl, dr = ls / lh - 1, rs_ / rh - 1
        P(f"  [{t}] SF all rms {A_['rms']:.4f} U {A_['U_median']:.2f} line {'PASS' if line(A_) else 'FAIL'} (X43 {pool(hard, range(len(GALS)))['rms']:.4f}); "
          f"LOW rms {lh:.4f} -> {ls:.4f} ({100 * dl:+.1f}%); REST {rh:.4f} -> {rs_:.4f} ({100 * dr:+.1f}%)")
        per = [(names[i], (soft[i][0] / soft[i][1]) ** 0.5 - (hard[i][0] / hard[i][1]) ** 0.5, xs[i]) for i in range(len(GALS))]
        per.sort(key=lambda p: p[1])
        P("    largest improvements (d rms): " + ", ".join(f"{n} {d:+.3f} (X0 {x:.2f})" for n, d, x in per[:10]))
        P("    largest worsenings  (d rms): " + ", ".join(f"{n} {d:+.3f} (X0 {x:.2f})" for n, d, x in per[::-1][:10]))
        fv[t] = dict(line=line(A_), rms=A_["rms"], low=(lh, ls, dl), rest=(rh, rs_, dr), nlow=len(LOW))
    if all(v["line"] and v["low"][2] <= -0.05 and v["rest"][2] <= 0.02 for v in fv.values()): verd = "SOFT FLOOR PREFERRED"
    elif all(v["low"][2] >= 0.05 for v in fv.values()) or not all(v["line"] for v in fv.values()): verd = "HARD FLOOR PREFERRED"
    else: verd = "NOT DECIDED"
    P(f"  VERDICT [{f}]: {verd}")
    RES["footings"][f] = dict(per_bg=fv, verdict=verd, low=[names[i] for i in LOW])
V = {f: RES["footings"][f]["verdict"] for f in FEET}
RES["verdict"] = V["canonical"] if V["canonical"] == V["alt"] else f"UNDECIDED (footings disagree: {V})"
if MUTATE and os.path.exists(os.path.join(HERE, "x69_soft_floor_results.json")):
    NJ = json.load(open(os.path.join(HERE, "x69_soft_floor_results.json")))
    dm = max(abs(RES["footings"][f]["per_bg"][t]["low"][1] - NJ["footings"][f]["per_bg"][t]["low"][1]) for f in FEET for t in BGS)
    P(f"MUTATE sensitivity: max LOW rms change vs normal {dm:.2e} ({'sensitive' if dm > 1e-4 else 'HARNESS INSENSITIVE'})")
P(f"\n=== VERDICT (both footings): {RES['verdict']}  [c_f EXTERNAL]")
n = sum(ok for _, ok in checks); P(f"checks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s")
RES["checks"] = {k: bool(v) for k, v in checks}
open(os.path.join(HERE, f"x69_soft_floor{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x69_soft_floor_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if n == len(checks) else 1)
