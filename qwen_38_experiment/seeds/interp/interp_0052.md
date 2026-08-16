# INTERP 0052 -- charitable read of seed_0052 (random collision)

## Decipher
 (b1) polyhedral solid angle R_dm = 0.387 "bounds" the Koide relation Q_Koide = 2/3.
 (b2) a footing-invariant combination of the CKM CP phase delta_13 ~ 1.14 rad is the
       "shadow of the DBI wall".
 (wildcard) what single dimensionless number do BOTH share if true?
Charitable synthesis: two projections of ONE footing-invariant dimensionless number x*.
Near-coincidences in [0.33, 0.39]: delta_13/pi = 1.14/3.1416 = 0.363; R_dm = 0.387;
Koide gap 1 - 2/3 = 0.333.

## Hypothesis H0052
A single footing-invariant dimensionless number x* (declared ~= 0.38, NOT the fitted
kappa=1/2) such that:
 (A) R_dm = 0.387 is x* as a polyhedral solid angle, bounding the Koide coefficient via
     |R_dm - (1 - 2/3)| <= tol (R_dm pins the 1/3 gap).
 (B) the footing-invariant functional f(delta_13) = delta_13/pi equals the SAME x*
     (the "DBI wall shadow"): delta_13/pi = x* = R_dm.

## Exact test (mm_search.py, FDR pre-registered by the tool)
1. b2 family: {delta_13, delta_13/pi, delta_13 mod pi, sin(delta_13), cos(delta_13)},
   delta_13 = 1.14 rad.
2. b1 family: {R_dm, R_dm-(1-2/3), R_dm/(2/3), 1-R_dm, 2*R_dm}, R_dm = 0.387, Q_Koide = 2/3.
3. mm_search.py --custom: does any family(B) element coincide with any family(A) element
   within the O(1) prefactor window? Report FDR p-value; any k..2k-sigma NEAR-MISS band
   is DATA, not a hit.
4. Both footings (9.3619e-11 / 1.1279e-10): confirm zero footing-dependence (all three
   quantities are dimensionless -> invariance exact; a footing drift = bug).

## Kill criteria
- REFUTE: no (A,B) pair collapses to one x* within the 2x-FDR window, OR f(delta_13)!=R_dm
  beyond tolerance -> the two bullets share no number.
- DISCARD: the only match needs >= 2 free O(1) prefactors (a dial = p-hacking, PROTOCOL),
  or x* is forced to a fitted value not dimensionally anchored.
- CONVENTION-grade match = MISS, not a hit.
- If x* is forced to equal kappa=1/2 (fitted 0.551+/-0.043): record REFUTED/NULL, do NOT
  claim a derivation.

## Status
UNTESTED. A separate blind session referees this; not tested here.
