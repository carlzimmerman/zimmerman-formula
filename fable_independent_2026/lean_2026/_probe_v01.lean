import Mathlib
open MeasureTheory Set intervalIntegral
noncomputable section
theorem intBdd (f : ℝ → ℝ) (a b : ℝ) (hc : Continuous f) :
    IntervalIntegrable f MeasureTheory.volume a b := hc.intervalIntegrable a b
set_option pp.explicit true in
example : ∫ x in (-1 : ℝ)..0, x ^ 2 + ∫ x in (0 : ℝ)..1, x ^ 2
    = ∫ x in (-1 : ℝ)..1, x ^ 2 := by
  exact integral_add_adjacent_intervals (a := (-1 : ℝ)) (b := 0) (c := 1)
    (f := fun x => x ^ 2) (μ := MeasureTheory.volume)
    (intBdd _ _ _ (by fun_prop)) (intBdd _ _ _ (by fun_prop))
