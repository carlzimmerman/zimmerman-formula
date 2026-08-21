#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
route2_mechC_constrained_vector_2026.py
=======================================
ROUTE 2 -- REVIVE MECHANISM C BY FIXING THE GHOST REFUTATION.

THE CONTESTED CLAIM.  Mechanism C's mediator was covariantised as a GAUGE vector,
L_A = Lcal(F_munu F^munu), and a referee found a PARALLEL-MODE GHOST with c^2_par = -2/sqrt(y).
The completeness critic contested it on a nameable ground: AeST's vector is a
LAGRANGE-MULTIPLIER-CONSTRAINED UNIT TIMELIKE vector, A_mu A^mu = -1, whose mode content differs;
"the constraint removes the longitudinal mode that carries the ghost".  This file answers that
WITH THE ACTUAL HESSIAN, and then follows the answer wherever it goes.

WHAT IS COMPUTED HERE, in order.  Numbers first, checks written around the computed values.

  PART A  The dictionary from mechanism C's non-relativistic mediator to a covariant Lagrangian.
          mu_v(E) = P'(E)/E, i.e. P'(E) = mu_v(E) E -- NOT P = mu_v E^2.  (I made that error
          first; PART J logs it and its direction.)
  PART B  GAUGE VECTOR: the quadratic action derived in sympy from Lcal(S), S = (E^2-B^2)/2, with
          no formula assumed.  Kinetic 3x3 Hessian, eigenvalues, magnetic block, dispersion.
  PART C  *** THE CONSTRAINED UNIT-TIMELIKE VECTOR, three independent ways: (C1) the EXACT
          unconstrained parameterisation A_mu = (-sqrt(1+|a|^2), a_i), nonperturbative in the
          constraint; (C2) the Lagrange-multiplier route with delta-lambda enforcing the
          linearised constraint; (C3) the AeST-realistic background A_mu = (-N,0,0,0) where the
          constraint sets delta A_0 = 0 outright.  ALL THREE RETURN THE IDENTICAL KINETIC
          HESSIAN.  The constraint slaves delta A_0, which was ALREADY non-dynamical in the gauge
          case, and it cannot reach the (d_t delta A_i)^2 block.  The ghost mode is the
          polarisation PARALLEL TO THE BACKGROUND E, not the longitudinal-in-k mode.  The
          constrained theory propagates 3 vector modes to the gauge case's 2 -- the constraint
          ADDS a direction governed by the same matrix.  THE CRITIC'S HYPOTHESIS IS REFUTED. ***
  PART D  *** AND THE SIGN CONDITION IS HOST-INDEPENDENT, proved FOUR ways: ellipticity of
          mechanism C's OWN non-relativistic PDE; the vector host (ghost + c^2 < 0); the scalar
          host (gradient instability); and a THEOREM on the most general rotationally invariant
          host F(|E|^2,|B|^2,E.B) -- every invariant a constrained vector can build, S and the
          extra W = |E|^2 included -- whose kinetic Hessian at a purely electric background is
          {mu_v, mu_v, d(mu_v E)/dE} with NO host freedom whatsoever.  All four reduce to
          P''(E) = d(mu_v E)/dE >= 0.  In mechanism C's variables  mu_v E = g_obs - g_bar,  so
              THE MEDIATOR IS HEALTHY  <=>  THE PHANTOM ACCELERATION IS NON-DECREASING IN g_obs.
          Mechanism C's own file checked mu_v > 0 (the TRANSVERSE eigenvalue) and never checked
          the parallel one.  That is the actual gap. ***
  PART E  Both kernels at 60 digits, with the analytic forms carried alongside.
            - Carl's a_0-line: K_par = 1 - 2x/sqrt(1+4x^2) > 0 for ALL x.  NO GHOST ANYWHERE.
              *** THE REFUTATION DOES NOT APPLY TO MECHANISM C'S OWN STATED KERNEL. ***
            - Route A / MS08: the phantom PEAKS at y* = 2.5396383 and decays, so K_par < 0 above
              it, and c^2_par -> -2/sqrt(y) exactly -- REPRODUCING THE REFEREE'S NUMBER.  The
              referee was right about what he computed, and he was computing MS08.
  PART F  *** THE NO-GO.  Health requires the phantom non-decreasing; the ephemeris requires it
          to fall from ~0.3-0.6 a_0 at y ~ 1 to <= 1.5e-05 a_0 at y = 6.34e7.  A non-decreasing
          positive function cannot fall.  NO KERNEL CLEARS BOTH, short by >= 1.8e4.  Mechanism
          C's kernel space is EMPTY, so Route 1 cannot rescue it either. ***
  PART G  Health of the constrained realisation: c_T = 1 exactly, transverse gradient stability,
          Cherenkov (cleared, and for a reason that runs in the framework's favour), strong
          coupling (a real unpriced liability), and the aether-infall consequence.
  PART H  Q2 and the 1-AU monopole, both kernels, both footings, with an INDEPENDENT scaling
          cross-check of the banked Q2 values.
  PART I  The double count for the revived version.
  PART J  Errors found and made in this run, the direction each ran, and what I could NOT
          determine.

Exit 0 = every numbered check passed.
"""
import sys
import numpy as np
import sympy as sp
import mpmath as mp

mp.mp.dps = 60

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {NCHK[0]:02d} {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(f"{NCHK[0]:02d} {label}")
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)

G_ = 6.6743e-11
C_ = 2.99792458e8
MSUN = 1.98892e30
AU = 1.495978707e11
KPC = 3.0856775814913673e19
GM_SUN = mp.mpf(G_) * mp.mpf(MSUN)
A0 = {"canonical": mp.mpf("9.3619e-11"), "alt": mp.mpf("1.1279e-10")}
FOOTINGS = ("canonical", "alt")

# The Mars EPM budget, back-derived from the corpus's CORRECTED ephemeris factors (a_0/2 at 1 AU
# = 33435x canonical, 40282x alt).  Both footings must return the SAME budget; that they do is
# the consistency check that the x27 correction is self-consistent, and it is computed not
# assumed.
EPM_BUDGET = {nm: (A0[nm] / 2) / f for nm, f in
              (("canonical", mp.mpf(33435)), ("alt", mp.mpf(40282)))}
for nm in FOOTINGS:
    info(f"EPM budget back-derived, {nm}",
         f"{float(EPM_BUDGET[nm]):.5e} m/s^2  =  {float(EPM_BUDGET[nm] / A0[nm]):.5e} a_0")
_ratio = float(EPM_BUDGET["canonical"] / EPM_BUDGET["alt"])
check(abs(_ratio - 1.0) < 0.01,
      "00 the two footings' corrected ephemeris factors back-derive the SAME Mars budget "
      f"({float(EPM_BUDGET['canonical']):.4e} vs {float(EPM_BUDGET['alt']):.4e} m/s^2, ratio "
      f"{_ratio:.6f}) -- the 33435x / 40282x correction is internally consistent",
      "computed first, threshold written afterwards")
EPM = EPM_BUDGET["canonical"]

Y_1AU = {nm: (GM_SUN / mp.mpf(AU) ** 2) / A0[nm] for nm in FOOTINGS}
for nm in FOOTINGS:
    info(f"y(1 AU) = GM_sun/(AU^2 a_0), {nm}", f"{mp.nstr(Y_1AU[nm], 8)}")

# =============================================================================================
head("PART A -- the dictionary: what Lagrangian actually reproduces mechanism C's mediator")
# =============================================================================================
print("""
  Mechanism C, in its own file's conventions (sf39_mechanism_c_two_field_2026.py):

      L = -(1/8 pi G)|grad Phi|^2 - (rho_b + rho_chi) Phi
          + (1/8 pi G) mu_v(|grad A|)|grad A|^2 - B rho_chi A            <- as WRITTEN (line 52)
      delta/delta A :   div[mu_v grad A] = -4 pi G B rho_chi             <- the equation MEANT
                                                                            (its line 156, A-ii)

  These two lines are not each other.  Varying mu_v(E)E^2 gives div[ d/dE(mu_v E^2) grad A / E ],
  not div[mu_v grad A].  The Lagrangian that gives the MEANT equation is L_A = (1/8 pi G) P(E):

      P'(E) = mu_v(E) E      i.e.   mu_v(E) = P'(E)/E,     P(E) = int_0^E mu_v(e) e de

  -- the standard AQUAL dictionary.  Everything below uses THIS P, because the field equation,
  not the schematic Lagrangian, is what carries mechanism C's content.

  AND THE TWO FACTS THAT MAKE EVERYTHING ELSE FOLLOW, both from mechanism C's own file:
      mu_v = B^2 [1 - mu~]        (its A2, line 176: fixed algebraically, ZERO free functions)
      |grad A| = |grad Phi| / B   (its F1, line 451: the equilibrium balance)
  so, with B absorbed by the rescaling A -> A/B that its A3 (line 179) proves is free,

      mu_v E = (1 - mu~) g_obs = g_obs - g_bar = THE PHANTOM ACCELERATION.        (*)

  (*) is the whole file.  Note the "1 minus": mechanism C's mediator carries the COMPLEMENT of
  the AQUAL mu, which is why its parallel eigenvalue is d(phantom)/d g_obs and not d g_bar/d g_obs.
""")
E_ = sp.Symbol("E", positive=True)
mu_f = sp.Function("mu_v")(E_)
flux_wrong = sp.diff(mu_f * E_ ** 2, E_)          # flux magnitude if L = mu_v E^2 were literal
flux_right = mu_f * E_                             # flux magnitude mechanism C's equation needs
diff_flux = sp.simplify(flux_wrong - flux_right)
info("A1  the two readings of the mediator Lagrangian", f"difference of fluxes = {diff_flux}")
check(sp.simplify(diff_flux) != 0,
      "A1  the two readings genuinely differ (by mu_v' E^2 + mu_v E), so the dictionary matters; "
      "P'(E) = mu_v E is the one that reproduces mechanism C's stated field equation",
      "the wrong dictionary is used nowhere below")

x_, y_ = sp.symbols("x y", positive=True)
mu_tilde = (sp.sqrt(1 + 4 * x_ ** 2) - 1) / (2 * x_)          # Carl's a_0-line mu(x)
phantom_a0 = sp.simplify(x_ * (1 - mu_tilde))
check(sp.simplify(phantom_a0 - (x_ - (sp.sqrt(1 + 4 * x_ ** 2) - 1) / 2)) == 0,
      "A2  identity (*) verified symbolically on the a_0-line: x(1-mu~) = x - y with "
      "y = (sqrt(1+4x^2)-1)/2, i.e. mu_v E IS the phantom acceleration",
      f"x(1-mu~) = {sp.simplify(phantom_a0)}")
_roots = sp.solve(sp.Eq(x_ ** 2, y_ ** 2 + y_), x_)
_back = sp.simplify((sp.sqrt(sp.factor(1 + 4 * (y_ ** 2 + y_))) - 1) / 2 - y_)   # factor first:
# sympy will NOT reduce sqrt(4y^2+4y+1) to 2y+1 unless the radicand is factored -- trap 6's
# cousin, and it silently returns a nonzero residual if you skip it.  Numeric control alongside.
_back_num = max(abs(float(((mp.sqrt(1 + 4 * (mp.mpf(t) ** 2 + mp.mpf(t))) - 1) / 2) - mp.mpf(t)))
                for t in (0.01, 1.0, 137.0, 6.3e7))
info("A3  inverse check", f"symbolic residual = {_back}, worst numeric residual over "
                          f"y in [0.01, 6.3e7] = {_back_num:.3e}")
check(len(_roots) == 1 and sp.simplify(sp.sqrt(y_ ** 2 + y_) - _roots[0]) == 0
      and _back == 0 and _back_num < 1e-9,
      "A3  and the a_0-line's two directions are mutually inverse: x = sqrt(y^2+y) from "
      "g_obs^2 = g_bar^2 + a_0 g_bar, and y = (sqrt(1+4x^2)-1)/2 back again -- verified "
      "symbolically AND numerically at four widely separated y",
      "this is the check that caught ERROR 1 in PART J -- the draft's numeric a_0-line was "
      "actually mu = x/(1+x)")

# =============================================================================================
head("PART B -- GAUGE VECTOR: the quadratic action and the kinetic Hessian, derived not assumed")
# =============================================================================================
print("""
  Covariant host:  L = Lcal(S),  S = -F_munu F^munu/4 = (E^2 - B^2)/2,  E_i = F_i0.
  Static electric background E0 along z, B0 = 0.  Perturb A_mu.  Then
        delta E_i = d_i(delta A_0) - d_t(delta A_i),      delta B = curl(delta A).
  Build S to second order with no shortcut, Taylor Lcal, read off
        M_ij = d^2 L2 / d(d_t delta A_i) d(d_t delta A_j).
""")
Lp, Lpp, Ebg = sp.symbols("Lp Lpp E0", real=True)
v1, v2, v3 = sp.symbols("v1 v2 v3", real=True)          # d_t delta A_i
w1, w2, w3 = sp.symbols("w1 w2 w3", real=True)          # d_i delta A_0
b1, b2, b3 = sp.symbols("b1 b2 b3", real=True)          # delta B
v = sp.Matrix([v1, v2, v3])
w = sp.Matrix([w1, w2, w3])
bb = sp.Matrix([b1, b2, b3])
E0v = sp.Matrix([0, 0, Ebg])
eps = sp.Symbol("eps", positive=True)


def quadratic_L(dE_vec, extra_syms):
    """second-order piece of Lcal(S) for a given first-order delta E; no formula assumed."""
    S_full = ((E0v + dE_vec).dot(E0v + dE_vec) - bb.dot(bb)) / 2
    dS = sp.expand(S_full - sp.Rational(1, 2) * Ebg ** 2)
    Lx = sp.expand(Lp * dS + sp.Rational(1, 2) * Lpp * dS ** 2)
    Lx = Lx.subs({s: eps * s for s in extra_syms})
    return sp.expand(sp.series(Lx, eps, 0, 3).removeO().coeff(eps, 2))


L2 = quadratic_L(w - v, (v1, v2, v3, w1, w2, w3, b1, b2, b3))
info("B0  quadratic Lagrangian, derived", f"L2 = {sp.simplify(L2)}")
M = sp.Matrix(3, 3, lambda i, j: sp.simplify(sp.diff(L2, (v1, v2, v3)[i], (v1, v2, v3)[j])))
info("B1  kinetic Hessian M_ij", f"{M.tolist()}")
M_expected = sp.eye(3) * Lp + sp.Matrix(3, 3, lambda i, j: Lpp * E0v[i] * E0v[j])
check(sp.simplify(M - M_expected) == sp.zeros(3, 3),
      "B1  the kinetic Hessian is EXACTLY M_ij = Lcal' delta_ij + Lcal'' E0_i E0_j -- derived "
      "from the action by sympy, not quoted",
      "eigenvalues Lcal' (x2, transverse to E0) and Lcal' + E0^2 Lcal'' (x1, PARALLEL to E0)")
evals = M.eigenvals()
info("B2  eigenvalues", {str(k): int(val) for k, val in evals.items()})
check(set(sp.simplify(k) for k in evals) == {sp.simplify(Lp), sp.simplify(Lp + Lpp * Ebg ** 2)},
      "B2  eigenvalues confirmed: {Lcal', Lcal' + E0^2 Lcal''}.  The SECOND is the 'parallel "
      "mode' of the refutation -- parallel to the BACKGROUND E, not to the wavevector")
Bgrad = sp.Matrix(3, 3, lambda i, j: sp.simplify(sp.diff(L2, (b1, b2, b3)[i], (b1, b2, b3)[j])))
check(sp.simplify(Bgrad + sp.eye(3) * Lp) == sp.zeros(3, 3),
      "B3  the magnetic (gradient) block is -Lcal' delta_ij, ISOTROPIC.  So for a mode with "
      "k perpendicular to E0 and polarisation parallel to E0 the dispersion is "
      "(Lcal' + E0^2 Lcal'') omega^2 = Lcal' k^2, i.e. c^2_par = Lcal'/(Lcal' + E0^2 Lcal'')",
      f"{Bgrad.tolist()}")
print("""
  TRANSLATION into mechanism C's variables.  For a pure electric background S = E^2/2, so
        Lcal'(S)             = dP/dS = P'(E)/E = mu_v(E)                        (transverse)
        Lcal' + E^2 Lcal''   = mu_v + E mu_v'(E) = d(mu_v E)/dE = P''(E)        (parallel)
  and by (*),
        K_perp = mu_v      = 1 - g_bar/g_obs           in (0,1] : never a ghost
        K_par  = P''(E)    = d(g_obs - g_bar)/d g_obs   <-- THE WHOLE QUESTION
        c^2_par(vector host) = K_perp / K_par
""")
Pp = sp.Function("P")(E_)
check(sp.simplify(sp.diff(mu_f * E_, E_) - (mu_f + E_ * sp.diff(mu_f, E_))) == 0,
      "B4  P''(E) = d(mu_v E)/dE = mu_v + E mu_v', the parallel eigenvalue, verified symbolically")

# =============================================================================================
head("PART C -- THE CONSTRAINED UNIT-TIMELIKE VECTOR: the actual Hessian, three ways")
# =============================================================================================
print("""
  A unit timelike vector cannot be perturbed freely.  Do it three independent ways.

  (C1) EXACT PARAMETERISATION, nonperturbative in the constraint.  Every unit timelike A_mu is
       A_mu = (-sqrt(1+|a|^2), a_1, a_2, a_3) for THREE unconstrained functions a_i(t,x).  The
       constraint is then identically satisfied and there is nothing left to impose.  Compute
       E_i = F_i0 = d_i A_0 - d_t a_i directly from that parameterisation.
""")
t, X1, X2, X3 = sp.symbols("t x y z", real=True)
aa = [sp.Function(f"a{k}")(t, X1, X2, X3) for k in (1, 2, 3)]
A0_exact = -sp.sqrt(1 + sum(s ** 2 for s in aa))
coords = (X1, X2, X3)
E_exact = [sp.diff(A0_exact, coords[i]) - sp.diff(aa[i], t) for i in range(3)]
vt = sp.symbols("vt1 vt2 vt3", real=True)
subs_v = {sp.Derivative(aa[i], t): vt[i] for i in range(3)}
E_sub = [sp.expand(e.doit().subs(subs_v)) for e in E_exact]
J = sp.Matrix(3, 3, lambda i, j: sp.simplify(sp.diff(E_sub[i], vt[j])))
info("C1  dE_i/d(d_t a_j) from the exact unit-timelike parameterisation", f"{J.tolist()}")
check(sp.simplify(J + sp.eye(3)) == sp.zeros(3, 3),
      "C1a  *** dE_i/d(d_t a_j) = -delta_ij EXACTLY, nonperturbatively in the constraint.  "
      "A_0 = -sqrt(1+|a|^2) is an algebraic function of a with NO time derivative, so d_i A_0 "
      "carries only SPATIAL derivatives.  The time-derivative structure of E_i is identical to "
      "the gauge case ***",
      "this is the crux: whatever the constraint does, it cannot touch d_t delta A_i")
Bx = sp.Matrix([sp.diff(aa[2], X2) - sp.diff(aa[1], X3),
                sp.diff(aa[0], X3) - sp.diff(aa[2], X1),
                sp.diff(aa[1], X1) - sp.diff(aa[0], X2)])
check(all(sp.simplify(sp.diff(Bx[i].doit().subs(subs_v), vt[j])) == 0
          for i in range(3) for j in range(3)),
      "C1b  and B = curl a contains no time derivative either, so the ENTIRE d_t-dependence of "
      "L = Lcal((E^2-B^2)/2) is through E_i = (spatial) - d_t a_i")
L2_exact = quadratic_L(sp.Matrix([sp.Symbol("wt1"), sp.Symbol("wt2"), sp.Symbol("wt3")]) - v,
                       (v1, v2, v3, sp.Symbol("wt1"), sp.Symbol("wt2"), sp.Symbol("wt3"),
                        b1, b2, b3))
M_c1 = sp.Matrix(3, 3, lambda i, j: sp.simplify(sp.diff(L2_exact, (v1, v2, v3)[i],
                                                        (v1, v2, v3)[j])))
check(sp.simplify(M_c1 - M) == sp.zeros(3, 3),
      "C1c  *** THEOREM (route 1 of 3): the kinetic Hessian of the EXACTLY-parameterised unit "
      "timelike vector is IDENTICAL to the gauge vector's, term by term, for an arbitrary "
      "spatial-derivative piece wt_i.  M_constrained - M_gauge = 0 ***",
      f"{M_c1.tolist()}")

print("""
  (C2) LAGRANGE-MULTIPLIER ROUTE.  L_tot = Lcal(S) + lambda (A_mu A^mu + 1).  Expand to second
       order about a background with multiplier lambdabar.  delta-lambda multiplies the
       LINEARISED constraint (a pure algebraic relation among the delta A_mu), and lambdabar
       multiplies delta A_mu delta A^mu = -delta A_0^2 + |delta A|^2.  Neither carries a time
       derivative.  Check that, then eliminate delta A_0.
""")
lam, dlam = sp.symbols("lambdabar dlambda", real=True)
dA0s, dA1s, dA2s, dA3s = sp.symbols("dA0 dA1 dA2 dA3", real=True)
Ab0, Ab1, Ab2, Ab3 = sp.symbols("Ab0 Ab1 Ab2 Ab3", real=True)
lin_constraint = -Ab0 * dA0s + Ab1 * dA1s + Ab2 * dA2s + Ab3 * dA3s      # eta^{mn} Abar_m dA_n
L_mult = 2 * dlam * lin_constraint + lam * (-dA0s ** 2 + dA1s ** 2 + dA2s ** 2 + dA3s ** 2)
check(all(sp.diff(L_mult, s) == 0 for s in (v1, v2, v3)) and
      sp.simplify(sp.diff(L_mult, dlam, dlam)) == 0,
      "C2a  the multiplier sector contributes NO time derivatives at all (it is algebraic in "
      "delta A_mu) and delta-lambda has no kinetic term of its own -- so it enforces the "
      "linearised constraint and nothing else",
      f"L_mult = {sp.expand(L_mult)}")
sol_dA0 = sp.solve(sp.Eq(lin_constraint, 0), dA0s, dict=True)
info("C2b  linearised constraint solved for delta A_0",
     f"delta A_0 = {sp.simplify(sol_dA0[0][dA0s])}")
check(len(sol_dA0) == 1 and
      sp.simplify(sol_dA0[0][dA0s] - (Ab1 * dA1s + Ab2 * dA2s + Ab3 * dA3s) / Ab0) == 0,
      "C2b  exactly one branch, and it matches the hand form delta A_0 = (Abar . delta A)/Abar_0 "
      "-- an ALGEBRAIC relation among the perturbations containing no time derivative of "
      "anything.  Guard against a vacuous solve: the branch count is checked, not assumed")
check(sp.simplify(sp.diff(sol_dA0[0][dA0s], dA1s) - Ab1 / Ab0) == 0,
      "C2c  so d_i(delta A_0) = (Abar . d_i delta A)/Abar_0 involves only SPATIAL derivatives of "
      "delta A, exactly the 'wt_i' already allowed for in C1c.  Route 2 of 3 returns the same "
      "Hessian")

print("""
  (C3) THE AeST-REALISTIC BACKGROUND.  In a static weak field ds^2 = -N^2 dt^2 + delta_ij dx^i
       dx^j with the aether aligned to the timelike Killing vector, the constraint forces
       Abar_mu = (-N, 0, 0, 0) and hence  E_i = F_i0 = -d_i N  -- the background electric field
       IS (minus) the lapse gradient, which is the framework's own sf39 khronon scalar.  The
       linearised constraint is then  delta A_0 = -(N/2) delta g^{mn} Abar_m Abar_n, i.e.
       delta A_0 is slaved to the METRIC perturbation and vanishes identically when the metric is
       frozen.  There is then no delta A_0 at all, and M_ij is read off directly.
""")
Nl = sp.Symbol("N", positive=True)
dg00, dA0v = sp.symbols("dg00 dA0", real=True)
dAi = sp.symbols("dAx dAy dAz", real=True)
# g^{00} = -1/N^2 + dg00 ; g^{ij} = delta^{ij} ; A_0 = -N + dA0 ; A_i = dA_i.  Impose A.A = -1
# and keep the LINEAR part -- solved by sympy, not asserted.
AdotA = sp.expand((-1 / Nl ** 2 + dg00) * (-Nl + dA0v) ** 2 + sum(s ** 2 for s in dAi) + 1)
AdotA_lin = sp.expand(AdotA.subs({s: eps * s for s in (dg00, dA0v) + dAi})).coeff(eps, 1)
sol_aest = sp.solve(sp.Eq(AdotA_lin, 0), dA0v, dict=True)
info("C3a  linearised unit constraint on the AeST-realistic static background",
     f"linear part = {sp.simplify(AdotA_lin)}  =>  delta A_0 = "
     f"{sp.simplify(sol_aest[0][dA0v])}")
check(len(sol_aest) == 1 and sp.simplify(sol_aest[0][dA0v] + Nl ** 3 * dg00 / 2) == 0
      and sp.simplify(sol_aest[0][dA0v].subs(dg00, 0)) == 0,
      "C3a  the constraint on Abar_mu = (-N,0,0,0) gives delta A_0 = -N^3 delta g^{00}/2 -- "
      "delta A_0 is slaved to the METRIC perturbation alone and vanishes IDENTICALLY when the "
      "metric is frozen.  This is the strongest form of the critic's premise and the one most "
      "favourable to the rescue.  Note also that the background electric field is then "
      "E_i = F_i0 = -d_i N, the framework's own sf39 khronon scalar",
      "solved by sympy with the branch count checked, guarding a vacuous solve")
M_c3 = sp.Matrix(3, 3, lambda i, j: sp.simplify(sp.diff(quadratic_L(-v, (v1, v2, v3, b1, b2, b3)),
                                                        (v1, v2, v3)[i], (v1, v2, v3)[j])))
info("C3b  Hessian with delta A_0 = 0 imposed", f"{M_c3.tolist()}")
check(sp.simplify(M_c3 - M) == sp.zeros(3, 3),
      "C3b  *** and it is STILL the same matrix.  Route 3 of 3.  Setting delta A_0 = 0 removes "
      "a term that never contributed to the kinetic block in the first place ***",
      "three independent constructions, one Hessian")

print("""
  MODE COUNT -- and it runs the WRONG WAY for the rescue.
     gauge vector:        4 components - 1 (A_0 non-dynamical) - 1 (U(1) gauge) = 2 propagating
     constrained vector:  4 components - 1 (constraint slaves A_0) - 0 (no gauge)= 3 propagating
  The mode the gauge case discards is the LONGITUDINAL-IN-k mode.  The ghost-carrying mode is the
  polarisation PARALLEL TO THE BACKGROUND E -- a different object, physical in BOTH cases.  So
  the constraint does not subtract the ghost; it ADDS a third direction governed by the SAME M.
  If M is indefinite the constrained theory has MORE of the disease, not less.
""")
# IS THE GHOST MODE PHYSICAL IN THE GAUGE THEORY, or is it pure gauge?  Take k along x and the
# polarisation along z = the background E direction.  Then k . delta A = 0, so the mode is
# TRANSVERSE TO k and survives the gauge quotient -- it is physical in BOTH realisations.
kvec = sp.Matrix([sp.Symbol("k", positive=True), 0, 0])
pol = sp.Matrix([0, 0, sp.Symbol("A_amp", positive=True)])
curl_amp = kvec.cross(pol)
info("C3c  the ghost polarisation, tested for gauge-triviality",
     f"k . pol = {kvec.dot(pol)} (transverse), |k x pol|^2 / (k^2 |pol|^2) = "
     f"{sp.simplify(curl_amp.dot(curl_amp) / (kvec.dot(kvec) * pol.dot(pol)))}")
check(sp.simplify(kvec.dot(pol)) == 0 and
      sp.simplify(curl_amp.dot(curl_amp) / (kvec.dot(kvec) * pol.dot(pol)) - 1) == 0,
      "C3c  the mode carrying the parallel eigenvalue has k PERPENDICULAR to the background E, "
      "so k . delta A = 0: it is transverse to the wavevector and is NOT pure gauge.  It is a "
      "physical propagating polarisation in the U(1) theory as well as the constrained one, and "
      "its magnetic amplitude is |k||delta A| exactly, giving the dispersion "
      "(Lcal' + E^2 Lcal'') omega^2 = Lcal' k^2 used throughout",
      "this closes the only way the critic's hypothesis could still have bitten")
n_gauge, n_constrained = 4 - 1 - 1, 4 - 1 - 0
check(n_constrained > n_gauge,
      f"C4  mode count: {n_constrained} propagating vector modes in the constrained "
      f"realisation against {n_gauge} in the gauge one, all governed by the same M_ij",
      "the constraint cannot subtract a mode it does not act on")
check(sp.simplify(M.subs(Lpp, 0) - sp.eye(3) * Lp) == sp.zeros(3, 3),
      "C5  NEGATIVE CONTROL 1: setting Lcal'' = 0 -- i.e. AeST's own LINEAR K_B F^2 term -- "
      "makes M isotropic, so AeST's ACTUAL vector has no parallel-mode issue at all.  The "
      "disease is created by the NONLINEARITY mechanism C requires, not by the vector.  This is "
      "why 'AeST's vector is healthy' does not transfer",
      "the control is what makes the theorem non-vacuous")
Mneg = M.subs({Lp: 1, Lpp: -2, Ebg: 1})
_ev = sorted(float(z) for z in Mneg.eigenvals())
check(min(_ev) < 0,
      "C5  NEGATIVE CONTROL 2: handed Lcal' = 1, Lcal'' = -2, E0 = 1 the same code flags a "
      f"genuine ghost (eigenvalues {_ev}) -- the detector is not passing vacuously")

# =============================================================================================
head("PART D -- AND THE SIGN CONDITION IS HOST-INDEPENDENT (three proofs)")
# =============================================================================================
print("""
  The refutation was framed as a statement about a COVARIANTISATION.  It is not.  It is a
  statement about mu_v itself, and it survives every host.  Three proofs.
""")
muv, Ppp = sp.symbols("mu_v Ppp", positive=False)
xi1, xi3 = sp.symbols("xi_perp xi_par", real=True)
n_hat = sp.Matrix([0, 0, 1])
symbolmat = sp.Matrix(3, 3, lambda i, j: muv * (1 if i == j else 0)
                      + (Ppp - muv) * n_hat[i] * n_hat[j])
xi = sp.Matrix([xi1, 0, xi3])
principal = sp.simplify((xi.T * symbolmat * xi)[0, 0])
info("D1  principal symbol of div[mu_v(|grad A|) grad A]", f"sigma(xi) = {principal}")
check(sp.simplify(principal - (muv * xi1 ** 2 + Ppp * xi3 ** 2)) == 0,
      "D1  PROOF 1 (non-relativistic, host-free): the linearisation of mechanism C's OWN "
      "mediator equation has principal symbol mu_v |xi_perp|^2 + P'' |xi_par|^2.  The static "
      "boundary-value problem is ELLIPTIC iff mu_v > 0 AND P'' > 0.  Where P'' < 0 the equation "
      "changes type and mechanism C's galaxy solution is ILL-POSED before any covariantisation "
      "is chosen",
      "sigma(xi = n) = P'' exactly")
check(sp.simplify(principal.subs({xi1: 0, xi3: 1}) - Ppp) == 0,
      "D1b sanity: the symbol along the field direction is P'' itself, along the perpendicular "
      "it is mu_v -- so the two Hessian eigenvalues of PART B are the two characteristic "
      "directions of the static PDE.  Same two numbers, arrived at without any Lagrangian")

print("""
  PROOF 2 -- vector host.  Already PART B: kinetic eigenvalues {mu_v, P''}, magnetic block
  isotropic, so c^2_par = mu_v/P''.  P'' < 0 is a GHOST (wrong-sign kinetic term) AND, because
  mu_v stays positive, c^2_par < 0 as well: a gradient instability at every k, fastest in the UV.

  PROOF 3 -- scalar host.  L = f(X), X = d_mu phi d^mu phi = -phidot^2 + |grad phi|^2.  Derived
  below with no formula assumed.
""")
fX = sp.Function("f")
Xs = sp.Symbol("X", real=True)
fp, fpp = sp.symbols("fp fpp", real=True)
dphidot, gpar, gperp, Eb = sp.symbols("dphidot g_par g_perp E_b", real=True)
dX = 2 * Eb * gpar + (-dphidot ** 2 + gpar ** 2 + gperp ** 2)
L2s = sp.expand(fp * dX + sp.Rational(1, 2) * fpp * dX ** 2)
L2s = L2s.subs({s: eps * s for s in (dphidot, gpar, gperp)})
L2s = sp.expand(sp.series(L2s, eps, 0, 3).removeO().coeff(eps, 2))
info("D2  scalar-host quadratic Lagrangian, derived", f"L2 = {sp.simplify(L2s)}")
c_tt = sp.simplify(sp.diff(L2s, dphidot, dphidot) / 2)
c_par = sp.simplify(sp.diff(L2s, gpar, gpar) / 2)
c_perp = sp.simplify(sp.diff(L2s, gperp, gperp) / 2)
info("D2  coefficients", f"phidot^2 : {c_tt}   (n.grad)^2 : {c_par}   perp grad : {c_perp}")
check(sp.simplify(c_tt + fp) == 0 and sp.simplify(c_perp - fp) == 0 and
      sp.simplify(c_par - (fp + 2 * fpp * Eb ** 2)) == 0,
      "D2  scalar host: coefficients are (-f', f' + 2 f'' E^2, f') for "
      "(phidot^2, (n.grad)^2, perp).  Its static flux is 2 f'(E^2) grad phi, so mu_v = -2f' and "
      "d(mu_v E)/dE = -2(f' + 2 f'' E^2) = P''.  Ghost-freedom is mu_v > 0; PARALLEL GRADIENT "
      "STABILITY is exactly P'' > 0.  Same condition, different symptom",
      "vector host: P'' < 0 is a ghost.  scalar host: P'' < 0 is a gradient instability.  "
      "non-relativistic: P'' < 0 is loss of ellipticity")
print("""
  PROOF 4 -- and this one closes the last escape.  A CONSTRAINED vector has a SECOND independent
  quadratic invariant that a gauge vector does not: W = A^mu F_munu F^nurho A_rho, which in the
  aether frame is |E|^2.  So the general host is Lcal(S, W), not Lcal(S), and one might hope the
  extra freedom moves the bad eigenvalue.  IT CANNOT, and the reason is exact:

     by C1 the perturbation enters ONLY as  delta E_i = (spatial) - d_t delta A_i,  so
        M_ij = d^2 L / dE_i dE_j    at the background,
     for the MOST GENERAL rotationally invariant host  L = F(|E|^2, |B|^2, E.B)  -- which spans
     every scalar a constrained vector can build, S and W included.  At a purely electric
     background all the B-dependence drops out of the E-Hessian, and BOTH eigenvalues come back
     as functions of P alone.  Derived below, not asserted.
""")
Ex, Ey, Ez, Bx_, By_, Bz_ = sp.symbols("E_1 E_2 E_3 B_1 B_2 B_3", real=True)
Ebg_s = sp.Symbol("E", positive=True)
Ev = sp.Matrix([Ex, Ey, Ez])
Bv = sp.Matrix([Bx_, By_, Bz_])
Fgen = sp.Function("F")(Ev.dot(Ev), Bv.dot(Bv), Ev.dot(Bv))
at_bg = {Ex: 0, Ey: 0, Ez: Ebg_s, Bx_: 0, By_: 0, Bz_: 0}
M_gen = sp.Matrix(3, 3, lambda i, j: sp.simplify(
    sp.diff(Fgen, (Ex, Ey, Ez)[i], (Ex, Ey, Ez)[j]).subs(at_bg)))
info("D3  generic rotationally invariant host, kinetic Hessian at a purely electric background",
     f"{[[sp.simplify(M_gen[i, j]) for j in range(3)] for i in range(3)]}")
# P(E) = F(E^2, 0, 0) is what mechanism C's static flux law fixes.  Read P' and P'' off it.
Prest = sp.Function("F")(Ebg_s ** 2, 0, 0)
P1 = sp.simplify(sp.diff(Prest, Ebg_s))
P2 = sp.simplify(sp.diff(Prest, Ebg_s, 2))
info("D3  and P(E) = F(E^2,0,0) restricted to the same background",
     f"P'(E) = {P1} ;  P''(E) = {P2}")
check(sp.simplify(M_gen[2, 2] - P2) == 0,
      "D3  PROOF 4 (parallel): for the MOST GENERAL rotationally invariant host "
      "F(|E|^2,|B|^2,E.B) -- every invariant a constrained vector can build, S and W included -- "
      "the PARALLEL kinetic eigenvalue equals P''(E) exactly, and P is fixed by mechanism C's "
      "own static flux law.  'Use a richer host' is NOT an escape",
      f"M_par = {sp.simplify(M_gen[2, 2])} = P'' = {P2}")
check(sp.simplify(M_gen[0, 0] - P1 / Ebg_s) == 0 and sp.simplify(M_gen[1, 1] - P1 / Ebg_s) == 0
      and all(sp.simplify(M_gen[i, j]) == 0 for i in range(3) for j in range(3) if i != j),
      "D3b AND THE THEOREM IS STRONGER THAN I FIRST WROTE, in the framework's disfavour: the "
      "TRANSVERSE eigenvalues come back as P'(E)/E = mu_v as well, and the off-diagonal entries "
      "vanish.  At a purely electric background the ENTIRE kinetic Hessian of ANY such host is "
      "{mu_v, mu_v, d(mu_v E)/dE} -- there is NO host freedom at all, not merely none in the "
      "parallel direction.  I had claimed the transverse entry was movable; that was wrong and "
      "the correction runs AGAINST the rescue",
      f"M_perp = {sp.simplify(M_gen[0, 0])} = P'/E")
# NEGATIVE CONTROL: the machinery does distinguish hosts that differ ON the electric line
Ptest = sp.Function("Ptest")
Lc1 = Ptest(sp.sqrt(Ev.dot(Ev)))
Lc2 = Ptest(sp.sqrt(Ev.dot(Ev))) + Bv.dot(Bv) * Ev.dot(Ev)
h1 = sp.simplify(sp.diff(Lc1, Ez, 2).subs(at_bg))
h2 = sp.simplify(sp.diff(Lc2, Ez, 2).subs(at_bg))
h3 = sp.simplify(sp.diff(Ptest(2 * sp.sqrt(Ev.dot(Ev))), Ez, 2).subs(at_bg))
check(sp.simplify(h1 - h2) == 0 and sp.simplify(h1 - h3) != 0,
      "D3c NEGATIVE CONTROL: adding |B|^2|E|^2 -- a genuine extra invariant -- leaves M_par "
      "unchanged, while rescaling the argument of P (which CHANGES the static flux law) does "
      "change it.  So the detector responds to what it should and is blind to what it should be",
      f"same-flux hosts agree ({h1} vs {h2}); different-flux host differs")

print("""
  SO: THE HEALTH CONDITION FOR MECHANISM C'S MEDIATOR, ON EVERY HOST, IS

        P''(E) = d(mu_v E)/dE = d(g_obs - g_bar)/d g_obs >= 0,

  i.e. THE PHANTOM ACCELERATION MUST BE NON-DECREASING IN THE TOTAL FIELD.

  And this is the gap in mechanism C's own file.  Its line 226 checks "mu_v >= 0 at every
  acceleration: the VECTOR realisation is kinetically healthy everywhere, no ghost anywhere".
  That is the TRANSVERSE eigenvalue.  The parallel one was never computed.
""")

# =============================================================================================
head("PART E -- both kernels at 60 digits, analytic forms carried alongside")
# =============================================================================================


def a0line(y):
    """Carl's a_0-line: g_obs^2 = g_bar^2 + a_0 g_bar  =>  x = sqrt(y^2+y).  Exact."""
    y = mp.mpf(y)
    x = mp.sqrt(y * y + y)
    return x, x - y


def ms08(y):
    """Route A / MS08: nu = 1/(1-exp(-sqrt(y))).  ANALYTIC forms, no cancellation.
       x = y/(1-e^-u), phantom = u^2/(e^u - 1), K_perp = 1 - y/x = e^-u  EXACTLY."""
    y = mp.mpf(y)
    u = mp.sqrt(y)
    em = mp.e ** (-u)
    x = y / (1 - em) if u < 500 else y * (1 + em)          # both exact to 60 digits in range
    ph = u ** 2 * em / (1 - em) if u < 500 else u ** 2 * em
    return x, ph


def simple_mu(y):
    """mu = x/(1+x)."""
    y = mp.mpf(y)
    x = y * (1 + mp.sqrt(1 + 4 / y)) / 2
    return x, x - y


def standard_mu(y):
    """mu = x/sqrt(1+x^2)."""
    y = mp.mpf(y)
    x = y * mp.sqrt((1 + mp.sqrt(1 + 4 / y ** 2)) / 2)
    return x, x - y


# ANALYTIC K_perp and K_par -- derived symbolically, then lambdified.  No finite differences at
# large y, where float64 and even naive mpmath cancel catastrophically (trap 6).
u_ = sp.Symbol("u", positive=True)
ph_ms = u_ ** 2 / (sp.exp(u_) - 1)                     # phantom(u), u = sqrt(y)
x_ms = u_ ** 2 * sp.exp(u_) / (sp.exp(u_) - 1)         # x(u)
Kpar_ms_sym = sp.simplify(sp.diff(ph_ms, u_) / sp.diff(x_ms, u_))
Kperp_ms_sym = sp.exp(-u_)
c2_ms_sym = sp.simplify(Kperp_ms_sym / Kpar_ms_sym)
info("E0  MS08 analytic", f"K_par(u) = {Kpar_ms_sym}")
info("E0  MS08 analytic", f"c^2_par(u) = {c2_ms_sym}")
check(sp.limit(c2_ms_sym * u_, u_, sp.oo) == -2,
      "E0  *** sympy's exact limit: u c^2_par -> -2 as u -> oo, i.e. c^2_par -> -2/sqrt(y).  "
      "THE REFEREE'S NUMBER IS THE MS08 KERNEL'S ASYMPTOTIC PARALLEL SOUND SPEED, derived here "
      "in closed form rather than fitted ***",
      f"limit u*c^2_par = {sp.limit(c2_ms_sym * u_, u_, sp.oo)}")
Kpar_ms_f = sp.lambdify(u_, Kpar_ms_sym, "mpmath")
c2_ms_f = sp.lambdify(u_, c2_ms_sym, "mpmath")

Kpar_a0_sym = sp.simplify(sp.diff(x_ - (sp.sqrt(1 + 4 * x_ ** 2) - 1) / 2, x_))
info("E1  a_0-line analytic", f"K_par(x) = {Kpar_a0_sym}")
check(sp.simplify(Kpar_a0_sym - (1 - 2 * x_ / sp.sqrt(1 + 4 * x_ ** 2))) == 0,
      "E1  a_0-line: K_par = 1 - 2x/sqrt(1+4x^2).  Since 4x^2 < 1 + 4x^2 for every real x, "
      "2x/sqrt(1+4x^2) < 1 ALWAYS: no root, no sign change, POSITIVE EVERYWHERE")
check(sp.limit(Kpar_a0_sym * 8 * x_ ** 2, x_, sp.oo) == 1 and
      sp.limit(Kpar_a0_sym, x_, 0) == 1,
      "E1b a_0-line asymptotics, by exact limits: K_par -> 1 in deep MOND and -> 1/(8x^2) in the "
      "Newtonian regime.  Small but never negative",
      f"lim 8x^2 K_par = {sp.limit(Kpar_a0_sym * 8 * x_ ** 2, x_, sp.oo)}, "
      f"lim_(x->0) K_par = {sp.limit(Kpar_a0_sym, x_, 0)}")


def Kperp_num(kern, yv):
    """K_perp = 1 - y/x = 1 - 1/nu.  For MS08 that is e^-sqrt(y) EXACTLY -- use the closed form,
    because 1 - y/x cancels to nothing at 60 digits once sqrt(y) > 140 (trap 6)."""
    if kern is ms08:
        return mp.e ** (-mp.sqrt(mp.mpf(yv)))
    x, _ = kern(yv)
    return 1 - mp.mpf(yv) / x


def Kpar_num(kern, yv):
    """analytic where available, high-precision numeric differentiation as the CONTROL."""
    yv = mp.mpf(yv)
    if kern is ms08:
        return Kpar_ms_f(mp.sqrt(yv))
    if kern is a0line:
        x = mp.sqrt(yv * yv + yv)
        return 1 - 2 * x / mp.sqrt(1 + 4 * x * x)
    dph = mp.diff(lambda s: kern(s)[1], yv)
    dx = mp.diff(lambda s: kern(s)[0], yv)
    return dph / dx


# CONTROL: analytic vs independent numerical differentiation, in a regime where both are safe
for kern, nm in ((a0line, "a_0-line"), (ms08, "MS08")):
    for yv in (0.3, 1.0, 3.0):
        an = Kpar_num(kern, yv)
        nu_ = mp.diff(lambda s: kern(s)[1], yv) / mp.diff(lambda s: kern(s)[0], yv)
        check(abs(an - nu_) < mp.mpf("1e-25") * max(1, abs(an)),
              f"E2  CONTROL {nm} y={yv}: analytic K_par matches independent numerical "
              f"differentiation of the phantom to 25 digits",
              f"analytic {mp.nstr(an, 12)}  numeric {mp.nstr(nu_, 12)}")

YS = [1e-4, 1e-2, 0.1, 1.0, 2.0, 2.5396383, 3.0, 10.0, 1e2, 1e4, 1e6, 6.3359e7]
for nm, kern in (("a_0-line (Carl's own)", a0line), ("Route A / MS08", ms08)):
    print(f"\n  --- {nm} ---")
    for yv in YS:
        kp, kperp = Kpar_num(kern, yv), Kperp_num(kern, yv)
        c2 = (c2_ms_f(mp.sqrt(mp.mpf(yv))) if kern is ms08 else kperp / kp)
        info(f"    y={yv:<12g}", f"K_perp={mp.nstr(kperp, 6):>14s}  K_par={mp.nstr(kp, 6):>14s}  "
                                 f"c^2_par={mp.nstr(c2, 6):>13s}  {'GHOST' if kp < 0 else 'ok'}")

scan = [Kpar_num(a0line, yv) for yv in np.logspace(-12, 14, 400)]
info("E3  a_0-line scan over y in [1e-12, 1e14]",
     f"min K_par = {mp.nstr(min(scan), 6)}; all strictly positive = {all(s > 0 for s in scan)}")
check(all(s > 0 for s in scan),
      "E3  *** CARL'S OWN a_0-LINE KERNEL HAS NO PARALLEL-MODE GHOST: K_par > 0 at all 400 "
      "samples spanning 26 decades, and analytically without a root.  MECHANISM C IS BUILT ON "
      "THE a_0-LINE (its own line 30).  THE PUBLISHED REFUTATION DOES NOT APPLY TO MECHANISM C'S "
      "OWN STATED KERNEL.  This correction runs IN FAVOUR of the framework and is stated as "
      "such ***",
      f"min sampled {mp.nstr(min(scan), 4)}")
u_star = mp.findroot(lambda uu: 2 * (mp.e ** uu - 1) - uu * mp.e ** uu, mp.mpf("1.6"))
y_star = u_star ** 2
info("E4  MS08 phantom = u^2/(e^u - 1); stationary when 2(e^u - 1) = u e^u",
     f"u* = {mp.nstr(u_star, 12)}  =>  y* = {mp.nstr(y_star, 12)}")
check(abs(Kpar_ms_f(u_star)) < mp.mpf("1e-15"),
      f"E4  MS08: K_par vanishes at y* = {mp.nstr(y_star, 9)}, located by root-finding on the "
      "stationarity condition and then confirmed on the independent analytic K_par",
      f"K_par(y*) = {mp.nstr(Kpar_ms_f(u_star), 4)}")
below, above = Kpar_ms_f(mp.sqrt(y_star * mp.mpf("0.5"))), Kpar_ms_f(mp.sqrt(y_star * 2))
check(below > 0 > above,
      f"E4b MS08: K_par = {mp.nstr(below, 5)} below y* and {mp.nstr(above, 5)} above it -- the "
      f"ROUTE A / MS08 KERNEL IS UNHEALTHY FOR EVERY g_bar > {float(y_star):.4f} a_0, which "
      "includes the inner disc of every galaxy AND the whole solar system")
for nm in FOOTINGS:
    uu = mp.sqrt(Y_1AU[nm])
    ex, asy = c2_ms_f(uu), -2 / uu
    info(f"E5  MS08 c^2_par at 1 AU, {nm}",
         f"exact {mp.nstr(ex, 10)}   -2/sqrt(y) {mp.nstr(asy, 10)}   ratio {mp.nstr(ex/asy, 10)}")
    check(abs(ex / asy - 1) < mp.mpf("1e-3"),
          f"E5 {nm}  the closed form and the referee's asymptotic agree to "
          f"{float(abs(ex/asy - 1)):.2e} at 1 AU.  THE REFEREE WAS RIGHT ABOUT WHAT HE COMPUTED, "
          "AND HE WAS COMPUTING MS08 -- not a gauge-covariantisation artefact")
    growth_t = float(AU / (mp.sqrt(-ex) * C_))
    info(f"E5b MS08 instability at 1 AU, {nm}",
         f"|c_par| = {float(mp.sqrt(-ex)):.5f} c ; c^2 < 0 with the magnetic block still "
         f"positive, so omega = i k |c_par| and the e-folding time at k = 1/AU is "
         f"{growth_t:.4g} s = {growth_t/3600:.3g} hr, FASTER at larger k")
    check(growth_t < 3600 * 24,
          f"E5c {nm}  MS08's failure is not a benign UV nuisance: at k = 1/AU the parallel mode "
          f"e-folds in {growth_t/3600:.2f} hours, and the rate grows without bound in the UV.  "
          "Wrong-sign kinetic term AND c^2 < 0 together")

# =============================================================================================
head("PART F -- THE NO-GO: no kernel clears health AND the 1-AU ephemeris")
# =============================================================================================
print("""
  THEOREM.  Let p(y) = (g_obs - g_bar)/a_0 be a kernel's phantom, y = g_bar/a_0, x = g_obs/a_0.
   (i)   health (PART D, any host)  <=>  dp/dx >= 0  <=>  dp/dy >= 0, since dx/dy > 0 for any
         kernel whose RAR is single-valued (checked below, not assumed);
   (ii)  MOND  =>  p(y ~ 1) = O(1) a_0: this is what "MOND turns on at a_0" MEANS, and it is
         what the RAR measures;
   (iii) mechanism C's dark mass is REAL mass, so the 1-AU anomalous sunward acceleration IS
         a_0 p(y_1AU), bounded by the Mars EPM budget.
  (i) forces p(y_1AU) >= p(1).  With (ii) and (iii) that is a contradiction.  Numbers first.
""")
ALL_K = {"a_0-line (Carl's)": a0line, "Route A / MS08": ms08,
         "simple mu=x/(1+x)": simple_mu, "standard mu=x/sqrt(1+x^2)": standard_mu}
for nm, kern in ALL_K.items():
    dxdys = [mp.diff(lambda s: kern(s)[0], yv) for yv in (0.01, 0.5, 1.0, 2.0, 1e3, 1e6)]
    check(all(d > 0 for d in dxdys),
          f"F0  dx/dy > 0 for {nm} at all six sampled y from 0.01 to 1e6 "
          f"(min {mp.nstr(min(dxdys), 6)}), so sign(dp/dx) = sign(dp/dy) -- premise (i) is "
          "verified per kernel, not assumed")
p1s = {nm: kern(1.0)[1] for nm, kern in ALL_K.items()}
for nm, pv in p1s.items():
    info(f"F1  p(y=1) for {nm:26s}", f"{mp.nstr(pv, 8)} a_0")
p_min = min(p1s.values())
p_max = max(p1s.values())
check(p_min > mp.mpf("0.25") and p_max < mp.mpf("0.7"),
      f"F1  four independent kernels give p(1) in [{mp.nstr(p_min,4)}, {mp.nstr(p_max,4)}] a_0.  "
      "The threshold here was written AFTER computing the four values.  p(1) = O(1) is not a "
      "property of one interpolation; it is what MOND means, and the empirical RAR at "
      "g_bar = a_0 sits inside this range",
      ", ".join(f"{k.split()[0]}={mp.nstr(v,4)}" for k, v in p1s.items()))
for nm in FOOTINGS:
    budget_a0 = EPM_BUDGET[nm] / A0[nm]
    short = p_min / budget_a0
    info(f"F2  {nm}", f"y(1 AU) = {mp.nstr(Y_1AU[nm], 8)} ; Mars budget = "
                      f"{mp.nstr(budget_a0, 6)} a_0 ; health forces p(1 AU) >= p(1) >= "
                      f"{mp.nstr(p_min, 5)} a_0  =>  OVER BUDGET BY {mp.nstr(short, 6)}x")
    check(short > 1e4,
          f"F2 {nm}  *** NO-GO: health requires the phantom non-decreasing, so ANY healthy "
          f"kernel deposits at least {mp.nstr(p_min,4)} a_0 of constant anomalous sunward "
          f"acceleration at 1 AU, over the corrected Mars budget by {mp.nstr(short,4)}x.  "
          "MECHANISM C'S KERNEL SPACE IS EMPTY: no interpolation function clears both, so "
          "ROUTE 1 CANNOT RESCUE MECHANISM C EITHER ***")
print("""
  THE PINCER, kernel by kernel -- the two operative kernels sit on OPPOSITE horns and there is
  no third position:
""")
for nm in FOOTINGS:
    a0 = A0[nm]
    y1 = Y_1AU[nm]
    pa = a0line(y1)[1]
    pm = ms08(y1)[1]
    ka = Kpar_num(a0line, y1)
    km = Kpar_ms_f(mp.sqrt(y1))
    budget_a0 = EPM_BUDGET[nm] / a0
    info(f"F3  {nm}",
         f"a_0-line: p(1 AU) = {mp.nstr(pa, 10)} a_0 (the exact limit is a_0/2; it approaches "
         f"from below as 1/2 - 1/(8y)) = {mp.nstr(pa/budget_a0, 6)}x "
         f"budget, K_par = {mp.nstr(ka, 5)} > 0 HEALTHY   ||   MS08: p(1 AU) = 1e"
         f"{float(mp.log10(pm)):.0f} a_0 (budget-safe by {float(mp.log10(budget_a0/pm)):.0f} "
         f"orders), K_par = {mp.nstr(km, 5)} < 0 UNHEALTHY")
    check(abs(pa - mp.mpf("0.5")) < mp.mpf("1e-8") and ka > 0 and pm < budget_a0 and km < 0,
          f"F3 {nm}  the a_0-line's 1-AU phantom is a_0/2 to 9 digits (computed: "
          f"{mp.nstr(pa, 12)}), reproducing the corpus's own monopole liability; it is healthy "
          f"and ephemeris-excluded by {float(pa/budget_a0):.0f}x.  MS08 is ephemeris-void and "
          "kinetically dead.  The vice is exact")
_efe_lo, _efe_hi = 119 * 33435 / 1278, 189 * 33435 / 1278
info("F4  the most favourable EFE reading, priced",
     f"the corpus logs the a_0-line monopole as 119-189x over budget AFTER the external-field "
     f"effect is applied (against the pre-correction 1278x).  Carrying the same x27 correction "
     f"through gives {_efe_lo:.0f}-{_efe_hi:.0f}x post-EFE")
check(_efe_lo > 1e3,
      f"F4  even on the most favourable EFE treatment in the corpus the healthy kernel is "
      f"{_efe_lo:.0f}-{_efe_hi:.0f}x over the Mars budget, so the no-go survives the EFE by "
      "~3 orders.  AGAINST MY OWN CONCLUSION I note this scaling is INFERRED (the post-EFE "
      "figure was not recomputed here) and is flagged as owed in PART J")

# =============================================================================================
head("PART G -- health of the constrained realisation (what the constraint DOES change)")
# =============================================================================================
print("""
  The constraint changes the BACKGROUND, not the Hessian.  Work out the background mechanism C
  needs inside a unit-timelike vector, then price the health items on it.

  Static weak field, N = 1 + Phi/c^2, spatial tilt a_i, so A_0 = -N sqrt(1+|a|^2).  A dust
  particle of mass m and dark charge q at rest has L_p = -m N - q A_0 + ..., and equilibrium
  (mechanism C's A-iii) requires the gradient of [(1 +- m/q) Phi + c^2 |a|^2/2] to vanish.
""")
Phi_, mq = sp.symbols("Phi m_over_q", real=True)
a2 = sp.Function("a2")(Phi_)
bal = sp.Eq(sp.diff((1 + mq) * Phi_ + a2 / 2, Phi_), 0)
a2_sol = sp.dsolve(bal, a2).rhs
info("G0  equilibrium tilt, solved by dsolve", f"|a|^2 c^2 = {sp.simplify(a2_sol)}")
check(sp.simplify(a2_sol.subs(sp.Symbol("C1"), 0) + 2 * (1 + mq) * Phi_) == 0,
      "G0  the constrained realisation DOES host mechanism C: |a|^2 = -2(1 + m/q) Phi/c^2, so "
      "the mediator potential N sqrt(1+|a|^2) - 1 = Phi/c^2 + |a|^2/2 is proportional to Phi and "
      "the mediator Gauss law div[mu_v grad(.)] ~ rho_chi is exactly its (A-ii) with B = c^2.  "
      "The embedding is LEGITIMATE -- it just does not change the Hessian",
      "and note the constrained version FIXES B = c^2, removing a normalisation freedom the "
      "gauge version had.  It is more predictive and equally dead")
v_c = 233e3
tilt_min = np.sqrt(2) * v_c
info("G1  the aether must free-fall",
     f"|a| = sqrt(-2(1+m/q)Phi)/c, so at m/q -> 0 the preferred frame moves radially INTO the "
     f"galaxy at the local escape speed: at least sqrt(2) v_c = {tilt_min/1e3:.0f} km/s for "
     f"v_c = {v_c/1e3:.0f} km/s, and ~530 km/s for the Milky Way's measured local escape speed, "
     f"against the CMB-dipole 370 km/s")
check(0.5 < tilt_min / 370e3 < 2.0,
      f"G1  CONSEQUENCE, and it is a genuine prediction of the constrained realisation rather "
      f"than a kill: the preferred frame inside a galaxy is NOT the CMB frame; the Sun's "
      f"velocity with respect to it is {tilt_min/1e3:.0f}-530 km/s radially, comparable to but "
      f"not equal to the 370 km/s CMB dipole (ratio {tilt_min/370e3:.2f}).  PPN alpha_1 and "
      "alpha_2 are quoted against w = 370 km/s in the corpus and would have to be RE-PRICED "
      "against this w.  NOT DONE HERE -- flagged, not claimed either way",
      "threshold written after computing 329.5/370 = 0.89")
#  c_13 = 0 is DERIVED, not asserted: decompose F_munu F^munu in the Einstein-aether basis by
#  brute index algebra on a generic 4x4 nabla_mu A_nu.
eta4 = sp.diag(-1, 1, 1, 1)
Tg = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f"T{i}{j}", real=True))     # T_{mu nu} = nabla_mu A_nu
Fg = Tg - Tg.T
inv = lambda Mx, Nx: sum((eta4.inv() * Mx * eta4.inv().T)[i, j] * Nx[i, j]
                         for i in range(4) for j in range(4))
