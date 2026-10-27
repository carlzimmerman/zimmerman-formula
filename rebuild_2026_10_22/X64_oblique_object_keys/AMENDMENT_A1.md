# X64 AMENDMENT A1 — implementation fixes (post first run; check code only)

The first run printed candidate values and the separation results with K0 and K3 failing; its step-0 stop rule fired
(verdict UNDECIDED). Three bugs were in the check code, not in the physics. No candidate formula, label, interval rule,
trials rule, verdict rule or input changed. After the fixes the candidate tables and every separation status are the
same as in the first run.

1. **K0 CSV parsing.** X19's `x19_classes.csv` writes unavailable cells as the token `NA`. The step-0 parser accepted
   only empty, `nan` or `None`, so Groups (e, f_hot, kT) and UMa (ρ_env) were flagged as mismatches. `NA` is now
   accepted as "unavailable" (matching X19's `None` interval).
2. **K0 infinite Z.** The cosmic background's Z is +inf in both X19's table and the CSV. `|inf − inf|` is NaN, so the
   comparison failed. Exactly equal values (including equal infinities) now count as a match.
3. **K3 expected margin.** The synthetic separable table has max(hi, EXCLUDED) = 1 and min(lo, RETAIN) = 2, so the
   margin is 1.00 dex. The check's hard-coded 1.20 was wrong; the code's 1.00 was right.

With the fixes: K0 passes (1596 cells, 0 rows failing; X19 verdict and all statuses reproduced). Checks 7/7.
