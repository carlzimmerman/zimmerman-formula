#!/usr/bin/env python3
r"""mi_routeA_admissibility_audit_2026.py -- LANE 1: THE ADMISSIBILITY AUDIT. Is Route A's exponential kernel
theoretically admissible where the framework's power laws were not? Tested against every published condition
the corpus has identified, and tested LIKE-FOR-LIKE against three comparators plus a power-law family.

THE FOUR CONDITION SETS, and where each one is stated:
  (a) MILGROM 2022, PRD 106:064060 -- modified inertia at the level of the EQUATIONS OF MOTION, with the
      footnote that such theories "are not necessarily governed by an action". Stated requirement: x mu(x)
      MONOTONIC. Here proved ANALYTICALLY and EXACTLY for Route A (the corpus's kernel module only had K4's
      numerical grid), and the same closed form is given for every comparator.
  (b) MILGROM 1994, Ann. Phys. 229:384, class (34) + eq. (60). Five conditions: f(0)=1, the 2/3 deep-MOND
      normalisation, f > 0, f monotone decreasing, and ANALYTICITY of f at z = 0. The corpus banked (i) that
      the analyticity condition excludes EVERY interpolating function in use, and (ii) that it tested only
      four of the five, and only for alpha=2. This script tests all five for Route A and for four comparators.
  (c) THE BEKENSTEIN-MILGROM HEALTH SET, already proved for Route A by mi_route_a_field_theory_2026.py (11/11)
      and NOT re-derived here. What is done here is the thing that gives that proof meaning: the SAME six
      conditions on the comparators.
  (d) THE LIMIT RATES, with the ephemeris bound converted from a number into a CONDITION ON THE KERNEL'S
      NEWTONIAN APPROACH EXPONENT, anchored on the corpus's own committed Levenberg-Marquardt fit.
  (e) UNIQUENESS. Is Route A picked out, or is it one of a class?

WHAT THIS SCRIPT FOUND, stated before the arithmetic so nobody has to hunt for it:
  * (a) and (c) are NON-DISCRIMINATING. Route A passes; so does every comparator, including the whole
    one-parameter power-law family. "Route A is healthy" carries no comparative information at all.
  * (b) Route A FAILS literal analyticity, exactly as all four comparators do -- but by the mildest possible
    mechanism: its Milgrom-1994 kinetic function is C^infinity at the Newtonian point, where alpha=1, alpha=2
    and the simple mu are not even C^1.
  * (d) The ephemeris bound is p >= 2.26 (canonical) / 2.32 (alt) on the exponent of nu - 1 ~ C y^-p, robust
    to a factor 10 either way in the LM fit's absorption. NEW EXACT EQUIVALENCE: Milgrom's f is differentiable
    at the Newtonian point IFF p > 2, so the analytic-regularity threshold and the Solar-System threshold are
    the SAME threshold, with the data marginally stronger.
  * (e) *** ROUTE A IS NOT UNIQUE AND, ON THIS LANE, NOT EVEN PREFERRED. *** mu(x) = x/(1+x^4)^(1/4) -- the
    p = 4 member of the framework's own power-law family -- satisfies ALL FIVE Milgrom-1994 conditions
    INCLUDING THE ANALYTICITY CONDITION ROUTE A FAILS, the whole BM health set, Milgrom 2022, exact BTFR, and
    the ephemeris bound with a ~1e6 margin. Within the power family analyticity forces p/2 to be an integer
    >= 2, so p = 4 is the MINIMAL fully admissible member. Consequence: Milgrom-1994 analyticity IMPLIES the
    ephemeris bound. Route A buys unbounded margin and a closed-form free function; it does not buy
    admissibility, and it forfeits an analyticity that p = 4 would have kept.

PROVENANCE CAVEAT, load-bearing for (b) and (e): the Milgrom-1994 conditions used here are taken from THIS
CORPUS'S OWN TRANSCRIPTION of the paper in reviews/mi_eq34_inversion_banked_2026.py (B2) and
real_research/reviews/mi_milgrom1994_home_test_2026.py, not from the primary source, which is not in the
repository. The quoted condition is "f(z) has to be non-singular at z = 0 in the complex plane. If it has a
Taylor expansion ... f(z) = 1 + sum_m b_m z^m". Everything downstream of that quote -- the corollary, the
exclusion ladder, the p = 4 result -- is derived and verified here independently. But if the transcription is
wrong, or if Milgrom states a sixth condition the corpus did not record, the p = 4 headline weakens. Anyone
acting on it should check Ann. Phys. 229:384 directly.

WHAT WOULD OVERTURN THE HEADLINE: (i) a sixth stated condition in class (34) that p = 4 fails; (ii) p = 4
costing more than ~0.01 dex on SPARC (unlikely: the corpus's own scan finds alpha = 1, 2 and infinity within
0.0084 dex of one another at fixed a0, and p = 4 is bracketed by 2 and infinity, but it has NOT been run);
(iii) p = 4 failing one of the seven disc/front numbers Route A was re-solved on.

Route A's kernel is IMPORTED from the adopted module and never redefined. a0 is an INPUT on both footings and
is never fitted. Exit 0 = ran and every check held.
"""
from __future__ import annotations

import math
import os
import sys

import mpmath as mp
import numpy as np
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mi_route_a_kernel import (A0_ALT, A0_CANON, dmu_dx, log_nu_minus1, mu, mu_alpha2,  # noqa: E402
                               mu_simple, nu_alpha1, nu_alpha2, one_minus_mu, u_of_x)

mp.mp.dps = 40
ok: list[tuple[bool, str]] = []
HERE = os.path.dirname(os.path.abspath(__file__))


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 108)
    print(f"  {t}")
    print("=" * 108)


# ===================================================================== the kernels, all as mu(X), X = a/a0
# X is the MI argument a/a0 (= the AQUAL |grad phi|/a0). Milgrom 1994's variable is t = a0^2/a^2 = X^-2.
def _uA(X):
    """Route A: solve u^2 = X(1 - e^-u) at mpmath precision, seeded from the adopted module's fast inverse."""
    X = mp.mpf(X)
    g = float(u_of_x(float(X))) if 1e-11 < X < 1e11 else (float(X) if X < 1 else math.sqrt(float(X)))
    return mp.findroot(lambda u: u * u + X * mp.expm1(-u), mp.mpf(g))


def mu_routeA(X):
    return -mp.expm1(-_uA(X))


def mu_a1(X):
    X = mp.mpf(X)
    return (mp.sqrt(1 + 4 * X * X) - 1) / (2 * X)


def mu_a2(X):
    X = mp.mpf(X)
    return X / mp.sqrt(1 + X * X)


def mu_simp(X):
    X = mp.mpf(X)
    return X / (1 + X)


def mu_pow(X, p):
    X = mp.mpf(X)
    return X / (1 + X ** mp.mpf(p)) ** (mp.mpf(1) / mp.mpf(p))


# nu - 1 as a function of y = g_bar/a0, exact, at mpmath precision (float64 cancels these to noise)
def num1_routeA(y):
    return 1 / mp.expm1(mp.sqrt(mp.mpf(y)))


def num1_a1(y):
    y = mp.mpf(y)
    return mp.sqrt(1 + 1 / y) - 1


def num1_a2(y):
    y = mp.mpf(y)
    return mp.sqrt((y * y + mp.sqrt(y**4 + 4 * y * y)) / 2) / y - 1


def num1_simp(y):
    y = mp.mpf(y)
    return (y + mp.sqrt(y * y + 4 * y)) / (2 * y) - 1


def num1_pow(y, p):
    """for mu = X/(1+X^p)^(1/p) the algebraic form is EXACTLY nu = (1 + X^-p)^(1/p) with X = y nu.

    Solved by inverting y = X mu_p(X) with a Newton solve on X (the naive fixed point on nu OSCILLATES for
    y << 1, where nu ~ y^-1/2). At 40 dps the subtraction X/y - 1 keeps ~26 digits even at y ~ 2e3, where
    nu - 1 is 1e-14, so no cancellation-safe rewriting is needed.
    """
    y, p = mp.mpf(y), mp.mpf(p)
    g = mp.sqrt(y) if y < 1 else y
    X = mp.findroot(lambda Xv: Xv * mu_pow(Xv, p) - y, g)
    return X / y - 1


# 1 - mu(X), in CANCELLATION-FREE form. Needed because every tail integral below lives at large X, where
# `1 - mu` computed naively is the difference of two numbers that agree to 4 log10(X) digits: at X = 1e10 and
# 40 dps the p = 4 tail would silently underflow to exactly 0. Same trap as the corpus's 1 - exp(-47) == 1.0,
# one variable further out.
def om_routeA(X):
    return mp.e ** (-_uA(X))


def om_a1(X):
    X = mp.mpf(X)
    w = 1 / (4 * X * X)
    return 1 / (2 * X) - w / (mp.sqrt(1 + w) + 1)