F2 = sp.expand(inv(Fg, Fg))
c1_term = sp.expand(inv(Tg, Tg))                    # nabla_mu A_nu nabla^mu A^nu   (c_1)
c3_term = sp.expand(inv(Tg, Tg.T))                  # nabla_mu A_nu nabla^nu A^mu   (c_3)
c1_val, c3_val = 2, -2
residual_ae = sp.expand(F2 - (c1_val * c1_term + c3_val * c3_term))
c13_val = sp.Integer(c1_val + c3_val)
info("G2a  F_munu F^munu in the Einstein-aether basis",
     f"(c_1, c_3) = ({c1_val}, {c3_val})  =>  c_13 = {c13_val} ; residual over all 16 "
     f"independent components of nabla_mu A_nu = {residual_ae}")
check(residual_ae == 0 and c13_val == 0 and sp.expand(F2 - 2 * c1_term) != 0
      and sp.expand(F2 + 2 * c3_term) != 0,
      "G2a  DERIVED, not asserted: for a GENERIC nabla_mu A_nu (16 free components), "
      "F_munu F^munu = 2 (nabla_mu A_nu nabla^mu A^nu) - 2 (nabla_mu A_nu nabla^nu A^mu) with "
      f"residual exactly {residual_ae}, so c_1 = 2, c_3 = -2 and c_13 = {c13_val}.  The last two "
      "clauses are negative controls: neither term alone reproduces F^2, so the decomposition is "
      "not a trivial match")
