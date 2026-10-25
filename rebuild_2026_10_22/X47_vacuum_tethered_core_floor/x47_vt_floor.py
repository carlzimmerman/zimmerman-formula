#!/usr/bin/env python3
"""X47_vacuum_tethered_core_floor: hypothesis VT, cold dark energy binds only where its own pull exceeds g_T = (peak B/x^2 / 2) a0.

Frozen criteria: FROZEN_CRITERIA.md (bafcb4754e). EM1's machinery up to its halo-profile block (SPARC loader, fit, CLASS
backgrounds) is executed read-only in its own namespace. kappa = 1/2 FITTED; footings never pooled; route E; cold dark
energy is a gravitating field component, not matter. One thread.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x47_vt_floor.py                 -> .out, _results.json  (exit 0)
    X47_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x47_vt_floor.py    -> _MUTATE (arctan sign flipped; K0, K1 fail; exit 1)
"""
import os, sys, json, math, time, resource, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import quad

T0 = time.time()
MUTATE = os.environ.get("X47_MUTATE", "0") == "1"
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
RES = dict(frozen="bafcb4754e", mutate=MUTATE, checks={})
checks = []

# ------------------------------------------------------------------ EM1 (read-only, up to halo profiles; includes CLASS backgrounds)
EM1SRC = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); TE = open(EM1SRC).read()
codeE = TE[:TE.index("# ---------------- halo profiles")]
NE = {"__file__": EM1SRC, "__name__": "em1_ro"}; argv0 = sys.argv; sys.argv = [EM1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(codeE, EM1SRC, "exec"), NE)
sys.argv = argv0
GALS, fit_one, pooled, line, UPS, LAW, A0, BGSE = (NE[k] for k in ("GALS", "fit_one", "pooled", "line", "UPS", "LAW", "A0", "BGS"))
G, MSUN, MPC = NE["G"], NE["MSUN"], NE["MPC"]
PC = 3.0857e16; KPC = 3.0857e19; C_LIGHT = 299792458.0
FEET = ("canonical", "alt")
P(f"X47_vacuum_tethered_core_floor  {'MUTATE run (arctan sign flipped in B)' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; route E; cold dark energy = gravitating w~0 field component, not matter; not theory closed")
P(f"EM1 machinery executed read-only: {len(GALS)} SPARC galaxies [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

# ------------------------------------------------------------------ Burkert at fixed surface density (X38's conventions)
def B(x):
    x = np.asarray(x, float)
    return np.log1p(x * x) + 2 * np.log1p(x) + (2 if MUTATE else -2) * np.arctan(x)
SAT = {"n": 0}
def solve_r0(Mtot, Rout, Sig):
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(B(Rout / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10})
    lpk = float(pk.x)
    if lm(lpk) < math.log(Mtot):
        SAT["n"] += 1; return math.exp(lpk)
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), lpk, xtol=1e-14))
SIG = {f: A0[f] / (2 * math.pi * G) for f in FEET}                                     # kg/m^2
SIG_PC = {f: SIG[f] * PC ** 2 / MSUN for f in FEET}
xg = np.logspace(-3, 2, 200001); gx = B(xg) / xg ** 2
ipk = int(np.argmax(gx)); X_PK = float(minimize_scalar(lambda x: -float(B(x)) / x ** 2, bounds=(xg[max(ipk - 5, 0)], xg[ipk + 5]), method="bounded", options={"xatol": 1e-12}).x)
ZETA_A0 = float(B(X_PK)) / X_PK ** 2 / 2                                               # g_T / a0 (peak self-pull of the a0/(2 pi G) Burkert)
B1H = float(B(1.0)) / 2                                                                # self-pull at r0, / a0
GT = {f: ZETA_A0 * A0[f] for f in FEET}
LAM = 32 * math.pi * A0["canonical"] ** 2 / C_LIGHT ** 4                                # canonical footing: a0 = c^2 sqrt(Lambda / 32 pi)
ZETA = ZETA_A0 / math.sqrt(32 * math.pi)
P(f"Sigma_a0 = a0/(2 pi G): canonical {SIG_PC['canonical']:.2f}, alt {SIG_PC['alt']:.2f} Msun/pc^2")
P(f"Burkert self-pull at fixed Sigma: g(x) = (a0/2) B(x)/x^2; peak at x_pk {X_PK:.5f}: g_pk/a0 {ZETA_A0:.6f}; at r0 B(1)/2 {B1H:.6f} (peak/r0 - 1 = {ZETA_A0 / B1H - 1:+.2e})")
P(f"g_T = {ZETA_A0:.6f} a0 = canonical {GT['canonical']:.4e}, alt {GT['alt']:.4e} m/s^2; zeta = g_T/(c^2 sqrt Lambda) = {ZETA:.6f} (canonical footing, "
  f"Lambda = 32 pi a0^2/c^4 = {LAM:.4e} m^-2; the alt footing's a0 is set by rho_total, so there g_T = {ZETA_A0:.6f} a0_alt)")
