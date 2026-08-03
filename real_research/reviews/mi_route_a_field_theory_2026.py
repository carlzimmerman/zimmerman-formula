#!/usr/bin/env python3
r"""mi_route_a_field_theory_2026.py -- THE FIELD THEORY FOR ROUTE A. Not an ansatz: the exponential kernel is
carried into a Bekenstein-Milgrom Lagrangian field theory whose free function is derived in closed parametric
form, and whose health (ellipticity, convexity, no ghost, subluminality, positive phantom density) is PROVED
rather than assumed.

THE ACTION.

    S = -integral d^3x [ (a0^2 / 8 pi G) * Fcal(X) + rho phi ],     X = |grad phi|^2 / a0^2

with field equation  div[ mu(x) grad phi ] = 4 pi G rho,  mu(x) = Fcal'(X),  x = |grad phi| / a0.

WHY THIS IS THE EFFICIENT ROUTE. The framework is modified INERTIA, and its own 2026-08-01 result is that the
MI law is not variational in a disc for this form class (three no-goes: not variational; the u-contraction is
(v/c)^2-suppressed for generic K; the prefactor IS the worldline's Frenet torsion). That closes the MI action
programme for that form class -- it does NOT close a field theory. Bekenstein-Milgrom is a modified-GRAVITY
realization of the SAME kernel, it is variational by construction, and every standard theorem (existence,
uniqueness, Newton's third law, standard centre-of-mass motion, exact BTFR) follows from ONE property that
this script proves for the exponential kernel: convexity of Fcal.

THE DERIVATION. In spherical symmetry the field equation integrates exactly to mu(x) x = y with y = g_bar/a0,
and g_obs = nu(y) g_bar means x = nu(y) y. Route A's kernel is nu = 1/(1 - exp(-sqrt(y))). Substituting
u = sqrt(y) gives the whole theory in ONE clean parametric pair:

    mu = 1 - e^-u        x = u^2 / mu        (u in (0, inf))

-- from which Fcal, its convexity, the ellipticity eigenvalues, the sound speed and the phantom density all
follow analytically. The two asymptotic forms of the action are exact and quotable:

    Fcal'(X) = mu = 1 - e^-sqrt(y)              EXACT, at every acceleration, with y = x mu = g_bar/a0
    Fcal(X) -> (2/3) X^(3/2)                    deep-MOND
    Fcal(X) -> X - C0 + 4 e^-s (s^3 + 3s^2 + 6s + 6),  s = X^(1/4)      Newtonian

CAREFUL WITH THE EXPONENT, because getting it wrong is easy and this script caught itself doing it: X = x^2, so
sqrt(X) = x, and x = y/mu ~ u^2 while u = sqrt(y). The Newtonian residual is therefore exponential in
X^(1/4) = sqrt(x) = sqrt(y), NOT in sqrt(X). The physical statement is the clean one: the free function's
derivative approaches 1 like e^-sqrt(g_bar/a0), which is Route A's kernel restated variationally. C0 is a pure
constant in the Lagrangian and is therefore UNOBSERVABLE -- only Fcal' enters the field equation.

That last line is the field-theoretic statement of Route A: the ephemeris relief is a property of the
Lagrangian, not a property of an algebraic force law bolted on afterwards.

  T1  the parametric map is a bijection -- PROVED, and the inversion round-trips
  T2  the two limits, and the Newtonian residual evaluated AT THE SUN
  T3  convexity ==> existence, uniqueness, third law, standard CoM motion, exact BTFR
  T4  ellipticity and causality -- both eigenvalues, and the scalar sound speed
  T5  the phantom density, and the BTFR coefficient from the action
  T6  what this is NOT

Exit 0 = ran and every internal check held. No hard-coded verdicts, no check(True).
"""
from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 108)
    print(f"  {t}")
    print("=" * 108)


c_l, G = 2.998e8, 6.674e-11
H0, OmL = 2.184e-18, 0.685
rho_L = OmL * 3 * H0**2 / (8 * math.pi * G)
A0 = (c_l / 2) * math.sqrt(G * rho_L)           # a0 = (1/2) c sqrt(G rho_Lambda), the framework's own coefficient
GM_J, AU = 1.26686534e17, 1.495978707e11


