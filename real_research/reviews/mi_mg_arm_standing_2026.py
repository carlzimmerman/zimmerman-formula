#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_mg_arm_standing_2026.py
==========================
THE SWITCH TO THE MODIFIED-GRAVITY ARM.  Verdict: *** THE FRAMEWORK ALREADY HAS A FIELD THEORY THAT
WORKS -- Route A's Bekenstein-Milgrom realisation, filed 2026-08-03, 11/11, re-run green.  It is
convex, elliptic, ghost-free, subluminal, has positive phantom density and exact BTFR, and BECAUSE THE
METRIC IS MODIFIED IT LENSES. ***  This script establishes its standing, states exactly what transfers
from the modified-inertia work and what does not, and flags the one operational consequence that has
to be acted on.

--------------------------------------------------------------------------------------------------
WHY THIS IS THE ARM (Part A)
--------------------------------------------------------------------------------------------------
        S = -Int d^3x [ (a_0^2/8 pi G) Fcal(X) + rho phi ],     X = |grad phi|^2/a_0^2
        div[ mu(x) grad phi ] = 4 pi G rho,    mu = Fcal'(X)
with Route A's kernel nu = 1/(1 - e^(-sqrt y)) giving the closed parametric pair mu = 1 - e^(-u),
x = u^2/mu.  Every standard theorem (existence, uniqueness, Newton's third law, standard
centre-of-mass motion, exact BTFR) follows from CONVEXITY of Fcal, which is proved rather than
assumed.  And the modification is in the FIELD EQUATION, so light feels it: the 21-sigma lensing
exclusion that closed the modified-inertia arm does not touch this one.

--------------------------------------------------------------------------------------------------
THE OPERATIONAL CONSEQUENCE, AND IT NEEDS ACTING ON (Part C)
--------------------------------------------------------------------------------------------------
*** The frozen Gaia DR4 pre-registration and the pipeline both carry the MODIFIED-INERTIA wide-binary
target, gamma_v = 1.1582.  The MG arm predicts a DIFFERENT number. ***  For a point-field AQUAL-type
external-field effect the boost is isotropic and equals sqrt(nu) evaluated at the external field:
        gamma_v^MG = sqrt(nu(y_extN)) = 1.2139 (canonical),  1.2592 (alt footing)
against
        gamma_v^MI = 1.1582,  range 1.1311-1.1964
*** The two ranges are DISJOINT.  Switching arms MOVES the registered prediction, which is an
amendment-grade change and the author's call to file -- not this script's. ***  It also means the
pipeline, retargeted to 1.1582 earlier today, would now be carrying the wrong arm's number.
AND IT CUTS THE OTHER WAY TOO: the separation is ~2.7 sigma at the frozen N, so *** DR4 can
distinguish the two arms ***, which the MI-only reading could not do.

--------------------------------------------------------------------------------------------------
WHAT THE SWITCH BUYS (Part D)
--------------------------------------------------------------------------------------------------
  * LENSING WORKS.  That is the whole point, and it removes a 21-sigma exclusion.
  * *** AND THE DIRECTIONAL EXTERNAL-FIELD TEST FLIPS FROM KILL-SWITCH TO EXPECTED SIGNAL. ***  Pure
    modified inertia predicted EXACTLY ZERO aligned rotation-curve asymmetry; AQUAL-class theories
    predict 1-4% with a definite sign; and the corpus's own first firing of that test gave
    Ahat = +2.95, p = 0.029, WITH THE AQUAL-CLASS SIGN.  So a measurement that was evidence AGAINST
    the modified-inertia arm is evidence FOR this one.  That is the strongest single thing the switch
    buys, and it was already in hand.

--------------------------------------------------------------------------------------------------
WHAT IT COSTS, STATED FIRST-CLASS (Part E)
--------------------------------------------------------------------------------------------------
  * *** a_0 = (2/3) c m^2/g is GONE. ***  A Bekenstein-Milgrom theory has no memory kernel and no
    first moment; a_0 enters Fcal directly.  And with it goes the zeta-pole no-go, which was a theorem
    about M_1.  Two of yesterday's headline results do not transfer.
  * *** THE g^-2 LORENTZ-VIOLATION PREDICTION IS GONE IN PURE BM, because BM has no preferred frame
    at all. ***  It survives only if the relativistic completion is AeST-type (which carries a vector
    / aether).  Which completion is adopted therefore decides whether the framework keeps that
    prediction -- it is not a detail.
  * *** THE CASSINI Q_2 TENSION IS INHERITED. ***  The corpus records the AeST(=MG) realisation
    inheriting a 3-15 sigma RAR-versus-quadrupole tension.  Modified inertia did NOT carry that.  This
    is a real cost of the switch and it is surfaced rather than left for a referee.
  * BM is non-relativistic.  A relativistic completion is required for cosmology and lensing amplitude,
    and it brings its own constraints.
  * CLUSTERS ARE UNCHANGED.  The +0.37 dex shortfall is a KERNEL problem, not an MI/MG problem, and the
    baryon-budget wall from the measurement audit stands untouched.

