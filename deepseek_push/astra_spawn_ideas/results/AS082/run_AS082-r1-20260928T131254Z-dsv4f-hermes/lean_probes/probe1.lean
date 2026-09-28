import Mathlib

noncomputable section

-- probe: shapes needed by AS082 certificate (4.34.0-rc2 build)
#check intervalIntegral.integral_const
#check smul_eq_mul
#check mul_left_cancel₀
#check sub_eq_zero
#check mul_eq_zero

example (A r_in r : ℝ) :
    ∫ x in r_in..r, (4 * Real.pi * A) = 4 * Real.pi * A * (r - r_in) := by
  rw [intervalIntegral.integral_const]
  rw [smul_eq_mul]
  ring

example (r_in : ℝ) : r_in ≠ r_in + 1 := by
  linarith

end