def om_pow(X, p):
    X, p = mp.mpf(X), mp.mpf(p)
    return -mp.expm1(-mp.log1p(X ** (-p)) / p)


def om_simp(X):
    return 1 / (1 + mp.mpf(X))


KERNELS = [
    ("Route A   1-mu = e^-sqrt(y)", mu_routeA, num1_routeA, om_routeA, None),
    ("alpha=1   nu = sqrt(1+1/y)", mu_a1, num1_a1, om_a1, 1.0),
    ("alpha=2   mu = x/sqrt(1+x^2)", mu_a2, num1_a2, lambda X: om_pow(X, 2), 2.0),
    ("simple    mu = x/(1+x)", mu_simp, num1_simp, om_simp, 1.0),
    ("power p=3 mu = x/(1+x^3)^(1/3)", lambda X: mu_pow(X, 3), lambda y: num1_pow(y, 3),
     lambda X: om_pow(X, 3), 3.0),
    ("power p=4 mu = x/(1+x^4)^(1/4)", lambda X: mu_pow(X, 4), lambda y: num1_pow(y, 4),
     lambda X: om_pow(X, 4), 4.0),
]

banner("A0  THE COMPARATOR FAMILY IS ANCHORED ON THE ADOPTED MODULE, NOT RE-INVENTED")

# mu_pow at p=2 must BE the corpus's alpha=2 kernel, and mu_routeA must BE the module's mu.
w_p2, w_ra, w_s, w_a2 = 0.0, 0.0, 0.0, 0.0
for Xv in [mp.mpf(10) ** k for k in range(-8, 9)]:
    w_p2 = max(w_p2, abs(mu_pow(Xv, 2) / mu_a2(Xv) - 1))
    w_ra = max(w_ra, abs(mu_routeA(Xv) / mp.mpf(float(mu(float(Xv)))) - 1))
    w_s = max(w_s, abs(mu_simp(Xv) / mp.mpf(float(mu_simple(float(Xv)))) - 1))
    w_a2 = max(w_a2, abs(mu_a2(Xv) / mp.mpf(float(mu_alpha2(float(Xv)))) - 1))
check(w_p2 < mp.mpf("1e-30") and float(w_ra) < 1e-12 and float(w_s) < 1e-14 and float(w_a2) < 1e-14,
      f"A0 the power-law family mu_p = x/(1+x^p)^(1/p) at p = 2 IS the corpus's alpha=2 kernel identically "
      f"(worst relative {float(w_p2):.1e} over sixteen decades at 40 dps), and this script's mpmath "
      f"re-implementations of Route A, the simple mu and alpha=2 agree with the ADOPTED float64 module to "
      f"{float(w_ra):.1e} / {float(w_s):.1e} / {float(w_a2):.1e}. So every number below is about the adopted "
      f"kernel, and the p-family is a genuine one-parameter extension THROUGH it, not a substitute for it")

w_om = 0.0
for nm, mf, _nf, om, p in KERNELS:
    for Xv in [mp.mpf(10) ** k for k in range(-3, 4)]:
        w_om = max(w_om, float(abs(om(Xv) / (1 - mf(Xv)) - 1)))
check(w_om < 1e-25,
      f"A0a the cancellation-free 1 - mu forms used in every tail integral below agree with the plain "
      f"1 - mu(X) to {w_om:.1e} over x = 1e-3 to 1e3, and that residual IS the plain form's own error: at "
      f"x = 1e3 the p = 4 tail is 2.5e-13, so the naive difference has already thrown away thirteen of forty "
      f"digits. By x = 1e10 it throws away all forty and reports the tail as an exact zero -- the corpus's "
      f"1 - exp(-47) == 1.0 trap, one variable further out. Every tail integral below therefore uses the "
      f"expm1/log1p forms")

check(abs(A0_CANON - 9.3614e-11) / 9.3614e-11 < 1e-4 and abs(A0_ALT - 1.13e-10) / 1.13e-10 < 1e-4,
      f"A0b both footings carried as INPUTS throughout, never fitted: a0 = {A0_CANON:.4e} (canonical, "
      f"kappa = 1/2 on rho_DE/cH_Lambda) and {A0_ALT:.4e} (alt, rho_total/cH0)")


# ===================================================================== (a) MILGROM 2022 -- x mu(x) monotonic
banner("(a)  MILGROM 2022 PRD 106:064060 -- x mu(x) MONOTONIC, PROVED ANALYTICALLY FOR ROUTE A")

u = sp.Symbol("u", positive=True)
mu_s = 1 - sp.exp(-u)
X_s = u**2 / mu_s
# x mu = u^2 identically, so d(x mu)/dx = (du^2/du)/(dX/du) = 2u / X'(u).
dXdu = sp.simplify(sp.diff(X_s, u))
lhs = sp.simplify(2 * u / dXdu)
rhs = 2 * mu_s**2 / (2 - (2 + u) * sp.exp(-u))
resid = sp.simplify(sp.together(lhs - rhs))
print(f"  Route A parametrically:  mu = 1 - e^-u,  x = u^2/mu   =>   x mu = u^2  EXACTLY")
print(f"  dx/du = {sp.simplify(dXdu)}")
print(f"  d(x mu)/dx = 2u / (dx/du) = {sp.simplify(rhs)}")
check(sp.simplify(resid) == 0,
      f"a1 EXACT CLOSED FORM, symbolically verified: d(x mu)/dx = 2 mu^2 / [2 - (2+u) e^-u] with "
      f"u = sqrt(x mu). Residual against 2u/(dx/du) simplifies to {sp.simplify(resid)} identically -- so the "
      f"sign of Milgrom 2022's monotonicity condition is decided by ONE scalar inequality, "
      f"2 e^u > 2 + u")

gpos = sp.series(2 * sp.exp(u) - 2 - u, u, 0, 13).removeO()
cf = [sp.nsimplify(gpos.coeff(u, k)) for k in range(13)]
print(f"  2 e^u - 2 - u  =  {' + '.join(f'{c} u^{k}' for k, c in enumerate(cf) if c != 0)} + ...")
check(cf[0] == 0 and cf[1] == 1 and all(c > 0 for c in cf[1:]) and
      all(sp.nsimplify(2 / sp.factorial(k)) == cf[k] for k in range(2, 13)),
      f"a2 and that inequality is PROVED, not sampled: 2 e^u - 2 - u has Taylor coefficients 0, 1, then "
      f"exactly 2/k! for every k >= 2 -- all strictly positive -- so it is > 0 for every u > 0 with no "
      f"numerical evaluation anywhere. Hence d(x mu)/dx > 0 STRICTLY on (0, inf). Route A satisfies "
      f"Milgrom 2022's only stated admissibility requirement EXACTLY")

# and the closed form must reproduce the ADOPTED module's own derivative. Evaluated at 40 dps, because in
# float64 the closed form's own denominator 2 - (2+u)e^-u cancels two O(1) numbers down to O(u) and loses
# eight digits by u ~ 3e-8 -- that is a defect of the CLOSED FORM's evaluation, not of the module.
wm, wm_at = 0.0, 0.0
for Xv in np.logspace(-8, 8, 65):
    uu = _uA(Xv)
    m_mp = -mp.expm1(-uu)
    cf_val = 2 * m_mp**2 / (2 - (2 + uu) * mp.e ** (-uu))
    r = abs(mp.mpf(float(mu(Xv)) + Xv * float(dmu_dx(Xv))) / cf_val - 1)
    if r > wm:
        wm, wm_at = float(r), Xv
check(wm < 1e-12,
      f"a3 the closed form, evaluated at 40 dps, agrees with the ADOPTED float64 module's own "
      f"mu(x) + x dmu/dx to a worst-case relative {wm:.2e} (at x = {wm_at:.1e}) over sixteen decades -- so "
      f"the analytic result and the object the disc solves actually call are the same function, and "
      f"mi_route_a_kernel.py's K4 numerical grid is now backed by a proof")

print("\n  the SAME condition, in closed form, for every comparator (x = mpmath-symbolic checks below):")
xx = sp.Symbol("x", positive=True)
COMP_SYM = [("alpha=1", (sp.sqrt(1 + 4 * xx**2) - 1) / (2 * xx)), ("alpha=2", xx / sp.sqrt(1 + xx**2)),
            ("simple", xx / (1 + xx)), ("power p=3", xx / (1 + xx**3) ** sp.Rational(1, 3)),
            ("power p=4", xx / (1 + xx**4) ** sp.Rational(1, 4))]
mono_all, muinc_all = True, True
for nm, m_e in COMP_SYM:
    d1 = sp.simplify(sp.diff(xx * m_e, xx))
    d2 = sp.simplify(sp.diff(m_e, xx))
    pos1 = all(float(d1.subs(xx, v)) > 0 for v in (1e-6, 1e-2, 1.0, 10.0, 1e4, 1e8))
    pos2 = all(float(d2.subs(xx, v)) > 0 for v in (1e-6, 1e-2, 1.0, 10.0, 1e4, 1e8))
    mono_all &= pos1
    muinc_all &= pos2
    print(f"      {nm:<11} d(x mu)/dx = {d1}")
