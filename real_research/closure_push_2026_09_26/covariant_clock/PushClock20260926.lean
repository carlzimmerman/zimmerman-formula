import Mathlib

/-! Conditional scalar positivity bridges only; no action, PDE or DOF theorem. -/
namespace PushClock20260926

theorem radial_susceptibility_positive (R q d : ℝ)
    (hR : 0 < R) (hq : 0 < q) (hd : 0 < d) :
    0 < R ^ 2 * q * (1 + 4 * q / d) := by positivity

theorem nonzero_susceptibility_response (R q d nu : ℝ)
    (hR : 0 < R) (hq : 0 < q) (hd : 0 < d) (hnu : nu ≠ 0) :
    -(R ^ 2 * q * (1 + 4 * q / d)) * nu ≠ 0 := by
  exact mul_ne_zero (neg_ne_zero.mpr (ne_of_gt (radial_susceptibility_positive R q d hR hq hd))) hnu

theorem healthy_scalar_combination_positive (A B : ℝ) (hA : 0 < A) (hB : 0 < B) :
    0 < A + 3 * B := by positivity

end PushClock20260926

#print axioms PushClock20260926.radial_susceptibility_positive
#print axioms PushClock20260926.nonzero_susceptibility_response
#print axioms PushClock20260926.healthy_scalar_combination_positive
