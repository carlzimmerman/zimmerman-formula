# X26_cold_sector_map: AMENDMENT A1 (implementation only; RUN1 killed before any graded number was printed)

No family, grid, constraint, line, rule or verdict class changes.

RUN1 printed step 0 (K0a–K0f all PASS), K1 and K2, then numpy warned "divide by zero encountered in log" in the cluster-table
interpolation. Some KT clusters carry zero MID weight, so their tabulated d is 0 at every node and log-linear interpolation
returns NaN, which would have failed every cluster constraint silently. RUN1 was killed before any constraint pass fraction,
allowed region or threshold table was printed (its last line was the cosmic-medium σ_cos, ρ_b,0 setup line). Its partial log
is not kept as a lane output.

Changes (code only):
1. **Table interpolation:** log-linear in d where a cluster's tabulated d is positive at every node, linear in d otherwise
   (a zero-weight cluster then contributes exactly 0, as in X21's sums). The count of such clusters per cell is printed. An
   assertion stops the run if any cluster prediction is non-finite.
2. **K1** treats a non-finite ratio as a failure (RUN1's `max` would have skipped a NaN).
3. **Cosmic thresholds:** ±inf thresholds (ok at every / no C₀ in the bisection range) are interpolated as ±99 in log₁₀ C₀
   instead of being dropped; the upper end of the bisection range (C₀ = 10^5.5 km/s) is never evaluated directly (stiff ODE);
   a threshold within one step of it is recorded as +inf. Progress lines are printed to the terminal only.

# AMENDMENT A2 (post-result, disclosed; a check only, no rule change)

RUN2 (the first complete run, kept as the lane output if A2's check passes) found the scenario-B allowed set to be a thin
sheet, one c_* grid step thick, sitting on the cluster window. Because the cluster grades there come from the interpolated
d-table (K1 tolerance 1 %), A2 adds **K5**: every allowed (c_*, r, q) and its c_* ± 1 neighbours are re-graded on the four
cluster constraints (C-T1, C-T2, C-T3, C-KTb, both h cells) with the hydrostatic model evaluated directly per cluster (no
table). K5 passes iff no grade flips. The Z margins at each allowed point are printed. If K5 fails, the flipped points are
listed and the direct grades are the model's; the verdict line is then re-read by hand in the README and disclosed. No other
change; the verdict code, the grid and all lines are unchanged.

# AMENDMENT A3 (post-result, reported only; no verdict weight)

Two reported lines, added after RUN2/RUN3 showed allowed points with r = 0 and a universal (r = q = 0) allowed point on alt
at c_* = 10^2.875 = 750 km/s, a value between X23 A1's scan nodes (c_s,need × 3 and × 4):
1. the X7 MGAS500 terciles (all 326 clusters; X23 A1's C-T1..T3) at every scenario-B allowed point with r = 0 (σ does not
   enter there, so every cluster can be graded);
2. a fine universal scan, c_s = 500–1000 km/s in 36 log steps, graded directly (no table) on the KT terciles + slope and on
   the MGAS500 terciles, both h cells.
Neither line changes the frozen verdict code; both are quoted in the README as reported.
