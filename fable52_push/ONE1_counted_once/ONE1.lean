/-
ONE1 (criteria a967a38851): Lean statements for the counted-once halo. They certify the algebra the lane's model uses, not the
physics and not the data. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

Setting. x = r / r_M, r_M = sqrt(G M_b / a0). The law's own halo has enclosed mass M(<r) / M_b = m(x) = nu(1 / x^2)
= 1/2 + sqrt(1/4 + x^2). It holds a share X M_b, so it ends where m = 1 + X and the enclosed mass is 1 + X beyond:
mt X x = min (m x) (1 + X).

  end_radius        : for X, x >= 0, m x = 1 + X iff x^2 = X (X + 1).
  continuity        : m (sqrt (X (X + 1))) = 1 + X: the enclosed mass is continuous at the end radius.
  far_ratio         : a point of (1 + X) M_b over the isothermal form, ((1 + X) / (pi u^2)) / (1 / (4 u)) = 4 (1 + X) / (pi u).
  m_mono            : m is monotone on x >= 0 (enclosed mass grows outward).
  mt_le_m           : the truncated halo never holds more than the law's.
  mt_mono_X         : the truncated enclosed mass is monotone in X.
  inner_unaffected  : inside the end radius the truncated halo is the law's halo.
  outer_point       : beyond the end radius the enclosed mass is 1 + X.
  shell_lowers      : a thin shell outside a projected radius lowers DeltaSigma there:
                      for 0 < c < 1 (c = sqrt(1 - R^2 / s^2)), (1 - c) / (1 - c^2) - 1 / (2 c) < 0.
  ratio_mono        : an outer amplitude that does not fall and a positive inner amplitude that does not rise give a ratio that
                      does not fall (the shape-ratio lemma; that the projected stack meets its premises is checked numerically).
-/
import Mathlib

namespace ONE1

noncomputable def m (x : ℝ) : ℝ := 1 / 2 + Real.sqrt (1 / 4 + x ^ 2)

noncomputable def mt (X x : ℝ) : ℝ := min (m x) (1 + X)

theorem end_radius (X x : ℝ) (hX : 0 ≤ X) (_hx : 0 ≤ x) : m x = 1 + X ↔ x ^ 2 = X * (X + 1) := by
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

theorem continuity (X : ℝ) (hX : 0 ≤ X) : m (Real.sqrt (X * (X + 1))) = 1 + X := by
  have hp : 0 ≤ X * (X + 1) := by positivity
  have hx : 0 ≤ Real.sqrt (X * (X + 1)) := Real.sqrt_nonneg _
  exact (end_radius X _ hX hx).mpr (Real.sq_sqrt hp)

theorem far_ratio (X u : ℝ) (hu : 0 < u) :
    ((1 + X) / (Real.pi * u ^ 2)) / (1 / (4 * u)) = 4 * (1 + X) / (Real.pi * u) := by
  have hpi : 0 < Real.pi := Real.pi_pos
  field_simp

theorem m_mono (x y : ℝ) (hx : 0 ≤ x) (hxy : x ≤ y) : m x ≤ m y := by
  unfold m
  have h : 1 / 4 + x ^ 2 ≤ 1 / 4 + y ^ 2 := by nlinarith
  have := Real.sqrt_le_sqrt h
  linarith

theorem mt_le_m (X x : ℝ) : mt X x ≤ m x := min_le_left _ _

theorem mt_mono_X (X Y x : ℝ) (hXY : X ≤ Y) : mt X x ≤ mt Y x := by
  unfold mt
  exact min_le_min le_rfl (by linarith)

theorem inner_unaffected (X x : ℝ) (hX : 0 ≤ X) (hx : 0 ≤ x) (hin : x ≤ Real.sqrt (X * (X + 1))) : mt X x = m x := by
  unfold mt
  apply min_eq_left
  have h1 := m_mono x _ hx hin
  rw [continuity X hX] at h1
  exact h1

theorem outer_point (X x : ℝ) (hX : 0 ≤ X) (hout : Real.sqrt (X * (X + 1)) ≤ x) : mt X x = 1 + X := by
  unfold mt
  apply min_eq_right
  have h1 := m_mono _ x (Real.sqrt_nonneg _) hout
  rw [continuity X hX] at h1
  exact h1

theorem shell_lowers (c : ℝ) (hc0 : 0 < c) (hc1 : c < 1) : (1 - c) / (1 - c ^ 2) - 1 / (2 * c) < 0 := by
  have h1 : 0 < 1 - c ^ 2 := by nlinarith
  have h2 : (1 - c) / (1 - c ^ 2) = 1 / (1 + c) := by
    rw [div_eq_div_iff (ne_of_gt h1) (by linarith)]
    ring
  have h3 : 1 / (1 + c) < 1 / (2 * c) := one_div_lt_one_div_of_lt (by linarith) (by linarith)
  rw [h2]
  linarith

theorem ratio_mono (aX aY bX bY : ℝ) (ha : 0 ≤ aX) (hab : aX ≤ aY) (hb : bY ≤ bX) (hbY : 0 < bY) :
    aX / bX ≤ aY / bY := by
  have hbX : 0 < bX := lt_of_lt_of_le hbY hb
  have hd : aY / bY - aX / bX = (aY * bX - aX * bY) / (bX * bY) := by
    field_simp
  have hn : 0 ≤ aY * bX - aX * bY := by nlinarith
  have hq : 0 ≤ (aY * bX - aX * bY) / (bX * bY) := div_nonneg hn (by positivity)
  linarith

end ONE1

#print axioms ONE1.end_radius
#print axioms ONE1.continuity
#print axioms ONE1.far_ratio
#print axioms ONE1.m_mono
#print axioms ONE1.mt_le_m
#print axioms ONE1.mt_mono_X
#print axioms ONE1.inner_unaffected
#print axioms ONE1.outer_point
#print axioms ONE1.shell_lowers
#print axioms ONE1.ratio_mono
