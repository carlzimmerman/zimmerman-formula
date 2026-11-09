/-
SS2 MUTATE (FROZEN_CRITERIA.md 390a1dc5ff): Lean statements for variant G's switch at alpha 4.39. They certify the switch, not the
physics. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
F x u = -log u + x^4/4 (1 - u^4); the retention f at alpha is the root of F x f = alpha.
  * hasDerivAt_F, closed_form_solves : the closed form solves dy/dtau = -y/(1 + (x0 y)^4)
  * half_retention                   : F x (1/2) = alpha <-> x^4 = (64/15)(alpha - log 2)  (x_crit 1.993 at 4.39, numerical)
  * retention_mono                   : the root is monotone in x0
  * bound_low  : x0 <= 0.65, alpha 4.39 -> f < 0.0137      (galaxy-scale halos drain)
  * bound_24   : x0 >= 2.4,  alpha 4.39 -> f > 0.83
  * bound_3    : x0 >= 3,    alpha 4.39 -> f > 0.94        (groups and clusters keep their share)
-/
import Mathlib

namespace SS2M
noncomputable def F (x u : ℝ) : ℝ := -Real.log u + x ^ 4 / 4 * (1 - u ^ 4)
/-- MUTATE: a bound the true root (0.8375 at x0 2.4) violates. Must NOT compile. -/
theorem bound_24_wrong (x f : ℝ) (hx : 2.4 ≤ x) (hf : 0 < f) (h : F x f = 4.39) : 0.85 < f := by
  by_contra hc
  have hc : f ≤ 0.85 := not_lt.mp hc
  have hl : Real.log f ≤ f - 1 := Real.log_le_sub_one_of_pos hf
  have hx4 : (2.4 : ℝ) ^ 4 ≤ x ^ 4 := pow_le_pow_left₀ (by norm_num) hx 4
  have hf4 : f ^ 4 ≤ (0.85 : ℝ) ^ 4 := pow_le_pow_left₀ hf.le hc 4
  unfold F at h
  nlinarith [mul_le_mul_of_nonneg_right hx4 (by nlinarith : (0 : ℝ) ≤ 1 - f ^ 4)]
end SS2M
