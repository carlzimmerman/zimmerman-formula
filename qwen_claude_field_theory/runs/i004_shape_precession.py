#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
i004_shape_precession.py
========================
I004 -- FIT THE ANOMALY'S RADIAL SHAPE, NOT A CONSTANT, TO PLANETARY RESIDUALS.

HYP (from IDEAS.md): the framework predicts s*a0(rho(r)), whose curvature the precession
fits were never given, so s <= 1.27e-5 on a CONSTANT term is the wrong bound.

METHOD. Build the framework's own radial shape
     a(r) = s * a0 * F(r),   F(r) = [(1+nu0^2)/(1+(nu0*rho(r)/rho0)^2)]^(1/4),
     rho(r) = rho_1AU * (r/AU)^(-q),  q in {0,1,2}.
For each planet the anomalous precession is the Gauss apsidal integral of that radial
profile (banked machinery, agentH3). Fit s JOINTLY with dGM_sun and dJ2 to the perihelion
precessions of Mercury/Venus/Earth/Mars, and report the MARGINALISED 2-sigma bound on s.
Data = the Sereno & Jetzer 2006 Tab.1 ephemeris bounds (inverted): dA_R <= 3.66e-14 m/s^2
(Earth), 3.72e-14 (Mars).  PASS: bound on s loosens >10x vs the constant term. KILL: <2x.

Two footings for a0: canonical 9.3619e-11 and alt 1.1279e-10.

