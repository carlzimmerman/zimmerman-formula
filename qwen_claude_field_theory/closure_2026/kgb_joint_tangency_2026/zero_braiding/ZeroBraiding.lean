import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith

/-! Conditional real-algebra only. The matrix relation must first be derived
from the original vacuum scalar equation and principal matrix. Neither the
action reduction, its on-shell hypotheses, nor mode counting is formalized. -/
namespace ZeroBraiding

theorem timelike_ratio_positive (v0 v1 : ℝ)
    (hrad : 0 < v1 ^ 2) (htime : v1 ^ 2 < v0 ^ 2) :
    0 < (v0 ^ 2 - v1 ^ 2) / v1 ^ 2 := by
  exact div_pos (sub_pos.mpr htime) hrad

theorem no_strict_bounded_scalar_energy (v0 v1 K T : ℝ)
    (hrad : 0 < v1 ^ 2) (htime : v1 ^ 2 < v0 ^ 2)
    (hrelation : K = ((v0 ^ 2 - v1 ^ 2) / v1 ^ 2) * T) :
    ¬ (0 < K ∧ T < 0) := by
  rintro ⟨hK, hT⟩
  have hratio := timelike_ratio_positive v0 v1 hrad htime
  have hnegative := mul_neg_of_pos_of_neg hratio hT
  rw [← hrelation] at hnegative
  linarith

theorem zero_radial_fails_strict_bound (R : ℝ) (hR : R = 0) :
    ¬ R < 0 := by
  rw [hR]
  exact lt_irrefl 0

#print axioms timelike_ratio_positive
#print axioms no_strict_bounded_scalar_energy
#print axioms zero_radial_fails_strict_bound
end ZeroBraiding
