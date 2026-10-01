import Mathlib
open MeasureTheory Real

theorem setIcc_to_ivl (f : ℝ → ℝ) (a b : ℝ) (hab : a ≤ b) :
    ∫ x in Set.Icc a b, f x ∂volume = ∫ x in a..b, f x := by
  rw [← setIntegral_congr_set Ioc_ae_eq_Icc, ← intervalIntegral.integral_of_le hab]

/-- Per-slice substitution (conductor bank, zero-sorry): r = sqrt(u^2+w^2). -/
theorem slice_subst (H : ℝ → ℝ → ℝ) (hHc : Continuous (fun p : ℝ × ℝ => H p.1 p.2))
    (w : ℝ) (hw : 0 ≤ w) (hw1 : w ≤ 1) (c : ℝ) :
    ∫ r in w..1, r * H (Real.sqrt (r ^ 2 - w ^ 2)) c
      = ∫ u in (0:ℝ)..Real.sqrt (1 - w ^ 2), u * H u c := by
  sorry
