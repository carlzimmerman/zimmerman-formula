module

public import protected_auxiliaries.ChiralFold
public import Mathlib.Data.Rat.Cast.Order
meta import Mathlib.Tactic.NormNum

public section

open Why4.ChiralFold

theorem timelike_rational_root : cubic (-529 / 2880 : ℚ) (-15 / 8) = 0 := by
  norm_num [cubic]

theorem timelike_ghost_control : chiTimeCoefficient (6 : ℚ) (-529 / 2880) (-15 / 8) < 0 := by
  exact timelike_chi_coefficient_negative 6 (-529 / 2880) (-15 / 8)
    (by norm_num) (by norm_num) (by norm_num) timelike_rational_root

theorem spatial_root_is_not_excluded :
    cubic (5 / 12 : ℚ) (1 / 2) = 0 ∧ (1 / 2 : ℚ) ^ 2 < 3 := by
  norm_num [cubic]

theorem fold_kinetic_and_jacobian_control :
    (6 : ℚ) - 2 * 1 ^ 2 = 4 ∧ 6 - 3 * 1 ^ 2 = 3 ∧ 6 - 6 * 1 ^ 2 = 0 := by
  norm_num
