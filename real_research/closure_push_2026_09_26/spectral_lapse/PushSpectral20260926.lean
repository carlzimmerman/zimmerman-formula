import Mathlib

/-! Algebraic bridges for the nonlinear positive-lapse construction.
Spatial integration, weighted Poincare, and constraint preservation are not
formalized here. No full gravity certificate is asserted. -/
namespace PushSpectral20260926

theorem log_lapse_to_linear_equation (A b y y1 y2 : ℝ) (hy : y ≠ 0) :
    A+b*((2*y1/y)^2+2*(2*y2/y-2*(y1/y)^2)) = A+4*b*y2/y := by
  field_simp
  <;> ring

theorem ground_state_factorization_density (y y1 y2 f f1 : ℝ)
    (hy : y ≠ 0) :
    (y1*f+y*f1)^2+(y2/y)*(y*f)^2-y^2*f1^2 =
      y1^2*f^2+2*y*f*f1*y1+y*f^2*y2 := by
  field_simp
  <;> ring

theorem fixed_action_global_constraint (ell q Lambda rho0 A : ℝ)
    (hq : ell*q^2 = Lambda+rho0) :
    -ell*q^2+Lambda+(rho0+A)=A := by linarith

theorem source_density_positive (rho0 A bound : ℝ)
    (hA : -bound ≤ A) (hr : bound < rho0) : 0 < rho0+A := by linarith

theorem positive_lapse_from_positive_root (y : ℝ) (hy : 0 < y) : 0 < y^2 := by positivity

#print axioms log_lapse_to_linear_equation
#print axioms ground_state_factorization_density
#print axioms fixed_action_global_constraint
#print axioms source_density_positive
#print axioms positive_lapse_from_positive_root
end PushSpectral20260926
