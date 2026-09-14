# INTERP 0041 -- from SEED 0041 (random collision, charitable decipher)

## Hypothesis H41
The wide-binary band and the CKM CP phase are two independent projections of ONE
frozen dimensionless number, and that number is the **top-Yukawa coupling y_t ~ 0.70**.
Both bullets are routes that must land on the same y_t; the wildcard answer is y_t itself.

## Exact quantities
- Wide-binary band B = [B_lo, B_hi] = [1.1614, 1.1814] (frozen, dimensionless ratio).
  Midpoint phi_mid = 1.1714 rad.
- Top Yukawa target y_t = 0.70 (frozen; y_t(m_t) ~ 0.73, GUT ~0.65-0.70).
- CKM CP phase delta_CKM = 1.14 rad (PDG ~1.1439, i.e. ~65.3 deg).
- CKM mixing angles (the "structure"): theta12=0.1797, theta13=0.0148, theta23=0.4298 rad.

## Route A -- bullet 1 (polyhedral solid angle -> y_t)
Treat B as a polar-angle band on the unit sphere; its complementary-cap solid
angle as a fraction of the full sphere 4*pi is the "polyhedral solid angle"
map to the top Yukawa:
    y_t^A = (1 + cos(phi_mid))/2 = cos^2(phi_mid/2)  = solid angle of complement cap / 4*pi
phi_mid = 1.1714 -> y_t^A = (1 + 0.38938)/2 = 0.6947 ~ 0.70.
(This is a charitable proposal; a blind referee must recompute and judge it
against 0.70 -- not a pre-registered match.)

## Route B -- bullet 2 (CKM CP phase structural average, nu0-meter)
"Structural average of the CP phase" = the phase distributed over the CKM
3x3 structure, read in the conditional nu0-meter with DR4 as a charge gauge:
    y_t^B = <delta>_struct = (theta12 + theta13 + theta23 + delta_CKM)/4
         = (0.1797 + 0.0148 + 0.4298 + 1.1439)/4 = 0.4420  (charitable first guess).
Hypothesis: y_t^B must be re-derived by the nu0 charge-gauge procedure and land
on y_t ~ 0.70, NOT on this naive 0.442 (that value is flagged as likely WRONG,
forcing the referee to find the structure that actually reproduces y_t, or to
REFUTE the route).

## Wildcard (bullet 3): shared dimensionless number = y_t ~ 0.70
Both routes are independent (a spherical-cap solid angle vs a flavor-structure
average); agreement is non-trivial and not CONVENTION-grade (0.70 is not a
trivially recognizable constant of either route alone).

## Exact test
1. Compute y_t^A = cos^2(1.1714/2) and record it.
2. Compute y_t^B via the nu0-meter charge-gauge procedure (DR4); record it.
3. Compare: PASS iff |y_t^A - 0.70| <= 0.08 AND |y_t^B - 0.70| <= 0.08 AND
   |y_t^A - y_t^B| <= 0.08 (2-sigma at kappa-style 0.043).

## Kill condition (what refutes it)
- If |y_t^A - y_t^B| > 0.08 -> routes disagree -> REFUTED.
- If either route deviates > 0.08 from 0.70 -> REFUTED.
- If both hit 0.70 only by a CONVENTION-grade identity (0.70 read off trivially
  from one route) -> DISCARD.
- If y_t^B cannot be produced by the nu0 charge-gauge at all -> NULL.

## Footings
All quantities here are dimensionless (solid angles in sr, ratios, y_t, phases in
rad); the two a0 footings (9.3619e-11 / 1.1279e-10) do not enter -- N/A.

## Notes
Charitable decipher only. The naive y_t^B = 0.442 is a placeholder to force the
blind referee to search the structural average that (if it exists) lands on 0.70.
No claim that y_t or kappa is derived. To be tested by a separate blind session.
