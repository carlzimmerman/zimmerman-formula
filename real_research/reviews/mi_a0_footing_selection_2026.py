#!/usr/bin/env python3
r"""mi_a0_footing_selection_2026.py -- TWO INDEPENDENT ESTIMATORS BRACKET THE ALTERNATIVE FOOTING, AND THE
ALTERNATIVE FOOTING IS ALSO kappa = 1/2.

Two measurements landed within a day of each other, from different data cuts and different estimators:
  * SPARC profile likelihood, Upsilon free per galaxy  ->  a0_hat = 1.077e-10   (mi_a0_profile_likelihood_sparc_2026.py)
  * a0-LINE gas-dominated slope, GLS                   ->  a0_hat = 1.181e-10   (prep_2026/a0_line/averaging_floor.py)
Both run HIGH of the canonical 9.36e-11 -- by 15% and 26%. Read as a problem for the framework, that is a
coherent 1.6-2.4 sigma pull against its published number.

But the corpus's standing rule is to run BOTH FOOTINGS and show the spread, and the second footing is not a
different theory -- it is the SAME kappa = 1/2 with a different density and rate substituted:
    canonical    a0 = (c/2) sqrt(G rho_DE)      = cH_Lambda/Z    -> 9.36e-11
    alternative  a0 = (c/2) sqrt(G rho_total)   = cH_0/Z         -> 1.13e-10
So the question this script asks is NOT "is kappa = 1/2 right" but "WHICH FOOTING do the data pick, given
kappa = 1/2 either way" -- and whether the two estimators' pull is evidence about the footing rather than
evidence against the coefficient.

  F1  the two footings, derived from first principles, and the identity that makes them the same kappa
  F2  where the two independent estimators sit relative to each footing
  F3  is the ALT footing bracketed, and is that a coincidence? -- with a control that could say no
  F4  what this does and does NOT license

Exit 0 = ran and every internal check held. No hard-coded verdicts.
"""
from __future__ import annotations

import math
import sys

import sympy as sp

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 104)
    print(f"  {t}")
    print("=" * 104)


c = 2.99792458e8
G = 6.674e-11
H0 = 67.4 * 1000.0 / 3.0856775814913673e22        # Planck-like, s^-1
OM_L = 0.685
Z = math.sqrt(32.0 * math.pi / 3.0)


banner("F1  THE TWO FOOTINGS -- SAME kappa = 1/2, DIFFERENT DENSITY AND RATE")

# symbolic: a0 = kappa c sqrt(G rho) and the Friedmann conversion to a rate
kap, cs, Gs, rho, Hs = sp.symbols("kappa c G rho H", positive=True)
a0_dens = kap * cs * sp.sqrt(Gs * rho)
rho_from_H = 3 * Hs**2 / (8 * sp.pi * Gs)          # critical density at rate H
a0_rate = sp.simplify(a0_dens.subs(rho, rho_from_H))
Z_sym = sp.simplify(cs * Hs / a0_rate.subs(kap, sp.Rational(1, 2)))
print(f"  a0 = kappa c sqrt(G rho);  substituting rho = 3H^2/(8 pi G) gives a0 = {a0_rate}")
print(f"  at kappa = 1/2 this is a0 = cH/Z with Z = {Z_sym} = {float(Z_sym):.5f}")
check(sp.simplify(Z_sym - sp.sqrt(32 * sp.pi / 3)) == 0,
      f"F1a the density form and the rate form are the SAME statement: kappa = 1/2 <=> Z = sqrt(32pi/3) = "
      f"{float(Z_sym):.5f}. The 32pi/3 is the Einstein-coupling conversion and it CANCELS -- the content is "
      f"the single number kappa = 1/2, fitted, not derived")

H_LAM = H0 * math.sqrt(OM_L)                        # the pure-Lambda de Sitter rate
A0_CANON = c * H_LAM / Z
A0_ALT = c * H0 / Z
print(f"\n  canonical:   rho = rho_DE,    rate = H_Lambda = H0 sqrt(Om_L) = {H_LAM:.4e} s^-1")
print(f"               a0 = c H_Lambda / Z = {A0_CANON:.4e} m/s^2")
print(f"  alternative: rho = rho_total,  rate = H_0                       = {H0:.4e} s^-1")
print(f"               a0 = c H_0 / Z       = {A0_ALT:.4e} m/s^2")
print(f"  the footing fork is a factor {A0_ALT/A0_CANON:.4f} = {100*(A0_ALT/A0_CANON-1):.1f}%")
check(abs(A0_CANON - 9.36e-11) / 9.36e-11 < 0.01 and abs(A0_ALT - 1.13e-10) / 1.13e-10 < 0.015,
      f"F1b both footings reproduce the corpus's committed values from first principles: "
      f"{A0_CANON:.4e} vs the banked 9.36e-11, and {A0_ALT:.4e} vs the banked 1.13e-10. So this script is not "
      f"introducing a third convention -- it is using the corpus's own two")
