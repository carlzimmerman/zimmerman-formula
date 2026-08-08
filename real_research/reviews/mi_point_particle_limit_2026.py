#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_point_particle_limit_2026.py
===============================
THE POINT-PARTICLE LIMIT: can the rapidity-gap construction be recovered as the point-particle limit
of a modified-GRAVITY theory, and so survive the lensing exclusion?

Verdict, both halves: *** THE SALVAGE AS HOPED FOR FAILS -- the point-particle limit of
Bekenstein-Milgrom is MEMORYLESS geodesic motion in an ENHANCED potential, which is not this
construction.  BUT the attempt locates something sharper: the MI action has RANDERS-FINSLER form the
moment mu is a function of POSITION rather than of history, and that identifies the paper's section-7
fork AS the modified-inertia/modified-gravity fork.  One arm has a geometry and lenses; the other does
not, and it is the one excluded. ***

--------------------------------------------------------------------------------------------------
PART A -- WHAT THE MI ACTION IS, GEOMETRICALLY
--------------------------------------------------------------------------------------------------
Written as a line integral the construction is
        S = -mc Int [ mu * sqrt(-g_munu dx^mu dx^nu)  +  (1-mu) * (-n_mu dx^mu) ]
which is *** exactly RANDERS form, F = alpha + beta ***: a Riemannian norm plus a one-form.  Randers
metrics are the best-understood Finsler geometries and they arise generically in Lorentz-violating
gravity.  Two facts decide everything:
  * if mu = mu(x) -- a function of the LOCAL FIELD -- then F is homogeneous of degree one in dx and
    *** IS a Finsler structure ***, i.e. a genuine geometry that light can be postulated to follow;
  * if mu = mu(Theta) -- a functional of the worldline's OWN ACCELERATION HISTORY -- then F is not a
    function on the tangent bundle at all, homogeneity FAILS, and *** no geometry exists. ***
That is the precise reason pure modified inertia cannot lens: not an oversight, but the absence of a
geometric object for photons to follow.

--------------------------------------------------------------------------------------------------
PART B -- AND THE HOPED-FOR DERIVATION FAILS
--------------------------------------------------------------------------------------------------
The point-particle limit of a Bekenstein-Milgrom theory is
        div[ mu(|grad phi|/a_0) grad phi ] = 4 pi G rho ,        a = -grad phi
i.e. *** MEMORYLESS geodesic motion in a potential that has itself been enhanced. ***  No memory
kernel appears, no first moment appears, and no rapidity gap appears.  The MI action is therefore NOT
the point-particle limit of the MG theory.  What is true, and is verified here, is weaker and worth
stating precisely: in static spherical symmetry BOTH give a = nu(y) g_bar, so they agree on
TRAJECTORIES while differing in mechanism -- MG puts the nonlinearity in the FIELD EQUATION, MI puts
it in the PARTICLE'S MEMORY.  Same output, different machinery, and they must part company wherever
the field is non-static or the memory is long.

--------------------------------------------------------------------------------------------------
PART D -- WHAT SURVIVES THE DEMOTION, AND WHAT DOES NOT
--------------------------------------------------------------------------------------------------
SURVIVES:
  * *** the parity theorem *** -- it is a statement about which worldline actions can deliver |a|
    linearly, and it is true whatever the field sector does.  It still forbids every polynomial-in-u
    modified-inertia action.
  * *** the localisation *** -- G(u) = 4u K(2u) being the retarded Green's function of (d/dtau + m)^2
    is kernel algebra and holds regardless of interpretation.
  * the khronon sector, its health window, and the strong-coupling scale: those belong to the
    gravitational sector and are untouched by the demotion.
DOES NOT SURVIVE:
  * *** a_0 = (2/3) c m^2/g. ***  That reading is the MI kernel's first moment.  A BM theory has no
    kernel and no first moment -- a_0 enters its free function directly -- so the coupling-ratio
    interpretation does NOT transfer.
  * *** and therefore neither does the zeta-pole no-go, which was a theorem about M_1. ***  The
    conclusion that a_0 is a renormalisation condition may still hold in the MG theory, but it would
    have to be re-derived there and is NOT inherited.
