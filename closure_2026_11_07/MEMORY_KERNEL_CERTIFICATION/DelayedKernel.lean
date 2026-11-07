import Mathlib
open MeasureTheory Set
namespace MemoryDelay
noncomputable def kernel (s : ℝ) : ℝ := 100 * max 0 (min (s - 4/5) (1 - s))

theorem kernel_continuous : Continuous kernel := by
  unfold kernel
  fun_prop

theorem kernel_nonneg (s : ℝ) : 0 ≤ kernel s := by
  unfold kernel
  positivity

theorem kernel_zero_left {s : ℝ} (hs : s ≤ 4/5) : kernel s = 0 := by
  unfold kernel
  have : min (s-4/5) (1-s) ≤ 0 := le_trans (min_le_left _ _) (by linarith)
  rw [max_eq_left this]; ring

theorem kernel_zero_right {s : ℝ} (hs : 1 ≤ s) : kernel s = 0 := by
  unfold kernel
  have : min (s-4/5) (1-s) ≤ 0 := le_trans (min_le_right _ _) (by linarith)
  rw [max_eq_left this]; ring

theorem kernel_rising {s : ℝ} (hs : s ∈ Icc (4/5 : ℝ) (9/10)) :
    kernel s = 100 * (s - 4/5) := by
  unfold kernel
  rw [min_eq_left (by linarith [hs.2]), max_eq_right (by linarith [hs.1])]

theorem kernel_falling {s : ℝ} (hs : s ∈ Icc (9/10 : ℝ) 1) :
    kernel s = 100 * (1 - s) := by
  unfold kernel
  rw [min_eq_right (by linarith [hs.1]), max_eq_right (by linarith [hs.2])]

theorem early_mass : (∫ s in (0 : ℝ)..(4/5), kernel s) = 0 := by
  have h : (∫ s in (0 : ℝ)..(4/5), kernel s) = ∫ _ in (0 : ℝ)..(4/5), (0 : ℝ) := by
    apply intervalIntegral.integral_congr
    intro s hs
    rw [uIcc_of_le (by norm_num : (0 : ℝ) ≤ 4/5)] at hs
    exact kernel_zero_left hs.2
  simpa using h

theorem rising_mass : (∫ s in (4/5 : ℝ)..(9/10), kernel s) = 1/2 := by
  have h : (∫ s in (4/5 : ℝ)..(9/10), kernel s) =
      ∫ s in (4/5 : ℝ)..(9/10), 100 * (s - 4/5) := by
    apply intervalIntegral.integral_congr
    intro s hs
    rw [uIcc_of_le (by norm_num : (4/5 : ℝ) ≤ 9/10)] at hs
    exact kernel_rising hs
  rw [h, intervalIntegral.integral_const_mul,
    intervalIntegral.integral_sub (f := fun s : ℝ => s) (g := fun _ : ℝ => (4/5 : ℝ))
      (continuous_id.intervalIntegrable _ _) (continuous_const.intervalIntegrable _ _),
    integral_id, intervalIntegral.integral_const]
  norm_num

theorem falling_mass : (∫ s in (9/10 : ℝ)..1, kernel s) = 1/2 := by
  have h : (∫ s in (9/10 : ℝ)..1, kernel s) =
      ∫ s in (9/10 : ℝ)..1, 100 * (1 - s) := by
    apply intervalIntegral.integral_congr
    intro s hs
    rw [uIcc_of_le (by norm_num : (9/10 : ℝ) ≤ 1)] at hs
    exact kernel_falling hs
  rw [h, intervalIntegral.integral_const_mul,
    intervalIntegral.integral_sub (f := fun _ : ℝ => (1 : ℝ)) (g := fun s : ℝ => s)
      (continuous_const.intervalIntegrable _ _) (continuous_id.intervalIntegrable _ _),
    integral_id, intervalIntegral.integral_const]
  norm_num

