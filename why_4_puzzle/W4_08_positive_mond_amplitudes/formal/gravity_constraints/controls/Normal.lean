module

public import gravity_constraints.GravitySelection
public import Mathlib.Data.Rat.Cast.Order
meta import Mathlib.Tactic.NormNum

public section

open Why4.GravitySelection

theorem shift_and_lapse_control :
    rawQuadratic (2 : ℚ) 2 1 7 3 1 2 1 = 26 ∧
    lapseEquation (2 : ℚ) 2 1 (7 / 2) 3 1 2 1 = 0 := by
  norm_num [rawQuadratic, lapseEquation]

theorem redshift_control :
    (1 : ℚ) * (2 * 1 ^ 2 + 4 * 1 * 0 / 1 + 2 * 0 ^ 2 / 1 ^ 2) -
      (2 / 1) * (3 * 1 * 1 * 1 ^ 2 - 2 * 1 * 1 * 1 ^ 2 + 2 * 1 * 1 * 0) = 0 := by
  norm_num

theorem positive_reduced_kinetic_control :
    reducedKinetic (2 : ℚ) 3 2 1 2 = 4 ∧
    0 < reducedKinetic (2 : ℚ) 3 2 1 2 := by
  norm_num [reducedKinetic]

theorem deformation_control :
    (3 : ℚ) * ((1 + 1) * 5) ^ 2 / 2 ^ 3 =
      4 * ((3 : ℚ) * 5 ^ 2 / 2 ^ 3) := by
  norm_num

theorem physical_force_control :
    (((1 : ℚ) / (1 + 1)) * 2) ^ 2 / ((1 + 1) * 3) = 1 / 6 ∧
    ((1 : ℚ) / (1 + 1)) ^ 3 * (2 ^ 2 / (1 * 3)) = 1 / 6 := by
  norm_num

-- Generic P=448/125 is a nonvacuous exact target-equation control;
-- it is deliberately not an asserted evaluation of actual pi.
theorem nonvacuous_ppn_control :
    (0 : ℚ) < 448 / 125 ∧ (448 / 125 : ℚ) < 4 ∧
    125 * (448 / 125 : ℚ) * (1 + 1 / 8) * (1 / 3) ^ 3 =
      32 * (1 - 1 / 8) * (1 - 1 / 3) ∧
    (1 : ℚ) - 2 * (1 / 3) < 1 / 2 := by
  norm_num

theorem nonzero_band_control :
    bandPolynomial (1 : ℚ) 0 = -3 / 16 ∧
    bandPolynomial (1 : ℚ) (-11 / 49) < 0 := by
  norm_num [bandPolynomial]
