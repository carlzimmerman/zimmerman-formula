# AZ2 AMENDMENT A1 (2026-11-12, post hoc, after the frozen runs were seen; committed alone before the amended run)

**What failed.** KA3 (profile minimum within Delta chi^2 0.1 of the free fit at each Om) fails in the headline cell T2 (BAO +
Pantheon+) at Om 0.30 in both footings: the profile on the 2.33 node found a lower chi^2 than the free fit by 0.357 (canonical)
and 0.373 (alt). Every other cell passes (|gap| <= 0.086). Cause: the free 5-node fit (three fixed starts, Nelder-Mead then
Powell) stops short of the minimum; the profile, warm-started node by node, gets lower. As frozen, the headline cell is
therefore NO VERDICT in both footings. The frozen Delta chi^2 values were already taken from min(free, profile), so D_band and
D_rival are unchanged in substance; what is wrong is the reported best sqrt X(2.33) and the KA3 check itself.

**Seen before writing this:** all frozen cells and Om-profiled rows for both footings (headline label as computed: FLAT HOLDS /
EXPANSION-MODEL DEPENDENT, D_band 1.76 / 1.79, D_rival ~361, X5 95 % grid interval [0.96, 2.5]); KA1 PASS, KA2 PASS; the first
MUTATE cell (canonical T1 Om 0.25).

**Change (only this).** In each cell, after the profile, the free fit is re-run with all five nodes free, started from the
nodes of the lowest profile point (in addition to the frozen starts); the free minimum is the lower of the two. KA3 is then
re-checked with the same 0.1 tolerance. Grid, flat band [0.90, 1.10], rival, labels, headline cell, KA1/KA2, MUTATE and its
bite rule are unchanged. Run with `AZ2_A1=1`; outputs `az2_<mode>_A1.json/.out` beside the frozen outputs. Both readings
(frozen: NO VERDICT on the headline cell; amended: whatever A1 gives) are reported in RESULT.md.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