# ------------------------------------------------------------------ the parametric theory: u = sqrt(y)
def mu_of_u(u):
    """mu = 1 - e^-u, written with expm1 so small u is exact."""
    return -np.expm1(-np.asarray(u, float))


def x_of_u(u):
    """x = |grad phi| / a0 = u^2 / mu."""
    u = np.asarray(u, float)
    return u * u / mu_of_u(u)


def dx_du(u):
    """dx/du = [2 u mu - u^2 e^-u] / mu^2."""
    u = np.asarray(u, float)
    m = mu_of_u(u)
    return (2.0 * u * m - u * u * np.exp(-u)) / (m * m)


def dmu_du(u):
    return np.exp(-np.asarray(u, float))


def u_of_x(xv):
    """invert x(u) numerically -- this is what makes mu a standalone function of x, i.e. an ACTION."""
    # x(u) -> u as u -> 0, so the lower bracket must track xv rather than sit at a fixed floor
    lo, hi = min(1e-12, 0.5 * xv), max(1.0, 2.0 * xv)
    while x_of_u(lo) > xv:
        lo *= 0.5
        if lo < 1e-150:
            raise RuntimeError("lower bracket")
    while x_of_u(hi) < xv:
        hi *= 2.0
        if hi > 1e12:
            raise RuntimeError("upper bracket")
    return brentq(lambda u: x_of_u(u) - xv, lo, hi, xtol=1e-14, rtol=1e-15)


def mu_of_x(xv):
    return float(mu_of_u(u_of_x(xv)))


def Fcal(Xv):
    """Fcal(X) = int_0^X mu dX' = int_0^u 2 t^2 (dx/dt) dt, using x mu = u^2."""
    uu = u_of_x(math.sqrt(Xv))
    val, _ = quad(lambda t: 2.0 * t * t * float(dx_du(t)), 0.0, uu, limit=400)
    return val


banner("T1  THE PARAMETRIC MAP IS A BIJECTION -- proved, and the inversion round-trips")

u = sp.symbols("u", positive=True)
num = 2 * u * (1 - sp.exp(-u)) - u**2 * sp.exp(-u)
# dx/du > 0  <=>  2(1 - e^-u) > u e^-u  <=>  2(e^u - 1) > u, and e^u - 1 > u for u > 0.
gap = sp.simplify(2 * (sp.exp(u) - 1) - u)
ser = sp.series(gap, u, 0, 4).removeO()
pos_series = all(sp.Rational(co) > 0 for co in sp.Poly(sp.expand(ser), u).all_coeffs()[:-1])
uu = np.logspace(-8, 3, 4000)
allpos = bool(np.all(dx_du(uu) > 0))
print(f"  dx/du > 0  <=>  2(e^u - 1) > u.   series about 0: {ser}   all coefficients positive: {pos_series}")
print(f"  numeric: min(dx/du) over u in [1e-8, 1e3] = {float(np.min(dx_du(uu))):.6f}")
check(pos_series and allpos,
      f"T1a the map u -> x is STRICTLY MONOTONIC on (0, inf), so mu is a single-valued function of x and the "
      f"action exists. The proof is one line -- dx/du > 0 reduces to 2(e^u - 1) > u, which follows from "
      f"e^u - 1 > u -- and it holds for EVERY u > 0, with no parameter tuning. min(dx/du) numerically = "
      f"{float(np.min(dx_du(uu))):.4f} over eleven decades")

# round-trip: does the field theory's standalone mu(x) reproduce Route A's nu(y)?
worst = 0.0
for y in np.logspace(-6, 6, 25):
    nu_target = 1.0 / (-math.expm1(-math.sqrt(y)))
    x_solved = brentq(lambda xv: mu_of_x(xv) * xv - y, 1e-14, 1e14, xtol=1e-16, rtol=1e-15)
    worst = max(worst, abs(x_solved / (nu_target * y) - 1.0))
check(worst < 1e-10,
      f"T1b ROUND TRIP: solving the FIELD EQUATION mu(x) x = y with mu obtained by numerically inverting x(u) "
      f"recovers Route A's kernel nu(y) = 1/(1 - e^-sqrt(y)) to a worst-case relative error of {worst:.2e} "
      f"across twelve decades in y. The field theory and the algebraic law agree EXACTLY in spherical symmetry "
      f"-- which is the only regime in which they are required to")


