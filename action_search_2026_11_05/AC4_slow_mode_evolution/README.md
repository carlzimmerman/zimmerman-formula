# AC4: AC3's slow modes evolved on their own background — NO VERDICT (and the test lacks power)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md, commit
a6c19b3845, frozen before any graded number. Script: evolve.py (0df9505ab8).

## Label: NO VERDICT

- **Main (81 cases):** no case amplifies beyond the GR control. max R = 1.0 over all cases
  (R = 1 means neither run grew past its start); witness max R = 0.305. Omega (symplectic
  product) conserved to 3.9e-11 everywhere; every integration reached a = e^5.
- **One witness misses the frozen convergence line:** (eps_phi 2, eps_m .9, Lstar .001, k 100),
  R = 0.30494 vs 0.30499 between rtol 1e-9 and 1e-11, beyond the frozen 1e-4. By the frozen rule
  that case is NO VERDICT, so the run is NO VERDICT. A separately labelled tolerance ladder
  (diag_tolerance.py, evidence_diag_tolerance.json; not graded) gives R = 0.30493-0.30499 over
  rtol 1e-9 to 1e-13 with no trend: a sampling floor of max-over-oscillation, not drift.
- **M1 (drop Kdot) bites:** Omega drift 0.057-0.72 on all 8 witnesses against the 1e-6 line.
  The conservation check catches a wrong equation.
- **M2 (flipped stiffness sign) does NOT bite:** max R 0.79; the candidate's amplitude barely
  changes (e.g. 2.52 -> 2.60). The criteria said this would be reported, not that it was a
  pass condition. **Consequence: on these backgrounds the graded quantity cannot tell a healthy
  stiffness from a flipped one, so even a clean R <= 10 would not have shown health.**

## Why the test has no power here

On the constant-V background the clock's rolling parameter falls as eps_phi ~ a^-6 (1e-11 by
about four e-folds). The clock's X goes to zero, the modes leave the horizon within one to two
e-folds, and the polarization term stops mattering before any slow growth could accumulate.
The GR control is itself ill-conditioned in the same limit (its zeta-gauge kinetic term K11 -> 0
and it grows at about +1.41 H), which is why R is small everywhere.

## What would decide it

A background on which the clock keeps rolling (X bounded away from zero over many e-folds),
for example a tracking potential, with the flipped-sign control required to bite before any
pass is read. That is also AC2's open X > 0 preservation obligation. Not attempted here.

## Files

FROZEN_CRITERIA.md; evolve.py; evidence/main, evidence/m1_drop_kdot, evidence/m2_flipped
(result.json each); evidence_*.log; diag_tolerance.py and evidence_diag_tolerance.json.
Numerics notes (no criteria change): Bdot - P and Kdot are simplified symbolically to cancel
large k^2 a terms; max_t is read from dense output, 8 points per step.