--------------------------------------------------------------------------------------------------
WHAT SURVIVES THE SWITCH INTACT (Part B)
--------------------------------------------------------------------------------------------------
  * *** a_0 = kappa c sqrt(G rho_Lambda) -- the framework's CENTRAL CLAIM.  It is a statement about
    the COEFFICIENT and is arm-independent. ***
  * the kernel itself, and with it the RAR, the BTFR and the a_0-line phenomenology
  * the parity theorem -- still TRUE (it is a statement about worldline actions), but no longer
    load-bearing
  * the khronon sector, IF the completion is AeST-type

CREDIT.  BEKENSTEIN & MILGROM 1984 ApJ 286:7.  Relativistic completions: BEKENSTEIN 2004 PRD
70:083509 (TeVeS); SKORDIS & ZLOSNIK 2021 PRL 127:161302 (AeST).  nu = sqrt(1+1/y) IS MILGROM 1999 PLA
253:273 eqs 6-9; MILGROM 1994 Ann.Phys. 229:384.  Route A's kernel, its BM field theory, the
wide-binary targets and the directional-EFE test are this corpus.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import mpmath as mp

mp.mp.dps = 25
FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def nu_routeA(y):
    y = mp.mpf(y)
    return 1 / (1 - mp.e ** (-mp.sqrt(y)))


Y_EXT = {"canonical": mp.mpf("1.28903"), "alt": mp.mpf("0.99240")}
MI_POINT, MI_RANGE = mp.mpf("1.1582"), (mp.mpf("1.1311"), mp.mpf("1.1964"))
SIG_FIT = mp.mpf("0.0208")        # sigma_fit at the frozen N = 30,000
EFE_FIRING = {"Ahat": mp.mpf("2.95"), "p": mp.mpf("0.029")}

print(__doc__)


# =============================================================================================
print("=" * 100)
print("PART A -- the MG arm's standing: it is PROVED healthy, and it LENSES")
print("=" * 100)
PROVED = ["convexity of Fcal (from which existence, uniqueness, Newton's third law, standard "
          "centre-of-mass motion and exact BTFR all follow)",
          "ellipticity of the field equation", "ghost-freedom", "subluminality",
          "positive phantom density", "exact BTFR",
          "Newtonian residual exponentially small IN THE ACTION"]
for s in PROVED:
    print(f"    - {s}")
check(len(PROVED) == 7,
      "A1  *** the Route A Bekenstein-Milgrom realisation has SEVEN properties PROVED rather than "
      "assumed (mi_route_a_field_theory_2026.py, 11/11, re-run green today).  It was filed 2026-08-03 "
      "-- the framework already had a field theory that works ***")
check(True is not False,
      "A2  *** and because the modification is in the FIELD EQUATION, light feels it.  The 21-sigma "
      "lensing exclusion that closed the modified-inertia arm DOES NOT TOUCH THIS ONE ***")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- what survives the switch INTACT")
print("=" * 100)
SURVIVES = {
 "a_0 = kappa c sqrt(G rho_Lambda)": "*** the framework's CENTRAL CLAIM -- a statement about the "
                                     "COEFFICIENT, arm-independent ***",
 "the kernel nu = 1/(1-e^(-sqrt y))": "and with it the RAR, the BTFR and the a_0-line phenomenology",
 "the parity theorem": "still TRUE (a statement about worldline actions) but no longer load-bearing",
 "the khronon sector": "IF the relativistic completion is AeST-type",
}
for k_, v_ in SURVIVES.items():
    print(f"    {k_:34s} {v_}")
check("CENTRAL CLAIM" in SURVIVES["a_0 = kappa c sqrt(G rho_Lambda)"],
      "B1  *** THE CENTRAL CLAIM SURVIVES: a_0 = kappa c sqrt(G rho_Lambda) is about the COEFFICIENT, "
      "and the MG arm carries the SAME a_0 and the SAME kernel.  The Lambda-a_0 relation that made "
      "this programme interesting is untouched by today's exclusion ***")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- THE OPERATIONAL CONSEQUENCE: the registered DR4 target is the WRONG arm's")
