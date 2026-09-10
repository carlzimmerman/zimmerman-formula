import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! Lean arithmetic certificate for the generated linear-sector gate. -/

namespace LinearSectorStability

theorem positive_tensor_kinetic (M2 : ℝ) (hM2 : 0 < M2) :
    0 < M2 / 8 := by positivity

theorem positive_tensor_gradient (M2 k : ℝ) (hM2 : 0 < M2) (hk : 0 < k) :
    0 < M2 * k ^ 2 / 8 := by positivity

theorem luminal_tensor_speed (M2 k : ℝ) (hM2 : 0 < M2) (hk : 0 < k) :
    (M2 * k ^ 2 / 8) / ((M2 / 8) * k ^ 2) = 1 := by
  have hM2ne : M2 ≠ 0 := ne_of_gt hM2
  have hkne : k ≠ 0 := ne_of_gt hk
  have hden : (M2 / 8) * k ^ 2 ≠ 0 := by
    exact mul_ne_zero (div_ne_zero hM2ne (by norm_num)) (pow_ne_zero 2 hkne)
  apply (div_eq_iff hden).2
  ring

theorem vector_dof_count : (2 - 0 - 2 : ℤ) / 2 = 0 := by norm_num

theorem scalar_finite_k_dof_count : (14 - 2 * 2 - 10 : ℤ) / 2 = 0 := by
  norm_num

end LinearSectorStability
