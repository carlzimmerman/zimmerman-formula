module

public import Mathlib.Data.Rat.Cast.Order
meta import Mathlib.Tactic.NormNum

public section

-- Positive propagating quadratic coefficients do not make this Jacobian positive.
theorem fold_jacobian_positive : (6 : ℚ) - 6 * 1 ^ 2 > 0 := by
  norm_num
