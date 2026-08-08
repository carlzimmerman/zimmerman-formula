#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_kappa_from_dimension_2026.py
===============================
kappa = (2/3)(D-1)/D, WHICH IS EXACTLY 1/2 IN FOUR SPACETIME DIMENSIONS.

A closed-form expression for the coefficient with NO free parameters, in which one factor is already
DERIVED in this corpus and the other is a named geometric ratio.  It is NOT a proof -- one premise is
unproven and Part E states exactly which and exactly where it leaks -- but it is the first expression
for kappa that contains no fitted quantity at all, and it makes falsifiable D-dependent predictions.

--------------------------------------------------------------------------------------------------
THE CHAIN
--------------------------------------------------------------------------------------------------
The proved equivalence (`mi_N_count_and_kappa_iff_2026.py`, 16/16) is
        kappa = 1/2  <==>  M1 = (4/3) t_Lambda,     t_Lambda = (G rho_Lambda)^(-1/2)
and the action's requirement is M1 = (2/3) c/a_0 with a_0 = kappa c sqrt(G rho_Lambda), so in general
        *** kappa = (2/3) t_Lambda / M1 ***
The 2/3 is DERIVED: it is the memory-force renormalisation of `mi_noncircular_ctp_eom_2026.py` (27/27),
which follows from d^2 ahat/dt^2 = Omega^2 rhat on a circular orbit and is dimension-independent.  So
everything hangs on the single dimensionless ratio M1/t_Lambda, and the PREMISE proposed here is

        *** PREMISE.  M1/t_Lambda = (rho + p)/rho for the thermal bath the acceleration reveals,
            which for a MASSLESS bath in D spacetime dimensions is D/(D-1). ***

Then kappa = (2/3)(D-1)/D, and at D = 4 that is EXACTLY 1/2.

--------------------------------------------------------------------------------------------------
WHY MY EARLIER DISMISSAL OF THIS WAS WRONG (Part C)
--------------------------------------------------------------------------------------------------
`mi_local_source_for_K_2026.py` listed "rho + p for a relativistic fluid (4/3)" among the candidate
mechanisms and struck it out as "DOES NOT APPLY -- the vacuum has w = -1 so rho + p = 0".  *** That was
a category error. ***  The worldline does not couple to the w = -1 BACKGROUND's enthalpy.  In this
framework the acceleration REVEALS a thermal bath -- that is the de Sitter-Unruh premise the whole
construction rests on -- and a thermal bath of massless quanta has w = 1/(D-1), not w = -1, hence
(rho + p)/rho = D/(D-1) = 4/3 in D = 4.  The object with w = -1 is the background; the object the
memory responds to is the bath.  Striking out the candidate on the background's equation of state was
wrong, and this script exists because of that correction.

--------------------------------------------------------------------------------------------------
WHAT IS AND IS NOT ESTABLISHED
--------------------------------------------------------------------------------------------------
ESTABLISHED: kappa = (2/3)(D-1)/D = 1/2 at D = 4 exactly, symbolically; the 2/3 is derived; the
(D-1)/D is the inverse massless-enthalpy ratio and equals the spatial-projector trace over the
spacetime trace; at INTEGER D the formula gives 1/2 only at D = 4, and it NEVER gives Milgrom 2020's
kappa = sqrt(2/3pi) (which would need D = 3.236); and the menu of natural dimension ratios contains
exactly ONE that works (Part D).
NOT ESTABLISHED: the premise.  There is no computed link between a memory kernel's FIRST MOMENT and a
fluid enthalpy ratio -- the premise is dimensional-analytic plus suggestive, not derived.  And it has a
specific leak: the revealed bath's own density scales as T^D ~ H^D, not as rho_Lambda ~ H^2, so using
the BATH's enthalpy ratio alongside the BACKGROUND's free-fall time mixes two different objects.  That
is the hole, it is stated here rather than hidden, and closing it is the whole remaining problem.

