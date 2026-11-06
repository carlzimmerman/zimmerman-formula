/-
MUTATE twin of FRW_correction.lean: three planted false claims. Each must FAIL to compile.
-/
import Mathlib

namespace FRWCorrectionMutate

/-- FALSE: the legacy square equals the corrected square identically. -/
theorem legacy_eq_corrected (z : ℝ) : (1 - 2 * z) ^ 2 = (1 - z) ^ 2 := by ring

/-- FALSE: the legacy UV denominator z + (1-2z)^2 equals the corrected one. -/
theorem legacy_uv (z : ℝ) : z + (1 - 2 * z) ^ 2 = 1 - z + z ^ 2 := by ring

/-- FALSE: phase speed bounded by 1 with a NEGATIVE mixing factor. -/
theorem phase_speed_neg_f (E l x : ℝ) (hE : 0 < E) (hl : 0 ≤ l) :
    E * (1 + l * x ^ 2) / (E * (1 + l * x ^ 2) + (-1) * x ^ 2) ≤ 1 := by
  rw [div_le_one (by nlinarith)]; nlinarith

end FRWCorrectionMutate