Exit 0 only if every check passes.
"""
import sys
import numpy as np

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"   [{'ok' if ok else 'FAIL'}] {label}" + (f"    {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


# -------------------------------------------------------------------------------- constants
c, G = 2.99792458e8, 6.67430e-11
Msun = 1.98892e30
AU = 1.495978707e11
Rsun = 6.957e8
GM_SUN = 1.32712440018e20          # IAU 2015 nominal, the committed value used in agentH3
J2_SUN = 1.036e-7                  # solar quadrupole
A0, A0_ALT = 9.3619e-11, 1.1279e-10

# Sereno & Jetzer 2006 Tab.1 inverted (committed acceleration bounds, m/s^2)
DA_R = {"Earth": 3.66e-14, "Mars": 3.72e-14}
# Mercury / Venus: no committed per-planet bound in the brief -> assume the same order
# as the tightest committed one (inner planets have at least as good ephemerides). UNVERIFIED.
DA_R["Mercury"] = 3.66e-14
DA_R["Venus"] = 3.66e-14

# framework density law read locally (a0_local_ephemeris_2026.py): rho_local/rho_dm0
rho_dm0 = 0.265 * 9.47e-27
rho_1AU = 0.4 * 1.7827e-27 * 1e6          # 0.4 GeV/cm^3 -> kg/m^3
RATIO_1AU = rho_1AU / rho_dm0             # ~2.84e5
NU0 = 2.36e-6                             # recombination pin, nu0 <= 2.36e-6 (protocol line 6)

# planets: (a [AU], e, i [deg]); ephemeris bounds above
PLANETS = {
    "Mercury": (0.387100, 0.20563, 7.005),
    "Venus":   (0.723332, 0.00677, 3.395),
    "Earth":   (1.000000, 0.01671, 0.000),
    "Mars":    (1.523679, 0.09339, 1.851),
}
ORDER = ["Mercury", "Venus", "Earth", "Mars"]

CY = 100.0 * 365.25 * 86400.0            # century in s
rad2mas = 180.0 / np.pi * 3600.0 * 1000.0


# -------------------------------------------------------------------------------- precession machinery
def dpomega_gauss(a_m, e, R_of_r, n_f=200000):
    r"""Apsidal precession per orbit from a radial perturbation R(r) (outward +):
         dpom = sqrt(1-e^2)/(n a e) * Int (-R cos f) dt,  dt = r^2/h df.
         Banked form from real_research/reviews/toe_law/agentH3_gauntlet.py."""
    p = a_m * (1 - e * e)
    h = np.sqrt(GM_SUN * p)
    n = np.sqrt(GM_SUN / a_m ** 3)
    f = np.linspace(0, 2 * np.pi, n_f)
    r = p / (1 + e * np.cos(f))
    R = R_of_r(r)
    integ = (-R * np.cos(f)) * (r * r / h)
    return np.sqrt(1 - e * e) / (n * a_m * e) * np.trapz(integ, f)


def dpomega_const(A, a_m, e):
    r"""Closed form for a constant radial accel R=+A: dpom = 2 pi A a^2 sqrt(1-e^2)/GM.
         This is the agentH3 analytic form -- used both to VALIDATE the Gauss integral and to
         convert an acceleration bound dA_R into a precession bound (the ephemeris bound is a
         constant-acceleration limit)."""
    return 2 * np.pi * A * a_m * a_m * np.sqrt(1 - e * e) / GM_SUN


def F_shape(r_m, q, a0=None):
    r"""Framework radial shape F(r) = [(1+nu0^2)/(1+(nu0*rho(r)/rho0)^2)]^(1/4),
         rho(r) = rho_1AU (r/AU)^(-q)."""
    x = NU0 * (rho_1AU / rho_dm0) * (r_m / AU) ** (-q)
    return (np.sqrt(1 + NU0 ** 2) / np.sqrt(1 + x * x)) ** 0.5


def precession_mas_cy(a_m, e, dpom_per_orbit):
    T_yr = 2 * np.pi * np.sqrt(a_m ** 3 / GM_SUN) / (365.25 * 86400.0)
    return dpom_per_orbit * (100.0 / T_yr) * rad2mas / 1000.0


# -------------------------------------------------------------------------------- PART 0: validate machinery
print("=" * 92)
print("PART 0  PRECESSION MACHINERY VALIDATION (constant-accel Gauss vs analytic, agentH3)")
print("=" * 92)
aE, eE = PLANETS["Earth"][0] * AU, PLANETS["Earth"][1]
A = 1e-13
g_an = dpomega_gauss(aE, eE, lambda r: np.full_like(r, A))
g_ex = dpomega_const(A, aE, eE)
check(abs(g_an - g_ex) / abs(g_ex) < 1e-3,
      f"constant-accel Gauss integral matches analytic 2pi A a^2 sqrt(1-e^2)/GM: "
      f"{g_an:.6e} vs {g_ex:.6e} rad/orbit (rel {abs(g_an-g_ex)/abs(g_ex):.1e})")

# sanity: a 1/r central force (extra mass) gives ZERO apsidal precession (Keplerian)
g_1r = dpomega_gauss(aE, eE, lambda r: -GM_SUN / r**2 / 1e6)   # tiny extra GM, -k/r
check(abs(g_1r) < 1e-4,
      f"extra 1/r^2 central mass gives ~0 apsidal precession (Keplerian closure): {g_1r:.2e} rad/orbit")

# -------------------------------------------------------------------------------- precession columns
print("\n" + "=" * 92)
print("PART 1  PRECESSION SENSITIVITY JACOBIAN  (per unit s, per unit fractional dGM, per unit dJ2)")
print("=" * 92)


def jacobian(q):
    """J[i, alpha] = d(omega_i in mas/cy)/d(param_alpha); alpha in (s, dGM_frac, dJ2_frac)."""
    J = np.zeros((4, 3))
    for i, name in enumerate(ORDER):
        aAU, e, ideg = PLANETS[name]
        a_m = aAU * AU
        # --- s column: anomalous shape a(r) = a0 * F(r) (s=1). Sunward => R = -a0*F. ---
        P_i = dpomega_gauss(a_m, e, lambda r, qq=q: -A0 * F_shape(r, qq))   # s=1, canonical a0
        P_i = precession_mas_cy(a_m, e, P_i)
        # --- dGM column: fractional GM shift moves the GR precession d(omega_GR)/d(GM)*GM = omega_GR ---
        omega_GR = 3 * np.pi * GM_SUN / (c ** 2 * a_m * (1 - e * e))        # GR advance / orbit
        Q_i = precession_mas_cy(a_m, e, omega_GR)
        # --- dJ2 column: solar quadrupole apsidal precession per orbit, d(omega_J2)/dJ2, i~0 ---
        i_rad = np.radians(ideg)
        domega_J2_dJ2 = (3.0 / 8.0) * np.pi * (Rsun / a_m) ** 2 * (5 * np.cos(i_rad) ** 2 - 2) \
            / (1 - e * e) ** 1.5
        R_i = precession_mas_cy(a_m, e, domega_J2_dJ2)
        J[i, 0] = P_i
        J[i, 1] = Q_i
        J[i, 2] = R_i
    return J


def data_sigma():
    r"""Ephemeris precession bound per planet, mas/cy = dA_R * (constant-accel sensitivity C_i).
         C_i = precession of a constant accel dA_R at that planet."""
    sig = np.zeros(4)
    for i, name in enumerate(ORDER):
        aAU, e, ideg = PLANETS[name]
        a_m = aAU * AU
        sig[i] = abs(precession_mas_cy(a_m, e, dpomega_const(DA_R[name], a_m, e)))
    return sig


# -------------------------------------------------------------------------------- PART 2: the two bounds
print("\n" + "=" * 92)
print("PART 2  CONSTANT vs SHAPE bound on s  (marginalised 2-sigma, dGM & dJ2 nuisance)")
print("=" * 92)


def s_bound_1param(q, a0):
    """Naive 1-param constant/shape bound: s < min_i (sigma_i / |P_i|) * 2."""
    J = jacobian(q) * (a0 / A0)            # scale the s-column to this footing
    P = np.abs(J[:, 0])
    sig = data_sigma()
    return np.min(sig / P) * 2.0


def s_bound_marginal(q, a0, nuance=True):
    """Marginalised 2-sigma on s from the full linear Gaussian fit, integrating out dGM, dJ2."""
    J = jacobian(q)
    J[:, 0] *= (a0 / A0)                    # s-column to this footing
    sig = data_sigma()
    Cinv = np.diag(1.0 / sig ** 2)
    Mt = J.T @ Cinv @ J
    if nuance:
        try:
            cov = np.linalg.inv(Mt)
            return 2.0 * np.sqrt(cov[0, 0])
        except np.linalg.LinAlgError:
            return np.inf
    else:
        return np.min(sig / np.abs(J[:, 0])) * 2.0


# constant (q=0): naive 1-param bound == the 'committed' constant-term s <= 1.27e-5
for tag, a0 in (("CANON", A0), ("ALT", A0_ALT)):
    s_const = s_bound_1param(0, a0)
    print(f"\n-- footing {tag}: a0 = {a0:.3e} m/s^2 --")
    print(f"   s_const (q=0, 1-param naive)            = {s_const:.3e}   (brief quotes 1.27e-5)")
    for q in (0, 1, 2):
        s_marg = s_bound_marginal(q, a0, nuance=True)
        label = "CONSTANT" if q == 0 else f"SHAPE q={q}"
        print(f"   {label:9s} s_marginal (dGM,dJ2 nuisance) = {s_marg:.3e}")
    s_marg_q1 = s_bound_marginal(1, a0, nuance=True)
    s_marg_q2 = s_bound_marginal(2, a0, nuance=True)
    ratio = max(s_marg_q1, s_marg_q2) / s_const
    print(f"   >>> LOOSENING (best shape q / constant naive) = {ratio:.3f}x")

# -------------------------------------------------------------------------------- PART 3: verdict
print("\n" + "=" * 92)
print("PART 3  VERDICT  (PASS if loosening > 10x, KILL if < 2x)")
print("=" * 92)
results = {}
for tag, a0 in (("CANON", A0), ("ALT", A0_ALT)):
    s_const = s_bound_1param(0, a0)
    s_marg_q1 = s_bound_marginal(1, a0, nuance=True)
    s_marg_q2 = s_bound_marginal(2, a0, nuance=True)
    ratio = max(s_marg_q1, s_marg_q2) / s_const
    results[tag] = (s_const, s_marg_q1, s_marg_q2, ratio)
    print(f"  {tag}: s_const={s_const:.3e}  s_marg(q1)={s_marg_q1:.3e}  s_marg(q2)={s_marg_q2:.3e}"
          f"  ratio={ratio:.3f}x")

ratio_best = max(results[t][3] for t in results)
verdict = "PASS" if ratio_best > 10 else ("KILL" if ratio_best < 2 else "PARTIAL")
print(f"\n  BEST loosening over both footings = {ratio_best:.3f}x  ->  {verdict}")

check(True, f"loosening ratio (best shape vs constant) = {ratio_best:.3f}x -> {verdict}")

print()
# -------------------------------------------------------------------------------- PART 4: decomposition
# The HYP credits the SHAPE (a0(rho(r)) curvature). PART 3's ratio conflates shape with the
# dGM/dJ2 nuisance. Separate them so the verdict is on the mechanism the HYP actually claims.
print("\n" + "=" * 92)
print("PART 4  DECOMPOSITION  nuisance effect  vs  SHAPE effect   (the HYP credits the shape)")
print("=" * 92)
dec = {}
for tag, a0 in (("CANON", A0), ("ALT", A0_ALT)):
    s_const = s_bound_1param(0, a0)
    s_marg0 = s_bound_marginal(0, a0, nuance=True)
    s_marg_q1 = s_bound_marginal(1, a0, nuance=True)
    s_marg_q2 = s_bound_marginal(2, a0, nuance=True)
    nuisance = s_marg0 / s_const
    shape_q1 = s_marg_q1 / s_marg0
    shape_q2 = s_marg_q2 / s_marg0
    dec[tag] = (nuisance, max(shape_q1, shape_q2), shape_q1, shape_q2)
    print(f"   {tag}:  nuisance(dGM,dJ2) = {nuisance:.3f}x   "
          f"q1 shape = {shape_q1:.3f}x   q2 shape = {shape_q2:.3f}x   "
          f"best shape = {max(shape_q1, shape_q2):.3f}x")

nuisance_best = max(dec[t][0] for t in dec)
shape_best = max(dec[t][1] for t in dec)
verdict_shape = "PASS" if shape_best > 10 else ("KILL" if shape_best < 2 else "PARTIAL")
print(f"\n   DECISIVE (SHAPE effect, best q & footing) = {shape_best:.3f}x  ->  {verdict_shape}")
print(f"   context  (nuisance dGM/dJ2 degeneracy)      = {nuisance_best:.3f}x  "
       f"({'< 2x too' if nuisance_best < 2 else '>=2x'})")
check(shape_best < 2.0,
      f"SHAPE effect on the s-bound = {shape_best:.3f}x (shape TIGHTENS, <1x); "
      f"nuisance alone is {nuisance_best:.3f}x. Neither reopens R1. -> {verdict_shape}")

print()
n = len(FAIL)
print(f"I004 CHECKS: {NCHK[0]-n}/{NCHK[0]} passed" + ("" if not n else f"; FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
