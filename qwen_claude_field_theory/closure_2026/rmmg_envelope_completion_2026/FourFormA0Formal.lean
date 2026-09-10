import Mathlib.Data.Real.Basic
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! Algebraic four-form normalization used by the envelope branch. -/

namespace RMMGEnvelope

theorem fourform_energy (q Z : ℝ) :
    q * (Z * q) - Z * q ^ 2 / 2 = Z * q ^ 2 / 2 := by
  ring

theorem fourform_a0_relation
    (q Z b beta G c : ℝ) (hden : Z + 2 * b * beta ^ 2 ≠ 0) :
    beta ^ 2 * c ^ 2 * G * q ^ 2 =
      (2 * beta ^ 2 / (Z + 2 * b * beta ^ 2)) * c ^ 2 * G *
        ((Z * q ^ 2 / 2) + b * beta ^ 2 * q ^ 2) := by
  let d : ℝ := Z + 2 * b * beta ^ 2
  have hd : d ≠ 0 := by
    simpa [d] using hden
  have hfactor :
      (2 * beta ^ 2) * c ^ 2 * G *
          ((Z * q ^ 2 / 2) + b * beta ^ 2 * q ^ 2) =
        beta ^ 2 * c ^ 2 * G * q ^ 2 * d := by
    dsimp [d]
    ring
  rw [show Z + 2 * b * beta ^ 2 = d by rfl, div_eq_mul_inv]
  calc
    beta ^ 2 * c ^ 2 * G * q ^ 2 =
        beta ^ 2 * c ^ 2 * G * q ^ 2 * d * d⁻¹ := by
          symm
          calc
            beta ^ 2 * c ^ 2 * G * q ^ 2 * d * d⁻¹ =
                (beta ^ 2 * c ^ 2 * G * q ^ 2) * (d * d⁻¹) := by ring
            _ = beta ^ 2 * c ^ 2 * G * q ^ 2 := by
                rw [mul_inv_cancel₀ hd, mul_one]
    _ = ((2 * beta ^ 2) * c ^ 2 * G *
          ((Z * q ^ 2 / 2) + b * beta ^ 2 * q ^ 2)) * d⁻¹ := by
          rw [hfactor]
    _ = (2 * beta ^ 2 * d⁻¹) * c ^ 2 * G *
          ((Z * q ^ 2 / 2) + b * beta ^ 2 * q ^ 2) := by
          ring

/- The fitted normalization is explicit: it is a coupling relation, not a
   consequence of the exponential constitutive function. -/
theorem kappa_sq_quarter_of_coupling_relation
    (b beta Z : ℝ) (hbeta : beta ≠ 0)
    (hrel : Z + 2 * b * beta ^ 2 = 8 * beta ^ 2) :
    2 * beta ^ 2 / (Z + 2 * b * beta ^ 2) = (1 / 4 : ℝ) := by
  rw [hrel]
  field_simp [hbeta]
  ring

theorem kappa_eq_half_of_coupling_relation
    (b beta Z : ℝ) (hbeta : 0 < beta)
    (hrel : Z + 2 * b * beta ^ 2 = 8 * beta ^ 2) :
    Real.sqrt (2 * beta ^ 2 / (Z + 2 * b * beta ^ 2)) = (1 / 2 : ℝ) := by
  have hbeta_ne : beta ≠ 0 := ne_of_gt hbeta
  rw [hrel]
  have hratio : 2 * beta ^ 2 / (8 * beta ^ 2) = (1 / 2 : ℝ) ^ 2 := by
    field_simp [hbeta_ne]
    ring
  rw [hratio, Real.sqrt_sq_eq_abs, abs_of_nonneg]
  norm_num

end RMMGEnvelope
