#!/usr/bin/env python3
r"""mi_route_a_mi_vs_mg_separation_2026.py -- LANE 2: WHICH OBSERVABLE MAXIMALLY SEPARATES MODIFIED INERTIA
FROM MODIFIED GRAVITY UNDER ROUTE A?

THE PROBLEM. Every disc number in this corpus was solved with an AQUAL / Bekenstein-Milgrom (or QUMOND)
field solver -- modified GRAVITY. The framework's commitment is modified INERTIA. In spherical symmetry the
two coincide identically (the field equation integrates to mu(x) x = y). Outside spherical symmetry they are
DIFFERENT THEORIES. This file scans candidate observables, computes both sides under Route A's exponential
kernel, and ranks them by separation over the observable's realistic measurement uncertainty.

THE ONE IDENTITY THAT ORGANISES THE WHOLE FILE. With x = nu(y) y and y = mu(x) x,
    L_mu(x) = dln mu / dln x  >= 0        L_nu(y) = dln nu / dln y  <= 0
    (1 + L_mu)(1 + L_nu) = 1     EXACTLY, for any kernel.
In a dominant uniform external field every candidate reduces to a statement about L_mu, and the MG and MI
answers turn out to be sqrt(1+L_mu) and 1/(1+L_mu) -- on OPPOSITE SIDES OF 1. That sign opposition is the
lane's answer and it is kernel-INDEPENDENT.

WHAT IS COMPUTED (nothing below is rescaled from a committed number; every comparator is re-run here)

  K  the identity, sympy-generic; and L_mu at the Milky Way's external field for four kernels. Route A
     MAXIMISES it -> Route A is the kernel on which this whole class of test is sharpest.

  W  OBSERVABLE A -- WIDE-BINARY ORIENTATION ANISOTROPY (the robustness winner).
     MI (the framework's own algebraic map, linearised): force par/perp = 1 + L_nu = 1/(1+L_mu) < 1.
     AQUAL deep-EFE: par/perp = sqrt(1+L_mu) > 1, from the EXACT closed-form solution of the anisotropic
        Poisson equation -- verified three ways (sympy PDE residual, an independent flux-normalisation
        integral, and the QUMOND road, which agrees in sign). QUMOND: par/perp = 1/(1+L_nu/2), between them.
     *** OPPOSITE SIGN, and PROVED so for any monotone kernel: MI < 1 < QUMOND < AQUAL, symbolically. ***
     AND THE OTHER HALF, against interest: the ORIENTATION-AVERAGED gamma_v does NOT separate MI from MG.
     A proper deep-EFE solve gives QUMOND EXACTLY the MI value (both are trace(response)/3 -- an identity,
     not a coincidence) and AQUAL 0.26 sigma from it. The committed 2.01 sigma_tot "physical MI-vs-MG
     separation" was a separation from the heuristic comparator sqrt(nu(y_extN)) = 1.2138, which omits the
     external field's own l = 0 back-reaction -- the delta-function content of d2/dz2(1/r) -- and
     corresponds to neither field theory. All of this front's MI-vs-MG content is in the ORIENTATION.

  D  OBSERVABLE B -- THE ALIGNED EFE ROTATION-CURVE DIPOLE (the sep/sigma winner, and it hurts).
     laneA's own solver and its own asym_local / asym_algebraic definitions, Route A kernel: the MI
     amplitude is 9-25x the AQUAL/QUMOND one on the frozen sample's own cells, and OPPOSITE in sign for
     e >~ 2x. Under the pre-registered matched filter the MI expectation is E[Ahat] = 10.3, against the
     in-hand FIRST_FIRING measurement +2.95 (analytic sd 3.13). That is 2.3 sigma AGAINST the framework's
     own modified-inertia amplitude, while the AQUAL floor sits 0.65 sigma below the measurement.

  R  OBSERVABLE C -- the non-spherical disc rotation curve (AQUAL solve vs the algebraic map, same baryons)
     and OBSERVABLE D -- the vertical/radial ratio, both from the same solves, with grid convergence.

  T  OBSERVABLE E -- the isolated deep-MOND two-body coefficient. The algebraic map's deep limit is derived
     numerically and shown to equal Milgrom arXiv:2503.07106 Eq (31) exactly; AQUAL's Eq (30) differs by
     x3.28 in C, x1.35 in velocity. Both reduce to C = 1 in the test-particle limit (the control).

  X  OBSERVABLE F -- Newton's third law. BM/AQUAL inherits it from convexity (committed). The algebraic map
     violates it: 0.106 a0 for a 1+0.5 Msun pair at 10 kAU. Route A makes it unobservably small in the
     solar system (that is why Route A was adopted) but NOT at wide-binary or galaxy-pair accelerations.
     Formally an infinite separation; the measurement channel is empty, and it is the reason the MI side of
     every row above is less constrained than the MG side, not more.

  S  the ranking, and (c) what the best one would take.
  H  (d) THE ASYMMETRY IN RIGOUR, stated for the winner: genuine or under-determined?

PRIOR ART, credited: nu = sqrt(1+1/y) IS Milgrom 1999 PLA 253:273 eq 9. The a0 ~ c sqrt(G rho_Lambda) FORM
is Milgrom 1994 Ann.Phys. 229:384. Milgrom 1986 ApJ 302:617 solved the EFE-dominated AQUAL point mass; the
squashed-coordinate solution used in W is his, re-derived and re-verified here, not claimed as new. Milgrom
2022 PRD 106:064060 builds MI at the level of the equations of motion with the explicit footnote that such
theories "are not necessarily governed by an action". Milgrom arXiv:2503.07106 supplies the linear MI
two-body coefficients and the exact CoM decoupling used in H. Carl's distinctive content is kappa = 1/2 and
the MI completion; a0 is an INPUT everywhere here and is never fitted.

BOTH a0 FOOTINGS are carried on every dimensional number. Exit 0 = every check held.
"""
from __future__ import annotations

import math
import pathlib
import sys

import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "directional_efe_2026"))

from mi_route_a_kernel import (A0_ALT, A0_CANON, dmu_dx, mu, mu_alpha2,  # noqa: E402
                               mu_simple, nu, nu_alpha1, nu_alpha2)

np.seterr(over="ignore", divide="ignore", invalid="ignore")

CHECKS: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    CHECKS.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 118)
    print(f"  {t}")
    print("=" * 118)


G_N, MSUN, KPC, KAU = 6.674e-11, 1.989e30, 3.0856775814913673e19, 1.496e14
GYR = 3.1557e16
FOOT = {"canonical": A0_CANON, "alt": A0_ALT}
# the two g_ext conventions of the frozen pre-registration (sec 1.1), used verbatim
GEXT = {"primary g_ext,obs": 1.778e-10, "alt Vc^2/R0": 2.078e-10}
# committed comparators this file must reproduce or it is not like-for-like
COM_YEXTN, COM_NU, COM_GPAR, COM_GPERP, COM_GV = 1.28903, 1.47342, 1.0380, 1.2138, 1.15820
COM_MGROW = 1.2138                    # mi_route_a_wb_gamma_v_2026 V4: the recomputed "framework-as-MG" row
COM_A0_A1, COM_A0_RA = 4.7652, 4.3170  # laneA alpha=1 / Route A A(x=0.10, e=0.03), per cent
COM_N_AQ_VS_B = 1385                  # mi_route_a_efe_dipole_resolve_2026 S7, canonical/maxclu
COM_NUVERT_A2 = 1.024                 # mi_aqual_solve_framework_kernel_2026, alpha=2, canonical
SIG_FIT_30K, SIG_SYS = 0.0191, 0.02   # frozen error model, N = 30,000
AHAT_OBS, AHAT_SD_AN, AHAT_SD_BS = 2.95, 3.13, 1.05   # prep_2026/aligned_firing/FIRST_FIRING.md, n = 16
WHISP_RMS_PRE = 0.187                 # ibid, 70-galaxy WHISP lopsidedness rms in the A = 2(v_r-v_a)/(v_r+v_a)
#                                       convention -- an ENSEMBLE noise used as an ensemble noise


# ============================================================================================== helpers
def L_mu_of(mufun, dmufun, x):
    """L_mu = dln mu / dln x, evaluated with the kernel's own analytic derivative."""
    x = float(x)
    return (x / float(mufun(x))) * float(dmufun(x))


def dmu_a2(x):
    return (1.0 + np.asarray(x, float) ** 2) ** -1.5


def dmu_simple(x):
    return (1.0 + np.asarray(x, float)) ** -2.0


def mu_a1(x):
    """the retired alpha=1 kernel in mu form: y = (-1 + sqrt(1+4x^2))/2, mu = y/x."""
    x = np.asarray(x, float)
    return (-1.0 + np.sqrt(1.0 + 4.0 * x * x)) / (2.0 * x)


def dmu_a1(x):
    x = np.asarray(x, float)
    s = np.sqrt(1.0 + 4.0 * x * x)
    return (2.0 * x / s - (-1.0 + s) / (2.0 * x)) / x


KERNELS = {"Route A (exp)": (mu, dmu_dx, nu),
           "alpha=2 (superseded)": (mu_alpha2, dmu_a2, nu_alpha2),
           "alpha=1 (retired)": (mu_a1, dmu_a1, nu_alpha1),
           "simple (control)": (mu_simple, dmu_simple, lambda y: 0.5 + np.sqrt(0.25 + 1.0 / np.asarray(y, float)))}


def yN_from_obs(x_obs, nufun):
    """closure inversion: the NEWTONIAN y whose boosted field is the OBSERVED x_obs. Amendment 4(b)."""
    return brentq(lambda y: float(nufun(y)) * y - x_obs, 1e-12, 1e8, xtol=1e-15, rtol=8.9e-16)


# ================================================================================================== K
banner("K  THE ONE IDENTITY, AND WHY ROUTE A IS THE KERNEL ON WHICH THIS CLASS OF TEST IS SHARPEST")

print(r"""  Everything in this file reduces to two logarithmic slopes of the SAME kernel:
      L_mu(x) = dln mu / dln x   (>= 0, mu increasing)          the AQUAL / MG slope
      L_nu(y) = dln nu / dln y   (<= 0, nu decreasing)          the MI slope
  and they are not independent. From y = mu(x) x, dln y / dln x = 1 + L_mu; from nu = x / y,
      dln nu / dln y = dln x / dln y - 1 = 1/(1 + L_mu) - 1   ==>   (1 + L_mu)(1 + L_nu) = 1  EXACTLY.
  So ONE number decides every deep-external-field comparison below. That is why the MG and MI answers come
  out as sqrt(1+L_mu) and 1/(1+L_mu): reciprocal-flavoured, and on OPPOSITE SIDES OF 1.
""")

xs = sp.symbols("x", positive=True)
m = sp.Function("m")
Lmu_s = sp.simplify(xs * sp.diff(m(xs), xs) / m(xs))
ys = sp.simplify(m(xs) * xs)                                   # y(x)
nus = sp.simplify(xs / ys)                                     # nu as a function of x
# L_nu = dln nu/dln y = (dln nu/dln x) / (dln y/dln x)
dlnnu_dlnx = sp.simplify(xs * sp.diff(sp.log(nus), xs))
dlny_dlnx = sp.simplify(xs * sp.diff(sp.log(ys), xs))
Lnu_s = sp.simplify(dlnnu_dlnx / dlny_dlnx)
ident = sp.simplify((1 + Lmu_s) * (1 + Lnu_s) - 1)
print(f"  sympy, generic mu(x):   L_mu = {Lmu_s},   L_nu = {sp.simplify(Lnu_s)}")
print(f"  (1 + L_mu)(1 + L_nu) - 1 = {ident}")
check(ident == 0,
      f"K1 the identity (1+L_mu)(1+L_nu) = 1 holds for an ARBITRARY kernel mu(x), proved symbolically with "
      f"sympy on an undetermined function (residual {ident}). Every MG-vs-MI number below is therefore a "
      f"statement about the single slope L_mu, and no kernel can decouple them")