check(mono_all and muinc_all,
      f"a4 *** AND THAT IS WHY (a) IS NON-DISCRIMINATING: *** every comparator satisfies Milgrom 2022 too. "
      f"For the whole power family d(x mu_p)/dx = x(2+x^p)(1+x^p)^-((p+1)/p) and dmu_p/dx = "
      f"(1+x^p)^-((p+1)/p), both MANIFESTLY positive for every p > 0; alpha=1 gives 2x/sqrt(1+4x^2) and the "
      f"simple mu gives x(x+2)/(1+x)^2. So Milgrom 2022 gives the MI reading a legitimate published "
      f"action-free home -- it gives that home to alpha=1 and alpha=2 equally, and Route A gains no "
      f"comparative standing from it")

print("""
  ONE STRUCTURAL POINT WORTH RECORDING, because it collapses three separate-looking conditions into one:
  d(x mu)/dx > 0 is simultaneously (i) Milgrom 2022's MI admissibility condition (a -> g_N is a bijection,
  so the equation of motion has a unique solution), (ii) the LONGITUDINAL eigenvalue of the AQUAL principal
  symbol, i.e. ellipticity, and (iii) the condition that y nu(y) be invertible, i.e. QUMOND's own
  well-posedness. For Route A all three reduce to 2 e^u > 2 + u. They are one inequality, not three.""")


# ===================================================================== (b) MILGROM 1994's FIVE CONDITIONS
banner("(b)  MILGROM 1994 Ann.Phys. 229:384 -- eq. (60), and the ANALYTICITY CONDITION")

print("""  Milgrom's eq. (60) fixes mu from the free function f of class (34): with t = a0^2/a^2,
      mu = f(t) - t f'(t),    f(t) = t INT_t^inf mu(s)/s^2 ds.
  Substituting s = X^-2 turns that into a form the corpus did not have, and it is the useful one:

      *** f(t) = (2/T^2) INT_0^T mu(X) X dX,     T = t^-1/2 = a/a0 ***

  i.e. f is the AREA-WEIGHTED MEAN of mu over the kernel's own argument. Two consequences drop straight out:
      f(t) = 1 + b_1 t + 2 t Q(T),   b_1 = -2 INT_0^inf [1 - mu(X)] X dX,   Q(T) = INT_T^inf [1-mu] X dX,
  so b_1 -- the coefficient of the FIRST Taylor term, which Milgrom's own corollary shows contributes exactly
  nothing to mu -- is finite if and only if [1-mu] X is integrable at infinity. That is the whole story.""")


def F_of_T(mu_f, T, nodes=None):
    """f(t) at t = T^-2, via f = (2/T^2) INT_0^T mu(X) X dX. Exact for any mu."""
    T = mp.mpf(T)
    pts = [mp.mpf(0)] + [q for q in (mp.mpf("1e-3"), mp.mpf(1), mp.mpf(10)) if q < T] + [T]
    return 2 / T**2 * mp.quad(lambda X: mu_f(X) * X, pts if nodes is None else nodes)


# --- b1: the general formula must reproduce BOTH of the corpus's committed closed forms exactly
def f1_closed(t):
    t = mp.mpf(t)
    return mp.sqrt(t + 4) / 2 - mp.sqrt(t) + (t / 4) * mp.asinh(2 / mp.sqrt(t))


def f2_closed(t):
    t = mp.mpf(t)
    return mp.sqrt(1 + t) - t * mp.asinh(1 / mp.sqrt(t))


w1, w2 = 0.0, 0.0
for Tv in (mp.mpf("0.01"), mp.mpf(1), mp.mpf(3), mp.mpf(30), mp.mpf(300)):
    tv = 1 / Tv**2
    w1 = max(w1, abs(F_of_T(mu_a1, Tv) / f1_closed(tv) - 1))
    w2 = max(w2, abs(F_of_T(mu_a2, Tv) / f2_closed(tv) - 1))
check(float(w1) < 1e-25 and float(w2) < 1e-25,
      f"b1 the general form f = (2/T^2) INT_0^T mu X dX reproduces BOTH closed forms banked by "
      f"reviews/mi_eq34_inversion_banked_2026.py -- f_1 = sqrt(t+4)/2 - sqrt(t) + (t/4) asinh(2/sqrt t) to "
      f"{float(w1):.1e} and f_2 = sqrt(1+t) - t asinh(1/sqrt t) to {float(w2):.1e}. So the machinery below is "
      f"validated against committed results before it is used on anything new")

# --- the C^1 dichotomy, tested as a decade-doubling tail integral so no divergence has to be caught
print(f"\n  D(Xm) = INT_Xm^100Xm [1 - mu] X dX -- the increment of b_1 per two decades. -> 0 iff b_1 exists:")
print(f"  {'kernel':<32}{'D(1e2)':>13}{'D(1e4)':>13}{'D(1e6)':>13}{'ratio 1e6/1e4':>15}{'b_1 exists?':>13}")
print("  " + "-" * 99)
b1_exists = {}
for nm, mf, _nf, om, p in KERNELS:
    Ds = []
    for Xm in (mp.mpf(100), mp.mpf(10) ** 4, mp.mpf(10) ** 6):
        Ds.append(mp.quad(lambda X: om(X) * X, [Xm, 10 * Xm, 100 * Xm]))
    r = Ds[2] / Ds[1] if Ds[1] != 0 else mp.mpf(0)
    b1_exists[nm] = r < mp.mpf("0.95")               # the ratio is exactly 100^(2-p): 1 at p=2, >1 below
    print(f"  {nm:<32}{mp.nstr(Ds[0], 5):>13}{mp.nstr(Ds[1], 5):>13}{mp.nstr(Ds[2], 5):>13}"
          f"{mp.nstr(r, 4):>15}{'YES' if b1_exists[nm] else 'NO':>13}")
check(b1_exists["Route A   1-mu = e^-sqrt(y)"] and b1_exists["power p=3 mu = x/(1+x^3)^(1/3)"]
      and b1_exists["power p=4 mu = x/(1+x^4)^(1/4)"]
      and not b1_exists["alpha=1   nu = sqrt(1+1/y)"] and not b1_exists["alpha=2   mu = x/sqrt(1+x^2)"]
      and not b1_exists["simple    mu = x/(1+x)"],
      f"b2 *** THE DICHOTOMY IS SHARP AND IT SPLITS THE KERNELS IN USE FROM ROUTE A. *** The two-decade "
      f"increment of b_1 falls by 100^(2-p), so b_1 exists (i.e. f is differentiable at the Newtonian point) "
      f"for Route A and for p = 3, 4; it does NOT for alpha=1, alpha=2 or the simple mu. alpha=1 and the "
      f"simple mu diverge LINEARLY (f - 1 ~ -c sqrt t, so f is not even C^1 -- ratio 100), alpha=2 diverges "
      f"LOGARITHMICALLY (f - 1 ~ (1/2) t ln t -- ratio exactly 1, the marginal case). Route A's increment is "
      f"already 7.7e-38 by x = 1e4 and 1.0e-425 by x = 1e6, which is why the tails had to be computed "
      f"cancellation-free (A0a)")

# --- the threshold in p, pinned numerically
print(f"\n  the same test scanned in p, to locate the threshold exactly (predicted: b_1 exists iff p > 2):")
thr = {}
for pv in (1.5, 1.9, 2.0, 2.1, 2.5, 3.0, 4.0):
    Ds = [mp.quad(lambda X: om_pow(X, pv) * X, [Xm, 10 * Xm, 100 * Xm])
          for Xm in (mp.mpf(10) ** 4, mp.mpf(10) ** 6)]
    thr[pv] = float(Ds[1] / Ds[0])
    print(f"      p = {pv:<5} D(1e6)/D(1e4) = {thr[pv]:.4e}   ({'converging' if thr[pv] < 0.95 else 'not'})")
check(all(thr[pv] > 0.95 for pv in (1.5, 1.9, 2.0)) and all(thr[pv] < 0.95 for pv in (2.1, 2.5, 3.0, 4.0))
      and abs(thr[2.0] - 1.0) < 1e-3,
      f"b3 the threshold sits at p = 2 EXACTLY: at p = 2 the two-decade increment is constant to "
      f"{abs(thr[2.0]-1.0):.1e} (the pure logarithm), it GROWS for p < 2 and it DECAYS for p > 2. So "
      f"*** f is differentiable at the Newtonian point IF AND ONLY IF nu - 1 falls faster than 1/y^2, "
      f"equivalently iff the anomalous acceleration falls faster than 1/g_bar. *** alpha=2 sits exactly ON "
      f"the marginal case")

# --- Route A: b_1 two independent ways, and the flatness of the remainder
b1_A_X = -2 * mp.quad(lambda X: om_routeA(X) * X, [0, 1, 10, 100, 1000, 10000])


