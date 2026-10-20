module

public import current_interactions.CurrentEnergy
public import Mathlib.Data.Rat.Cast.Order
meta import Mathlib.Tactic.NormNum

public section

open Why4.CurrentEnergy

-- A positive occupied neutral amplitude cannot be a zero-energy minimum.
theorem occupied_vacuum : neutralEnergy (1 : ℚ) 3 1 1 = 0 := by
  norm_num [neutralEnergy]
