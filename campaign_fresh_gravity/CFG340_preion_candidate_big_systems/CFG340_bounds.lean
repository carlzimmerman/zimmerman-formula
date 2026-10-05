/-
CFG340: decisive R_max vs R_plausible(upper) inequalities (z_f = 3, both footings).
Inputs are the committed run's bisection results, rounded conservatively (R_max down, post-hoc pass edges up, to 0.01).
S1/S2/K1 fail their committed criterion already at R = 1, so R_max < 1; the post-hoc pass edges (0.236, 0.748, 0.828) are below 1.
-/
import Mathlib

namespace CFG340

-- frozen R_plausible upper ends
def rplS1 : ℚ := 3
def rplS2 : ℚ := 1230 / 100   -- 10^1.09 = 12.30 (rounded down: 12.302)
def rplX1 : ℚ := 3
def rplK1 : ℚ := 3
def rplC1 : ℚ := 6 / 5

-- bounds from the run (R_max rounded down; fail-edges rounded up)
def rmaxX1 : ℚ := 945 / 100   -- 9.453
def rmaxC1 : ℚ := 131 / 100   -- 1.319
def edgeS1 : ℚ := 24 / 100    -- passes only for R <= 0.236
def edgeS2 : ℚ := 75 / 100    -- 0.748
def edgeK1 : ℚ := 83 / 100    -- 0.828

/-- FAIL clause: each of S1, S2, K1 passes only below an edge that is below R_plausible (indeed below 1). -/
theorem s1_fail : edgeS1 < 1 ∧ edgeS1 < rplS1 := by unfold edgeS1 rplS1; norm_num
theorem s2_fail : edgeS2 < 1 ∧ edgeS2 < rplS2 := by unfold edgeS2 rplS2; norm_num
theorem k1_fail : edgeK1 < 1 ∧ edgeK1 < rplK1 := by unfold edgeK1 rplK1; norm_num

/-- X-ray ellipticals clear the PASS bar (R_max >= 2 R_plaus). -/
theorem x1_pass : 2 * rplX1 ≤ rmaxX1 := by unfold rplX1 rmaxX1; norm_num

/-- X-COP clears R_plaus but not 2 R_plaus (MARGINAL on its own). -/
theorem c1_marginal : rplC1 ≤ rmaxC1 ∧ rmaxC1 < 2 * rplC1 := by unfold rplC1 rmaxC1; norm_num

/-- The frozen decision: some population has R_max < R_plaus, hence FAIL. -/
theorem verdict_fail : ∃ e r : ℚ, (e, r) ∈ [(edgeS1, rplS1), (edgeS2, rplS2), (edgeK1, rplK1)] ∧ e < r :=
  ⟨edgeS1, rplS1, by simp, s1_fail.2⟩

end CFG340