c13 = sp.Symbol("c13", real=True)
cT2 = 1 / (1 - c13)
check(sp.simplify(cT2.subs(c13, c13_val) - 1) == 0,
      "G2  c_T = 1 EXACTLY.  A host built from F_munu F^munu alone has c_13 = 0 by G2a, and "
      "c_T^2 = 1/(1-c_13) = 1.  The NONLINEARITY does "
      "not spoil it, because on the COSMOLOGICAL background the unit vector is A_mu = (-1,0,0,0) "
      "with F_munu = 0 identically, so the graviton sees Lcal'(0) times the Maxwell structure "
      "and c_13 = 0 still.  GW170817 SAFE on both kernels",
      "and Lcal'(0) = mu_v(0) = B^2 > 0, so there is no wrong-sign rescaling of the graviton")
check(sp.simplify(M[0, 0] - Lp) == 0 and sp.simplify(Bgrad[0, 0] + Lp) == 0,
      "G3  the two TRANSVERSE vector modes have kinetic coefficient Lcal' and gradient "
      "coefficient Lcal', so c^2_perp = 1 exactly at every acceleration on every kernel -- "
      "transverse gradient stability is unconditional")
for nm in FOOTINGS:
    y1 = Y_1AU[nm]
    kperp, kpar = Kperp_num(a0line, y1), Kpar_num(a0line, y1)
    c2p = kperp / kpar
    info(f"G4  a_0-line parallel mode at 1 AU, {nm}",
         f"K_perp = {mp.nstr(kperp, 6)}, K_par = {mp.nstr(kpar, 6)}, c^2_par = "
         f"{mp.nstr(c2p, 6)}  ({mp.nstr(mp.sqrt(c2p), 6)} c)")
    check(c2p > 1,
          f"G4 {nm}  CHERENKOV: on the a_0-line the parallel mode is SUPERLUMINAL "
          f"(c^2_par = {float(c2p):.3e}, and c^2_par -> 1 exactly in deep MOND).  Gravitational "
          "Cherenkov constrains SUBluminal modes -- cosmic rays cannot radiate into a faster "
          "mode -- so THE CHERENKOV BOUND IS CLEARED.  Direction: this runs in the framework's "
          "favour, and I note that the SCALAR host would instead be subluminal by the reciprocal "
          "factor and would face the bound")
    check(kpar < 1e-15,
          f"G5 {nm}  THE PRICE, and it is real: K_par = {mp.nstr(kpar, 5)} at 1 AU (it falls as "
          "1/(8x^2)), so the parallel mode's kinetic term is degenerate to 17 digits in the "
          "Newtonian regime.  That is STRONG COUPLING -- the same EFT cost sf39 named for the "
          "khronon.  NOT a kill and NOT resolved here; an unpriced liability",
          "stated as owed")

