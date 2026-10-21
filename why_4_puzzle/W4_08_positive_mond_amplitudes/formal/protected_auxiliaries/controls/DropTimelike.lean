module

public import protected_auxiliaries.ChiralFold
public import Mathlib.Data.Rat.Cast.Order
meta import Mathlib.Tactic.NormNum

public section

open Why4.ChiralFold

-- Applying the conclusion on a spatial root after dropping x<0 is false.
theorem spatial_root_also_ghost :
    cubic (5 / 12 : ℚ) (1 / 2) = 0 ∧ 3 < (1 / 2 : ℚ) ^ 2 := by
  norm_num [cubic]
