import Mathlib
open Real

noncomputable section

/-- AS054 T1: exact separation of the OR and average compositions for the
    corpus completion p(y) = y/(1+y): mu_OR(y) - mu_avg(y) = y/(1+y)^2. -/
theorem or_avg_difference (y : ℝ) (hy : y ≠ -1) :
    1 - (1 / (1 + y)) ^ 2 - y / (1 + y) = y / (1 + y) ^ 2 := by
  have h1 : 1 + y ≠ 0 := by
    intro hz
    apply hy
    linarith
  have h2 : (1 + y) ^ 2 ≠ 0 := pow_ne_zero 2 h1
  field_simp [h1, h2]
  ring

/-- AS054 T2: the OR response strictly dominates the average on the whole
    deep/intermediate domain (positive separation, completion-independent
    in shape: the difference is p(1-p) for any completion; here proven for
    the corpus member). -/
theorem or_avg_separated (y : ℝ) (hy : y > 0) : 1 - 1 / (1 + y) ^ 2 > y / (1 + y) := by
  have hyne : y ≠ -1 := by linarith
  have h1 : 1 + y ≠ 0 := by
    intro hz
    apply hyne
    linarith
  have h2 : (1 + y) ^ 2 ≠ 0 := pow_ne_zero 2 h1
  have hsq : 0 < (1 + y) ^ 2 := by nlinarith [hy]
  have hcore : (1 + y) ^ 2 - 1 > y * (1 + y) := by nlinarith [hy]
  field_simp [h1, h2, hsq]
  exact hcore

/-- AS054 T3: on the generic 2-jet p = y + c*y^2 the OR composition has
    linear coefficient exactly 2, independent of the completion coefficient c:
    mu_OR = 1 - (1 - p)^2 = 2y + (2c+1)y^2. -/
theorem or_slope_jet (y c : ℝ) :
    1 - (1 - (y + c * y ^ 2)) ^ 2 =
      2 * y + (2 * c - 1) * y ^ 2 - 2 * c * y ^ 3 - c ^ 2 * y ^ 4 := by
  ring

/-- AS054 T4: the average composition on the same generic 2-jet has linear
    coefficient exactly 1 (p itself); completion-independent. -/
theorem avg_slope_jet (y c : ℝ) : ((y + c * y ^ 2) + (y + c * y ^ 2)) / 2 = y + c * y ^ 2 := by
  ring

/-- AS054 T5: the slope gap OR - avg is exactly 1 at linear order, for every
    completion coefficient c. -/
theorem slope_gap_jet (y c : ℝ) :
    1 - (1 - (y + c * y ^ 2)) ^ 2 - (y + c * y ^ 2) =
      y + (c - 1) * y ^ 2 - 2 * c * y ^ 3 - c ^ 2 * y ^ 4 := by
  ring

/-- AS054 T6: the unequal-channel OR composition 1-(1-p)(1-q) with
    p = y + c*y^2, q = y + d*y^2 has the same origin slope 2 as the
    equal-channel OR but a different shape (quadratic coefficient c+d-1): it
    saturates at 1 and is not mu_OR for c != d. -/
theorem unequal_or_slope_jet (y c d : ℝ) :
    1 - (1 - (y + c * y ^ 2)) * (1 - (y + d * y ^ 2)) =
      2 * y + (c + d - 1) * y ^ 2 - (c + d) * y ^ 3 - c * d * y ^ 4 := by
  ring

/-- AS054 T7: saturation of the average response (corpus member): for every
    epsilon > 0 there is M >= 0 such that for all y >= M, 1 < epsilon*(1+y),
    i.e. |1 - mu_avg(y)| = 1/(1+y) < epsilon (cleared form; equivalence by
    1+y > 0). mu_avg saturates at 1: the saturation premise is satisfied by a
    non-OR composition. -/
theorem sat_avg_cleared : ∀ ε : ℝ, ε > 0 → ∃ M ≥ 0, ∀ y ≥ M, 1 < ε * (1 + y) := by
  intro ε hε
  refine ⟨1 / ε, ?M0, ?ball⟩
  · exact le_of_lt (div_pos (by norm_num) hε)
  · intro y hy
    have hMpos : 0 < 1 / ε := div_pos (by norm_num) hε
    have hy0 : 0 < y := lt_of_lt_of_le hMpos hy
    have hεinv : ε * (1 / ε) = 1 := by field_simp [hε.ne']
    have hle : 1 ≤ ε * y := by
      rw [← hεinv]
      exact mul_le_mul_of_nonneg_left hy hε.le
    nlinarith [hle, hε]

/-- AS054 T8: saturation of the OR response (corpus member): for every
    epsilon > 0 there is M >= 0 such that for all y >= M, 1 < epsilon*(1+y)^2,
    i.e. |1 - mu_OR(y)| = 1/(1+y)^2 < epsilon (cleared form). -/
theorem sat_or_cleared : ∀ ε : ℝ, ε > 0 → ∃ M ≥ 0, ∀ y ≥ M, 1 < ε * (1 + y) ^ 2 := by
  intro ε hε
  refine ⟨1 / ε, ?M0, ?ball⟩
  · exact le_of_lt (div_pos (by norm_num) hε)
  · intro y hy
    have hMpos : 0 < 1 / ε := div_pos (by norm_num) hε
    have hy0 : 0 < y := lt_of_lt_of_le hMpos hy
    have hεinv : ε * (1 / ε) = 1 := by field_simp [hε.ne']
    have hle : 1 ≤ ε * y := by
      rw [← hεinv]
      exact mul_le_mul_of_nonneg_left hy hε.le
    nlinarith [hle, hε, hy0]

/-- AS054 T9: the fractional-exponent composition member 1 - sqrt(1 - p) with
    p = y/(1+y): its complement squared equals 1/(1+y), i.e. it saturates at 1
    (as y -> infinity, sqrt(1/(1+y)) -> 0). -/
theorem frac_family_sq (y : ℝ) (hy : y > -1) :
    (Real.sqrt (1 / (1 + y))) ^ 2 = 1 / (1 + y) := by
  have hden : 0 < 1 + y := by linarith [hy]
  have hpos : 0 ≤ 1 / (1 + y) := by positivity
  exact Real.sq_sqrt hpos

/-- AS054 T10: positivity of the fractional member on the deep domain:
    1 - sqrt(1/(1+y)) > 0 for y > 0. -/
theorem frac_family_pos (y : ℝ) (hy : y > 0) : 1 - Real.sqrt (1 / (1 + y)) > 0 := by
  have hden : 0 < 1 + y := by linarith [hy]
  have hlt : 1 / (1 + y) < 1 := by
    field_simp
    linarith [hy]
  have hpos : 0 ≤ 1 / (1 + y) := by positivity
  have hs : Real.sqrt (1 / (1 + y)) < Real.sqrt 1 := Real.sqrt_lt_sqrt hpos hlt
  rw [Real.sqrt_one] at hs
  linarith

end