# numeric corroboration on Route A over decades, plus the reciprocal read off the nu side directly
worst = 0.0
for yv in np.logspace(-6, 5, 400):
    xv = float(nu(yv)) * yv
    Lm = L_mu_of(mu, dmu_dx, xv)
    h = 1e-5 * yv
    Ln = (math.log(float(nu(yv + h))) - math.log(float(nu(yv - h)))) / (math.log(yv + h) - math.log(yv - h))
    worst = max(worst, abs((1 + Lm) * (1 + Ln) - 1))
check(worst < 3e-8,
      f"K2 and it holds in the ACTUAL Route A numerics over eleven decades to {worst:.1e}, with L_nu taken "
      f"from a finite difference of nu() and L_mu from the module's analytic dmu_dx -- two independent "
      f"routes through the kernel module, so a bug in either would break this")

print(f"\n  L_mu at the Milky Way's external field -- the lever arm of every row below.")
print(f"  {'kernel':<24}{'footing':<11}{'g_ext conv':<20}{'x_ext':>8}{'y_extN':>9}{'nu':>9}{'L_mu':>9}")
print("  " + "-" * 100)
LTAB = {}
for kn, (mf, dmf, nf) in KERNELS.items():
    for fl, a0 in FOOT.items():
        for gn, ge in GEXT.items():
            xo = ge / a0
            yN = yN_from_obs(xo, nf)
            LTAB[(kn, fl, gn)] = (xo, yN, float(nf(yN)), L_mu_of(mf, dmf, xo))
            xo_, yN_, nu_, L_ = LTAB[(kn, fl, gn)]
            print(f"  {kn:<24}{fl:<11}{gn:<20}{xo_:>8.4f}{yN_:>9.5f}{nu_:>9.5f}{L_:>9.5f}")
L_RA = LTAB[("Route A (exp)", "canonical", "primary g_ext,obs")][3]
others = [LTAB[(k, "canonical", "primary g_ext,obs")][3] for k in KERNELS if k != "Route A (exp)"]
check(L_RA > max(others),
      f"K3 *** ROUTE A HAS THE LARGEST L_mu OF ALL FOUR KERNELS AT THE MILKY WAY'S EXTERNAL FIELD *** "
      f"({L_RA:.4f} against {min(others):.4f}-{max(others):.4f} for alpha=2 / alpha=1 / simple). Route A "
      f"approaches Newton exponentially at LARGE x but its transition is BROADER near x ~ 2, and x ~ 2 is "
      f"exactly where the solar neighbourhood sits. So the kernel switch that cost the EFE-dipole amplitude "
      f"9% and cost the kappa measurement 2.4 -> 0.7 sigma is the kernel switch that MAXIMISES this class "
      f"of MI-vs-MG test. That is the one place Route A helps, and it is why this lane is worth running now")
check(min(LTAB[("Route A (exp)", f, g)][3] for f in FOOT for g in GEXT) > 0.33,
      f"K3b and it is not a corner effect: over both a0 footings x both frozen g_ext conventions Route A's "
      f"L_mu spans {min(LTAB[('Route A (exp)', f, g)][3] for f in FOOT for g in GEXT):.4f}-"
      f"{max(LTAB[('Route A (exp)', f, g)][3] for f in FOOT for g in GEXT):.4f}, every corner above every "
      f"other kernel's canonical value")


# ================================================================================================== W
banner("W  OBSERVABLE A -- WIDE-BINARY ORIENTATION ANISOTROPY: MI AND MG PREDICT OPPOSITE SIGNS")

print(r"""  SETUP. A binary sits in a dominant uniform external field g_ex (locally: toward the Galactic centre).
  Ask how the internal two-body force depends on the angle between the SEPARATION VECTOR and g_ex.

  MI -- the framework's own algebraic map a = nu(|g_N|/a0) g_N applied to each star's TOTAL Newtonian
  field, linearised in the internal field (this is exactly the object Amendment 4(d) uses):
      a_in,obs = nu_ex [ g_in + L_nu (ghat.g_in) ghat ]
      force par / force perp = 1 + L_nu = 1/(1 + L_mu)  <  1        WEAKER along g_ex

  AQUAL -- linearise div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho about the uniform external solution:
      mu_ex [ lap(phi) + L_mu d2phi/dz2 ] = 4 pi G rho,   zhat || g_ex
  which the substitution zeta = z/sqrt(1+L_mu) turns into an ordinary Poisson equation, giving for a point
  mass the SQUASHED potential
      phi = -G M / [ mu_ex sqrt(1+L_mu) sqrt(R^2 + z^2/(1+L_mu)) ]
      force par / force perp = sqrt(1 + L_mu)  >  1                 STRONGER along g_ex
  (Milgrom 1986 ApJ 302:617's solution; re-derived and re-verified here, not claimed as new.)
""")

# --- W1 reproduce the committed MI eigenvalues exactly, or nothing below is like-for-like
xo_ra = GEXT["primary g_ext,obs"] / A0_CANON
yN_ra = yN_from_obs(xo_ra, nu)
nu_ra_ext = float(nu(yN_ra))
L_ra = L_mu_of(mu, dmu_dx, xo_ra)
Ln_ra = 1.0 / (1.0 + L_ra) - 1.0
g2par, g2perp = nu_ra_ext * (1.0 + Ln_ra), nu_ra_ext
gv_iso_mi = math.sqrt((g2par + 2.0 * g2perp) / 3.0)
print(f"  MI eigenvalues, canonical a0 / primary g_ext:  y_extN = {yN_ra:.5f}, nu = {nu_ra_ext:.5f}, "
      f"gamma_par = {math.sqrt(g2par):.4f}, gamma_perp = {math.sqrt(g2perp):.4f}, gamma_v = {gv_iso_mi:.5f}")
check(abs(yN_ra - COM_YEXTN) < 2e-5 and abs(nu_ra_ext - COM_NU) < 2e-5
      and abs(math.sqrt(g2par) - COM_GPAR) < 5e-5 and abs(math.sqrt(g2perp) - COM_GPERP) < 5e-5
      and abs(gv_iso_mi - COM_GV) < 5e-5,
      f"W1 the MI side reproduces mi_route_a_wb_gamma_v_2026's committed numbers exactly -- y_extN "
      f"{yN_ra:.5f} vs {COM_YEXTN}, gamma_par {math.sqrt(g2par):.4f} vs {COM_GPAR}, gamma_perp "
      f"{math.sqrt(g2perp):.4f} vs {COM_GPERP}, gamma_v {gv_iso_mi:.5f} vs {COM_GV}. So the MG side "
      f"computed below is bolted to the SAME closure, the same g_ext convention and the same kernel, and "
      f"the comparison is not two different conventions passing in the night")

# --- W2 sympy: the squashed potential solves the anisotropic PDE away from the source
Rr, zz, Ll, Aa = sp.symbols("R z L A", positive=True)
phi_sq = -Aa / sp.sqrt(Rr**2 + zz**2 / (1 + Ll))
lap_cyl = sp.diff(Rr * sp.diff(phi_sq, Rr), Rr) / Rr + sp.diff(phi_sq, zz, 2)
resid = sp.simplify(lap_cyl + Ll * sp.diff(phi_sq, zz, 2))
print(f"\n  sympy residual of  lap(phi) + L d2phi/dz2  on the squashed potential (r > 0):  {resid}")
check(resid == 0,
      f"W2 the squashed potential satisfies the AQUAL deep-EFE equation IDENTICALLY away from the source "
      f"(sympy residual {resid}), for symbolic L -- so the anisotropy factor sqrt(1+L_mu) is the exact "
      f"solution's, not a small-L expansion. A wrong squashing exponent would leave a nonzero residual here")

# --- W3 the amplitude, by an INDEPENDENT flux integral (the coordinate rescaling is not reused)
th = np.linspace(1e-9, math.pi - 1e-9, 400001)
sth, cth = np.sin(th), np.cos(th)
rr = 1.0
den = np.sqrt(sth**2 + cth**2 / (1.0 + L_ra))
dphidr = 1.0 / (rr**2 * den)                                   # A = 1
Qq = (rr * sth) ** 2 + (rr * cth) ** 2 / (1.0 + L_ra)
dphidz = ((rr * cth) / (1.0 + L_ra)) / Qq**1.5
flux = float(np.trapz((dphidr + L_ra * dphidz * cth) * 2.0 * math.pi * rr**2 * sth, th))
flux_pred = 4.0 * math.pi * math.sqrt(1.0 + L_ra)
print(f"  flux of [grad phi + L (dphi/dz) zhat] over a sphere, A = 1:  {flux:.9f}  vs  "
      f"4 pi sqrt(1+L) = {flux_pred:.9f}")
check(abs(flux / flux_pred - 1.0) < 1e-8,
      f"W3 an INDEPENDENT check of the amplitude: the conserved flux of the anisotropic operator over a "
      f"sphere equals 4 pi A sqrt(1+L_mu) to {abs(flux/flux_pred-1):.1e}, which fixes "
      f"A = GM/(mu_ex sqrt(1+L_mu)) without reusing the coordinate rescaling that produced it. Shape (W2) "
      f"plus normalisation (W3) plus Poisson uniqueness pins the solution")

# --- W4 the QUMOND road, independently -- including the term that is easy to drop
Cc, ll = sp.symbols("C L")
rs_, ths_ = sp.symbols("r theta", positive=True)
P2 = (3 * sp.cos(ths_) ** 2 - 1) / 2
Phi2 = Cc * P2 / rs_
lap_sph = sp.diff(rs_**2 * sp.diff(Phi2, rs_), rs_) / rs_**2 \
    + sp.diff(sp.sin(ths_) * sp.diff(Phi2, ths_), ths_) / (rs_**2 * sp.sin(ths_))
want = -ll * 2 * P2 / rs_**3       # the REGULAR part of -L_nu d2/dz2(-GM/r), G = M = nu_ex = 1
resid_qm = sp.simplify((lap_sph - want).subs(Cc, ll / 3))
resid_qm_wrong = sp.simplify((lap_sph - want).subs(Cc, ll / 2))
print(f"""
  QUMOND road, done independently: lap(Phi) = div[nu(|grad Phi_N|/a0) grad Phi_N] linearises to
      lap(Phi) = nu_ex [ 4 pi G rho + L_nu d2phi_N/dz2 ],   L_nu = dln nu/dln y at y_extN.
  *** AND HERE IS THE TERM IT IS EASY TO DROP, WHICH IS THE WHOLE POINT OF THIS SUBSECTION. ***
  d2/dz2 (1/r) is NOT just 2 P_2(cos th)/r^3. As a distribution
      d_i d_j (1/r) = (3 n_i n_j - delta_ij)/r^3  -  (4 pi/3) delta_ij delta^3(r),
  because the trace must give lap(1/r) = -4 pi delta^3 and the three second derivatives share it equally.
  So d2phi_N/dz2 carries a MONOPOLE point source of exactly one third of the Newtonian one, and the
  external field therefore RENORMALISES the effective mass:
      lap(Phi) = 4 pi G M nu_ex (1 + L_nu/3) delta^3  -  2 nu_ex L_nu G M P_2 / r^3.
  Dropping the delta term leaves the monopole boost at nu_ex and the answer wrong by L_nu/3 ~ 9%.
""")
check(resid_qm == 0 and resid_qm_wrong != 0,
      f"W4 the QUMOND deep-EFE l = 2 amplitude is C = nu_ex L_nu G M / 3, verified symbolically (residual "
      f"{resid_qm}, and a mutated C = L/2 leaves {sp.simplify(resid_qm_wrong)} so the check is not vacuous)")
# --- W4b MEASURE the delta coefficient numerically, because the whole monopole hangs on it and the
#     three candidate values give three plainly different gamma_v. Divergence theorem, no algebra reused:
#     int_{|r|<R} d2/dz2 (1/r) d3r = surface integral of (d/dz (1/r)) zhat.nhat, which must be -4pi/3.
_th = np.linspace(0.0, math.pi, 200001)
DELTA_COEF = {}
for _R in (0.1, 1.0, 7.3):
    _s, _c = np.sin(_th), np.cos(_th)
    dz_1r = -(_R * _c) / _R**3                                  # d/dz (1/r) = -z/r^3, on |r| = R
    DELTA_COEF[_R] = float(np.trapz(dz_1r * _c * 2.0 * math.pi * _R**2 * _s, _th))
    # and the REGULAR part 2 P_2 / r^3 must have zero angular average at every radius
