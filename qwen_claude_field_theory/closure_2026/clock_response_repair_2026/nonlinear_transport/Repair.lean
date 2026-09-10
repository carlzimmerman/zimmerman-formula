import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

namespace ClockBracketRepair

theorem Lorentz_Hamiltonian_identity (Q Y c d b k0 : ℝ) :
    ((c+d)*Q^2+b*Q^4/4+k0)-(c+b*Q^2/2)*Y-(d*Y-b*Y^2/4) =
    (c+d)*(Q^2-Y)+b*(Q^2-Y)^2/4+k0 := by ring

/- The derivative-to-symbol bridge is checked from the action in repair.py. -/
theorem bracket_cancellation (Q Y a b : ℝ) :
    -2*Q*(-a-b*(Q^2-Y)/2)-(2*a*Q+b*Q*(Q^2-Y))=0 := by ring

theorem preserves_A_B (q A B : ℝ) (hq : q≠0) :
    2*((3*A/q-B)/4)*q+((B-A/q)/(2*q^2))*q^3=A ∧
    2*((3*A/q-B)/4)+3*((B-A/q)/(2*q^2))*q^2=B := by
  constructor <;> field_simp <;> ring

#print axioms Lorentz_Hamiltonian_identity
#print axioms bracket_cancellation
#print axioms preserves_A_B
end ClockBracketRepair