def _h(w):
    """the u-parametrised [1-mu] X dX integrand with the e^-u stripped off: u^3[2-(2+u)e^-u]/mu^3 -> 2u^3."""
    m = -mp.expm1(-w)
    return w**3 * (2 - (2 + w) * mp.e ** (-w)) / m**3


def _uint(w):
    return mp.e ** (-w) * _h(w)


def Q_routeA(uT):
    """INT_uT^inf e^-u h(u) du = e^-uT INT_0^inf e^-w h(uT+w) dw -- the shift factors the tiny exponential
    out of the quadrature, so the result stays accurate at uT = 1000 where a direct quad loses six digits."""
    uT = mp.mpf(uT)
    return mp.e ** (-uT) * mp.quad(lambda w: mp.e ** (-w) * _h(uT + w), [0, 5, 20, 100, 400])


b1_A_u = -2 * mp.quad(_uint, [0, 1, 5, 20, 60, 200])
check(abs(b1_A_X / b1_A_u - 1) < mp.mpf("1e-18"),
      f"b4 Route A's b_1 = {mp.nstr(b1_A_u, 14)}, computed two independent ways -- direct quadrature in X "
      f"with an mpmath root-solve for u at every node, and the exact u-parametrised integrand "
      f"e^-u u^3[2-(2+u)e^-u]/mu^3 with no root-solve at all -- agreeing to "
      f"{mp.nstr(abs(b1_A_X/b1_A_u-1), 3)}. FINITE, so Route A's Milgrom-1994 kinetic function IS "
      f"differentiable at the Newtonian point")

# *** and b_1 IS the AQUAL free function's 'unobservable' additive constant, with the sign flipped ***
C0_COMMITTED = 25.975758      # mi_route_a_field_theory_2026.py, T2b: Fcal -> X - C0 + 4e^-s(s^3+3s^2+6s+6)
check(abs(-b1_A_u / mp.mpf(C0_COMMITTED) - 1) < mp.mpf("1e-7"),
      f"b4b *** AN EXACT BRIDGE BETWEEN THE TWO FORMALISMS, and it is new. *** Since "
      f"Fcal(X_A) = 2 INT_0^x mu X dX with X_A = x^2, the general form above says f(t) = Fcal(X_A)/X_A at "
      f"X_A = 1/t: *** MILGROM 1994's KINETIC FUNCTION IS THE BEKENSTEIN-MILGROM FREE FUNCTION DIVIDED BY "
      f"X. *** Hence b_1 = -C0 identically, and numerically {mp.nstr(-b1_A_u, 10)} against the committed "
      f"C0 = {C0_COMMITTED} of mi_route_a_field_theory_2026.py (agreeing to "
      f"{mp.nstr(abs(-b1_A_u/mp.mpf(C0_COMMITTED)-1), 3)}). The two objects the corpus separately called "
      f"'pure gauge' and 'unobservable' are THE SAME CONSTANT, unobservable for the same reason")

print(f"\n  Route A's remainder R(t)/t = 2 Q(T) must vanish faster than EVERY power for f to be C^infinity")
print(f"  with a TERMINATING Taylor series 1 + b_1 t. Test: 2Q(T) T^2N -> 0 for N = 1, 2, 3, 5, 10:")
TT = (mp.mpf(10) ** 5, mp.mpf(10) ** 7, mp.mpf(10) ** 9)
QA = {Tv: Q_routeA(_uA(Tv)) for Tv in TT}
Q4 = {Tv: mp.quad(lambda X: om_pow(X, 4) * X, [Tv, 10 * Tv, mp.inf]) for Tv in TT}
flatA, flat4 = True, True
for Nv in (1, 2, 3, 5, 10):
    rowA = [2 * QA[Tv] * Tv ** (2 * Nv) for Tv in TT]
    row4 = [2 * Q4[Tv] * Tv ** (2 * Nv) for Tv in TT]
    print(f"      N = {Nv:<3} Route A: " + "  ".join(f"{mp.nstr(v, 4):>12}" for v in rowA)
          + f"   |  p = 4: " + "  ".join(f"{mp.nstr(v, 4):>12}" for v in row4))
    flatA &= rowA[-1] < mp.mpf("1e-6") and all(rowA[i] > rowA[i + 1] for i in range(len(rowA) - 1))
    if Nv == 1:
        flat4 &= all(abs(v / mp.mpf("0.25") - 1) < mp.mpf("1e-9") for v in row4)
    else:
        flat4 &= all(row4[i] < row4[i + 1] for i in range(len(row4) - 1)) and row4[-1] > mp.mpf("1e6")
uTref = _uA(mp.mpf(10) ** 5)
asym = 2 * mp.e ** (-uTref) * (uTref**3 + 3 * uTref**2 + 6 * uTref + 6)
rel_as = abs(QA[mp.mpf(10) ** 5] / asym - 1)
check(flatA and rel_as < mp.mpf("1e-30"),
      f"b5 *** ROUTE A's f IS C^INFINITY AT THE NEWTONIAN POINT WITH A TERMINATING TAYLOR SERIES. *** "
      f"2Q(T) T^2N is monotonically decreasing in T and below 1e-6 by T = 1e9 for every N up to 10, so every "
      f"Taylor coefficient b_m with m >= 2 is exactly zero and f = 1 + b_1 t + (a remainder flatter than "
      f"every power). The quadrature also matches the closed asymptote 2 e^-u (u^3+3u^2+6u+6) at u = sqrt(x) "
      f"to {mp.nstr(rel_as, 3)} -- i.e. the correction is below the 40-dps quadrature floor, and 2Q = "
      f"4e^-s(s^3+3s^2+6s+6) is EXACTLY the Newtonian tail of Fcal that "
      f"mi_route_a_field_theory_2026.py banked, recovered here from a different integral. THE PRICE: b_1 "
      f"contributes IDENTICALLY NOTHING to mu (Milgrom's own m = 1 cancellation), so the entire Taylor "
      f"expansion Milgrom writes down is the TRIVIAL Newtonian one and all of the MOND physics sits in the "
      f"non-perturbative remainder. Route A's departure from Newton is NON-PERTURBATIVE in a0")
check(flat4,
      f"b6 and the contrast is exactly as the analytic structure predicts: for p = 4, 2Q T^2 sits at 1/4 to "
      f"1e-9 at every T (a genuine t^2 term in f, b_2 = 1/4) while 2Q T^2N GROWS without bound for N >= 2. "
      f"p = 4's expansion CARRIES the physics at order t^2 = (a0/a)^4; Route A's carries none of it at any "
      f"order. Both are checked here, and each would fail if the other's behaviour appeared")

# --- Milgrom 1994's OTHER FOUR conditions, which the corpus only ever tested for alpha=2
def F_routeA(T):
    """f(t) for Route A at t = T^-2, u-parametrised: mu X = u^2 exactly, so the integrand needs no solve --
    INT_0^T mu X dX = INT_0^uT u^3 [2-(2+u)e^-u] / mu^2 du, which is O(u^2) at the origin."""
    uT = _uA(T)
    nodes = [mp.mpf(0)] + [q for q in (mp.mpf(1), mp.mpf(5), mp.mpf(20), mp.mpf(100)) if q < uT] + [uT]
    return 2 / mp.mpf(T) ** 2 * mp.quad(
        lambda w: w**3 * (2 - (2 + w) * mp.e ** (-w)) / (-mp.expm1(-w)) ** 2, nodes)


FSET = [("Route A", F_routeA), ("alpha=2 (the corpus's control)", lambda T: F_of_T(mu_a2, T)),
        ("power p=3", lambda T: F_of_T(lambda X: mu_pow(X, 3), T)),
        ("power p=4", lambda T: F_of_T(lambda X: mu_pow(X, 4), T))]
print(f"\n  Milgrom 1994's OTHER FOUR conditions on f -- which the corpus tested only for alpha=2 (T1a-T1c of")
print(f"  mi_milgrom1994_home_test_2026.py). f(0)=1; f sqrt(t) -> 2/3 deep; f > 0; f monotone DECREASING in t:")
print(f"  {'kernel':<32}{'f(t=1e-12)':>14}{'f sqrt(t) at t=1e14':>22}{'f>0 & decr. in t':>19}")
print("  " + "-" * 86)
m94 = {}
for nm, Ff in FSET:
    f0 = Ff(mp.mpf(10) ** 6)                                  # t = 1e-12
    # evaluated at t = 1e14, not 1e8: Route A and the simple mu have mu/X = 1 - X + O(X^2), so f sqrt(t)
    # carries a GENUINE finite-T correction -(3/4)T -- 7.5e-5 at T = 1e-4. It is the limit that is 2/3.
    fd = Ff(mp.mpf(10) ** -7) * mp.mpf(10) ** 7               # t = 1e14, f sqrt(t) = f/T
    Ts = [mp.mpf(10) ** k for k in range(-3, 4)]              # t from 1e6 down to 1e-6
    vals = [Ff(Tv) for Tv in Ts]
    posdec = all(v > 0 for v in vals) and all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))
    m94[nm] = (abs(f0 - 1) < mp.mpf("1e-10"), abs(fd - mp.mpf(2) / 3) < mp.mpf("1e-6"), posdec)
    print(f"  {nm:<32}{mp.nstr(f0, 10):>14}{mp.nstr(fd, 12):>22}{'ok' if posdec else 'NO':>19}")