ang_P2 = float(np.trapz(0.5 * (3.0 * np.cos(_th) ** 2 - 1.0) * 2.0 * math.pi * np.sin(_th), _th)) / (4 * math.pi)
worst_delta = max(abs(v / (-4.0 * math.pi / 3.0) - 1.0) for v in DELTA_COEF.values())
CANDIDATES = {"1/3 (correct, trace-shared)": 1.0 / 3.0, "1 (as if d2/dz2 were the Laplacian)": 1.0,
              "0 (delta term DROPPED)": 0.0}
print(f"  MEASURED delta coefficient of d2/dz2(1/r) by the divergence theorem, at three radii: "
      f"{', '.join(f'{v/math.pi:.6f} pi' for v in DELTA_COEF.values())}  (target -4/3 pi)")
print(f"  angular average of the regular part P_2: {ang_P2:.2e}")
print(f"  {'candidate delta share':<38}{'monopole boost':>16}{'gamma_v':>10}")
for nm_, f_ in CANDIDATES.items():
    print(f"  {nm_:<38}{nu_ra_ext*(1+Ln_ra*f_):>16.5f}{math.sqrt(nu_ra_ext*(1+Ln_ra*f_)):>10.5f}")
check(worst_delta < 1e-6 and abs(ang_P2) < 1e-9,
      f"W4b THE DELTA COEFFICIENT IS MEASURED, NOT ASSERTED: the divergence theorem applied on spheres of "
      f"three different radii returns -4 pi/3 to {worst_delta:.1e}, radius-independently, while the regular "
      f"part 2 P_2/r^3 has zero angular average ({ang_P2:.1e}) -- so the ENTIRE volume integral is the "
      f"delta, and its share of the Laplacian's -4 pi is exactly 1/3. The table above shows why that "
      f"matters: the three candidate shares 1/3, 1 and 0 give gamma_v = "
      f"{math.sqrt(nu_ra_ext*(1+Ln_ra/3)):.4f}, {math.sqrt(nu_ra_ext*(1+Ln_ra)):.4f} and "
      f"{math.sqrt(nu_ra_ext):.4f} -- three plainly distinguishable answers, and the measurement picks the "
      f"first")
b_qm_par = nu_ra_ext * ((1 + Ln_ra / 3) - Ln_ra / 3)            # P_2(1) = 1
b_qm_perp = nu_ra_ext * ((1 + Ln_ra / 3) + Ln_ra / 6)           # P_2(0) = -1/2
b_qm_iso = nu_ra_ext * (1 + Ln_ra / 3)
check(abs(b_qm_par / nu_ra_ext - 1) < 1e-12
      and abs(math.sqrt(b_qm_iso) - COM_MGROW) > 0.04,
      f"W4c *** AND THIS DISQUALIFIES THE COMPARATOR THE CORPUS HAS BEEN USING AS ITS 'MG' ROW -- it is the "
      f"'0 (delta term DROPPED)' row of the table above, to the digit. *** mi_route_a_wb_gamma_v_2026 V4 "
      f"defines that row as the asymptote <nu(y_tot)> -> nu(y_extN), giving gamma_v = sqrt(nu) = "
      f"{COM_MGROW}. A proper QUMOND deep-EFE solve gives {math.sqrt(b_qm_iso):.5f} -- lower by "
      f"{COM_MGROW - math.sqrt(b_qm_iso):.4f}, precisely the omitted delta term. The banked row is not "
      f"arithmetically wrong; it is a HEURISTIC MG ('apply nu to the total field') that corresponds to "
      f"neither field theory. By-product worth one line: QUMOND's PARALLEL boost comes out exactly nu_ex "
      f"({b_qm_par:.5f}), and so does AQUAL's, so the two MG realisations agree along the field axis and "
      f"differ only across it")
# --- W4d the structural identity, PROVED symbolically on a generic response tensor
nuS, LS = sp.symbols("nu_ex L_nu")
thS, phS = sp.symbols("theta phi")
nhat = sp.Matrix([sp.sin(thS) * sp.cos(phS), sp.sin(thS) * sp.sin(phS), sp.cos(thS)])
zhat = sp.Matrix([0, 0, 1])
Tten = nuS * (sp.eye(3) + LS * zhat * zhat.T)
radial = sp.simplify((nhat.T * Tten * nhat)[0, 0])              # the radial-force boost at direction nhat
avg = sp.simplify(sp.integrate(sp.integrate(radial * sp.sin(thS), (thS, 0, sp.pi)),
                               (phS, 0, 2 * sp.pi)) / (4 * sp.pi))
tr3 = sp.simplify(Tten.trace() / 3)
print(f"\n  sympy, generic response tensor T_ij = nu_ex(delta_ij + L_nu zhat_i zhat_j):")
print(f"      radial boost at direction nhat  = {radial}")
print(f"      solid-angle average             = {avg}")
print(f"      trace/3                         = {tr3}")
check(sp.simplify(avg - tr3) == 0 and sp.simplify(avg - nuS * (1 + LS / 3)) == 0,
      f"W4d *** AND THE REASON THAT MATTERS: THE QUMOND MONOPOLE IS IDENTICALLY THE MI ORIENTATION "
      f"AVERAGE. *** Proved symbolically, by carrying out the solid-angle integral of the MI response "
      f"tensor's radial boost and finding it equals trace/3 = nu_ex(1 + L_nu/3) -- exactly the combination "
      f"W4b just measured as QUMOND's delta-function source strength. Both objects ARE the trace of the "
      f"same response tensor, so in the deep-EFE limit the orientation-averaged two-body force of modified "
      f"inertia and of QUMOND is THE SAME NUMBER, {b_qm_iso:.6f}. No sample size can separate them on that "
      f"statistic")

# --- W5 the sign opposition, all four kernels, both footings, both g_ext conventions
def aq_boosts(nu_ex, L):
    """AQUAL deep-EFE radial-force boosts: par, perp, and the solid-angle average."""
    k = L / (1.0 + L)
    inv_S = math.asin(math.sqrt(k)) / math.sqrt(k) if k > 1e-12 else 1.0
    return nu_ex, nu_ex / math.sqrt(1.0 + L), nu_ex / math.sqrt(1.0 + L) * inv_S


print(f"\n  {'kernel':<22}{'footing':<11}{'gext':<20}{'MI par/perp':>12}{'QUMOND':>9}{'AQUAL':>8}"
      f"{'MI v-ratio':>12}{'AQUAL v':>9}")
print("  " + "-" * 104)
SIGN_ROWS = {}
for kn in KERNELS:
    for fl in FOOT:
        for gn in GEXT:
            xo, yN, nue, L = LTAB[(kn, fl, gn)]
            Ln = 1.0 / (1.0 + L) - 1.0
            r_mi = 1.0 + Ln
            r_qm = ((1 + Ln / 3) - Ln / 3) / ((1 + Ln / 3) + Ln / 6)     # = 1/(1 + L_nu/2)
            p, q, _ = aq_boosts(nue, L)
            r_aq = p / q
            SIGN_ROWS[(kn, fl, gn)] = (r_mi, r_qm, r_aq)
            print(f"  {kn:<22}{fl:<11}{gn:<20}{r_mi:>12.5f}{r_qm:>9.5f}{r_aq:>8.5f}"
                  f"{math.sqrt(r_mi):>12.5f}{math.sqrt(r_aq):>9.5f}")
allrows = list(SIGN_ROWS.values())
# and the ordering is a THEOREM, proved symbolically in L, not a survey of cells
Lsym = sp.symbols("L", positive=True)
Lnsym = 1 / (1 + Lsym) - 1
mi_sym = sp.simplify(1 + Lnsym)
qm_sym = sp.simplify(1 / (1 + Lnsym / 2))
aq_sym = sp.sqrt(1 + Lsym)
print(f"\n  symbolic, for ANY monotone kernel (L = L_mu > 0):  MI = {mi_sym},  QUMOND = {sp.simplify(qm_sym)},"
      f"  AQUAL = sqrt(1+L)")
print(f"      1 - MI      = {sp.simplify(1 - mi_sym)}          > 0")
print(f"      QUMOND - 1  = {sp.simplify(qm_sym - 1)}          > 0")
print(f"      AQUAL^2 - QUMOND^2 = {sp.factor(sp.simplify(aq_sym**2 - qm_sym**2))}   > 0")
ord_ok = (sp.simplify(1 - mi_sym) == Lsym / (1 + Lsym)
          and sp.simplify(qm_sym - 1) == Lsym / (Lsym + 2)
          and sp.simplify(aq_sym**2 - qm_sym**2 - Lsym**2 * (1 + Lsym) / (2 + Lsym) ** 2) == 0)
check(ord_ok and all(a < 1.0 < b < c for a, b, c in allrows),
      f"W5 *** THE SIGN OPPOSITION IS A THEOREM, NOT A ROUTE A ACCIDENT. *** Symbolically, for any monotone "
      f"kernel: 1 - MI = L/(1+L) > 0, QUMOND - 1 = L/(2+L) > 0 and AQUAL^2 - QUMOND^2 = L^2(1+L)/(2+L)^2 > 0, "
      f"so MI < 1 < QUMOND < AQUAL strictly whenever L_mu > 0. Corroborated on all {len(allrows)} numeric "
      f"cells (4 kernels x 2 a0 footings x 2 frozen g_ext conventions). A measured SIGN therefore "
      f"discriminates with no kernel commitment, no a0 footing choice and no mass model at all")
r_mi, r_qm, r_aq = SIGN_ROWS[("Route A (exp)", "canonical", "primary g_ext,obs")]
sep_ratio_ra = math.sqrt(r_aq) - math.sqrt(r_mi)
check(sep_ratio_ra > max(math.sqrt(SIGN_ROWS[(k, 'canonical', 'primary g_ext,obs')][2])
                         - math.sqrt(SIGN_ROWS[(k, 'canonical', 'primary g_ext,obs')][0])
                         for k in KERNELS if k != "Route A (exp)"),
      f"W5b and Route A gives the WIDEST separation of the four kernels in the velocity ratio: "
      f"{math.sqrt(r_mi):.4f} (MI) vs {math.sqrt(r_aq):.4f} (AQUAL), a gap of {sep_ratio_ra:.4f}, against "
      f"{min(math.sqrt(SIGN_ROWS[(k,'canonical','primary g_ext,obs')][2]) - math.sqrt(SIGN_ROWS[(k,'canonical','primary g_ext,obs')][0]) for k in KERNELS if k != 'Route A (exp)'):.4f}-"
      f"{max(math.sqrt(SIGN_ROWS[(k,'canonical','primary g_ext,obs')][2]) - math.sqrt(SIGN_ROWS[(k,'canonical','primary g_ext,obs')][0]) for k in KERNELS if k != 'Route A (exp)'):.4f} "
      f"for the others -- K3's L_mu ordering carried into the observable")

# --- W6 the ORIENTATION AVERAGE is nearly blind: the uncomfortable half of this section
_, _, b_aq_iso = aq_boosts(nu_ra_ext, L_ra)
gv_aq, gv_qm = math.sqrt(b_aq_iso), math.sqrt(b_qm_iso)
sig_tot = math.hypot(SIG_FIT_30K, SIG_SYS)
print(f"\n  ORIENTATION-AVERAGED gamma_v at N = 30,000 (frozen sigma_tot = {sig_tot:.5f}):")
print(f"      MI (algebraic map; the committed target)          {gv_iso_mi:.5f}")
print(f"      QUMOND monopole, proper deep-EFE solve            {gv_qm:.5f}   -> |MI - QUMOND| = "
      f"{abs(gv_iso_mi-gv_qm):.5f} = {abs(gv_iso_mi-gv_qm)/sig_tot:.2f} sigma_tot")
