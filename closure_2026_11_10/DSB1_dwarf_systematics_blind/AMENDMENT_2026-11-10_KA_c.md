# DSB1 amendment 2026-11-10: KA-c re-specified (post-freeze; committed alone before any graded number)

Post-freeze. Written after the frozen run stopped at KA-c (RESULT_BLIND.md, commit 8e189b5326) and before any class residual
of the real data was computed. RB2's and DG1's results are still unopened. The frozen reading (STOPPED AT KA-c, no label)
stands and is reported first; this file defines a second, amended reading.

## Why

KA-c as frozen asked that a mock built at the nominal data side with every row at B x 10^0.40 be recovered within 0.10 dex
with the full budget on. The budget contains a term that is one-sided by its frozen prior (T10, Minor+2010 binary inflation
U[0, 0.30] for 4-10 km/s systems): it moves a class centre by its mean effect, by design. A mock that does not contain that
inflation cannot be recovered at its planted value. The check was mis-specified; the pipeline is not wrong there. The
second cause (Coma, T8 symmetric in sigma under a mean of log sigma^2: Jensen bias -0.06 dex) is a property of the frozen
pipeline and is kept in the graded reading; it is disclosed and a reported-only variant removes it.

## Amended known answer KA-c' (replaces KA-c's recovery line; its limit and budget-off parts unchanged)

- Differential recovery: for every graded class and footing, |rec(+0.40) - rec(0) - 0.40| <= 0.10 dex, rec(delta) the full-
  budget class residual of the planted mock (N 1,000, the frozen KA-c seeds; rec(0) with the same seed). This tests that the
  pipeline returns a planted offset on top of the budget's own centre shift.
- rec(0), the budget's own null shift, is reported beside every graded class residual with its per-term decomposition.

## Grading under the amendment

Unchanged from FROZEN_CRITERIA.md sections 2-6 (budget, statistic, power rule, labels, lane label, mutations). Reported
beside, not graded: Coma UDGs with T8 drawn symmetric in log sigma (log10 sigma ~ N(log10 sigma_obs, esig / (sigma ln 10)),
absolute value not needed), which removes the Jensen shift; its label is reported, never substituted.

Outputs of the amended reading go to dsb1_amended.json / .out (and dsb1_MUTATE.* for the mutations); the frozen outputs
dsb1.json / .out stay as committed.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