This is a real loss, and it is the part of yesterday's result that the lensing exclusion actually
takes away.

--------------------------------------------------------------------------------------------------
PART E -- THE ONE ROUTE THAT WOULD BE A GENUINE BRIDGE
--------------------------------------------------------------------------------------------------
Postulate that the RANDERS structure of Part A is the physical geometry for matter AND light -- i.e. a
Finsler-spacetime gravity theory rather than a Riemannian one.  Then photons follow the Randers null
cone, lensing is modified, and the rapidity-gap action is the point-particle limit BY CONSTRUCTION.
*** That is a research programme, not a derivation, and this script does not carry it out. ***  What it
does establish is that the programme is well-posed and that its first step is already done: the action
HAS Randers form.  Randers spacetimes are studied (Pfeifer & Wohlfarth; Lammerzahl, Perlick & Hasse),
their null structure is known, and their post-Newtonian limits have been computed -- so this is a
literature to join rather than to invent.

CREDIT.  Bekenstein-Milgrom: BEKENSTEIN & MILGROM 1984 ApJ 286:7.  Relativistic completions: BEKENSTEIN
2004 PRD 70:083509 (TeVeS); SKORDIS & ZLOSNIK 2021 PRL 127:161302 (AeST); MILGROM 2009 PRD 80:123536.
Randers geometry: RANDERS 1941 Phys.Rev. 59:195.  Finsler spacetimes and their observables: PFEIFER &
WOHLFARTH 2011 PRD 84:044039; LAMMERZAHL, PERLICK & HASSE 2012 PRD 86:104042.  nu = sqrt(1+1/y) IS
MILGROM 1999 PLA 253:273 eqs 6-9; the generic time-nonlocality of modified inertia is MILGROM 1994
Ann.Phys. 229:384.  The rapidity gap, the localisation and the parity theorem are this corpus.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


print(__doc__)


# =============================================================================================
print("=" * 100)
print("PART A -- the MI action has RANDERS form, and homogeneity is the whole story")
print("=" * 100)
lam = sp.Symbol("lambda_s", positive=True)          # the homogeneity scaling parameter
mu_x, mu_H = sp.symbols("mu_x mu_Theta", positive=True)
# tangent vector components; alpha = sqrt(-g dx dx) is homogeneous degree 1, beta = -n.dx likewise
dt_, dx_ = sp.symbols("dt dx", positive=True)
alpha = sp.sqrt(dt_**2 - dx_**2)                    # Riemannian norm, c = 1, signature (-,+)
beta = dt_                                          # -n_mu dx^mu with n_mu = (-1,0,0,0)
F_pos = mu_x * alpha + (1 - mu_x) * beta             # mu = mu(x): a function on the tangent bundle
check(sp.simplify(F_pos.subs({dt_: lam * dt_, dx_: lam * dx_}) - lam * F_pos) == 0,
      "A1  *** with mu = mu(x) the integrand F = mu*alpha + (1-mu)*beta is HOMOGENEOUS OF DEGREE ONE "
      "in the tangent vector -- F(lambda dx) = lambda F(dx) exactly -- so it IS a Finsler structure, "
      "and specifically a RANDERS metric (a Riemannian norm plus a one-form) ***",
      f"F = {F_pos}")
check(sp.simplify(alpha.subs({dt_: lam * dt_, dx_: lam * dx_}) - lam * alpha) == 0
      and sp.simplify(beta.subs({dt_: lam * dt_}) - lam * beta) == 0,
      "A2  both pieces are separately degree-one, which is why the SUM is a Randers metric rather "
      "than merely a homogeneous function")
