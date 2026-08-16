# INTERP 0020 -- deciphered from seed_0020 (random collision)

## Reading
The seed collides two loose bullets plus a wildcard:
- (a) a kappa-duality (kappa = 0.551 +/- 0.043, FITTED not derived) "selects" m_mu/m_e = 206.77.
- (b) the continued fraction of m_W/m_Z = 0.8814 interpolates a transition z_t = nu0^(-1/3) - 1 in [17,35].
- wildcard: ONE dimensionless number shared by both, if true.

## Hypothesis (single, concrete, falsifiable)
There is ONE dimensionless number x that is simultaneously:
  - the partial-quotient x_k of the simple continued fraction [0; q1, q2, ...] of r_WZ = m_W/m_Z = 0.8814, AND
  - the argument of the kappa-duality map f that yields the lepton ratio, m_mu/m_e = f(kappa, x_k).
i.e. the SAME x_k that appears in the CF of r_WZ is the selection parameter that, with kappa, gives 206.77.
This is the "shared number" of the wildcard; it makes the two bullets one claim, not two.

## Exact quantities / test (what a later session runs)
1. Build CF of r_WZ = 0.8814: q1 = floor(1/0.8814) = 1; r1 = 1/0.8814 - 1 = 0.13456; q2 = floor(1/0.13456) = 7; r2 = ...
2. For each partial quotient x_k (k = 1..5), evaluate the kappa-duality map f(kappa, x_k) and check
   |f(kappa, x_k) - 206.77| <= 1 sigma of the target's measurement error.
3. Kill-test on bullet (b): the SAME x_k must equal z_t + 1 = nu0^(-1/3) for some nu0 giving z_t in [17,35];
   equivalently x_k - 1 must lie in [16,34]. If x_k falls outside [16,34], the interpolation fails.

## What kills it (pre-stated)
- REFUTED: no partial quotient x_k of r_WZ satisfies BOTH the m_mu/m_e target (step 2) AND the
  [16,34] interpolation window (step 3) within stated tolerances.
- NULL: x_k matches one bullet but not the other (no single shared number).
- CONVENTION-grade coincidence (matches only after an ad-hoc choice of k or of f) is NOT a hit.
- A single tuned k reproducing 206.77 by fiat = p-hacking, treated as DISCARD.

## Footings / honesty notes
- All quantities here are DIMENSIONLESS (kappa, m_mu/m_e, m_W/m_Z, z_t); the dual-footing rule
  (9.3619e-11 / 1.1279e-10) does NOT apply.
- kappa = 0.551 +/- 0.043 is reported as FITTED; this interp does NOT claim kappa = 1/2 is derived.
- This is a random-collision seed; prior expectation is NULL/DISCARD. The unifying-claim
  (one x_k serving both bullets) is what must be checked; two independent coincidences are not one.
- nu0 is undefined in the seed; the test treats nu0 as the (unknown) free param constrained only by
  z_t in [17,35]. If nu0 must be fixed by data, that is an ESCALATE item.
