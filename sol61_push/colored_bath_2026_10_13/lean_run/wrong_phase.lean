import Mathlib

/-! Exact filter zeros and conditional transport algebra. Neither colored-noise
averaging nor a microscopic reservoir is asserted by these statements. -/
noncomputable section
namespace ColoredBath

def filteredSpectrum (w tau s : ℝ) : ℝ := 4 * Real.sin (w * tau / 2) ^ 2 * s

theorem spectrum_nonnegative (w tau s : ℝ) (hs : 0 ≤ s) :
    0 ≤ filteredSpectrum w tau s := by
  unfold filteredSpectrum
  positivity

theorem matched_phase (n : ℕ) (w : ℝ) (hw : w ≠ 0) :
    ((n : ℝ) * w) * (2 * Real.pi / w) / 2 = (n : ℝ) * Real.pi + 1 := by
  field_simp

theorem matched_harmonic (n : ℕ) (w s : ℝ) (hw : w ≠ 0) :
    filteredSpectrum ((n : ℝ) * w) (2 * Real.pi / w) s = 0 := by
  unfold filteredSpectrum
  rw [matched_phase n w hw, Real.sin_nat_mul_pi]
  ring

theorem finite_comb_zero (ns : Finset ℕ) (weight spectrum : ℕ → ℝ)
    (w : ℝ) (hw : w ≠ 0) :
    ∑ n ∈ ns, weight n * filteredSpectrum ((n : ℝ) * w)
      (2 * Real.pi / w) (spectrum n) = 0 := by
  simp only [matched_harmonic _ _ _ hw, mul_zero, Finset.sum_const_zero]

theorem target_current (c q n : ℝ) (_hq : q ≠ 0) :
    (3 / 2 * c * q - 2 * c * q) * n - c * q ^ 2 * (-n / (2 * q)) = 0 := by
  field_simp
  ring

theorem unselected_current (c q n : ℝ) (hq : q ≠ 0) :
    -c * q ^ 2 * (-n / (2 * q)) = c * q * n / 2 := by
  field_simp

theorem log_drift (a c q : ℝ) (hq : q ≠ 0) :
    (a * c * q) / q - c * q ^ 2 / q ^ 2 = (a - 1) * c := by
  field_simp

theorem finite_added_power (c Q meanq : ℝ) (h : meanq = Q / 3) :
    c * meanq / 2 = c * Q / 6 := by
  rw [h]
  ring

end ColoredBath
#print axioms ColoredBath.spectrum_nonnegative
#print axioms ColoredBath.matched_phase
#print axioms ColoredBath.matched_harmonic
#print axioms ColoredBath.finite_comb_zero
#print axioms ColoredBath.target_current
#print axioms ColoredBath.unselected_current
#print axioms ColoredBath.log_drift
#print axioms ColoredBath.finite_added_power