print(f"      AQUAL monopole, exact in L (both NEW here)        {gv_aq:.5f}   -> |MI - AQUAL|  = "
      f"{abs(gv_iso_mi-gv_aq):.5f} = {abs(gv_iso_mi-gv_aq)/sig_tot:.2f} sigma_tot")
print(f"      the banked 'framework-as-MG' comparator sqrt(nu)  {COM_MGROW:.5f}   -> the {abs(gv_iso_mi-COM_MGROW)/sig_tot:.2f} "
      f"sigma_tot that mi_route_a_wb_gamma_v_2026 V4d recorded as the MI-vs-MG separation")
check(abs(gv_iso_mi - gv_aq) / sig_tot < 0.5
      and abs(gv_iso_mi - COM_MGROW) / sig_tot > 1.5,
      f"W6 *** REPORTED AGAINST INTEREST, AND IT IS THE SECOND MOST IMPORTANT RESULT IN THIS FILE: THE "
      f"ORIENTATION-AVERAGED WIDE-BINARY STATISTIC DOES NOT SEPARATE MI FROM MG AT ALL. *** Against QUMOND "
      f"it is EXACTLY degenerate ({abs(gv_iso_mi-gv_qm)/sig_tot:.3f} sigma_tot, W4d's identity); against "
      f"AQUAL, whose monopole is exact-in-L here, it is {abs(gv_iso_mi-gv_aq)/sig_tot:.2f} sigma_tot. The "
      f"committed {abs(gv_iso_mi-COM_MGROW)/sig_tot:.2f} sigma_tot 'physical MI-vs-MG separation' is a "
      f"separation from the heuristic sqrt(nu(y_extN)) comparator, which W4c shows is neither field theory. "
      f"So section 1.5's 'MI vs MG likely UNDECIDABLE' does not merely STAND -- on the orientation-averaged "
      f"statistic it is stronger than the document claims, and the 2.01 sigma should not be carried forward "
      f"as MI-vs-MG. Everything the front has on this axis lives in the ORIENTATION DEPENDENCE below")

# --- W7 the exact nonlinear MI map: where the anisotropy lives, and the built-in null control
def mi_rel_boost(m1, m2, d, nhat, gexN_vec, a0):
    """EXACT (unlinearised) algebraic-map relative acceleration, attractive component, / Newtonian."""
    n = np.asarray(nhat, float)
    n = n / np.linalg.norm(n)
    g1 = +G_N * m2 / d**2 * n
    g2 = -G_N * m1 / d**2 * n

    def amap(gv):
        return float(nu(np.linalg.norm(gv) / a0)) * gv

    ar = amap(gexN_vec + g2) - amap(gexN_vec + g1)
    return float(-np.dot(ar, n)) / (G_N * (m1 + m2) / d**2)


print(f"\n  EXACT (unlinearised) MI map, M = 1.5 Msun equal masses, canonical a0 / primary g_ext:")
print(f"  {'s [kAU]':>8}{'g_in/a0':>10}{'g_in/g_extN':>13}{'par boost':>11}{'perp boost':>12}"
      f"{'par/perp':>10}{'asymptote':>11}")
mprof = {}
gexN_vec = np.array([0.0, 0.0, yN_ra * A0_CANON])
for s in (2, 5, 10, 15, 20, 30, 50):
    d = s * KAU
    gin = G_N * 1.5 * MSUN / d**2
    bp = mi_rel_boost(0.75 * MSUN, 0.75 * MSUN, d, [0, 0, 1], gexN_vec, A0_CANON)
    bq = mi_rel_boost(0.75 * MSUN, 0.75 * MSUN, d, [1, 0, 0], gexN_vec, A0_CANON)
    mprof[s] = bp / bq
    print(f"  {s:>8}{gin/A0_CANON:>10.4f}{gin/(yN_ra*A0_CANON):>13.4f}{bp:>11.5f}{bq:>12.5f}"
          f"{bp/bq:>10.5f}{r_mi:>11.5f}")
check(abs(mprof[30] / r_mi - 1) < 0.005 and mprof[2] > 0.999 and mprof[5] > 1.0,
      f"W7 *** THE TEST CARRIES ITS OWN NULL CONTROL. *** The exact map reaches the deep-EFE asymptote "
      f"{r_mi:.5f} to {abs(mprof[30]/r_mi-1):.2%} by 30 kAU, but at 2 kAU the anisotropy is GONE "
      f"({mprof[2]:.5f}) and at 5 kAU it is weakly the OTHER way ({mprof[5]:.5f}) because the internal "
      f"field dominates and both theories are Newtonian there. So the 1-5 kAU population of the SAME "
      f"survey is a zero-signal calibration sample for every orientation systematic (tidal alignment, "
      f"extinction, scan-angle) -- the single most valuable observational property of this observable, and "
      f"it is why its systematics do not have to be trusted a priori")

# --- W8 projection dilution, by Monte Carlo, and the forecast
rng = np.random.default_rng(20260803)
NMC = 600000
vv = rng.normal(size=(NMC, 3))
vv /= np.linalg.norm(vv, axis=1)[:, None]
ss = rng.normal(size=(NMC, 3))
ss /= np.linalg.norm(ss, axis=1)[:, None]
c2t = vv[:, 2] ** 2
vp = vv - (np.sum(vv * ss, axis=1)[:, None]) * ss
gp = np.tile(np.array([0.0, 0.0, 1.0]), (NMC, 1)) - ss[:, 2:3] * ss
nvp, ngp = np.linalg.norm(vp, axis=1), np.linalg.norm(gp, axis=1)
gsel = (nvp > 1e-4) & (ngp > 1e-4)
c2p = (np.sum(vp * gp, axis=1) / (nvp * ngp)) ** 2


def b_of_c2(model, c2):
    if model == "MI":
        return nu_ra_ext * (1.0 + Ln_ra * c2)
    if model == "QUMOND":
        # nu_ex[(1 + L_nu/3) - (L_nu/3) P_2] = nu_ex[1 + (L_nu/2)(1 - cos^2)]
        return nu_ra_ext * (1.0 + (Ln_ra / 2.0) * (1.0 - c2))
    return nu_ra_ext / math.sqrt(1.0 + L_ra) / np.sqrt(1.0 - c2 * L_ra / (1.0 + L_ra))


def slope(yv, c2):
    Xd = c2 - c2.mean()
    return float(np.sum(Xd * (yv - yv.mean())) / np.sum(Xd * Xd))


print(f"\n  PROJECTION DILUTION (only the SKY-PROJECTED separation and the sky-projected g_ext direction are "
      f"observable):")
print(f"  {'model':<9}{'B(true cos^2)':>15}{'B(projected)':>14}{'D':>8}")
BT, BP = {}, {}
for mdl in ("MI", "AQUAL", "QUMOND"):
    yv = np.sqrt(b_of_c2(mdl, c2t))
    BT[mdl] = slope(yv, c2t)
    BP[mdl] = slope(yv[gsel], c2p[gsel])
    print(f"  {mdl:<9}{BT[mdl]:>15.5f}{BP[mdl]:>14.5f}{BP[mdl]/BT[mdl]:>8.4f}")
Ds = [BP[m] / BT[m] for m in BT]
check(max(Ds) - min(Ds) < 0.005 and 0.40 < np.mean(Ds) < 0.50,
      f"W8 the dilution is PURELY GEOMETRIC: D = {min(Ds):.4f}-{max(Ds):.4f} across three physically "
      f"different models (spread {max(Ds)-min(Ds):.4f}), so it can be applied as a single factor "
      f"{np.mean(Ds):.3f} and it does not smuggle a model choice into the forecast. The sign is untouched "
      f"by projection -- it is an attenuation, never an inversion")

VARC2P = float(c2p[gsel].var())
SIG1 = SIG_FIT_30K * math.sqrt(30000.0)                    # per-pair scatter implied by the frozen model
print(f"\n  FORECAST. Var(cos^2 psi_proj) = {VARC2P:.5f}; the frozen error model sigma_fit = {SIG_FIT_30K} "
      f"at N = 30,000 implies a per-pair scatter sigma_1 = {SIG1:.3f}.")
print(f"  Optimal (continuous cos^2 psi) fit of the modulation amplitude B:  sigma_B = sigma_1 / "
      f"sqrt(N Var(cos^2 psi_proj)).")
print(f"  {'comparison':<18}{'|dB|':>9}{'N=30k':>9}{'N=100k':>9}{'N=300k':>9}{'N(3 sig)':>11}")
NEEDED = {}
for other in ("AQUAL", "QUMOND"):
    dB = abs(BP["MI"] - BP[other])
    row = [dB / (SIG1 / math.sqrt(N * VARC2P)) for N in (30000, 100000, 300000)]
    NEEDED[other] = SIG1**2 / (VARC2P * (dB / 3.0) ** 2)
    print(f"  {'MI vs ' + other:<18}{dB:>9.5f}{row[0]:>9.2f}{row[1]:>9.2f}{row[2]:>9.2f}"
          f"{NEEDED[other]:>11,.0f}")
z30 = abs(BP["MI"] - BP["AQUAL"]) / (SIG1 / math.sqrt(30000.0 * VARC2P))
z30_qm = abs(BP["MI"] - BP["QUMOND"]) / (SIG1 / math.sqrt(30000.0 * VARC2P))
check(z30 > abs(gv_iso_mi - gv_aq) / sig_tot * 5.0 and z30_qm > 1.5,
      f"W9 at the pre-registered N = 30,000 the ORIENTATION-RESOLVED statistic separates MI from AQUAL at "
      f"{z30:.2f} sigma and from QUMOND at {z30_qm:.2f} sigma, against "
      f"{abs(gv_iso_mi-gv_aq)/sig_tot:.2f} and {abs(gv_iso_mi-gv_qm)/sig_tot:.3f} sigma for the "
      f"orientation-AVERAGED statistic on the SAME pairs with the SAME error model -- a factor "
      f"{z30/(abs(gv_iso_mi-gv_aq)/sig_tot):.0f} against AQUAL and an infinite factor against QUMOND, which "
      f"the averaged statistic cannot separate at any N (W4d). 3 sigma needs N ~ {NEEDED['AQUAL']:,.0f} "
      f"pairs. This is the whole recommendation of the lane: the orientation dependence is where the "
      f"wide-binary front's MI-vs-MG content actually is, and the frozen pipeline already has the "
      f"ingredients")
print(f"  AND THE SYSTEMATIC BUDGET, which is the reason this is not just the isotropic test again: an "
      f"ISOTROPIC systematic contributes NOTHING to B (it has no cos^2 psi projection), so the frozen "
      f"sigma_sys = {SIG_SYS} does not enter. What does enter is any ORIENTATION-CORRELATED systematic. "
      f"Requiring 3 sigma caps it at |dB|/3 = {abs(BP['MI']-BP['AQUAL'])/3:.4f} in B; W7's 1-5 kAU null "
      f"sample measures exactly that quantity in situ.")
for ssd in (0.0, 0.005, 0.01, 0.02):
    need = (abs(BP["MI"] - BP["AQUAL"]) / 3.0) ** 2 - ssd**2
    txt = f"{SIG1**2/(VARC2P*need):,.0f}" if need > 0 else "UNREACHABLE at any N"
    print(f"      orientation-correlated sigma_sys(B) = {ssd:5.3f}  ->  N(3 sigma) = {txt}")


# ================================================================================================== D
banner("D  OBSERVABLE B -- THE ALIGNED EFE ROTATION-CURVE DIPOLE: a factor 9-25, and the in-hand data "
       "already lean AGAINST MI")

_src = (HERE / "directional_efe_2026/laneA_predictions.py").read_text()
LA: dict = {"__name__": "laneA_anchor"}
exec(compile(_src[: _src.index("def main()")], "laneA_predictions.py", "exec"), LA)   # noqa: S102


def nu_ra_v(y):
    return 1.0 / -np.expm1(-np.sqrt(np.asarray(y, float)))