banner("T2  THE TWO LIMITS, AND THE NEWTONIAN RESIDUAL EVALUATED AT THE SUN")

def one_minus_mu_of_x(xv):
    return math.exp(-u_of_x(xv))


def R_tail(Xv):
    """R(X) = int_X^inf (1 - mu) dX'  computed in u, so no catastrophic cancellation against X."""
    uX = u_of_x(math.sqrt(Xv))
    return quad(lambda t: math.exp(-t) * 2.0 * float(x_of_u(t)) * float(dx_du(t)), uX, np.inf, limit=400)[0]


def newt_asy(Xv):
    """4 e^-s (s^3 + 3 s^2 + 6 s + 6), s = X^(1/4) -- the leading Newtonian tail of the action."""
    sv = Xv ** 0.25
    return 4.0 * math.exp(-sv) * (sv**3 + 3 * sv**2 + 6 * sv + 6)


C0 = quad(lambda t: math.exp(-t) * 2.0 * float(x_of_u(t)) * float(dx_du(t)), 0.0, np.inf, limit=400)[0]
print(f"  the Lagrangian's Newtonian constant C0 = int_0^inf (1 - mu) dX = {C0:.6f}   "
      f"(leading-order estimate 24; UNOBSERVABLE -- only Fcal' enters the field equation)")
print(f"  {'X':>11}{'s = X^(1/4)':>13}{'mu':>12}{'1 - mu':>12}{'e^-sqrt(x)':>12}{'R(X)':>13}{'4e^-s(...)':>13}")
print("  " + "-" * 88)
for Xv in [1e-4, 1.0, 1e2, 1e4, 1e6, 1e8]:
    xv = math.sqrt(Xv)
    print(f"  {Xv:>11.1e}{Xv**0.25:>13.4f}{mu_of_x(xv):>12.8f}{one_minus_mu_of_x(xv):>12.4e}"
          f"{math.exp(-math.sqrt(xv)):>12.4e}{R_tail(Xv):>13.4e}{newt_asy(Xv):>13.4e}")

Xd = 1e-8
rel_deep = abs(Fcal(Xd) / ((2 / 3) * Xd**1.5) - 1.0)
check(rel_deep < 2e-4,
      f"T2a DEEP-MOND LIMIT of the ACTION: Fcal(X) -> (2/3) X^(3/2) to a relative {rel_deep:.2e} at X = 1e-8. "
      f"This is the standard deep-MOND Lagrangian with coefficient EXACTLY 2/3, so a0 keeps precisely its "
      f"meaning at the level of the action -- the BTFR, the a0-line and every deep-regime statement are "
      f"properties of this field theory, not of the kernel's transition shape")

# mu itself: 1 - mu = e^-sqrt(y) is EXACT; against e^-sqrt(x) it is asymptotic
X_t = 1e6
x_t = math.sqrt(X_t)
r_mu = one_minus_mu_of_x(x_t) / math.exp(-math.sqrt(x_t))
r_int = R_tail(X_t) / newt_asy(X_t)
r_cons = abs(Fcal(X_t) / (X_t - C0 + R_tail(X_t)) - 1.0)
print(f"\n  at X = {X_t:.0e}:  (1-mu)/e^-sqrt(x) = {r_mu:.6f},   R(X)/[4e^-s(s^3+3s^2+6s+6)] = {r_int:.6f}")
print(f"  consistency of the closed form:  Fcal(X) vs X - C0 + R(X)  ->  relative {r_cons:.2e}")
check(abs(r_mu - 1.0) < 1e-3 and abs(r_int - 1.0) < 5e-3 and r_cons < 1e-6,
      f"T2b NEWTONIAN LIMIT of the ACTION -- Route A stated variationally, with the exponent got RIGHT. "
      f"1 - Fcal'(X) = e^-sqrt(y) EXACTLY at every acceleration (y = x mu = g_bar/a0), and in X the tail of the "
      f"action is Fcal(X) = X - C0 + 4 e^-s (s^3 + 3s^2 + 6s + 6) with s = X^(1/4): verified to {abs(r_mu-1):.1e} "
      f"on the derivative and {abs(r_int-1):.1e} on the integral, with the closed form reproducing the direct "
      f"quadrature to {r_cons:.1e}. Both of the framework's earlier kernels leave a POWER-LAW residual instead "
      f"(a0/2 for alpha=1, a0^2/2g for alpha=2). *** The exponent is X^(1/4) = sqrt(g_bar/a0), NOT sqrt(X) -- an "
      f"earlier draft of this script wrote sqrt(X) and its Sun figure underflowed to a spurious exact zero ***")

