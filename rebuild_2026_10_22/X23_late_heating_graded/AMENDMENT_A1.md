# X23 AMENDMENT A1 (POST-RESULT, disclosed)

RUN1 (`x23_late_heating_graded_RUN1.out` / `_results_RUN1.json`) is kept as run.

1. **Check code only (K0).** RUN1 compared both footings' NONE sets with X19's canonical list. X19's printed alt set adds
   Antlia II (`x19_selector_rank_test.out` line 135), so K0 failed on a hard-coded list. The list is now per footing.
   No graded number changes: RUN1 and the rerun print identical class lines.
2. **Reported-only label reading.** The frozen rule grades |E_obs − E_pred|/s < 2. That rule marks every NONE class with
   E_obs < 0 (SPARC, MW disc, UMa, TDGs, DF2/DF4, Crater II) as OVER, even where late heating adds ≈ 0 dex. Those
   residuals are the isolated law's own, not late heating's, so the frozen rule cannot tell model failure from baseline
   failure on those rows. It is also why the footings "disagree" (only SPARC small, Z_res −1.71 vs −2.60). A1 adds a
   label-level reading: L_pred = X19's L-S label applied to Z_pred = E_pred/s, compared with the X19 label for every
   decisive class. **The frozen verdict is unchanged and printed first.** A1 has no verdict weight.
