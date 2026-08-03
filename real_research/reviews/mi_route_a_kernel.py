#!/usr/bin/env python3
r"""mi_route_a_kernel.py -- THE SINGLE SOURCE OF TRUTH for Route A's kernel, importable by every disc re-solve.

Route A replaces the framework's power-law approach to Newton with an EXPONENTIAL one. Adopted 2026-08-02 after
`mi_route_a_exponential_kernel_2026.py` (9/9) priced the trade and `mi_route_a_field_theory_2026.py` (11/11)
built the Bekenstein-Milgrom field theory and proved its health.

THE KERNEL, in the two forms the corpus needs:

  nu(y)  = 1 / (1 - e^-sqrt(y))          y = g_bar / a0      -- the ALGEBRAIC / modified-inertia form
  mu(x)  defined parametrically by                            -- the FIELD-THEORY / AQUAL form
      mu = 1 - e^-u        x = u^2 / mu        u = sqrt(y)

These are the SAME kernel: in spherical symmetry the AQUAL field equation integrates to mu(x) x = y, so
x = nu(y) y and the two forms are exact inverses of each other. Outside spherical symmetry they DIFFER, which
is exactly why the disc numbers have to be re-solved rather than rescaled.

WHY A MODULE. An AQUAL Picard solve calls mu(x) on the order of 10^7 times. A brentq inversion per call is
unusable, so mu_exp() inverts x(u) by a table lookup refined with Newton steps -- vectorized, and validated
against brentq to machine precision by this file's own self-test. Every disc re-solve imports from here so
that a single definition of the kernel is in force everywhere.

NUMERICAL LANDMINES, all of which have already bitten this corpus once:
  * 1 - exp(-47.25) rounds to exactly 1.0 in float64. Use nu_minus1() / one_minus_mu(), never nu(y) - 1.
  * e^-u underflows to exactly 0 past u ~ 745, so strict inequalities on mu read as equalities at large u.
  * the Newtonian residual is exponential in sqrt(y) = X^(1/4), NOT in sqrt(X) = x.

Run directly to execute the self-test.
"""
from __future__ import annotations

import math

import numpy as np

# ------------------------------------------------------------------ the two a0 footings, unchanged by Route A
C_L, G_N = 2.998e8, 6.674e-11
H0, OM_L = 2.184e-18, 0.685
RHO_L = OM_L * 3 * H0**2 / (8 * math.pi * G_N)
Z_FW = 2 * math.sqrt(8 * math.pi / 3)                      # Z = 2 sqrt(8 pi / 3) = sqrt(32 pi / 3)
A0_CANON = (C_L / 2) * math.sqrt(G_N * RHO_L)              # 9.3614e-11  -- rho_DE / cH_Lambda, kappa = 1/2
A0_ALT = 1.13e-10                                          # rho_total / cH0
A0_M20 = A0_CANON * Z_FW / (2 * math.pi)                   # Milgrom 2020's kappa = 1/2pi on the same cH_Lambda
A0 = {"canon": A0_CANON, "alt": A0_ALT}


# ------------------------------------------------------------------ nu(y): the algebraic form
def nu(y):
    """nu = 1 / (1 - e^-sqrt(y)),  y = g_bar/a0.  g_obs = nu(y) g_bar."""
    return 1.0 / -np.expm1(-np.sqrt(np.asarray(y, float)))


def log_nu_minus1(y):
    """log(nu - 1) = -s - log1p(-e^-s), s = sqrt(y). Never overflows or underflows.

    Past y ~ 5e5 the anomaly nu - 1 = e^-sqrt(y) is smaller than float64's smallest normal (~1e-308), so at
    solar-system accelerations it is not merely tiny but UNREPRESENTABLE. Any ephemeris-scale statement must be
    made through this function; nu_minus1() will correctly return 0.0 there and that 0.0 is an underflow, not
    a physical zero.
    """
    s = np.sqrt(np.asarray(y, float))
    return -s - np.log1p(-np.exp(-s))


