import Mathlib

/-! CFG665 MUTATE: each theorem below is a FALSE variant of a certified one and MUST fail to compile.
M1 local_lag with B/2 -> B; M2 nu_sqrt floor with 1/(1+sqrt2) -> 1/phi (deep form); M3 double_count upper 2 -> 3/2.
Each is also refuted positively (the `_refuted` theorems compile) so the failure is not a tactic accident. -/

namespace CFG665M
open Real

-- M1 (must FAIL)
theorem M1_local_lag_full (B : ℝ) (h0 : 0 ≤ B) (h1 : B < 1) : B ≤ 1 / Real.sqrt (1 - B) - 1 := by
  set s := Real.sqrt (1 - B)
  have hpos : 0 < 1 - B := by linarith
  have hs : 0 < s := Real.sqrt_pos.mpr hpos
  have hs2 : s ^ 2 = 1 - B := Real.sq_sqrt hpos.le
  have : B + 1 ≤ 1 / s := by rw [le_div_iff₀ hs]; nlinarith [sq_nonneg (1 - s)]
  linarith

-- M1 refuted: at B = 3/4, 1/sqrt(1/4) - 1 = 1 > 3/4 holds, but at B = 1/4 the claim needs 1/sqrt(3/4) - 1 >= 1/4,
-- i.e. sqrt(3/4) <= 4/5, false since (4/5)^2 = 16/25 < 3/4.
theorem M1_refuted : ¬ (∀ B : ℝ, 0 ≤ B → B < 1 → B ≤ 1 / Real.sqrt (1 - B) - 1) := by
  intro h
  have := h (1/4) (by norm_num) (by norm_num)
  have hs : (4/5 : ℝ) < Real.sqrt (1 - 1/4) := by
    rw [Real.lt_sqrt (by norm_num)]; norm_num
  have hsp : 0 < Real.sqrt (1 - 1/4 : ℝ) := by positivity
  have : 1 / Real.sqrt (1 - 1/4 : ℝ) < 5/4 := by
    rw [div_lt_iff₀ hsp]; linarith
  linarith

-- M2 (must FAIL): nu_sqrt deep floor with phi instead of 1 + sqrt 2
theorem M2_floor_sqrt_phi (y : ℝ) (hy : 0 < y) (hy1 : y ≤ 1) :
    Real.sqrt y / ((1 + Real.sqrt 5) / 2) ≤ (Real.sqrt (1 + 1 / y) - 1) * y := by
  nlinarith [Real.sqrt_nonneg y, Real.sqrt_nonneg (1 + 1/y), Real.sq_sqrt hy.le]

-- M2 refuted at y = 1: sqrt 2 - 1 < 1/phi = 2/(1 + sqrt 5)
theorem M2_refuted : ¬ (Real.sqrt 1 / ((1 + Real.sqrt 5) / 2) ≤ (Real.sqrt (1 + 1 / 1) - 1) * 1) := by
  rw [not_le]
  have h2 : Real.sqrt 2 < 1.4143 := by rw [Real.sqrt_lt' (by norm_num)]; norm_num
  have h5 : Real.sqrt 5 < 2.2361 := by rw [Real.sqrt_lt' (by norm_num)]; norm_num
  have h5p : 0 < (1 + Real.sqrt 5) / 2 := by positivity
  have e : (1:ℝ) + 1 / 1 = 2 := by norm_num
  rw [Real.sqrt_one, e, mul_one, lt_div_iff₀ h5p]
  nlinarith [Real.sqrt_nonneg 5, Real.sqrt_nonneg 2]

-- M3 (must FAIL)
theorem M3_double_count (F gb : ℝ) (hgb : 0 < gb) (hF : gb ≤ F) : (2 * F - gb) / F < 3 / 2 := by
  have hFp : 0 < F := lt_of_lt_of_le hgb hF
  rw [div_lt_iff₀ hFp]; linarith

-- M3 refuted: F = 10, gb = 1 gives 19/10 > 3/2
theorem M3_refuted : ¬ (∀ F gb : ℝ, 0 < gb → gb ≤ F → (2 * F - gb) / F < 3 / 2) := by
  intro h; have := h 10 1 (by norm_num) (by norm_num); norm_num at this

end CFG665M
