import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

/- Conditional real algebra only. The covariant contractions, ADM map and
  interpretation as momenta are independently checked, not formalized here. -/
namespace DHOSTKinetic

theorem determinant_zero (F v T : ℝ) (hF : F ≠ 0) :
    (-4*F/3)*(-3*v^2*T^2/F)-(-2*v*T)^2=0 := by
  field_simp
  ring

theorem null_vector (F v T : ℝ) (hF : F ≠ 0) :
    (-4*F/3)*(-3*v*T)+(-2*v*T)*(2*F)=0 ∧
    (-2*v*T)*(-3*v*T)+(-3*v^2*T^2/F)*(2*F)=0 := by
  constructor
  · ring
  · field_simp
    ring

theorem trace_square (F v T K z : ℝ) (hF : F ≠ 0) :
    -2*F*K^2/3-2*v*T*K*z-3*v^2*T^2*z^2/(2*F) =
      -2*F/3*(K+3*v*T*z/(2*F))^2 := by
  field_simp
  ring

theorem kinetic_primary (F v T K z h : ℝ) (hF : F ≠ 0) :
    h*(-2*v*T*K-3*v^2*T^2*z/F) -
      (v*T/F)*(h*(-2*F*K-3*v*T*z))=0 := by
  field_simp
  ring

#print axioms determinant_zero
#print axioms null_vector
#print axioms trace_square
#print axioms kinetic_primary
end DHOSTKinetic
