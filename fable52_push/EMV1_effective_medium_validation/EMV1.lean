/-
EMV1 (criteria f924165783): Lean statements for the closed forms the lane uses as known answers. They certify the algebra and the
inequalities, not the physics or the numerics. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

The law's permittivity: mu(u) = u / (1 + u). Fields in units of a0, the bubble radius 1.
  homog_alpha_bounds    : a linear homogeneous sphere with 0 <= m <= 1 has -1/2 <= (m - 1) / (m + 2) <= 0.
  No galaxy (M_b = 0): the interior field is uniform, x > 0, and the external field it answers is e(x) = x (3 x + 2) / (3 (1 + x)).
  uniform_matching      : x (mu(x) + 2) = 3 e(x)  (potential continuity plus flux continuity for a uniform interior).
  eOf_pos, eOf_strictMono, uniform_unique : e(x) > 0, strictly increasing on x >= 0, so the uniform solution is unique.
  alpha_tot_closed, alpha_tot_is_homog    : alpha_tot = 1 - x / e = (mu - 1) / (mu + 2) = -1 / (2 + 3 x).
  dipole_identity       : p / (R^3 a0) = alpha_tot e = e - x.
  hasDerivAt_eOf        : de/dx = (3 x^2 + 6 x + 2) / (3 (1 + x)^2).
  alpha_inc_closed      : alpha_inc = d(e - x)/de = 1 - 1 / (de/dx) = -1 / (3 x^2 + 6 x + 2).
  alpha_order           : -1/2 < alpha_tot < alpha_inc < 0 for x > 0 (the incremental response is the weaker one).
  allowance_line        : Maxwell-Garnett q_C = -3 f alpha / (1 + 2 f alpha) meets q_C <= q iff f <= q / (-alpha (3 + 2 q)).
  allowance_ge_insulating : for -1/2 <= alpha < 0 that allowance is at least SWT1's q / (3/2 + q).
-/
import Mathlib

namespace EMV1

noncomputable def mu (u : ℝ) : ℝ := u / (1 + u)

/-! ### Linear homogeneous sphere -/

theorem homog_alpha_bounds (m : ℝ) (h0 : 0 ≤ m) (h1 : m ≤ 1) :
    -(1 / 2 : ℝ) ≤ (m - 1) / (m + 2) ∧ (m - 1) / (m + 2) ≤ 0 := by
  have h : 0 < m + 2 := by linarith
  constructor
  · rw [le_div_iff₀ h]; linarith
  · rw [div_le_iff₀ h]; nlinarith

/-! ### No galaxy: the uniform nonlinear solution -/

noncomputable def eOf (x : ℝ) : ℝ := x * (3 * x + 2) / (3 * (1 + x))

theorem uniform_matching (x : ℝ) (hx : 0 < x) : x * (mu x + 2) = 3 * eOf x := by
  unfold mu eOf
  have h : (1 + x) ≠ 0 := by positivity
  field_simp
  ring

theorem eOf_pos (x : ℝ) (hx : 0 < x) : 0 < eOf x := by
  unfold eOf; positivity

theorem eOf_strictMono (a b : ℝ) (ha : 0 ≤ a) (hab : a < b) : eOf a < eOf b := by
  unfold eOf
  have h1 : 0 < 3 * (1 + a) := by linarith
  have h2 : 0 < 3 * (1 + b) := by linarith
  rw [div_lt_div_iff₀ h1 h2]
  have hb : 0 ≤ b := by linarith
  have hk : 0 < 3 * (a + b) + 2 + 3 * a * b := by nlinarith [mul_nonneg ha hb]
  nlinarith [mul_pos (sub_pos.mpr hab) hk]

theorem uniform_unique (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) (h : eOf a = eOf b) : a = b := by
  rcases lt_trichotomy a b with hlt | heq | hgt
  · exact absurd h (ne_of_lt (eOf_strictMono a b ha hlt))
  · exact heq
  · exact absurd h (ne_of_gt (eOf_strictMono b a hb hgt))

theorem alpha_tot_closed (x : ℝ) (hx : 0 < x) : 1 - x / eOf x = -1 / (2 + 3 * x) := by
  unfold eOf
  have h1 : (1 + x) ≠ 0 := by positivity
  have h2 : (3 * x + 2) ≠ 0 := by positivity
  have h3 : x ≠ 0 := hx.ne'
  have h4 : (2 + 3 * x) ≠ 0 := by positivity
  field_simp
  ring

theorem alpha_tot_is_homog (x : ℝ) (hx : 0 < x) : (mu x - 1) / (mu x + 2) = -1 / (2 + 3 * x) := by
  unfold mu
  have h1 : (1 + x) ≠ 0 := by positivity
  have h2 : (2 + 3 * x) ≠ 0 := by positivity
  have h3 : (x + 2 * (1 + x)) ≠ 0 := by positivity
  have h4 : x / (1 + x) + 2 = (x + 2 * (1 + x)) / (1 + x) := by field_simp
  have h5 : x / (1 + x) - 1 = (x - (1 + x)) / (1 + x) := by field_simp
  rw [h4, h5, div_div_div_cancel_right₀ h1, div_eq_div_iff h3 h2]
  ring

