import Mathlib
noncomputable section
namespace ResponseCone
theorem radial_speed_gt_two (a u : ℝ) (hu : 0<u) (ha : u<a) :
    2 < (2*a-u)/(a-u) := by
  apply (lt_div_iff₀ (by linarith : 0<a-u)).2
  linarith

theorem vacuum_response_zero (k alpha : ℝ) (ha : alpha ≠ 0)
    (h : k/alpha^2=0) : k=0 := by
  exact (div_eq_zero_iff).mp h |>.resolve_right (pow_ne_zero _ ha)

theorem regulated_force_lower_bound (u a k alpha : ℝ)
    (ha : 0<a) : k*u/alpha^2 ≤ k*u/alpha^2+u^2/a := by
  have h : 0 ≤ u^2/a := div_nonneg (sq_nonneg _) (le_of_lt ha)
  linarith

theorem conformal_lensing (psi phi shift : ℝ) :
    (psi+shift)+(phi-shift)=psi+phi := by ring

#print axioms radial_speed_gt_two
#print axioms vacuum_response_zero
#print axioms regulated_force_lower_bound
#print axioms conformal_lensing
end ResponseCone