def nup_ra_v(y):
    y = np.asarray(y, float)
    s = np.sqrt(y)
    mm = -np.expm1(-s)
    return -np.exp(-s) / (2.0 * s * mm * mm)


print("  laneA_predictions.py is EXEC'd, not re-implemented: solve_qumond (the MG/QUMOND-class l-mode BVP)")
print("  and asym_algebraic (the pointwise algebraic map) are the anchor's own definitions, in the anchor's")
print("  own (x, e, gamma) parametrisation, so the two sides are measured with one ruler.")
_s3_a1 = LA["solve_qumond"](LA["nu_fw"], LA["nup_fw"], 0.03)
_s3_ra = LA["solve_qumond"](nu_ra_v, nup_ra_v, 0.03)
A0_a1 = 100 * LA["asym_local"](_s3_a1, 0.10, 0.0)[0]
A0_ra = 100 * LA["asym_local"](_s3_ra, 0.10, 0.0)[0]
check(abs(A0_a1 - COM_A0_A1) < 0.002 and abs(A0_ra - COM_A0_RA) < 0.002,
      f"D1 the anchor reproduces BOTH committed reference amplitudes A(x=0.10, e=0.03): alpha=1 "
      f"{A0_a1:.4f}% vs the committed {COM_A0_A1}%, Route A {A0_ra:.4f}% vs the committed {COM_A0_RA}%. "
      f"The solver is the committed one and the kernel swap is the only change")

print(f"\n  MG (QUMOND-class BVP) vs MI (algebraic map), Route A kernel in BOTH, gamma = 0:")
print(f"  {'x':>6}{'e':>8}{'e/x':>7}{'A_MG %':>10}{'A_MI %':>10}{'A_MI/A_MG':>11}{'sign':>18}")
_sols: dict = {}


def sol_ra(e):
    if e not in _sols:
        _sols[e] = LA["solve_qumond"](nu_ra_v, nup_ra_v, e)
    return _sols[e]


opp = 0
tot = 0
for x in (0.05, 0.10, 0.20):
    for e in (0.01, 0.03, 0.05, 0.10, 0.20, 0.30):
        a_mg = LA["asym_local"](sol_ra(e), x, 0.0)[0]
        a_mi = LA["asym_algebraic"](nu_ra_v, e, x, 0.0)
        tot += 1
        sgn = "SAME" if a_mg * a_mi > 0 else "*** OPPOSITE ***"
        if a_mg * a_mi < 0:
            opp += 1
        print(f"  {x:>6.2f}{e:>8.3f}{e/x:>7.2f}{100*a_mg:>10.4f}{100*a_mi:>10.4f}{a_mi/a_mg:>11.2f}{sgn:>18}")
check(opp >= 5,
      f"D2 the two theories have OPPOSITE-SIGNED dipoles on {opp} of {tot} map cells -- every cell with "
      f"e >~ 2x, where the QUMOND field solve has passed through its committed x <~ e reversal (e_0 = "
      f"0.105 at x = 0.10) while the algebraic map's own reversal is out at e* = 6.63 a0. Two sign "
      f"reversals separated by a factor ~60 in e is a fork, not an amplitude comparison -- but see D5")

# --- the pre-registered matched filter, evaluated under MI on the frozen n = 16 sample's own cells
FIRING = [("NGC2903", 0.121, 0.0064, -0.103), ("UGC05721", 0.044, 0.0096, -3.168),
          ("UGC05829", 0.072, 0.0083, +0.924), ("UGC06446", 0.048, 0.0052, +1.749),
          ("NGC3726", 0.083, 0.0073, +1.040), ("UGC06787", 0.089, 0.0049, +0.473),
          ("NGC3992", 0.130, 0.0037, +0.145), ("NGC4088", 0.290, 0.0075, +0.348),
          ("NGC4100", 0.117, 0.0053, -0.931), ("UGC07151", 0.128, 0.0106, -0.536),
          ("UGC07323", 0.173, 0.0088, -0.673), ("UGC07524", 0.064, 0.0079, -1.686),
          ("UGC07603", 0.049, 0.0092, +3.215), ("NGC4559", 0.083, 0.0118, -2.080),
          ("UGC09133", 0.033, 0.0027, -1.030), ("UGC12732", 0.047, 0.0028, +0.439)]
print(f"\n  THE PRE-REGISTERED MATCHED FILTER, Ahat = sum(A_i p_i/s^2)/sum(p_i^2/s^2), with p_i the FROZEN")
print(f"  alpha=1 predictors of FIRST_FIRING.md. Under a hypothesis H, E[Ahat] = the p_i^2-weighted mean of")
print(f"  A_H(x_i,e_i)/A_alpha1(x_i,e_i). Both a0 footings: the alt footing rescales every x_i and e_i by")
print(f"  a0_canon/a0_alt = {A0_CANON/A0_ALT:.4f}.")
print(f"  {'footing':<11}{'E[Ahat] MI':>12}{'E[Ahat] AQUAL/QUMOND':>22}{'R range':>14}"
      f"{'z(MI) analytic':>16}{'z(MG) analytic':>16}")
EMI, EMG = {}, {}
_sa1: dict = {}
for fl, sc in (("canonical", 1.0), ("alt", A0_CANON / A0_ALT)):
    nmi = nmg = dd = 0.0
    Rs = []
    for _nm, x0, e0, p in FIRING:
        x, e = x0 * sc, e0 * sc
        if e not in _sa1:
            _sa1[e] = LA["solve_qumond"](LA["nu_fw"], LA["nup_fw"], e)
        a_a1 = LA["asym_local"](_sa1[e], x, 0.0)[0]
        a_ra = LA["asym_local"](sol_ra(e), x, 0.0)[0]
        a_mi = LA["asym_algebraic"](nu_ra_v, e, x, 0.0)
        w = p * p
        nmi += (a_mi / a_a1) * w
        nmg += (a_ra / a_a1) * w
        dd += w
        Rs.append(a_mi / a_ra)
    EMI[fl], EMG[fl] = nmi / dd, nmg / dd
    print(f"  {fl:<11}{EMI[fl]:>12.3f}{EMG[fl]:>22.3f}{f'{min(Rs):.1f}-{max(Rs):.1f}':>14}"
          f"{(EMI[fl]-AHAT_OBS)/AHAT_SD_AN:>16.2f}{(EMG[fl]-AHAT_OBS)/AHAT_SD_AN:>16.2f}")
check(EMI["canonical"] > 6.0 and abs(EMI["alt"] / EMI["canonical"] - 1) < 0.05,
      f"D3 the framework's own modified-inertia law predicts E[Ahat] = {EMI['canonical']:.2f} (canonical) / "
      f"{EMI['alt']:.2f} (alt) in the frozen statistic, against {EMG['canonical']:.3f} for the "
      f"QUMOND-class field solve on the same kernel and the same cells. Footing-robust to "
      f"{abs(EMI['alt']/EMI['canonical']-1):.1%}: the map is written in dimensionless (x, e) so the footing "
      f"only moves where the galaxies sit on it")
# --- D3b before using the firing's numbers, RECONSTRUCT them from its own published table
_Ai = np.array([-0.0277, -0.1230, +0.0108, +0.0116, -0.0565, +0.0768, -0.0065, -0.1188,
                +0.0795, +0.0642, -0.0192, -0.0039, +0.1294, -0.1355, -0.0563, +0.0712])
_pi = np.array([p for _n, _x, _e, p in FIRING]) / 100.0
ahat_rec = float((_Ai * _pi).sum() / (_pi * _pi).sum())
sd_rec = float(WHISP_RMS_PRE / math.sqrt((_pi * _pi).sum()))
print(f"\n  RECONSTRUCTION CHECK before any of that is used: with equal per-galaxy sigma the published table's")
print(f"  own A_i and p_i give Ahat = {ahat_rec:.4f} and analytic sd = {WHISP_RMS_PRE}/sqrt(sum p_i^2) = "
      f"{sd_rec:.4f}.")
check(abs(ahat_rec - AHAT_OBS) < 0.01 and abs(sd_rec - AHAT_SD_AN) < 0.01,
      f"D3b the firing is RECONSTRUCTED from its own published table: Ahat {ahat_rec:.4f} vs the committed "
      f"{AHAT_OBS} and analytic sd {sd_rec:.4f} vs the committed {AHAT_SD_AN}. So the E[Ahat] values above "
      f"are normalised in exactly the statistic that produced +{AHAT_OBS}, the 16 rows were transcribed "
      f"correctly, and the confrontation below is not comparing two different estimators")

print(f"\n  AND THE CONFRONTATION WITH THE NUMBER ALREADY ON RECORD (FIRST_FIRING.md, n = 16, exploratory):")
print(f"      measured Ahat = {AHAT_OBS:+.2f}, analytic sd {AHAT_SD_AN} (70-galaxy WHISP ensemble rms -- the")
print(f"      CONSERVATIVE error), bootstrap sd {AHAT_SD_BS} (the 16 happen to be less lopsided)")
for lab, sd in (("analytic / ensemble (used for the verdict)", AHAT_SD_AN),
                ("bootstrap on the 16 (aggressive)", AHAT_SD_BS)):
    print(f"      {lab:<44} z(MI) = {(EMI['canonical']-AHAT_OBS)/sd:+.2f}   "
          f"z(MG) = {(EMG['canonical']-AHAT_OBS)/sd:+.2f}")
z_mi_an = (EMI["canonical"] - AHAT_OBS) / AHAT_SD_AN
z_mg_an = (EMG["canonical"] - AHAT_OBS) / AHAT_SD_AN
check(z_mi_an > 2.0 and abs(z_mg_an) < 1.0,
      f"D4 *** THE UNCOMFORTABLE RESULT, AND IT IS THE MOST IMPORTANT NUMBER IN THIS FILE. *** On the "
      f"CONSERVATIVE ensemble error bar the in-hand 16-galaxy firing sits {z_mi_an:.2f} sigma BELOW the "
      f"framework's own modified-inertia prediction and {abs(z_mg_an):.2f} sigma from the QUMOND-class "
      f"MG prediction. On the sample's own bootstrap it is "
      f"{(EMI['canonical']-AHAT_OBS)/AHAT_SD_BS:.1f} sigma below MI. The measured +{AHAT_OBS} was banked as "
      f"'3x the AQUAL floor, inside the 1-5x loop-orbit bracket' -- read against MI it is a factor "
      f"{EMI['canonical']/AHAT_OBS:.1f} SHORT. This is exploratory (n = 16, the corpus's own framing) and I "
      f"did not re-run the pipeline; it is a flagged lead, not a kill. But it is a lead pointing the wrong "
      f"way for the framework's literal law, and it is cheap to settle")
sep_vs_B = (EMI["canonical"] - EMG["canonical"]) / (EMG["canonical"] * (1.0 - 0.27))
N_DIP_SCALE = COM_N_AQ_VS_B / sep_vs_B**2
N_DIP_SD = 16.0 * (3.0 / ((EMI["canonical"] - EMG["canonical"]) / AHAT_SD_AN)) ** 2
N_DIP = max(N_DIP_SCALE, N_DIP_SD)                     # carry the CONSERVATIVE one forward
print(f"\n  REQUIRED N, two independent ways because the answer is small enough to be suspicious:")
print(f"   (i)  scaling the committed N(3 sigma) = {COM_N_AQ_VS_B} (AQUAL-vs-BranchB, separation "
      f"E[Ahat] x (1 - 0.27)) by the {sep_vs_B:.2f}x wider MI-vs-MG separation  ->  {N_DIP_SCALE:.1f} galaxies")
print(f"   (ii) directly from the n = 16 firing's own analytic sd {AHAT_SD_AN}: the MI-MG gap is "
      f"{(EMI['canonical']-EMG['canonical'])/AHAT_SD_AN:.2f} sigma at n = 16, so 3 sigma needs "
      f"{N_DIP_SD:.1f}")
