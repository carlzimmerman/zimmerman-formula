import Mathlib
noncomputable section
namespace ActionLift
-- Algebraic consequences of the stated quadratic reduction only.
theorem reduced_gradient (b x : ℝ) :
 ((1-2*b)*x+b*x)^2-2*(1-b)*x*((1-2*b)*x+b*x)
 = -(1-b)^2*x^2 := by ring

theorem invertible_branch_stiffness (m b : ℝ) (hm : 0 < m) (hb : b ≠ 1) :
 0 < m*(1-b)^2 := by
 apply mul_pos hm
 exact sq_pos_of_ne_zero (by intro h; apply hb; linarith)

theorem positive_clock_static_scale (a q m : ℝ)
 (ha : 0 < a) (hq : 0 < q) (hm : 0 < m) :
 0 < 2*a*q^4/m := by positivity

theorem lensing_ratio (b phi : ℝ) :
 (phi+(1-2*b)*phi)/2=(1-b)*phi := by ring

#print axioms reduced_gradient
#print axioms invertible_branch_stiffness
#print axioms positive_clock_static_scale
#print axioms lensing_ratio
end ActionLift
