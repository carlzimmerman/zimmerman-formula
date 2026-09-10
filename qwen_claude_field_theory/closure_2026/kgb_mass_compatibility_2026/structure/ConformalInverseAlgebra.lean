import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity

/-! Conditional algebra after the determinant and field-equation reductions
checked in SymPy. No physical mapping, smooth continuation, or DOF count is
formalized. All real variables represent finite coefficients. -/
namespace KGBConformalInverseStructure

theorem computed_determinant_nonzero (det f z X U B p r : ℝ)
    (hdet : det = 4*f*z*(2*X+U)/(B*p*r))
    (hf : f ≠ 0) (hz : z ≠ 0) (hX : 0 < X) (hU : 0 < U)
    (hB : B ≠ 0) (hp : p ≠ 0) (hr : r ≠ 0) : det ≠ 0 := by
  rw [hdet]
  have hQ : 2*X+U ≠ 0 := ne_of_gt (by linarith)
  exact div_ne_zero
    (mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hf) hz) hQ)
    (mul_ne_zero (mul_ne_zero hB hp) hr)

theorem computed_three_by_three_is_invertible
    (M : Matrix (Fin 3) (Fin 3) ℝ) (f z X U B p r : ℝ)
    (hdet : M.det = 4*f*z*(2*X+U)/(B*p*r))
    (hf : f ≠ 0) (hz : z ≠ 0) (hX : 0 < X) (hU : 0 < U)
    (hB : B ≠ 0) (hp : p ≠ 0) (hr : r ≠ 0) : IsUnit M := by
  apply (Matrix.isUnit_iff_isUnit_det M).2
  exact isUnit_iff_ne_zero.2
    (computed_determinant_nonzero M.det f z X U B p r hdet hf hz hX hU hB hp hr)

theorem zero_gradient_forces_zero_density
    (F B f a zr P rho : ℝ)
    (hF : F ≠ 0) (hB : B ≠ 0) (hf : f ≠ 0) (ha : a ≠ 0)
    (hP : P = 0) (hpreserve : (2*f*a/B)*zr = 0)
    (hdensity : 2*F*rho = 2*f*zr/B-P) : rho = 0 := by
  have hcoef : 2*f*a/B ≠ 0 :=
    div_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hf) ha) hB
  have hzr : zr = 0 := (mul_eq_zero.mp hpreserve).resolve_left hcoef
  have hproduct : (2*F)*rho = 0 := by simpa [hzr, hP] using hdensity
  exact (mul_eq_zero.mp hproduct).resolve_left (mul_ne_zero (by norm_num) hF)

theorem finite_exponential_target_density_positive (y r : ℝ)
    (hy : 0 < y) (hr : 0 < r) :
    0 < 4*y^2*Real.exp (-y)/(r*(1-Real.exp (-y)+y*Real.exp (-y))) := by
  have he : Real.exp (-y) < 1 := Real.exp_lt_one_iff.mpr (by linarith)
  have hexp : 0 < Real.exp (-y) := Real.exp_pos (-y)
  apply div_pos
  · positivity
  · exact mul_pos hr (add_pos (sub_pos.mpr he) (mul_pos hy hexp))

theorem zero_gradient_incompatible_with_positive_density
    (F B f a zr P rho : ℝ)
    (hF : F ≠ 0) (hB : B ≠ 0) (hf : f ≠ 0) (ha : a ≠ 0)
    (hP : P = 0) (hpreserve : (2*f*a/B)*zr = 0)
    (hdensity : 2*F*rho = 2*f*zr/B-P) (hrho : 0 < rho) : False := by
  have hzero := zero_gradient_forces_zero_density
    F B f a zr P rho hF hB hf ha hP hpreserve hdensity
  linarith

#print axioms computed_determinant_nonzero
#print axioms computed_three_by_three_is_invertible
#print axioms zero_gradient_forces_zero_density
#print axioms finite_exponential_target_density_positive
#print axioms zero_gradient_incompatible_with_positive_density
end KGBConformalInverseStructure
