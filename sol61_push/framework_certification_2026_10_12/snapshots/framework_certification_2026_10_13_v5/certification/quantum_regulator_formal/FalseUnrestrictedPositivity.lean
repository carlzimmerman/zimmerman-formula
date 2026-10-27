import NREnergy

/-! Fixed-regulator quantum quadratic-form completion. Imports Mathlib via the
archived checked OWN NREnergy coefficient certificate. A,B map E to F, including
annihilation maps H_Q to H_(Q-2); no A/B commutation or scalar field replacement.
Complete complex inner-product spaces include finite charge sectors. Physical
NR/regulator/normal-ordering assumptions are explicit in correspondence.
No evolution invariance, gravity, continuum or renormalized UV claim. -/
noncomputable section
open scoped InnerProduct
namespace FrameworkQuantumEnergy
variable {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

def interactionForm (δ c k : ℝ) (A B : E →L[ℂ] F) (v : E) : ℝ :=
  δ * ‖B v‖ ^ 2 + 2 * c * RCLike.re (inner ℂ (B v) (A v)) + k * ‖A v‖ ^ 2

def interactionOperator (δ c k : ℝ) (A B : E →L[ℂ] F) : E →L[ℂ] E :=
  (δ : ℂ) • (B.adjoint.comp B) +
    (c : ℂ) • (B.adjoint.comp A + A.adjoint.comp B) + (k : ℂ) • (A.adjoint.comp A)

omit [CompleteSpace E] [CompleteSpace F] in
/-- Genuine Hilbert-space norm identity for arbitrary operator-applied vectors. -/
theorem quadratic_form_completion (δ c k : ℝ) (A B : E →L[ℂ] F) (v : E) (hδ : δ ≠ 0) :
    interactionForm δ c k A B v =
      δ * ‖B v + ((c / δ : ℝ) : ℂ) • A v‖ ^ 2 + (k - c ^ 2 / δ) * ‖A v‖ ^ 2 := by
  rw [norm_add_sq (𝕜 := ℂ), inner_smul_right, norm_smul, mul_pow,
    Complex.norm_real, Real.norm_eq_abs, sq_abs]
  have hr (r : ℝ) (z : ℂ) : RCLike.re ((r : ℂ) * z) = r * RCLike.re z :=
    Complex.re_ofReal_mul r z
  rw [hr]
  unfold interactionForm
  field_simp
  ring

/-- The form is exactly the normal-ordered A-dagger-A/B-dagger-B operator form. -/
theorem adjoint_form_correspondence (δ c k : ℝ) (A B : E →L[ℂ] F) (v : E) :
    RCLike.re (inner ℂ v (interactionOperator δ c k A B v)) = interactionForm δ c k A B v := by
  have hr (r : ℝ) (z : ℂ) : RCLike.re ((r : ℂ) * z) = r * RCLike.re z :=
    Complex.re_ofReal_mul r z
  simp only [interactionOperator, add_apply, smul_apply,
    ContinuousLinearMap.comp_apply, inner_add_right, inner_smul_right,
    ContinuousLinearMap.adjoint_inner_right, map_add, hr]
  rw [inner_re_symm (𝕜 := ℂ) (A v) (B v),
    inner_self_eq_norm_sq (𝕜 := ℂ) (B v), inner_self_eq_norm_sq (𝕜 := ℂ) (A v)]
  unfold interactionForm
  ring

omit [CompleteSpace E] [CompleteSpace F] in
theorem interaction_nonnegative (δ c k : ℝ) (A B : E →L[ℂ] F) (v : E)
    (hδ : 0 < δ) (hk : 0 ≤ k - c ^ 2 / δ) : 0 ≤ interactionForm δ c k A B v := by
  rw [quadratic_form_completion δ c k A B v hδ.ne']
  positivity

omit [CompleteSpace E] [CompleteSpace F] in
/-- Positivity uses the actual derived OWN NR coefficients, not an assumed leaf. -/
theorem actual_nr_interaction_nonnegative (m M g rep : ℝ) (A B : E →L[ℂ] F) (v : E)
    (hm : 0 < m) (hM : 2 * m < M) (hrep : 0 ≤ rep) :
    0 ≤ interactionForm (FrameworkNREnergy.delta m M) (FrameworkNREnergy.c3 m M g)
      (FrameworkNREnergy.quartic m M g rep) A B v := by
  apply interaction_nonnegative
  · unfold FrameworkNREnergy.delta; linarith
  · exact FrameworkNREnergy.remainder_nonnegative m M g rep hm hM hrep

/-- On any vector, a positive kinetic quadratic form is bounded by total D form. -/
theorem actual_nr_energy_bound (m M g rep : ℝ) (A B : E →L[ℂ] F) (T : E →L[ℂ] E)
    (v : E) (hm : 0 < m) (hM : 2 * m < M) (hrep : 0 ≤ rep)
    (hT : 0 ≤ RCLike.re (inner ℂ v (T v))) :
    0 ≤ RCLike.re (inner ℂ v (T v)) ∧
      RCLike.re (inner ℂ v (T v)) ≤
        RCLike.re (inner ℂ v ((T + interactionOperator (FrameworkNREnergy.delta m M)
          (FrameworkNREnergy.c3 m M g) (FrameworkNREnergy.quartic m M g rep) A B) v)) := by
  have hi := actual_nr_interaction_nonnegative m M g rep A B v hm hM hrep
  rw [add_apply, inner_add_right, map_add, adjoint_form_correspondence]
  exact ⟨hT, by linarith⟩

omit [CompleteSpace E] [CompleteSpace F] in
/-- Finite regulator sums preserve the positive bound, with explicit positive weights. -/
theorem finite_regulator_form_bound {ι : Type*} (s : Finset ι) (m M g rep : ℝ)
    (A B : ι → E →L[ℂ] F) (weights : ι → ℝ) (T : E →L[ℂ] E) (v : E)
    (hm : 0 < m) (hM : 2 * m < M) (hrep : 0 ≤ rep)
    (hw : ∀ i ∈ s, 0 ≤ weights i) (hT : 0 ≤ RCLike.re (inner ℂ v (T v))) :
    0 ≤ RCLike.re (inner ℂ v (T v)) ∧
      RCLike.re (inner ℂ v (T v)) ≤ RCLike.re (inner ℂ v (T v)) +
        ∑ i ∈ s, weights i * interactionForm (FrameworkNREnergy.delta m M)
          (FrameworkNREnergy.c3 m M g) (FrameworkNREnergy.quartic m M g rep) (A i) (B i) v := by
  have hs : 0 ≤ ∑ i ∈ s, weights i * interactionForm (FrameworkNREnergy.delta m M)
      (FrameworkNREnergy.c3 m M g) (FrameworkNREnergy.quartic m M g rep) (A i) (B i) v := by
    apply Finset.sum_nonneg
    intro i hi
    exact mul_nonneg (hw i hi) (actual_nr_interaction_nonnegative m M g rep (A i) (B i) v hm hM hrep)
  exact ⟨hT, by linarith⟩

omit [CompleteSpace E] [CompleteSpace F] in
/-- Dimensionless cell annihilators require c/sqrt(volume), k/volume;
 the same exact own-coefficient positivity holds for every positive cell volume. -/
theorem cell_normalized_interaction_nonnegative (m M g rep volume : ℝ)
    (A B : E →L[ℂ] F) (v : E) (hm : 0 < m) (hM : 2 * m < M)
    (hrep : 0 ≤ rep) (hvolume : 0 < volume) :
    0 ≤ interactionForm (FrameworkNREnergy.delta m M)
      (FrameworkNREnergy.c3 m M g / Real.sqrt volume)
      (FrameworkNREnergy.quartic m M g rep / volume) A B v := by
  apply interaction_nonnegative
  · unfold FrameworkNREnergy.delta; linarith
  · have he : FrameworkNREnergy.quartic m M g rep / volume -
        (FrameworkNREnergy.c3 m M g / Real.sqrt volume) ^ 2 / FrameworkNREnergy.delta m M =
        FrameworkNREnergy.remainder m M g rep / volume := by
      rw [div_pow, Real.sq_sqrt hvolume.le]
      unfold FrameworkNREnergy.remainder
      ring
    rw [he]
    exact div_nonneg (FrameworkNREnergy.remainder_nonnegative m M g rep hm hM hrep) hvolume.le

end FrameworkQuantumEnergy
#print axioms FrameworkQuantumEnergy.quadratic_form_completion
#print axioms FrameworkQuantumEnergy.adjoint_form_correspondence
#print axioms FrameworkQuantumEnergy.interaction_nonnegative
#print axioms FrameworkQuantumEnergy.actual_nr_interaction_nonnegative
#print axioms FrameworkQuantumEnergy.actual_nr_energy_bound
#print axioms FrameworkQuantumEnergy.finite_regulator_form_bound

#print axioms FrameworkQuantumEnergy.cell_normalized_interaction_nonnegative

/- EXPECTED FAILURE: delta>0 alone cannot ensure positive interaction operator form. -/
example : 0 ≤ FrameworkQuantumEnergy.interactionForm 1 1 0
    (ContinuousLinearMap.id ℂ ℂ) (-(ContinuousLinearMap.id ℂ ℂ)) (1 : ℂ) := by
  norm_num [FrameworkQuantumEnergy.interactionForm, inner, RCLike.re, neg_apply]
