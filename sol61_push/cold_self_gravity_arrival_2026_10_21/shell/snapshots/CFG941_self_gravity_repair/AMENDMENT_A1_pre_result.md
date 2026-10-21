# CFG941 amendment A1 (pre-result, 2026-10-20)

Written after the criteria commit (0b41bd0cf) and before any script run or number of this lane.

**What.** Test (a)'s numeric deep-BTFR evaluation point moves from y = g_N/a₀ = 1e-12 to y = 1e-14.

**Why.** For the closed-form law, V⁴/(G M_b a₀) = ν(y)² y = 1 + √y + y/4 + … So at y = 1e-12 the law *itself* deviates by
1e-6 + 2.5e-13, i.e. it would miss the frozen 1e-6 line by 2.5e-13. That is a slip in my criteria (I wrote the correction as
O(y) instead of O(√y)), found while writing the script. At y = 1e-14 the law's own correction is 1e-7, ten times inside the
line.

**What does not change.** The primary BTFR test, the symbolic limit lim_{y→0} V⁴/(G M_b a₀) = 1, is unchanged. Every other
test, tolerance, control and class rule is unchanged. No repair's outcome was known when this was written (nothing had been run).
