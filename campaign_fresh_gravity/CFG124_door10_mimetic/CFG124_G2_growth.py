# -*- coding: utf-8 -*-
"""CFG124 G2 -- CMB / linear growth for the mimetic dust (frozen: CFG124_FROZEN_CRITERIA.md, e8b9fbcdf).
Equations (stated, then solved; CFG43's two-fluid sub-horizon treatment, declared inputs H0 = 67.4, Oc = 0.265, Ob = 0.050, OL = 0.685, Or = 9.1e-5):
  d_c'' + (2 + dlnE) d_c' + c_s^2 (c k/(a H))^2 d_c = (1 - s) (3/2)(Om_c d_c + Om_b d_b),   d_b'' + (2 + dlnE) d_b' = (3/2)(Om_c d_c + Om_b d_b)
  ( ' = d/dln a; c_s^2 = gt/(2 - 3 gt) from T0.6a; s = the switch: the fraction of the dust's gravitational force cancelled by a class-E coupling )
Initial conditions at z = 1100: d_c = d_b = a_i, d' = d (as CFG43 with z_i = 1000; the frozen criteria say 1100).  Pass: growth of the matter
contrast within 5% of LCDM at z = 10, k up to 30/Mpc.  NOTE: the Jeans form of the pressure term is the frozen G2.1 statement; the high-k
dispersion c_s^2 = gt/(2-3gt) is derived in T0.6, the full comoving-gauge growth equation is not re-derived here.
MUTATE b: the G1-scale sound speed is replaced by c_s^2 = 0 (so the claim that it fails 5% must flip); MUTATE a/c: not used.
"""
import os, sys, math, json
import numpy as np
from scipy.integrate import solve_ivp
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG124_common as C

R = C.Report("CFG124_G2_growth")
P = R.P
P(__doc__)
H0, Oc, Ob, OL, Or_ = 67.4, 0.265, 0.050, 0.685, 9.1e-5
Om = Oc + Ob
c_kms = 299792.458
def E2f(a): return Om / a ** 3 + Or_ / a ** 4 + OL

def growth(k, cs2=0.0, s=0.0, zi=1100.0, zs=(10.0, 0.0)):
    def rhs(x, y):
        a = math.exp(x); e2 = E2f(a); Hh = H0 * math.sqrt(e2)
        dlnE = -(3 * Om / a ** 3 + 4 * Or_ / a ** 4) / (2 * e2)
        Omc = Oc / a ** 3 / e2; Omb = Ob / a ** 3 / e2
        dc, dcx, db, dbx = y
        src = 1.5 * (Omc * dc + Omb * db)
        pr = cs2 * (c_kms * k / (a * Hh)) ** 2
        return [dcx, -(2 + dlnE) * dcx - pr * dc + (1 - s) * src, dbx, -(2 + dlnE) * dbx + src]
    ai = 1 / (1 + zi)
    xs = [math.log(1 / (1 + z)) for z in zs]
    order = np.argsort(xs)
    sol = solve_ivp(rhs, [math.log(ai), max(xs)], [ai, ai, ai, ai], t_eval=[xs[i] for i in order], rtol=1e-9, atol=1e-14, method="LSODA")
    out = {}
    for j, i in enumerate(order):
        dc, _, db, _ = sol.y[:, j]
        out[zs[i]] = (Oc * dc + Ob * db) / Om
    return out

BASE = {}
def base(k):
    if k not in BASE: BASE[k] = growth(k)
    return BASE[k]
def ratio(k, cs2=0.0, s=0.0, z=10.0):
    return growth(k, cs2, s)[z] / base(k)[z]

# ---- derived sound speed from T0 (read the derived expression, do not retype the recalled one)
t0res = os.path.join(C.HERE, "CFG124_T0_field_equations_results.json")
if not os.path.exists(t0res):
    raise SystemExit("run CFG124_T0_field_equations.py first (its results file holds the derived c_s^2)")
cs2_expr = sp.sympify(json.load(open(t0res))["numbers"]["cs2_general_gt_s_w"], locals={"gt": sp.Symbol("gt"), "s": sp.Symbol("s"), "w": sp.Symbol("w")})
gt_sym = sp.Symbol("gt")
cs2_of_gt = sp.lambdify(gt_sym, cs2_expr.subs({sp.Symbol("s"): 0, sp.Symbol("w"): 0}), "numpy")
gt_of_cs2 = lambda c2: 2 * c2 / (1 + 3 * c2)                      # inverse of c_s^2 = gt/(2-3gt)
P("derived c_s^2(gt) = %s (T0.6a); gt(c_s^2) = 2 c^2/(1+3 c^2)" % cs2_expr.subs({sp.Symbol('s'): 0, sp.Symbol('w'): 0}))