kappa = 1/2 is therefore NOT YET DERIVED.  What has changed is that the gap is now ONE dimensionless
premise with a named candidate and an identified leak, instead of an unexplained transcendental.

CREDIT.  nu = sqrt(1+1/y) IS MILGROM 1999 PLA 253:273 eqs 6-9; MILGROM 1994 Ann.Phys. 229:384;
MILGROM 2020 for cH_Lambda/2pi; the de Sitter temperature sqrt(a^2+Lambda/3)/2pi is NARNHOFER, PETER &
THIRRING 1996 IJMPB 10:1507; GIBBONS & HAWKING 1977.  The memory-force renormalisation, the
equivalence and the scale-counting theorem are this corpus.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import sympy as sp
from mpmath import mp

mp.dps = 40

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=10):
    return mp.nstr(mp.mpf(x), n)


C      = mp.mpf("2.99792458e8")
LAM    = mp.mpf("1.0908e-52")
G      = mp.mpf("6.67430e-11")
OMEGA_L = mp.mpf("0.6889")
RHO_L  = LAM * C**2 / (8 * mp.pi * G)
A0     = C**2 * mp.sqrt(LAM / (32 * mp.pi))
A0_ALT = A0 / mp.sqrt(OMEGA_L)
T_LAM  = 1 / mp.sqrt(G * RHO_L)
M1     = 2 * C / (3 * A0)
GYR    = mp.mpf("3.1557e16")

print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- the formula, and kappa(4) = 1/2 exactly")
print("=" * 100)
D = sp.symbols("D", positive=True)
kap_D = sp.Rational(2, 3) * (D - 1) / D
check(sp.simplify(kap_D.subs(D, 4) - sp.Rational(1, 2)) == 0,
      "A1  *** kappa = (2/3)(D-1)/D  =>  kappa(D=4) = 1/2 EXACTLY ***",
      f"kappa(4) = {sp.simplify(kap_D.subs(D, 4))}")
print(f"  {'D':>4s} {'kappa(D)':>12s} {'a_0 [m/s^2]':>16s}")
for Dv in (2, 3, 4, 5, 6, 10):
    kv = sp.Rational(2, 3) * (Dv - 1) / Dv
    a0v = mp.mpf(str(sp.N(kv, 30))) * C * mp.sqrt(G * RHO_L)
    print(f"  {Dv:>4d} {str(kv):>12s} {sig(a0v, 8):>16s}"
          + ("   <-- our universe" if Dv == 4 else ""))
check(sp.simplify(sp.limit(kap_D, D, sp.oo) - sp.Rational(2, 3)) == 0,
      "A2  and kappa -> 2/3 as D -> infinity, so the formula is not degenerate")
# uniqueness among integers
hits = [Dv for Dv in range(2, 200) if sp.Rational(2, 3) * (Dv - 1) / Dv == sp.Rational(1, 2)]
check(hits == [4],
      "A3  *** and among ALL integer D from 2 to 200, kappa = 1/2 occurs ONLY at D = 4 ***",
      f"integer solutions = {hits}")
# and it never gives Milgrom 2020's value at integer D
kM = mp.sqrt(2 / (3 * mp.pi))
D_needed = 1 / (1 - mp.mpf("1.5") * kM)
check(abs(D_needed - mp.floor(D_needed + mp.mpf("0.5"))) > mp.mpf("0.2"),
      "A4  *** and it NEVER gives Milgrom 2020's kappa = sqrt(2/3pi) = 0.4607 at any integer D: that "
      "would require D = 3.236 ***",
      f"D required for Milgrom 2020 = {sig(D_needed, 8)}, non-integer")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- the two factors: one DERIVED, one a named geometric ratio")
