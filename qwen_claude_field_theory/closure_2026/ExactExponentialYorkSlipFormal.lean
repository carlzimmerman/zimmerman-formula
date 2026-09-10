import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! Lean certificate for the exact exponential York/QUMOND slip coefficient. -/

namespace ExactExponentialYorkSlip

theorem metric_difference_factor
    (nu q0 q1 : ℝ) :
    ((-2 + nu) * q0 ^ 2) - ((-2 + nu) * q1 ^ 2) =
      (nu - 2) * (q0 ^ 2 - q1 ^ 2) := by
  ring

theorem generic_metric_difference_factor
    (A Aprime Fprime u q0 q1 : ℝ) :
    ((Fprime - 2 * (A + u * Aprime)) * q0 ^ 2) -
        ((Fprime - 2 * (A + u * Aprime)) * q1 ^ 2) =
      (Fprime - 2 * (A + u * Aprime)) * (q0 ^ 2 - q1 ^ 2) := by
  ring

theorem exponential_nu_not_const_two
    (h : ∀ x : ℝ, 0 < x → 1 / (1 - Real.exp (-x)) = 2) : False := by
  have h1 := h 1 (by norm_num)
  have h2 := h 2 (by norm_num)
  have hd1 : (1 - Real.exp (-1 : ℝ)) ≠ 0 := by
    intro hz
    rw [hz] at h1
    norm_num at h1
  have hd2 : (1 - Real.exp (-2 : ℝ)) ≠ 0 := by
    intro hz
    rw [hz] at h2
    norm_num at h2
  field_simp [hd1] at h1
  field_simp [hd2] at h2
  have heq : Real.exp (-1 : ℝ) = Real.exp (-2 : ℝ) := by
    linarith
  have hlt : Real.exp (-2 : ℝ) < Real.exp (-1 : ℝ) := by
    apply Real.exp_lt_exp.mpr
    norm_num
  linarith

end ExactExponentialYorkSlip
