import Mathlib
import H1_bpst

/-!
MUTATE controls for H1_bpst.lean.  Every theorem named `M1*` states a FALSE variant and re-uses the true proof script:
each MUST fail to compile (one error each).  Every `M1*_refuted` proves the negation of the false variant from the
true theorem: each MUST compile.  (No `sorry` is used anywhere here: a failed theorem is reported by Lean as an error.)
-/

open MeasureTheory Set Real Filter Topology

-- M1a: the BPST radial integral is 16, not 8
theorem M1a_bpst_integral_is_8 {ρ : ℝ} (hρ : 0 < ρ) : ∫ r in Ioi (0:ℝ), bpstRadial ρ r = 8 := by
  have hcont : ContinuousWithinAt (bpstPrim ρ) (Ici 0) 0 :=
    (bpst_hasDerivAt hρ 0).continuousAt.continuousWithinAt
  have hnn : ∀ x ∈ Ioi (0:ℝ), 0 ≤ bpstRadial ρ x := by
    intro x hx
    have : 0 < x := hx
    unfold bpstRadial; positivity
  have := integral_Ioi_of_hasDerivAt_of_nonneg hcont (fun x _ => bpst_hasDerivAt hρ x) hnn
    (bpst_prim_tendsto hρ)
  rw [this, bpst_prim_zero hρ]; norm_num

theorem M1a_refuted {ρ : ℝ} (hρ : 0 < ρ) : ¬ (∫ r in Ioi (0:ℝ), bpstRadial ρ r = 8) := by
  intro h; rw [bpst_radial_integral hρ] at h; norm_num at h

-- M1b: Vol(S^3) = 2 pi^2, not pi^2
theorem M1b_volS3_is_pi_sq : volS3 = π ^ 2 := by
  unfold volS3; rw [int_sin_sq, int_sin]; ring

theorem M1b_refuted : ¬ (volS3 = π ^ 2) := by
  intro h; rw [volS3_eq] at h
  have := Real.pi_pos
  nlinarith [sq_pos_of_pos this]

-- M1c: instanton number 1, not 2
theorem M1c_instanton_number_two {ρ : ℝ} (hρ : 0 < ρ) :
    (1 / (32 * π ^ 2)) * (volS3 * ∫ r in Ioi (0:ℝ), bpstRadial ρ r) = 2 := by
  rw [bpst_radial_integral hρ, volS3_eq]
  have : π ≠ 0 := Real.pi_pos.ne'
  field_simp; ring

theorem M1c_refuted {ρ : ℝ} (hρ : 0 < ρ) :
    ¬ ((1 / (32 * π ^ 2)) * (volS3 * ∫ r in Ioi (0:ℝ), bpstRadial ρ r) = 2) := by
  intro h; rw [bpst_instanton_number hρ] at h; norm_num at h

-- M1d: the size dependence 16 * rho would break scale-freeness
theorem M1d_size_dependent {ρ : ℝ} (hρ : 0 < ρ) : ∫ r in Ioi (0:ℝ), bpstRadial ρ r = 16 * ρ := by
  rw [bpst_radial_integral hρ]

theorem M1d_refuted : ¬ (∀ ρ : ℝ, 0 < ρ → ∫ r in Ioi (0:ℝ), bpstRadial ρ r = 16 * ρ) := by
  intro h
  have h2 := h 2 (by norm_num)
  rw [bpst_radial_integral (by norm_num)] at h2
  norm_num at h2

-- M1e: the primitive differentiates to 192, not 190 (the constant is sharp)
noncomputable def bpstRadialWrong (ρ r : ℝ) : ℝ := 190 * ρ ^ 4 * r ^ 3 / (r ^ 2 + ρ ^ 2) ^ 4

theorem M1e_hasDerivAt_wrong {ρ : ℝ} (hρ : 0 < ρ) (r : ℝ) : HasDerivAt (bpstPrim ρ) (bpstRadialWrong ρ r) r := by
  have hu0 : r ^ 2 + ρ ^ 2 ≠ 0 := by positivity
  have h1 : HasDerivAt (fun r : ℝ => r ^ 2 + ρ ^ 2) (2 * r) r := by
    simpa using ((hasDerivAt_pow 2 r).add_const (ρ ^ 2))
  have h2 := h1.fun_pow 2
  have h3 := h1.fun_pow 3
  have h4 := (hasDerivAt_const r (1:ℝ)).fun_div (h2.const_mul 2) (by positivity)
  have h5 := (hasDerivAt_const r (ρ ^ 2)).fun_div (h3.const_mul 3) (by positivity)
  have h7 := ((h4.fun_neg).fun_add h5).const_mul (96 * ρ ^ 4)
  unfold bpstPrim
  refine h7.congr_deriv ?_
  unfold bpstRadialWrong
  norm_num
  field_simp
  ring

-- the true derivative is unique, so the wrong one is refuted: at r = 1, rho = 1 the values differ
theorem M1e_refuted : bpstRadialWrong 1 1 ≠ bpstRadial 1 1 := by
  unfold bpstRadialWrong bpstRadial; norm_num

#print axioms M1a_refuted
#print axioms M1b_refuted
#print axioms M1c_refuted
#print axioms M1d_refuted
#print axioms M1e_refuted
#print axioms M1a_bpst_integral_is_8
#print axioms M1b_volS3_is_pi_sq
#print axioms M1c_instanton_number_two
#print axioms M1d_size_dependent
#print axioms M1e_hasDerivAt_wrong
