module

public import clock_flux.ClockTilt
public import Mathlib.Data.Rat.Cast.Order
meta import Mathlib.Tactic.NormNum

public section

open Why4.ClockTilt

-- Positive time coefficients alone do not make this coupled clock stable.
theorem positive_kinetic_implies_stable_tilt :
    (0 : ℚ) ≤ tiltOmegaSquared 44 5 1 1 := by
  norm_num [tiltOmegaSquared]
