import Mathlib.Data.Real.Basic
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! Conditional real algebra. SymPy separately checks the determinant and
physical equation reductions; these are hypotheses, not formalized variation.
No secondary constraint, Dirac count, or stability statement is proved. -/
namespace NonaffineClockVariation

theorem static_determinant_nonzero (det f z X U B p r : ℝ)
    (hdet : det = 4*f*z*(2*X+U)/(B*p*r))
    (hf : f ≠ 0) (hz : z ≠ 0) (hX : 0 < X) (hU : 0 < U)
    (hB : B ≠ 0) (hp : p ≠ 0) (hr : r ≠ 0) : det ≠ 0 := by
  rw [hdet]
  have hQ : 2*X+U ≠ 0 := ne_of_gt (by linarith)
  exact div_ne_zero
    (mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hf) hz) hQ)
    (mul_ne_zero (mul_ne_zero hB hp) hr)

theorem static_matrix_is_invertible
    (M : Matrix (Fin 3) (Fin 3) ℝ) (f z X U B p r : ℝ)
    (hdet : M.det = 4*f*z*(2*X+U)/(B*p*r))
    (hf : f ≠ 0) (hz : z ≠ 0) (hX : 0 < X) (hU : 0 < U)
    (hB : B ≠ 0) (hp : p ≠ 0) (hr : r ≠ 0) : IsUnit M := by
  apply (Matrix.isUnit_iff_isUnit_det M).2
  exact isUnit_iff_ne_zero.2
    (static_determinant_nonzero M.det f z X U B p r hdet hf hz hX hU hB hp hr)

theorem correlated_curvature_invariant
    (j PX GX f PXX0 GXX0 : ℝ) :
    GX*(PXX0+j*PX/f)-PX*(GXX0+j*GX/f) = GX*PXX0-PX*GXX0 := by
  ring

theorem matched_mass_curvature_cancellation
    (j f PX GX p1 p2 g1 g2 : ℝ) :
    ((p1+j*PX/f)-(p2+j*PX/f) = p1-p2) ∧
    ((g1+j*GX/f)-(g2+j*GX/f) = g1-g2) := by
  constructor <;> ring

theorem common_j_cannot_repair_nonzero_curvature_gap
    (j f PX p1 p2 : ℝ) (hgap : p1 ≠ p2) :
    p1+j*PX/f ≠ p2+j*PX/f := by
  exact fun h => hgap (add_right_cancel h)

theorem quadratic_unitary_primary_relation
    (F f A K V pstar pi : ℝ) (hF : F ≠ 0)
    (hp : pstar = -2*f*A*K-3*f^2*A^2*V/F)
    (hpi : pi = -2*F*K-3*f*A*V) : F*pstar-f*A*pi = 0 := by
  rw [hp,hpi]
  field_simp
  ring

theorem zero_gradient_positive_density_obstruction
    (F B f a zr P rho : ℝ)
    (hF : F ≠ 0) (hB : B ≠ 0) (hf : f ≠ 0) (ha : a ≠ 0)
    (hP : P = 0) (hpreserve : (2*f*a/B)*zr = 0)
    (hdensity : 2*F*rho = 2*f*zr/B-P) (hrho : 0 < rho) : False := by
  have hcoef : 2*f*a/B ≠ 0 :=
    div_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hf) ha) hB
  have hzr : zr = 0 := (mul_eq_zero.mp hpreserve).resolve_left hcoef
  have hproduct : (2*F)*rho = 0 := by simpa [hzr,hP] using hdensity
  have hzero : rho = 0 :=
    (mul_eq_zero.mp hproduct).resolve_left (mul_ne_zero (by norm_num) hF)
  linarith

#print axioms static_determinant_nonzero
#print axioms static_matrix_is_invertible
#print axioms correlated_curvature_invariant
#print axioms matched_mass_curvature_cancellation
#print axioms common_j_cannot_repair_nonzero_curvature_gap
#print axioms quadratic_unitary_primary_relation
#print axioms zero_gradient_positive_density_obstruction
end NonaffineClockVariation