check(abs(A0_ALT / A0_CANON - 1 / math.sqrt(OM_L)) < 1e-9,
      f"F1c and the fork is EXACTLY 1/sqrt(Om_L) = {1/math.sqrt(OM_L):.4f}: the two footings differ by one "
      f"factor of sqrt(Om_L) and nothing else, so the choice is purely 'which density does the horizon see'")


banner("F2  WHERE THE TWO INDEPENDENT ESTIMATORS SIT")

# both from committed scripts in this corpus, this week
EST = [
    ("SPARC profile likelihood, Upsilon free/galaxy", 1.0766e-10, 0.0544,
     "mi_a0_profile_likelihood_sparc_2026.py, Dchi2=1 with galaxy clustering"),
    ("a0-LINE gas-dominated slope, GLS",              1.181e-10,  0.13,
     "prep_2026/a0_line/averaging_floor.py, S6 at the 13% averaging floor"),
]
print(f"  {'estimator':<46}{'a0_hat':>11}{'sigma':>8}{'canon':>9}{'ALT':>9}")
print("  " + "-" * 84)
t_can, t_alt = [], []
for nm, ah, sg, src in EST:
    tc = (A0_CANON - ah) / (sg * ah)
    ta = (A0_ALT - ah) / (sg * ah)
    t_can.append(tc)
    t_alt.append(ta)
    print(f"  {nm:<46}{ah*1e10:>11.4f}{100*sg:>7.1f}%{tc:>+9.2f}{ta:>+9.2f}")
    print(f"       source: {src}")

# inverse-variance combine the two estimators (they use different data cuts and different estimators, so
# treating them as independent is the natural first pass -- F3 tests how much that assumption matters)
w = [1.0 / (sg * ah) ** 2 for nm, ah, sg, src in EST]
comb = sum(wi * ah for wi, (nm, ah, sg, src) in zip(w, EST)) / sum(w)
comb_sig = math.sqrt(1.0 / sum(w))
print(f"\n  inverse-variance combination: a0 = {comb:.4e} +- {comb_sig:.3e} ({100*comb_sig/comb:.1f}%)")
print(f"      canonical  9.36e-11 sits {(A0_CANON-comb)/comb_sig:+.2f} sigma")
print(f"      ALT        1.13e-10 sits {(A0_ALT-comb)/comb_sig:+.2f} sigma")
check(all(t < 0 for t in t_can),
      f"F2a both estimators sit ABOVE the canonical footing (t = {t_can[0]:+.2f}, {t_can[1]:+.2f}) -- the pull "
      f"is coherent in sign across two different data cuts, which is what makes it worth taking seriously "
      f"rather than dismissing as one noisy fit")
check(abs((A0_ALT - comb) / comb_sig) < abs((A0_CANON - comb) / comb_sig),
      f"F2b and the ALT footing is the CLOSER of the two to the combination: "
      f"{(A0_ALT-comb)/comb_sig:+.2f} sigma vs {(A0_CANON-comb)/comb_sig:+.2f} sigma. Neither is excluded, but "
      f"the data lean to rho_total/cH_0, not to rho_DE/cH_Lambda")


banner("F3  IS THE ALT FOOTING BRACKETED -- and could this test have said no?")

lo, hi = min(ah for nm, ah, sg, src in EST), max(ah for nm, ah, sg, src in EST)
bracket_alt = lo <= A0_ALT <= hi
bracket_can = lo <= A0_CANON <= hi
print(f"  the two estimators span [{lo*1e10:.4f}, {hi*1e10:.4f}] e-10")
print(f"      ALT       1.13e-10  bracketed: {bracket_alt}")
print(f"      canonical 9.36e-11  bracketed: {bracket_can}")
check(bracket_alt and not bracket_can,
      f"F3a *** THE TWO INDEPENDENT ESTIMATORS BRACKET THE ALTERNATIVE FOOTING AND BOTH LIE ABOVE THE "
      f"CANONICAL ONE. *** The ALT value 1.13e-10 falls inside [{lo*1e10:.3f}, {hi*1e10:.3f}]e-10; the "
      f"canonical 9.36e-11 falls below both")

