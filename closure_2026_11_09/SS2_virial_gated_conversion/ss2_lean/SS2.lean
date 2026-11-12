/-
SS2 (FROZEN_CRITERIA.md 390a1dc5ff): Lean statements for variant G's switch at alpha 4.39. They certify the switch, not the
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

namespace SS2

noncomputable def F (x u : ℝ) : ℝ := -Real.log u + x ^ 4 / 4 * (1 - u ^ 4)

theorem hasDerivAt_F (x u : ℝ) (hu : 0 < u) :
    HasDerivAt (F x) (-(1 + (x * u) ^ 4) / u) u := by
  have h1 : HasDerivAt (fun v => -Real.log v) (-(u⁻¹)) u := (Real.hasDerivAt_log hu.ne').neg
  have h2 : HasDerivAt (fun v => x ^ 4 / 4 * (1 - v ^ 4)) (x ^ 4 / 4 * (0 - (4 : ℝ) * u ^ 3)) u := by
    have := ((hasDerivAt_const u (1 : ℝ)).sub ((hasDerivAt_pow 4 u))).const_mul (x ^ 4 / 4)
    simpa using this
  have hfun : F x = (fun v => -Real.log v) + (fun v => x ^ 4 / 4 * (1 - v ^ 4)) := by
    funext v; simp [F]
  rw [hfun]
  have hu0 : u ≠ 0 := hu.ne'
  have hv : -u⁻¹ + x ^ 4 / 4 * (0 - 4 * u ^ 3) = -(1 + (x * u) ^ 4) / u := by
    field_simp
    ring
  exact (h1.add h2).congr_deriv hv

theorem closed_form_solves (x : ℝ) (y y' : ℝ → ℝ) (t : ℝ) (hy : HasDerivAt y (y' t) t) (hpos : 0 < y t)
    (hF : ∀ s, F x (y s) = s) : y' t = -y t / (1 + (x * y t) ^ 4) := by
  have hc : HasDerivAt (fun s => F x (y s)) (-(1 + (x * y t) ^ 4) / y t * y' t) t :=
    (hasDerivAt_F x (y t) hpos).comp t hy
  have hid : HasDerivAt (fun s => F x (y s)) 1 t := by
    have : (fun s => F x (y s)) = fun s => s := funext hF
    rw [this]; exact hasDerivAt_id t
  have heq := hc.unique hid
  have hq : 0 < 1 + (x * y t) ^ 4 := by positivity
  field_simp at heq ⊢
  linarith

theorem half_retention (x α : ℝ) : F x (1 / 2) = α ↔ x ^ 4 = 64 / 15 * (α - Real.log 2) := by
  have hl : Real.log (1 / 2 : ℝ) = -Real.log 2 := by rw [one_div, Real.log_inv]
  unfold F; rw [hl]
  constructor <;> intro h <;> nlinarith

theorem retention_mono (x1 x2 f1 f2 α : ℝ) (hx1 : 0 ≤ x1) (hx : x1 ≤ x2) (hf1 : 0 < f1) (hf1' : f1 ≤ 1) (hf2 : 0 < f2)
    (h1 : F x1 f1 = α) (h2 : F x2 f2 = α) : f1 ≤ f2 := by
  by_contra hc
  have hc : f2 < f1 := not_le.mp hc
  have hlog : Real.log f2 < Real.log f1 := Real.log_lt_log hf2 hc
  have h4 : f2 ^ 4 ≤ f1 ^ 4 := pow_le_pow_left₀ hf2.le hc.le 4
  have hx4 : x1 ^ 4 ≤ x2 ^ 4 := pow_le_pow_left₀ hx1 hx 4
  have hf14 : f1 ^ 4 ≤ 1 := pow_le_one₀ hf1.le hf1'
  unfold F at h1 h2
  nlinarith [pow_nonneg hx1 4, mul_le_mul_of_nonneg_right hx4 (sub_nonneg.2 hf14), mul_nonneg (pow_nonneg (le_trans hx1 hx) 4) (sub_nonneg.2 h4)]

theorem bound_low (x f : ℝ) (hx0 : 0 ≤ x) (hx : x ≤ 0.65) (hf : 0 < f) (h : F x f = 4.39) : f < 0.0137 := by
  have hx4 : x ^ 4 ≤ (0.65 : ℝ) ^ 4 := pow_le_pow_left₀ hx0 hx 4
  have hf4 : 0 ≤ f ^ 4 := by positivity
  unfold F at h
  have hlog : Real.log f ≤ -4.3453 := by nlinarith [mul_nonneg (pow_nonneg hx0 4) hf4]
  have he : (73 : ℝ) < Real.exp 4.3453 := by
    have h1 : Real.exp 4.3453 = Real.exp 1 ^ 4 * Real.exp 0.3453 := by
      rw [Real.exp_one_pow, ← Real.exp_add]; norm_num
    have h2 : (0.3453 : ℝ) + 1 ≤ Real.exp 0.3453 := Real.add_one_le_exp _
    have h3 : (2.7182818283 : ℝ) < Real.exp 1 := Real.exp_one_gt_d9
    have h4 : (2.7182818283 : ℝ) ^ 4 ≤ Real.exp 1 ^ 4 := pow_le_pow_left₀ (by norm_num) h3.le 4
    rw [h1]; nlinarith [Real.exp_pos 0.3453, pow_pos (Real.exp_pos 1) 4]
  have hle : f ≤ Real.exp (-4.3453) := by
    calc f = Real.exp (Real.log f) := (Real.exp_log hf).symm
      _ ≤ Real.exp (-4.3453) := Real.exp_le_exp.mpr hlog
  rw [Real.exp_neg] at hle
  have hp : 0 < Real.exp 4.3453 := Real.exp_pos _
  have hi : (Real.exp 4.3453)⁻¹ < 0.0137 := by
    rw [inv_lt_comm₀ hp (by norm_num)]; norm_num; linarith
  linarith

theorem bound_24 (x f : ℝ) (hx : 2.4 ≤ x) (hf : 0 < f) (h : F x f = 4.39) : 0.83 < f := by
  by_contra hc
  have hc : f ≤ 0.83 := not_lt.mp hc
  have hl : Real.log f ≤ f - 1 := Real.log_le_sub_one_of_pos hf
  have hx4 : (2.4 : ℝ) ^ 4 ≤ x ^ 4 := pow_le_pow_left₀ (by norm_num) hx 4
  have hf4 : f ^ 4 ≤ (0.83 : ℝ) ^ 4 := pow_le_pow_left₀ hf.le hc 4
  unfold F at h
  nlinarith [mul_le_mul_of_nonneg_right hx4 (by nlinarith : (0 : ℝ) ≤ 1 - f ^ 4)]

theorem bound_3 (x f : ℝ) (hx : 3 ≤ x) (hf : 0 < f) (h : F x f = 4.39) : 0.94 < f := by
  by_contra hc
  have hc : f ≤ 0.94 := not_lt.mp hc
  have hl : Real.log f ≤ f - 1 := Real.log_le_sub_one_of_pos hf
  have hx4 : (3 : ℝ) ^ 4 ≤ x ^ 4 := pow_le_pow_left₀ (by norm_num) hx 4
  have hf4 : f ^ 4 ≤ (0.94 : ℝ) ^ 4 := pow_le_pow_left₀ hf.le hc 4
  unfold F at h
  nlinarith [mul_le_mul_of_nonneg_right hx4 (by nlinarith : (0 : ℝ) ≤ 1 - f ^ 4)]

end SS2

#print axioms SS2.closed_form_solves
#print axioms SS2.half_retention
#print axioms SS2.retention_mono
#print axioms SS2.bound_low
#print axioms SS2.bound_24
#print axioms SS2.bound_3
