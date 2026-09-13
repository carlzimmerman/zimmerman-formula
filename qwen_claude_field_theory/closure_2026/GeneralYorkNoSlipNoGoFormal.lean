import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.Complex.Exponential
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! Algebraic certificate for the scoped first-gradient York/QUMOND obstruction. -/

namespace GeneralYorkNoSlipNoGo

theorem poisson_normalization_fixes_A {A q : ℝ} (hq : q ≠ 0)
    (h : -2 * A * q = -2 * q) : A = 1 := by
  apply (mul_left_cancel₀ hq)
  nlinarith

theorem no_slip_coefficient_after_poisson
    {Fprime : ℝ} : Fprime - 2 * (1 + 0) = Fprime - 2 := by ring

theorem exponential_not_equal_two_at_one :
    1 / (1 - Real.exp (-1 : ℝ)) ≠ 2 := by
  intro h
  have hd : (1 - Real.exp (-1 : ℝ)) ≠ 0 := by
    intro hz
    rw [hz] at h
    norm_num at h
  field_simp [hd] at h
  have hexpneg : Real.exp (-1 : ℝ) = (1 / 2 : ℝ) := by linarith
  have hexp1 : (2 : ℝ) < Real.exp 1 := by
    have hlt := Real.add_one_lt_exp (x := (1 : ℝ)) (by norm_num)
    norm_num at hlt ⊢
    exact hlt
  have hrecip : Real.exp (-1 : ℝ) < (1 / 2 : ℝ) := by
    calc
      Real.exp (-1 : ℝ) = (Real.exp (1 : ℝ))⁻¹ := by rw [Real.exp_neg]
      _ < ((2 : ℝ))⁻¹ :=
        (inv_lt_inv₀ (Real.exp_pos (1 : ℝ)) (by norm_num)).2 hexp1
      _ = (1 / 2 : ℝ) := by norm_num
  linarith

theorem exponential_response_not_constant_two
    (h : ∀ x : ℝ, 0 < x → 1 / (1 - Real.exp (-x)) = 2) : False := by
  have h1 := h 1 (by norm_num)
  exact exponential_not_equal_two_at_one h1

end GeneralYorkNoSlipNoGo