check(all(all(v) for v in m94.values()),
      f"b8 *** MILGROM 1994's OTHER FOUR CONDITIONS NOW VERIFIED FOR ROUTE A AND FOR p = 3, 4, not just for "
      f"alpha=2: *** f(0+) = 1 (the Newtonian normalisation of the kinetic Lagrangian), f sqrt(t) -> 2/3 (the "
      f"deep-MOND scaling in Milgrom's abstract, the condition that picks the physical branch over the "
      f"pure-gauge one), f > 0, and f monotone decreasing in t across seven decades. alpha=2 is carried as a "
      f"CONTROL and reproduces the corpus's T1a-T1c. So on four of the five conditions Route A and p = 4 both "
      f"pass; the fifth (analyticity) is where they part")

# --- the analyticity corollary, re-derived rather than quoted
z = sp.Symbol("z")
bs = sp.symbols("b1:8")
f_gen = 1 + sum(bs[m - 1] * z**m for m in range(1, 8))
mu_gen = sp.expand(f_gen - z * sp.diff(f_gen, z))
c_gen = [sp.expand(mu_gen.coeff(z, m)) for m in range(8)]
check(c_gen[0] == 1 and c_gen[1] == 0 and all(sp.simplify(c_gen[m] - bs[m - 1] * (1 - m)) == 0
                                              for m in range(2, 8)),
      f"b7 Milgrom's analyticity corollary re-derived symbolically, not quoted: for f = 1 + sum b_m z^m, "
      f"mu = f - z f' = 1 + sum b_m (1-m) z^m. The m = 1 coefficient CANCELS IDENTICALLY "
      f"(coefficient of z^1 = {c_gen[1]}), so an ANALYTIC f forces mu - 1 = O(z^2) = O((a0/a)^4) and forces "
      f"b_1 to be pure gauge. This is the condition the corpus banked; here it is proved from f, not asserted")

print("""
  *** AND NOW THE THEOREM THAT PLACES ROUTE A. *** Analyticity of f at z = 0 and a Newtonian anomaly that
  decays faster than every power are MUTUALLY EXCLUSIVE inside class (34), except in the degenerate case.
  Proof: if f is analytic at 0 then mu - 1 = sum_{m>=2} b_m(1-m) z^m is analytic there; if in addition mu - 1
  is FLAT at 0 (all derivatives vanish, which is what "faster than every power" means) then an analytic flat
  function vanishes identically on a neighbourhood, so mu == 1 for all accelerations above some finite
  threshold -- no MOND deviation at all in that regime, and the non-analyticity is merely pushed from z = 0
  out to a finite point ON the physical spectrum, which is worse for an operator function f(a0^2 D g^-1 D).
  So Route A's exclusion from class (34) is NOT the same failure as alpha=1's or alpha=2's. Theirs is a tail
  that an analytic f cannot produce (too SLOW). Route A's is a tail no analytic f can produce (too FLAT).
  Both are exclusions; only one of them is a symptom of a Newtonian limit that is too weak.""")

print("  the resulting LADDER of Milgrom-1994 regularity at the Newtonian point, computed above:")
print("      alpha=1, simple  :  f - 1 ~ -c sqrt(t)     NOT C^1   (divergence rate t^-1/2)")
print("      alpha=2          :  f - 1 ~ (1/2) t ln t   NOT C^1   (divergence rate ln(1/t), marginal)")
print("      Route A          :  f = 1 + b_1 t + flat   C^INFINITY but NOT analytic (essential singularity)")
print("      power p = 4      :  f = 1 + b_1 t + t^2/4  ANALYTIC   (see section (e))")


# ===================================================================== (c) the BM health set, comparators
banner("(c)  THE BEKENSTEIN-MILGROM HEALTH SET -- NOT re-derived for Route A; run on the COMPARATORS")

print("""  mi_route_a_field_theory_2026.py (11/11) already proved Route A convex, ghost-free, strictly
  elliptic, subluminal, positive-phantom and exact-BTFR. That proof only MEANS something if a comparator
  fails one of them. Six conditions, in the AQUAL variable x = |grad phi|/a0:
      H1 mu in (0,1)              H2 dmu/dx > 0 (convexity of F in X, and subluminality)
      H3 d(x mu)/dx > 0 (ellipticity)   H4 c_s^2 = mu/(x mu)' in (0,1)
      H5 mu/x -> 1 as x -> 0 (exact BTFR, coefficient 1, a0 keeps its meaning)
      H6 nu > 1 and dnu/dy < 0 (positive phantom density in spherical symmetry)

  The grid stops at x = 1e3 DELIBERATELY. Route A's 1 - mu = e^-sqrt(x) drops below 1e-40 by x ~ 8500, so at
  40 dps `mu < 1` would read as FALSE there for a purely arithmetic reason -- the same trap that already bit
  this corpus in float64 at u ~ 37. The strict inequalities beyond the grid are the ANALYTIC ones proved in
  (a) and (d3); numerics are used only where the precision can actually hold them.""")
print(f"\n  {'kernel':<32}{'H1':>5}{'H2':>5}{'H3':>5}{'H4':>5}{'H5':>5}{'H6':>5}{'c_s^2 deep':>12}"
      f"{'mu/x at 1e-8':>14}")
print("  " + "-" * 97)
health = {}
for nm, mf, nf, om, p in KERNELS:
    Xs = [mp.mpf(10) ** k for k in range(-6, 4)]
    h1 = all(0 < mf(Xv) < 1 for Xv in Xs)
    h2, h3 = True, True
    for Xv in Xs:
        hh = Xv * mp.mpf("1e-12")
        dmu = (mf(Xv + hh) - mf(Xv - hh)) / (2 * hh)
        dxm = ((Xv + hh) * mf(Xv + hh) - (Xv - hh) * mf(Xv - hh)) / (2 * hh)
        h2 &= dmu > 0
        h3 &= dxm > 0
    cs2 = []
    for Xv in Xs:
        hh = Xv * mp.mpf("1e-12")
        dxm = ((Xv + hh) * mf(Xv + hh) - (Xv - hh) * mf(Xv - hh)) / (2 * hh)
        cs2.append(mf(Xv) / dxm)
    h4 = all(0 < v < 1 for v in cs2)
    h5 = abs(mf(mp.mpf("1e-8")) / mp.mpf("1e-8") - 1) < mp.mpf("1e-7")
    # H6 is read off an X-scan rather than a y-scan: y = X mu(X) and nu = 1/mu(X), so nu > 1 and dnu/dy < 0
    # follow from mu < 1 with mu increasing while y increases -- and y's monotonicity is checked too.
    ys = [Xv * mf(Xv) for Xv in Xs]
    nus = [1 / mf(Xv) for Xv in Xs]
    h6 = (all(v > 1 for v in nus) and all(nus[i] > nus[i + 1] for i in range(len(nus) - 1))
          and all(ys[i] < ys[i + 1] for i in range(len(ys) - 1)))
    health[nm] = (h1, h2, h3, h4, h5, h6)
    print(f"  {nm:<32}" + "".join(f"{'ok' if v else 'NO':>5}" for v in health[nm])
          + f"{float(cs2[0]):>12.6f}{float(mf(mp.mpf('1e-8'))/mp.mpf('1e-8')):>14.9f}")
check(all(all(v) for v in health.values()),
      f"c1 *** (c) IS NON-DISCRIMINATING, AND THAT IS THE HONEST RESULT: *** all six BM health conditions "
      f"hold for ALL {len(KERNELS)} kernels, including every comparator and the whole power family, with "
      f"c_s^2 -> 1/2 in the deep limit for every one of them. Route A's health proof is correct and it is "
      f"also uninformative comparatively -- it does not distinguish Route A from the kernels it replaced, and "
      f"no argument for Route A may lean on it")


# ===================================================================== (d) THE LIMIT RATES
banner("(d)  THE REQUIRED LIMIT RATES -- and the ephemeris bound AS A CONDITION ON THE APPROACH EXPONENT")

# deep limit, all kernels: nu sqrt(y) -> 1. Evaluated through the X-scan (y = X mu, nu = 1/mu) so that the
# p-family needs no inversion here: nu sqrt(y) = sqrt(X mu)/mu.
deep = {}
for nm, mf, nf, om, p in KERNELS:
    Xv = mp.mpf("1e-8")
    deep[nm] = float(mp.sqrt(Xv * mf(Xv)) / mf(Xv))
    print(f"      {nm:<32} nu sqrt(y) at x = 1e-8 (y = {float(Xv*mf(Xv)):.2e}) : {deep[nm]:.10f}")
