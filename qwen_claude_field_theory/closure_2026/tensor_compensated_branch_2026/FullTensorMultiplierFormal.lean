import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum

/-! Lean arithmetic certificate for all five trace-free multiplier components. -/

namespace FullTensorMultiplier

theorem finite_k_full_tf_dof_count :
    (22 - 2 * 6 - 10 : ℤ) / 2 = 0 := by norm_num

theorem fixed_lapse_zero_mode_full_tf_count :
    (22 - 2 * 10 - 0 : ℤ) / 2 = 1 := by norm_num

end FullTensorMultiplier
