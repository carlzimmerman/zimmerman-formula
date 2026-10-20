module

public import clock_flux.ClockTilt
public import Mathlib.Data.Rat.Cast.Order
meta import Mathlib.Tactic.NormNum

public section

-- Even the simple lower-bound control P=3 does not give a quarter.
theorem conditional_amplitude_equals_quarter :
    (32 * (3 : ℚ) / 9) / (4096 / 1125) = 1 / 4 := by
  norm_num