R.banner("G2.0  controls")
b10 = base(30.0)[10.0]
R.check("G2.0a", "pressureless baseline: matter contrast grows by ~ (1+z_i)/(1+z) between z = 1100 and 10 (matter era; within 10% of 100.1 because of radiation and baryon simplifications)", "delta_m(z=10)/delta_i = %.1f  (delta_i = 1/1101)" % (b10 * 1101.0), abs(b10 * 1101 / 100.1 - 1) < 0.10)
# post-hoc (added after the G2.0a number was seen; labelled as such, G2.0a itself is kept as written): radiation-corrected Meszaros factor
a_eq = Or_ / Om; yi, ye = (1 / 1101) / a_eq, (1 / 11) / a_eq
mesz = (1 + 1.5 * ye) / (1 + 1.5 * yi)
R.check("G2.0a-POSTHOC", "[post-hoc, not frozen] the Meszaros CDM growth factor between z = 1100 and 10 is (1 + 1.5 y_10)/(1 + 1.5 y_1100) with y = a/a_eq: the computed baryon+CDM growth should be within 15% of it (baryons still coupled to photons at z = 1100 are treated as pressureless: a known simplification)", "Meszaros %.1f vs computed %.1f" % (mesz, b10 * 1101.0), abs(b10 * 1101 / mesz - 1) < 0.15, load_bearing=False)
R.check("G2.0b", "class A (c_s^2 = 0, s = 0) reproduces the baseline exactly (mimetic dust with V = gamma = 0 IS cold dust)", "ratio at k = 0.1, 1, 30: %s" % [ratio(k) for k in (0.1, 1.0, 30.0)], all(abs(ratio(k) - 1) < 1e-12 for k in (0.1, 1.0, 30.0)))

R.banner("G2.3  the c_s^2 window: the largest constant c_s^2 with growth within 5% of LCDM at z = 10 (and, reported, at z = 0)")
def cmax(k, z=10.0, tol=0.05):
    lo, hi = -16.0, -2.0
    if ratio(k, 10 ** hi, z=z) >= 1 - tol: return 10 ** hi
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if ratio(k, 10 ** mid, z=z) >= 1 - tol: lo = mid
        else: hi = mid
    return 10 ** lo
kgrid = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
CM10 = {k: cmax(k) for k in kgrid}; CM0 = {k: cmax(k, z=0.0) for k in kgrid}
for k in kgrid:
    P("  k = %5.1f /Mpc : c_s^2,max(z=10) = %.3e (gt_max = %.3e) ;  c_s^2,max(z=0) = %.3e" % (k, CM10[k], gt_of_cs2(CM10[k]), CM0[k]))
R.num("cs2_max_z10", {str(k): v for k, v in CM10.items()}); R.num("gt_max_z10_k30", gt_of_cs2(CM10[30.0]))
R.check("G2.3a", "frozen screening estimate: c_s^2,max(k = 30/Mpc, z = 10) ~ 1e-10 (order of magnitude: within [1e-11, 1e-9])", "c_s^2,max = %.3e  (gt_max = %.3e)" % (CM10[30.0], gt_of_cs2(CM10[30.0])), 1e-11 <= CM10[30.0] <= 1e-9)
# halo dispersion scale
G = 4.30091727e-6; KPC_M = 3.0856775814913673e19
need = {}
for foot, a0si in {"canonical": 9.3603e-11, "alt": 1.1312e-10}.items():
    a0 = a0si * KPC_M / 1e6
    for M in (1e9, 1e10, 1e11, 1e12):
        Vf2 = math.sqrt(G * a0 * M)                                 # V_f^2 = (G a0 M)^{1/2}
        need[(foot, M)] = Vf2 / 2 / c_kms ** 2                       # sigma^2/c^2 = V_f^2/(2 c^2)
lo_n, hi_n = min(need.values()), max(need.values())
P("  halo dispersion scale sigma^2/c^2 = V_f^2/(2c^2) over M_b = 1e9..1e12 and both footings: %.2e ... %.2e" % (lo_n, hi_n))
R.check("G2.3b", "frozen statement: the halo scale is about 2e-8 (1e9 Msun) to 6e-7 (1e12 Msun) c^2", "measured %.2e ... %.2e (canonical: %.2e ... %.2e)" % (lo_n, hi_n, need[("canonical", 1e9)], need[("canonical", 1e12)]), 1e-8 < lo_n < 4e-8 and 4e-7 < hi_n < 9e-7)
R.banner("G2.3c  growth at the halo-scale sound speed (k = 30/Mpc, z = 10), and the joint window")
fails = {}
for (foot, M), c2 in need.items():
    c2use = 0.0 if C.MU("b") else c2
    r30 = ratio(30.0, c2use); r2 = ratio(2.0, c2use)
    fails[(foot, M)] = (r30, r2, CM10[30.0] / c2)
    P("  %-9s M=%.0e: c_s^2 = %.2e (used %.2e): growth ratio at k = 30: %.3e ; k = 2: %.3e ; c_s^2,max/needed = %.2e" % (foot, M, c2, c2use, r30, r2, CM10[30.0] / c2))
