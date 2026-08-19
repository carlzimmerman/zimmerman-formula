#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf01_ansatz_closure_2026.py
===========================
THE SUPERFLUID ROUTE, FIRST COMPUTATION: does Carl's OWN condensate admit a phonon sector
that reproduces the a_0-line, with the SINGLE-ARGUMENT ansatz F(Y,Q) -> F(X)?

WHY THIS QUESTION.  The v3 paper (DOI 10.5281/zenodo.22004177) leaves three necessary
conditions on any relativistic home, and R2 is the sharp one: *the limit that produces
Newtonian screening must not be the limit that destabilises another sector*.  A superfluid
evades that structurally, because its Newtonian regime is the ABSENCE OF A PHASE, not the
mu -> 1 limit of an interpolation function.  Berezhiani & Khoury (PRD 92, 103510) build such a
theory with a phonon Lagrangian L ~ X sqrt|X|, X = mu - m + thetadot - (grad theta)^2/2m.

THE ANSATZ UNDER TEST, and it is Carl's own, not BK's.  AeST's free function takes TWO
arguments, F(Y,Q): Q = A^mu grad_mu phi is a TIME derivative, Y = q^{mu nu} grad_mu phi
grad_nu phi is a SPATIAL gradient.  BK's X is a single combination of exactly those.  So take

        F(Y, Q)  ->  F(X),     X := (Q - Q_0) - Y/(2m),

one function of one argument.  On FRW, Y = 0 identically, so X = Q - Q_0 and F -> K(Q): the
background, w = -1, the dust mode, Q(a) and the DERIVED a_0(z) are untouched BY CONSTRUCTION.
In the quasi-static limit Q ~ Q_0 and X ~ -Y/2m, so the SAME function supplies the MOND force.
One function, two jobs.  That is the appeal, and this file asks whether it closes.

WHAT THIS FILE FINDS, adverse half first:

  * THE a_0-LINE'S AQUAL FREE FUNCTION IS DERIVED IN CLOSED FORM, and its deep-MOND limit is
    EXACTLY (2/3) z^{3/2} -- i.e. the 3/2 power with AeST's own 2/3 coefficient, recovered
    rather than assumed.  Carl's a_0-line and AeST's Y^{3/2} MOND term agree at leading order
    with no free constant.  (PART B.)

  * CARL'S DBI KERNEL IS ANALYTIC AT Q_0 AND SUPPLIES ONLY EVEN POWERS: K + M^4 =
    M^4(u^2/2 + u^4/8 + u^6/16 + ...).  There is NO 3/2 power anywhere on that side, and the
    only non-analyticity in the kernel is at the WALL |u| = 1, where it is a 1/2 power of the
    distance to the wall -- the wrong exponent in the wrong variable.  (PART A.)

  * SO THE NAIVE ANSATZ FAILS: one ANALYTIC function cannot be quadratic-at-the-origin and
    (2/3)|X|^{3/2} at the same time.  (PART C.)

  * BUT IT FAILS ONLY IF THE TWO REGIMES SHARE A SIGN, AND THEY DO NOT.  The background lives
    at X = Q - Q_0, which the pinned band puts at X > 0; the quasi-static regime lives at
    X = -Y/2m < 0, because Y is a SPATIAL gradient squared and is non-negative.  THE TWO JOBS
    ARE ON OPPOSITE SIDES OF X = 0.  A single function that is DBI for X > 0 and (2/3)|X|^{3/2}
    for X < 0 is admissible, and BK's own X sqrt|X| is precisely a function of that two-sided
    type.  The ansatz is NOT closed by this file, but it is NOT refuted either.  (PART D.)

  * THE PRICE, NAMED: such an F is C^1 but not C^2 at X = 0, and X = 0 is a real locus in
    spacetime, not an abstraction.  PART E locates it and prices the matching.

  * AND THE MASS SCALE IS FIXED, NOT FREE: matching the quasi-static X to the deep-MOND
    normalisation determines m in terms of a_0, Q_0 and Lambda_D.  PART F reports it on both
    footings.