print(f"  The conservative one, {N_DIP:.0f} galaxies, is carried into the ranking.")
check(N_DIP < 237 and N_DIP_SD / N_DIP_SCALE < 3.0,
      f"D5 on separation-over-uncertainty this observable is not merely the best in the table, it is "
      f"ALREADY OVER-POWERED: the two estimates agree to a factor {N_DIP_SD/N_DIP_SCALE:.1f} and both are "
      f"tiny -- {N_DIP_SCALE:.0f} and {N_DIP_SD:.0f} galaxies against the 237 in the in-hand per-side "
      f"WALLABY crossmatch and the 16 already fired. NOTE the honest cost of that: an observable this "
      f"powerful is also an observable that can be LOST quickly, and D4 says the first 16 point the wrong "
      f"way")

# --- D6 an ALIGNMENT-FREE budget argument, which needs no matched filter at all
pmi = np.array([R_ * p / 100.0 for R_, p in
                zip([LA["asym_algebraic"](nu_ra_v, e, x, 0.0) / LA["asym_local"](sol_ra(e), x, 0.0)[0]
                     for _n, x, e, _p in FIRING], [p for _n, _x, _e, p in FIRING])])
A_MEAS = np.array([-0.0277, -0.1230, +0.0108, +0.0116, -0.0565, +0.0768, -0.0065, -0.1188,
                   +0.0795, +0.0642, -0.0192, -0.0039, +0.1294, -0.1355, -0.0563, +0.0712])
WHISP_RMS = WHISP_RMS_PRE                     # FIRST_FIRING.md convention 1, 70 WHISP galaxies
rms_mi, rms_meas = float(np.sqrt((pmi**2).mean())), float(np.sqrt((A_MEAS**2).mean()))
rms_mg = float(np.sqrt(((np.array([p for _n, _x, _e, p in FIRING]) / 100.0) ** 2).mean()))
print(f"\n  AND A BUDGET ARGUMENT THAT NEEDS NO ALIGNMENT STATISTIC AT ALL. The MI law's per-galaxy predicted")
print(f"  dipole on these 16 lines of sight has rms {rms_mi:.4f} and reaches {np.abs(pmi).max():.4f} at its")
print(f"  largest, against a MEASURED rms of {rms_meas:.4f} on the same 16 and the 70-galaxy WHISP")
print(f"  lopsidedness rms {WHISP_RMS} -- and that {WHISP_RMS} is the TOTAL, including intrinsic m = 1")
print(f"  asymmetry, warps, interactions and noise, of which an EFE dipole can only be one part.")
check(rms_mi > 1.5 * rms_meas and rms_mi > 0.8 * WHISP_RMS,
      f"D6 so the MI amplitude is in tension with the lopsidedness BUDGET, independently of any alignment: "
      f"its predicted aligned dipole alone has rms {rms_mi:.3f} = {rms_mi/rms_meas:.1f}x the total measured "
      f"rms of these 16 galaxies and {100*rms_mi/WHISP_RMS:.0f}% of the entire 70-galaxy lopsidedness rms. "
      f"The MG prediction, rms {rms_mg:.4f}, "
      f"sits comfortably inside it. This is a second, independent and cruder route to the same direction as "
      f"D4, and being cruder it is harder to escape: it uses no g_ext directions and no permutation null")


# ================================================================================================== R
banner("R  OBSERVABLES C AND D -- the non-spherical disc rotation curve, and the vertical/radial ratio")


def load_anchor(fname, cut_at):
    src = (HERE / fname).read_text()
    g = {"__name__": f"anchor_{fname}"}
    exec(compile(src[: src.index(cut_at)], str(HERE / fname), "exec"), g)   # noqa: S102
    return g


AK = load_anchor("mi_aqual_solve_framework_kernel_2026.py", 'banner("A0')
_cache: dict = {}


def aq_solve(mufun, a0, n=150, growth=1.06, newtonian=False):
    key = (id(mufun), a0, n, growth, newtonian)
    if key not in _cache:
        AK["mu_fw"] = mufun
        _cache[key] = AK["solve_aqual"](a0, n=n, growth=growth, newtonian=newtonian)
    return _cache[key]


print("  The SAME Miyamoto-Nagai + Hernquist baryons, the SAME a0 (an INPUT), two theories:")
print("    MG  : the full Bekenstein-Milgrom solve, v_c^2 = R |dPhi/dR| at z = 0")
print("    MI  : the pointwise algebraic map, v_c^2 = R nu(g_N/a0) g_N with the SAME analytic g_N")
Rc, zc, PhiN = aq_solve(mu_alpha2, A0_CANON, newtonian=True)
gN_mid = np.abs(np.gradient(PhiN[:, 0], Rc))
PROF = {}
for kn, (mf, _dmf, nf) in (("Route A (exp)", KERNELS["Route A (exp)"]),
                           ("alpha=2 (superseded)", KERNELS["alpha=2 (superseded)"])):
    for fl, a0 in FOOT.items():
        _, _, P = aq_solve(mf, a0)
        gA = np.abs(np.gradient(P[:, 0], Rc))
        PROF[(kn, fl)] = (gA, np.array([float(nf(g / a0)) * g for g in gN_mid]))
print("  (each column below = g_MG / g_MI at that radius; < 1 means the field solve is WEAKER than the map)")
print(f"  {'R [kpc]':>8}{'g_N/a0':>9}" + "".join(f"{k + ' ' + f:>20}"
                                                 for k in ("RouteA", "alpha=2") for f in FOOT))
sel = [(Rk, int(np.argmin(np.abs(Rc - Rk * KPC)))) for Rk in (2, 3, 5, 8, 12, 20, 30)]
for Rk, i in sel:
    row = "".join(f"{PROF[(k, f)][0][i]/PROF[(k, f)][1][i]:>20.4f}"
                  for k in ("Route A (exp)", "alpha=2 (superseded)") for f in FOOT)
    print(f"  {Rc[i]/KPC:>8.2f}{gN_mid[i]/A0_CANON:>9.3f}{row}")
inner = (Rc > 2 * KPC) & (Rc < 30 * KPC)
SPAN = {}
for k in ("Route A (exp)", "alpha=2 (superseded)"):
    for f in FOOT:
        r = PROF[(k, f)][0][inner] / PROF[(k, f)][1][inner]
        SPAN[(k, f)] = (float(r.min()), float(r.max()), float(r.max() - r.min()))
print(f"\n  {'kernel':<22}{'footing':<11}{'min g_MG/g_MI':>15}{'max':>9}{'peak-to-trough':>16}{'in dex':>9}")
for k in ("Route A (exp)", "alpha=2 (superseded)"):
    for f in FOOT:
        lo, hi, sp_ = SPAN[(k, f)]
        print(f"  {k:<22}{f:<11}{lo:>15.4f}{hi:>9.4f}{sp_:>16.4f}{math.log10(hi/lo):>9.4f}")
R1_FAC = SPAN[("Route A (exp)", "canonical")][2] / SPAN[("alpha=2 (superseded)", "canonical")][2]
check(R1_FAC > 1.5,
      f"R1 Route A WIDENS the disc AQUAL-vs-algebraic discrepancy by a factor {R1_FAC:.2f}: peak-to-trough "
      f"over 2-30 kpc grows from {SPAN[('alpha=2 (superseded)','canonical')][2]:.4f} (alpha=2) to "
      f"{SPAN[('Route A (exp)','canonical')][2]:.4f} in g, i.e. from "
      f"{math.log10(SPAN[('alpha=2 (superseded)','canonical')][1]/SPAN[('alpha=2 (superseded)','canonical')][0]):.4f} "
      f"to {math.log10(SPAN[('Route A (exp)','canonical')][1]/SPAN[('Route A (exp)','canonical')][0]):.4f} "
      f"dex. The sign is fixed: MG is WEAKER than the algebraic map in the inner disc and marginally "
      f"STRONGER outside ~17 kpc, so the difference is a radial RAMP, not an offset")
# grid systematic on that span -- the corpus has already been bitten by a mesh effect larger than a signal
Rc_c, zc_c, PhiN_c = aq_solve(mu_alpha2, A0_CANON, n=120, growth=1.08, newtonian=True)
gN_c = np.abs(np.gradient(PhiN_c[:, 0], Rc_c))
_, _, Pc = aq_solve(mu, A0_CANON, n=120, growth=1.08)
gA_c = np.abs(np.gradient(Pc[:, 0], Rc_c))
mi_c = np.array([float(nu(g / A0_CANON)) * g for g in gN_c])
selc = (Rc_c > 2 * KPC) & (Rc_c < 30 * KPC)
rc_ = gA_c[selc] / mi_c[selc]
span_c = float(rc_.max() - rc_.min())
print(f"  grid systematic: the same span on the coarse mesh (n = 120, growth 1.08) is {span_c:.4f} vs "
      f"{SPAN[('Route A (exp)','canonical')][2]:.4f} fine -- {abs(span_c/SPAN[('Route A (exp)','canonical')][2]-1):.1%}")
check(abs(span_c / SPAN[("Route A (exp)", "canonical")][2] - 1) < 0.30,
      f"R2 and the span is mesh-stable to {abs(span_c/SPAN[('Route A (exp)','canonical')][2]-1):.0%} between "
      f"two genuinely different meshes (growth 1.06 vs 1.08 -- in this solver growth, NOT n, is what "
      f"refines), so the doubling in R1 is physics and not discretisation. It is not a small systematic "
      f"either, and it is carried into the ranking")


def nu_pair(P, PN, Rgrid, zgrid, Rt, zk):
    """nu_rad and nu_vert at the SAME grid cell in R -- the consistent measurement of V3 in the anchor."""
    i = int(np.argmin(np.abs(Rgrid - Rt)))
    gR, gRn = np.gradient(P[:, 0], Rgrid), np.gradient(PN[:, 0], Rgrid)
    kv = abs(np.interp(zk * KPC, zgrid, np.gradient(P[i, :], zgrid)))
    kn = abs(np.interp(zk * KPC, zgrid, np.gradient(PN[i, :], zgrid)))
    return abs(gR[i]) / abs(gRn[i]), kv / kn


print(f"\n  OBSERVABLE D -- vertical/radial. The ALGEBRAIC MI law has nu_vert = nu_rad IDENTICALLY (one "
      f"scalar multiplies the whole vector g_N), so MI predicts EXACTLY 1 under every kernel.")
print(f"  {'kernel':<22}{'footing':<11}{'nu_rad':>9}{'nu_vert':>9}{'ratio':>9}{'MG-MI splitting':>18}")
VR = {}
for kn, (mf, _d, _n) in (("Route A (exp)", KERNELS["Route A (exp)"]),
                         ("alpha=2 (superseded)", KERNELS["alpha=2 (superseded)"])):
    for fl, a0 in FOOT.items():
        _, _, P = aq_solve(mf, a0)
        nr, nv = nu_pair(P, PhiN, Rc, zc, AK["R0"], 1.1)
        VR[(kn, fl)] = nv / nr
        print(f"  {kn:<22}{fl:<11}{nr:>9.4f}{nv:>9.4f}{nv/nr:>9.4f}{100*(nv/nr-1):>17.2f}%")
check(abs(VR[("alpha=2 (superseded)", "canonical")] - COM_NUVERT_A2) < 0.002,
      f"R3 the alpha=2 arm reproduces the committed comparator "
      f"{VR[('alpha=2 (superseded)','canonical')]:.4f} vs {COM_NUVERT_A2}, so the Route A value "
      f"{VR[('Route A (exp)','canonical')]:.4f} is like-for-like. The MG-vs-MI splitting on this observable "
      f"is {100*(VR[('Route A (exp)','canonical')]-1):.2f} pp, against a Bovy & Rix Sigma_dyn error bar of "
      f"4/68 = 5.9% and a Holmberg & Flynn 6/74 = 8.1% -- i.e. "
      f"{100*(VR[('Route A (exp)','canonical')]-1)/8.1:.2f}-"
      f"{100*(VR[('Route A (exp)','canonical')]-1)/5.9:.2f} sigma. NON-DIAGNOSTIC, confirming the banked "
      f"verdict for a reason the banked verdict did not state: MI's prediction here is exactly 1")