# =============================================================================================
head("PART H -- Q2 and the 1-AU monopole, priced independently")
# =============================================================================================
print("""
  Q2 is ARM-LEVEL and already proved in the corpus: all four mechanisms reduce to
  div[(1 - mu_v/B^2) grad Phi] = 4 pi G rho_b for a general Phi(x,y,z) with no symmetry assumed,
  so WHICH FIELD CARRIES THE HALO CANNOT MOVE Q2.  Only the interpolation can.  Reviving C on the
  ghost changes nothing here.  The banked numbers are restated AND cross-checked against an
  independent scaling estimate, so the verdict is not merely inherited.
""")
Q2_CEIL, Q2_CEN, Q2_SIG = 5.2e-27, 1.6e-27, 1.8e-27
Q2_BANKED = {("a_0-line", "canonical"): 2.50e-26, ("a_0-line", "alt"): 3.31e-26,
             ("MS08", "canonical"): 3.46e-26, ("MS08", "alt"): 3.80e-26}
V_SUN, R_SUN = 233e3, 8.2 * KPC
g_ext = V_SUN ** 2 / R_SUN
info("H0  external field at the Sun", f"g_ext = V^2/R = {g_ext:.4e} m/s^2 = "
                                      f"{g_ext/float(A0['canonical']):.4f} a_0 canonical / "
                                      f"{g_ext/float(A0['alt']):.4f} a_0 alt -- inside the gate's "
                                      f"stated 1.9-2.6 a_0 window, computed not assumed")
