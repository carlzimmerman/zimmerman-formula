import Mathlib

open MeasureTheory Set
open scoped RealInnerProductSpace

namespace MemoryKernel

/-- Shared measure and shared nonnegative kernel; integrability is explicit. -/
theorem integral_order {α : Type*} [MeasurableSpace α] (μ : Measure α)
    (k web host : α → ℝ) (c : ℝ)
    (hiw : Integrable (fun s => k s * web s) μ)
    (hih : Integrable (fun s => k s * host s) μ)
    (hk : ∀ᵐ s ∂μ, 0 ≤ k s) (ho : ∀ᵐ s ∂μ, c * host s ≤ web s) :
    c * (∫ s, k s * host s ∂μ) ≤ ∫ s, k s * web s ∂μ := by
  rw [← integral_const_mul]
  apply integral_mono_ae (hih.const_mul c) hiw
  filter_upwards [hk, ho] with s hs ht
  nlinarith [mul_le_mul_of_nonneg_left ht hs]

/-- A source cap bounds the filtered response without assuming a constant history. -/
theorem source_cap {α : Type*} [MeasurableSpace α] (μ : Measure α)
    (k src : α → ℝ) (cap : ℝ) (hkInt : Integrable k μ)
    (hInt : Integrable (fun s => k s * src s) μ)
    (hk : ∀ᵐ s ∂μ, 0 ≤ k s) (hc : ∀ᵐ s ∂μ, src s ≤ cap) :
    (∫ s, k s * src s ∂μ) ≤ cap * ∫ s, k s ∂μ := by
  rw [← integral_const_mul]
  apply integral_mono_ae hInt (hkInt.const_mul cap)
  filter_upwards [hk, hc] with s hs ht
  nlinarith [mul_le_mul_of_nonneg_left ht hs]

