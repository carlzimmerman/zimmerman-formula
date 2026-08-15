# INTERP 0004 -- seed_0004 deciphered

## Source bullets (charitable reading)
1. A polyhedral solid angle built from the two-footing fork
   (f_- = 9.3619e-11, f_+ = 1.1279e-10) might quantize the PMNS solar
   mixing tan^2(theta_12) = 0.307.
2. A saturation bound on the lepton mass ratio m_mu/m_e = 206.77
   may be the shadow (secondary feature / envelope) of the a0-bump
   cluster response, peaked at a0.
3. Wildcard: the ONE dimensionless number both bullets share.

## The one shared number (my committed conjecture)
The two footings are two branches of the same dimensional length, so the
ONLY fork-derived dimensionless quantity is the normalized "missing-cone"
solid angle

    s = 1 - f_-/f_+ = 0.16997     (equivalently Omega_f/4pi, Omega_f = 2.1359 sr)

with fork ratio r = f_+/f_- = 1.20478. Note the polyhedral solid angle of a
regular tetrahedron is 0.5513 sr -- numerically == kappa (fitted 0.551 +-0.043),
so "polyhedral solid angle" plausibly means the tetrahedral Omega = 0.5513,
which r feeds. The wildcard guess: both the PMNS angle and the mu/e saturation
are functions of the single number s = 0.16997 (the fork's solid-angle defect).
This is a CONJECTURE, not a result; it is very likely NULL/REFUTED.

## Falsifiable hypothesis (ONE test)
H: s = 0.16997 maps onto BOTH targets by one shared dimensionless relation,
i.e. there exist simple rationals q1,q2 such that
    tan^2(theta_12) = q1 * s     and     m_mu/m_e = q2 * s,
with |q_i| small (<= 3, integer or half-integer). Equivalently the single
number s is the common root; a hit requires the SAME s to serve both.

## Exact quantities
- s = 1 - 9.3619e-11 / 1.1279e-10 = 0.16997 (both footings used, dimensional
  numbers, per protocol).
- Target A: tan^2(theta_12) = 0.307.
- Target B: m_mu/m_e = 206.77.
- Reference polyhedral solid angle: tetrahedral 0.5513 sr (== kappa).

## Exact test
Run mm_search.py (it pre-registers FDR). Search small-integer rationals q
mapping s -> 0.307 and s -> 206.77. A genuine hit requires s to satisfy
BOTH mappings under the SAME q-convention; a match to only one target is
half a hit = NULL. Exclude CONVENTION-grade matches (do not count).
Report both footings on any dimensional figure.

## What kills it
- |q1*s - 0.307| > 1e-2 for all q1 in the search grid, OR
- |q2*s - 206.77| > 1e-2 for all q2 in the search grid, OR
- the only match is CONVENTION-grade / degenerate (q = trivial 1 or
  a pure unit re-scaling), OR
- the two targets require DIFFERENT s (relation is not common) -> NULL.
Any one of these = REFUTED/NULL = success. kappa stays fitted, not derived.

## Fidelity
Deciphered charitably; no self-test performed. Both footings on all
dimensional numbers. CONVENTION-grade excluded. Referee to run next session.
