import Mathlib
noncomputable section
namespace Relaxation

-- Algebraic checks only: the action and its interpretation are not formalized here.
theorem speed_gap_identity (m : ℝ) :
    (1+2*m^3)-m*(2+m^3) = (1-m)^3*(1+m) := by ring

theorem radial_speed_bounds (m : ℝ) (hm : 0 < m) (h1 : m < 1) :
    0 < m*(2+m^3)/(1+2*m^3) ∧ m*(2+m^3)/(1+2*m^3) < 1 := by
  have hc : 0 < m^3 := pow_pos hm 3
  have hd : 0 < 1+2*m^3 := by positivity
  constructor
  · exact div_pos (mul_pos hm (by positivity)) hd
  · apply (div_lt_one hd).mpr
    have hg : 0 < (1-m)^3*(1+m) := mul_pos (pow_pos (by linarith) 3) (by linarith)
    rw [← speed_gap_identity m] at hg
    linarith

theorem residual_identity (m : ℝ) (h : 1-m^3 ≠ 0)
    (hd : 1+m+m^2 ≠ 0) :
    m/(1-m^3)*(1-m) = m/(1+m+m^2) := by
  field_simp
  ring

theorem auxiliary_monotone (a b : ℝ) (ha : 1 ≤ a) (hab : a < b) :
    a^2*(a-1) < b^2*(b-1) := by
  have hb : 0 < b := by linarith
  have haa : 0 < a := by linarith
  have hsq : a^2 < b^2 := by nlinarith
  have hdiff : 0 < b-a := by linarith
  have hp : 0 < b^2*(b-a) := mul_pos (sq_pos_of_pos hb) hdiff
  have hq : 0 ≤ (b^2-a^2)*(a-1) := mul_nonneg (by linarith) (by linarith)
  nlinarith

#print axioms speed_gap_identity
#print axioms radial_speed_bounds
#print axioms residual_identity
#print axioms auxiliary_monotone
end Relaxation