theorem dipole_identity (x : ℝ) (hx : 0 < x) : (1 - x / eOf x) * eOf x = eOf x - x := by
  have h := (eOf_pos x hx).ne'
  field_simp

theorem hasDerivAt_eOf (x : ℝ) (hx : 0 < x) :
    HasDerivAt eOf ((3 * x ^ 2 + 6 * x + 2) / (3 * (1 + x) ^ 2)) x := by
  have hn : HasDerivAt (fun y : ℝ => y * (3 * y + 2)) (1 * (3 * x + 2) + x * (3 * 1)) x :=
    (hasDerivAt_id' x).mul (((hasDerivAt_id' x).const_mul 3).add_const 2)
  have hd : HasDerivAt (fun y : ℝ => 3 * (1 + y)) (3 * 1) x :=
    ((hasDerivAt_id' x).const_add 1).const_mul 3
  have hne : 3 * (1 + x) ≠ 0 := by positivity
  have key : ((1 * (3 * x + 2) + x * (3 * 1)) * (3 * (1 + x)) - x * (3 * x + 2) * (3 * 1)) / (3 * (1 + x)) ^ 2
      = (3 * x ^ 2 + 6 * x + 2) / (3 * (1 + x) ^ 2) := by
    rw [div_eq_div_iff (by positivity) (by positivity)]; ring
  exact (hn.div hd hne).congr_deriv key

theorem alpha_inc_closed (x : ℝ) (hx : 0 < x) :
    1 - 1 / ((3 * x ^ 2 + 6 * x + 2) / (3 * (1 + x) ^ 2)) = -1 / (3 * x ^ 2 + 6 * x + 2) := by
  have h1 : (3 * x ^ 2 + 6 * x + 2) ≠ 0 := by positivity
  have h2 : (1 + x) ≠ 0 := by positivity
  field_simp
  ring

theorem alpha_order (x : ℝ) (hx : 0 < x) :
    -(1 / 2 : ℝ) < -1 / (2 + 3 * x) ∧ -1 / (2 + 3 * x) < -1 / (3 * x ^ 2 + 6 * x + 2) ∧
      -1 / (3 * x ^ 2 + 6 * x + 2) < 0 := by
  have h1 : 0 < 2 + 3 * x := by linarith
  have h2 : 0 < 3 * x ^ 2 + 6 * x + 2 := by positivity
  refine ⟨?_, ?_, ?_⟩
  · rw [lt_div_iff₀ h1]; nlinarith
  · rw [div_lt_div_iff₀ h1 h2]; nlinarith
  · exact div_neg_of_neg_of_pos (by norm_num) h2

/-! ### The allowance on the filling -/

theorem allowance_line (f α q : ℝ) (hf : 0 ≤ f) (hf1 : f < 1) (hα1 : -(1 / 2) ≤ α) (hα0 : α < 0) (hq : 0 < q) :
    -3 * f * α / (1 + 2 * f * α) ≤ q ↔ f ≤ q / (-α * (3 + 2 * q)) := by
  have hden : 0 < 1 + 2 * f * α := by nlinarith [mul_nonneg hf (show (0 : ℝ) ≤ α + 1 / 2 by linarith)]
  have hden2 : 0 < -α * (3 + 2 * q) := by nlinarith
  rw [div_le_iff₀ hden, le_div_iff₀ hden2]
  constructor <;> intro h <;> nlinarith

theorem allowance_ge_insulating (α q : ℝ) (hα1 : -(1 / 2) ≤ α) (hα0 : α < 0) (hq : 0 < q) :
    q / (3 / 2 + q) ≤ q / (-α * (3 + 2 * q)) := by
  have h0 : 0 < 3 / 2 + q := by linarith
  have h1 : 0 < -α * (3 + 2 * q) := by nlinarith
  rw [div_le_div_iff₀ h0 h1]
  nlinarith [mul_nonneg hq.le (show (0 : ℝ) ≤ 3 / 2 + q - (-α * (3 + 2 * q)) by nlinarith)]

end EMV1

#print axioms EMV1.homog_alpha_bounds
#print axioms EMV1.uniform_matching
#print axioms EMV1.eOf_pos
#print axioms EMV1.eOf_strictMono
#print axioms EMV1.uniform_unique
#print axioms EMV1.alpha_tot_closed
#print axioms EMV1.alpha_tot_is_homog
#print axioms EMV1.dipole_identity
#print axioms EMV1.hasDerivAt_eOf
#print axioms EMV1.alpha_inc_closed
#print axioms EMV1.alpha_order
#print axioms EMV1.allowance_line
#print axioms EMV1.allowance_ge_insulating

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
