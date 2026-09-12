import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity

/-! Restricted scalar constitutive discriminants only.
The action variation and Taylor-jet interpretation are supplied by the companion
symbolic derivation. No scalar potential is identified with the physical metric.
The canonical completion affects c1 only. Both signs of beta and the spherical
cubic term affect c2 only. No custom axiom or sorry.
-/

namespace SphericalScaling
noncomputable section

/-- Coefficient representation of c1*p+c2*p^2+c3*p^3+c5*p^5. -/
def frozenFluxJet (c1 c2 c3 c5 : ℝ) (degree : ℕ) : ℝ :=
  if degree = 1 then c1 else if degree = 2 then c2
  else if degree = 3 then c3 else if degree = 5 then c5 else 0

/-- Coefficient representation of the fifth-order exponential flux jet. -/
def exponentialFluxJet (a normalization : ℝ) (degree : ℕ) : ℝ :=
  if degree = 2 then normalization/a
  else if degree = 3 then -(normalization/(2*a^2))
  else if degree = 4 then normalization/(6*a^3)
  else if degree = 5 then -(normalization/(24*a^4)) else 0

theorem frozen_fourth_coefficient (c1 c2 c3 c5 : ℝ) :
    frozenFluxJet c1 c2 c3 c5 4 = 0 := by
  simp [frozenFluxJet]

theorem exponential_fourth_coefficient (a normalization : ℝ) :
    exponentialFluxJet a normalization 4 = normalization/(6*a^3) := by
  simp [exponentialFluxJet]

theorem restricted_flux_jets_differ (c1 c2 c3 c5 a normalization : ℝ)
    (ha : 0 < a) (hn : 0 < normalization) :
    frozenFluxJet c1 c2 c3 c5 ≠ exponentialFluxJet a normalization := by
  intro heq
  have hcoeff := congrArg (fun f : ℕ → ℝ => f 4) heq
  rw [frozen_fourth_coefficient, exponential_fourth_coefficient] at hcoeff
  have hp : 0 < normalization/(6*a^3) := by positivity
  exact (ne_of_lt hp) hcoeff

/-- A hypothetical directly sourced cubic scalar and a MOND radial square law
can overlap only at one radius when gamma and normalization are fixed.
No baryonic interpretation of the scalar charge is asserted. -/
theorem cubic_and_mond_overlap_radius (gamma normalization radius p charge : ℝ)
    (hc : charge ≠ 0)
    (hcubic : 2*gamma*radius*p^2 = charge)
    (hmond : radius^2*p^2 = normalization*charge) :
    radius = 2*gamma*normalization := by
  have hprod : charge*(radius-2*gamma*normalization) = 0 := by
    linear_combination 2*gamma*hmond-radius*hcubic
  have hzero := (mul_eq_zero.mp hprod).resolve_left hc
  exact sub_eq_zero.mp hzero

#print axioms frozen_fourth_coefficient
#print axioms exponential_fourth_coefficient
#print axioms restricted_flux_jets_differ
#print axioms cubic_and_mond_overlap_radius
end
end SphericalScaling
