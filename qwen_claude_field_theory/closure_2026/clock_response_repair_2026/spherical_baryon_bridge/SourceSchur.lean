import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

namespace SphericalBaryonSource

noncomputable section

/- Finite-dimensional real algebra for the displayed quadratic scalar action.
The coefficients are arbitrary real numbers at one time and wavenumber.
This file does not vary a covariant action, justify a gauge reduction, prove
PDE well-posedness, or establish a MOND force law. D = 0 is excluded. -/

def fullLagrangian (A0 J B0 D E C0 fz fv0 fu0 z u v : ℝ) : ℝ :=
  A0 * v^2 / 2 + J * z * v + B0 * u * v + D * z^2 / 2 +
    E * z * u + C0 * u^2 / 2 + fz * z + fv0 * v + fu0 * u

def constraintSolution (D J E fz u v : ℝ) : ℝ :=
  -(J * v + E * u + fz) / D

def reducedLagrangian (A0 J B0 D E C0 fz fv0 fu0 u v : ℝ) : ℝ :=
  (A0 - J^2 / D) * v^2 / 2 + (B0 - J * E / D) * u * v +
    (C0 - E^2 / D) * u^2 / 2 + (fv0 - J * fz / D) * v +
    (fu0 - E * fz / D) * u - fz^2 / (2 * D)

theorem constraint_residual (D J E fz u v : ℝ) (hD : D ≠ 0) :
    D * constraintSolution D J E fz u v + J * v + E * u + fz = 0 := by
  unfold constraintSolution
  field_simp
  ring

/-- Exact substitution includes both source coefficients and the constant. -/
theorem sourced_schur_identity
    (A0 J B0 D E C0 fz fv0 fu0 u v : ℝ) (hD : D ≠ 0) :
    fullLagrangian A0 J B0 D E C0 fz fv0 fu0
      (constraintSolution D J E fz u v) u v =
    reducedLagrangian A0 J B0 D E C0 fz fv0 fu0 u v := by
  unfold fullLagrangian constraintSolution reducedLagrangian
  field_simp
  ring

/-- The canonical momentum of the displayed reduced quadratic polynomial. -/
def reducedMomentum (A0 J B0 D E fz fv0 u v : ℝ) : ℝ :=
  (A0 - J^2 / D) * v + (B0 - J * E / D) * u + fv0 - J * fz / D

/-- The linear coefficient in a velocity increment is the displayed momentum. -/
theorem velocity_increment
    (A0 J B0 D E C0 fz fv0 fu0 u v dv : ℝ) :
    reducedLagrangian A0 J B0 D E C0 fz fv0 fu0 u (v + dv) -
      reducedLagrangian A0 J B0 D E C0 fz fv0 fu0 u v =
    reducedMomentum A0 J B0 D E fz fv0 u v * dv +
      (A0 - J^2 / D) * dv^2 / 2 := by
  unfold reducedLagrangian reducedMomentum
  ring

/-- Equal zero physical field/velocity data require the affine source shift. -/
theorem zero_physical_data_momentum
    (A0 J B0 D E fz fv0 : ℝ) :
    reducedMomentum A0 J B0 D E fz fv0 0 0 = fv0 - J * fz / D := by
  simp [reducedMomentum]

/-- In particular, zero canonical momentum is incompatible when this shift is nonzero. -/
theorem zero_physical_data_not_zero_momentum
    (A0 J B0 D E fz fv0 : ℝ) (hsource : fv0 - J * fz / D ≠ 0) :
    reducedMomentum A0 J B0 D E fz fv0 0 0 ≠ 0 := by
  simpa [reducedMomentum] using hsource

#print axioms constraint_residual
#print axioms sourced_schur_identity
#print axioms velocity_increment
#print axioms zero_physical_data_momentum
#print axioms zero_physical_data_not_zero_momentum

end

end SphericalBaryonSource