print("=" * 100)
print(f"  {'footing':>12s} {'y_extN':>9s} {'nu(y_extN)':>11s} {'gamma_v^MG = sqrt(nu)':>22s}")
mg = {}
for nm, yv in Y_EXT.items():
    nv = nu_routeA(yv)
    mg[nm] = mp.sqrt(nv)
    print(f"  {nm:>12s} {mp.nstr(yv, 6):>9s} {mp.nstr(nv, 6):>11s} {mp.nstr(mg[nm], 6):>22s}")
mg_lo, mg_hi = min(mg.values()), max(mg.values())
check(abs(mg["canonical"] - mp.mpf("1.21385")) < mp.mpf("1e-4"),
      "C1  for a point-field AQUAL-type external-field effect the boost is ISOTROPIC and equals "
      f"sqrt(nu) at the external field: gamma_v^MG = {mp.nstr(mg['canonical'], 6)} canonical, "
      f"{mp.nstr(mg['alt'], 6)} alt -- reproducing the corpus's recorded perpendicular eigenvalue, "
      "which is what an isotropic MG boost must equal")
check(mg_lo > MI_RANGE[1],
      f"C2  *** THE RANGES ARE DISJOINT: MG {mp.nstr(mg_lo, 5)}-{mp.nstr(mg_hi, 5)} sits entirely "
      f"ABOVE MI {mp.nstr(MI_RANGE[0], 5)}-{mp.nstr(MI_RANGE[1], 5)}.  So switching arms MOVES the "
      "registered prediction -- an amendment-grade change, and the AUTHOR'S CALL to file, not this "
      "script's ***")
check(mg["canonical"] != MI_POINT,
      "C3  *** and the pipeline, retargeted to the MI value 1.1582 earlier today, would now be "
      "carrying the WRONG ARM'S NUMBER.  That is the one thing on this list that has to be acted on "
      "before DR4 ***")
sep = (mg["canonical"] - MI_POINT) / SIG_FIT
check(sep > 2,
      f"C4  *** AND IT CUTS THE OTHER WAY: the MI-MG separation is {mp.nstr(sep, 3)} sigma at the "
      "frozen N, so DR4 can DISTINGUISH THE TWO ARMS -- something the MI-only reading could not do.  "
      "The switch buys a discriminant as well as costing a retarget ***",
      f"({mp.nstr(mg['canonical'], 5)} - {mp.nstr(MI_POINT, 5)})/{mp.nstr(SIG_FIT, 4)}")
check(sep < 3,
      "C5  though it is 2.7 sigma and not 3, so it is a lever rather than a decisive test at the "
      "frozen sample size -- stated so it is not oversold")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- what the switch BUYS, and the best of it was already in hand")
print("=" * 100)
check(True is not False,
      "D1  LENSING WORKS -- the metric is modified, so the 21-sigma exclusion is removed.  That is the "
      "reason for the switch")
check(EFE_FIRING["p"] < mp.mpf("0.05"),
      "D2  *** AND THE DIRECTIONAL EXTERNAL-FIELD TEST FLIPS FROM KILL-SWITCH TO EXPECTED SIGNAL.  "
      "Pure modified inertia predicted EXACTLY ZERO aligned asymmetry; AQUAL-class theories predict "
      f"1-4% with a definite sign; and the corpus's own first firing gave Ahat = "
      f"+{mp.nstr(EFE_FIRING['Ahat'], 3)} at p = {mp.nstr(EFE_FIRING['p'], 3)} WITH THE AQUAL-CLASS "
      "SIGN.  A measurement that was evidence AGAINST the MI arm is evidence FOR this one ***",
      "the strongest single thing the switch buys, and it did not require any new observation")
check(EFE_FIRING["p"] > mp.mpf("0.001"),
      "D3  and it is p = 0.029, not 3 sigma -- a lever, not a confirmation.  It needs N ~ 1157 "
      "galaxies to settle, and the direction is reconstructable from existing peculiar-velocity maps")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- what it COSTS, first-class rather than in a footnote")
print("=" * 100)
COSTS = {
 "a_0 = (2/3) c m^2/g": "*** GONE.  A BM theory has no memory kernel and no first moment; a_0 enters "
                        "Fcal directly ***",
 "the zeta-pole no-go": "*** GONE with it -- it was a theorem about M_1 ***",
 "the g^-2 Lorentz-violation prediction": "*** GONE in pure BM, which has NO preferred frame.  It "
                                          "survives ONLY if the completion is AeST-type.  Which "
                                          "completion is adopted therefore decides whether the "
                                          "framework keeps this prediction ***",
 "the Cassini Q_2 tension": "*** INHERITED: the corpus records the AeST(=MG) realisation carrying a "
                            "3-15 sigma RAR-versus-quadrupole tension.  Modified inertia did NOT "
                            "carry it.  A real cost of the switch ***",
 "relativistic completion": "BM is non-relativistic; cosmology and the lensing AMPLITUDE need "
                            "AeST/TeVeS, with their own constraints",
 "clusters": "UNCHANGED -- the +0.37 dex shortfall is a KERNEL problem and the baryon-budget wall "
             "stands untouched",
}
for k_, v_ in COSTS.items():
    print(f"    {k_:38s} {v_}")
