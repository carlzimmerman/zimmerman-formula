/-
NSW1 MUTATE twin: false versions of five NSW1 statements, with the proofs that close the true ones. This file must FAIL to
compile.
  Wg_by_parts_M        : A2 with the wrong power of 1 + u (cube in place of square)
  stress_jump_M        : the tangential term dropped (the stress jump claimed equal to SWT1's W(u) for every n)
  Wg_le_normal_flux_M  : a false bound, W_g <= d (the normal flux alone, as if the wall were always an equipotential)
  gout_sq_bound_M      : a false bound, W_g^2 <= |g_out|^2 / 2
  hasDerivAt_G_M       : the antiderivative step without the switch factor (1 - d / sqrt(v^2 - e_t^2))
kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace NSW1M

noncomputable def J (u : ℝ) : ℝ := u - Real.log (1 + u)
noncomputable def W (u : ℝ) : ℝ := u - Real.log (1 + u) - u ^ 2 / (2 * (1 + u) ^ 2)
noncomputable def Wg (u n : ℝ) : ℝ := u - Real.log (1 + u) - n ^ 2 / (2 * (1 + u) ^ 2)

theorem Wg_by_parts_M (u n : ℝ) (hu : 0 ≤ u) :
    J u * 1 - ((u ^ 2 / 2 - (n * u / (1 + u)) * n)
      - (((n * u / (1 + u)) ^ 2 + (u ^ 2 - n ^ 2)) / 2 - (n * u / (1 + u)) * (n * u / (1 + u))))
      = u - Real.log (1 + u) - n ^ 2 / (2 * (1 + u) ^ 3) := by
  unfold J
  have h : (1 + u) ≠ 0 := by positivity
  field_simp
  ring

theorem stress_jump_M (u n : ℝ) (hu : 0 ≤ u) :
    ((u ^ 2 - n ^ 2) - (n * u / (1 + u)) ^ 2) / 2 - (-(n * u / (1 + u)) * n + u ^ 2 / 2 - J u) = W u := by
  unfold J W
  have h : (1 + u) ≠ 0 := by positivity
  field_simp
  ring

theorem Wg_le_normal_flux_M (u n : ℝ) (hu : 0 ≤ u) (hn0 : 0 ≤ n) (hnu : n ≤ u) : Wg u n ≤ n * u / (1 + u) := by
  unfold Wg
  have hp : 0 < 1 + u := by linarith
  have hlog : 1 - (1 + u)⁻¹ ≤ Real.log (1 + u) := Real.one_sub_inv_le_log_of_pos hp
  have h2 : 0 ≤ n ^ 2 / (2 * (1 + u) ^ 2) := by positivity
  have h3 : u - (1 - (1 + u)⁻¹) = u ^ 2 / (1 + u) := by
    field_simp
    ring
  linarith

theorem gout_sq_bound_M (u j t : ℝ) (hu : 0 < u) (hj0 : 0 ≤ j) (hju : j ≤ u)
    (hw0 : 0 ≤ j - u ^ 2 / (2 * (1 + u) ^ 2)) (hwy : j - u ^ 2 / (2 * (1 + u) ^ 2) ≤ u ^ 2 / (1 + u))
    (ht0 : 0 ≤ t) (htu : t ≤ u ^ 2) :
    (j - t / (2 * (1 + u) ^ 2)) ^ 2 ≤ (t * u ^ 2 / (1 + u) ^ 2 + (u ^ 2 - t)) / 2 := by
  have hp : (1 + u) ≠ 0 := by positivity
  have key : u ^ 2 * ((t * u ^ 2 / (1 + u) ^ 2 + (u ^ 2 - t)) / 2 - (j - t / (2 * (1 + u) ^ 2)) ^ 2)
      = (u ^ 2 - t) * (u ^ 2 - j ^ 2)
        + t * ((u ^ 2 / (1 + u)) ^ 2 - (j - u ^ 2 / (2 * (1 + u) ^ 2)) ^ 2)
        + (1 / (2 * (1 + u) ^ 2)) ^ 2 * u ^ 2 * t * (u ^ 2 - t) := by
    field_simp
    ring
  have h1 : 0 ≤ (u ^ 2 - t) * (u ^ 2 - j ^ 2) := by
    apply mul_nonneg (by linarith)
    nlinarith [mul_nonneg (sub_nonneg.mpr hju) (add_nonneg hu.le hj0)]
  have h2 : 0 ≤ t * ((u ^ 2 / (1 + u)) ^ 2 - (j - u ^ 2 / (2 * (1 + u) ^ 2)) ^ 2) := by
    apply mul_nonneg ht0
    nlinarith [mul_nonneg (sub_nonneg.mpr hwy) (add_nonneg (le_trans hw0 hwy) hw0)]
  have h3 : 0 ≤ (1 / (2 * (1 + u) ^ 2)) ^ 2 * u ^ 2 * t * (u ^ 2 - t) := by
    have hc : 0 ≤ (1 / (2 * (1 + u) ^ 2)) ^ 2 * u ^ 2 := by positivity
    exact mul_nonneg (mul_nonneg hc ht0) (by linarith)
  have hX : 0 ≤ u ^ 2 * ((t * u ^ 2 / (1 + u) ^ 2 + (u ^ 2 - t)) / 2 - (j - t / (2 * (1 + u) ^ 2)) ^ 2) := by
    rw [key]; linarith
  have hu2 : 0 < u ^ 2 := by positivity
  have hY : 0 ≤ (t * u ^ 2 / (1 + u) ^ 2 + (u ^ 2 - t)) / 2 - (j - t / (2 * (1 + u) ^ 2)) ^ 2 := by
    by_contra hneg
    rw [not_le] at hneg
    have := mul_neg_of_pos_of_neg hu2 hneg
    linarith
  linarith

theorem hasDerivAt_G_M (d e2 v : ℝ) (hv : 0 < v) (hpos : 0 < v ^ 2 - e2) :
    HasDerivAt (fun x : ℝ => x ^ 2 / 2 - d * Real.sqrt (x ^ 2 - e2)) ((1 + v) * (v / (1 + v))) v := by
  have hs : 0 < Real.sqrt (v ^ 2 - e2) := Real.sqrt_pos.mpr hpos
  have hs' : Real.sqrt (v ^ 2 - e2) ≠ 0 := ne_of_gt hs
  have hp : (1 + v) ≠ 0 := by positivity
  have hn : HasDerivAt (fun x : ℝ => x ^ 2) (2 * v) v := by
    simpa using hasDerivAt_pow 2 v
  have h1 : HasDerivAt (fun x : ℝ => x ^ 2 - e2) (2 * v) v := hn.sub_const e2
  have h2 : HasDerivAt (fun x : ℝ => Real.sqrt (x ^ 2 - e2)) (2 * v / (2 * Real.sqrt (v ^ 2 - e2))) v :=
    h1.sqrt (ne_of_gt hpos)
  have h3 : HasDerivAt (fun x : ℝ => x ^ 2 / 2) (2 * v / 2) v := hn.div_const 2
  have h4 : HasDerivAt (fun x : ℝ => x ^ 2 / 2 - d * Real.sqrt (x ^ 2 - e2))
      (2 * v / 2 - d * (2 * v / (2 * Real.sqrt (v ^ 2 - e2)))) v := h3.sub (h2.const_mul d)
  have hderiv : 2 * v / 2 - d * (2 * v / (2 * Real.sqrt (v ^ 2 - e2))) = (1 + v) * (v / (1 + v)) := by
    field_simp
  exact h4.congr_deriv hderiv

end NSW1M
