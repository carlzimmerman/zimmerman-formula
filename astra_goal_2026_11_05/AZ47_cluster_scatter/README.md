# IN PROGRESS — scatter measured; saved-candidate pilot regraded

Kappa=1/2 FITTED; not theory closed. No BK2 search or source file changed.
Protocol75abae6f8b preceded measurement; criteria774bb8db44 froze the
measured covariance before candidate evaluation. Amendment b06499a5dc
corrects a verbal inequality typo before candidate results.

Four train clusters give mass-ratio scatter0.0680,0.0764,0.0785,0.1059,
0.0669dex at x=.1,.2,.3,.5,.7. Three holdout clusters were not used to
choose it. The empirical covariance is rank3 with radial correlations
0.632–0.997. Noise subtraction produces four negative eigenvalues; PSD
projection retains one positive mode. This intrinsic estimate is an
assumption conditioned on a very small sample and unknown measurement
covariances, not a precise population covariance. All10 measurement,
known-answer and40/80-digit precision checks pass. Full matrices and
leave-one-out sensitivity are in scatter.json, hash frozen in criteria.

## Saved stage2 pilot, not the full retained-hit census

All50 archived near misses per row below were evaluated. Counts are
conditional G3 bookkeeping flags only; none is a newly validated BK2
survivor. Original G3 ERR passes are0 in every row.

| Set | Footing | Diagonal inflation | Full covariance | Stable under all leave-one-out covariances |
|---|---|---:|---:|---:|
| L1 real | canonical |33|21|11|
| L2 real | canonical |47|27|26|
| L1 real | alt |30|16|9|
| L2 real | alt |50|24|24|
| L1 scrambled | canonical |19|0|0|
| L2 scrambled | canonical |25|0|0|
| L1 scrambled | alt |25|0|0|
| L2 scrambled | alt |25|0|0|

This difference is why radial covariance cannot be replaced by five
independent extra error bars. The zero-covariance mutation changes88
real-candidate conditional flags and none of the scrambled controls.
The synthetic mutation also bites. All824 pilot checks pass, including
exact-old-footing archive anchors, zero-covariance recovery, independent
dense/block calculations and40/80-digit matrix comparisons for the law
and a near miss on each footing. The new canonical grade uses9.3603e-11;
archive anchors retain BK2's9.360324825027975e-11. Output trees are separate.

The pilot took0.62seconds and66MB RSS. This does not establish the full
streaming census performance. The local retained hits span L1/L2, both
footings and real/control sets; their complete processing, chunk1000/2000
pairs, same-size repeat and full aggregate report remain outstanding.
The old prefilter omitted other grammar expressions, so even the full
retained-hit census cannot retroactively prove a new whole-search count.

Calibrated population-level G3 inference remains NO VERDICT: the frozen
Gaussian covariance assumption, finite-sample covariance estimate,
unknown radial measurement errors and original candidate selection do
not make Z_cov an established standard-normal statistic. The pilot says
how the bookkeeping changes, not that the underlying laws are validated.

## Reproduce

Use the existing conda environment with numpy, scipy, astropy and mpmath.
From the repository root:

    python astra_goal_2026_11_05/AZ47_cluster_scatter/measure.py
    python astra_goal_2026_11_05/AZ47_cluster_scatter/pilot.py

Both exit0 for these recorded checks. measure.py regenerates the frozen
scientific scatter JSON deterministically in the recorded environment;
g3.py refuses a mismatching hash. Source hashes and versions are recorded.
No downloads, publications, messages or pushes occurred.
