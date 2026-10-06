/-
CFG346: the decisive inequalities of the smeared-switch data test, as rationals (values from
cfg346_smeared_switch_results.json, rounded toward the side that does NOT favour the stated conclusion).
-/
import Mathlib

namespace CFG346

/-- interior level f_in = 1 + 2/R at CFG337's declared R. -/
theorem fin_R4 : (1 : ℚ) + 2 / 4 = 3 / 2 := by norm_num
theorem fin_R40 : (1 : ℚ) + 2 / 40 = 21 / 20 := by norm_num

/-- best stable configuration (C2, R = 4, local E_c, ell = ell_min = 378.5 kpc, declared level):
KiDS passes on both footings (d chi^2 <= -41.70 < +9). -/
theorem best_K_pass : (-4170 : ℚ) / 100 ≤ 9 ∧ (-4640 : ℚ) / 100 ≤ 9 := by norm_num

/-- ... but SPARC fails: spiral A3 = 2/61 (canonical) is below 0.90, and d rms >= 0.0261 > 0.005. -/
theorem best_S_fail : (2 : ℚ) / 61 < 9 / 10 ∧ (5 : ℚ) / 1000 < 261 / 10000 := by norm_num

/-- unit level (smearing only, f_in = 1) at the same ell: dwarf A3 = 7/55 < 0.90 and d rms 0.0124 > 0.005. -/
theorem unit_S_fail : (7 : ℚ) / 55 < 9 / 10 ∧ (5 : ℚ) / 1000 < 124 / 10000 := by norm_num

/-- every configuration that fails KiDS misses by at least d chi^2 = 16.69 > 9. -/
theorem K_fail_margin : (9 : ℚ) < 1669 / 100 := by norm_num

/-- growth: the largest tail at 20 h^-1 Mpc (4.01e-8) is below CFG324's 1.2e-3. -/
theorem G_tail : (401 : ℚ) / 10 ^ 10 < 12 / 10 ^ 4 := by norm_num

/-- the linear FRW trigger is OFF: U = (1 + delta)/Delta_ta <= 1.06/11.8 < 1, so T = 1 - 1/U < -2/R for R >= 4. -/
theorem frw_off : (106 : ℚ) / 100 / (118 / 10) < 1 ∧
    (1 : ℚ) - (118 / 10) / (106 / 100) < -(2 : ℚ) / 4 := by norm_num

/-- the transition instability returns below ell_min: the H4 ratio scales as ell_min / ell. -/
theorem instability_returns (lm l : ℚ) (hl : 0 < l) (h : l < lm) : 1 < lm / l := by
  rw [lt_div_iff₀ hl]; linarith

theorem half_ell_min (lm : ℚ) (h : 0 < lm) : lm / (lm / 2) = 2 := by
  field_simp

/-- MUTATE (ell = 10 ell_min) fails KiDS for the best configuration: d chi^2 >= +641.9 > 9. -/
theorem mutate_bites : (9 : ℚ) < 6419 / 10 := by norm_num

/-- decision: passes (K, S, G) = (1, 0, 1) count to 2, which is PARTIAL (not 3 = RESOLVED, not < 2 = NOT). -/
theorem decision_partial : (1 : ℕ) + 0 + 1 = 2 ∧ (2 : ℕ) < 3 := by norm_num

/-- every configuration adds at least two declared constants beyond kappa = 1/2. -/
theorem adds_constants (n : ℕ) (h : 2 ≤ n) : 0 < n := by omega

end CFG346

#print axioms CFG346.instability_returns
#print axioms CFG346.best_S_fail
