import Mathlib

noncomputable section
open scoped Real
namespace Probe

example {X : ℝ} (hX : 0 < X) :
    (1 / (2 * Real.sqrt X) / 2) * Real.sqrt (1 + 4 * X)
      + (Real.sqrt X / 2) * (4 / (2 * Real.sqrt (1 + 4 * X)))
      + ((2 * Real.sqrt X + Real.sqrt (1 + 4 * X))⁻¹
        * (2 * (1 / (2 * Real.sqrt X)) + 4 / (2 * Real.sqrt (1 + 4 * X)))) / 4
      - 1 / (2 * Real.sqrt X)
    = (Real.sqrt (1 + 4 * X) - 1) / (2 * Real.sqrt X) := by
  have hw : Real.sqrt X ≠ 0 := ne_of_gt (Real.sqrt_pos.2 hX)
  have harg : 0 < 1 + 4 * X := by nlinarith [sq_nonneg X]
  have hvpos : 0 < Real.sqrt (1 + 4 * X) := Real.sqrt_pos.2 harg
  have hv : Real.sqrt (1 + 4 * X) ≠ 0 := ne_of_gt hvpos
  have h2w : 0 ≤ 2 * Real.sqrt X := by
    apply mul_nonneg
    · norm_num
    · exact Real.sqrt_nonneg X
  have hpos : 0 < 2 * Real.sqrt X + Real.sqrt (1 + 4 * X) :=
    add_pos_of_nonneg_of_pos h2w hvpos
  have hden : 2 * Real.sqrt X + Real.sqrt (1 + 4 * X) ≠ 0 := ne_of_gt hpos
  have hvv : Real.sqrt (1 + 4 * X) * Real.sqrt (1 + 4 * X) = 1 + 4 * X :=
    Real.mul_self_sqrt (le_of_lt harg)
  have hww : Real.sqrt X * Real.sqrt X = X := Real.mul_self_sqrt (le_of_lt hX)
  have hvv2 : (Real.sqrt (1 + 4 * X)) ^ 2 = 1 + 4 * X := by
    simpa [sq] using hvv
  have hww2 : (Real.sqrt X) ^ 2 = X := by
    simpa [sq] using hww
  field_simp [hw, hv, hden]
  nlinarith [hvv2, hww2]

end Probe