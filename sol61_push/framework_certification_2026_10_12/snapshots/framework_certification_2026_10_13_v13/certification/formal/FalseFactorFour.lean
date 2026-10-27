import Mathlib
/- EXPECTED FAILURE: a positive dimensionless coefficient κ=1 does not force factor four. -/
example : (1 : ℝ) * 1 / (1 * Real.sqrt (1 * 1)) ^ 2 = 4 := by
  norm_num