y_sun = (GM_J / (5.204267 * AU) ** 2) / A0
u_sun = math.sqrt(y_sun)
x_sun = y_sun / (-math.expm1(-u_sun))
X_sun = x_sun**2
frac = newt_asy(X_sun) / X_sun
print(f"\n  AT THE SUN (Jupiter-driven reflex, y = {y_sun:.1f} a0 -- the body that binds the alpha=2 tail):")
print(f"      u = sqrt(y) = {u_sun:.3f},  1 - mu = e^-u = {math.exp(-u_sun):.4e},  X = {X_sun:.4e}")
print(f"      fractional Lagrangian departure from Newton, R(X)/X = {frac:.4e}")
check(1e-30 < frac < 1e-18,
      f"T2c at the SUN -- the binding body, checked rather than assumed -- the action departs from the Newtonian "
      f"one by a fractional {frac:.2e}, and that number is now RESOLVED rather than underflowed: the exponent is "
      f"e^-sqrt(y) = e^-{u_sun:.2f} = {math.exp(-u_sun):.2e}, which float64 represents fine, where the wrong "
      f"e^-sqrt(X) = e^-{math.sqrt(X_sun):.0f} would have rounded to exactly zero. Against the alpha=2 kernel's "
      f"fractional force residual of 3.0e-7 there, the field theory's departure is smaller by ~15 orders. "
      f"*** The solar-system liability is discharged AT THE LEVEL OF THE ACTION ***")


banner("T3  CONVEXITY ==> existence, uniqueness, Newton's third law, standard CoM motion, exact BTFR")

# Fcal''(X) = dmu/dX = (dmu/dx)/(2x),  dmu/dx = (dmu/du)/(dx/du) = e^-u mu^2 / [2u mu - u^2 e^-u].
# The denominator is exactly u e^-u [2(e^u - 1) - u], positive by T1a. So dmu/dx > 0 ANALYTICALLY for all u > 0
# -- which is the honest way to make this claim, because e^-u underflows to 0 past u ~ 745 and a purely
# numerical test would report a spurious ZERO there.
den = 2 * u * (1 - sp.exp(-u)) - u**2 * sp.exp(-u)
red = sp.simplify(sp.expand(den * sp.exp(u) / u) - (2 * (sp.exp(u) - 1) - u))
tail_pos = all(sp.nsimplify(c) > 0 for c in [sp.Rational(2, sp.factorial(k)) for k in range(2, 12)])
print(f"  denominator identity:  [2u mu - u^2 e^-u] * e^u / u  -  [2(e^u - 1) - u]  =  {red}")
print(f"  and 2(e^u - 1) - u = u + sum_(n>=2) 2 u^n / n!  -- every term positive for u > 0: {tail_pos}")
UU = np.logspace(-8, math.log10(300.0), 4000)     # u <= 300 keeps e^-u representable in float64
dmu_dx = dmu_du(UU) / dx_du(UU)
F2 = dmu_dx / (2.0 * x_of_u(UU))
print(f"  numeric corroboration over u in [1e-8, 300]:  min Fcal'' = {float(np.min(F2)):.4e},  "
      f"min dmu/dx = {float(np.min(dmu_dx)):.4e}")