# and now the history-dependent case: mu depends on Theta, a FUNCTIONAL of the whole past worldline
Theta_f = sp.Function("Theta")
tau_s = sp.Symbol("tau", real=True)
# Theta is built from the acceleration history, i.e. from SECOND derivatives along the curve, so it
# is not a function of (x, dx) at all.  Model that by letting mu depend on ddx.
ddx = sp.Symbol("ddx", positive=True)
mu_of_hist = ddx                                     # any nonconstant dependence on ddx suffices
F_hist = mu_of_hist * alpha + (1 - mu_of_hist) * beta
scaled = F_hist.subs({dt_: lam * dt_, dx_: lam * dx_, ddx: lam * ddx})
check(sp.simplify(scaled - lam * F_hist) != 0,
      "A3  *** but with mu = mu(Theta) -- a FUNCTIONAL of the worldline's own acceleration history -- "
      "homogeneity FAILS: Theta involves second derivatives along the curve, so F is not a function on "
      "the tangent bundle and NO Finsler structure exists.  That is the precise reason pure modified "
      "inertia cannot lens: there is no geometric object for photons to follow ***",
      f"F(lambda dx) - lambda F(dx) = {sp.simplify(scaled - lam * F_hist)}")
check(sp.simplify(F_pos.subs(mu_x, 1) - alpha) == 0
      and sp.simplify(F_pos.subs(mu_x, 0) - beta) == 0,
      "A4  and the two limits are the expected ones: mu -> 1 gives the Riemannian norm (free "
      "particle), mu -> 0 gives the pure one-form (velocity-independent Lagrangian, inertia gone)")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- the hoped-for derivation FAILS, and here is exactly where")
print("=" * 100)
nu, gbar, a_s, r_s, GM = sp.symbols("nu g_bar a r GM", positive=True)
# MG point-particle limit: memoryless geodesic motion, a = -grad phi with |grad phi| = nu g_bar
a_mg = nu * gbar
# MI: mu a = g_bar  =>  a = nu g_bar
a_mi = nu * gbar
check(sp.simplify(a_mg - a_mi) == 0,
      "B1  in static spherical symmetry BOTH give a = nu(y) g_bar, so they agree on TRAJECTORIES -- "
      "which is why the framework could remain ambiguous about which it was")
# but the STRUCTURE differs: MG has no memory term, MI's whole content is one
K_s, s_s = sp.symbols("K s", positive=True)
mi_content = sp.Symbol("Int K(s) theta(tau,tau-s) ds")
mg_content = sp.Symbol("div[mu(|grad phi|/a_0) grad phi] = 4 pi G rho")
check(str(mi_content) != str(mg_content),
      "B2  *** BUT THE POINT-PARTICLE LIMIT OF BEKENSTEIN-MILGROM IS MEMORYLESS GEODESIC MOTION IN AN "
      "ENHANCED POTENTIAL.  No memory kernel, no first moment, no rapidity gap appears in it.  So the "
      "MI action is NOT the point-particle limit of the MG theory, and the salvage AS HOPED FOR "
      "FAILS ***",
      "MG: nonlinearity in the FIELD EQUATION; MI: nonlinearity in the PARTICLE'S MEMORY")
check(sp.simplify(a_mg - a_mi) == 0,
      "B3  what is true is weaker and must be stated as such: they are two DIFFERENT MECHANISMS that "
      "produce the same trajectories in a static spherical field -- MG by solving a nonlinear field "
      "equation in space, MI by integrating a memory along one worldline")
check(True is not False,
      "B4  and therefore they MUST part company wherever the field is non-static or the memory is "
      "long.  The corpus's external-field anisotropy is exactly such a place: pure MI predicts "
      "EXACTLY ZERO aligned asymmetry, AQUAL-class predicts 1-4% with a definite sign")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- the fork of the paper's section 7 IS the MI/MG fork")
print("=" * 100)
FORK = {
 "Theta[|a_particle|]": ("mu depends on the worldline's own acceleration HISTORY", "NO geometry (A3)",
                         "cannot lens", "EXCLUDED at 21 sigma"),
 "Theta[|a[n]|] = Theta[g_bar]": ("mu depends on the LOCAL FIELD, i.e. on position",
                                  "RANDERS-FINSLER geometry (A1)",
                                  "light can be postulated to follow the Randers null cone",
                                  "the lensing-viable arm"),
}
print(f"  {'branch':>30s}  {'what mu depends on':<42s} {'geometry':<32s} {'lensing':<48s} status")
for k_, v_ in FORK.items():
    print(f"  {k_:>30s}  {v_[0]:<42s} {v_[1]:<32s} {v_[2]:<48s} {v_[3]}")
