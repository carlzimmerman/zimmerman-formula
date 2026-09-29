import Mathlib
import H5_freefall

/-! MUTATE controls for H5_freefall.lean: each `M5*` is a FALSE variant with the true proof script (must FAIL);
each `M5*_refuted` proves its negation from the true theorem (must COMPILE). -/

open MeasureTheory Set Real Filter Topology

-- M5a: int_0^1 sqrt(x/(1-x)) dx = pi/4 (wrong; it is pi/2)
theorem M5a_int_wrong : ∫ x in (0:ℝ)..1, Real.sqrt (x / (1 - x)) = π / 4 := by
  have hint : IntervalIntegrable (fun x : ℝ => Real.sqrt (x / (1 - x))) volume 0 1 := by
    refine intervalIntegral.intervalIntegrable_deriv_of_nonneg (g := ffPrim)
      ffPrim_continuous.continuousOn ?_ ?_
    · intro x hx
      simp only [min_eq_left zero_le_one, max_eq_right zero_le_one] at hx
      exact ffPrim_hasDerivAt hx.1 hx.2
    · intro x _; exact Real.sqrt_nonneg _
  have := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le (zero_le_one' ℝ)
    ffPrim_continuous.continuousOn (fun x hx => ffPrim_hasDerivAt hx.1 hx.2) hint
  rw [this, ffPrim_one, ffPrim_zero]; ring

theorem M5a_refuted : ¬ (∫ x in (0:ℝ)..1, Real.sqrt (x / (1 - x)) = π / 4) := by
  intro h; rw [int_sqrt_ratio] at h
  have := Real.pi_pos
  linarith

-- M5b: t_ff^2 = 3 pi/(16 G rho) (wrong; it is 3 pi/(32 G rho))
theorem M5b_tff_sq_wrong {G ρ r0 : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hr : 0 < r0) :
    tff G ((4 * π / 3) * ρ * r0 ^ 3) r0 ^ 2 = 3 * π / (16 * G * ρ) := by
  have hp := Real.pi_pos
  rw [tff_uniform hG hρ hr, Real.sq_sqrt (by positivity)]
  field_simp
  ring

theorem M5b_refuted {G ρ r0 : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hr : 0 < r0) :
    ¬ (tff G ((4 * π / 3) * ρ * r0 ^ 3) r0 ^ 2 = 3 * π / (16 * G * ρ)) := by
  intro h
  rw [tff_sq_uniform hG hρ hr] at h
  have hp := Real.pi_pos
  field_simp at h
  nlinarith [mul_pos (mul_pos hG hρ) hp]

-- M5c: t_ff = (pi/2) sqrt(r0^3/(GM)) (dropped the 2) -- wrong
theorem M5c_tff_wrong {G M r0 : ℝ} (hG : 0 < G) (hM : 0 < M) (hr : 0 < r0) :
    tff G M r0 = (π / 2) * Real.sqrt (r0 ^ 3 / (G * M)) := by
  have hk : 0 < 2 * G * M := by positivity
  set g : ℝ → ℝ := fun r => 1 / Real.sqrt (2 * G * M * (1 / r - 1 / r0)) with hg
  have h := intervalIntegral.integral_comp_mul_left (a := (0:ℝ)) (b := 1) g hr.ne'
  simp only [mul_zero, mul_one, smul_eq_mul] at h
  have hcongr : ∫ x in (0:ℝ)..1, g (r0 * x) = ∫ x in (0:ℝ)..1, Real.sqrt (r0 / (2 * G * M)) * Real.sqrt (x / (1 - x)) := by
    refine intervalIntegral.integral_congr (fun x hx => ?_)
    exact tff_integrand hG hM hr hx
  rw [hcongr, intervalIntegral.integral_const_mul, int_sqrt_ratio] at h
  have h2 : ∫ x in (0:ℝ)..r0, g x = r0 * (Real.sqrt (r0 / (2 * G * M)) * (π / 2)) := by
    have := h
    field_simp at this ⊢
    linarith
  unfold tff
  show ∫ r in (0:ℝ)..r0, g r = _
  rw [h2]
  have h3 : Real.sqrt (r0 ^ 3 / (G * M)) = r0 * Real.sqrt (r0 / (2 * G * M)) := by
    rw [show r0 ^ 3 / (G * M) = r0 ^ 2 * (r0 / (2 * G * M)) by ring, Real.sqrt_mul (by positivity),
      Real.sqrt_sq hr.le]
  rw [h3]; ring

theorem M5c_refuted : ¬ (∀ G M r0 : ℝ, 0 < G → 0 < M → 0 < r0 → tff G M r0 = (π / 2) * Real.sqrt (r0 ^ 3 / (G * M))) := by
  intro h
  have h1 := h 1 1 1 one_pos one_pos one_pos
  rw [tff_eq one_pos one_pos one_pos] at h1
  have hp := Real.pi_pos
  have h2 : Real.sqrt (1 ^ 3 / (2 * 1 * 1)) = Real.sqrt (1 ^ 3 / (1 * 1)) := by
    have := mul_left_cancel₀ (by positivity : π / 2 ≠ 0) h1
    exact this
  have h3 := Real.sqrt_inj (by norm_num) (by norm_num) |>.mp h2
  norm_num at h3

-- M5d: the cycloid does NOT solve the energy equation with 4GM instead of 2GM
theorem M5d_cycloid_wrong {G M r0 A η : ℝ} (hG : 0 < G) (hM : 0 < M) (hr : 0 < r0)
    (hA : A ^ 2 = r0 ^ 3 / (8 * G * M)) (hη : Real.cos η ≠ -1) :
    ((-(r0 / 2) * Real.sin η) / (A * (1 + Real.cos η))) ^ 2
      = 4 * G * M * (1 / ((r0 / 2) * (1 + Real.cos η)) - 1 / r0) := by
  have hc : 1 + Real.cos η ≠ 0 := fun h => hη (by linarith)
  have hs : Real.sin η ^ 2 = (1 - Real.cos η) * (1 + Real.cos η) := by
    nlinarith [Real.sin_sq_add_cos_sq η]
  have hAne : A ≠ 0 := by
    intro h; rw [h] at hA
    have : 0 < r0 ^ 3 / (8 * G * M) := by positivity
    nlinarith
  have hGM : G * M ≠ 0 := by positivity
  have h1 : (A * (1 + Real.cos η)) ^ 2 = r0 ^ 3 / (8 * G * M) * (1 + Real.cos η) ^ 2 := by rw [mul_pow, hA]
  have h2 : (-(r0 / 2) * Real.sin η) ^ 2 = (r0 / 2) ^ 2 * ((1 - Real.cos η) * (1 + Real.cos η)) := by
    rw [← hs]; ring
  rw [div_pow, h1, h2]
  field_simp
  ring

theorem M5d_refuted {G M r0 A η : ℝ} (hG : 0 < G) (hM : 0 < M) (hr : 0 < r0)
    (hA : A ^ 2 = r0 ^ 3 / (8 * G * M)) (hη : Real.cos η ≠ -1) (hc : Real.cos η ≠ 1) :
    ¬ (((-(r0 / 2) * Real.sin η) / (A * (1 + Real.cos η))) ^ 2
      = 4 * G * M * (1 / ((r0 / 2) * (1 + Real.cos η)) - 1 / r0)) := by
  intro h
  rw [cycloid_energy hG hM hr hA hη] at h
  have h1c : 1 + Real.cos η ≠ 0 := fun h => hη (by linarith)
  have hc0 : 1 - Real.cos η ≠ 0 := fun h => hc (by linarith)
  have hGM : 0 < G * M := by positivity
  have : 2 * G * M * (1 / ((r0 / 2) * (1 + Real.cos η)) - 1 / r0) =
      (2 * G * M / r0) * ((1 - Real.cos η) / (1 + Real.cos η)) := by
    field_simp; ring
  rw [this] at h
  have h2 : 4 * G * M * (1 / ((r0 / 2) * (1 + Real.cos η)) - 1 / r0) =
      2 * ((2 * G * M / r0) * ((1 - Real.cos η) / (1 + Real.cos η))) := by
    field_simp; ring
  rw [h2] at h
  have hpos : (2 * G * M / r0) * ((1 - Real.cos η) / (1 + Real.cos η)) ≠ 0 := by
    have hcos := Real.cos_le_one η
    have hcos2 := Real.neg_one_le_cos η
    have hlt : Real.cos η < 1 := lt_of_le_of_ne hcos hc
    have hgt : -1 < Real.cos η := lt_of_le_of_ne hcos2 (Ne.symm hη)
    positivity
  apply hpos
  linarith

#print axioms M5a_refuted
#print axioms M5b_refuted
#print axioms M5c_refuted
#print axioms M5d_refuted
#print axioms M5a_int_wrong
#print axioms M5b_tff_sq_wrong
#print axioms M5c_tff_wrong
#print axioms M5d_cycloid_wrong
