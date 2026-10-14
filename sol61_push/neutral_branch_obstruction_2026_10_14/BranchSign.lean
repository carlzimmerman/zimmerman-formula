import Mathlib

-- Conditional algebraic sign results. The physical reduction and derivative
-- identity are derived in REPORT.md and checked separately by symbolic algebra.
theorem branch_pressure_negative (D δ g H : ℝ)
    (hδ : 0 < δ) (hD : δ < D) (hB : 0 < H - g * D) :
    (-(D - δ) / 2) * (D * (D - δ) / (2 * (H - g * D))) < 0 := by
  have ht : 0 < D - δ := sub_pos.mpr hD
  have hd : 0 < D := lt_trans hδ hD
  have hx : 0 < D * (D - δ) / (2 * (H - g * D)) := by positivity
  have hm : -(D - δ) / 2 < 0 := by linarith
  exact mul_neg_of_neg_of_pos hm hx

theorem branch_inverse_slope_negative (D δ g H : ℝ)
    (hδ : 0 < δ) (hD : δ < D) (hg : 0 < g) (hH : 0 < H)
    (hB : 0 < H - g * D) :
    -(1 : ℝ) / (2 *
      (((2 * D - δ) * (H - g * D) + g * D * (D - δ)) /
          (H - g * D)^2 +
        H * (D - δ) * ((H - g * D) + g * (D - δ)) /
          (H - g * D)^3)) < 0 := by
  have ht : 0 < D - δ := sub_pos.mpr hD
  have hd : 0 < D := lt_trans hδ hD
  have htwo : 0 < 2 * D - δ := by linarith
  have hp : 0 <
      ((2 * D - δ) * (H - g * D) + g * D * (D - δ)) /
          (H - g * D)^2 +
        H * (D - δ) * ((H - g * D) + g * (D - δ)) /
          (H - g * D)^3 := by positivity
  exact div_neg_of_neg_of_pos (by norm_num) (by positivity)
