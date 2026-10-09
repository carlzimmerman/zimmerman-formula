import Mathlib
/-! MUTATE for TORUS_WL1: FALSE, must fail — a LIGHT pair (x, x, y) with y > x can never satisfy Koide
(false: y = (4 + 3√2) x works). -/
theorem mutate_light_pair_never (x y : ℝ) (hx : 0 < x) (hxy : x < y) :
    (2 * x ^ 2 + y ^ 2) / (2 * x + y) ^ 2 ≠ 2 / 3 := by
  have hpos : (2 * x + y) ^ 2 ≠ 0 := by nlinarith
  rw [Ne, div_eq_iff hpos]
  intro h
  nlinarith [mul_pos hx hx, mul_pos hx (lt_trans hx hxy)]
