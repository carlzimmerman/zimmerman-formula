import Mathlib

open MeasureTheory Set Real Filter Topology

noncomputable def bpstRadial (ρ r : ℝ) : ℝ := 192 * ρ ^ 4 * r ^ 3 / (r ^ 2 + ρ ^ 2) ^ 4

noncomputable def bpstPrim (ρ r : ℝ) : ℝ :=
  96 * ρ ^ 4 * (-(1 / (2 * (r ^ 2 + ρ ^ 2) ^ 2)) + ρ ^ 2 / (3 * (r ^ 2 + ρ ^ 2) ^ 3))

theorem bpst_hasDerivAt {ρ : ℝ} (hρ : 0 < ρ) (r : ℝ) : HasDerivAt (bpstPrim ρ) (bpstRadial ρ r) r := by
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
  unfold bpstRadial
  norm_num
  field_simp
  ring

theorem bpst_prim_zero {ρ : ℝ} (hρ : 0 < ρ) : bpstPrim ρ 0 = -16 := by
  unfold bpstPrim
  have : ρ ≠ 0 := hρ.ne'
  field_simp
  ring

theorem bpst_prim_tendsto {ρ : ℝ} (_hρ : 0 < ρ) : Tendsto (bpstPrim ρ) atTop (𝓝 0) := by
  have hu : Tendsto (fun r : ℝ => r ^ 2 + ρ ^ 2) atTop atTop :=
    tendsto_atTop_add_const_right _ _ (tendsto_pow_atTop (by norm_num))
  have h2 : Tendsto (fun r : ℝ => 2 * (r ^ 2 + ρ ^ 2) ^ 2) atTop atTop :=
    ((tendsto_pow_atTop (by norm_num : (2:ℕ) ≠ 0)).comp hu).const_mul_atTop (by norm_num)
  have h3 : Tendsto (fun r : ℝ => 3 * (r ^ 2 + ρ ^ 2) ^ 3) atTop atTop :=
    ((tendsto_pow_atTop (by norm_num : (3:ℕ) ≠ 0)).comp hu).const_mul_atTop (by norm_num)
  have a2 := (tendsto_const_nhds (x := (1:ℝ))).div_atTop h2
  have a3 := (tendsto_const_nhds (x := ρ ^ 2)).div_atTop h3
  have h := ((a2.neg).add a3).const_mul (96 * ρ ^ 4)
  have e : bpstPrim ρ = fun r => 96 * ρ ^ 4 * (-(1 / (2 * (r ^ 2 + ρ ^ 2) ^ 2)) + ρ ^ 2 / (3 * (r ^ 2 + ρ ^ 2) ^ 3)) := by
    funext r; rfl
  rw [e]
  have h0 : 96 * ρ ^ 4 * (-(0:ℝ) + 0) = 0 := by ring
  rw [h0] at h
  exact h

/-- The improper radial BPST integral, for EVERY size rho > 0: int_0^inf 192 rho^4 r^3/(r^2+rho^2)^4 dr = 16. -/
theorem bpst_radial_integral {ρ : ℝ} (hρ : 0 < ρ) : ∫ r in Ioi (0:ℝ), bpstRadial ρ r = 16 := by
  have hcont : ContinuousWithinAt (bpstPrim ρ) (Ici 0) 0 :=
    (bpst_hasDerivAt hρ 0).continuousAt.continuousWithinAt
  have hnn : ∀ x ∈ Ioi (0:ℝ), 0 ≤ bpstRadial ρ x := by
    intro x hx
    have : 0 < x := hx
    unfold bpstRadial; positivity
  have := integral_Ioi_of_hasDerivAt_of_nonneg hcont (fun x _ => bpst_hasDerivAt hρ x) hnn
    (bpst_prim_tendsto hρ)
  rw [this, bpst_prim_zero hρ]; norm_num

/-- Exact finite-radius version: int_0^R = bpstPrim(R) + 16 (so the tail is O(R^-4)). -/
theorem bpst_partial_integral {ρ : ℝ} (hρ : 0 < ρ) (R : ℝ) :
    ∫ r in (0:ℝ)..R, bpstRadial ρ r = bpstPrim ρ R + 16 := by
  have hcont : Continuous (bpstRadial ρ) := by
    unfold bpstRadial
    refine Continuous.div (by fun_prop) (by fun_prop) (fun x => by positivity)
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt (fun x _ => bpst_hasDerivAt hρ x)
    (hcont.intervalIntegrable _ _), bpst_prim_zero hρ]
  ring

theorem bpst_partial_tendsto {ρ : ℝ} (hρ : 0 < ρ) :
    Tendsto (fun R : ℝ => ∫ r in (0:ℝ)..R, bpstRadial ρ r) atTop (𝓝 16) := by
  have h := (bpst_prim_tendsto hρ).add_const 16
  simp only [zero_add] at h
  refine h.congr (fun R => ?_)
  rw [bpst_partial_integral hρ R]

/-! ### sphere volumes from sine-power integrals -/

theorem int_sin : ∫ x in (0:ℝ)..π, Real.sin x = 2 := by
  rw [integral_sin]; simp; norm_num

theorem int_sin_sq : ∫ x in (0:ℝ)..π, Real.sin x ^ 2 = π / 2 := by
  rw [integral_sin_sq]; simp

theorem int_sin_cube : ∫ x in (0:ℝ)..π, Real.sin x ^ 3 = 4 / 3 := by
  show ∫ x in (0:ℝ)..π, Real.sin x ^ (2 * 1 + 1) = 4 / 3
  rw [integral_sin_pow_odd]
  norm_num [Finset.prod_range_one]

/-- Vol(S^3) as the iterated integral of the round volume element sin^2 th1 sin th2 (dth1 dth2 dphi). -/
noncomputable def volS3 : ℝ :=
  (∫ x in (0:ℝ)..π, Real.sin x ^ 2) * (∫ x in (0:ℝ)..π, Real.sin x) * (2 * π)

theorem volS3_eq : volS3 = 2 * π ^ 2 := by
  unfold volS3; rw [int_sin_sq, int_sin]; ring

/-- The instanton number of the BPST profile: (1/(32 pi^2)) * (Vol S^3) * int r^3 ... = 1, for every size rho. -/
theorem bpst_instanton_number {ρ : ℝ} (hρ : 0 < ρ) :
    (1 / (32 * π ^ 2)) * (volS3 * ∫ r in Ioi (0:ℝ), bpstRadial ρ r) = 1 := by
  rw [bpst_radial_integral hρ, volS3_eq]
  have : π ≠ 0 := Real.pi_pos.ne'
  field_simp; ring

theorem bpst_total_action {ρ : ℝ} (hρ : 0 < ρ) :
    volS3 * ∫ r in Ioi (0:ℝ), bpstRadial ρ r = 32 * π ^ 2 := by
  rw [bpst_radial_integral hρ, volS3_eq]; ring

/-- size independence: two different sizes give the same total. -/
theorem bpst_size_independent {ρ₁ ρ₂ : ℝ} (h₁ : 0 < ρ₁) (h₂ : 0 < ρ₂) :
    (∫ r in Ioi (0:ℝ), bpstRadial ρ₁ r) = ∫ r in Ioi (0:ℝ), bpstRadial ρ₂ r := by
  rw [bpst_radial_integral h₁, bpst_radial_integral h₂]

#print axioms bpst_hasDerivAt
#print axioms bpst_radial_integral
#print axioms bpst_partial_integral
#print axioms bpst_partial_tendsto
#print axioms volS3_eq
#print axioms bpst_instanton_number
#print axioms bpst_total_action
#print axioms bpst_size_independent
