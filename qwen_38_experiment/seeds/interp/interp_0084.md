# interp_0084 -- charitable decipher of seed_0084

## Seed (random collision)
1. "torsion of the a0-line g^2 - g_b^2 = a0*gb might set the Koide relation (2/3)."
2. "an entropy partition of the top Yukawa (~0.70) could be measured by the two-footing fork (9.3619e-11 vs 1.1279e-10)."
3. wildcard: "what single dimensionless number would BOTH bullets share if true?"

## Charitable reading -> ONE falsifiable hypothesis H

Two-footing ratio (the only concrete number the seed hands over):
  rho = a0_alt / a0_can = 1.1279e-10 / 9.3619e-11 = 1.2048.
Both footings stated: 9.3619e-11 (canonical) and 1.1279e-10 (alt). H uses rho, the
ratio, so it is footing-independent.

**Shared number.** The single dimensionless number both bullets share is rho = 1.2048:
- Bullet 1: the "torsion" T of the a0-line g^2 - g_b^2 = a0*g_b is a computable
  curve-geometry invariant; H claims T is a named function of rho, T = tau(rho), and
  tau(1.2048) = 2/3 (the Koide Q of the three neutrino masses).
- Bullet 2: the top Yukawa yt ~= 0.70 is the "entropy partition" produced by the fork;
  H claims yt = psi(rho) for the SAME principled map, i.e. yt and Q are two views of rho.

Concretely, H asserts ONE named, un-fitted function F of rho that returns BOTH
F(rho)=2/3 (Koide) and F(rho)=0.70 (top Yukawa) -- the wildcard's "single number."
Because 2/3 != 0.70, the shared object must be rho itself, with 2/3 and 0.70 being two
derived projections; H must name them.

## Exact test
- A (Koide / torsion): compute the torsion T of the a0-line at rho, require
  |T - 2/3| <= 0.02 (2/3 = 0.6667 +- 0.02; tolerance chosen ~2x the fitted-kappa
  0.043 spread, generous but non-trivial).
- B (top Yukawa): require the two-footing partition of yt to land
  |yt_hat - 0.70| <= 0.04 (yt = 0.656 +- 0.005 measured; 0.04 is a loose outer bound).
- W (wildcard / unification): the SAME rho = 1.2048 must feed BOTH A and B through
  named maps (no new fit parameter). Report whether one rho yields both.

## What kills it
- If T != 2/3 within 0.02  -> bullet 1 REFUTED.
- If yt_hat != 0.70 within 0.04 -> bullet 2 REFUTED.
- If no single named function of rho gives both 2/3 and 0.70 -> wildcard REFUTED.
- Any free parameter tuned to hit a number = p-hacking = DISCARD (CONVENTION-grade only).

## Honest prior
This is a random collision; expect REFUTED/NULL/DISCARD unless a named map of the
single ratio rho 1.2048 genuinely reproduces both 2/3 and 0.70. Both footings used;
no kappa=1/2 claim; searches (if any) via mm_search.py with its own FDR.