# ================================================================================================== T
banner("T  OBSERVABLE E -- the isolated deep-MOND two-body coefficient: a factor 3.3 in C, 1.35 in velocity")


def C_MI(q):
    """the algebraic map's deep limit, DERIVED below: V^4 = C G M a0, C = (sqrt(mu1)+sqrt(mu2))^2."""
    m1, m2 = 1.0 / (1.0 + q), q / (1.0 + q)
    return (math.sqrt(m1) + math.sqrt(m2)) ** 2


def C_AQ(q):
    """Milgrom arXiv:2503.07106 Eq (30): the isolated AQUAL/QUMOND-class deep-MOND two-body coefficient."""
    m1, m2 = 1.0 / (1.0 + q), q / (1.0 + q)
    return (4.0 / 9.0) * ((1.0 - m1**1.5 - m2**1.5) / (m1 * m2)) ** 2


print("  In the deep limit the algebraic map gives a_rel = sqrt(G a0)(sqrt(m1)+sqrt(m2))/r, hence")
print("  V^4 = G M a0 (sqrt(mu1)+sqrt(mu2))^2 -- which is Milgrom arXiv:2503.07106 Eq (31), his beta = 3/2")
print("  'pure MI' coefficient, reached here from the framework's own kernel and not borrowed.")
print(f"  {'q = m2/m1':>10}{'C_MI':>10}{'C_AQUAL':>10}{'C_MI/C_AQ':>11}{'V ratio':>10}")
for q in (1e-6, 1e-3, 0.01, 0.1, 0.3, 0.5, 1.0):
    print(f"  {q:>10g}{C_MI(q):>10.5f}{C_AQ(q):>10.5f}{C_MI(q)/C_AQ(q):>11.4f}{(C_MI(q)/C_AQ(q))**0.25:>10.5f}")
check(abs(C_MI(1e-6) - 1.0) < 3e-3 and abs(C_AQ(1e-6) - 1.0) < 3e-3,
      f"T1 THE CONTROL BOTH SIDES MUST PASS: in the test-particle limit q -> 0 both coefficients go to 1 "
      f"(C_MI = {C_MI(1e-6):.5f}, C_AQUAL = {C_AQ(1e-6):.5f}), i.e. both reduce to the BTFR V^4 = G M a0. "
      f"The two theories are indistinguishable for a test particle and separate only when both masses "
      f"matter -- which is the whole content of 'modified inertia is about the inertia of each body'")
worst_dml = 0.0
for q in (1.0, 0.5, 0.1):
    for a0 in FOOT.values():
        m1, m2 = MSUN, q * MSUN
        d = 3.0e17
        g1, g2 = G_N * m2 / d**2, G_N * m1 / d**2
        arel = float(nu(g1 / a0)) * g1 + float(nu(g2 / a0)) * g2
        worst_dml = max(worst_dml, abs((arel * d) ** 2 / (G_N * (m1 + m2) * a0) / C_MI(q) - 1))
check(worst_dml < 0.01,
      f"T2 and the closed form is not asserted: evaluating the Route A map directly at a separation deep in "
      f"the MOND regime reproduces C_MI over q = 0.1-1 and BOTH footings to {worst_dml:.2%} (the residual "
      f"is the kernel's own subleading term, nu = y^-1/2 + 1/2 + ...). Independently confirms Eq (31)")
check(C_MI(1.0) / C_AQ(1.0) > 3.0,
      f"T3 for an equal-mass pair the coefficients differ by {C_MI(1.0)/C_AQ(1.0):.2f} in C and "
      f"{(C_MI(1.0)/C_AQ(1.0))**0.25:.3f} in velocity, and in OPPOSITE DIRECTIONS relative to the "
      f"test-particle baseline C = 1: MI is FASTER (C = {C_MI(1.0):.2f}), AQUAL SLOWER "
      f"(C = {C_AQ(1.0):.2f}). A 35% velocity difference is enormous -- but it is a strictly ISOLATED "
      f"deep-MOND statement, and the Milky Way disc has g_ext ~ 1.9 a0 everywhere, so no Galactic wide "
      f"binary is in this regime. Its address is isolated galaxy PAIRS, where a stellar-mass error of "
      f"0.15 dex already costs {100*(10**0.15)**0.25-100:.0f}% in V and eats a third of the signal")


# ================================================================================================== X
banner("X  OBSERVABLE F -- NEWTON'S THIRD LAW: exactly satisfied by BM/AQUAL, violated by the algebraic map")

print(r"""  BM/AQUAL: mi_route_a_field_theory_2026 PROVED the Route A free function strictly convex, from which the
  theory inherits Newton's third law and standard centre-of-mass motion. The violation is EXACTLY ZERO.

  The algebraic map: apply a = nu(|g_N|/a0) g_N to each body of an isolated pair. The Newtonian parts of
  m1 a1 and m2 a2 cancel identically (m1 g1 = m2 g2 = G m1 m2/d^2), so what survives is
      a_cm = [G m1 m2 / (d^2 (m1+m2))] | (nu(y1) - 1) - (nu(y2) - 1) |
  written through nu - 1 because Route A's anomaly is e^-sqrt(y) and the naive subtraction nu(y) - 1
  rounds to exactly 0.0 past y ~ 1300 in float64. It vanishes only for m1 = m2.
""")


def a_cm(m1, m2, d, nfun, a0):
    y1, y2 = G_N * m2 / d**2 / a0, G_N * m1 / d**2 / a0
    return (G_N * m1 * m2 / (d**2 * (m1 + m2))) * abs(float(nfun(y1)) - float(nfun(y2)))


def a_cm_stable(m1, m2, d, a0):
    """Route A, through the log form: correct where nu - 1 underflows below the smallest normal."""
    from mi_route_a_kernel import log_nu_minus1
    y1, y2 = G_N * m2 / d**2 / a0, G_N * m1 / d**2 / a0
    t1, t2 = float(log_nu_minus1(y1)), float(log_nu_minus1(y2))
    hi = max(t1, t2)
    return (G_N * m1 * m2 / (d**2 * (m1 + m2))) * math.exp(hi) * abs(1.0 - math.exp(min(t1, t2) - hi))


CASES = [("1.0 + 0.5 Msun binary", 10 * KAU, MSUN, 0.5 * MSUN),
         ("1.0 + 0.5 Msun binary", 30 * KAU, MSUN, 0.5 * MSUN),
         ("galaxy pair 1e11 + 1e10", 100 * KPC, 1e11 * MSUN, 1e10 * MSUN),
         ("Sun + Jupiter", 5.2 * 1.496e11, MSUN, 9.55e-4 * MSUN)]
print(f"  {'system':<26}{'sep [m]':>11}{'kernel':>10}{'a_cm/a0 canon':>16}{'a_cm/a0 alt':>14}"
      f"{'dv per Gyr [m/s]':>18}")
XT = {}
for nm, d, m1, m2 in CASES:
    for kn, nf in (("Route A", nu), ("alpha=2", nu_alpha2), ("alpha=1", nu_alpha1)):
        vals = []
        for fl, a0 in FOOT.items():
            v = a_cm_stable(m1, m2, d, a0) if kn == "Route A" else a_cm(m1, m2, d, nf, a0)
            vals.append(v / a0)
        XT[(nm, d, kn)] = vals
        print(f"  {nm:<26}{d:>11.3e}{kn:>10}{vals[0]:>16.4e}{vals[1]:>14.4e}"
              f"{vals[0]*A0_CANON*GYR:>18.3e}")
check(XT[("1.0 + 0.5 Msun binary", 10 * KAU, "Route A")][0] > 0.05
      and XT[("Sun + Jupiter", 5.2 * 1.496e11, "Route A")][0] < 1e-15,
      f"X1 the algebraic map's third-law violation is a LOW-ACCELERATION pathology and Route A is exactly "
      f"the kernel that confines it there: {XT[('1.0 + 0.5 Msun binary', 10*KAU, 'Route A')][0]:.3f} a0 for "
      f"a 1+0.5 Msun pair at 10 kAU and "
      f"{XT[('galaxy pair 1e11 + 1e10', 100*KPC, 'Route A')][0]:.4f} a0 for an unequal galaxy pair, but "
      f"{XT[('Sun + Jupiter', 5.2*1.496e11, 'Route A')][0]:.2e} a0 for Sun + Jupiter, where alpha=1 gave "
      f"{XT[('Sun + Jupiter', 5.2*1.496e11, 'alpha=1')][0]:.3f} a0 -- the retired a0/2 ephemeris liability, "
      f"recovered here from a completely different direction as a third-law violation")
# is it observable? the CoM circulates rather than runs away, for a circular orbit
d10 = 10 * KAU
y1_, y2_ = G_N * 0.5 * MSUN / d10**2 / A0_CANON, G_N * MSUN / d10**2 / A0_CANON
arel = G_N * 1.5 * MSUN / d10**2 * (float(nu(y1_)) * (1 / 3) + float(nu(y2_)) * (2 / 3))
Om2 = arel / d10
wobble = a_cm_stable(MSUN, 0.5 * MSUN, d10, A0_CANON) / Om2 / d10
print(f"\n  IS IT OBSERVABLE? For a circular orbit the self-force lies along the rotating separation vector,")
print(f"  so the centre of mass CIRCULATES rather than runs away: amplitude a_cm/Omega^2 = "
      f"{wobble:.4f} x the separation, at the orbital period (~Myr).")
check(0.001 < wobble < 0.5,
      f"X2 so the separation between the two theories on this row is FORMALLY INFINITE (zero versus "
      f"{XT[('1.0 + 0.5 Msun binary', 10*KAU, 'Route A')][0]:.3f} a0) and OBSERVATIONALLY EMPTY: the "
      f"predicted signature is a {wobble:.1%}-of-separation centre-of-mass epicycle on a megayear "
      f"timescale, which nothing measures. It does not enter the ranking as an observable. What it does is "
      f"set the price of every MI row above -- see H")


# ================================================================================================== S
banner("S  (a) + (b) THE SCAN, RANKED BY SEPARATION OVER REALISTIC MEASUREMENT UNCERTAINTY")

vr_split = 100 * (VR[("Route A (exp)", "canonical")] - 1)
ROWS = [
    ("EFE aligned RC dipole (matched filter)", f"E[Ahat] {EMI['canonical']:.1f}",
     f"{EMG['canonical']:.2f}", f"x{sep_vs_B:.1f}, + sign flip e>2x",
     f"{N_DIP_SCALE:.0f}-{N_DIP_SD:.0f} galaxies; 237 in hand",
     f"{3*math.sqrt(237/N_DIP):.0f}-{3*math.sqrt(237/N_DIP_SCALE):.0f}"),
    ("wide-binary ORIENTATION anisotropy", f"{math.sqrt(r_mi):.4f}", f"{math.sqrt(r_aq):.4f}",
     f"OPPOSITE SIGN, {math.sqrt(r_aq)-math.sqrt(r_mi):.3f} in v", f"{NEEDED['AQUAL']:,.0f} pairs for 3 sig",
     f"{z30:.2f}"),
    ("isolated deep-MOND 2-body coefficient", f"C = {C_MI(1.0):.2f}", f"C = {C_AQ(1.0):.2f}",
     f"x{C_MI(1.0)/C_AQ(1.0):.2f} in C, x{(C_MI(1.0)/C_AQ(1.0))**0.25:.2f} in V",
     f"0.15 dex M_* -> {100*((10**0.15)**0.25-1):.0f}% in V",
     f"~{((C_MI(1.0)/C_AQ(1.0))**0.25 - 1)/((10**0.15)**0.25 - 1):.1f}"),
    ("disc RC shape, field solve vs the map", "ratio = 1 by construction",
     f"{SPAN[('Route A (exp)','canonical')][0]:.3f}-{SPAN[('Route A (exp)','canonical')][1]:.3f}",
     f"{math.log10(SPAN[('Route A (exp)','canonical')][1]/SPAN[('Route A (exp)','canonical')][0]):.3f} dex radial ramp",
     "0.005 dex ensemble; M/L absorbs most", "~1-3"),
    ("vertical/radial ratio at R0", "1.0000 EXACTLY", f"{VR[('Route A (exp)','canonical')]:.4f}",
     f"{vr_split:.2f} pp", "Sigma_dyn 5.9-8.1%", f"{vr_split/8.1:.2f}-{vr_split/5.9:.2f}"),
    ("wide-binary ORIENTATION-AVERAGED gamma_v", f"{gv_iso_mi:.4f}",
     f"{gv_aq:.4f} AQ / {gv_qm:.4f} QM", f"{abs(gv_iso_mi-gv_aq):.4f} AQ, {abs(gv_iso_mi-gv_qm):.5f} QM",
     f"sigma_tot {sig_tot:.4f} at N=30k",
     f"{abs(gv_iso_mi-gv_aq)/sig_tot:.2f} / {abs(gv_iso_mi-gv_qm)/sig_tot:.3f}"),
    ("Newton's third law / CoM self-accel", f"{XT[('1.0 + 0.5 Msun binary', 10*KAU, 'Route A')][0]:.3f} a0",
     "0 EXACTLY (convexity)", "formally infinite",
     f"no channel ({wobble:.0%}-of-sep epicycle)", "n/a"),
]
print(f"  {'observable':<40}{'MI':<26}{'MG (AQUAL/QUMOND)':<22}{'separation':<34}{'uncertainty':<36}"
      f"{'sep/sig'}")
