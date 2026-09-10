import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith

/-!
Generic conditional preservation algebra over the reals.

Here `p` is an abstract shared control, not the radial scalar gradient.
These theorems do not establish that a physical shared-action inverse has
preservation equation `a + p*b = 0`, nor do they establish integrability,
existence of an ODE solution, or any stability property of a gravity theory.
-/
namespace KGBSharedPreservationAudit

theorem preservation_forces_control (a b p : ℝ)
    (hb : b ≠ 0) (hpreserve : a + p*b = 0) : p = -a/b := by
  apply (eq_div_iff hb).2
  linarith

theorem preservation_control_unique (a b p q : ℝ)
    (hb : b ≠ 0) (hp : a + p*b = 0) (hq : a + q*b = 0) : p = q := by
  exact (preservation_forces_control a b p hb hp).trans
    (preservation_forces_control a b q hb hq).symm

theorem zero_coefficient_nonzero_residual_has_no_solution (a b : ℝ)
    (hb : b = 0) (ha : a ≠ 0) : ¬ ∃ p : ℝ, a + p*b = 0 := by
  rintro ⟨p, hp⟩
  rw [hb, mul_zero, add_zero] at hp
  exact ha hp

theorem zero_coefficient_zero_residual_is_unconstrained (p : ℝ) :
    (0 : ℝ) + p*0 = 0 := by simp

#print axioms preservation_forces_control
#print axioms preservation_control_unique
#print axioms zero_coefficient_nonzero_residual_has_no_solution
#print axioms zero_coefficient_zero_residual_is_unconstrained
end KGBSharedPreservationAudit
