# X21 AMENDMENT A2 (POST-RESULT, check code only)

**What happened.** RUN2 (`x21_switch_anatomy_RUN2_K3.out` / `_results_RUN2_K3.json`, kept) passed K0, K1, K2, K4 and failed K3
with value `nan`. All results had been printed when this was found.

**Cause.** K3's λ = 0 leg divides by each cluster's MID model sum d_i. 14 of the 326 clusters have no MID weight
(E ≥ 1e8 in all three MID bins), so d_i = 0 exactly and 0/0 = nan. The solver leg (|model sum − target| at the solved λ) was
finite; `max` of a list containing nan returned nan.

**Change.** The λ = 0 leg compares relative differences where d_i > 0 and absolute differences where d_i = 0. The threshold
(≤ 1e-4) is unchanged. No statistic, class or verdict depends on K3's code; every result line of RUN2 must reproduce in the
final run (checked by diff, reported in the README).
