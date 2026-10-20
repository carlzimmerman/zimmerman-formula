module
public import PairedBandStress
public import Mathlib.Data.Rat.Cast.Order
meta import Mathlib.Tactic.NormNum

public section
open Why4.PairedBandStress

-- Deliberately false vacuum claim; offset=7 cancels only vacuum stress.
example : energy (1 : ℚ) 1 (3 / 4) (5 / 4) + 7 +
    (pressure (1 : ℚ) 1 (3 / 4) (5 / 4) - 7) = 0 := by
  norm_num [energy, shape, nullStress, pressure]