def nu_minus1(y):
    """nu - 1 = 1 / expm1(sqrt(y)), evaluated through the log form so it neither overflows nor warns.

    STABLE where `nu(y) - 1` is not: that subtraction rounds to exactly 0.0 past y ~ 1300 because
    1 - exp(-37) is 1.0 in float64. Underflows to 0.0 past y ~ 5e5 -- use log_nu_minus1() there.
    """
    return np.exp(log_nu_minus1(y))


# ------------------------------------------------------------------ mu(x): the AQUAL form
def _mu_of_u(u):
    return -np.expm1(-np.asarray(u, float))


def _x_of_u(u):
    u = np.asarray(u, float)
    return u * u / _mu_of_u(u)


_UG = np.logspace(-12.0, 6.0, 400001)
_XG = _x_of_u(_UG)
_LU, _LX = np.log(_UG), np.log(_XG)


def u_of_x(x):
    """invert x = u^2/(1 - e^-u) for u: log-space table lookup + 3 Newton steps. Vectorized."""
    x = np.asarray(x, float)
    u = np.exp(np.interp(np.log(x), _LX, _LU))
    for _ in range(4):
        e = np.exp(-u)
        f = u * u + x * np.expm1(-u)                       # F(u) = u^2 - x(1 - e^-u); -expm1(-u) is exact
        fp = 2.0 * u - x * e                               #   at small u where (1.0 - e) loses ~8 digits
        u = u - np.where(fp != 0.0, f / fp, 0.0)
        u = np.clip(u, 1e-300, None)
    return u


def mu(x):
    """mu(x) = 1 - e^-u(x), the AQUAL interpolating function. mu -> x deep, mu -> 1 Newtonian."""
    return _mu_of_u(u_of_x(x))


def one_minus_mu(x):
    """1 - mu = e^-u(x) -- STABLE where mu itself saturates to 1.0 in float64."""
    return np.exp(-u_of_x(x))


def dmu_dx(x):
    """dmu/dx = (dmu/du)/(dx/du) = e^-u mu^2 / [2 u mu - u^2 e^-u] > 0 for all u > 0 (proved analytically)."""
    u = u_of_x(x)
    m = _mu_of_u(u)
    e = np.exp(-u)
    return e * m * m / (2.0 * u * m - u * u * e)


# ------------------------------------------------------------------ the superseded kernels, for controls only
def nu_alpha2(y):
    """the kernel Route A REPLACES: mu = x/sqrt(1+x^2), i.e. g_obs^2 = g_bar^2 + ... alpha=2."""
    y = np.asarray(y, float)
    y2 = y * y
    return np.sqrt((y2 + np.sqrt(y2 * y2 + 4.0 * y2)) / 2.0) / y


def mu_alpha2(x):
    x = np.asarray(x, float)
    return x / np.sqrt(1.0 + x * x)


def nu_alpha1(y):
    """the earlier exact-identity kernel, retired for ephemeris reasons."""
    return np.sqrt(1.0 + 1.0 / np.asarray(y, float))


def mu_simple(x):
    """the literature's 'simple' mu -- a control, NOT the framework's."""
    x = np.asarray(x, float)
    return x / (1.0 + x)