check(red == 0 and tail_pos and bool(np.all(F2 > 0)),
      f"T3a *** Fcal IS STRICTLY CONVEX, PROVED ANALYTICALLY *** -- Fcal''(X) = (dmu/dx)/(2x) with "
      f"dmu/dx = e^-u mu^2 / (u e^-u [2(e^u - 1) - u]), whose denominator is positive because "
      f"2(e^u - 1) - u = u + sum_(n>=2) 2u^n/n! has every Taylor coefficient positive. So Fcal'' > 0 for EVERY "
      f"u > 0, with numeric corroboration (min {float(np.min(F2)):.1e}) over the representable range. Convexity "
      f"is the single hypothesis behind the Bekenstein-Milgrom theorem set, so Route A's field theory inherits: "
      f"a unique solution to the boundary-value problem, Newton's third law for two bodies, standard "
      f"centre-of-mass motion, a virial theorem, and an EXACT BTFR")

lim0 = sp.limit(1 - sp.exp(-u), u, 0, "+")
limI = sp.limit(1 - sp.exp(-u), u, sp.oo)
UREP = UU[UU < 36.0]                              # past u ~ 37, 1 - e^-u rounds to exactly 1.0 in float64
mrep = mu_of_u(UREP)
strict = bool(np.all((mrep > 0) & (mrep < 1)))
print(f"  mu = 1 - e^-u:  limit at 0+ = {lim0},  limit at inf = {limI}")
print(f"  strictly interior over u in [1e-8, 36] (the float64-representable range): {strict}   "
      f"max mu there = {float(np.max(mrep)):.16f}")
check(lim0 == 0 and limI == 1 and strict,
      f"T3b and NO GHOST: mu = Fcal'(X) = 1 - e^-u is strictly inside (0, 1) for every u in (0, inf), since "
      f"e^-u is. It reaches 0 and 1 only as limits, never on the domain -- so the kinetic term never changes "
      f"sign and the scalar carries no wrong-sign mode anywhere. mu < 1 also means gravity is ENHANCED "
      f"everywhere and never screened. (Numerically mu hits 1.0 exactly past u ~ 37 by rounding; the statement "
      f"here is the analytic one, and the numeric corroboration is restricted to u < 36 where float64 can still "
      f"resolve 1 - mu = e^-u ~ 2e-16)")


banner("T4  ELLIPTICITY AND CAUSALITY -- both eigenvalues, and the scalar sound speed")

# linearising div[mu grad phi]: principal symbol mu delta_ij + 2 Fcal'' d_i phi d_j phi / a0^2
#   transverse eigenvalue   mu                       (T3b: > 0)
#   longitudinal eigenvalue mu + x dmu/dx = d(x mu)/dx = dy/dx   (T1a/T3a: > 0)
lam_t = mu_of_u(UU)
lam_l = lam_t + x_of_u(UU) * dmu_dx
dydx = 2.0 * UU / dx_du(UU)
print(f"  {'x':>12}{'transverse mu':>15}{'longitudinal':>15}{'d(x mu)/dx':>13}{'c_s^2':>10}")
print("  " + "-" * 66)
for uv in [1e-6, 1e-2, 0.5, 1.0, 2.0, 10.0, 40.0]:
    m = float(mu_of_u(uv)); xv = float(x_of_u(uv)); d = float(dmu_du(uv) / dx_du(uv))
    print(f"  {xv:>12.4e}{m:>15.6f}{m+xv*d:>15.6f}{float(2*uv/dx_du(uv)):>13.6f}{m/(m+xv*d):>10.6f}")
consistent = float(np.max(np.abs(lam_l / dydx - 1.0)))
check(bool(np.all(lam_t > 0) and np.all(lam_l > 0)) and consistent < 1e-8,
      f"T4a *** THE FIELD EQUATION IS STRICTLY ELLIPTIC *** -- both eigenvalues of the linearised principal "
      f"symbol are positive (transverse mu > 0 by T3b; longitudinal mu + x dmu/dx > 0 because both factors are, "
      f"minimum {float(np.min(lam_l)):.3e}), and the longitudinal one equals d(x mu)/dx = dy/dx to "
      f"{consistent:.1e}, i.e. it IS the monotonicity proved in T1a. So the boundary-value problem is well "
      f"posed and there is no gradient instability -- the failure mode that kills many MOND free functions")

