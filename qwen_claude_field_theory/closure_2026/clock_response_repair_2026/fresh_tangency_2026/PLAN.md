# Fresh-state metric evolution consistency

Base `67c9ceaa8`; previous goal turn made progress (committed action-derived
density-gap calculation and conditional Lean bounds). Full same-action MOND
gravity closure remains the target, not numerical convergence alone.

The existing global tangency measurements use states evolved before the
center mixed-derivative repair. First discriminator: freshly evolve the
unchanged action and the current solver, then differentiate its radial
constraint projection independently. Do not reinterpret an old-state failure
as evidence that the repaired evolution fails in the same way.

Routes, in order:

1. Fresh-state refinement, 65/129/257 points, t=.02, dt=.00025, the original
   amplitude=.02, width=.3, outer=3, gamma=1e-6. Compute full r<2.8 metric
   tangency errors, including the center. This distinguishes historical-state
   contamination from a persisting defect; numerical success is not PDE proof.
2. If the defect persists, compare spline and finite-difference spatial jets
   on those fresh states, and test local mixed-derivative consistency. No
   coefficient changes or filters chosen to reduce a physical residual.
3. If spatial jets are consistent, isolate radial ODE tolerance, startup, and
   time-step effects, separately. No late-time force claim until these checks
   support metric-evolution consistency.

Run each individual computation within 600 s with cooperative one-thread
numerical-library limits, retain fresh states and actual errors. No new empirical
data, observational prediction, full stability proof, or Lean closure is implied.

Lean is reserved for a substantive exact identity if this investigation yields
one; it cannot certify a convergence rate from three sampled mesh sizes.