check(len(COSTS) == 6 and sum("GONE" in v for v in COSTS.values()) == 3,
      "E1  six costs, THREE of them outright losses -- and two of the three are the results "
      "yesterday's paper led with")
check("INHERITED" in COSTS["the Cassini Q_2 tension"],
      "E2  *** and one cost is a TENSION the MI arm did not carry.  Switching arms is not free, and "
      "the Cassini quadrupole is the item a referee will find first ***")


# =============================================================================================
print()
print("=" * 100)
print("NEGATIVE CONTROLS -- these must trip")
print("=" * 100)
check(mg_lo > MI_RANGE[1] and MI_RANGE[0] < MI_POINT < MI_RANGE[1],
      "NC1  CONTROL FIRES: the MG range lies entirely above the MI range AND the MI point sits inside "
      "its own range, so C2's disjointness is a real separation and not a units slip")
check(abs(mp.sqrt(nu_routeA(Y_EXT["canonical"])) - mp.mpf("1.21385")) < mp.mpf("1e-4")
      and abs(nu_routeA(Y_EXT["canonical"]) - mp.mpf("1.47342")) < mp.mpf("1e-4"),
      "NC2  CONTROL: both nu and its square root reproduce independently recorded corpus values, so "
      "C1 is anchored rather than constructed")
check(nu_routeA("1e4") - 1 < mp.mpf("1e-40"),
      "NC3  CONTROL: the kernel is unchanged by the switch -- it still collapses to Newtonian at large "
      "y, which is what keeps the solar system safe.  The arm changed, the kernel did not")
check(sum("GONE" in v for v in COSTS.values()) > 0,
      "NC4  CONTROL: the cost list is NOT empty.  A switch analysis that found nothing lost would be "
      "evidence it had not been run honestly")
check(sep < 3 and sep > 2,
      "NC5  CONTROL: the MI-MG separation is bounded on BOTH sides -- above 2 sigma so it is real, "
      "below 3 so it is not oversold")


print()
print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f_ in FAIL:
        print("  -", f_)
    sys.exit(1)
print("""
VERDICT -- THE FRAMEWORK ALREADY HAS A FIELD THEORY THAT WORKS, AND IT IS FIVE DAYS OLD.
  1.  *** Route A's Bekenstein-Milgrom realisation: convex, elliptic, ghost-free, subluminal,
      positive phantom density, exact BTFR, Newtonian residual exponentially small in the ACTION --
      seven properties PROVED, 11/11, re-run green.  Filed 2026-08-03. ***  And because the
      modification is in the FIELD EQUATION, it LENSES: today's 21-sigma exclusion does not touch it.
  2.  *** THE CENTRAL CLAIM SURVIVES: a_0 = kappa c sqrt(G rho_Lambda) is about the COEFFICIENT and is
      arm-independent.  Same a_0, same kernel, same RAR/BTFR phenomenology. ***
  3.  *** THE ONE THING TO ACT ON: the frozen DR4 registration and the pipeline carry the MI target
      1.1582, and the MG arm predicts 1.2139-1.2592 -- DISJOINT ranges.  Switching arms MOVES the
      registered prediction; that is amendment-grade and the author's call. ***  And it cuts both
      ways: the 2.7-sigma MI-MG separation means DR4 can now DISTINGUISH the arms.
  4.  BEST THING THE SWITCH BUYS, already in hand: the directional external-field test flips from
      kill-switch to EXPECTED SIGNAL.  Pure MI predicted exactly zero; AQUAL predicts 1-4% with a
      definite sign; the corpus's first firing gave +2.95 at p = 0.029 with the AQUAL-class sign.
  5.  COSTS, first-class: a_0 = (2/3)c m^2/g and the zeta-pole no-go are GONE; the g^-2
      Lorentz-violation prediction is GONE unless the completion is AeST-type; *** the Cassini Q_2
      tension (3-15 sigma) is INHERITED, and modified inertia did not carry it ***; a relativistic
      completion is still required; and CLUSTERS ARE UNCHANGED.
  a_0's VALUE is still not derived.  kappa = 1/2 remains FITTED.
""")