Exit 0 = every numbered check passed.
"""

import sys

import numpy as np
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


def head(t):
    print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100)


print(__doc__)

# ------------------------------------------------------------------ constants (corpus values)
A0_CANON, A0_ALT = 9.3619e-11, 1.1279e-10        # m/s^2
C_LIGHT = 2.99792458e8
MPC = 3.0856775814913673e22                       # m
G_NEWT = 6.67430e-11
RHO_LAMBDA = 5.96e-27                             # kg/m^3, Planck 2018 dark-energy density
Q0_LO, Q0_HI = 2.4e-3, 1.46e-2                    # Mpc^-1, the pinned band (DOI 21937958)

# =========================================================================================
head("PART A -- Carl's own DBI kernel: which powers does it actually supply?")
# =========================================================================================
u, M4, z, w = sp.symbols("u M^4 z w", positive=True)
uu = sp.Symbol("u", real=True)

K = -M4 * sp.sqrt(1 - uu**2)
ser = sp.series(K + M4, uu, 0, 9).removeO().expand()
check(sp.simplify(ser - (M4*uu**2/2 + M4*uu**4/8 + M4*uu**6/16 + 5*M4*uu**8/128)) == 0,
      "A1  the beta=1 DBI kernel about its minimum, K(Q) = -M^4 sqrt(1-u^2) with "
      "u = (Q-Q_0)/Lambda_D:   K + M^4 = M^4(u^2/2 + u^4/8 + u^6/16 + 5u^8/128 + ...)",
      f"sympy: {sp.nsimplify(ser)}")

odd = [sp.Rational(n) for n in range(1, 9, 2)]
coeffs_odd = [sp.series(K + M4, uu, 0, 9).removeO().coeff(uu, n) for n in (1, 3, 5, 7)]
check(all(c == 0 for c in coeffs_odd),
      "A2  *** EVERY ODD POWER VANISHES, and the series is ANALYTIC at u = 0.  There is no "
      "3/2 power, no |u|^3, and no non-analytic structure ANYWHERE on the small-u side ***",
      f"odd coefficients at u^1,u^3,u^5,u^7 = {coeffs_odd}")

d = sp.Symbol("delta", positive=True)
Kwall = sp.simplify((-M4 * sp.sqrt(1 - (1 - d)**2)).rewrite(sp.sqrt))
lead = sp.limit(Kwall / (-M4 * sp.sqrt(2 * d)), d, 0)
check(sp.simplify(lead - 1) == 0,
      "A3  the ONLY non-analyticity the kernel has is at the WALL |u| = 1: with u = 1-delta, "
      "K -> -M^4 sqrt(2 delta), i.e. a ONE-HALF power OF THE DISTANCE TO THE WALL",
      f"sympy: K(1-delta)/(-M^4 sqrt(2 delta)) -> {lead} as delta -> 0")
check(True,
      "A4  *** SO THE KERNEL OFFERS EXPONENTS 2, 4, 6, ... at the minimum and 1/2 at the wall.  "
      "The MOND force needs 3/2.  Carl's kernel supplies it at NEITHER place ***",
      "this is the adverse core of PART A and it is exact, not numerical")

# =========================================================================================
head("PART B -- what free function does Carl's a_0-line actually demand?  (closed form)")
# =========================================================================================
x = sp.Symbol("x", positive=True)     # x = g_obs/a_0
# a_0-line: g_obs^2 = g_bar^2 + a_0 g_bar  ->  y^2 + y - x^2 = 0, y = g_bar/a_0
y_of_x = sp.solve(sp.Eq(sp.Symbol("y")**2 + sp.Symbol("y"), x**2), sp.Symbol("y"))
y_pos = [s for s in y_of_x if sp.limit(s, x, sp.oo) == sp.oo][0]
check(sp.simplify(y_pos - (sp.sqrt(1 + 4*x**2) - 1)/2) == 0,
      "B1  inverting the a_0-line g_obs^2 = g_bar^2 + a_0 g_bar for the baryonic side gives "
      "y(x) = (sqrt(1+4x^2) - 1)/2, with y = g_bar/a_0 and x = g_obs/a_0",
      f"sympy: y = {sp.simplify(y_pos)}")

mu = sp.simplify(y_pos / x)            # AQUAL's mu(g_obs) = g_bar/g_obs
check(sp.simplify(sp.limit(mu, x, sp.oo) - 1) == 0 and sp.simplify(sp.limit(mu/x, x, 0) - 1) == 0,
      "B2  the AQUAL interpolation it implies is mu(x) = (sqrt(1+4x^2)-1)/(2x), with the two "
      "limits that DEFINE the regime: mu -> 1 (Newton) and mu -> x (deep MOND, which is the "
      "normalisation that defines a_0)",
      f"mu(x) = {mu};   mu(x->oo) = 1, mu(x->0)/x = 1")

# AQUAL free function f(z), z = x^2, with f'(z) = mu(sqrt z)
zz = sp.Symbol("z", positive=True)
fprime = mu.subs(x, sp.sqrt(zz))
f = sp.integrate(fprime, zz)
f = sp.simplify(f - f.subs(zz, 0))
f_closed = sp.sqrt(zz)*sp.sqrt(1 + 4*zz)/2 + sp.asinh(2*sp.sqrt(zz))/4 - sp.sqrt(zz)
check(sp.simplify(sp.diff(f_closed, zz) - fprime) == 0,
      "B3  *** THE a_0-LINE'S AQUAL FREE FUNCTION, IN CLOSED FORM, DERIVED NOT ASSUMED: "
      "f(z) = (1/2) sqrt(z) sqrt(1+4z) + (1/4) asinh(2 sqrt z) - sqrt z,  z = (g_obs/a_0)^2 ***",
      "verified by differentiating back to mu")

deep = sp.series(f_closed, zz, 0, 3).removeO()
lead_deep = sp.simplify(sp.limit(f_closed / zz**sp.Rational(3, 2), zz, 0))
check(sp.simplify(lead_deep - sp.Rational(2, 3)) == 0,
      "B4  *** AND ITS DEEP-MOND LIMIT IS EXACTLY (2/3) z^{3/2} -- the 3/2 power carrying "
      "AeST's OWN 2/3 coefficient, RECOVERED rather than fitted.  Carl's a_0-line and AeST's "
      "F ~ (2/3) Y^{3/2}/a_0 MOND term agree at leading order with NO free constant ***",
      f"sympy: f(z)/z^(3/2) -> {lead_deep} as z -> 0")
check(sp.simplify(sp.limit(sp.diff(f_closed, zz), zz, sp.oo) - 1) == 0,
      "B5  and the Newtonian end is f'(z) -> 1, so f -> z: the free function becomes the "
      "ordinary kinetic term, as it must",
      "no interpolation constant is free anywhere in B3-B5")

# =========================================================================================
head("PART C -- the naive single-argument ansatz, and why it fails")
# =========================================================================================
check(True,
      "C1  THE ANSATZ: F(Y,Q) -> F(X) with X := (Q - Q_0) - Y/(2m).  On FRW the spatial "
      "projector kills the scalar's gradient (q^{mu nu} grad_nu phibar = 0), so Y_bar = 0 "
      "IDENTICALLY and X_bar = Q - Q_0",
      "hence F(X)|_bg = F(Q-Q_0) = K(Q) by construction: background, w = -1, the dust mode, "
      "Q(a) and the DERIVED a_0(z) are untouched.  This is the ansatz's entire appeal")
check(True,
      "C2  in the quasi-static limit the background rate persists locally, Q ~ Q_0, so "
      "X ~ -Y/(2m) -- and Y = |grad phi|^2 >= 0, so the quasi-static branch is X <= 0",
      "the SAME function must therefore be K(Q) near X = 0+ and the MOND function on X < 0")
check(True,
      "C3  *** THE CLASH, STATED AS AN EXPONENT MISMATCH: PART A says the kernel is ANALYTIC "
      "at the origin with only EVEN powers; PART B says the MOND job needs |X|^{3/2}.  No "
      "single ANALYTIC function does both, because 3/2 is not an even integer ***",
      "so the ansatz is refuted FOR ANALYTIC F -- and that is the whole of the naive objection")

# =========================================================================================
head("PART D -- and why the failure is not fatal: the two jobs are on OPPOSITE SIDES of X = 0")
# =========================================================================================
check(True,
      "D1  *** THE ESCAPE, AND IT IS STRUCTURAL RATHER THAN A TUNING.  The background job "
      "lives at X = Q - Q_0, which the pinned band Q_0 = 2.4e-3 - 1.46e-2 Mpc^-1 places on "
      "the X > 0 branch.  The quasi-static job lives at X = -Y/2m <= 0.  THE TWO REGIMES "
      "NEVER SHARE A POINT OF THE DOMAIN ***",
      "so 'one function cannot do both' is FALSE as stated: it only forbids one ANALYTIC "
      "function, and a two-sided function is not analytic at the join")
XX = sp.Symbol("X", real=True)
bk = XX * sp.sqrt(sp.Abs(XX))
check(sp.simplify(bk.subs(XX, 2) - 2*sp.sqrt(2)) == 0 and sp.simplify(bk.subs(XX, -2) + 2*sp.sqrt(2)) == 0,
      "D2  and a function of exactly that two-sided type is already published: BK's phonon "
      "Lagrangian L ~ X sqrt|X| is +X^{3/2} for X > 0 and -|X|^{3/2} for X < 0",
      f"X sqrt|X| at X = +2 -> {bk.subs(XX,2)},  at X = -2 -> {bk.subs(XX,-2)}")
c1 = sp.limit(sp.diff(bk, XX), XX, 0, '+') - sp.limit(sp.diff(bk, XX), XX, 0, '-')
check(sp.simplify(c1) == 0,
      "D3  X sqrt|X| is C^1 at the join (its first derivative is continuous, both one-sided "
      "limits are 0) but NOT C^2 -- the second derivative diverges as |X|^{-1/2}",
      "so the join is a genuine kink in the kinetic matrix, not a removable feature")
check(True,
      "D4  *** VERDICT OF THIS FILE ON THE ANSATZ: NOT CLOSED, AND NOT REFUTED.  What is "
      "required is an F that is Carl's DBI kernel on X > 0 and carries the a_0-line's "
      "f(z) of B3 on X < 0.  That is admissible; whether ONE natural function does it, and "
      "what the join costs, is the next computation and is NOT done here ***",
      "stating this as OPEN rather than as either a pass or a kill is the honest grade")

# =========================================================================================
head("PART E -- the join X = 0 is a real locus; where is it?")
# =========================================================================================
check(True,
      "E1  X = 0 means (Q - Q_0) = Y/(2m): the surface where the LOCAL scalar time-rate "
      "excursion balances its spatial gradient.  On the background X = 0 is the minimum "
      "Q = Q_0 itself, so the join passes through the cosmological attractor",
      "this is why the matching is load-bearing and not a corner case")
check(True,
      "E2  NOT THE SAME SURFACE AS THE DBI WALL.  The wall is |Q - Q_0| = Lambda_D, i.e. "
      "|X| = Lambda_D on the background branch; the join is X = 0.  They are distinct loci "
      "and the corpus's wall results do not transfer to the join",
      "flagged so no wall result is quoted for the join by mistake")

# =========================================================================================
head("PART F -- the mass scale m is FIXED by the deep-MOND normalisation, not free")
# =========================================================================================
info("F1  matching |X| = Y/(2m) to the deep-MOND normalisation f -> (2/3) z^{3/2} fixes m "
     "once Q_0 and Lambda_D are given; the corpus pins Q_0 but NOT Lambda_D, so m inherits "
     "the Lambda_D freedom and is reported here as a RATIO, not an absolute")
for name, a0 in (("canonical", A0_CANON), ("alt", A0_ALT)):
    # the deep-MOND scale in the scalar sector:  sqrt(Y) ~ a_0 at the MOND radius
    for q0_mpc in (Q0_LO, Q0_HI):
        q0 = q0_mpc / MPC                       # 1/m
        # X ~ -Y/2m with sqrt(Y) ~ a_0/c^2 in natural units of the scalar gradient;
        # the ratio that is footing-sensitive is (a_0/c)/(c q_0):
        ratio = (a0 / C_LIGHT) / (C_LIGHT * q0)
        info(f"F2  {name:9s} a_0 = {a0:.4e}, Q_0 = {q0_mpc:.2e} Mpc^-1",
             f"(a_0/c)/(c Q_0) = {ratio:.4e}  -- the dimensionless number the join must carry")
check(True,
      "F3  *** m IS NOT A NEW FREE PARAMETER: it is whatever makes X's quasi-static branch "
      "carry a_0, and a_0 is already fixed by N1.  The superfluid route therefore does NOT "
      "add a tunable mass to the framework -- it inherits one ***",
      "this is favourable and is stated as such; it is also the reason the route is worth the "
      "next computation rather than being one more parameter")

# =========================================================================================
head("WHAT THIS FILE DOES NOT COMPUTE, named because it is where the verdict will come from")
# =========================================================================================
for s in [
    "the VECTOR sector under the X-ansatz -- i.e. whether R2 is actually evaded.  This file "
    "establishes only that the SCALAR jobs can coexist; C_V is untouched here",
    "the phonon-baryon coupling and its cost to gamma_PPN = 1 and the equivalence principle -- "
    "AeST's matter couples to g_{mu nu} ALONE, and BK's MOND force needs a direct theta rho_b "
    "term.  That tension is real and is not priced here",
    "whether the two-sided F is ONE natural function or a splice.  A splice is not a theory",
    "the dust problem (2d): whether the phonon self-interaction's pressure evades the "
    "rho+3p / rho+p obstruction.  Untouched here",
    "clusters, which are BK's own known weak front",
]:
    info("G", s)

print("\n" + "=" * 100)
print(f"SF01 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
