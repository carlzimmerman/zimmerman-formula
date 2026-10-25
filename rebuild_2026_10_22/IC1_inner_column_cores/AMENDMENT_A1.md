# IC1 AMENDMENT A1 (pre-result: committed with the script, before any graded number)

These three clarifications make the frozen text match the committed code it says it executes. They do not change the rule,
the f range, the matching or the verdict classes.

1. **S0a reference files.** X40b's results JSON stores the X38-baseline *groups* line (`footings[f].X38_groups`). It does
   not store the s ≡ 1 SPARC and cluster numbers. X40b's own K0 compares those against X38's committed
   `x38_sd_halos_results.json`. S0a/K0 therefore checks:
   - SPARC rms and median Υ (both backgrounds) and all 30 cluster preds per footing against X38's committed JSON, which is
     X40b's K0 reference;
   - groups mean and Z against X40b's committed JSON.
   The tolerance is unchanged (1e-6). Rerunning the whole X40b script is replaced by executing its machinery read-only plus
   this check.
2. **No BCG in the lensing source.** The criteria's "+ CFG922 BCG, exactly as X40b" describes X40b's rule-A input g_b(r)
   only. In X40b's executed code, a rule that does not read g_b (its "one", B and C paths, and hence X38) adds no BCG to the
   lensing source. IC1 does not read g_b, so it follows that path. This is also what K0 (reproducing X38) requires.
3. **Cluster collapse mass.** "M = 6.364 M_b" is implemented exactly as X41's executed code: M = Mfair + M_b(grid end),
   from X30's `prep`.

Also disclosed, with no effect on grading: the groups estimator's ±0.01 dex finite-difference slope re-evaluates s at the
shifted M200. X40b's rule C does the same.