check(all(abs(v - 1) < 1e-7 for v in deep.values()),
      f"d1 the DEEP rate is identical for every kernel by construction: nu sqrt(y) -> 1, so all six define "
      f"the SAME a0 and every comparison below is like-for-like. Worst deviation "
      f"{max(abs(v-1) for v in deep.values()):.1e}")

# the Newtonian exponent p, symbolically
print(f"\n  the NEWTONIAN approach, nu - 1 = C y^-p, obtained by series expansion (not asserted):")
eps = sp.Symbol("eps", positive=True)
pc = {}
for nm, m_e in COMP_SYM:
    ser = sp.series(sp.simplify((1 - m_e).subs(xx, 1 / eps)), eps, 0, 5).removeO()
    # the smallest power of eps = 1/x with a nonzero coefficient IS the exponent p
    pw = None
    for q in (sp.Rational(1, 2), 1, sp.Rational(3, 2), 2, sp.Rational(5, 2), 3, 4):
        cc = sp.simplify(sp.limit(ser / eps**q, eps, 0))
        if cc != 0 and cc.is_finite:
            pw, C = q, cc
            break
    pc[nm] = (pw, C)
    print(f"      {nm:<11} 1 - mu = {sp.nsimplify(C)} x^-{pw} + ...   =>  p = {pw}")
check(pc["alpha=1"][0] == 1 and pc["simple"][0] == 1 and pc["alpha=2"][0] == 2
      and pc["power p=3"][0] == 3 and pc["power p=4"][0] == 4
      and pc["alpha=2"][1] == sp.Rational(1, 2) and pc["power p=4"][1] == sp.Rational(1, 4),
      f"d2 the exponents, from the series and not from memory: alpha=1 p = 1, simple p = 1, alpha=2 p = 2 "
      f"with C = 1/2, and mu_p gives p with C = 1/p. (For nu - 1 the same p holds, since x/y -> 1.)")

# Route A: flat, verified in LOG space because e^-sqrt(y) is unrepresentable past y ~ 5e5
print(f"\n  Route A's Newtonian approach is FLAT -- faster than every power. Verified in log space, because")
print(f"  nu - 1 = e^-sqrt(y) drops below float64's smallest normal past y ~ 5e5:")
flat_ok = True
for Nv in (2, 5, 10, 20, 50):
    row = []
    for yv in (1e6, 1e8, 1e10):
        val = Nv * math.log(yv) + float(log_nu_minus1(yv))
        row.append(val)
    flat_ok &= all(row[i] > row[i + 1] for i in range(len(row) - 1)) and row[-1] < 0
    print(f"      N = {Nv:<3} log[y^N (nu-1)] at y = 1e6, 1e8, 1e10 : "
          + "  ".join(f"{v:+11.2f}" for v in row))
check(flat_ok,
      f"d3 for every N tested up to 50, log[y^N (nu - 1)] is negative and DECREASING with y, so "
      f"y^N (nu - 1) -> 0: Route A's p is effectively infinite. Computed through log_nu_minus1() because "
      f"nu_minus1() underflows to a spurious 0.0 past y ~ 5e5 -- the float64 trap the corpus already "
      f"documented")

# --- the ephemeris bound as a condition on p, anchored on the committed LM fit
print("""
  NOW THE EPHEMERIS, CONVERTED INTO A CONDITION ON p. The anchor is the corpus's OWN committed
  Levenberg-Marquardt fit (agentE_solar_reflex.py, re-banked by mi_alpha2_sun_reflex_2026.py): six bodies,
  per-body mu INCLUDING the Sun, GM_sun + GM_J + 36 initial conditions free. Its result for alpha=2 is a
  post-fit Mars ranging residual of 12.74 m (canonical) / 18.6 m (alt) against a 1.5 m budget, i.e. 8.49x /
  12.40x over. The binding body is the SUN, whose Jupiter-driven reflex is 2.09e-7 m/s^2.

  ASSUMPTION, stated because it is the one soft joint in this section: the post-fit residual is taken
  PROPORTIONAL to the anomalous acceleration at the Sun, with the proportionality calibrated on alpha=2. The
  committed fit's own s^2 scaling supports proportionality in AMPLITUDE; what is assumed is that the
  ABSORPTION EFFICIENCY does not change with the tail's SHAPE. That is defensible here because for every
  p > 1 the anomaly is already Sun-dominated (the Sun's tail exceeds Mars's by >1e3 at p = 2 and by ~1e12 at
  p = 4), so steeper tails are MORE Sun-only, i.e. more like the shape the factor was calibrated on. The
  sensitivity to a factor 10 either way is computed below.""")

AU, GN = 1.496e11, 6.674e-11        # the committed anchor's own constants, so y_Sun reproduces exactly
M_J, R_J = 1.898e27, 5.204 * AU
G_SUN = GN * M_J / R_J**2
OVER = {"canon": 12.74 / 1.5, "alt": 18.6 / 1.5}
A0F = {"canon": A0_CANON, "alt": A0_ALT}
print(f"\n  Sun's reflex g = {G_SUN:.4e} m/s^2  ->  y_Sun = {G_SUN/A0_CANON:.1f} a0 (canon) / "
      f"{G_SUN/A0_ALT:.1f} (alt)")


def over_budget(num1_f, footing):
    """post-fit Mars residual / budget for a kernel, scaled off the committed alpha=2 anchor."""
    a0 = A0F[footing]
    yS = mp.mpf(G_SUN) / mp.mpf(a0)
    return OVER[footing] * (num1_f(yS) / num1_a2(yS))


cons = {f: float(over_budget(num1_a2, f)) for f in OVER}
check(all(abs(cons[f] / OVER[f] - 1) < 1e-12 for f in OVER),
      f"d4 the scaling is anchored, not invented: fed alpha=2 it returns exactly the committed "
      f"{cons['canon']:.2f}x (canonical) / {cons['alt']:.2f}x (alt) over the 1.5 m Mars budget")


def p_min(footing, slack=1.0):
    """smallest p with (1/p) y^(1-p) g_Sun <= slack * budget, solved on the asymptotic tail."""
    a0 = A0F[footing]
    yS = mp.mpf(G_SUN) / mp.mpf(a0)
    lim = num1_a2(yS) * slack / OVER[footing]          # allowed nu - 1 at the Sun

    def g(pv):
        return mp.log(1 / mp.mpf(pv)) - mp.mpf(pv) * mp.log(yS) - mp.log(lim)
    return float(mp.findroot(g, mp.mpf(2.5)))


PM = {f: p_min(f) for f in OVER}
print(f"\n  {'footing':<8}{'y_Sun':>9}{'allowed nu-1 at Sun':>22}{'p_min':>8}"
      f"{'p_min if absorption x10':>26}{'p_min if x1/10':>17}")
print("  " + "-" * 92)
sens = {}
for f in OVER:
    yS = mp.mpf(G_SUN) / mp.mpf(A0F[f])
    lim = float(num1_a2(yS) / OVER[f])
    sens[f] = (p_min(f, 10.0), p_min(f, 0.1))
    print(f"  {f:<8}{float(yS):>9.1f}{lim:>22.4e}{PM[f]:>8.3f}{sens[f][0]:>26.3f}{sens[f][1]:>17.3f}")
check(2.0 < PM["canon"] < 2.4 and 2.0 < PM["alt"] < 2.5
      and all(1.9 < sens[f][0] < 2.2 and 2.4 < sens[f][1] < 2.7 for f in OVER),
      f"d5 *** THE EPHEMERIS BOUND, AS A THEOREM-SHAPED CONDITION ON THE KERNEL: a viable kernel must have "
      f"nu - 1 = O(y^-p) with p >= {PM['canon']:.2f} (canonical) / {PM['alt']:.2f} (alt). *** The number is "
      f"robust: allowing the LM fit to absorb ten times MORE moves it only to "
      f"{sens['canon'][0]:.2f}/{sens['alt'][0]:.2f}, and ten times LESS only to "
      f"{sens['canon'][1]:.2f}/{sens['alt'][1]:.2f}. (p_min is quoted at the mu_p family's own amplitude "
      f"C = 1/p; a different C moves p_min only as ln C / ln y_Sun, i.e. by 0.09 per factor of 2.) So p_min "
      f"lies in (2, 2.7) on any reading -- which "
      f"immediately EXCLUDES alpha=1 (p=1), the simple mu (p=1) and alpha=2 (p=2), and is the sharpest way "
      f"to say why the framework's own two kernels failed the Solar System")

print(f"\n  and the per-kernel standing at the Sun, both footings (post-fit Mars residual / 1.5 m budget):")
print(f"  {'kernel':<32}{'p':>6}{'canon x over':>15}{'alt x over':>13}{'canon margin':>15}{'verdict':>10}")
print("  " + "-" * 93)
verdict = {}
for nm, mf, nf, om, p in KERNELS:
    oc, oa = float(over_budget(nf, "canon")), float(over_budget(nf, "alt"))
    verdict[nm] = max(oc, oa) < 1.0
    print(f"  {nm:<32}{('inf' if p is None else f'{p:.0f}'):>6}{oc:>15.3e}{oa:>13.3e}"
          f"{1/oc if oc > 0 else float('inf'):>15.3e}{'PASS' if verdict[nm] else 'FAIL':>10}")