# CONTROL: bracketing is cheap if the interval is wide. How wide is the interval compared to the fork?
frac_width = (hi - lo) / A0_ALT
fork = A0_ALT / A0_CANON - 1
print(f"\n  CONTROL -- is bracketing informative, or just a wide interval?")
print(f"      interval width          = {100*frac_width:.1f}% of the ALT value")
print(f"      the footing fork itself = {100*fork:.1f}%")
print(f"      ratio width/fork        = {frac_width/fork:.2f}")
check(frac_width < fork,
      f"F3b the bracket is INFORMATIVE, not automatic: the two estimators agree with each other to "
      f"{100*frac_width:.1f}%, which is TIGHTER than the {100*fork:.1f}% footing fork they are being asked to "
      f"resolve ({frac_width/fork:.2f}x). Had the estimators disagreed by more than the fork, bracketing "
      f"either footing would have been meaningless and this check would FAIL")

# and the honest counterweight: is standard MOND's g_dagger even better fit than either footing?
G_DAG = 1.20e-10
print(f"\n  COUNTERWEIGHT -- the empirical standard-MOND g_dagger = {G_DAG:.2e}:")
print(f"      sits {(G_DAG-comb)/comb_sig:+.2f} sigma from the combination")
better_than_alt = abs(G_DAG - comb) < abs(A0_ALT - comb)
check(not better_than_alt,
      f"F3c stated against interest: the purely EMPIRICAL g_dagger = 1.20e-10 sits "
      f"{(G_DAG-comb)/comb_sig:+.2f} sigma from the combination, "
      f"worse than the ALT footing's {(A0_ALT-comb)/comb_sig:+.2f} sigma. That is the ONE genuinely "
      f"favourable thing here and it is weak: the horizon-derived ALT value fits better than the fitted "
      f"g_dagger, but only because the estimators land near 1.1e-10 and every MOND-family value is near "
      f"there too. If this check ever FAILS, the wording above must be rewritten, not the check")


banner("F4  WHAT THIS LICENSES, AND WHAT IT DOES NOT")

print(f"""  *** THE PULL IS ABOUT THE FOOTING, NOT ABOUT kappa. *** This is the single most useful thing here, and
  it reframes a result that looked bad for the framework:
   * BOTH footings are kappa = 1/2. They differ by exactly one factor of sqrt(Om_L) = {math.sqrt(OM_L):.4f} (F1c) --
     i.e. purely by which density the horizon is taken to see, rho_DE or rho_total. Nothing about the
     coefficient changes between them.
   * Two independent estimators -- different data cuts, different estimators, different systematics -- agree
     to {100*frac_width:.1f}% and BRACKET the ALT footing while both sitting above the canonical one (F3a).
   * The bracket is informative rather than automatic: the estimators agree more tightly than the fork they
     are resolving ({frac_width/fork:.2f}x, F3b).
  So "a0 runs 15-26% high of 9.36e-11" is NOT evidence against kappa = 1/2. It is evidence about which
  footing to publish, and the corpus already carries both.

  WHAT THIS DOES NOT LICENSE, and these matter:
   * It does NOT show a horizon-derived a0 beats a fitted one. The empirical g_dagger = 1.20e-10 sits
     {(G_DAG-comb)/comb_sig:+.2f} sigma from the combination, {'BETTER than' if better_than_alt else 'not better than'} the ALT footing (F3c). These
     estimators say "the scale is near 1.1e-10", which every MOND-family value already says.
   * It does NOT make the ALT footing correct. The canonical footing is not excluded -- it sits
     {(A0_CANON-comb)/comb_sig:+.2f} sigma from the combination, which is a lean, not a kill.
   * The two estimators are NOT fully independent: both use SPARC galaxies, and the a0-line's gas-dominated
     subsample is a subset of the profile likelihood's 175. Treating them as independent OVERSTATES the
     combined precision. The bracketing result (F3a) does not depend on that assumption; the {100*comb_sig/comb:.1f}%
     combined error bar does, and should be treated as a floor-violating optimism.
   * The a0-line's own 13% floor CANNOT be beaten by more galaxies (averaging_floor.py: N=2000 still leaves
     12.8%), so this fork will not be resolved by sample size on that estimator.

  WHAT WOULD SETTLE IT: the two footings differ by sqrt(Om_L), so anything that measures a0 to better than
  ~10% with a systematic budget that is not shared between the two estimators decides it. The profile
  likelihood's {100*0.0544:.1f}% is already there on paper -- but it is forecast-grade, because it has no distance or
  inclination error treatment. Adding that treatment is the concrete next step, and it is the same script.""")

banner("RESULT")
n = sum(1 for x, _ in ok if x)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for x, m in ok:
        if not x:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: the high-a0 pull is a FOOTING question, both footings are kappa=1/2, and the ALT is bracketed.")
