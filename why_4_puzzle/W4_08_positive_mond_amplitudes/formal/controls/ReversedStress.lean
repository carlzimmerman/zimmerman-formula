module
public import PairedBandStress
public import Mathlib.Data.Rat.Cast.Order
meta import Mathlib.Tactic.NormNum

public section
open Why4.PairedBandStress

-- Deliberately false after changing the physical band's null-stress sign.
example : energy (1 : ℚ) 1 (3 / 4) (5 / 4) / 2 <
    -nullStress (1 : ℚ) 1 (3 / 4) (5 / 4) := by
  norm_num [energy, shape, nullStress]
