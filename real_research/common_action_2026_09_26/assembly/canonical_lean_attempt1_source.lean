import Mathlib

/-! Algebraic bridges only. The direct-method continuum argument is in
CANONICAL_AUXILIARY.md and is not formalized by these declarations. -/
namespace CanonicalAuxiliary20260926

theorem carrier_legendre (A B v W : ℝ) (hA : A ≠ 0) :
    (A*v)*v - (A*v^2/2-B*W) = (A*v)^2/(2*A)+B*W := by
  field_simp
  ring

theorem auxiliary_square_completion (a z u alpha cN : ℝ)
    (hc : cN = 1-alpha/2) :
    alpha*(a-z)^2+4*a*z-2*z^2-4*cN*z*u =
      alpha*a^2-2*cN*(z-(a-u))^2+2*cN*(a-u)^2 := by
  subst cN
  ring

theorem shifted_square_coercive (p b : ℝ) :
    p^2/2-b^2 ≤ (p-b)^2 := by
  nlinarith [sq_nonneg (p-2*b)]

theorem canonical_hessian_lower_bound (m grad2 rho v : ℝ)
    (hr : 0 ≤ rho) :
    2*m*grad2 ≤ 2*m*grad2+rho*v^2 := by
  have : 0 ≤ rho*v^2 := mul_nonneg hr (sq_nonneg v)
  linarith

theorem canonical_hessian_strict (m grad2 rho v : ℝ)
    (hm : 0 < m) (hg : 0 < grad2) (hr : 0 ≤ rho) :
    0 < 2*m*grad2+rho*v^2 := by
  have hp : 0 < 2*m*grad2 := by positivity
  have hn : 0 ≤ rho*v^2 := mul_nonneg hr (sq_nonneg v)
  linarith

end CanonicalAuxiliary20260926
#print axioms CanonicalAuxiliary20260926.carrier_legendre
#print axioms CanonicalAuxiliary20260926.auxiliary_square_completion
#print axioms CanonicalAuxiliary20260926.shifted_square_coercive
#print axioms CanonicalAuxiliary20260926.canonical_hessian_lower_bound
#print axioms CanonicalAuxiliary20260926.canonical_hessian_strict