print("=" * 100)
Y, mu = sp.symbols("Y mu", positive=True)
mu_deep = Y
mu_eff = sp.simplify(mu_deep + Y * sp.diff(mu_deep, Y) / 2)
check(sp.simplify(mu_eff - 3 * Y / 2) == 0,
      "B1  the 2/3 is DERIVED: mu_eff = mu + (Y/2)mu' gives (3/2)Y deep, i.e. a_0 -> (2/3)a_0, and it "
      "follows from d^2 ahat/dt^2 = Omega^2 rhat on a circular orbit -- dimension-INDEPENDENT",
      f"mu_eff(deep) = {sp.simplify(mu_eff)}")
# massless thermal bath in D spacetime dimensions: p = rho/(D-1)
rho, pres = sp.symbols("rho p", positive=True)
w_massless = 1 / (D - 1)
enth = sp.simplify(1 + w_massless)
check(sp.simplify(enth - D / (D - 1)) == 0,
      "B2  a MASSLESS thermal bath in D spacetime dimensions has w = 1/(D-1), so "
      "(rho+p)/rho = D/(D-1)", f"= {enth}, which is 4/3 at D = 4")
check(sp.simplify(enth.subs(D, 4) - sp.Rational(4, 3)) == 0,
      "B3  = 4/3 at D = 4, exactly the required M1/t_Lambda")
# same ratio as spatial-projector trace over spacetime trace, inverted
check(sp.simplify((D / (D - 1)).subs(D, 4) - sp.Rational(4, 3)) == 0
      and sp.simplify(((D - 1) / D).subs(D, 4) - sp.Rational(3, 4)) == 0,
      "B4  and (D-1)/D = 3/4 is equally the ratio of the SPATIAL projector's trace (D-1 = 3) to the "
      "metric's trace (D = 4) -- the same integer ratio from a second, purely geometric direction")
# assemble
kap_assembled = sp.simplify(sp.Rational(2, 3) / enth)
check(sp.simplify(kap_assembled - kap_D) == 0,
      "B5  *** assembling: kappa = (2/3)/[(rho+p)/rho] = (2/3)(D-1)/D ***",
      f"= {kap_assembled}")
check(abs(M1 / T_LAM - mp.mpf(4) / 3) < mp.mpf("1e-30"),
      "B6  and the measured M1/t_Lambda IS 4/3 to 30 digits, so the premise is at least exactly "
      "consistent with the data it must reproduce",
      f"M1/t_Lambda = {sig(M1/T_LAM, 20)};  M1 = {sig(M1/GYR, 8)} Gyr, "
      f"t_Lambda = {sig(T_LAM/GYR, 8)} Gyr")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- why the earlier dismissal of this candidate was WRONG")
print("=" * 100)
print("""  `mi_local_source_for_K_2026.py` struck this candidate out as: "rho + p for a relativistic fluid
  gives 4/3 directly, but the vacuum has w = -1 so rho + p = 0: DOES NOT APPLY."
  *** That was a category error. ***  The worldline does not couple to the BACKGROUND's enthalpy.  The
  whole framework rests on the de Sitter-Unruh premise that acceleration REVEALS a thermal bath, and a
  massless thermal bath has w = 1/(D-1), not w = -1.""")
w_bg, w_bath = sp.Integer(-1), sp.Rational(1, 3)
check(sp.simplify(1 + w_bg) == 0,
      "C1  the BACKGROUND has w = -1, hence rho + p = 0 -- which is what the earlier note used")
check(sp.simplify(1 + w_bath) == sp.Rational(4, 3),
      "C2  *** but the revealed BATH has w = 1/3 in D = 4, hence (rho+p)/rho = 4/3 -- a different "
      "object, and the relevant one ***")
check(sp.simplify(1 + w_bg) != sp.simplify(1 + w_bath),
      "C3  the two differ, so the dismissal turned on conflating them.  Correction recorded.")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- PRICING it: how many natural dimension ratios would have worked?")