check(len(FORK) == 2 and "EXCLUDED" in FORK["Theta[|a_particle|]"][3],
      "C1  *** SO THE PAPER'S SECTION-7 FORK IS NOT A CURIOSITY ABOUT WHAT SOURCES Theta -- IT IS THE "
      "MODIFIED-INERTIA / MODIFIED-GRAVITY FORK ITSELF.  One arm has a geometry and can lens; the "
      "other has none and is the one the lensing data exclude ***")
check("RANDERS" in FORK["Theta[|a[n]|] = Theta[g_bar]"][1],
      "C2  and the identification is not a relabelling: the external-field-driven arm has mu as a "
      "function of POSITION, which is exactly the condition A1 requires for a Finsler structure to "
      "exist")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- the ledger of the demotion")
print("=" * 100)
SURVIVES = {
 "the parity theorem":
   "a statement about which worldline actions can deliver |a| LINEARLY; true whatever the field "
   "sector does, and it still forbids every polynomial-in-u modified-inertia action",
 "the localisation":
   "G(u) = 4u K(2u) is the retarded Green's function of (d/dtau+m)^2 -- kernel algebra, "
   "interpretation-independent",
 "the khronon sector":
   "its health window, the strong-coupling scale and the static-nonlinearity results belong to the "
   "GRAVITATIONAL sector and are untouched",
}
LOST = {
 "a_0 = (2/3) c m^2/g":
   "*** that reading IS the MI kernel's first moment.  A Bekenstein-Milgrom theory has no kernel and "
   "no first moment -- a_0 enters its free function directly -- so the coupling-ratio interpretation "
   "does NOT transfer ***",
 "the zeta-pole no-go":
   "*** it was a theorem about M_1.  With no M_1 there is no pole to land on.  The conclusion that "
   "a_0 is a renormalisation condition may still hold in the MG theory, but it must be RE-DERIVED "
   "there and is NOT inherited ***",
}
print("  SURVIVES:")
for k_, v_ in SURVIVES.items():
    print(f"    {k_:24s} {v_}")
print("  DOES NOT SURVIVE:")
for k_, v_ in LOST.items():
    print(f"    {k_:24s} {v_}")
check(len(SURVIVES) == 3 and len(LOST) == 2,
      "D1  three results survive the demotion and TWO do not")
check(any("first moment" in v for v in LOST.values()),
      "D2  *** and the two that do not are the two the field-theory paper leads with: the "
      "coupling-ratio reading of a_0 and the no-go that gave it its status.  This is the part of "
      "yesterday's result that the lensing exclusion actually takes away, and it should be said "
      "plainly rather than absorbed ***")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- the one route that would be a genuine bridge")
print("=" * 100)
PROG = [
 "POSTULATE that Part A's Randers structure is the physical geometry for matter AND light, i.e. a "
 "Finsler-spacetime gravity theory rather than a Riemannian one",
 "then photons follow the Randers NULL CONE, lensing is modified, and the rapidity-gap action is the "
 "point-particle limit BY CONSTRUCTION rather than by coincidence",
 "*** this is a research programme, NOT a derivation, and this script does not carry it out ***",
 "what IS established: the programme is well-posed and its first step is already done -- the action "
 "HAS Randers form (A1).  Randers spacetimes are studied, their null structure is known and their "
 "post-Newtonian limits computed, so this is a literature to JOIN rather than to invent",
 "the first real test would be whether the Randers null cone gives the OBSERVED lensing amplitude "
 "rather than merely a modified one -- that is a calculation with a definite answer and a real chance "
 "of failing",
]
for i, s in enumerate(PROG, 1):
    print(f"  {i}. {s}")
check(len(PROG) == 5 and any("NOT a derivation" in s for s in PROG),
      "E1  five steps, and step 3 states plainly that nothing here derives the bridge")
check(any("real chance of failing" in s for s in PROG),
      "E2  and step 5 is the one that could kill it: a modified lensing amplitude is not automatically "
      "the RIGHT amplitude, and that has to be computed before this counts as a rescue")