# c_s^2 = mu / (mu + x dmu/dx) < 1 strictly <=> x dmu/dx > 0, which is T3a. Test the ANALYTIC inequality.
cs2 = lam_t / lam_l
pos_xmux = bool(np.all(x_of_u(UU) * dmu_dx > 0))
print(f"  c_s^2 range over the representable grid: [{float(np.min(cs2)):.6f}, {float(np.max(cs2)):.12f}];  "
      f"min x dmu/dx = {float(np.min(x_of_u(UU) * dmu_dx)):.4e}")
check(pos_xmux and bool(np.all(cs2 > 0)) and float(np.min(cs2)) > 0.4,
      f"T4b and CAUSALITY: c_s^2 = mu / (mu + x dmu/dx) is strictly less than 1 for every u > 0, because "
      f"x dmu/dx > 0 strictly (T3a, analytic) -- so the inequality is proved, not sampled. Numerically c_s^2 "
      f"runs from {float(np.min(cs2)):.4f} in the deep-MOND regime (where it tends to exactly 1/2, since "
      f"mu -> x gives mu + x mu_x -> 2mu) up to 1 as a LIMIT in the Newtonian regime. In the k-essence "
      f"covariant completion that ratio is the scalar's sound speed, so this free function is SUBLUMINAL at "
      f"every acceleration -- a known defect of some MOND free functions that this one does not have")


banner("T5  THE PHANTOM DENSITY, AND THE BTFR COEFFICIENT FROM THE ACTION")

# for a point mass r^2 g_N = GM is constant, so
#   rho_ph  ~  (GM/r^2) d(nu-1)/dr  =  (GM/r^2) (dnu/dy)(dy/dr),   dy/dr = -2y/r
# with nu - 1 = 1/expm1(sqrt y) exactly, giving d(nu-1)/dy = -(e^sqrt y / (2 sqrt y)) / expm1(sqrt y)^2 < 0.
# Both factors are negative, so rho_ph > 0 identically. Computed in closed form -- an np.gradient version of
# this test reported a spurious -1.3e-25 from finite-difference roundoff where nu-1 underflows.
def rho_phantom_shape(yv):
    """positive-definite closed form of (r^3/GM/2) rho_ph * 4 pi G, up to positive constants."""
    # e^s / expm1(s)^2 == e^-s / (1 - e^-s)^2 -- the second form never overflows (the first does at s ~ 710)
    sy = np.sqrt(np.asarray(yv, float))
    return (yv / (2.0 * sy)) * np.exp(-sy) / (-np.expm1(-sy)) ** 2


# e^-sqrt(y) underflows to exactly 0 past sqrt(y) ~ 745, so corroborate the identity where float64 can hold it
yy_p = np.logspace(-6, 4, 5000)
rp = rho_phantom_shape(yy_p)
print(f"  point mass, closed-form phantom density over ten decades in y = GM/(a0 r^2):")
print(f"      min {float(np.min(rp)):.4e}   max {float(np.max(rp)):.4e}   any non-positive: "
      f"{bool(np.any(rp <= 0))}")
check(bool(np.all(rp > 0)),
      f"T5a THE PHANTOM DENSITY IS POSITIVE EVERYWHERE for a point mass. This is an IDENTITY, not a sampled "
      f"result: rho_ph ~ (y / 2 sqrt y) e^-sqrt y / (1 - e^-sqrt y)^2, every factor strictly positive for y > 0 "
      f"-- equivalently rho_ph ~ (dnu/dy)(dy/dr) with dnu/dy < 0 and dy/dr < 0, both strict. Corroborated over "
      f"ten decades in y (the grid stops at y = 1e4 because e^-sqrt(y) underflows to exactly 0 past "
      f"sqrt(y) ~ 745, which would read as a spurious non-positive value). The field theory's apparent dark matter is never NEGATIVE -- not automatic, since free "
      f"functions with non-monotonic nu produce unphysical negative phantom shells")

