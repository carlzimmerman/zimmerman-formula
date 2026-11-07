import Mathlib
open MeasureTheory
namespace LimberKernel

/-- GL2's code-transcribed geometric weight, without the Poisson k^-4 factor.
The Limber and Poisson physical identifications are inputs to this certificate. -/
noncomputable def oldWeight (chi sourceChi z H P : ℝ) : ℝ :=
  ((sourceChi-chi)/(chi*sourceChi))^2 * (1+z)^2 / H * P / chi^2

/-- The inverse fourth power is evaluated at k = ell/chi (ell=L+1/2). -/
theorem poisson_factor {ell chi : ℝ} (hl : ell ≠ 0) (hc : chi ≠ 0) :
    1/(ell/chi)^4 = (chi/ell)^4 := by
  field_simp

theorem corrected_weight {chi sourceChi z H P ell : ℝ}
    (hc : chi ≠ 0) (hs : sourceChi ≠ 0) (hH : H ≠ 0) (hl : ell ≠ 0) :
    oldWeight chi sourceChi z H P * (chi/ell)^4 =
      (sourceChi-chi)^2 * (1+z)^2 * P / (sourceChi^2*H*ell^4) := by
  unfold oldWeight
  field_simp

/-- Dropping the correction leaves an inverse-fourth radial factor. -/
theorem old_weight_radial_power {chi sourceChi z H P : ℝ}
    (hc : chi ≠ 0) (hs : sourceChi ≠ 0) (hH : H ≠ 0) :
    oldWeight chi sourceChi z H P =
      (sourceChi-chi)^2*(1+z)^2*P/(sourceChi^2*H*chi^4) := by
  unfold oldWeight
  field_simp

/-- A factor common to every slice at fixed ell cancels from a ratio. -/
theorem common_factor_cancels (num den c : ℝ) (hc : c ≠ 0) :
    (c*num)/(c*den) = num/den := by
  field_simp

/-- Correct finite quadrature ratio: ell^-4 cancels; chi_i^4 stays inside
both weighted sums. No numerical power spectrum is assumed to be correct. -/
theorem corrected_quadrature {ι : Type*} (s : Finset ι) (w P chi R : ι → ℝ)
    (ell : ℝ) (hl : ell ≠ 0) :
    (∑ i ∈ s, (w i * P i * chi i^4 / ell^4) * R i^2) /
      (∑ i ∈ s, w i * P i * chi i^4 / ell^4) =
    (∑ i ∈ s, w i * P i * chi i^4 * R i^2) /
      (∑ i ∈ s, w i * P i * chi i^4) := by
  have hnum : (∑ i ∈ s, (w i*P i*chi i^4/ell^4)*R i^2) =
      (1/ell^4) * (∑ i ∈ s, w i*P i*chi i^4*R i^2) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i hi
    ring
  have hden : (∑ i ∈ s, w i*P i*chi i^4/ell^4) =
      (1/ell^4) * (∑ i ∈ s, w i*P i*chi i^4) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i hi
    ring
  rw [hnum,hden]
  exact common_factor_cancels _ _ (1/ell^4) (by positivity)

/-- Exact covariance identity: reweighting by a slice-dependent factor
preserves the response iff the cross-product (covariance numerator) vanishes. -/
theorem reweighting_difference (a b A B : ℝ) (hb : b ≠ 0) (hB : B ≠ 0) :
    A/B-a/b = (A*b-a*B)/(B*b) := by
  field_simp

theorem reweighting_invariant_iff (a b A B : ℝ) (hb : b ≠ 0) (hB : B ≠ 0) :
    A/B = a/b ↔ A*b = a*B := by
  exact div_eq_div_iff hB hb

/-- Positive two-slice example. Responses squared are 0 and 1; radial
corrections are 1^4 and 2^4. Equal factors would cancel; these do not. -/
theorem radial_factor_does_not_cancel :
    ((1 : ℝ)*0^2+1*1^2)/(1+1) = 1/2 ∧
    ((1 : ℝ)*1^4*0^2+1*2^4*1^2)/(1*1^4+1*2^4) = 16/17 ∧
    (1/2 : ℝ) ≠ 16/17 := by
  norm_num

/-- If the response is constant in every slice, any nonnegative correction
with nonzero total weight does preserve it. The correction need not change
all ratios or move any particular observational label. -/
theorem constant_response (s : Finset ℕ) (w : ℕ → ℝ) (r : ℝ)
    (hden : (∑ i ∈ s, w i) ≠ 0) :
    (∑ i ∈ s, w i*r)/(∑ i ∈ s, w i) = r := by
  rw [← Finset.sum_mul]
  field_simp

/-- Continuum analogue of the fixed-ell cancellation. No slice-dependent
factor can be moved out by this theorem. -/
theorem continuous_common_factor {α : Type*} [MeasurableSpace α]
    (μ : MeasureTheory.Measure α) (f g : α → ℝ) (c : ℝ) (hc : c ≠ 0) :
    (∫ x, c*f x ∂μ)/(∫ x, c*g x ∂μ) = (∫ x, f x ∂μ)/(∫ x, g x ∂μ) := by
  rw [MeasureTheory.integral_const_mul,MeasureTheory.integral_const_mul]
  exact common_factor_cancels _ _ c hc

/-- A power suppression confined to a set of slices can change the weighted
mean by no more than those slices' total corrected weight. This quantifies
power only when the corrected weights and affected set have been established. -/
theorem suppression_weight_bound {ι : Type*} (s S : Finset ι) (hS : S ⊆ s)
    (w response : ι → ℝ)
    (hw : ∀ i ∈ s, 0 ≤ w i) (hsum : ∑ i ∈ s, w i = 1)
    (hr0 : ∀ i ∈ s, 0 ≤ response i) (hr1 : ∀ i ∈ s, response i ≤ 1)
    (hoff : ∀ i ∈ s, i ∉ S → response i = 1) :
    0 ≤ 1-(∑ i ∈ s, w i*response i) ∧
    1-(∑ i ∈ s, w i*response i) ≤ ∑ i ∈ S, w i := by
  have heq : 1-(∑ i ∈ s, w i*response i) = ∑ i ∈ s, w i*(1-response i) := by
    simp only [mul_sub,mul_one,Finset.sum_sub_distrib,hsum]
  rw [heq]
  constructor
  · apply Finset.sum_nonneg
    intro i hi
    exact mul_nonneg (hw i hi) (sub_nonneg.mpr (hr1 i hi))
  · have hsupport : (∑ i ∈ s, w i*(1-response i)) = ∑ i ∈ S, w i*(1-response i) := by
      symm
      apply Finset.sum_subset hS
      intro i hi hni
      rw [hoff i hi hni]
      ring
    rw [hsupport]
    apply Finset.sum_le_sum
    intro i hi
    have hwi := hw i (hS hi)
    have hri := hr0 i (hS hi)
    nlinarith

end LimberKernel
#print axioms LimberKernel.poisson_factor
#print axioms LimberKernel.corrected_weight
#print axioms LimberKernel.old_weight_radial_power
#print axioms LimberKernel.common_factor_cancels
#print axioms LimberKernel.corrected_quadrature
#print axioms LimberKernel.reweighting_difference
#print axioms LimberKernel.reweighting_invariant_iff
#print axioms LimberKernel.radial_factor_does_not_cancel
#print axioms LimberKernel.constant_response

#print axioms LimberKernel.continuous_common_factor
#print axioms LimberKernel.suppression_weight_bound