RES["g_T"] = dict(zeta_over_a0=ZETA_A0, B1_half=B1H, x_pk=X_PK, g_T_m_s2=GT, zeta_c2sqrtLambda_canonical=ZETA, Lambda_canonical_m2=LAM, Sigma_a0_Msun_pc2=SIG_PC)

# ------------------------------------------------------------------ STEP 0 (stop rule)
X38J = json.load(open(os.path.join(REB, "X38_a0_surface_density_halos", "x38_sd_halos_results.json")))
X40bout = open(os.path.join(REB, "X40b_core_surface_density_scaling", "x40b_sd_scaling.out")).read()
EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
F3 = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
BGS = {t: dict(a=EM1J["rows"][t]["R1"]["a"], b=EM1J["rows"][t]["R1"]["b"], h=F3[t]["params"]["h"]) for t in ("A_c2b_refit", "B_cfg886_bg")}
def m200_r200(q, a, b, h):
    rc = 3 * (100 * h * 1e3 / MPC) ** 2 / (8 * math.pi * G)
    M200 = 10 ** (a + b * (q["lMb"] - 10)) * MSUN
    return M200, (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
def sparc(f, a, b, h):
    rows = []
    for q in GALS:
        M200, R200 = m200_r200(q, a, b, h)
        r0 = solve_r0(M200, R200, SIG[f]); gh = G * math.pi * SIG[f] * r0 ** 2 * B(q["Rm"] / r0) / q["Rm"] ** 2
        rows.append(fit_one(q, np.log10(np.maximum(q["GB"] + gh[:, None], 1e-300))))
    return pooled([r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows])
s0 = []; maxd = 0.0
for f in FEET:
    for t, bg in BGS.items():
        st = sparc(f, bg["a"], bg["b"], bg["h"]); ref = X38J["footings"][f]["sparc"][t]
        d = abs(st["rms"] - ref["rms"]); maxd = max(maxd, d)
        s0.append(d <= 1e-6 and st["U_median"] == ref["U_median"])
        P(f"S0a X38 SPARC [{f}|{t}]: rms {st['rms']:.8f} (X38 {ref['rms']:.8f}, |d| {d:.1e}); median U {st['U_median']:.2f} (X38 {ref['U_median']:.2f})")
k0 = all(s0)
P(f"K0 (S0a) X38 SPARC reproduced: max |d rms| {maxd:.1e}: {'PASS' if k0 else 'FAIL'}"); checks.append(("K0", k0))
b1_x40b = float(X40bout.split("B(1) ")[1].split()[0])
r0t, Rt = KPC, 10 * KPC; rho0 = SIG["canonical"] / r0t
quadM = quad(lambda r: 4 * math.pi * r * r * rho0 * r0t ** 3 / ((r + r0t) * (r * r + r0t * r0t)), 0, Rt, epsabs=0, epsrel=1e-12, limit=400)[0]
cfM = math.pi * SIG["canonical"] * r0t ** 2 * float(B(Rt / r0t))
k1 = abs(B1H - b1_x40b / 2) < 1e-5 and abs(cfM / quadM - 1) < 1e-6
P(f"K1 (S0b) B(1)/2 {B1H:.6f} vs X40b B(1)/2 {b1_x40b / 2:.6f}; Burkert closed form vs quadrature {cfM / quadM - 1:+.2e}: {'PASS' if k1 else 'FAIL'}")
checks.append(("K1", k1))
STOP = not (k0 and k1)
if STOP:
    P("STEP 0 FAILED -> STOP; verdict UNDECIDED (frozen stop rule)")

# ------------------------------------------------------------------ TASK 2a: sympy profile dependence
P("\n=== TASK 2a: floor condition 'peak self-pull = g_T' for cored profiles (sympy, PYTHONHASHSEED=0)")
x = sp.symbols("x", positive=True)
prof = {
    "Burkert": (1 / ((1 + x) * (1 + x ** 2)), sp.pi * (sp.log(1 + x ** 2) + 2 * sp.log(1 + x) + (2 if MUTATE else -2) * sp.atan(x))),
    "pseudo-isothermal": (1 / (1 + x ** 2), 4 * sp.pi * (x - sp.atan(x))),
}
for n in (2, 3, 4):
    y = x ** sp.Rational(1, n)
    prof[f"Einasto n={n}"] = (sp.exp(-y), sp.expand_func(4 * sp.pi * n * sp.lowergamma(3 * n, y)))
X14 = {"Burkert": sp.Integer(1), "pseudo-isothermal": sp.sqrt(3)}
for n in (2, 3, 4): X14[f"Einasto n={n}"] = sp.log(4) ** n
PROJ = {"Burkert": sp.pi / 2, "pseudo-isothermal": sp.pi}
for n in (2, 3, 4): PROJ[f"Einasto n={n}"] = 2 * sp.factorial(n)
mp.mp.dps = 30
T2A = {}; k2 = True
for name, (rho, Mt) in prof.items():
    res = sp.simplify(sp.diff(Mt, x) - 4 * sp.pi * x ** 2 * rho)
    ok = res == 0
    if not ok:      # fall back to high-precision numeric zero test at 7 points (disclosed in output)
        ok = all(abs(complex(sp.N(res.subs(x, v), 30))) < 1e-25 for v in (0.01, 0.1, 0.5, 1, 2, 7, 30))
    k2 &= bool(ok)
    gfun = sp.lambdify(x, Mt / x ** 2, "mpmath")
    dg = sp.lambdify(x, sp.diff(Mt / x ** 2, x), "mpmath")
    grid = [mp.mpf(10) ** (mp.mpf(i) / 50 - 3) for i in range(0, 301)]
    vals = [gfun(v) for v in grid]; i = max(range(len(vals)), key=lambda j: vals[j])
    try:
        xpk = mp.findroot(dg, grid[i])
    except ValueError:             # no interior peak (only reachable in the MUTATE run, where g diverges at x -> 0): grid max, check fails
        xpk = grid[i]; ok = False; k2 = False
    C = gfun(xpk)                                     # g_pk = C * G rho0 r_s
    x14 = float(X14[name]); proj = float(PROJ[name])
    # Sigma conventions for g_pk = g_T, in units of Sigma_a0 = a0/(2 pi G):  rho0 r_s = g_T/(G C)
    rs_unit = float(ZETA_A0 * 2 * mp.pi / C)          # rho0 r_s / Sigma_a0
    T2A[name] = dict(dMdx_check=bool(ok), symbolic_exact=bool(res == 0), x_pk=float(xpk), C=float(C), x_quarter=x14,
                     rho0_rquarter_over_Sigma_a0=rs_unit * x14, Sigma_proj0_over_Sigma_a0=rs_unit * proj,
                     mean_enclosed_at_rpk_over_Sigma_a0=float(ZETA_A0 * 2))
    P(f"  {name:18s} dM/dx = 4 pi x^2 rho: {'exact' if res == 0 else ('numeric' if ok else 'FAIL')}; x_pk {float(xpk):.4f}; g_pk = {float(C):.5f} G rho0 r_s; "
      f"rho0 r_1/4 = {rs_unit * x14:.3f} Sigma_a0 ({rs_unit * x14 * SIG_PC['canonical']:.1f} / {rs_unit * x14 * SIG_PC['alt']:.1f} Msun/pc^2); "
      f"Sigma_proj(0) = {rs_unit * proj:.3f} Sigma_a0; M(<r_pk)/(pi r_pk^2) = {ZETA_A0 * 2:.4f} Sigma_a0 (identity)")
P(f"K2 sympy dM/dx = 4 pi x^2 rho for all five profiles: {'PASS' if k2 else 'FAIL'}"); checks.append(("K2", k2))
RES["task2a"] = T2A
sp_r = [T2A[k]["rho0_rquarter_over_Sigma_a0"] for k in T2A]
P(f"  spread of rho0 r_1/4 across shapes: {min(sp_r):.3f}-{max(sp_r):.3f} Sigma_a0 ({math.log10(max(sp_r) / min(sp_r)):.2f} dex). "
  "For any fixed-shape family g_pk = C G rho0 r_s, so the floor <=> constant Sigma by dimensional analysis: a restatement of X38, not a result.")

# ------------------------------------------------------------------ TASK 2b: SPARC per-galaxy free Sigma
P("\n=== TASK 2b: SPARC, per-galaxy free Sigma (X38's own g(r0) = g_T for every galaxy BY CONSTRUCTION; not a test)")
LS = np.round(np.arange(-1.5, 1.5001, 0.02), 2)
iu05 = int(np.argmin(np.abs(UPS - 0.50)))
bgA = BGS["A_c2b_refit"]
T2B = {}
for f in FEET:
    best_free, best_05, frac_below = [], [], []
    for q in GALS:
        M200, R200 = m200_r200(q, bgA["a"], bgA["b"], bgA["h"])
        lg = []
        for l in LS:
            Sg = SIG[f] * 10 ** l; r0 = solve_r0(M200, R200, Sg)
            gh = G * math.pi * Sg * r0 ** 2 * B(q["Rm"] / r0) / q["Rm"] ** 2
            lg.append(np.log10(np.maximum(q["GB"] + gh[:, None], 1e-300)))
        lg = np.array(lg)                                                            # (nS, n, nU)
        OK, W = q["OK"], q["W"]
        r = np.where(OK[None], np.log10(q["GO"])[None, :, None] - lg, 0.0); Wm = np.where(OK, W[:, None], 0.0)[None]
        mse = (Wm * r * r).sum(1) / np.maximum(Wm.sum(1), 1e-300)                 # (nS, nU)
        best_free.append(float(LS[np.argmin(mse.min(1))]))
        best_05.append(float(LS[np.argmin(mse[:, iu05])]))
        # D3: X38 halo (Sigma_a0) mass inside R_last with g_h < g_T
        r0 = solve_r0(M200, R200, SIG[f]); Rl = float(q["Rm"].max())
        xs = np.linspace(1e-6, Rl / r0, 4001); gq = (A0[f] / 2) * B(xs) / xs ** 2
        dm = 4 * np.pi * xs ** 2 / ((1 + xs) * (1 + xs ** 2))
        frac_below.append(float(np.trapz(dm * (gq < GT[f]), xs) / np.trapz(dm, xs)))
    SAT["n"] = 0
    out = {}
    for lab, arr in (("U_free", np.array(best_free)), ("U_0.50", np.array(best_05))):
        con = (arr > LS[0] + 0.1) & (arr < LS[-1] - 0.1); a = arr[con]
        p16, p50, p84 = np.percentile(a, [16, 50, 84])
        out[lab] = dict(N_all=int(arr.size), N_constrained=int(con.sum()), median_dex=float(p50), p16=float(p16), p84=float(p84),
                        halfwidth_dex=float((p84 - p16) / 2), frac_below_m030=float(np.mean(a < -0.30)), frac_above_p030=float(np.mean(a > 0.30)),
                        frac_within_015=float(np.mean(np.abs(a) <= 0.15)), centred=bool(abs(p50) <= 0.15), narrow=bool((p84 - p16) / 2 <= 0.25))
        o = out[lab]
        P(f"  [{f}] {lab}: constrained {o['N_constrained']}/{o['N_all']}; log10(g(r0)/g_T) median {o['median_dex']:+.3f} [16-84 {o['p16']:+.2f}, {o['p84']:+.2f}], "
          f"half-width {o['halfwidth_dex']:.2f} dex; below -0.30: {o['frac_below_m030']:.3f}; above +0.30: {o['frac_above_p030']:.3f}; within 0.15: {o['frac_within_015']:.3f}"
          f" -> centred {o['centred']}, narrow {o['narrow']}")
    d1 = out["U_free"]["frac_below_m030"] <= 1 / 3
    fb = np.array(frac_below)
    d3 = float(np.median(fb)) <= 0.5
    out["D1_pass"] = bool(d1); out["D3_median_frac_mass_below_gT"] = float(np.median(fb)); out["D3_min"] = float(fb.min()); out["D3_pass"] = bool(d3)
    P(f"  [{f}] D1 (floor: <= 1/3 of constrained cores below -0.30 dex): {'PASS' if d1 else 'FAIL'}")
    P(f"  [{f}] D3 (VT-L self-consistency): X38 halo mass inside R_last with g_h < g_T: median {np.median(fb):.4f}, min {fb.min():.4f} -> {'PASS' if d3 else 'FAIL'}"
      f"  (analytic: g_T is the halo's own peak, so g_h <= g_T at every radius)")
    T2B[f] = out
RES["task2b"] = T2B
# context (PROVISIONAL / EXTERNAL), never in a verdict
G09 = 72.0; G09lo, G09hi = 45.0, 114.0
gG = {k: math.pi * G * v * MSUN / PC ** 2 for k, v in (("c", G09), ("lo", G09lo), ("hi", G09hi))}
li = 176.8
P(f"  context PROVISIONAL Gentile+2009 (transcribed in CFG4_galaxy_law.py): <Sigma>(<r0) = 72 (+42/-27) -> g(r0) = pi G <Sigma> = {gG['c']:.3e} [{gG['lo']:.2e}, {gG['hi']:.2e}] m/s^2"
  f" = {gG['c'] / GT['canonical']:.2f} / {gG['c'] / GT['alt']:.2f} g_T (canonical / alt)")
P(f"  context EXTERNAL Li+2020 Burkert fits (record h5_h95_h58.out, F25): rho0 r0 median {li} Msun/pc^2 (scatter 0.452 dex) -> g(r0)/g_T = {li / SIG_PC['canonical']:.2f} / {li / SIG_PC['alt']:.2f}")
RES["context"] = dict(Gentile09_g_r0=gG, Gentile09_over_gT={f: gG["c"] / GT[f] for f in FEET}, Li2020_over_gT={f: li / SIG_PC[f] for f in FEET})

# ------------------------------------------------------------------ TASK 3: D-T premises (sympy)
P("\n=== TASK 3: theorem D-T (CFG941 DERIVATION 1.3)")
gN, u, a0s, c2, K, rho = sp.symbols("g_N u a_0 c_2 K rho_c", positive=True)
g_ = gN + u
lawsol = sp.solve(sp.Eq(gN, g_ ** 2 / (g_ + a0s)), gN)
Fu = [sp.simplify(g_.subs(gN, s_)) for s_ in lawsol]
dt1 = any(sp.simplify(F_ - a0s * u / (a0s - u)) == 0 for F_ in Fu)
selfcoef = sp.expand((1 - c2) * K * rho)
P(f"  DT1 reproduced: tether force F(u) = g with the law imposed -> {Fu} ; equals a0 u/(a0 - u): {dt1}")
P(f"  linear self-gravity coefficient of a tethered medium: {selfcoef} -> 0 at c2 = 1 (D-T), full K rho_c at c2 = 0 (no tether)")
RES["task3"] = dict(DT1_reproduced=bool(dt1), selfgravity_coefficient=str(selfcoef))

# ------------------------------------------------------------------ TASK 4: linear self-acceleration vs g_T
P("\n=== TASK 4: linear self-acceleration of the cold sector vs g_T")
P(f"  EM1 KC (CLASS sigma8 vs F3): {NE['RES']['checks']['KC']['value']}")
k3 = bool(NE["RES"]["checks"]["KC"]["ok"]); checks.append(("K3", k3))
KG = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0]; ZG = [0, 0.5, 1, 2, 3, 5, 10, 30]
J223 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG223_a0_over_cosmic_time", "cfg223_results.json")))
ZC = np.array(J223["curves"]["z"], float); MDEC = np.array(J223["curves"]["M-DEC"], float)
mdec = lambda z: float(np.interp(z, ZC, MDEC))
T4 = {}
for t in BGS:
    bg = BGSE[t]; cc = bg["c"]; h = bg["h"]; p = F3[t]["params"]
    kk, Pk = bg["cB"].__defaults__[1].__defaults__[0], bg["cB"].__defaults__[1].__defaults__[1]
    D2 = kk ** 3 * Pk / (2 * math.pi ** 2)
    rhoc0 = p["omega_cdm"] * 3 * (100e3 / MPC) ** 2 / (8 * math.pi * G)
    rhom0 = (p["omega_cdm"] + p["omega_b"]) * 3 * (100e3 / MPC) ** 2 / (8 * math.pi * G)
    D = lambda z: cc.scale_independent_growth_factor(z) / cc.scale_independent_growth_factor(0.0)
    def gk(k, z, rho0=rhoc0):
        d2 = float(np.exp(np.interp(math.log(k), np.log(kk), np.log(D2))))
        return 4 * math.pi * G * rho0 * (1 + z) ** 2 * D(z) * math.sqrt(d2) / (k * h / MPC)
    def gcum(z, kmin=0.01, rho0=rhoc0):
        w = kk >= kmin; kp = kk[w] * h / MPC
        return 4 * math.pi * G * rho0 * (1 + z) ** 2 * D(z) * math.sqrt(np.trapz(D2[w] / kp ** 2, np.log(kk[w])))
    tab = {}
    for z in ZG:
        tab[str(z)] = {str(k): gk(k, z) for k in KG}; tab[str(z)]["cum"] = gcum(z)
    T4[t] = dict(table_m_s2=tab)
    for f in FEET:
        worst = max(3 * tab[str(z)][str(k)] / GT[f] for z in ZG if z <= 3 for k in KG)
        # z_cross: nu * g_k(z) = g_T, scanning z up to 3000
        zs = np.concatenate([np.linspace(0, 30, 301), np.logspace(math.log10(31), math.log10(3000), 300)])
        Dz = np.array([D(z) for z in zs])
        zc = {}
        for nu in (1, 3):
            zc[nu] = {}
            for k in KG:
                d2 = float(np.exp(np.interp(math.log(k), np.log(kk), np.log(D2))))
                gz = nu * 4 * math.pi * G * rhoc0 * (1 + zs) ** 2 * Dz * math.sqrt(d2) / (k * h / MPC)
                above = np.where(gz >= GT[f])[0]
                zc[nu][str(k)] = float(zs[above[0]]) if above.size else None
        T4[t][f] = dict(max_nu3_ratio_z_le_3=worst, z_cross=zc, G1_pass=bool(worst >= 1.0) and all(
            3 * tab[str(z)][str(k)] >= GT[f] for z in ZG if z <= 3 for k in KG))
        P(f"  [{t}|{f}] g_T {GT[f]:.3e}; largest nu=3 linear g_k/g_T over k 0.01-10, z <= 3: {worst:.4f} -> G1 {'PASS' if T4[t][f]['G1_pass'] else 'FAIL'}")
        P(f"     z_cross (nu=1 g_k = g_T, tether OFF above): " + ", ".join(f"k {k}: {zc[1][str(k)]:.0f}" if zc[1][str(k)] is not None else f"k {k}: >3000" for k in KG))
        P(f"     z_cross (nu=3): " + ", ".join(f"k {k}: {zc[3][str(k)]:.0f}" if zc[3][str(k)] is not None else f"k {k}: >3000" for k in KG))
    for z in ZG:
        r_ = tab[str(z)]
        P(f"  [{t}] z {z:>4}: g_k (m/s^2) " + " ".join(f"{r_[str(k)]:.2e}" for k in KG) + f" | cum(k>=0.01) {r_['cum']:.2e} | /g_T canon {max(r_[str(k)] for k in KG) / GT['canonical']:.4f} (max k)")
    # g_T(z) with M-DEC (reported)
    T4[t]["gT_MDEC_ratio_max_z_le_3"] = {f: max(3 * tab[str(z)][str(k)] / (GT[f] * mdec(z)) for z in ZG if z <= 3 for k in KG) for f in FEET}
    P(f"  [{t}] with g_T(z) on M-DEC: largest nu=3 ratio z <= 3: canonical {T4[t]['gT_MDEC_ratio_max_z_le_3']['canonical']:.4f}, alt {T4[t]['gT_MDEC_ratio_max_z_le_3']['alt']:.4f}")
    # turnaround self-pull (cold part only), reported
    ta = {}
    for z in (0, 1, 2, 3, 5):
        for lM in (10, 11, 12, 13):
            Mt = 10 ** lM * MSUN; rho_ta = 5.55 * rhom0 * (1 + z) ** 3
            Rta = (3 * Mt / (4 * math.pi * rho_ta)) ** (1 / 3)
            ta[f"z{z}_M1e{lM}"] = G * Mt * (p["omega_cdm"] / (p["omega_cdm"] + p["omega_b"])) / Rta ** 2
    T4[t]["turnaround_cold_pull_m_s2"] = ta
    P(f"  [{t}] cold self-pull at turnaround / g_T(canonical): " + "; ".join(f"z {z}: " + "/".join(f"{ta[f'z{z}_M1e{lM}'] / GT['canonical']:.3f}" for lM in (10, 11, 12, 13)) for z in (0, 1, 2, 3, 5))
      + "  (M = 1e10/1e11/1e12/1e13 Msun)")
