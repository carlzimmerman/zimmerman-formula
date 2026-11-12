/-
SS1 variants B-G (AMENDMENT_A2 2b866ef57a): Lean statements for the Hill-4 switch. They certify the switch, not the physics.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

F x u = -log u + x^4/4 (1 - u^4). Retention f at time alpha is the root of F x f = alpha.
  * hasDerivAt_F       : dF/du = -(1 + (x u)^4)/u           (u > 0)
  * closed_form_solves : if F x (y t) = t along a differentiable y > 0, then y' = -y/(1 + (x y)^4)
  * half_retention     : F x (1/2) = alpha  <->  x^4 = (64/15)(alpha - log 2)
  * retention_mono     : the root is monotone in x0
  * bound_195          : x0 >= 1.95, alpha = 3.80  ->  f > 0.249
  * bound_32           : x0 >= 3.2,  alpha = 3.80  ->  f > 0.958
(The third bound in the relayed list, f < 0.0235 for x0 <= 0.65, is checked numerically in parts/v_ka.json; it needs
exp(3.7554) > 42.55, which is not formalised here.)
-/
import Mathlib

namespace SS1V

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

theorem bound_195 (x f : ℝ) (hx : 1.95 ≤ x) (hf : 0 < f) (h : F x f = 3.80) : 0.249 < f := by
  by_contra hc
  have hc : f ≤ 0.249 := not_lt.mp hc
  have hl : Real.log f ≤ f - 1 := Real.log_le_sub_one_of_pos hf
  have hx4 : (1.95 : ℝ) ^ 4 ≤ x ^ 4 := pow_le_pow_left₀ (by norm_num) hx 4
  have hf4 : f ^ 4 ≤ (0.249 : ℝ) ^ 4 := pow_le_pow_left₀ hf.le hc 4
  unfold F at h
  nlinarith [mul_le_mul_of_nonneg_right hx4 (by nlinarith : (0 : ℝ) ≤ 1 - f ^ 4)]

theorem bound_32 (x f : ℝ) (hx : 3.2 ≤ x) (hf : 0 < f) (h : F x f = 3.80) : 0.958 < f := by
  by_contra hc
  have hc : f ≤ 0.958 := not_lt.mp hc
  have hl : Real.log f ≤ f - 1 := Real.log_le_sub_one_of_pos hf
  have hx4 : (3.2 : ℝ) ^ 4 ≤ x ^ 4 := pow_le_pow_left₀ (by norm_num) hx 4
  have hf4 : f ^ 4 ≤ (0.958 : ℝ) ^ 4 := pow_le_pow_left₀ hf.le hc 4
  unfold F at h
  nlinarith [mul_le_mul_of_nonneg_right hx4 (by nlinarith : (0 : ℝ) ≤ 1 - f ^ 4)]

end SS1V

#print axioms SS1V.closed_form_solves
#print axioms SS1V.half_retention
#print axioms SS1V.retention_mono
#print axioms SS1V.bound_195
#print axioms SS1V.bound_32