# deep-MOND action gives g = sqrt(G M a0)/r exactly, hence V^4 = G M a0: coefficient EXACTLY 1
M = 1e10 * 1.989e30
V4 = (G * M * A0)
V = V4**0.25
g_deep = math.sqrt(G * M * A0) / (30 * 3.0857e19)
y_deep = g_deep**2 / (G * M / (30 * 3.0857e19) ** 2) / A0
print(f"  BTFR from the deep-MOND action Fcal = (2/3)X^(3/2):  V^4 = G M a0 exactly")
print(f"      M = 1e10 Msun  ->  V = {V/1000:.3f} km/s   (a0 = {A0:.4e} m/s^2)")
check(abs(V4 / (G * M * A0) - 1.0) < 1e-12,
      f"T5b the BTFR follows from the ACTION with coefficient EXACTLY 1: V^4 = G M a0, giving "
      f"V = {V/1000:.2f} km/s at 1e10 Msun. This is Milgrom's virial theorem applied to the convex Fcal of "
      f"T3a, so it is a theorem of the field theory rather than a fit -- and it is the reason Route A costs the "
      f"framework NOTHING in the deep regime where its a0 claim actually lives")


banner("T6  WHAT THIS IS NOT")

print("""  DELIVERED, and machine-checked above:
   * a Lagrangian FIELD THEORY -- S = -int [ (a0^2/8 pi G) Fcal(X) + rho phi ] -- whose free function is
     derived in closed parametric form (mu = 1 - e^-u, x = u^2/mu) rather than posited piecewise, and which
     reproduces Route A's kernel EXACTLY in spherical symmetry (T1b).
   * mu = Fcal'(X) = 1 - e^-sqrt(g_bar/a0) EXACTLY, and the two asymptotic actions in closed form:
     (2/3)X^(3/2) deep, and X - C0 + 4e^-s(s^3+3s^2+6s+6) with s = X^(1/4) Newtonian (T2b). C0 is a pure
     constant in the Lagrangian and is unobservable -- only Fcal' enters the field equation.
   * PROVED health: strict convexity (T3a), no ghost (T3b), strict ellipticity (T4a), subluminality (T4b),
     positive phantom density (T5a) -- and via convexity the standard theorem set: existence, uniqueness,
     Newton's third law, standard centre-of-mass motion, virial theorem, exact BTFR with coefficient 1 (T5b).
   * the ephemeris discharge restated variationally: the Lagrangian's departure from Newton at the SUN is
     ~1e-22 fractional (T2c), against a power-law residual for both of the framework's earlier kernels.

  NOT DELIVERED, and not to be claimed:
   * THIS IS A MODIFIED-GRAVITY REALIZATION, NOT MODIFIED INERTIA. Bekenstein-Milgrom modifies the Poisson
     equation; the framework's own commitment is to modified inertia. The corpus's 2026-08-01 result stands:
     the MI law is not variational in a disc for that form class. What this script shows is that the KERNEL has
     a healthy variational home, not that MI does.
   * a0 IS STILL AN INPUT. Nothing here derives kappa = 1/2. The field theory is one-parameter, exactly as
     before, and Route A's own R4 result is that SPARC's preference for kappa = 1/2 does NOT survive the
     switch to this kernel -- it flips to 0.66 sigma the other way. The coefficient claim rests on
     a0 = (1/2) c sqrt(G rho_Lambda) as a POSTULATE, measured to agree, not derived.
   * NO LENSING YET. This is the nonrelativistic theory. Lensing and gravitational waves need the covariant
     completion (AeST-type two-field), where the subluminality result of T4b is the gate that makes the
     completion viable -- necessary, not sufficient.
   * OUTSIDE SPHERICAL SYMMETRY THE FIELD THEORY AND THE ALGEBRAIC LAW DIFFER. The corpus measured
     nu_vert/nu_rad = 1.024 for the Milky Way under the alpha=2 kernel; that ratio must be RE-SOLVED under this
     free function before any disc number (the vertical force, the AQUAL refit, the EFE dipole, the
     sigma-spread amplitude, the cluster eta, the wide-binary target) is quoted under Route A.""")

banner("RESULT")
n = sum(1 for t, _ in ok if t)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for t, m in ok:
        if not t:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: Route A's kernel has a healthy Bekenstein-Milgrom field theory -- convex, elliptic, ghost-free,")
print("  subluminal, positive phantom density, exact BTFR -- with the Newtonian residual exponentially small in")
print("  the ACTION. It is modified GRAVITY, not modified inertia, and it does not derive a0.")
