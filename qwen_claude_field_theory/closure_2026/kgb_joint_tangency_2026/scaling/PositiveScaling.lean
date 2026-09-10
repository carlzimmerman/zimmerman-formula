import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

/- Conditional arithmetic under the separately established positive vacuum
   scaling: A,N invariant; B maps to B/s; f,j map to s*f,s*j.
   No action variation, constraint algebra, Dirac or empirical theorem. -/
namespace PositiveVacuumScaling

theorem control_equations_invariant (s A B N f j : ℝ) (hs : 0 < s) :
    A + (s*f)*(B/s) = A + f*B ∧
    N + (s*j)*(B/s) = N + j*B := by
  have hn : s ≠ 0 := ne_of_gt hs
  constructor <;> field_simp [hn]

theorem determinant_zero_iff (s N1 N2 B1 B2 : ℝ) (hs : 0 < s) :
    (N1*(B2/s)-N2*(B1/s)=0) ↔ (N1*B2-N2*B1=0) := by
  have hn : s ≠ 0 := ne_of_gt hs
  have identity : N1*(B2/s)-N2*(B1/s) = (N1*B2-N2*B1)/s := by ring
  rw [identity]
  simp [div_eq_zero_iff, hn]

end PositiveVacuumScaling

#print axioms PositiveVacuumScaling.control_equations_invariant
#print axioms PositiveVacuumScaling.determinant_zero_iff