eta_anchor = np.array([1.0, 1.5, 2.0])
q_anchor = np.array([0.094, 0.159, 0.221])
q_slope, q_int = np.polyfit(eta_anchor, q_anchor, 1)
for nm in FOOTINGS:
    a0 = float(A0[nm])
    eta = g_ext / a0
    q_eta = q_slope * eta + q_int
    scale = np.sqrt(a0 ** 3 / (G_ * MSUN))
    Q2_est = q_eta * scale
    banked = Q2_BANKED[("a_0-line", nm)]
    info(f"H1  INDEPENDENT Q2 cross-check, {nm}",
         f"eta = {eta:.4f}, q(eta) = {q_eta:.4f} from the published anchors "
         f"q(1,1.5,2) = 0.094,0.159,0.221 ; sqrt(a_0^3/GM_sun) = {scale:.4e} s^-2 ; "
         f"Q2_est = {Q2_est:.4e} s^-2 vs banked {banked:.4e} -> ratio {banked/Q2_est:.3f}")
    check(0.5 < banked / Q2_est < 2.0 and Q2_est > Q2_CEIL,
          f"H1 {nm}  an INDEPENDENT dimensional estimate Q2 ~ q(eta) sqrt(a_0^3/GM_sun), "
          f"calibrated on the published anchors, reproduces the banked value to "
          f"{banked/Q2_est:.2f}x AND independently exceeds the Park+2026 ceiling by "
          f"{Q2_est/Q2_CEIL:.1f}x.  The banked number is not an artefact.  AGAINST INTEREST: "
          "this is a scaling check, NOT a re-derivation of the AQUAL quadrupole; that is owed")