check(verdict["Route A   1-mu = e^-sqrt(y)"] and verdict["power p=3 mu = x/(1+x^3)^(1/3)"]
      and verdict["power p=4 mu = x/(1+x^4)^(1/4)"]
      and not verdict["alpha=1   nu = sqrt(1+1/y)"] and not verdict["alpha=2   mu = x/sqrt(1+x^2)"]
      and not verdict["simple    mu = x/(1+x)"],
      f"d6 Route A clears by ~{1/float(over_budget(num1_routeA,'canon')):.1e}x -- but p = 3 clears by "
      f"~{1/float(over_budget(lambda y: num1_pow(y,3),'canon')):.1e}x and p = 4 by "
      f"~{1/float(over_budget(lambda y: num1_pow(y,4),'canon')):.1e}x, on both footings. *** So the "
      f"ephemeris does NOT force an exponential. It forces p >= 2.3, and the framework's own power family "
      f"reaches that at p = 3. Route A's exponential is SUFFICIENT, not necessary ***")

print("""
  *** AND THE TWO THRESHOLDS COINCIDE. *** Section (b) established that Milgrom 1994's kinetic function f is
  differentiable at the Newtonian point iff p > 2. Section (d) establishes that the Solar System requires
  p >= 2.26-2.32. These are the SAME threshold, reached from completely independent directions -- one from
  the mathematical regularity of a 1994 nonlocal action, one from Mars ranging in 2026 -- with the data
  marginally the stronger of the two. Every interpolating function in use sits at or below the marginal
  case, and that single fact explains both the corpus's analyticity exclusion and its ephemeris liability.""")


# ===================================================================== (e) UNIQUENESS, OR A CLASS
banner("(e)  IS ROUTE A UNIQUE? -- NO. AND THE CLASS CONTAINS A FULLY ADMISSIBLE POWER LAW")

t = sp.Symbol("t", positive=True)
mu4_x = xx / (1 + xx**4) ** sp.Rational(1, 4)
mu4_t = sp.simplify(mu4_x.subs(xx, 1 / sp.sqrt(t)))
check(sp.simplify(mu4_t - (1 + t**2) ** sp.Rational(-1, 4)) == 0,
      f"e1 in Milgrom's own variable t = a0^2/a^2 the p = 4 kernel is EXACTLY mu = (1 + t^2)^(-1/4) "
      f"(sympy residual {sp.simplify(mu4_t - (1+t**2)**sp.Rational(-1,4))}) -- a function of t^2, hence "
      f"ANALYTIC at t = 0 with NO LINEAR TERM. Those are precisely the two things Milgrom's analyticity "
      f"corollary demands")

ser4 = sp.series((1 + t**2) ** sp.Rational(-1, 4), t, 0, 8).removeO()
cm = {m: sp.nsimplify(sp.expand(ser4).coeff(t, m)) for m in range(1, 8)}
print(f"  mu_(p=4) - 1 = " + " + ".join(f"({cm[m]}) t^{m}" for m in range(1, 8) if cm[m] != 0) + " + ...")
bm = {m: sp.simplify(cm[m] / (1 - m)) for m in range(2, 8)}
print(f"  => via b_m = c_m/(1-m):  b_2 = {bm[2]}, b_3 = {bm[3]}, b_4 = {bm[4]}, b_6 = {bm[6]}")
b1s = sp.Symbol("b1s")
f4 = 1 + b1s * t + sum(bm[m] * t**m for m in range(2, 8))
recon = sp.expand(sp.simplify(f4 - t * sp.diff(f4, t)) - (1 + sum(cm[m] * t**m for m in range(1, 8))))
check(cm[1] == 0 and bm[2] == sp.Rational(1, 4) and bm[3] == 0 and bm[4] == -sp.Rational(5, 96)
      and sp.simplify(recon) == 0,
      f"e2 the reconstruction closes EXACTLY: the linear coefficient of mu - 1 is {cm[1]}, and the f built "
      f"from b_m = c_m/(1-m) satisfies f - t f' = mu identically (residual {sp.simplify(recon)}) with b_1 "
      f"free, b_2 = 1/4, b_3 = 0, b_4 = -5/96. *** THE p = 4 KERNEL HAS AN ANALYTIC MILGROM-1994 KINETIC "
      f"FUNCTION. *** It satisfies the fifth condition -- the one the corpus banked as excluding every "
      f"interpolating function in use, and the one Route A fails")

# b_1 for p=4 numerically vs the closed form, and b_2 from the tail integral vs 1/4
a_ex = mp.mpf(1) / 4
b1_4_closed = -a_ex * mp.sqrt(mp.pi) * mp.gamma(a_ex + mp.mpf(1) / 2) / mp.gamma(a_ex + 1)
b1_4_quad = -2 * mp.quad(lambda X: om_pow(X, 4) * X, [0, 1, 10, 100, mp.inf])
Q4b = mp.quad(lambda X: om_pow(X, 4) * X, [mp.mpf(10) ** 5, mp.mpf(10) ** 6, mp.inf])
b2_4_num = 2 * Q4b * (mp.mpf(10) ** 5) ** 2
check(abs(b1_4_quad / b1_4_closed - 1) < mp.mpf("1e-12") and abs(b2_4_num / mp.mpf("0.25") - 1) < 1e-8,
      f"e3 and its Taylor coefficients are confirmed two independent ways: b_1 = {float(b1_4_quad):.10f} from "
      f"quadrature vs the closed form -a sqrt(pi) Gamma(a+1/2)/Gamma(a+1) at a = 1/4 = "
      f"{float(b1_4_closed):.10f} (agreeing to {float(abs(b1_4_quad/b1_4_closed-1)):.1e}); and b_2 = "
      f"{float(b2_4_num):.8f} from the tail integral 2Q(T)T^2 vs the 1/4 the analyticity corollary demands. "
      f"Two derivations, one from an integral and one from a series, meeting at 1/4")

# radius of convergence: (1+t^2)^-1/4 = sum_k C(-1/4,k) t^2k, so b_2k = C(-1/4,k)/(1-2k) EXACTLY, and the
# nearest singularities are the branch points t = +-i, i.e. radius 1. Tested as |b_m|^(1/m) -> 1.
rad = {}
for k in (5, 10, 20, 40):
    bk = sp.binomial(sp.Rational(-1, 4), k) / (1 - 2 * k)
    rad[2 * k] = float(abs(bk) ** sp.Rational(1, 2 * k))
print(f"  |b_m|^(1/m) at m = " + ", ".join(f"{m}: {v:.4f}" for m, v in rad.items()))
ks = sorted(rad)
check(all(rad[ks[i]] < rad[ks[i + 1]] for i in range(len(ks) - 1)) and 0.85 < rad[80] < 1.0,
      f"e4 the radius of convergence is FINITE and equal to 1, so f_(p=4) is analytic on a genuine disc and "
      f"not merely formally: b_2k = C(-1/4,k)/(1-2k) exactly, and |b_m|^(1/m) climbs monotonically "
      f"{rad[10]:.4f} -> {rad[20]:.4f} -> {rad[40]:.4f} -> {rad[80]:.4f} toward 1 (the coefficients decay "
      f"only like k^-7/4, a power, which is what radius 1 looks like). The obstruction is the pair of branch "
      f"points t = +-i, exactly the same analytic structure as Milgrom's OWN worked example f = "
      f"(1+t)^(-1/2), whose radius is also 1 -- so 'non-singular at z = 0 in the complex plane' is satisfied "
      f"in precisely the sense he uses the phrase")

# p=4 is the minimal admissible member of the family
print(f"\n  which members of mu_p = x/(1+x^p)^(1/p) are admissible? in Milgrom's variable mu = "
      f"(1 + t^(p/2))^(-1/p):")
print(f"  {'p':>5}{'leading power of t in mu-1':>30}{'analytic in t?':>17}{'linear term zero?':>20}"
      f"{'admissible?':>13}")
print("  " + "-" * 85)
adm = {}
for pv in (2, 3, 4, 5, 6, 8):
    q = sp.Rational(pv, 2)
    analytic = q.is_integer
    nolin = q >= 2
    adm[pv] = bool(analytic and nolin)
    print(f"  {pv:>5}{str(q):>30}   {'yes' if analytic else 'NO (half-integer)':<19}"
          f"{'yes' if nolin else 'NO':<20}{'YES' if adm[pv] else 'no':<6}")
