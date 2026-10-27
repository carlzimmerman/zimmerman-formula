import Mathlib

namespace SectorSelection32Pi

theorem action_square (v z m b : ℝ) (hv : v ≠ 0) :
    v*z^2-2*m*b*z = v*(z-m*b/v)^2-m^2*b^2/v := by
  field_simp
  <;> ring

theorem continuous_minimum (v z m b : ℝ) (hv : 0 < v) :
    -(m^2*b^2/v) ≤ v*z^2-2*m*b*z := by
  rw [action_square v z m b (ne_of_gt hv)]
  have h := mul_nonneg (le_of_lt hv) (sq_nonneg (z-m*b/v))
  linarith

theorem zero_offset_order (m l w : ℝ) (hm : 0 < m)
    (hl : 0 < l) (hw : 0 < w) : w*(3*0-2*m*l) < 0 := by
  have h : 0 < w*(2*m*l) := by positivity
  nlinarith

theorem shifted_offset_order (m l w : ℝ) (hm : 0 < m)
    (hl : 0 < l) (hw : 0 < w) : 0 < w*(3*(m*l)-2*m*l) := by
  have h : 0 < w*m*l := by positivity
  nlinarith

#print axioms action_square
#print axioms continuous_minimum
#print axioms zero_offset_order
#print axioms shifted_offset_order
end SectorSelection32Pi
