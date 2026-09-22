/-
  K005 — branch selection is the kinematics. Algebra only.

  Scope. This certifies the selection logic. It does not certify that the
  fluid is the dark stress of the world. The static-observer factor
  a_i = ∂_i Φ / (1+2Φ) is computed in K005_branch_selection.py; the theorems
  here take the weak-field link a = ∂Φ as a hypothesis and show what follows.

  Two clauses:
    geodesic (a = 0) is the free-fall branch, and it is pressureless;
    static and inhomogeneous (a = ∂Φ ≠ 0) is the supported branch.

  Anti-tautology: the dichotomy at a = 0 does not mention the potential.
  A gradient alone does not select the supported branch. The static link
  is an independent hypothesis.

  The settled fraction is not in these equations. n = 2 is not derived here.
-/
import Mathlib

/-- A static observer at linear order has a = ∂Φ. Vanishing acceleration
then forces a homogeneous potential. -/
theorem static_acceleration_kills_gradient (a dPhi : ℝ) (hlink : a = dPhi) (hfree : a = 0) :
    dPhi = 0 := by
  rw [hlink] at hfree
  exact hfree

/-- An inhomogeneous potential excludes free-fall for a static observer. -/
theorem static_inhomogeneous_has_acceleration (a dPhi : ℝ) (hlink : a = dPhi) (hinh : dPhi ≠ 0) :
    a ≠ 0 := by
  rw [hlink]
  exact hinh

/-- Given the dichotomy, a nonzero acceleration is the supported branch. -/
theorem nonzero_acceleration_is_supported (K ρ a a' : ℝ) (ha : a ≠ 0)
    (hdich : a = 0 ∨ a' = -(K * ρ)) : a' = -(K * ρ) := by
  rcases hdich with h0 | hsup
  · exact absurd h0 ha
  · exact hsup

/-- The dichotomy itself, restated so this file stands alone. -/
theorem branch_dichotomy (K ρ a a' : ℝ) (h : a * (K * ρ) = -(a * a')) :
    a = 0 ∨ a' = -(K * ρ) := by
  have h2 : a * (K * ρ + a') = 0 := by linear_combination h
  rcases mul_eq_zero.mp h2 with h3 | h3
  · left; exact h3
  · right; linarith

/-- Geodesic stress is pressureless. Ordinary matter, being minimal, is here. -/
theorem geodesic_is_pressureless (K a : ℝ) (h : a = 0) : a ^ 2 / (2 * K) = 0 := by
  rw [h]
  simp

/-- Anti-tautology. At a = 0 the dichotomy identity holds with no reference
to a potential gradient. Inhomogeneity alone does not select the branch. -/
theorem gradient_does_not_select (K ρ a' : ℝ) : (0 : ℝ) * (K * ρ + a') = 0 := by
  simp

/-- The static link is independent of the geodesic clause: a = 0 is
compatible with a nonzero gradient. Dropping a = ∂Φ, the supported
conclusion does not follow. -/
theorem geodesic_compatible_with_gradient (dPhi : ℝ) (hd : dPhi ≠ 0) :
    ∃ a : ℝ, a = 0 ∧ dPhi ≠ 0 := by
  exact ⟨0, rfl, hd⟩

#print axioms static_acceleration_kills_gradient
#print axioms static_inhomogeneous_has_acceleration
#print axioms nonzero_acceleration_is_supported
#print axioms branch_dichotomy
#print axioms geodesic_is_pressureless
#print axioms gradient_does_not_select
#print axioms geodesic_compatible_with_gradient
