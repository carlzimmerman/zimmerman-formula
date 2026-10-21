module

public import current_interactions.CurrentEnergy
meta import Mathlib.Tactic.NormNum

public section

open Why4.CurrentEnergy

-- This uses p=2Q nu and omits the interaction's canonical shift.
theorem wrong_current_legendre :
    (4 : ℚ) * 2 - timeLagrangian 1 2 1 1 = timeHamiltonian 1 4 1 1 := by
  norm_num [timeLagrangian, timeHamiltonian]
