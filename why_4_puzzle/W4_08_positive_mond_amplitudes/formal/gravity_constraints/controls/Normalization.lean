module

public import gravity_constraints.GravitySelection
public import Mathlib.Data.Rat.Cast.Order
meta import Mathlib.Tactic.NormNum

public section

-- Mutation: doubling the MOND cubic while asserting unchanged amplitude.
theorem false_deformation_invariance :
    (3 : ℚ) * ((1 + 1) * 5) ^ 2 / 2 ^ 3 = (3 : ℚ) * 5 ^ 2 / 2 ^ 3 := by
  norm_num
