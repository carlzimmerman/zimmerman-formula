import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
  Polynomial certificates for the rank-changing curvature-projector audit.
  The Python file supplies the principal-symbol interpretation; these lemmas
  certify the displayed coefficients and the zero-field source obstruction.
-/

namespace RankChangingCurvature

def h00 (_u v : ℝ) : ℝ := v ^ 2
def h01 (u v : ℝ) : ℝ := u * v
def h11 (u _v : ℝ) : ℝ := u ^ 2

theorem projector_orthogonal_00 (u v : ℝ) :
    h00 u v * (-u) + h01 u v * v = 0 := by
  simp [h00, h01]
  ring

theorem projector_orthogonal_11 (u v : ℝ) :
    h01 u v * (-u) + h11 u v * v = 0 := by
  simp [h01, h11]
  ring

theorem projector_determinant_zero (u v : ℝ) :
    h00 u v * h11 u v - h01 u v ^ 2 = 0 := by
  simp [h00, h01, h11]
  ring

def hxx (epsilon h3 : ℝ) : ℝ := epsilon ^ 2 * h3 ^ 2

theorem hxx_second_variation_expansion
    (epsilon h3 delta : ℝ) :
    hxx epsilon (h3 + delta) =
      hxx epsilon h3 + 2 * epsilon ^ 2 * h3 * delta
        + epsilon ^ 2 * delta ^ 2 := by
  simp [hxx]
  ring

def auxTerm (epsilon h3 cxx lambda : ℝ) : ℝ :=
  cxx * lambda * hxx epsilon h3

theorem aux_quadratic_remainder
    (epsilon h3 delta cxx lambda : ℝ) :
    auxTerm epsilon (h3 + delta) cxx lambda
      - auxTerm epsilon h3 cxx lambda
      - 2 * cxx * lambda * epsilon ^ 2 * h3 * delta =
        cxx * lambda * epsilon ^ 2 * delta ^ 2 := by
  simp [auxTerm, hxx]
  ring

theorem highest_derivative_hessian_coefficient
    (epsilon cxx lambda : ℝ) :
    2 * cxx * lambda * epsilon ^ 2 =
      2 * cxx * epsilon ^ 2 * lambda := by
  ring

theorem highest_derivative_hessian_nonzero
    (epsilon cxx lambda : ℝ)
    (hepsilon : epsilon ≠ 0)
    (hcxx : cxx ≠ 0)
    (hlambda : lambda ≠ 0) :
    2 * cxx * epsilon ^ 2 * lambda ≠ 0 := by
  have htwo : (2 : ℝ) ≠ 0 := by norm_num
  have heps2 : epsilon ^ 2 ≠ 0 := pow_ne_zero 2 hepsilon
  exact mul_ne_zero (mul_ne_zero (mul_ne_zero htwo hcxx) heps2) hlambda

theorem highest_derivative_hessian_zero_at_zero
    (cxx lambda : ℝ) :
    2 * cxx * (0 : ℝ) ^ 2 * lambda = 0 := by
  norm_num

theorem zero_field_source_equation_inconsistent
    (J k response : ℝ) (hJ : 0 < J) :
    ¬ ((0 : ℝ) ^ 2 * k ^ 2 * response = J) := by
  norm_num
  exact (ne_of_gt hJ).symm

end RankChangingCurvature
