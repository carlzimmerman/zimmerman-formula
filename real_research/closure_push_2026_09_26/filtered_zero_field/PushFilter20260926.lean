import Mathlib

/-! Finite-mode Cauchy--Schwarz bridge for the heat-smoothed force.
The continuum Fourier representation, Gaussian summability, and ODE theorem
remain analytic dependencies; this file does not certify the coupled PDE. -/
namespace PushFilter20260926
open scoped BigOperators

theorem finite_mode_derivative_bound {ι : Type*} (s : Finset ι)
    (weight amplitude : ι → ℝ) :
    (∑ i ∈ s, weight i * amplitude i)^2 ≤
      (∑ i ∈ s, (weight i)^2) * (∑ i ∈ s, (amplitude i)^2) := by
  exact Finset.sum_mul_sq_le_sq_mul_sq s weight amplitude

theorem heat_mode_bound {ι : Type*} (s : Finset ι)
    (frequency amplitude : ι → ℝ) (xi : ℝ) :
    (∑ i ∈ s, (frequency i * Real.exp (-(xi*frequency i)^2/2)) * amplitude i)^2 ≤
      (∑ i ∈ s, (frequency i * Real.exp (-(xi*frequency i)^2/2))^2) *
      (∑ i ∈ s, (amplitude i)^2) := by
  exact finite_mode_derivative_bound s _ _

theorem square_root_response_not_linear (eps bound : ℝ)
    (he : 0 < eps) (hb : 0 < bound) (hsmall : eps*bound^2 < 1) :
    bound*eps < Real.sqrt eps := by
  have hp : 0 < Real.sqrt eps := Real.sqrt_pos.2 he
  have hs := Real.sq_sqrt he.le
  have hm := mul_lt_mul_of_pos_left hsmall he
  nlinarith [mul_pos hb he]

#print axioms finite_mode_derivative_bound
#print axioms heat_mode_bound
#print axioms square_root_response_not_linear
end PushFilter20260926
