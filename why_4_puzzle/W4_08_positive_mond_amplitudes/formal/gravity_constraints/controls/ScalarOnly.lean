module

public import gravity_constraints.GravitySelection
public import Mathlib.Data.Rat.Cast.Order
meta import Mathlib.Tactic.NormNum

public section

-- Mutation: importing scalar-only xi into the combined physical force.
theorem false_scalar_only_calibration :
    (((1 : ℚ) / (1 + 1)) * 2) ^ 2 / ((1 + 1) * 3) = 2 ^ 2 / ((1 : ℚ) * 3) := by
  norm_num