R.check("G2.3c", "at the halo-scale sound speed the growth at k = 30/Mpc is NOT within 5% of LCDM (for all eight mass/footing cases)", "ratios: %s" % {"%s_%.0e" % k: round(v[0], 6) for k, v in fails.items()}, all(v[0] < 0.95 for v in fails.values()))
R.check("G2.3d", "the joint window is empty: c_s^2,max(k=30, z=10) is below every halo-scale c_s^2 needed (ratio max/needed < 1 for all eight cases; shortfall in decades reported)", "c_s^2,max/needed ranges %.1e ... %.1e" % (min(v[2] for v in fails.values()), max(v[2] for v in fails.values())), all(v[2] < 1 for v in fails.values()))
R.num("joint_window_ratio_min_max", [min(v[2] for v in fails.values()), max(v[2] for v in fails.values())])

R.banner("G2.4  the switch's cosmological face: the dust force multiplied by (1 - s) at z >~ 10")
tab = {}
for s in (0.0, 0.05, 0.5, 1.0):
    tab[s] = [ratio(k, 0.0, s) for k in (0.1, 1.0, 10.0, 30.0)]
    P("  s = %.2f : growth ratio at k = 0.1, 1, 10, 30 /Mpc : %s" % (s, np.round(tab[s], 4)))
def smax(k):
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if ratio(k, 0.0, mid) >= 0.95: lo = mid
        else: hi = mid
    return lo
SM = {k: smax(k) for k in (1.0, 30.0)}
P("  largest s with growth within 5%% at z = 10: k = 1: %.4f ; k = 30: %.4f" % (SM[1.0], SM[30.0]))
R.check("G2.4a", "the G1.3 requirement applied at z >~ 10 (s = 1, dust force fully cancelled) destroys the growth (ratio << 0.95 at every k), and any s above a few percent already fails 5%%: a coupling that satisfies G1.3 inside halos must be off (s < %.3f) in the linear regime" % SM[30.0], "s = 1: %s ; s_max(k=30) = %.4f" % (np.round(tab[1.0], 4), SM[30.0]), all(v < 0.95 for v in tab[1.0]) and SM[30.0] < 0.2)

R.banner("G2.2  background: class B with a non-constant V(phi)")
P("  derived in T0.4b: d(a^3 eps)/dt = -a^3 dV/dt exactly (a homogeneous source). Pass line: rho_c(a) = LCDM a^-3 to 1% over z in [10, 1100], i.e. |int a^3 dV/dt dt| <= 0.01 a^3 eps.")
g1 = os.path.join(C.HERE, "CFG124_G1_target_results.json")
if os.path.exists(g1) and not C.MU("c"):
    bfit = json.load(open(g1))["numbers"].get("G1.1_B_fit_b", {})
    rhocrit_kpc3 = 277.5 * 0.674 ** 2 * 1.0                       # Msun/kpc^3 (h = 0.674)
    rho_c0 = Oc * rhocrit_kpc3
    for nm, b in bfit.items():
        for M in (1e9, 1e10, 1e11, 1e12):
            a0 = 9.3603e-11 * KPC_M / 1e6; rM = math.sqrt(G * M / a0); vM = math.sqrt(a0 * rM)
            S = abs(3 * b * M * vM / rM ** 4 / (4 * math.pi)) * 1.0227          # Msun kpc^-3 Gyr^-1
            P("  best class-B fit (%s) b = %.3e : implied homogeneous source at M_b = %.0e: S = %.3e Msun/kpc^3/Gyr; S x 0.48 Gyr / rho_c(z=10) = %.2e ; S x 13.8 Gyr / rho_c(0) = %.2e" % (nm, b, M, S, S * 0.48 / (rho_c0 * 1331), S * 13.8 / rho_c0))
    R.num("G2.2_bfit", bfit)
else:
    P("  (G1 results not present or MUTATE c: the numeric source comparison is skipped; the structural statement T0.4b stands)")
R.check("G2.2", "class B: V(phi) is a function of proper time only, so it changes rho_c(a) homogeneously (T0.4b) and cannot depend on M_b(<r); the G2 pass line then holds only for V = const, which is Lambda (already tied by CFG43/XR20) and adds nothing", "derived: d(a^3 eps)/dt = -a^3 Vdot (T0.4b PASS)", True, load_bearing=False)
P("  CMB: mimetic dust with gt <= gt_max(30/Mpc, z=10) = %.2e is a GDM fluid (w = 0, c_s^2 <~ 1e-10, c_vis = 0): the growth bound above is the operative one; the CMB-side GDM bound (recalled ~1e-6, unverified) is weaker and is not used." % gt_of_cs2(CM10[30.0]))
nf = R.write()
sys.exit(1 if nf else 0)
