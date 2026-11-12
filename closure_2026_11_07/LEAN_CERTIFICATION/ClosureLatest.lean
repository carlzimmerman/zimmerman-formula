import Mathlib

/-!
Exact algebraic consequences of the 2026-11-07 closure results.
Source bounds are hypotheses, not conclusions of this certificate.
WL1's coherent response model and FA3's pointwise source ordering remain inputs.
Memory is formalized for arbitrary finite sums, not continuous causal kernels.
Kappa = 1/2 FITTED; not theory closed.
-/
namespace ClosureLatest

/-- EW2, Delta = 0: no real scale satisfies both reported bounds. -/
theorem aest_window_empty (m : ℝ) : ¬ (10 ≤ m ∧ m ≤ 63 / 1000) := by
  rintro ⟨hw, hh⟩
  linarith

/-- Even the reported free-Delta envelope leaves no scale. -/
theorem aest_envelope_empty (m : ℝ) : ¬ (10 ≤ m ∧ m ≤ 1 / 10) := by
  rintro ⟨hw, hh⟩
  linarith

/-- The quoted x160 gap is rounded: its exact threshold ratio is 10000/63. -/
theorem aest_gap_ratio : (10 : ℝ) / (63 / 1000) = 10000 / 63 ∧
    (158 : ℝ) < 10000 / 63 ∧ (10000 / 63 : ℝ) < 160 := by
  norm_num

/-- WL1: even the smallest reported self-consistent population value fails
the coherent response gate. Applies separately to both footings, whose other
reported q values are larger. This does not prove the halo response model. -/
theorem population_gate_fails {q : ℝ} (hq : 384 / 1000 ≤ q) :
    1072 / 1000 < (1 + q) ^ 2 := by
  nlinarith [sq_nonneg (q - 384 / 1000)]

/-- 0.0354 is a rounded ceiling, not an exact equivalent of r <= 1.072. -/
theorem rounded_population_ceiling :
    (1072 / 1000 : ℝ) < (1 + 354 / 10000) ^ 2 := by
  norm_num

/-- FA3, finite-sum reading: a shared nonnegative kernel preserves a
pointwise web/host source bound. No normalization of the kernel is needed. -/
theorem positive_memory_order {ι : Type*} (s : Finset ι)
    (w web host : ι → ℝ) (c : ℝ)
    (hw : ∀ i ∈ s, 0 ≤ w i) (hsource : ∀ i ∈ s, c * host i ≤ web i) :
    c * (∑ i ∈ s, w i * host i) ≤ ∑ i ∈ s, w i * web i := by
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro i hi
  calc c * (w i * host i) = w i * (c * host i) := by ring
       _ ≤ w i * web i := mul_le_mul_of_nonneg_left (hsource i hi) (hw i hi)

/-- General incompatibility, conditional on the source-ordering conclusion. -/
theorem memory_window_empty {web host c hostMin webMax : ℝ}
    (hc : 0 ≤ c) (horder : c * host ≤ web) (hh : hostMin ≤ host)
    (hw : web ≤ webMax) (hgap : webMax < c * hostMin) : False := by
  have := mul_le_mul_of_nonneg_left hh hc
  linarith

/-- A weaker coefficient than FA3's quoted 0.17 still separates the gates,
IF the corresponding web/host ordering has been established. -/
theorem memory_numeric_empty {web host : ℝ}
    (horder : (33 / 1000) * host ≤ web) (hh : 816 / 1000 ≤ host)
    (hw : web ≤ 5 / 1000) : False := by
  nlinarith

/-- A low endpoint in a reported range does not imply the 0.17 coefficient. -/
theorem memory_range_caution : ¬ ((17 / 100 : ℝ) ≤ 33 / 1000) := by
  norm_num

/-- Concrete counterexample to EW2 MUTATE M1 (a0 = g = 1). -/
theorem cap_identity_counterexample : (1 : ℝ) * 1 / (1 + 1) ≠ 1 := by
  norm_num

/-- Concrete counterexample to EW2 MUTATE M2: one mode with w=1, B=2,
empty band S and b=2 gives an alleged reversed inequality 1 <= 0. -/
theorem reversed_leakage_counterexample :
    ¬ ((1 : ℝ) * 2 - 1 ≤ (2 - 1) * 0) := by
  norm_num

end ClosureLatest

#print axioms ClosureLatest.aest_window_empty
#print axioms ClosureLatest.aest_envelope_empty
#print axioms ClosureLatest.aest_gap_ratio
#print axioms ClosureLatest.population_gate_fails
#print axioms ClosureLatest.rounded_population_ceiling
#print axioms ClosureLatest.positive_memory_order
#print axioms ClosureLatest.memory_window_empty
#print axioms ClosureLatest.memory_numeric_empty
#print axioms ClosureLatest.memory_range_caution
#print axioms ClosureLatest.cap_identity_counterexample
#print axioms ClosureLatest.reversed_leakage_counterexample
