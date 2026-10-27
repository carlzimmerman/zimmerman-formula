import Mathlib

/-!
Smooth conditional source-density counterexample for upgrading a mode-integral
ledger to pointwise reciprocal power. No physical coupling is derived here.
A single retained receiver mode spreads a supplied total reaction A into
-A*cos(x)^2/pi. A smooth nonnegative local cold deposition A*sin(x)^2/pi
has the same total positive power, but their pointwise sum is nonzero.
This does not contradict the source's explicitly GLOBAL-only conservation.
-/
noncomputable section
namespace FrameworkLocalPower

def coldPower (A x : ℝ) : ℝ := (A / Real.pi) * Real.sin x ^ 2
def modePower (A x : ℝ) : ℝ := -(A / Real.pi) * Real.cos x ^ 2

theorem cold_power_nonnegative (A x : ℝ) (hA : 0 ≤ A) :
    0 ≤ coldPower A x := by
  unfold coldPower
  positivity

theorem cold_total (A : ℝ) :
    (∫ x in (0 : ℝ)..2 * Real.pi, coldPower A x) = 2*A := by
  unfold coldPower
  rw [intervalIntegral.integral_const_mul, integral_sin_sq]
  norm_num

theorem mode_total (A : ℝ) :
    (∫ x in (0 : ℝ)..2 * Real.pi, modePower A x) = -A := by
  unfold modePower
  rw [intervalIntegral.integral_const_mul, integral_cos_sq]
  norm_num

theorem integrated_ledger (A : ℝ) :
    (∫ x in (0 : ℝ)..2 * Real.pi, coldPower A x) +
    (∫ x in (0 : ℝ)..2 * Real.pi, modePower A x) = 0 := by
  rw [cold_total, mode_total]
  ring

/-- At the antinode the cold deposition is zero but the mode reaction is not. -/
theorem pointwise_ledger_fails (A : ℝ) (hA : 0 < A) :
    coldPower A 0 = 0 ∧ coldPower A 0 + modePower A 0 < 0 := by
  constructor
  · simp [coldPower]
  · simpa [coldPower, modePower] using neg_neg_of_pos (div_pos hA Real.pi_pos)

end FrameworkLocalPower
#print axioms FrameworkLocalPower.cold_power_nonnegative
#print axioms FrameworkLocalPower.cold_total
#print axioms FrameworkLocalPower.mode_total
#print axioms FrameworkLocalPower.integrated_ledger
#print axioms FrameworkLocalPower.pointwise_ledger_fails