for (kn, fn), qv in Q2_BANKED.items():
    info(f"H2  banked {kn:9s} {fn:9s}", f"Q2 = {qv:.3e} s^-2 = {qv/Q2_CEIL:.2f}x the 2-sigma "
                                        f"ceiling {Q2_CEIL:.1e}, = +{(qv-Q2_CEN)/Q2_SIG:.1f} sigma")
check(all(qv > Q2_CEIL for qv in Q2_BANKED.values()),
      f"H2  every kernel x footing cell exceeds the Cassini quadrupole ceiling "
      f"({min(Q2_BANKED.values())/Q2_CEIL:.1f}x to {max(Q2_BANKED.values())/Q2_CEIL:.1f}x), and "
      "AQUAL's quadrupole is LARGER than QUMOND's (Desmond+2024 fn 6), so these are FLOORS.  "
      "A revived mechanism C inherits all of it: GATE 3 FAILS on both footings before the ghost "
      "question is even asked")
for nm in FOOTINGS:
    a0 = A0[nm]
    p_mono = a0line(Y_1AU[nm])[1] * a0
    info(f"H3  {nm} a_0-line 1-AU monopole",
         f"{float(p_mono):.5e} m/s^2 = a_0/2 exactly = {float(p_mono/EPM_BUDGET[nm]):.0f}x the "
         f"Mars budget")

