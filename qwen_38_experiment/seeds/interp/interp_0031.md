# INTERP 0031 -- one Koide fraction (charitable read of SEED 0031)

SEED: (1) a holonomy angle of the off-switch at recombination sets the CKM CP
       phase delta ~ 1.14 rad.
       (2) a footing-invariant combination of the Koide relation 2/3 interpolates
       to the a0-line g^2 - g_b^2 = a0*g_b.
       (3) wildcard: the single dimensionless number BOTH bullets share.

## Hypothesis (single sentence)
There is ONE dimensionless number -- the Koide fraction K = 2/3 -- that appears in
both bullets through the SAME footing-invariant combination: bullet 1 reads it off
the off-switch holonomy angle at recombination, bullet 2 reads it off the
footing-invariant form of the a0-line; one K serves both, two K's => REFUTED.

## Bullet 1 -- exact test
- Quantity: CKM CP phase delta_CKM (PDG central ~1.143 rad, sigma ~ 0.03 rad).
- Off-switch holonomy: Omega_off = integral of the connection around the
  recombination loop (z_r ~ 1089). Prediction: delta_CKM = (pi/2)*K with K = 2/3
  -> delta = pi/3 = 1.0472 rad.
- KILL: |1.143 - 1.0472| = 0.096 rad ~ 3.2 sigma > 2 sigma => bullet 1 REFUTED.
  (Honest expectation: this is a likely REFUTED; the offset is too large.)

## Bullet 2 -- exact test
- Quantity: a0-line 1 - r^2 = lambda*r with r = g_b/g, lambda = a0/g^2; solution
  r = (sqrt(lambda^2 + 4) - lambda)/2, r ~ 1 - lambda/2.
- Footing-invariant combination: the footing ratio rho = a0^(2)/a0^(1) =
  1.1279e-10 / 9.3619e-11 = 1.20478; define I(K) = K^(1/2) * rho^(1/4) and claim
  the footing-invariant a0-line ratio r_hat = 1/r equals I(K) numerically.
- Both footings: report r_hat at 9.3619e-11 AND at 1.1279e-10; require they agree
  (that is the whole point of "footing-invariant").
- KILL: if I(K) != r_hat to within the coupling error, OR the two footings give
  different r_hat, bullet 2 is REFUTED.

## Wildcard -- the shared number
Charitable candidate: K = 2/3 (lepton Koide) is the single shared number.
FLAGGED, NOT A HIT: a golden-ratio / rational coincidence is a CONVENTION-grade /
p-hacking risk per PROTOCOL; the rho^(1/4) footing-cancel and the (pi/2)*K map are
built from the targets, so any match is CONVENTION-grade and must NOT be counted as
confirmation. Falsifiable content: ONE K = 2/3 serves both bullets; a second
independent K => REFUTED.

## Overall
If K extracted from bullet 1 and from bullet 2 agree to their errors AND neither is
CONVENTION-grade -> PURSUE. If either bullet misses > 2 sigma -> REFUTED
(success). If the match holds only via target-built conventions -> CONVENTION/DISCARD.
HONESTY: kappa = 1/2 is FITTED (0.551 +/- 0.043), not derived; do not claim
otherwise. Searches go through mm_search.py (FDR self-registered); never count a
CONVENTION-grade match as a hit.
