import Mathlib

/-!
# M3A -- CA5-GNC-R reciprocal vacuum: the exponential estimate and the all-q scalar sign theorem

Source: `real_research/breakthrough_review_2026_09_26/vacuum/ACTION.md` (R7 and the paragraph after it)
and `.../vacuum/check.py` (checks `logarithmic_derivative`, `integrated_stiffness_factor`, and the finite
regression `assert A>0 and C<0 and 2+dv+log_der>=1`).  The committed Lean files
`vacuum/ReciprocalVacuum20260926.lean` and `common_action_2026_09_26/evolution/PQBridge20260926.lean`
state explicitly that they do NOT certify the exponential-function estimate; this file does.

CERTIFIED (pure real analysis; premises => conclusions):
  * `dX_hasDerivAt`   : with r(x) = r0 e^{-xi^2 x/2} and d(x) = 2 - (2-alpha)(1-r(x))^2 the derivative is
                        d'(x) = -(2-alpha) xi^2 (1-r) r   (so 2 x d'(x) = -4 (2-alpha) u r (1-r), u = xi^2 x/2).
  * `u_exp_neg_le`    : u e^{-u} <= 1/2 for u >= 0.
  * `d_window`        : 0 < d < 2 for 0 < alpha < 2, 0 <= r0 <= 1/4.
  * `two_x_dprime_ge` : 2 x d'(x) >= -4 r0.
  * `margin`          : 2 + d + 2 x d'(x) >= 1.
  * `C_I_factor`      : the integrated-stiffness expression equals the factored form of R7 (algebraic identity).
  * `A_pos`, `C_I_neg`, `all_q_signs` : for every finite x > 0, K > 0, H > 0, xi > 0,
                        A = K x d/(K H^2 + x d) > 0 and C_I < 0.