if __name__ == "__main__":
    import sys

    from scipy.optimize import brentq

    ok = []

    def check(c, m):
        c = bool(c)
        ok.append((c, m))
        print(f"  [{'OK' if c else 'FAIL'}] {m}")

    print("=" * 100)
    print("  mi_route_a_kernel.py SELF-TEST")
    print("=" * 100)

    # K1 the fast inversion against brentq
    # brentq's xtol is ABSOLUTE, so a fixed 1e-15 gives only ~1e-7 RELATIVE precision on a root near 1e-8 --
    # the reference, not the fast inversion, was the imprecise side of an earlier version of this comparison.
    worst, worst_at = 0.0, 0.0
    for xv in np.logspace(-8, 8, 60):
        guess = float(u_of_x(xv))
        ub = brentq(lambda t: float(_x_of_u(t)) - xv, 1e-14, 1e9,
                    xtol=max(1e-300, 1e-16 * guess), rtol=8.9e-16)
        rel = abs(guess / ub - 1.0)
        if rel > worst:
            worst, worst_at = rel, xv
    check(worst < 1e-13,
          f"K1 the vectorized inversion matches brentq to a worst-case relative {worst:.2e} (at x = "
          f"{worst_at:.1e}) over sixteen decades in x, so the AQUAL solves get the exact kernel at "
          f"interpolation speed. The reference tolerance is scaled to the root: brentq's xtol is ABSOLUTE, so "
          f"a fixed 1e-15 would leave the COMPARATOR good to only ~1e-7 relative near x = 1e-8")

    # K2 the two forms are inverses: mu(x) x = y at x = nu(y) y
    worst2 = 0.0
    for yv in np.logspace(-8, 8, 60):
        xv = float(nu(yv)) * yv
        worst2 = max(worst2, abs(float(mu(xv)) * xv / yv - 1.0))
    check(worst2 < 1e-11,
          f"K2 the algebraic and AQUAL forms are exact inverses: mu(nu(y) y) * nu(y) y = y to {worst2:.2e} over "
          f"sixteen decades. One kernel, two representations -- they differ only OUTSIDE spherical symmetry")

    # K3 limits
    d = float(nu(1e-10)) * math.sqrt(1e-10)
    n_rep = float(nu_minus1(1e4))                          # sqrt(y) = 100, e^-100 = 3.7e-44: representable
    l_big = float(log_nu_minus1(1e6))                      # sqrt(y) = 1000: only the log form survives
    naive = float(nu(1e4)) - 1.0                           # the WRONG way, for contrast
    check(abs(d - 1.0) < 1e-4 and n_rep > 0.0 and abs(l_big + 1000.0) < 1e-6 and naive == 0.0,
          f"K3 limits, and the float64 trap made explicit: nu sqrt(y) -> 1 deep ({d:.6f} at y = 1e-10) so a0 "
          f"keeps exactly its meaning. At y = 1e4 the anomaly is nu - 1 = {n_rep:.3e} via nu_minus1(), while "
          f"the naive nu(y) - 1 gives exactly {naive:.1f} -- the subtraction is already dead there. At y = 1e6 "
          f"the value e^-1000 is below float64's smallest normal, so only log_nu_minus1() = {l_big:.1f} carries "
          f"it. Solar-system accelerations (y ~ 1e7-1e8) are in that regime, so ephemeris statements MUST use "
          f"the log form")

    # K4 mu monotone and in (0,1); dmu/dx > 0
    xs = np.logspace(-8, 5, 20000)
    ms = mu(xs)
    check(bool(np.all(np.diff(ms) >= 0) and np.all(ms > 0) and np.all(dmu_dx(xs) > 0)),
          f"K4 mu is monotone non-decreasing with mu in (0,1) and dmu/dx > 0 across thirteen decades "
          f"(min dmu/dx = {float(np.min(dmu_dx(xs))):.3e}) -- the ellipticity and convexity conditions the "
          f"field-theory script proved analytically, holding in the actual numerics the solvers will use")

    # K5 deep-MOND: mu -> x
    r = float(mu(1e-6)) / 1e-6
    check(abs(r - 1.0) < 1e-5,
          f"K5 deep-MOND limit of the AQUAL form: mu(x)/x = {r:.8f} at x = 1e-6, so the deep regime -- where "
          f"the BTFR, the a0-line and every a0 statement live -- is untouched by Route A")

    # K6 the footings
    check(abs(A0_CANON - 9.3614e-11) / 9.3614e-11 < 1e-4 and abs(A0_ALT / A0_CANON - 1.2071) < 0.01,
          f"K6 both footings carried, unchanged by the kernel switch: canonical {A0_CANON:.4e} "
          f"(= (1/2) c sqrt(G rho_Lambda), kappa = 1/2), alt {A0_ALT:.4e}, ratio {A0_ALT/A0_CANON:.4f} "
          f"(= 1/sqrt(Omega_Lambda)). Milgrom 2020's 1/2pi comparator = {A0_M20:.4e}")

    n = sum(1 for t, _ in ok if t)
    print(f"\n  {n}/{len(ok)} checks held.")
    if n != len(ok):
        for t, m in ok:
            if not t:
                print(f"    FAILED: {m}")
        sys.exit(1)
    print("  Exit 0: Route A's kernel is importable, fast, and validated in both representations.")
