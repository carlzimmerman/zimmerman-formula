# X19 AMENDMENT A2 (POST-RESULT; implementation of the step-0 checks only; no threshold, label rule, class, candidate or verdict line changed)

The first committed-path run (not committed; its .out was overwritten) printed **K0 FAIL, 3 mismatches** and therefore fired the
§6 stop rule (> 2 rows), and **K1 FAIL** on five X1 median cells. Both came from the check code, not from the record:

1. **Groups (K0).** The record prints the groups' offset in log σ (+0.010 / −0.010, P4 README T3). The script doubled it to dex in g
   (as frozen) but kept the single-digit tolerance (0.0005) on the doubled value, so −0.0205 vs −0.020 failed. The comparison is now made
   in the record's own unit (E/2 vs ±0.010, tolerance 0.0005). The E used everywhere is unchanged.
2. **Crater II and Antlia II (K0).** §6 says the JSON value is compared with "the printed value in the lane's .out / README". The script
   compared with the per-system CSV instead (alt differs from the bootstrap median by 0.005 and 0.001 dex). The references are now
   parsed from X1's printed class lines (`x1_hosted_recount.out`, "iso ±0.xx", all seven X1 classes, both footings). All match.
3. **X1 plain vs bootstrap medians (K1).** §6 lists this comparison as "reported"; §8 K1 did not exclude it. The record's class value is
   a bootstrap median over Monte-Carlo draws, which differs from the plain median of the per-system central values by up to 0.133 dex
   (M31 others, N = 5). It is now printed as `K1-reported`, and the script also prints the L-S labels of the X1 classes recomputed
   with the plain medians: **no label changes on either footing**.

With these fixes K0 (0 mismatches) and K1 (9/9) pass, the stop rule does not fire, and the verdict line is evaluated as frozen.
A reader who prefers the literal first run can read the verdict as UNDECIDED (stop rule); every rank-test number is identical in
both runs, because the class table E/s/Z values were never altered. MUTATE still fails K0 and K2 as required.

κ = ½ FITTED. Footings never pooled. Not "theory closed".