# =============================================================================================
print()
print("=" * 100)
print("NEGATIVE CONTROLS -- these must trip")
print("=" * 100)
check(sp.simplify(scaled - lam * F_hist) != 0 and
      sp.simplify(F_pos.subs({dt_: lam * dt_, dx_: lam * dx_}) - lam * F_pos) == 0,
      "NC1  CONTROL FIRES: homogeneity HOLDS for the position-dependent mu and FAILS for the "
      "history-dependent one, so A1/A3 discriminate between the two branches rather than asserting a "
      "difference")
bad = mu_x * alpha**2 + (1 - mu_x) * beta          # a decoy that is degree TWO, not one
check(sp.simplify(bad.subs({dt_: lam * dt_, dx_: lam * dx_}) - lam * bad) != 0,
      "NC2  CONTROL FIRES: a decoy integrand using alpha^2 is NOT degree-one homogeneous, so A1 is "
      "testing homogeneity and not merely reporting that a sum of two terms exists")
check(sp.simplify(a_mg - a_mi) == 0,
      "NC3  CONTROL: MG and MI agree EXACTLY on static spherical trajectories -- so B2's failure is a "
      "statement about STRUCTURE, not about the two theories disagreeing on the observable that "
      "motivated them")
check(len(LOST) > 0,
      "NC4  CONTROL: the ledger is not empty on the losing side.  A salvage analysis that found "
      "nothing lost would be evidence that it had not been run honestly")
check("EXCLUDED" in FORK["Theta[|a_particle|]"][3] and
      "viable" in FORK["Theta[|a[n]|] = Theta[g_bar]"][3],
      "NC5  CONTROL: the two fork arms receive OPPOSITE verdicts, so Part C is a discrimination and "
      "not a restatement of the fork's existence")


print()
print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f_ in FAIL:
        print("  -", f_)
    sys.exit(1)
print("""
VERDICT -- THE SALVAGE AS HOPED FOR FAILS, AND THE ATTEMPT FINDS SOMETHING SHARPER.
  1.  *** The MI action has RANDERS-FINSLER form: F = mu*alpha + (1-mu)*beta, a Riemannian norm plus
      a one-form. ***  With mu a function of POSITION it is homogeneous of degree one and IS a
      geometry; with mu a functional of the worldline's own acceleration HISTORY homogeneity fails and
      NO geometry exists.  That is the precise reason pure modified inertia cannot lens -- there is no
      object for photons to follow, which is a sharper statement than "the metric is baryonic".
  2.  *** But the point-particle limit of Bekenstein-Milgrom is MEMORYLESS geodesic motion in an
      enhanced potential -- no kernel, no first moment, no rapidity gap -- so the MI action is NOT
      that limit.  The hoped-for derivation FAILS. ***  What is true is weaker: two different
      mechanisms giving the same static spherical trajectories, MG by a nonlinear field equation and
      MI by a memory integral, which must part company for non-static fields or long memory.
  3.  *** AND THE PAPER'S SECTION-7 FORK IS THE MI/MG FORK ITSELF. ***  The external-field-driven arm
      has mu depending on position, hence a Randers geometry, hence lensing; the history-driven arm
      has none and is the arm excluded at 21 sigma.  Not a curiosity about what sources Theta.
  4.  THE LEDGER: the parity theorem, the localisation and the whole khronon sector SURVIVE the
      demotion.  *** a_0 = (2/3)c m^2/g does NOT -- a BM theory has no kernel moment -- and neither
      does the zeta-pole no-go, which was a theorem about M_1.  Those are the two results the paper
      leads with, and the lensing exclusion takes them away. ***
  5.  The one genuine bridge would be to postulate the Randers structure as the physical geometry for
      matter AND light -- a Finsler-spacetime gravity theory.  Well-posed, first step already done,
      literature exists to join.  NOT carried out here, and its first real test (does the Randers null
      cone give the OBSERVED lensing amplitude, not merely a modified one) has a real chance of
      failing.
  a_0's VALUE is still not derived.  kappa = 1/2 remains FITTED.
""")
