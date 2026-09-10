import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith

namespace CubicConstraintSchur

/- Conditional real algebra for eliminating an auxiliary quadratic variable.
No theorem here derives its hypotheses from a physical action or proves
finite-wavelength health, a global inverse, or a degree-of-freedom count. -/

/-- A negative constant and negative slope remain negative for wave2 >= 0. -/
theorem constraint_negative (D0 D2 wave2 : ℝ)
    (h0 : D0 < 0) (h2 : D2 < 0) (hw : 0 ≤ wave2) :
    D0 + D2*wave2 < 0 := by
  have hp : D2*wave2 ≤ 0 :=
    mul_nonpos_of_nonpos_of_nonneg (le_of_lt h2) hw
  linarith

/-- Eliminating a negative auxiliary quadratic coefficient adds a nonnegative term. -/
theorem schur_kinetic_positive (A0 J D : ℝ)
    (hA : 0 < A0) (hD : D < 0) :
    0 < A0 - J^2/D := by
  have hratio : J^2/D ≤ 0 :=
    div_nonpos_of_nonneg_of_nonpos (sq_nonneg J) (le_of_lt hD)
  linarith

/-- Combined conditional statement, including the zero spatial-wave case. -/
theorem finite_wave_schur_positive (A0 J D0 D2 wave2 : ℝ)
    (hA : 0 < A0) (h0 : D0 < 0) (h2 : D2 < 0) (hw : 0 ≤ wave2) :
    D0 + D2*wave2 < 0 ∧ 0 < A0 - J^2/(D0 + D2*wave2) := by
  have hD := constraint_negative D0 D2 wave2 h0 h2 hw
  exact ⟨hD, schur_kinetic_positive A0 J _ hA hD⟩

#print axioms constraint_negative
#print axioms schur_kinetic_positive
#print axioms finite_wave_schur_positive

end CubicConstraintSchur
