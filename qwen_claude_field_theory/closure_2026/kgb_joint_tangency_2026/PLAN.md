# Constructive joint-preservation checkpoint

Base: `f109d3d8ce1cdab6b5f63bea75bca83a8d4798f9`.
Previous goal turn: **progress** (committed initial matched jets, exact next
compatibility equation, numerical obstructions and audited scale claim).
Full same-action gravity goal remains unchanged and unachieved.

This implements the already identified next step: solve shared-action
preservation and health together. It does not replace the target with a
pointwise certificate. Global a0, its fitted dark-energy relation, no particle
dark matter, one physical matter metric and an explicitly counted clock remain
the conventions. Full nonlinear constraints, PPN, measured G_N, source/lensing,
causality/strong coupling, FLRW, zero modes and CMB are still required.

## Constructive routes and ownership

- Root: generalize the previously fixed y1=.1 initial family and solve both
  lower-jet matching and next tangency; use controlled numerical precision,
  not an arbitrary optimizer success flag. Own root-level files.
- `derivatives/`: exact/analytic fast next-derivative evaluator, checked against
  independent mpmath and the original varied inverse. This makes joint
  equations practical to solve, not a new ansatz.
- `zero_braiding/`: construct the previously unsearched common Gamma=0 branch,
  where lower H matching need not hold and w can be positive. Derive its own
  preservation and health conditions rather than discarding it by old filters.
- `scaling/`: prove which parameter rescalings preserve matching/health, so
  searching an overall normalization is not mistaken for a new physical route.

## Execution contract

- [x] Reinspect current tree and base; retain unrelated dirty work.
- [x] Write failing tests for general parametrization and known matched control.
- [x] Implement general pair construction with regular field/coordinate guards.
- [x] Run initial-family continuation to locate joint-equation roots or a
  bracket; solver exceptions and small normalized residuals are not successes.
- [x] Use the independently checked derivative helper for joint solving.
- [x] For any regular joint root, refine at increased precision, re-evaluate
  original action jets, and require the *same* F_XX in both health intervals.
- [x] If that passes, immediately differentiate the next compatibility
  condition and attempt invariant radial continuation; do not announce closure.
- [x] Run each created entry point and relevant old-action tests; compile
  conditional Lean statements and record their actual hypotheses.
- [ ] Preserve verified evidence, review, and push only this checkpoint.

Initial computations are bounded individually (up to minutes, not an unlimited
scan); no arbitrary global stopping quota is imposed on the gravity goal.
The first discriminator is a genuinely joint seed, not more initial-only fits.
No broad exclusion follows from a failed solver or an unsearched branch.

Outcome: one joint root was refined at 60/80 digits, then rejected by its
actual local scalar principal and the following preservation condition.
No invariant radial continuation of a healthy seed was possible at that point.
The checked conditional scaling and zero-braiding reductions are retained.

User's later request adds a bounded deliverable: a Mac-local parallel,
resumable two-mode search with no model/API calls. Only a four-job smoke is
run here; no long background search is started. The full gravity goal remains
OPEN; the computational checkpoint is not its completion.