/-- Projection, not comparison of vector magnitudes, prevents cancellation. -/
theorem vector_cone_bound {α E : Type*} [MeasurableSpace α]
    [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    (μ : Measure α) (v : α → E) (f : α → ℝ) (e : E)
    (hv : Integrable v μ) (hf : Integrable f μ) (he : ‖e‖ = 1)
    (hp : ∀ᵐ s ∂μ, f s ≤ ⟪e, v s⟫) :
    (∫ s, f s ∂μ) ≤ ‖∫ s, v s ∂μ‖ := by
  calc (∫ s, f s ∂μ) ≤ ∫ s, ⟪e, v s⟫ ∂μ := integral_mono_ae hf (hv.const_inner e) hp
       _ = ⟪e, ∫ s, v s ∂μ⟫ := integral_inner hv e
       _ ≤ ‖e‖ * ‖∫ s, v s ∂μ‖ := real_inner_le_norm _ _
       _ = ‖∫ s, v s ∂μ‖ := by rw [he, one_mul]

/-- A fixed nonzero reference direction converts a cone lower bound to a
normalized response bound. The weighted vector field must be integrable. -/
theorem normalized_vector_bound {α E : Type*} [MeasurableSpace α]
    [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    (μ : Measure α) (k : α → ℝ) (v : α → E) (e : E) (b : ℝ)
    (hkInt : Integrable k μ) (hv : Integrable (fun s => k s • v s) μ)
    (hk : ∀ᵐ s ∂μ, 0 ≤ k s) (he : ‖e‖ = 1)
    (hp : ∀ᵐ s ∂μ, b ≤ ⟪e, v s⟫) :
    b * (∫ s, k s ∂μ) ≤ ‖∫ s, k s • v s ∂μ‖ := by
  rw [← integral_const_mul]
  apply vector_cone_bound μ _ _ e hv (hkInt.const_mul b) he
  filter_upwards [hk, hp] with s hs ht
  simp only [inner_smul_right]
  nlinarith [mul_le_mul_of_nonneg_left ht hs]

/-- Nonincreasing kernels retain at least the age fraction at an earlier epoch.
This hypothesis is stronger than positivity and is necessary for this route. -/
theorem decreasing_kernel_age_fraction (k : ℝ → ℝ) {t T : ℝ}
    (ht : 0 < t) (htT : t ≤ T) (hdec : AntitoneOn k (Icc 0 T)) :
    t * (∫ s in (0 : ℝ)..T, k s) ≤ T * (∫ s in (0 : ℝ)..t, k s) := by
  have hT : 0 < T := lt_of_lt_of_le ht htT
  have hscaled (a : ℝ) (ha : 0 < a) (haT : a ≤ T) :
      AntitoneOn (fun u => k (a * u)) (uIcc (0 : ℝ) 1) := by
    rw [uIcc_of_le (by norm_num : (0 : ℝ) ≤ 1)]
    intro x hx y hy hxy
    apply hdec
    · exact ⟨mul_nonneg ha.le hx.1, by nlinarith [mul_le_mul_of_nonneg_left hx.2 ha.le]⟩
    · exact ⟨mul_nonneg ha.le hy.1, by nlinarith [mul_le_mul_of_nonneg_left hy.2 ha.le]⟩
    · exact mul_le_mul_of_nonneg_left hxy ha.le
  have h := intervalIntegral.integral_mono_on (μ := volume) (by norm_num : (0 : ℝ) ≤ 1)
    (hscaled T hT le_rfl).intervalIntegrable (hscaled t ht htT).intervalIntegrable
    (fun u hu => hdec
      ⟨mul_nonneg ht.le hu.1, by nlinarith [mul_le_mul_of_nonneg_left hu.2 ht.le]⟩
      ⟨mul_nonneg hT.le hu.1, by nlinarith [mul_le_mul_of_nonneg_left hu.2 hT.le]⟩
      (mul_le_mul_of_nonneg_right htT hu.1))
  rw [intervalIntegral.integral_comp_mul_left k hT.ne',
      intervalIntegral.integral_comp_mul_left k ht.ne'] at h
  have hd : (∫ s in (0 : ℝ)..T, k s) / T ≤ (∫ s in (0 : ℝ)..t, k s) / t := by
    simpa [smul_eq_mul, div_eq_mul_inv, mul_comm] using h
  have := (div_le_div_iff₀ hT ht).mp hd
  nlinarith

/-- Positive relaxation kernels are in the decreasing-kernel class. -/
theorem exponential_antitone (τ : ℝ) (hτ : 0 < τ) :
    Antitone (fun s : ℝ => Real.exp (-s / τ) / τ) := by
  intro x y hxy
  apply div_le_div_of_nonneg_right _ hτ.le
  apply Real.exp_le_exp.mpr
  exact div_le_div_of_nonneg_right (by linarith) hτ.le

theorem exponential_age_fraction {τ t T : ℝ} (hτ : 0 < τ) (ht : 0 < t) (htT : t ≤ T) :
    t * (∫ s in (0 : ℝ)..T, Real.exp (-s / τ) / τ) ≤
      T * (∫ s in (0 : ℝ)..t, Real.exp (-s / τ) / τ) :=
  decreasing_kernel_age_fraction _ ht htT ((exponential_antitone τ hτ).antitoneOn _)

/-- The age-corrected gate contradiction, with a deliberately conservative
age fraction 3/4, response coefficient 0.033 and host floor 0.816. -/
theorem age_corrected_gate_empty {web host massEarly massToday : ℝ}
    (he : (3/4) * massToday ≤ massEarly)
    (hh : (33/1000) * host ≤ massToday)
    (hw : massEarly ≤ web) (hhost : 816/1000 ≤ host)
    (hweb : web ≤ 5/1000) : False := by
  nlinarith

/-- Magnitude ordering alone cannot prevent vector cancellation, already on
an equal-weight two-atom positive measure. -/
theorem magnitude_only_counterexample :
    |(1 : ℝ)| = 1 ∧ |(-1 : ℝ)| = 1 ∧ |(1/2 : ℝ) * 1 + (1/2) * (-1)| = 0 := by
  norm_num

/-- A vector-valued source cap gives the host bound used in the physical
argument; this is an upper bound and does not assume directional alignment. -/
theorem vector_source_cap {α E : Type*} [MeasurableSpace α]
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    (μ : Measure α) (k : α → ℝ) (v : α → E) (cap : ℝ)
    (hkInt : Integrable k μ) (hv : Integrable (fun s => k s • v s) μ)
    (hk : ∀ᵐ s ∂μ, 0 ≤ k s) (hc : ∀ᵐ s ∂μ, ‖v s‖ ≤ cap) :
    ‖∫ s, k s • v s ∂μ‖ ≤ cap * ∫ s, k s ∂μ := by
  calc ‖∫ s, k s • v s ∂μ‖ ≤ ∫ s, ‖k s • v s‖ ∂μ := norm_integral_le_integral_norm _
       _ ≤ ∫ s, cap * k s ∂μ := by
         apply integral_mono_ae hv.norm (hkInt.const_mul cap)
         filter_upwards [hk, hc] with s hs ht
         simp only [norm_smul, Real.norm_eq_abs, abs_of_nonneg hs]
         nlinarith [mul_le_mul_of_nonneg_left ht hs]
       _ = cap * ∫ s, k s ∂μ := integral_const_mul _ _

/-- Explicit earlier-age floor for kernels that decrease with delay. -/
theorem cumulative_age_floor (k : ℝ → ℝ) {t T : ℝ}
    (ht : 0 < t) (htT : t ≤ T) (hfrac : (3/4) * T ≤ t)
    (hdec : AntitoneOn k (Icc 0 T)) (hk : ∀ s ∈ Icc 0 T, 0 ≤ k s) :
    (3/4) * (∫ s in (0 : ℝ)..T, k s) ≤ ∫ s in (0 : ℝ)..t, k s := by
  have hT := lt_of_lt_of_le ht htT
  have hmass := intervalIntegral.integral_nonneg (μ := volume) hT.le hk
  have hage := decreasing_kernel_age_fraction k ht htT hdec
  nlinarith [mul_nonneg (sub_nonneg.mpr hfrac) hmass]

/-- This composes the continuous-kernel age theorem with the physical
response inequalities. Only the age comparison is discharged here. -/
theorem decreasing_kernel_gate_empty (k : ℝ → ℝ) {t T web host : ℝ}
    (ht : 0 < t) (htT : t ≤ T) (hfrac : (3/4) * T ≤ t)
    (hdec : AntitoneOn k (Icc 0 T)) (hk : ∀ s ∈ Icc 0 T, 0 ≤ k s)
    (hh : (33/1000) * host ≤ ∫ s in (0 : ℝ)..T, k s)
    (hw : (∫ s in (0 : ℝ)..t, k s) ≤ web)
    (hhost : 816/1000 ≤ host) (hweb : web ≤ 5/1000) : False := by
  exact age_corrected_gate_empty (cumulative_age_floor k ht htT hfrac hdec hk)
    hh hw hhost hweb


end MemoryKernel



#print axioms MemoryKernel.integral_order
#print axioms MemoryKernel.source_cap
#print axioms MemoryKernel.vector_cone_bound
#print axioms MemoryKernel.normalized_vector_bound
#print axioms MemoryKernel.decreasing_kernel_age_fraction
#print axioms MemoryKernel.exponential_antitone
#print axioms MemoryKernel.exponential_age_fraction
#print axioms MemoryKernel.age_corrected_gate_empty
#print axioms MemoryKernel.magnitude_only_counterexample
#print axioms MemoryKernel.vector_source_cap
#print axioms MemoryKernel.cumulative_age_floor
#print axioms MemoryKernel.decreasing_kernel_gate_empty