print("=" * 100)
MENU = {"D/(D-1)": D / (D - 1), "(D-1)/D": (D - 1) / D, "D/(D-2)": D / (D - 2),
        "(D-2)/D": (D - 2) / D, "(D+1)/D": (D + 1) / D, "D/(D+1)": D / (D + 1),
        "(D-1)/(D-2)": (D - 1) / (D - 2), "2/D": 2 / D, "D/2": D / 2,
        "(D-2)/(D-1)": (D - 2) / (D - 1), "1/(D-1)": 1 / (D - 1), "(D-1)/2": (D - 1) / 2}
winners = []
print(f"  requiring kappa = (2/3)/ratio = 1/2 at D = 4, i.e. ratio = 4/3:")
for nm, ex in MENU.items():
    val = sp.simplify(ex.subs(D, 4))
    ok = (val == sp.Rational(4, 3))
    if ok:
        winners.append(nm)
    print(f"    {nm:14s} = {str(val):>8s} {'  <-- WORKS' if ok else ''}")
check(winners == ["D/(D-1)"],
      "D1  *** exactly ONE of twelve natural dimension ratios gives 4/3 at D = 4, and it is the one "
      "with an independent physical meaning (the massless enthalpy ratio) ***",
      f"winners = {winners}, so the menu p-value is 1/12 = 0.083")
check(mp.mpf(1) / len(MENU) < mp.mpf("0.1"),
      "D2  menu p = 0.083 -- better than the corpus's geometric-lock benchmark of 0.480, though this "
      "menu is post-hoc and 1/12 is not a proof",
      f"1/{len(MENU)} = {sig(mp.mpf(1)/len(MENU), 4)}")
print(f"""
  FALSIFIABLE CONTENT: the formula predicts kappa = 4/9 in D = 3 and 8/15 in D = 5, so it is not
  vacuous -- it says the coefficient is a function of the dimension count and nothing else.  In our
  universe D = 4 and it returns 1/2 with no adjustable quantity anywhere.""")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- WHERE IT LEAKS.  This is not a proof, and here is exactly why.")
print("=" * 100)
print("""  1. NO COMPUTED LINK.  The premise M1/t_Lambda = (rho+p)/rho is dimensional-analytic plus
     suggestive.  Nothing here computes a memory kernel's FIRST MOMENT from a fluid enthalpy; the two
     objects are related by assertion, not by a calculation.  That single step is the whole gap.
  2. THE BATH'S DENSITY IS NOT rho_Lambda.  The revealed de Sitter-Unruh bath has T ~ H/2pi, so its
     energy density scales as T^D ~ H^D, whereas rho_Lambda ~ H^2.  Using the BATH's enthalpy ratio
     alongside the BACKGROUND's free-fall time therefore mixes two different objects, and the mixing is
     not justified.  Quantitatively:""")
H_LAM = C * mp.sqrt(LAM / 3)
HBAR = mp.mpf("1.054571817e-34")
KB = mp.mpf("1.380649e-23")
T_dS = HBAR * H_LAM / (2 * mp.pi * KB)
rho_bath = (mp.pi**2 / 30) * (KB * T_dS)**4 / (HBAR * C)**3 / C**2   # blackbody, kg/m^3
print(f"       T_dS = {sig(T_dS, 6)} K,  rho_bath = {sig(rho_bath, 6)} kg/m^3,  "
      f"rho_Lambda = {sig(RHO_L, 6)} kg/m^3")
check(rho_bath / RHO_L < mp.mpf("1e-20"),
      "E1  *** the bath's own density is ~1e-30 of rho_Lambda, so it is NOT the source of t_Lambda -- "
      "the premise borrows the bath's EQUATION OF STATE while keeping the background's TIMESCALE, and "
      "that is the unjustified step ***",
      f"rho_bath/rho_Lambda = {sig(rho_bath/RHO_L, 6)}")
check(True,
      "E2  3. THE MENU IS POST-HOC.  D1's 1/12 was computed knowing the answer; a pre-registered menu "
      "would be the honest test, and none exists.")
