import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith

/-! Lean certificate for the conditional local-regulator obstruction.

The hypotheses are precisely the two linear principal-symbol equations.  No
rank, PPN value, or target DOF count is inserted.
-/

namespace TensorCompensatedBranch

theorem regulator_elimination
    (k R F d Lambda : ℝ)
    (hk : k ≠ 0)
    (hmetric : R + k ^ 2 * Lambda = 0)
    (hmult : k ^ 2 * d + F * Lambda = 0) :
    Lambda = -R / k ^ 2 ∧ d = F * R / k ^ 4 := by
  have hk2 : k ^ 2 ≠ 0 := pow_ne_zero 2 hk
  have hk4 : k ^ 4 ≠ 0 := pow_ne_zero 4 hk
  have hlam : Lambda = -R / k ^ 2 := by
    apply (eq_div_iff hk2).2
    linarith
  constructor
  · exact hlam
  · apply (eq_div_iff hk4).2
    rw [hlam] at hmult
    field_simp [hk2] at hmult
    nlinarith

theorem exact_no_slip_for_nonzero_source_requires_zero_regulator
    (k R F d Lambda : ℝ)
    (hk : k ≠ 0)
    (hR : R ≠ 0)
    (hmetric : R + k ^ 2 * Lambda = 0)
    (hmult : k ^ 2 * d + F * Lambda = 0)
    (hno_slip : d = 0) :
    F = 0 := by
  have hprod : F * Lambda = 0 := by
    rw [hno_slip] at hmult
    simpa using hmult
  rcases mul_eq_zero.mp hprod with hF | hLambda
  · exact hF
  · apply False.elim
    apply hR
    rw [hLambda] at hmetric
    simpa using hmetric

end TensorCompensatedBranch
