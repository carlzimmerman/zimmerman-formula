module

public import clock_flux.ClockTilt
public import Mathlib.Data.Rat.Cast.Order
meta import Mathlib.Tactic.NormNum

public section

open Why4.ClockTilt

theorem exact_static_branch_points :
    (3 / 4 : ℚ) ^ 3 - (3 + 13 * (11 / 112)) * (3 / 4) + 2 + 8 * (11 / 112) = 0 ∧
    (2 / 3 : ℚ) ^ 3 - (3 + 13 * (4 / 9)) * (2 / 3) + 2 + 8 * (4 / 9) = 0 := by
  norm_num

theorem rational_clock_coefficients :
    staticStiffness (-1 / 3 : ℚ) = 22 / 27 ∧
    54 * (1 + (-1 / 3 : ℚ) / 3 + (-1 / 3 : ℚ) ^ 2 / 6) = 49 ∧
    (54 : ℚ) * (5 / 6) * (-1 / 3) ^ 2 = 5 := by
  norm_num [staticStiffness]

theorem clock_frequency_control : tiltOmegaSquared (44 : ℚ) 5 1 1 = -220 / 49 ∧
    tiltOmegaSquared (44 : ℚ) 5 1 1 < 0 := by
  constructor
  · norm_num [tiltOmegaSquared]
  · exact tilt_frequency_negative 44 5 1 1 (by norm_num) (by norm_num)
      (by norm_num) (by norm_num)

theorem chi_characteristic_control :
    (1 : ℚ) / (67 / 75) = 75 / 67 ∧ (1 : ℚ) < 75 / 67 := by
  norm_num

theorem conditional_ratio_control :
    ((6 : ℚ) ^ 2 / 12) * (500 * 6 / 81) / (25 * 6 / 48) ^ 3 = 4096 / 1125 := by
  norm_num

theorem fixed_flux_energy_control :
    (6 : ℚ) * 1 - 6 * 1 ^ 6 / 6 = 5 ∧ -(6 : ℚ) * 1 ^ 6 / 6 = -1 := by
  norm_num