theorem today_mass : (∫ s in (0 : ℝ)..1, kernel s) = 1 := by
  have h1 := intervalIntegral.integral_add_adjacent_intervals
    (kernel_continuous.intervalIntegrable (μ := volume) 0 (4/5)) (kernel_continuous.intervalIntegrable (μ := volume) (4/5) (9/10))
  have h2 := intervalIntegral.integral_add_adjacent_intervals
    (kernel_continuous.intervalIntegrable (μ := volume) 0 (9/10)) (kernel_continuous.intervalIntegrable (μ := volume) (9/10) 1)
  rw [early_mass, rising_mass] at h1
  rw [← h1, falling_mass] at h2
  linarith

theorem global_mass : (∫ s : ℝ, kernel s) = 1 := by
  have hsup : Function.support kernel ⊆ Ioc (0 : ℝ) 1 := by
    intro s hs
    constructor
    · by_contra hn
      have hz := kernel_zero_left (s := s) (by linarith [not_lt.mp hn])
      exact hs hz
    · by_contra hn
      have hz := kernel_zero_right (s := s) (by linarith [not_le.mp hn])
      exact hs hz
  rw [← intervalIntegral.integral_eq_integral_of_support_subset hsup]
  exact today_mass

/-- The delayed kernel is integrable on the whole line. -/
theorem kernel_integrable : Integrable kernel (volume : Measure ℝ) := by
  apply kernel_continuous.integrable_of_hasCompactSupport
  apply HasCompactSupport.intro (isCompact_Icc : IsCompact (Icc (0 : ℝ) 1))
  intro x hx
  by_cases h : x ≤ 4/5
  · exact kernel_zero_left h
  · apply kernel_zero_right
    have : ¬ x ≤ 1 := by
      intro h1
      exact hx ⟨by linarith,h1⟩
    linarith

theorem kernel_causal_mass : (∫ s in Ioi (0 : ℝ), kernel s) = 1 := by
  rw [setIntegral_eq_integral_of_forall_compl_eq_zero, global_mass]
  intro s hs
  apply kernel_zero_left
  simp only [mem_Ioi,not_lt] at hs
  linarith

/-- Adding a small exponential tail makes the kernel strictly positive,
while preserving unit total causal mass. -/
noncomputable def positiveKernel (s : ℝ) : ℝ :=
  (999/1000) * kernel s + (1/1000) * Real.exp (-s)

theorem positiveKernel_continuous : Continuous positiveKernel := by
  unfold positiveKernel
  exact (continuous_const.mul kernel_continuous).add (by fun_prop)

theorem positiveKernel_pos (s : ℝ) : 0 < positiveKernel s := by
  unfold positiveKernel
  have h0 := kernel_nonneg s
  have hp := Real.exp_pos (-s)
  nlinarith

theorem positiveKernel_integrable : IntegrableOn positiveKernel (Ioi (0 : ℝ)) := by
  exact (kernel_integrable.integrableOn.const_mul (999/1000)).add
    ((integrableOn_exp_neg_Ioi 0).const_mul (1/1000))

theorem positiveKernel_causal_mass : (∫ s in Ioi (0 : ℝ), positiveKernel s) = 1 := by
  unfold positiveKernel
  rw [integral_add (kernel_integrable.integrableOn.const_mul (999/1000))
      ((integrableOn_exp_neg_Ioi 0).const_mul (1/1000)),
    integral_const_mul,integral_const_mul,kernel_causal_mass,integral_exp_neg_Ioi_zero]
  norm_num

theorem positiveKernel_today_floor : (999/1000 : ℝ) ≤ ∫ s in (0 : ℝ)..1, positiveKernel s := by
  have h := intervalIntegral.integral_mono_on (μ := volume) (by norm_num : (0 : ℝ) ≤ 1)
    ((continuous_const.mul kernel_continuous).intervalIntegrable 0 1)
    (positiveKernel_continuous.intervalIntegrable 0 1)
    (fun s _ => show (999/1000) * kernel s ≤ positiveKernel s from by
      unfold positiveKernel
      have := Real.exp_pos (-s)
      linarith)
  simp only [Pi.mul_apply] at h
  rw [intervalIntegral.integral_const_mul,today_mass] at h
  simpa using h

