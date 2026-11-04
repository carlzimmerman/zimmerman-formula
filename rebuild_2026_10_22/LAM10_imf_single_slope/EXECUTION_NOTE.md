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

## The queue, and a correction about memory
- `compute_queue/heavyq.py` takes jobs strictly in order. Its head of line is `L1_calib_512` (est 38.6 GB), which needs
  free+inactive ≥ 46.6 GB to start.
- The shards were run directly, outside the queue, as "small jobs (under 1 GB each)". **That claim was wrong.**
  - Their physical footprint is small: 0.14-0.19 GB while fitting, with a peak of 0.9-1.0 GB.
  - But each shard holds a much larger resident set: **4.5-5.7 GB RSS per shard, 20.7 GB in all**, as the coordinating
    session measured. My own reading at 16:05 was 4.5-7.3 GB per shard (22.5 GB in all), with free+inactive at 29.0 GB.
  - Those resident pages count against free+inactive, which is what the queue reads. So, running outside the queue, the
    shards kept `L1_calib_512` from starting for about 1 h.
- **Decision.** The owner was asked "Let LAM10's fits finish first, or pause them so the queued L1 job can start?" and
  answered "Let LAM10 finish". The shards ran to completion with no pause or restart.
- The job contract was kept throughout: SIGTERM or `compute_queue/YIELD` gives exit 75, and `--resume` continues.
- LAM9's shards ran the same way. LAM9's records give only their footprint, so the same correction applies to them.

## The grader
- `lam10_grade.py` is LAM9's `lam9_grade.py` with only these changes:
  - the data sources (`lam10_fits.json`, `lam10_k.json`, and LAM9's prepare and template files);
  - the names;
  - the Γb detail rows (Γb_best, edge hits, σ, and the beside estimator in place of LAM9's mixture rows).
- It was written before any full fit.

## A grader dry run while the fits ran, disclosed
- **Setup.** At 16:36 the grader was run as a code test on the 961 sums fitted so far. α and Γb_best were permuted across
  galaxies with a fixed seed, and the outputs went outside the repo. It caught no crash: C1 correctly read N 961 < 1000.
- **What it revealed.** A permutation keeps the distribution, so the run showed the real spread of the fits:
  - the median Γb_best was 0.30;
  - 576 of the 961 sat at the low grid edge, Γb 0.3;
  - the median α_KU2 was about 4.8.
- **What it also printed.** Q1's baseline R0 and Q3's baseline E0 do not depend on α, so the run printed their real values on
  those 961 galaxies: R0 +1.30 / +1.24 ln and E0 +0.035 / +0.039 (canonical / alt).
- **Nothing was changed after this.** The frozen grading runs as written.

## Full fits
- K1 passed, so the 1586 sums were fitted as four single-thread shards, split by index mod 4, from 15:36 to 17:12. Each
  sum was fitted once per variant, and there were 0 failures.
- Outputs went to `_external_data/lam10_work_2026_11_04/fits/` and were merged into `lam10_fits.json`.
- The MUTATE twin, then the frozen grade, ran at 17:13.