NOT CERTIFIED: the ADM derivation of the formulas A and C_I themselves (they are the hypotheses' definitions),
the value of V0, any small-q uniform coercivity, nonlinear health, the occupied gradient sector, and
r0 = ell/4 with 0 < ell <= 1 is used only as the hypothesis 0 <= r0 <= 1/4.
No physical claim is an axiom; kappa = 1/2 is not involved.
-/

noncomputable section
namespace M3A

open Real

/-- r(x) = r0 exp(-(xi^2/2) x). -/
def rr (r0 xi x : ℝ) : ℝ := r0 * Real.exp (-(xi ^ 2 / 2 * x))

/-- d(x) = alpha_e = 2 - (2 - alpha) (1 - r(x))^2. -/
def dX (alpha r0 xi x : ℝ) : ℝ := 2 - (2 - alpha) * (1 - rr r0 xi x) ^ 2

theorem rr_hasDerivAt (r0 xi x : ℝ) :
    HasDerivAt (fun y => rr r0 xi y) (-(xi ^ 2 / 2) * rr r0 xi x) x := by
  unfold rr
  have h1 : HasDerivAt (fun y : ℝ => -(xi ^ 2 / 2 * y)) (-(xi ^ 2 / 2 * 1)) x :=
    ((hasDerivAt_id' x).const_mul (xi ^ 2 / 2)).neg
  have h2 := (h1.exp).const_mul r0
  refine h2.congr_deriv ?_
  ring

theorem dX_hasDerivAt (alpha r0 xi x : ℝ) :
    HasDerivAt (fun y => dX alpha r0 xi y)
      (-(2 - alpha) * xi ^ 2 * (1 - rr r0 xi x) * rr r0 xi x) x := by
  unfold dX
  have h1 := rr_hasDerivAt r0 xi x
  have h2 := ((h1.const_sub 1).pow 2).const_mul (2 - alpha)
  have h3 := h2.const_sub 2
  refine h3.congr_deriv ?_
  ring

theorem u_exp_neg_le (u : ℝ) (hu : 0 ≤ u) : u * Real.exp (-u) ≤ 1 / 2 := by
  have h := Real.quadratic_le_exp_of_nonneg hu
  have hpos : 0 < Real.exp u := Real.exp_pos u
  have h2 : 2 * u ≤ Real.exp u := by nlinarith [sq_nonneg (u - 1)]
  rw [Real.exp_neg]
  rw [← div_eq_mul_inv]
  rw [div_le_iff₀ hpos]
  linarith

theorem rr_bounds (r0 xi x : ℝ) (h0 : 0 ≤ r0) (h1 : r0 ≤ 1 / 4) (hx : 0 ≤ x) :
    0 ≤ rr r0 xi x ∧ rr r0 xi x ≤ 1 / 4 := by
  unfold rr
  have he : 0 < Real.exp (-(xi ^ 2 / 2 * x)) := Real.exp_pos _
  constructor
  · positivity
  · have hx2 : 0 ≤ xi ^ 2 / 2 * x := by positivity
    have : Real.exp (-(xi ^ 2 / 2 * x)) ≤ 1 := by
      rw [Real.exp_le_one_iff]; linarith
    nlinarith

/-- 0 < d < 2. -/
theorem d_window (alpha r0 xi x : ℝ) (ha0 : 0 < alpha) (ha2 : alpha < 2)
    (h0 : 0 ≤ r0) (h1 : r0 ≤ 1 / 4) (hx : 0 ≤ x) :
    0 < dX alpha r0 xi x ∧ dX alpha r0 xi x < 2 := by
  obtain ⟨hr0, hr1⟩ := rr_bounds r0 xi x h0 h1 hx
  unfold dX
  have hb : 0 < 2 - alpha := by linarith
  have hq0 : 0 < 1 - rr r0 xi x := by linarith
  have hq1 : 1 - rr r0 xi x ≤ 1 := by linarith
  have hsq : (1 - rr r0 xi x) ^ 2 ≤ 1 := by nlinarith
  have hsqpos : 0 < (1 - rr r0 xi x) ^ 2 := by positivity
  constructor
  · nlinarith
  · nlinarith [mul_pos hb hsqpos]

/-- 2 x d'(x) = -4 (2-alpha) u e^{-u} r0 (1-r) with u = (xi^2/2) x, hence >= -4 r0. -/
theorem two_x_dprime_ge (alpha r0 xi x : ℝ) (ha0 : 0 < alpha) (ha2 : alpha < 2)
    (h0 : 0 ≤ r0) (h1 : r0 ≤ 1 / 4) (hx : 0 ≤ x) :
    -4 * r0 ≤ 2 * x * (-(2 - alpha) * xi ^ 2 * (1 - rr r0 xi x) * rr r0 xi x) := by
  obtain ⟨hr0, hr1⟩ := rr_bounds r0 xi x h0 h1 hx
  set u : ℝ := xi ^ 2 / 2 * x with hu
  have hu0 : 0 ≤ u := by rw [hu]; positivity
  have hue := u_exp_neg_le u hu0
  have hrr : rr r0 xi x = r0 * Real.exp (-u) := by unfold rr; rw [hu]
  have he0 : 0 < Real.exp (-u) := Real.exp_pos _
  -- 2 x xi^2 = 4 u
  have key : 2 * x * (-(2 - alpha) * xi ^ 2 * (1 - rr r0 xi x) * rr r0 xi x)
      = -4 * (2 - alpha) * (u * Real.exp (-u)) * r0 * (1 - rr r0 xi x) := by
    rw [hrr, hu]; ring
  rw [key]
  have hb : 0 < 2 - alpha := by linarith
  have hq0 : 0 ≤ 1 - rr r0 xi x := by linarith
  have hq1 : 1 - rr r0 xi x ≤ 1 := by linarith
  have hs0 : 0 ≤ u * Real.exp (-u) := by positivity
  -- (2-alpha) * s * r0 * (1-r) <= 2 * (1/2) * r0 * 1
  have hA : (2 - alpha) * (u * Real.exp (-u)) ≤ 2 * (1 / 2) := by
    apply mul_le_mul (by linarith) hue hs0 (by norm_num)
  have hB : (2 - alpha) * (u * Real.exp (-u)) * r0 * (1 - rr r0 xi x) ≤ 2 * (1 / 2) * r0 * 1 := by
    have h0' : 0 ≤ (2 - alpha) * (u * Real.exp (-u)) := by positivity
    calc (2 - alpha) * (u * Real.exp (-u)) * r0 * (1 - rr r0 xi x)
        ≤ (2 * (1 / 2)) * r0 * (1 - rr r0 xi x) := by
          apply mul_le_mul_of_nonneg_right _ hq0
          exact mul_le_mul_of_nonneg_right hA h0
      _ ≤ 2 * (1 / 2) * r0 * 1 := by
          apply mul_le_mul_of_nonneg_left hq1
          positivity
  nlinarith

/-- 2 + d + 2 x d' >= 1. -/
theorem margin (alpha r0 xi x : ℝ) (ha0 : 0 < alpha) (ha2 : alpha < 2)
    (h0 : 0 ≤ r0) (h1 : r0 ≤ 1 / 4) (hx : 0 ≤ x) :
    1 ≤ 2 + dX alpha r0 xi x
        + 2 * x * (-(2 - alpha) * xi ^ 2 * (1 - rr r0 xi x) * rr r0 xi x) := by
  have h := two_x_dprime_ge alpha r0 xi x ha0 ha2 h0 h1 hx
  have hd := (d_window alpha r0 xi x ha0 ha2 h0 h1 hx).1
  linarith

/-- The integrated-stiffness expression of check.py equals the factored form of R7. -/
theorem C_I_factor (K H x d dx : ℝ) (hden : K * H ^ 2 + x * d ≠ 0) :
    2 * x * (x * d) / (K * H ^ 2 + x * d) - 4 * x ^ 2 / (K * H ^ 2 + x * d)
      - 4 * K * H ^ 2 * x ^ 2 * (d + x * dx) / (K * H ^ 2 + x * d) ^ 2
    = -2 * x ^ 2 / (K * H ^ 2 + x * d) ^ 2
        * (K * H ^ 2 * (2 + d + 2 * x * dx) + x * d * (2 - d)) := by
  field_simp
  ring

theorem A_pos (K H x d : ℝ) (hK : 0 < K) (hH : H ≠ 0) (hx : 0 < x) (hd : 0 < d) :
    0 < K * x * d / (K * H ^ 2 + x * d) := by
  have : 0 < H ^ 2 := by positivity
  positivity

theorem C_I_neg (K H x d dx : ℝ) (hK : 0 < K) (hH : H ≠ 0) (hx : 0 < x)
    (hd : 0 < d) (hd2 : d < 2) (hm : 1 ≤ 2 + d + 2 * x * dx) :
    -2 * x ^ 2 / (K * H ^ 2 + x * d) ^ 2
        * (K * H ^ 2 * (2 + d + 2 * x * dx) + x * d * (2 - d)) < 0 := by
  have hH2 : 0 < H ^ 2 := by positivity
  have hden : 0 < (K * H ^ 2 + x * d) ^ 2 := by positivity
  have hn : 0 < K * H ^ 2 * (2 + d + 2 * x * dx) + x * d * (2 - d) := by
    have h1 : 0 < K * H ^ 2 * (2 + d + 2 * x * dx) := by
      apply mul_pos (by positivity); linarith
    have h2 : 0 < x * d * (2 - d) := by
      apply mul_pos (mul_pos hx hd); linarith
    linarith
  have hx2 : 0 < x ^ 2 := by positivity
  have : 0 < 2 * x ^ 2 / (K * H ^ 2 + x * d) ^ 2 := by positivity
  have hneg : -2 * x ^ 2 / (K * H ^ 2 + x * d) ^ 2
      = -(2 * x ^ 2 / (K * H ^ 2 + x * d) ^ 2) := by ring
  rw [hneg]
  nlinarith [mul_pos this hn]

/-- Assembled: for every finite x > 0 (any xi > 0, H != 0, K > 0, 0<alpha<2, 0<=r0<=1/4)
A > 0 and C_I < 0, with d'(x) the derivative of d. -/
theorem all_q_signs (alpha r0 xi x K H : ℝ) (ha0 : 0 < alpha) (ha2 : alpha < 2)
    (h0 : 0 ≤ r0) (h1 : r0 ≤ 1 / 4) (hx : 0 < x) (hK : 0 < K) (hH : H ≠ 0) :
    HasDerivAt (fun y => dX alpha r0 xi y)
        (-(2 - alpha) * xi ^ 2 * (1 - rr r0 xi x) * rr r0 xi x) x ∧
    0 < K * x * dX alpha r0 xi x / (K * H ^ 2 + x * dX alpha r0 xi x) ∧
    -2 * x ^ 2 / (K * H ^ 2 + x * dX alpha r0 xi x) ^ 2
      * (K * H ^ 2 * (2 + dX alpha r0 xi x
            + 2 * x * (-(2 - alpha) * xi ^ 2 * (1 - rr r0 xi x) * rr r0 xi x))
         + x * dX alpha r0 xi x * (2 - dX alpha r0 xi x)) < 0 := by
  have hw := d_window alpha r0 xi x ha0 ha2 h0 h1 hx.le
  refine ⟨dX_hasDerivAt alpha r0 xi x, A_pos K H x _ hK hH hx hw.1, ?_⟩
  exact C_I_neg K H x _ _ hK hH hx hw.1 hw.2 (margin alpha r0 xi x ha0 ha2 h0 h1 hx.le)

end M3A

#print axioms M3A.dX_hasDerivAt
#print axioms M3A.u_exp_neg_le
#print axioms M3A.d_window
#print axioms M3A.two_x_dprime_ge
#print axioms M3A.margin
#print axioms M3A.C_I_factor
#print axioms M3A.all_q_signs
