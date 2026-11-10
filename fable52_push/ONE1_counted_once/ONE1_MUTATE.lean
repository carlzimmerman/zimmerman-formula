/-
ONE1 MUTATE twin: false versions of ONE1.lean's statements, each with the same proof script. Every one must fail to compile.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  end_radius_wrong      : x^2 = X^2 in place of X (X + 1).
  continuity_wrong      : the enclosed mass at the end radius is X, not 1 + X.
  far_ratio_wrong       : 2 (1 + X) / (pi u) in place of 4 (1 + X) / (pi u).
  inner_wrong           : inside the end radius the truncated halo is already the point mass 1 + X.
  shell_raises          : a thin shell outside a projected radius raises DeltaSigma there.
  ratio_mono_wrong      : the shape ratio falls when the outer amplitude rises and the inner one falls.
-/
import Mathlib

namespace ONE1M

noncomputable def m (x : ℝ) : ℝ := 1 / 2 + Real.sqrt (1 / 4 + x ^ 2)

noncomputable def mt (X x : ℝ) : ℝ := min (m x) (1 + X)

theorem end_radius_wrong (X x : ℝ) (hX : 0 ≤ X) (_hx : 0 ≤ x) : m x = 1 + X ↔ x ^ 2 = X ^ 2 := by
  have hs : 0 ≤ 1 / 4 + x ^ 2 := by positivity
  constructor
  · intro h
    have h1 : Real.sqrt (1 / 4 + x ^ 2) = X + 1 / 2 := by unfold m at h; linarith
    have h2 := Real.sq_sqrt hs
    rw [h1] at h2
    nlinarith
  · intro h
    unfold m
    have h3 : 1 / 4 + x ^ 2 = (X + 1 / 2) ^ 2 := by nlinarith
    rw [h3, Real.sqrt_sq (by linarith)]
    ring

theorem continuity_wrong (X : ℝ) (hX : 0 ≤ X) : m (Real.sqrt (X * (X + 1))) = X := by
  have hp : 0 ≤ X * (X + 1) := by positivity
  unfold m
  rw [Real.sq_sqrt hp]
  have h3 : 1 / 4 + X * (X + 1) = (X + 1 / 2) ^ 2 := by ring
  rw [h3, Real.sqrt_sq (by linarith)]
  ring

theorem far_ratio_wrong (X u : ℝ) (hu : 0 < u) :
    ((1 + X) / (Real.pi * u ^ 2)) / (1 / (4 * u)) = 2 * (1 + X) / (Real.pi * u) := by
  have hpi : 0 < Real.pi := Real.pi_pos
  field_simp

theorem m_mono (x y : ℝ) (hx : 0 ≤ x) (hxy : x ≤ y) : m x ≤ m y := by
  unfold m
  have h : 1 / 4 + x ^ 2 ≤ 1 / 4 + y ^ 2 := by nlinarith
  have := Real.sqrt_le_sqrt h
  linarith

theorem inner_wrong (X x : ℝ) (hX : 0 ≤ X) (hx : 0 ≤ x) (hin : x ≤ Real.sqrt (X * (X + 1))) : mt X x = 1 + X := by
  unfold mt
  apply min_eq_right
  have h1 := m_mono x _ hx hin
  linarith

theorem shell_raises (c : ℝ) (hc0 : 0 < c) (hc1 : c < 1) : 0 < (1 - c) / (1 - c ^ 2) - 1 / (2 * c) := by
  have h1 : 0 < 1 - c ^ 2 := by nlinarith
  have h2 : (1 - c) / (1 - c ^ 2) = 1 / (1 + c) := by
    rw [div_eq_div_iff (ne_of_gt h1) (by linarith)]
    ring
  have h3 : 1 / (1 + c) < 1 / (2 * c) := one_div_lt_one_div_of_lt (by linarith) (by linarith)
  rw [h2]
  linarith

theorem ratio_mono_wrong (aX aY bX bY : ℝ) (ha : 0 ≤ aX) (hab : aX ≤ aY) (hb : bY ≤ bX) (hbY : 0 < bY) :
    aY / bY ≤ aX / bX := by
  have hbX : 0 < bX := lt_of_lt_of_le hbY hb
  have hd : aY / bY - aX / bX = (aY * bX - aX * bY) / (bX * bY) := by
    field_simp
  have hn : 0 ≤ aY * bX - aX * bY := by nlinarith
  have hq : 0 ≤ (aY * bX - aX * bY) / (bX * bY) := div_nonneg hn (by positivity)
  linarith

end ONE1M
