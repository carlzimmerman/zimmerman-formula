module

public import current_interactions.CurrentEnergy
public import current_interactions.FluxComparison
public import Mathlib.Data.Rat.Cast.Order
meta import Mathlib.Tactic.NormNum

public section

open Why4.CurrentEnergy

theorem correct_current_legendre :
    (2 : ℚ) * 2 - timeLagrangian 1 2 1 1 = timeHamiltonian 1 2 1 1 := by
  norm_num [timeLagrangian, timeHamiltonian]

theorem occupied_neutral_energy_positive : neutralEnergy (1 : ℚ) 3 1 1 = 2 := by
  norm_num [neutralEnergy]

theorem charged_minimum_control : chargedEnergy (2 : ℚ) 1 1 = 4 / 3 := by
  norm_num [chargedEnergy]

theorem charged_nonminimum_control : chargedEnergy (2 : ℚ) 2 1 > 4 / 3 := by
  norm_num [chargedEnergy]

theorem flux_order_control : (1 : ℚ) * (1 / 2) ^ 4 < 1 * (1 / 2) ^ 3 := by
  norm_num
