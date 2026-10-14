import Mathlib
namespace TransverseStrength
open scoped BigOperators

theorem finite_weighted_bound {ι : Type*} (s : Finset ι)
    (weight kernel : ι → ℝ) (ceiling : ℝ)
    (hw : ∀ i ∈ s, 0 ≤ weight i)
    (hk : ∀ i ∈ s, kernel i ≤ ceiling) :
    (∑ i ∈ s, weight i * kernel i) ≤ ceiling * ∑ i ∈ s, weight i := by
  calc
    (∑ i ∈ s, weight i * kernel i) ≤ ∑ i ∈ s, weight i * ceiling :=
      Finset.sum_le_sum (by intro i hi; exact mul_le_mul_of_nonneg_left (hk i hi) (hw i hi))
    _ = ceiling * ∑ i ∈ s, weight i := by rw [Finset.mul_sum]; apply Finset.sum_congr rfl; intro i hi; ring

theorem excitation_kernel_ceiling (x : ℝ) (hx : 0 ≤ x) :
    (1+x)/(1+2*x)^2 ≤ 1 := by
  have hp : 0 < (1+2*x)^2 := by positivity
  apply (div_le_iff₀ hp).2
  nlinarith [sq_nonneg x]
end TransverseStrength
#print axioms TransverseStrength.finite_weighted_bound
#print axioms TransverseStrength.excitation_kernel_ceiling
