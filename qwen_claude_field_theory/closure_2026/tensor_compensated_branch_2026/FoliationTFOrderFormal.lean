import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/-! Formal algebra for the derivative-order conditional no-go. -/

namespace TensorCompensatedBranch

theorem foliation_tf_operator_has_k2_factor (k A B C : ℝ) :
    k ^ 2 * A + k ^ 2 * B + k ^ 4 * C = k ^ 2 * (A + B + k ^ 2 * C) := by
  ring

theorem foliation_tf_operator_vanishes_at_zero (A B C : ℝ) :
    (0 : ℝ) ^ 2 * A + 0 ^ 2 * B + 0 ^ 4 * C = 0 := by
  norm_num

end TensorCompensatedBranch
