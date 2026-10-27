import Mathlib

/-! Conditional moment inequalities for positive common-minimum mixtures.
The physical operator dictionary and effective-action truncation are premises. -/
namespace Dilaton32Pi

theorem dimension_chords (d : ℝ) (hlo : 1 ≤ d) (hhi : d ≤ 4) :
    d^2 ≤ 5*d-4 ∧ 1/d ≤ (5-d)/4 := by
  have hp : 0 < d := by linarith
  have hprod := mul_nonneg (by linarith : 0 ≤ d-1) (by linarith : 0 ≤ 4-d)
  constructor
  · nlinarith
  · apply (div_le_iff₀ hp).2
    nlinarith

theorem mixture_shape_bound (m q : ℝ) (hm : 1 ≤ m) (hq : q ≤ 5*m-4) :
    (q-2*m+3)/(m+1)^2 ≤ (9/16:ℝ) := by
  have hp : 0 < (m+1)^2 := sq_pos_of_pos (by linarith)
  apply (div_le_iff₀ hp).2
  nlinarith [sq_nonneg (3*m-5)]

theorem mixture_energy_bound (m h : ℝ) (hm : 1 ≤ m)
    (hh : h ≤ (5-m)/4) : h*(m+1)^2/4 ≤ 2 := by
  have hprod := mul_nonneg (sq_nonneg (m-3)) (by linarith : 0 ≤ m+3)
  have hmul := mul_le_mul_of_nonneg_right hh (sq_nonneg (m+1))
  nlinarith

theorem shape_mismatch (s : ℝ) (hs : s ≤ (9/16:ℝ)) : s ≠ (3/2:ℝ) := by
  linarith

theorem energy_mismatch (r : ℝ) (hr : r ≤ 2) : r ≠ 64*Real.pi := by
  have hp := Real.pi_gt_three
  linarith

#print axioms dimension_chords
#print axioms mixture_shape_bound
#print axioms mixture_energy_bound
#print axioms shape_mismatch
#print axioms energy_mismatch
end Dilaton32Pi