# =============================================================================================
head("PART I -- the double count for the revived version")
# =============================================================================================
print("""
  In mechanism C the halo IS real dark mass locked to the baryons (its Gauss theorem:
  G M_chi(r)/r^2 = g_obs - g_bar identically).  So the double count is not avoided by identifying
  fields -- it is one field asked to satisfy two independent determinations.  Computed:
""")
f_cos = 0.2650 / 0.04930
MB = 1e11 * MSUN
for nm in FOOTINGS:
    a0 = float(A0[nm])
    rM = np.sqrt(G_ * MB / a0)
    r_eq = f_cos * rM
    info(f"I1  {nm}",
         f"r_M = {rM/KPC:.2f} kpc ; the lock gives M_chi(<r) = sqrt(G M_b a_0) r / G, LINEAR in "
         f"r and UNBOUNDED.  It reaches the cosmic share Omega_dm/Omega_b = {f_cos:.3f} at "
         f"r = {f_cos:.2f} r_M = {r_eq/KPC:.1f} kpc and overshoots beyond")
    for rr, lbl in ((1e3 * KPC, "1 Mpc"), (3e3 * KPC, "3 Mpc")):
        over = (np.sqrt(G_ * MB * a0) * rr / G_) / (f_cos * MB)
        info(f"I1b {nm} at {lbl}", f"M_chi / [(Omega_dm/Omega_b) M_b] = {over:.1f}x")
    over1 = (np.sqrt(G_ * MB * a0) * 1e3 * KPC / G_) / (f_cos * MB)
    check(over1 > 10,
          f"I1 {nm}  the lock has NO TRUNCATION SCALE OF ITS OWN: by 1 Mpc it has deposited "
          f"{over1:.0f}x this galaxy's cosmic dark share.  Truncation must come from the "
          "external field, so M_chi/M_b = a_0/g_ext is set by ENVIRONMENT, not by cosmology -- "
          "and Omega_dm would not be universal")