RES["task4"] = T4
G1 = {f: all(T4[t][f]["G1_pass"] for t in BGS) for f in FEET}

# ------------------------------------------------------------------ TASK 5: Sigma_floor(z)
P("\n=== TASK 5: Sigma_floor(z) = Sigma_a0 a0(z)/a0(0), DESI M-DEC (CFG223), reported only")
T5 = {}
for f in FEET:
    T5[f] = {str(z): dict(a0_ratio=mdec(z), Sigma_floor_Msun_pc2=SIG_PC[f] * mdec(z), g_T_m_s2=GT[f] * mdec(z),
                          Gentile_mean_Sigma_r0_Msun_pc2=SIG_PC[f] * mdec(z) * 2 * ZETA_A0) for z in (0, 0.5, 1, 2)}
    P(f"  [{f}] " + "; ".join(f"z {z}: a0 ratio {T5[f][str(z)]['a0_ratio']:.3f}, rho0 r0 {T5[f][str(z)]['Sigma_floor_Msun_pc2']:.1f} Msun/pc^2, g_T {T5[f][str(z)]['g_T_m_s2']:.3e}" for z in (0, 0.5, 1, 2)))
RES["task5"] = T5

# ------------------------------------------------------------------ verdict
checks.append(("K4", rss() < 1.0))
D1 = {f: T2B[f]["D1_pass"] for f in FEET}; D3 = {f: T2B[f]["D3_pass"] for f in FEET}
T1 = True     # premise analysis in README (D-T's always-on tether + law-as-equilibrium do not hold for dust-bound cores); sympy reproduces DT1
def vl(f):
    if STOP: return "UNDECIDED (step 0)"
    fails = ([] if G1[f] else ["growth"]) + ([] if D1[f] and D3[f] else ["data"]) + ([] if T1 else ["D-T"])
    return "VT FAILS AT " + " / ".join(fails) if fails else "VT CONSISTENT"
def vo(f):
    if STOP: return "UNDECIDED (step 0)"
    fails = ([] if D1[f] else ["data"]) + ([] if T1 else ["D-T"])
    return "VT-O FAILS AT " + " / ".join(fails) if fails else "VT-O CONSISTENT (NONLOCAL, mechanism open)"
V = {f: vl(f) for f in FEET}; VO = {f: vo(f) for f in FEET}
RES["verdict_VT_L_per_footing"] = V; RES["verdict_VT_O_per_footing"] = VO
RES["verdict"] = V["canonical"] if V["canonical"] == V["alt"] else f"UNDECIDED (footings disagree: {V})"
RES["verdict_VT_O"] = VO["canonical"] if VO["canonical"] == VO["alt"] else f"UNDECIDED (footings disagree: {VO})"
P(f"\n=== VERDICT (primary, VT-L): {RES['verdict']}   per footing {V}")
P(f"=== VT-O (reported): {RES['verdict_VT_O']}")
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(ok for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
open(os.path.join(HERE, f"x47_vt_floor{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x47_vt_floor_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if n == len(checks) else 1)
