# RRL3R AMENDMENT A1 (2026-11-14): KA-5's planted broken profile judged over 40 seeds, not one

Written and committed alone, after run 1 and before any word, f value or density-based prediction of this lane was
computed. Run 1 stopped at KA-5, so no primary, twin, bracket or word number exists yet.

## As-frozen reading (reported first, always)

Run 1 (`rrl3r_run1_ASFROZEN_KA5_FAIL.out`, commit 929d8af29b): KA-5's planted broken mock (3 / 5 / 35, seed 331103)
gave a_out = 4.7448 +/- 0.0820, 3.1 sigma below 5.0. a_in (3.044 +/- 0.117), rb (33.52 +/- 0.86) and the break
detection passed. Under the frozen rule the reading is **NO VERDICT (KNOWN ANSWER) for every case on both footings**.

## Why a fail is checked (verify a fail as hard as a pass)

`rrl3r_ka5_check.py` (same code, run 1's machinery) drew 40 further planted mocks of each kind:
- single a = 4.5: mean 4.5026, pull mean +0.07, pull sd 0.91, |pull| > 2 in 3 of 40;
- broken 3 / 5 / 35: a_out mean 5.037, pull mean +0.32, pull sd 0.95, no |pull| > 2; a_in pull mean +0.15, sd 0.88;
  rb pull mean +0.23, sd 0.86; all three tests pass in 40 of 40 seeds.
The fit is unbiased and its errors are right in size. Seed 331103 is a fluctuation of about 3 sigma.
The thresholds below were chosen after this diagnostic was seen (disclosed); they concern the machinery only, and no
number of the gate itself had been computed.

## The change

KA-5's broken-mock parameter test becomes: over the 40 seeds 331800 + k (k = 0..39), for each of a_in, a_out and rb,
|mean pull| <= 0.5 and pull sd between 0.6 and 1.4, and at least 34 of 40 seeds pass all three of the frozen
per-seed tests. Seed 331103 is still run and printed (as frozen, reported, not gating). Break detection on seed 331103
and the single-law part of KA-5 stay as frozen. Nothing else changes.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