theorem positiveKernel_early_ceiling :
    (∫ s in (0 : ℝ)..(4/5), positiveKernel s) ≤ 1/1000 := by
  have h := intervalIntegral.integral_mono_on (μ := volume) (by norm_num : (0 : ℝ) ≤ 4/5)
    (positiveKernel_continuous.intervalIntegrable 0 (4/5))
    (continuous_const.intervalIntegrable 0 (4/5))
    (fun s hs => show positiveKernel s ≤ (1/1000 : ℝ) from by
      unfold positiveKernel
      rw [kernel_zero_left hs.2]
      have hExp : Real.exp (-s) ≤ 1 := by
        rw [← Real.exp_zero]
        exact Real.exp_le_exp.mpr (by linarith [hs.1])
      nlinarith)
  rw [intervalIntegral.integral_const] at h
  norm_num at h ⊢
  linarith

/-- A genuine normalized, integrable, continuous, strictly positive causal
kernel defeats a cross-epoch lower bound, even with identical constant sources.
This does not claim that the delayed kernel passes the observational W1 gate. -/
theorem normalized_positive_counterexample :
    ∃ k : ℝ → ℝ, Continuous k ∧ (∀ s, 0 < k s) ∧
      IntegrableOn k (Ioi (0 : ℝ)) ∧ (∫ s in Ioi (0 : ℝ), k s) = 1 ∧
      (816/1000 : ℝ) ≤ (∫ s in (0 : ℝ)..1, k s) ∧
      (∫ s in (0 : ℝ)..(4/5), k s) < (5/1000 : ℝ) := by
  refine ⟨positiveKernel,positiveKernel_continuous,positiveKernel_pos,
    positiveKernel_integrable,positiveKernel_causal_mass,?_,?_⟩
  · have := positiveKernel_today_floor
    linarith
  · have := positiveKernel_early_ceiling
    linarith

/-- The delayed component contributes exactly zero at any earlier epoch
up to 4/5 of today's age, for any scalar or vector source history. -/
theorem delayed_source_zero {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (v : ℝ → E) {t : ℝ} (ht : 0 ≤ t) (htmax : t ≤ 4/5) :
    (∫ s in (0 : ℝ)..t, kernel s • v s) = 0 := by
  calc (∫ s in (0 : ℝ)..t, kernel s • v s) = ∫ _ in (0 : ℝ)..t, (0 : E) := by
         apply intervalIntegral.integral_congr
         intro s hs
         rw [uIcc_of_le ht] at hs
         dsimp only
         rw [kernel_zero_left (le_trans hs.2 htmax),zero_smul]
       _ = 0 := by simp

end MemoryDelay


#print axioms MemoryDelay.kernel_continuous
#print axioms MemoryDelay.kernel_nonneg
#print axioms MemoryDelay.kernel_zero_left
#print axioms MemoryDelay.kernel_zero_right
#print axioms MemoryDelay.kernel_rising
#print axioms MemoryDelay.kernel_falling
#print axioms MemoryDelay.early_mass
#print axioms MemoryDelay.rising_mass
#print axioms MemoryDelay.falling_mass
#print axioms MemoryDelay.today_mass
#print axioms MemoryDelay.global_mass
#print axioms MemoryDelay.kernel_integrable
#print axioms MemoryDelay.kernel_causal_mass
#print axioms MemoryDelay.positiveKernel_continuous
#print axioms MemoryDelay.positiveKernel_pos
#print axioms MemoryDelay.positiveKernel_integrable
#print axioms MemoryDelay.positiveKernel_causal_mass
#print axioms MemoryDelay.positiveKernel_today_floor
#print axioms MemoryDelay.positiveKernel_early_ceiling
#print axioms MemoryDelay.normalized_positive_counterexample
#print axioms MemoryDelay.delayed_source_zero
