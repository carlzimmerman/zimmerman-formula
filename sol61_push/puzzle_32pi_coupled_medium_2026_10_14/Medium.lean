import Mathlib
noncomputable section
namespace CoupledMedium

theorem determinant_identity (A B v rho : ℝ) :
    (A-B)*(rho+A*v^2)-(A*v)^2 = (A-B)*rho-A*B*v^2 := by ring

theorem moving_medium_stronger (A B v rho : ℝ)
    (ha : 0<A) (hb : 0<B) (hr : 0<rho)
    (hd : 0<(A-B)*rho-A*B*v^2) : B<A := by
  have h : 0 ≤ A*B*v^2 := by positivity
  have hp : 0 < (A-B)*rho := by linarith
  have := (mul_pos_iff_of_pos_right hr).mp hp
  linarith

theorem low_gradient_excluded (A b v : ℝ)
    (hv : 0<v) (h : A*v ≤ b) : A-b/v ≤ 0 := by
  have hh : A ≤ b/v := (le_div_iff₀ hv).2 h
  linarith

#print axioms determinant_identity
#print axioms moving_medium_stronger
#print axioms low_gradient_excluded
end CoupledMedium
