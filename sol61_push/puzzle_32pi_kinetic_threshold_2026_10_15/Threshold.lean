import Mathlib
noncomputable section
namespace KineticThreshold

theorem coefficient_factorization (n : ℝ) :
    (2*n-1)*(n-3/2)^2-2*n*(3-2*n) = (2*n-3)*(4*n^2+3)/4 := by ring

theorem long_shell_sign (n : ℝ) :
    0 ≤ (2*n-3)*(4*n^2+3)/4 ↔ (3:ℝ)/2 ≤ n := by
  have hp : 0 < 4*n^2+3 := by nlinarith [sq_nonneg n]
  constructor
  · intro h
    have hmul : 0 ≤ (2*n-3)*(4*n^2+3) := by linarith
    have hleft : 0 ≤ 2*n-3 := (mul_nonneg_iff_of_pos_right hp).mp hmul
    linarith
  · intro h
    have hleft : 0 ≤ 2*n-3 := by linarith
    exact div_nonneg (mul_nonneg hleft (le_of_lt hp)) (by norm_num)

theorem stable_threshold_speed (n : ℝ) (hn : (3:ℝ)/2 ≤ n) :
    2 ≤ 2*n-1 := by linarith

theorem potential_free_log_selects_power (n : ℝ) (h : 3-2*n=0) :
    n=(3:ℝ)/2 := by linarith

#print axioms coefficient_factorization
#print axioms long_shell_sign
#print axioms stable_threshold_speed
#print axioms potential_free_log_selects_power
end KineticThreshold
