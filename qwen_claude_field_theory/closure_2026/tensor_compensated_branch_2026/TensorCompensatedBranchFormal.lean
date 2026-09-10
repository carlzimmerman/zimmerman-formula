import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-! Lean finite-k algebra for the trace-free spatial compensator branch. -/

namespace TensorCompensatedBranch

theorem tf_multiplier_cancels
    (k M2 mu S Lambda : ℝ)
    (hk : k ≠ 0)
    (hsource : 2 * M2 * mu * S + k ^ 2 * Lambda = 0) :
    Lambda = -(2 * M2 * mu * S) / k ^ 2 := by
  have hk2 : k ^ 2 ≠ 0 := pow_ne_zero 2 hk
  apply (eq_div_iff hk2).2
  linarith

theorem exponential_tf_multiplier_cancels
    (k M2 y S Lambda : ℝ)
    (hk : k ≠ 0)
    (hsource : 2 * M2 * S * y ^ 2 * Real.exp (-y) + k ^ 2 * Lambda = 0) :
    Lambda = -(2 * M2 * S * y ^ 2 * Real.exp (-y)) / k ^ 2 := by
  have hk2 : k ^ 2 ≠ 0 := pow_ne_zero 2 hk
  apply (eq_div_iff hk2).2
  linarith

theorem opposite_scalar_shifts_cancel (k Lambda : ℝ) :
    k ^ 2 * Lambda + (-k ^ 2 * Lambda) = 0 := by ring

theorem nonzero_mode_hessian_constraint
    (k d : ℝ) (hk : k ≠ 0) (hC : k ^ 2 * d = 0) : d = 0 := by
  have hk2 : k ^ 2 ≠ 0 := pow_ne_zero 2 hk
  exact (mul_eq_zero.mp hC).resolve_left hk2

theorem exponential_mu_pos (y : ℝ) (hy : 0 < y) :
    0 < 1 - Real.exp (-y) := by
  have hneg : -y < 0 := by linarith
  have hexp : Real.exp (-y) < 1 := Real.exp_lt_one_iff.mpr hneg
  linarith

theorem luminal_ratio (M2 : ℝ) (hM2 : 0 < M2) : M2 / M2 = 1 :=
  div_self (ne_of_gt hM2)

theorem finite_k_scalar_dof_count :
    (14 - 2 * 2 - 10 : ℤ) / 2 = 0 := by norm_num

theorem homogeneous_scalar_dof_count :
    (14 - 2 * 6 - 0 : ℤ) / 2 = 1 := by norm_num

theorem expanding_flrw_branch
    (M2 rho Lambda H : ℝ)
    (hM2 : 0 < M2)
    (hsource : 0 < rho + M2 * Lambda)
    (hfriedmann : 3 * M2 * H ^ 2 = rho + M2 * Lambda)
    (hH : 0 < H) :
    H ^ 2 = (rho + M2 * Lambda) / (3 * M2) ∧
      0 < (rho + M2 * Lambda) / (3 * M2) ∧ 0 < H ^ 2 := by
  have hden : 3 * M2 ≠ 0 := by positivity
  have heq : H ^ 2 = (rho + M2 * Lambda) / (3 * M2) := by
    apply (eq_div_iff hden).2
    nlinarith
  refine ⟨heq, ?_, sq_pos_of_pos hH⟩
  exact div_pos hsource (by positivity)

theorem lapse_retained_zero_mode_dof_count :
    (12 - 2 * 6 - 0 : ℤ) / 2 = 0 := by norm_num

theorem homogeneous_constraint_preservation (N C : ℝ) :
    N * C * C - C * N * C = 0 := by ring

end TensorCompensatedBranch
