import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith

/-! Conditional no-go certificate for a local self-adjoint derivative multiplier.

The shared operator P models the fact that varying an action linear in a
multiplier puts the same formally self-adjoint spatial operator in the
multiplier and metric equations.  No numerical rank or DOF target is assumed.
-/

namespace TensorCompensatedBranch

theorem derivative_multiplier_zero_mode_incompatible
    (R P Lambda : ℝ)
    (hR : R ≠ 0)
    (hP0 : P = 0)
    (hmetric : R + P * Lambda = 0) :
    False := by
  apply hR
  rw [hP0] at hmetric
  simpa using hmetric

theorem derivative_multiplier_finite_k_solution
    (R P Lambda : ℝ)
    (hP : P ≠ 0)
    (hmetric : R + P * Lambda = 0) :
    Lambda = -R / P := by
  apply (eq_div_iff hP).2
  linarith

theorem derivative_multiplier_no_slip_forces_zero_regulator
    (R P F d Lambda : ℝ)
    (hR : R ≠ 0)
    (hP : P ≠ 0)
    (hmetric : R + P * Lambda = 0)
    (hmult : P * d + F * Lambda = 0)
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
