import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum

/-! Lean arithmetic certificate for the PPN-tuned constrained aether branch. -/

namespace PPNTunedAetherDirac

theorem finite_k_constrained_scalar_dof :
    (14 - 2 * 2 - 10 : ℤ) / 2 = 0 := by norm_num

theorem fixed_lapse_zero_mode_requires_lapse_constraint :
    (14 - 2 * 6 - 0 : ℤ) / 2 = 1 := by norm_num

end PPNTunedAetherDirac
