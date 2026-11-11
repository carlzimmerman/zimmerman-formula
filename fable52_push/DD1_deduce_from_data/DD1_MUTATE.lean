/-
DD1 MUTATE twin: false versions of the statements in DD1.lean. Every theorem here is false (or its proof does not go
through) and this file must FAIL to compile. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace DD1_MUTATE

open Real

noncomputable def XL (gb a : ℝ) : ℝ := (Real.sqrt (1 + 4 * a / gb) - 1) / 2

-- false: drops the -1
theorem X_is_mass_ratio_false (gobs gb r G : ℝ) (hgb : 0 < gb) (hr : 0 < r) (hG : 0 < G) :
    (gobs * r ^ 2 / G) / (gb * r ^ 2 / G) - 1 = gobs / gb := by
  have hr2 : 0 < r ^ 2 := by positivity
  field_simp

-- false: an extra + a on the right
theorem law_curve_false (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) :
    gb * (gb * (1 + XL gb a) + a) = (gb * (1 + XL gb a)) ^ 2 + a := by
  unfold XL
  set s := Real.sqrt (1 + 4 * a / gb) with hs
  have h0 : 0 ≤ 1 + 4 * a / gb := by positivity
  have hsq : s ^ 2 = 1 + 4 * a / gb := by rw [hs]; exact Real.sq_sqrt h0
  have key : gb * s ^ 2 = gb + 4 * a := by rw [hsq]; field_simp
  nlinarith [key]

-- false: a / g_bar in place of a / g
theorem law_in_gobs_false (g gb a : ℝ) (hg : 0 < g) (ha : 0 < a) (hlaw : gb = g ^ 2 / (g + a)) :
    g / gb - 1 = a / gb := by
  have hga : 0 < g + a := by linarith
  have hgb : 0 < gb := by rw [hlaw]; positivity
  rw [hlaw]
  field_simp
  ring

-- false: g_bar * a in place of g_bar / a
theorem law_scale_false (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) : XL gb a = XL (gb * a) 1 := by
  unfold XL
  congr 2
  field_simp

-- false: decreasing in a
theorem law_mono_a_false (gb a b : ℝ) (hgb : 0 < gb) (ha : 0 < a) (hab : a < b) : XL gb b < XL gb a := by
  unfold XL
  have h1 : 4 * a / gb < 4 * b / gb := by
    apply div_lt_div_of_pos_right _ hgb; linarith
  have h2 : 1 + 4 * a / gb < 1 + 4 * b / gb := by linarith
  have h0 : 0 ≤ 1 + 4 * a / gb := by positivity
  have := Real.sqrt_lt_sqrt h0 h2
  linarith

end DD1_MUTATE

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
