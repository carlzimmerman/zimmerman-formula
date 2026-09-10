import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! Lean identities for the derived c13=c14=0 preferred-frame locus. -/

namespace AEPpnTuning

theorem luminal_locus_c13 (c1 : ℝ) : c1 + (-c1) = 0 := by ring

theorem alpha1_numerator_vanishes (c1 : ℝ) :
    (-c1) ^ 2 + c1 * (-c1) = 0 := by ring

theorem alpha2_first_factor_vanishes (c1 : ℝ) :
    c1 + 2 * (-c1) - (-c1) = 0 := by ring

theorem alpha1_zero_on_locus
    (c1 : ℝ) (_hden : 2 * c1 - c1 ^ 2 + (-c1) ^ 2 ≠ 0) :
    -8 * ((-c1) ^ 2 + c1 * (-c1)) /
      (2 * c1 - c1 ^ 2 + (-c1) ^ 2) = 0 := by
  rw [alpha1_numerator_vanishes]
  simp

theorem luminal_ratio_on_locus (c1 : ℝ) :
    1 / (1 - (c1 + (-c1))) = 1 := by
  rw [luminal_locus_c13]
  norm_num

end AEPpnTuning