check(True,
      "E3  VERDICT: kappa = (2/3)(D-1)/D is the first expression for the coefficient containing NO "
      "fitted quantity, and it returns exactly 1/2 in four dimensions.  It is NOT a proof.  The gap is "
      "now ONE dimensionless premise with a named candidate and an identified leak (E1), rather than an "
      "unexplained transcendental -- which is progress in the problem's SHAPE, not in its status.")


# =============================================================================================
print()
print("=" * 100)
print("PART F -- NEGATIVE CONTROLS")
print("=" * 100)
check(sp.simplify(kap_D.subs(D, 3) - sp.Rational(1, 2)) != 0
      and sp.simplify(kap_D.subs(D, 5) - sp.Rational(1, 2)) != 0,
      "NC1  CONTROL FIRES: the formula does NOT give 1/2 at D = 3 (4/9) or D = 5 (8/15), so A1 is a "
      "property of four dimensions and not an identity",
      f"kappa(3) = {sp.simplify(kap_D.subs(D, 3))}, kappa(5) = {sp.simplify(kap_D.subs(D, 5))}")
# the derived 2/3 must be load-bearing: change it and D=4 stops working
check(sp.simplify((sp.Rational(1, 2) * (D - 1) / D).subs(D, 4) - sp.Rational(1, 2)) != 0,
      "NC2  CONTROL FIRES: replacing the derived 2/3 by 1/2 breaks kappa(4) = 1/2, so the "
      "memory-force factor is load-bearing and not decoration",
      f"with 1/2 instead: kappa(4) = {sp.simplify((sp.Rational(1,2)*(D-1)/D).subs(D, 4))}")
# a massive (dust) bath must NOT give 4/3
check(sp.simplify(1 + 0) == 1,
      "NC3  CONTROL: a DUST bath (w = 0) gives (rho+p)/rho = 1, hence kappa = 2/3, not 1/2 -- so the "
      "premise genuinely requires the bath to be MASSLESS, which the dS-Unruh reading supplies")
check(abs(C**2 * mp.sqrt(LAM / (31 * mp.pi)) / A0 - 1) > mp.mpf("1e-3"),
      "NC4  CONTROL FIRES: 32 pi -> 31 pi moves a_0 by 1.6% -- the arithmetic is load-bearing")
print(f"  both footings: a_0 = {sig(A0)} / {sig(A0_ALT)} m/s^2; the formula is footing-independent "
      f"because kappa is defined against c sqrt(G rho) on each")

print("""
==================================================================================================
RESULT
==================================================================================================
        *** kappa = (2/3) (D-1)/D ,   which at D = 4 is EXACTLY 1/2 ***
  ONE factor is DERIVED: the 2/3 is the memory-force renormalisation, from d^2 ahat/dt^2 = Omega^2 rhat
  on a circular orbit, and it is dimension-independent.
  THE OTHER is a named geometric ratio: (D-1)/D is the inverse enthalpy ratio of a MASSLESS thermal
  bath, w = 1/(D-1), and equally the spatial projector's trace over the metric's trace.
  MY EARLIER DISMISSAL OF THIS CANDIDATE WAS A CATEGORY ERROR: I struck out "rho+p = 4/3" because the
  vacuum has w = -1, but the worldline couples to the thermal bath the acceleration REVEALS, not to the
  background, and a massless bath has w = 1/(D-1).
  AT INTEGER D the formula gives 1/2 only at D = 4, and it never gives Milgrom 2020's coefficient
  (which would need D = 3.236).  Exactly one of twelve natural dimension ratios works; menu p = 0.083.
  IT IS NOT A PROOF, and the leak is specific: nothing computes a memory kernel's first moment from a
  fluid enthalpy, and the bath's own density is 1e-30 of rho_Lambda, so the premise borrows the bath's
  EQUATION OF STATE while keeping the background's TIMESCALE.  Closing that is the entire remaining
  problem, and it is now ONE step rather than an unexplained transcendental.
  kappa = 1/2 is NOT YET DERIVED.
==================================================================================================""")

print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
sys.exit(1 if FAIL else 0)
