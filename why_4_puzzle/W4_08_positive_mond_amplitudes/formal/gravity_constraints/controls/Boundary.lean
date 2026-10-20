module

public import gravity_constraints.GravitySelection
public import Mathlib.Data.Rat.Cast.Order
meta import Mathlib.Tactic.NormNum

public section

-- Mutation: keeping the static z^2 term after the redshift boundary.
theorem false_retained_restoring_term :
    (1 : ℚ) * (2 * 1 ^ 2 + 4 * 1 * 0 / 1 + 2 * 0 ^ 2 / 1 ^ 2) -
      (2 / 1) * (3 * 1 * 1 * 1 ^ 2 - 2 * 1 * 1 * 1 ^ 2 + 2 * 1 * 1 * 0) = 2 := by
  norm_num