print("  " + "-" * 186)
for r in ROWS:
    print(f"  {r[0]:<40}{r[1]:<26}{r[2]:<22}{r[3]:<34}{r[4]:<36}{r[5]}")

print(f"\n  (b) THE SINGLE BEST ONE, BY THE METRIC ASKED FOR: the ALIGNED EFE ROTATION-CURVE DIPOLE. It is")
print(f"  the only row already over-powered with data in hand ({N_DIP_SCALE:.0f}-{N_DIP_SD:.0f} galaxies needed, 237 crossmatched,")
print(f"  16 fired), and it separates MI from MG by a factor {sep_vs_B:.0f} in the pre-registered statistic")
print(f"  plus a sign flip over part of the map. THE RUNNER-UP IS THE MORE TRUSTWORTHY TEST and I would")
print(f"  spend the effort there: the wide-binary orientation anisotropy is a SIGN fork rather than an")
print(f"  amplitude comparison, needs no mass, no M/L and no eccentricity distribution, is unaffected by")
print(f"  any isotropic systematic, and carries its own in-survey null control at 1-5 kAU (W7).")
print(f"\n  AND THE TWO ROWS THAT MOVED AGAINST THE FRAMEWORK, stated as plainly as the two that helped:")
print(f"   * the pre-registered orientation-AVERAGED wide-binary gamma_v does not separate MI from MG at all:")
print(f"     {abs(gv_iso_mi-gv_qm)/sig_tot:.3f} sigma_tot against QUMOND (an exact degeneracy, W4d) and")
print(f"     {abs(gv_iso_mi-gv_aq)/sig_tot:.2f} sigma_tot against AQUAL. The committed "
      f"{abs(gv_iso_mi-COM_MGROW)/sig_tot:.2f} sigma was a separation from")
print(f"     the heuristic sqrt(nu(y_extN)) comparator, which is neither field theory (W4c).")
print(f"   * the in-hand n = 16 dipole firing sits {z_mi_an:.1f} sigma (conservative) below the framework's")
print(f"     own MI prediction and {abs(z_mg_an):.1f} sigma from MG's.")


banner("S2  (c) WHAT THE BEST ONE WOULD TAKE")
print(f"""  FOR THE DIPOLE (rank 1). Nothing new needs building; three things need doing.
   1. N. {N_DIP:.0f} galaxies with (i) a signed per-side rotation-curve asymmetry, (ii) an outer g_bar/a0,
      (iii) a reconstructed g_ext DIRECTION. In hand: 237 (prep_2026/wallaby_prep per-side crossmatch) and
      the 16 already fired. WALLABY DR2 and Apertif/WSRT-class HI surveys take that to 10^3.
   2. The MI predictor. The frozen pipeline's A_map is the QUMOND BVP map. An MI arm needs only
      asym_algebraic on the same (x_i, e_i) -- computed here for 16 galaxies in D3; extending it is minutes.
   3. THE OWED PIECE, and it can only move the verdict against the framework: the AQUAL loop-orbit
      amplification is 4.4-5.7x (committed). The algebraic map's loop-orbit response is NOT computed
      anywhere. If it is comparable, E[Ahat]_MI rises from {EMI['canonical']:.1f} to ~{5*EMI['canonical']:.0f}
      and the tension with the in-hand +{AHAT_OBS} grows from {z_mi_an:.1f} to ~{(5*EMI['canonical']-AHAT_OBS)/AHAT_SD_AN:.0f} sigma.
      If MI's response is instead SUPPRESSED, the tension shrinks. That integration is the single highest-
      value calculation this lane identifies, and I am flagging it precisely because I cannot predict which
      way it goes.

  FOR THE ANISOTROPY (rank 2, the one to bet on).
   1. N ~ {NEEDED['AQUAL']:,.0f} clean pairs at 3 sigma with the frozen per-pair scatter, rising to
      ~{SIG1**2/(VARC2P*((abs(BP['MI']-BP['AQUAL'])/3.0)**2-0.02**2)):,.0f} if an orientation-correlated systematic of 0.02 in B survives.
      El-Badry's Gaia DR3 wide-binary catalogue already holds ~1.3e6 candidates; the frozen 2-30 kAU clean
      cut is 3e4. DR4's longer astrometric baseline shrinks the per-pair velocity error, so N and sigma_1
      both improve. This is a DR4 measurement, not a next-decade one.
   2. PRECISION. The statistic is the amplitude B of a cos^2(psi) modulation, psi = angle between the
      sky-projected separation vector and the sky-projected Galactic-centre direction. Needed:
      sigma(B) < {abs(BP['MI']-BP['AQUAL'])/3.0:.4f}. Projection costs a flat factor D = {np.mean(Ds):.3f} (W8) and a full
      3D forward model recovers part of it.
   3. WHICH SURVEY. Gaia DR4 alone. The g_ext direction is the Galactic centre -- no external attractor
      reconstruction, no crossmatch, no distance ladder.
   4. THE SYSTEMATIC THAT MATTERS, named: Galactic tides shape wide-binary orientations and eccentricities,
      so the population's own orientation distribution is the confounder. W7 is the answer -- the 1-5 kAU
      pairs of the same catalogue have zero predicted signal in BOTH theories and measure that confounder
      directly.""")


# ================================================================================================== H
banner("H  (d) THE ASYMMETRY IN RIGOUR -- is the MI prediction genuine, or under-determined?")

print(f"""  Stated for the winner and the runner-up, without softening.

  THE MG SIDE IS PINNED. Route A's Bekenstein-Milgrom free function is derived in closed parametric form
  and PROVED strictly convex, ghost-free, strictly elliptic, subluminal and positive-phantom-density
  (mi_route_a_field_theory_2026, 11/11). From convexity it inherits existence, uniqueness, Newton's third
  law, standard centre-of-mass motion and a virial theorem. The deep-EFE anisotropy sqrt(1+L_mu) is the
  EXACT solution of the linearised field equation, verified here three independent ways (W2 sympy residual,
  W3 flux normalisation, W4 the QUMOND road agreeing in sign). Nothing about it is adjustable.

  THE MI SIDE IS NOT PINNED, in three specific ways.
   1. NO ACTION IN A DISC. Three no-goes (2026-08-01) close the action programme for this form class: the
      law is not variational in a disc, the u-contraction is (v/c)^2-suppressed for generic K, and that
      prefactor IS the worldline's Frenet torsion. Milgrom 2022 PRD 106:064060 builds MI at the level of
      the equations of motion with the explicit footnote that such theories "are not necessarily governed
      by an action" -- so the framework is entitled to that footing, but the footing carries no
      conservation theorems with it.
   2. IT VIOLATES NEWTON'S THIRD LAW, quantitatively: {XT[('1.0 + 0.5 Msun binary', 10*KAU, 'Route A')][0]:.3f} a0 for a 1+0.5 Msun pair at
      10 kAU (X1). A law with no conserved linear momentum is not a closed dynamical theory, and both
      winners' MI numbers are computed FROM that law.
   3. IT IS NOT THE ONLY MI REALISATION, and the alternatives disagree with it MAXIMALLY. Milgrom
      arXiv:2503.07106's linear/time-nonlocal MI has EXACT centre-of-mass decoupling (Eq 19-20), hence
      ZERO external-field effect: its wide-binary anisotropy is 1.0000 and its dipole is 0, and its
      two-body coefficient is C = 1 for ANY mass ratio (Eq 29) against the algebraic map's
      C = {C_MI(1.0):.2f}. So "MI" as a class spans par/perp in {{1.000, {r_mi:.3f}}}, dipole in {{0, E[Ahat] {EMI['canonical']:.1f}}}
      and C in {{1, {C_MI(1.0):.2f}}}.

  SO, FOR THE WINNER AND RUNNER-UP, PRECISELY:
   * the MI prediction is GENUINE as a prediction of THE FRAMEWORK'S OWN LITERAL ALGEBRAIC LAW. It is
     forced: no free function, no free parameter, footing-independent in the dimensionless ratio, and its
     SIGN cannot be tuned by the kernel (W5 proves it for any monotone mu). On that reading both tests are
     one-sided KILLS of the framework's law, and the dipole's already point that way (D4).
   * the MI prediction is UNDER-DETERMINED as a prediction of MODIFIED INERTIA AS A CLASS, because a
     legitimate MI realisation predicts the opposite extreme (zero). A null result therefore does NOT kill
     MI; it kills the algebraic reading and is simultaneously evidence against AQUAL/QUMOND.
   * the theory that is harder to pin down is NOT winning here. Every MI number in this file came out
     LARGER than its MG counterpart -- x{sep_vs_B:.0f} on the dipole, x{C_MI(1.0)/C_AQ(1.0):.1f} on the two-body coefficient -- and
     "larger" is what a measurement bites first. The under-determination is what makes a NULL uninformative
     about MI, not what makes a DETECTION favour it.

  THE THREE-WAY FORK, which is a cleaner falsification structure than most fronts in this corpus:
     par/perp > 1  ->  AQUAL/QUMOND-class MG; the framework's algebraic law is dead, kernel-independently.
     par/perp < 1  ->  a positive signature NO MG realisation in this class produces. A genuine MI win.
     par/perp = 1  ->  Milgrom's linear MI, or Newton. Evidence against the framework's law AND against
                       AQUAL/QUMOND at once.

  WHAT THIS FILE DOES NOT DO, so no one reads more into it than it earned:
   * no AQUAL solve at FINITE internal-to-external field ratio; the anisotropy comparison is a deep-EFE
     asymptotic statement and W7 shows it needs s >~ 15-20 kAU on the MI side. The MG side's approach to
     that asymptote is UNCOMPUTED.
   * the loop-orbit amplification of the MI dipole is UNCOMPUTED (S2 item 3) and could move D4's tension
     either way by a factor ~5.
   * the disc row is ONE baryon model (Miyamoto-Nagai + Hernquist) with a mesh systematic of
     {abs(span_c/SPAN[('Route A (exp)','canonical')][2]-1):.0%} on the very quantity being ranked.
   * the anisotropy forecast reuses the frozen sigma_fit as a per-pair scatter and scales it; that is an
     ensemble noise used as an ensemble noise, but it is a scaling, not a re-derived error model.
   * no door is closed by anything above, and nothing here bears on the RAR, the BTFR or the a0 line.""")

n_ok = sum(1 for t, _ in CHECKS if t)
print(f"\n  {n_ok}/{len(CHECKS)} checks held.")
if n_ok != len(CHECKS):
    for t, m in CHECKS:
        if not t:
            print(f"    FAILED: {m}")
    sys.exit(1)
print("  Exit 0.")
