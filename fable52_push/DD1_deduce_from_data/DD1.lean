/-
DD1 (criteria 2a3f76f295): Lean statements for the closed forms the lane uses. They certify the algebra,
not the physics. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  X_is_mass_ratio   with M = g r^2 / G for both the observed and the baryonic field, M_obs / M_b - 1 = g_obs / g_b - 1
  law_curve         X_L = (sqrt(1 + 4 a / g_b) - 1) / 2 and g = g_b (1 + X_L) solve g_b (g + a) = g^2 (the law)
  law_in_gobs       on the law, g / g_b - 1 = a / g: the law as a rule in g_obs is X g_obs = a0
  law_scale         X_L depends on g_b / a only: X_L(g_b, a) = X_L(g_b / a, 1)
  law_one_a0        two values of a that give the same X_L at one g_b are equal (a0 is identifiable from one point)
  law_mono_a        X_L increases strictly with a at fixed g_b
-/
import Mathlib

namespace DD1

open Real

noncomputable def XL (gb a : ℝ) : ℝ := (Real.sqrt (1 + 4 * a / gb) - 1) / 2

theorem X_is_mass_ratio (gobs gb r G : ℝ) (hgb : 0 < gb) (hr : 0 < r) (hG : 0 < G) :
    (gobs * r ^ 2 / G) / (gb * r ^ 2 / G) - 1 = gobs / gb - 1 := by
  have hr2 : 0 < r ^ 2 := by positivity
  field_simp

theorem law_curve (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) :
    gb * (gb * (1 + XL gb a) + a) = (gb * (1 + XL gb a)) ^ 2 := by
  unfold XL
  set s := Real.sqrt (1 + 4 * a / gb) with hs
  have h0 : 0 ≤ 1 + 4 * a / gb := by positivity
  have hsq : s ^ 2 = 1 + 4 * a / gb := by rw [hs]; exact Real.sq_sqrt h0
  have key : gb * s ^ 2 = gb + 4 * a := by rw [hsq]; field_simp
  nlinarith [key]

theorem law_in_gobs (g gb a : ℝ) (hg : 0 < g) (ha : 0 < a) (hlaw : gb = g ^ 2 / (g + a)) :
    g / gb - 1 = a / g := by
  have hga : 0 < g + a := by linarith
  have hgb : 0 < gb := by rw [hlaw]; positivity
  rw [hlaw]
  field_simp
  ring

theorem law_scale (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) : XL gb a = XL (gb / a) 1 := by
  unfold XL
  congr 2
  field_simp

theorem law_mono_a (gb a b : ℝ) (hgb : 0 < gb) (ha : 0 < a) (hab : a < b) : XL gb a < XL gb b := by
  unfold XL
  have h1 : 4 * a / gb < 4 * b / gb := by
    apply div_lt_div_of_pos_right _ hgb; linarith
  have h2 : 1 + 4 * a / gb < 1 + 4 * b / gb := by linarith
  have h0 : 0 ≤ 1 + 4 * a / gb := by positivity
  have := Real.sqrt_lt_sqrt h0 h2
  linarith

theorem law_one_a0 (gb a b : ℝ) (hgb : 0 < gb) (ha : 0 < a) (hb : 0 < b) (h : XL gb a = XL gb b) : a = b := by
  rcases lt_trichotomy a b with hab | hab | hab
  · exact absurd h (ne_of_lt (law_mono_a gb a b hgb ha hab))
  · exact hab
  · exact absurd h (ne_of_gt (law_mono_a gb b a hgb hb hab))

end DD1

#print axioms DD1.X_is_mass_ratio
#print axioms DD1.law_curve
#print axioms DD1.law_in_gobs
#print axioms DD1.law_scale
#print axioms DD1.law_mono_a
#print axioms DD1.law_one_a0

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
