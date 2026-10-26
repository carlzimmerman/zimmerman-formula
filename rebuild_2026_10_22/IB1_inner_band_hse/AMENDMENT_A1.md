# IB1 AMENDMENT A1 (POST-RESULT; check implementation only; committed alone before the rerun)

Run 1 (`ib1_hse_halo_run1_K1FAIL.out`) failed K1 at the 99th-percentile-kT cluster with `nan`. The failure is in the
check, not the model. That cluster's 2.0 R500 lies beyond the record's 3 Mpc gas cut, so the numeric side took the log of
zero density.

K1's window becomes r ∈ [0.05, min(2.0 R500, 2.9 Mpc)]. That stays inside the β-model part, where the frozen intent put
it. The tolerance (1e-5), the five test clusters and MUTATE are unchanged. No model line, cell, class or reported item
changes. Run 1's graded numbers stay on the record as they ran.
