# RS3 AMENDMENT A1 (committed before any script exists or any number of this lane is computed)

Criteria 8158e4645f, section 7 KA4 (planted positive control). As frozen, KA4 plants y = 0.5 + 0.4 u - 0.3 v plus
noise drawn from the full covariance C, which includes a fully correlated per-class term. With that noise each of the
7 class means sits at z ~ N(0, 1) from the true surface, so even a perfect fit fails the per-class 2-sigma line with
probability about 1 - 0.95^7 = 0.30 per footing and family. KA4 would then test the luck of one seed, not whether the
machinery can say yes.

Change (pass/fail rule only; line, data, variables, MUTATE unchanged):
- KA4 (gating): the planted surface WITHOUT noise; the pair (g_N, Sigma_b) must CARRY in both families, both footings,
  and every leave-one-class-out refit. Failure -> NO VERDICT.
- KA4n (reported, no gate): the same plant with noise from C over seeds 1-20; the share of seeds that carry is
  reported per family and footing as the line's power at a true monotone surface.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