# corroborate the p=3 non-analyticity by locating the half-integer power itself: the leading term of 1 - mu
# must be t^(3/2) -- finite nonzero when divided by t^(3/2), and zero when divided by t^1.
one_m_mu3 = 1 - (1 + t ** sp.Rational(3, 2)) ** sp.Rational(-1, 3)
L32 = sp.simplify(sp.limit(one_m_mu3 / t ** sp.Rational(3, 2), t, 0))
L1 = sp.simplify(sp.limit(one_m_mu3 / t, t, 0))
print(f"  p = 3 corroboration:  (1-mu)/t^(3/2) -> {L32}  (finite, nonzero)   and  (1-mu)/t -> {L1}")
has_half = (L32 != 0 and L32.is_finite and L1 == 0)
check(adm[4] and adm[6] and adm[8] and not adm[2] and not adm[3] and not adm[5] and has_half,
      f"e5 *** p = 4 IS THE MINIMAL FULLY ADMISSIBLE MEMBER OF THE FRAMEWORK'S OWN POWER FAMILY. *** "
      f"Analyticity in t requires p/2 to be an integer, and the vanishing linear term requires p/2 >= 2, so "
      f"the admissible set is p in {{4, 6, 8, ...}}. p = 2 is analytic but has the forbidden linear term "
      f"(that is exactly its logarithmic f); p = 3 and p = 5 carry a genuine half-integer power of t "
      f"(verified: 1 - mu ~ t^(3/2) at p = 3), which is the same square-root branch point alpha=1 has")

# and p=4 passes everything else, in one place
o4c = float(over_budget(lambda y: num1_pow(y, 4), "canon"))
o4a = float(over_budget(lambda y: num1_pow(y, 4), "alt"))
check(all(health["power p=4 mu = x/(1+x^4)^(1/4)"]) and o4c < 1e-5 and o4a < 1e-5 and 4.0 > PM["alt"],
      f"e6 *** AND p = 4 PASSES EVERYTHING ELSE SIMULTANEOUSLY: *** all six BM health conditions (table in "
      f"(c)), Milgrom 2022's monotonicity in manifestly-positive closed form (table in (a)), exact BTFR with "
      f"coefficient 1 (mu/x -> 1), and the ephemeris by {1/o4c:.2e}x (canonical) / {1/o4a:.2e}x (alt). Since "
      f"analyticity forces p >= 4 and the Solar System only requires p >= {PM['alt']:.2f}, *** MILGROM 1994's "
      f"ANALYTICITY CONDITION IMPLIES THE EPHEMERIS BOUND. *** The theoretical admissibility condition is "
      f"STRICTLY STRONGER than the Solar-System data constraint, so a kernel that takes Milgrom 1994 "
      f"seriously never has an ephemeris problem in the first place")

print("""
  SO WHAT IS THE CLASS? Collecting every condition that survived as a real constraint:
      (i)   mu/x -> 1 as x -> 0            deep-MOND normalisation; a0's meaning; exact BTFR
      (ii)  dmu/dx > 0                     subluminality, and convexity of F in X
      (iii) d(x mu)/dx > 0                 Milgrom 2022 admissibility = AQUAL ellipticity = QUMOND
                                            invertibility (one inequality, three names)
      (iv)  1 - mu = O(x^-p), p >= 2.3     the ephemeris, from the committed LM fit, both footings
      (v)   1 - mu analytic in x^-2 and    Milgrom 1994 class (34) with an analytic f -- OPTIONAL, since
            starting at x^-4                Milgrom 2022 explicitly does not require an action at all
  (i)-(iv) define an INFINITE-DIMENSIONAL class. It contains the whole power family with p >= 2.3, every
  exponential 1 - mu = e^-h(x) with h(x) ~ x deep and h/ln x -> inf, and mixtures. Route A is ONE member;
  1 - mu = e^-x (McGaugh 2008) is another; p = 3 and p = 4 are others. THERE IS NO UNIQUENESS HERE and it
  would be wrong to claim any. Adding (v) narrows the class sharply -- to kernels whose Newtonian anomaly is
  a power series in (a0/a)^2 beginning at the fourth power -- and Route A is NOT in the narrowed class while
  p = 4 is.

  WHAT ROUTE A DOES HAVE, stated fairly and without inflation:
    * unbounded ephemeris margin (~1e12 vs p = 4's ~1e6), so no future tightening of planetary ranging can
      ever reach it. Real, but a 1e6 margin is not a live liability either.
    * a closed-form Bekenstein-Milgrom free function with health PROVED, already committed. p = 4's F is an
      incomplete-beta object; nothing suggests it is unhealthy (the table in (c) says it is not), but it is
      not in closed form and its field theory has not been built.
    * an exponent with a physical reading: 1 - mu = exp(-sqrt(g_bar/a0)) = exp(-g_M/a0) where
      g_M = sqrt(g_bar a0) is the deep-MOND acceleration. The suppression of the departure from Newton is
      set by the deep-MOND acceleration in units of a0. That is a genuine piece of structure, and it is
      MOTIVATION, not derivation.
    * C^infinity regularity of f, which alpha=1, alpha=2 and the simple mu do not have.
  WHAT IT DOES NOT HAVE: any admissibility that alpha=2 lacked on (a) or (c); membership of class (34); and
  necessity, since p = 3 already discharges the ephemeris and p = 4 discharges it AND is fully admissible.""")


# ===================================================================== bookkeeping owed
banner("BOOKKEEPING OWED -- two credit lines and three tautologies found in committed files")

src_mod = open(os.path.join(HERE, "mi_route_a_kernel.py")).read()
src_adopt = open(os.path.join(HERE, "mi_route_a_exponential_kernel_2026.py")).read()
mod_shape_credit = [k for k in ("McGaugh", "Lelli", "Schombert", "RAR") if k in src_mod]
adopt_credits = "McGaugh" in src_adopt
check(mod_shape_credit == [] and adopt_credits,
      f"z1 CREDIT LINE OWED IN THE SINGLE SOURCE OF TRUTH. nu = 1/(1 - e^-sqrt(y)) is the RAR fitting "
      f"function of McGaugh, Lelli & Schombert 2016 (PRL 117:201101); the adopting script "
      f"mi_route_a_exponential_kernel_2026.py says so explicitly ('n = 2 is the McGaugh-RAR form'), but "
      f"mi_route_a_kernel.py -- the module every disc re-solve imports, and the file a referee will read as "
      f"THE definition of the kernel -- names no shape prior art at all (McGaugh / Lelli / Schombert / RAR "
      f"all absent: {mod_shape_credit}); its only citation is to Milgrom 2020 for the kappa = 1/2pi "
      f"comparator. The corpus already applies exactly this discipline to nu = sqrt(1+1/y) (Milgrom 1999 PLA "
      f"253:273 eq 9). Note the second-order consequence too: the standing rule 'never judge the framework "
      f"through McGaugh's nu' now needs restating, because under Route A the framework's OWN nu IS his. "
      f"Reported, NOT edited")

taut = open(os.path.join(HERE, "mi_milgrom1994_home_test_2026.py")).read().count("check(True is not False")
check(taut >= 4,
      f"z2 TAUTOLOGIES STILL LIVE IN A COMMITTED FILE: real_research/reviews/"
      f"mi_milgrom1994_home_test_2026.py contains {taut} occurrences of `check(True is not False, ...)` "
      f"(T2, T3, T4, T5) -- conditions that cannot fail. A fifth, softer one is in "
      f"reviews/mi_eq34_inversion_banked_2026.py: its B2a `check(all(o < 4 ...))` tests a variable that the "
      f"loop above it can only ever set to 1 or 2, so `< 4` is structurally unfailable. Reported here rather "
      f"than edited, per the standing rule; the SUBSTANCE of both scripts reproduces and is not in question")


banner("RESULT")
n = sum(1 for c, _ in ok if c)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("""  Exit 0. THE LANE'S ANSWER, in one paragraph:

  Route A is NOT admissible where the power laws were not. On Milgrom 2022 and on the Bekenstein-Milgrom
  health set it passes and so does every comparator -- both conditions are non-discriminating, and no
  argument for Route A may lean on either. On Milgrom 1994's analyticity condition it FAILS, as all four
  comparators do, though by the mildest mechanism available (C^infinity rather than not-C^1). Where Route A
  genuinely wins is the Newtonian RATE, and that win is now a theorem rather than a number: the ephemeris
  requires nu - 1 = O(y^-p) with p >= 2.26 canonical / 2.32 alt, robust to a factor ten in the fit's
  absorption, and independently Milgrom's kinetic function is differentiable only for p > 2 -- the same
  threshold from two unrelated directions. Route A satisfies it with p = infinity. But so does the
  framework's own power family from p = 3 up, and p = 4 satisfies EVERY condition tested here including the
  analyticity Route A forfeits, with a 1e6 ephemeris margin. Route A is one member of an
  infinite-dimensional admissible class, distinguished by margin and by a closed-form free function, not by
  necessity and not by admissibility. p = 4 has not been priced on SPARC, on the seven re-solved disc/front
  numbers, or on the wide-binary gate, and it must be before anyone acts on this.""")
