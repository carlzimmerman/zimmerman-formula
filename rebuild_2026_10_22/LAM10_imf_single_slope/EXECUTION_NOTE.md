# LAM10 execution note (not a method change)

κ = ½ FITTED; not theory closed. The criteria (e70770e272) are unedited. The scripts were committed before any fit
(009f39ec2f).

## A code test, disclosed (no real flux was fitted)
- **Setup.** Two single-template synthetics (10 Gyr, [M/H] +0.06, Γb 1.3 and 2.3), noiseless, on one sum's grid, masks and LSF.
- The profile's grid minimum fell on the input slope, and α came back exactly.
- The parabolic refinement, as frozen, put Γb_best at 1.212 and 2.259. The offset comes from the uneven grid spacing
  around those points.
- Each profile (13 slopes, one variant) took about 6 s.

## K1 and K2
- They ran from 15:02 to 15:35 on 2026-11-04 as four single-thread shards split by synthetic index, with `nice -n 10`.
- All 300 synthetics succeeded.
- LAM9's α_in was reproduced exactly (largest relative difference 0).

## The queue
- `compute_queue/heavyq.py` takes jobs strictly in order. Its head of line is a 38.6 GB job waiting for memory, and queueing
  this lane above it would hold that job back for hours.
- So the shards run directly as small jobs (under 1 GB each), with the job contract kept: SIGTERM or `compute_queue/YIELD`
  gives exit 75, and `--resume` continues.

## The grader
- `lam10_grade.py` is LAM9's `lam9_grade.py` with only these changes:
  - the data sources (`lam10_fits.json`, `lam10_k.json`, and LAM9's prepare and template files);
  - the names;
  - the Γb detail rows (Γb_best, edge hits, σ, and the beside estimator in place of LAM9's mixture rows).
- It was written before any full fit.

## Full fits
- K1 passed, so the 1586 sums are fitted as four single-thread shards, split by index mod 4. Each sum is fitted once per
  variant.
- Outputs go to `_external_data/lam10_work_2026_11_04/fits/` and are merged into `lam10_fits.json`.