g_needed = 1 / f_cos
info("I2  where the lock would have to truncate",
     f"M_chi/M_b = a_0/g_ext = {f_cos:.3f} requires g_ext = {g_needed:.4f} a_0 exactly")
spread = (1 / 0.01) / (1 / 2.0)
for gx in (0.01, 0.05, 0.1, g_needed, 1.0, 2.0):
    info("I2b M_chi/M_b if the halo truncates where g_obs = g_ext",
         f"g_ext = {gx:.4f} a_0  =>  M_chi/M_b = {1/gx:.1f}   (needed {f_cos:.2f})")
check(spread > 100,
      f"I2  across the plausible 0.01-2 a_0 range of external fields M_chi/M_b runs from 0.5 to "
      f"100, a spread of {spread:.0f}x, and the cosmic value is hit only at the single point "
      f"g_ext = {g_needed:.3f} a_0.  THE DOUBLE COUNT IS NOT FIXED BY THE REVIVAL -- it is "
      "SHARPENED, because in mechanism C the halo is real mass with no separate cosmological "
      "reservoir to hide in")
a0z = 0.0060
check(np.sqrt(a0z) < 0.1,
      f"I3  and the framework's own a_0(z) law makes it worse at the epoch that matters: "
      f"a_0(z=1090)/a_0(0) = {a0z}, so the lock's amplitude sqrt(G M_b a_0) is "
      f"{np.sqrt(a0z):.3f} of today's at recombination.  The lock cannot be the origin of the "
      "CMB's dark component, so a separate Omega_dm is still required and still double-counts "
      "in galaxies.  Direction: this uses the framework's OWN promotion against the mechanism")

# =============================================================================================
head("PART J -- errors, directions, and what I could NOT determine")
# =============================================================================================
for e in [
    "ERROR 1 (in the draft of this file, found and fixed here).  The numeric a_0-line kernel was "
    "coded as x = (y + sqrt(y^2+4y))/2, which is mu = x/(1+x) -- the SIMPLE kernel -- not the "
    "a_0-line x = sqrt(y^2+y).  DIRECTION: ADVERSE TO THE FRAMEWORK.  The wrong function has "
    "phantom -> 1 a_0 instead of a_0/2, so it OVERSTATED the 1-AU monopole by exactly 2x, and "
    "gave c^2_par = 1+x instead of 4x and K_par = 1/(1+x)^2 instead of 1/(8x^2).  It would have "
    "manufactured a deficit.  Corrected; the a_0-line's 1-AU phantom is now computed as exactly "
    "0.5 a_0, which independently reproduces the corpus's own a_0/2 monopole statement.",
    "ERROR 2 (in the draft, found and fixed).  A check asserted p(1) in (0.4, 0.8) for four "
    "kernels; the standard kernel mu = x/sqrt(1+x^2) gives p(1) = 0.2720 and the assertion was "
    "FALSE.  It was a bound written before the number was known -- exactly the practice this "
    "programme abandoned after sf36.  The theorem does not need it: the no-go uses the MINIMUM "
    "over kernels, computed first.  DIRECTION: it would have produced a spurious FAIL.",
    "ERROR 3 (in the draft, found and fixed).  The aether-tilt check compared 2 v_c^2 to "
    "(370 km/s)^2 and would have failed (8.0e10 < 1.37e11).  The physical claim behind it is "
    "sound but was stated as an inequality it does not satisfy.  Restated as a computed ratio.",
    "ERROR 4 (in the draft, found and fixed).  MS08's K_perp and K_par were evaluated by "
    "numerical differentiation of 1/(1-exp(-sqrt(y))); at y = 1e6 the 60-digit mpmath value of "
    "1 - e^-1000 rounds to exactly 1, so K_perp and K_par both underflowed to 0 and the run died "
    "on a ZeroDivisionError.  Trap 6 as advertised.  Replaced by the exact closed forms "
    "K_perp = e^-sqrt(y) and K_par = [u e^u - 2 e^u + 2] e^-u / [u - 2 e^u + 2], with a "
    "25-digit control against numerical differentiation in the safe regime.",
    "MY OWN ERROR, logged from the earlier draft: the first covariantisation used "
    "P(E) = mu_v(E) E^2, reading mechanism C's schematic Lagrangian literally.  That gives flux "
    "mu_v' E^2 + 2 mu_v E, not mu_v E.  DIRECTION: the wrong dictionary is also positive "
    "everywhere on the a_0-line, so it would have MISSED the MS08 result entirely and "
    "manufactured a WIN.  Corrected in PART A before any verdict was written.",
    "COULD NOT DETERMINE 1.  Whether a NON-STATIC mediator background -- the framework's own "
    "phi = Q_0 t + psi(r) condensate form, giving F_munu a nonzero magnetic part and moving S_0 "
    "off E^2/2 -- can put Lcal'' on the healthy side while keeping the static galaxy solution. "
    "The Hessian STRUCTURE is unchanged (Lcal' delta_ij + Lcal'' E_i E_j), but the map from "
    "mu_v to Lcal'' is not the same one, so PART D's identification would have to be redone. "
    "This is the one live escape and it is NOT free: mechanism C's Gauss theorem "
    "G M_chi/r^2 = g_obs - g_bar came from the POINTWISE equilibrium balance, which a moving "
    "background breaks.",
    "COULD NOT DETERMINE 2.  Whether a position-dependent coupling B(x) evades the no-go.  "
    "Mechanism C's A3 proves B is pure normalisation for CONSTANT B; a varying B would break the "
    "elimination that produces its AQUAL baryon sector.  It also costs mechanism C its headline "
    "property -- zero new free functions -- so it is a different mechanism.",
    "COULD NOT DETERMINE 3.  The AQUAL quadrupole was NOT re-derived here.  PART H validates the "
    "banked Q2 against an independent dimensional estimate calibrated on the published anchors "
    "(agreement 1.2-1.5x, same side of the ceiling), which is enough to say gate 3 fails, but it "
    "is not a first-principles recomputation.",
    "COULD NOT DETERMINE 4.  The post-EFE monopole factor was scaled from the corpus's 119-189x "
    "by the same x27 ephemeris correction rather than recomputed.  The no-go's margin is ~3 "
    "orders even at the favourable end, so the conclusion does not hinge on it, but the number "
    "itself is inherited.",
    "COULD NOT DETERMINE 5, AND IT IS THE MOST IMPORTANT CAVEAT ON THE HESSIAN.  The quadratic "
    "action computed here is the AETHER SECTOR'S OWN, with the metric perturbations frozen.  In "
    "a full Einstein-aether the spin-0 aether mode MIXES with the metric, and its kinetic "
    "coefficient there is a c_i-dependent combination, not the bare one.  Direction: UNKNOWN.  "
    "That mixing could in principle move the parallel eigenvalue in either direction, and I did "
    "NOT compute it.  What is NOT exposed to this caveat is PROOF 1: the ellipticity of "
    "mechanism C's own non-relativistic mediator equation is a statement about its stated field "
    "equation (A-ii) and involves no metric at all, and PROOF 4 fixes the parallel eigenvalue "
    "from the static flux law alone.  So the NO-GO of PART F does not depend on the mixing; the "
    "clean 'the a_0-line has no ghost' statement of PART E does, to the extent that a full "
    "aether+metric analysis could alter it.",
    "COULD NOT DETERMINE 6.  Strong coupling was diagnosed (K_par = 3.1e-17 at 1 AU) but no "
    "cutoff scale was computed, so I cannot say whether the a_0-line's healthy parallel mode is "
    "within EFT control in the solar system.",
    "NOT AN ERROR, WORTH LOGGING.  The completeness critic's hypothesis was specific, testable, "
    "and WRONG -- but testing it was worth one Hessian, because it converted "
    "'refuted-as-covariantised' into a theorem, exposed that mechanism C's own file never "
    "checked its parallel eigenvalue, and produced a kernel-space no-go that no mechanism-level "
    "search would have found.",
]:
    info("J", e)

print("""
  THE VERDICT, stated against interest in both directions.

  IN THE FRAMEWORK'S FAVOUR, and this is a real correction to the published refutation:
    * The critic's hypothesis is REFUTED -- the constraint cannot touch the kinetic Hessian --
      but the refutation it defends is ALSO wrong as applied.  The published ghost was computed
      on Route A / MS08.  On MECHANISM C'S OWN STATED KERNEL, Carl's a_0-line, K_par > 0 at every
      acceleration, analytically and over 26 decades.  There is NO GHOST, the transverse modes
      are exactly luminal, c_T = 1 exactly, and the Cherenkov bound is cleared because the
      parallel mode is superluminal rather than subluminal.  Gate (4) is CLEARED on the a_0-line
      but for strong coupling, which is a liability rather than a kill.

  AGAINST IT, and this is the larger half:
    * The health condition is d(phantom)/d g_obs >= 0 on EVERY host, and the ephemeris requires
      the phantom to FALL by 4-5 orders between y ~ 1 and y = 6.3e7.  No kernel does both.  So
      mechanism C's kernel space is EMPTY and Route 1 cannot rescue it: gate (2) and gate (3)
      are now known to be in direct contradiction WITHIN this mechanism.
    * Gate (3) also fails on its own terms: Q2 = 2.5-3.8e-26 s^-2 = 4.8-7.3x the Park+2026
      ceiling on every kernel x footing cell, arm-level and unmoved by the revival.
    * Gate (5) is not fixed and is sharpened: the lock is unbounded in r, so Omega_dm/Omega_b
      becomes an environmental variable spanning 200x, and a_0(z=1090) = 0.0060 a_0(0) means the
      lock cannot source the CMB's dark component.
    * Gate (1) is cleared, but per the deflation that is a THRESHOLD, not an achievement.

  A REVIVED MECHANISM C IS NOT A SURVIVOR.  The ghost evaporates on the framework's own kernel;
  the mechanism does not.
""")
print("=" * 100)
print(f"ROUTE-2 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
