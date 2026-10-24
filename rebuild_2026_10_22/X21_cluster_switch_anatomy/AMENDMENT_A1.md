# X21 AMENDMENT A1 (after step 0 of RUN1, before any graded number)

**What happened.** RUN1 (`x21_switch_anatomy_RUN1_K0.out` / `_results_RUN1_K0.json`, kept) stopped at the frozen step-0 rule:
K0 FAILED at max |dev| 7.7e-4 (line 1e-9). Every A and A_CAL (all, terciles, quintiles) and the all-cluster σ_STAT matched X7 to
≤ 2e-16, X13's all-source A and Z_STAT to 1.8e-15, and S0-b's Δχ² to 0.006. Only the per-bin σ_STAT differed (1e-5 to 8e-4).

**Cause (implementation, not data).** X7's `summ` computes σ_boot and σ_jk on the *uncalibrated* numerator Σ W B D (`nm["t"]`);
A_CAL then subtracts the leakage offset. RUN1's per-bin rows bootstrapped the leak-subtracted numerator. The all-cluster line
already used the uncalibrated numerator, which is why it matched exactly.

**Change.** The binned rows (step 0 and the reported binned tables) take σ_STAT from the uncalibrated numerator, as X7 does.
Nothing else changes. The graded unbinned tests (§3) keep σ from the statistic actually fitted (leak-subtracted n_i), as frozen.
No graded test, binned table, or budget number had been computed when this was written (RUN1 stopped at step 0).
