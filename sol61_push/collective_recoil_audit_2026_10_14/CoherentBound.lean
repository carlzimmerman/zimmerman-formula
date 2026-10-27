import Mathlib

namespace CollectiveRecoil
open scoped BigOperators

theorem coherent_amplitude_bound {ι : Type*} (s : Finset ι) (a : ι → ℂ)
    (ha : ∀ j ∈ s, ‖a j‖ ≤ 1) : ‖∑ j ∈ s, a j‖ ≤ (s.card : ℝ) := by
  calc
    ‖∑ j ∈ s, a j‖ ≤ ∑ j ∈ s, ‖a j‖ := norm_sum_le _ _
    _ ≤ ∑ j ∈ s, (1 : ℝ) := Finset.sum_le_sum (by intro j hj; exact ha j hj)
    _ = (s.card : ℝ) := by simp

theorem coherent_intensity_bound {ι : Type*} (s : Finset ι) (a : ι → ℂ)
    (ha : ∀ j ∈ s, ‖a j‖ ≤ 1) (f : ℝ) (hf : 0 ≤ f) :
    f*‖∑ j ∈ s, a j‖^2 ≤ f*(s.card : ℝ)^2 := by
  have h := coherent_amplitude_bound s a ha
  have hn := norm_nonneg (∑ j ∈ s, a j)
  have hc : (0 : ℝ) ≤ s.card := by positivity
  have hs : ‖∑ j ∈ s, a j‖^2 ≤ (s.card : ℝ)^2 := by nlinarith
  exact mul_le_mul_of_nonneg_left hs hf

end CollectiveRecoil

#print axioms CollectiveRecoil.coherent_amplitude_bound
#print axioms CollectiveRecoil.coherent_intensity_bound
