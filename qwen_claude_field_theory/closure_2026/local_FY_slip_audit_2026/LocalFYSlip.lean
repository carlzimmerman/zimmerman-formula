import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
Algebraic certificate for the restricted local spatial-gradient sector

  S_F = ∫ N * sqrt(det h) * F(Y),   Y = h^ij chi_i chi_j.

The differential-geometry variation is recorded in the accompanying Python
derivation.  These theorems certify the resulting stress decomposition,
principal-symbol determinant, and the aligned nonzero anisotropic source.  The
scope is conditional: no extra field or counter-stress is included here.
-/

namespace LocalFYSlip

theorem tracefree_aligned_trace (fy q : ℝ) :
    fy * (-2 * q ^ 2 / 3) + fy * (q ^ 2 / 3) + fy * (q ^ 2 / 3) = 0 := by
  ring

theorem aligned_tf_difference (fy q : ℝ) :
    fy * (-2 * q ^ 2 / 3) - fy * (q ^ 2 / 3) = -fy * q ^ 2 := by
  ring

theorem principal_determinant_factorization (fy fyy q : ℝ) :
    (2 * fy) ^ 2 * (2 * fy + 4 * fyy * q ^ 2) =
      8 * fy ^ 2 * (fy + 2 * fyy * q ^ 2) := by
  ring

theorem nonzero_aligned_source
    (fy q : ℝ) (hfy : fy ≠ 0) (hq : q ≠ 0) :
    -fy * q ^ 2 ≠ 0 := by
  exact (mul_ne_zero (neg_ne_zero.mpr hfy) (pow_ne_zero 2 hq))

theorem no_slip_conflicts_with_local_gradient_stress
    (fy q : ℝ) (hfy : 0 < fy) (hq : 0 < q)
    (h_no_slip_source : -fy * q ^ 2 = 0) : False := by
  nlinarith [sq_pos_of_pos hq]

end LocalFYSlip
