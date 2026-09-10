import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

/-! Exact conditional compatibility algebra. No physical mapping, invariant
manifold, constraint rank, or gravitational degree count is certified here.
The control p denotes P_X; it is not the radial clock derivative psi'. -/
namespace KGBMassCompatibilityStructure

theorem first_preservation_determinant
    (a2 a3 b2 b3 : ℝ) (hb : b2 ≠ 0) :
    (a3 + (-a2 / b2) * b3) * b2 = a3*b2 - a2*b3 := by
  field_simp [hb]
  ring

theorem determinant_tangency
    (a2 a3 b2 b3 a2d a3d b2d b3d : ℝ) (hb : b2 ≠ 0) :
    b2 * (a3d*b2 + a3*b2d - a2d*b3 - a2*b3d) =
      b2 * ((a3d + (-a2/b2)*b3d)*b2 - (a2d + (-a2/b2)*b2d)*b3)
        + b2d * (a3*b2 - a2*b3) := by
  field_simp [hb]
  ring

theorem common_higher_pressure_jet_cancels
    (p pX pXX h hX hXX1 hXX3 : ℝ) :
    (pXX*h + 2*pX*hX + p*hXX3) -
      (pXX*h + 2*pX*hX + p*hXX1) = p*(hXX3-hXX1) := by
  ring

#print axioms first_preservation_determinant
#print axioms determinant_tangency
#print axioms common_higher_pressure_jet_cancels
end KGBMassCompatibilityStructure
