/-
CFG357: decisive inequalities, in units of 1e-27 s^-2. Each computed Q2 (cfg357_results.json) is widened to a
rational interval of +-2% (the C4 grid-convergence tolerance). Cassini (Hees+ 2014): Q2 = 3 +- 3, so the 2-sigma
band is [-3, 9] and the 3-sigma upper bound is 12. This certifies the arithmetic only, not the PDE solution.
-/
import Mathlib

def lo (x : ℚ) : ℚ := x * (49/50)
def hi (x : ℚ) : ℚ := x * (51/50)
def inBand2 (x : ℚ) : Prop := -3 ≤ lo x ∧ hi x ≤ 9

-- filtered Q2 at the window edges (xi = 0.030 pc and 0.15 pc), both footings
def q_floor_can : ℚ := 63610/10000      -- 6.3610e-27
def q_floor_alt : ℚ := 74969/10000      -- 7.4969e-27
def q_top_can   : ℚ := 48108/1000000    -- 4.8108e-29
def q_top_alt   : ℚ := 56285/1000000    -- 5.6285e-29
-- unfiltered nu_mono and simple nu (p58 reproduction)
def q_nofilt_can : ℚ := 29207/1000      -- 2.9207e-26
def q_nofilt_alt : ℚ := 32054/1000      -- 3.2054e-26
def q_simple_can : ℚ := 21947/1000      -- 2.1947e-26

theorem floor_can_pass2 : inBand2 q_floor_can := by unfold inBand2 lo hi q_floor_can; norm_num
theorem floor_alt_pass2 : inBand2 q_floor_alt := by unfold inBand2 lo hi q_floor_alt; norm_num
theorem top_can_pass2 : inBand2 q_top_can := by unfold inBand2 lo hi q_top_can; norm_num
theorem top_alt_pass2 : inBand2 q_top_alt := by unfold inBand2 lo hi q_top_alt; norm_num
/-- sigma at the floor stays below 1.6 even at the interval's top: (hi - 3)/3 < 1.6 -/
theorem floor_alt_sigma_lt : (hi q_floor_alt - 3) / 3 < 8/5 := by unfold hi q_floor_alt; norm_num
/-- unfiltered: excluded beyond 3 sigma (lower interval end above 12) -/
theorem nofilt_can_fail3 : 12 < lo q_nofilt_can := by unfold lo q_nofilt_can; norm_num
theorem nofilt_alt_fail3 : 12 < lo q_nofilt_alt := by unfold lo q_nofilt_alt; norm_num
theorem simple_can_fail3 : 12 < lo q_simple_can := by unfold lo q_simple_can; norm_num
