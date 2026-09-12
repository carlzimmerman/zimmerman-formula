import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith

namespace TurningBound
theorem maximum_factorization (z : ℝ) :
    4*(1+z)^3-27*z = (2*z-1)^2*(z+4) := by ring

theorem profile_bound_polynomial (z : ℝ) (hz : 0 < z) :
    27*z ≤ 4*(1+z)^3 := by
  have h : 0 ≤ (2*z-1)^2*(z+4) :=
    mul_nonneg (sq_nonneg _) (by linarith)
  rw [← maximum_factorization] at h
  linarith

theorem turning_necessary_beta_bound (beta d ell z : ℝ)
    (hell : 0 < ell) (hz : 0 < z)
    (hroot : 9*ell*beta^2*(1+z)^3 = 4*d^2*z) :
    243*ell*beta^2 ≤ 16*d^2 := by
  have hz3 : 0 < (1+z)^3 := pow_pos (by linarith) _
  have hprofile := profile_bound_polynomial z hz
  have hprod := mul_nonneg (sq_nonneg d) (sub_nonneg.mpr hprofile)
  nlinarith [hroot]

#print axioms maximum_factorization
#print axioms profile_bound_polynomial
#print axioms turning_necessary_beta_bound
end TurningBound
