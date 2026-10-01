# Original XR22 statistics resource assessment

Decision: allow the unmodified statistics mutation/main runs after the force run; no sequential-bootstrap substitution is needed for the reported ~64 GiB machine with the bounded concurrent queue.

Inspected paths: `XR22_common.RegisteredEstimator`, `.fit`, `frozen_gate_inject1`, `run_estimator_direct`; `XR22_prereg_statistic.main`, `sepbins`, ladder, and resolved Galileon comparison; frozen pipeline `make_population`, `bin_medians`, `model_medians`.

The main estimator allocates bootstrap matrices for one acceleration bin at a time. The largest banked actual count is 218,384 and boot=300. One int64 index or float64 sample matrix is 0.4881 GiB; allowing an extra median/partition copy gives about 1.4644 GiB of dominant matrix storage. Selected-population vectors, coordinate temporaries and the model grids add memory, but no per-law copy of the full bootstrap matrix is retained. `RES` stores fitted summaries, not each full sampled population.

The largest separation bin is 193,127 with boot=100: one matrix is .1439 GiB, or .4317 GiB allowing three. The 3,000,000-pair frozen gate master uses boot=100 for model medians, in a single short-lived child process whose memory is released when it exits. The parent retains its two selected estimator populations; it does not retain the child's full generation temporaries. Galileon `resolved` computes an analytic median standard-error approximation rather than a bootstrap matrix.

As a deliberately loose structural comparison, putting all 1,500,000 generator draws in a single boot=300 bin would use 10.06 GiB for three matrices; putting all 3,000,000 gate draws in one boot=100 bin would use 6.71 GiB for three matrices. These extremes do not occur in the selected sample and are not measured whole-process bounds. Population generation and retained arrays must still be added. Actual source documentation reports about 5 GB for the statistics lane, consistent with the code's several-GiB scale. The new sequential-bootstrap 1.5M-draw audit measured .998 GiB peak RSS, but that is not claimed as the original estimator's peak.

Banked runtime: statistics mutation 440.2604 seconds; main 470.2702 seconds, about 15 minutes sequentially. Both use the original sample counts and statistic. The force pool ends before the wrapper launches statistics; at most the one frozen-gate child coexists with the statistics parent. Runtime and actual numerical comparisons are recorded by `full_reproduction.py`; no hard RSS cap or measured original-run peak is asserted by this assessment.
