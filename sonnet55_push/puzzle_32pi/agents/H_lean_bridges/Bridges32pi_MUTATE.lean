import Mathlib
import H2_s4_euler
import H3_horizon_area_lambda
import H7_p09_reduction
import Bridges32pi

/-! MUTATE controls for Bridges32pi.lean: each `M8*` is a FALSE variant with the true proof script (must FAIL);
each `M8*_refuted` proves its negation (must COMPILE). -/

open Real

-- M8a: the web with statement 1 replaced by Z^2 = 8 pi/3 (the kappa^2 = rho_Lambda near-miss)
theorem M8a_web_near_miss {a0 L : ℝ} (ha : 0 < a0) (hL : 0 < L) :
    List.TFAE [
      (1 / (a0 * L)) ^ 2 = 8 * π / 3,
      (π / a0 ^ 2) * (3 / L ^ 2) = 32 * π ^ 2,
      3 / L ^ 2 = 32 * π * a0 ^ 2 ] := by
  tfae_have 1 ↔ 2 := Zsq_iff_A_Lambda ha hL
  tfae_have 2 ↔ 3 := A_Lambda_iff ha
  tfae_finish

theorem M8a_refuted : ¬ (∀ a0 L : ℝ, 0 < a0 → 0 < L → List.TFAE [
      (1 / (a0 * L)) ^ 2 = 8 * π / 3,
      (π / a0 ^ 2) * (3 / L ^ 2) = 32 * π ^ 2]) := by
  intro h
  have hp := Real.pi_pos
  -- a0 = 1, L = 1/sqrt(32 pi/3): statement 2 is true, statement 1 is false
  set L := 1 / Real.sqrt (32 * π / 3) with hLdef
  have hpos : 0 < Real.sqrt (32 * π / 3) := Real.sqrt_pos.mpr (by positivity)
  have hL : 0 < L := by positivity
  have hLsq : L ^ 2 = 3 / (32 * π) := by
    rw [hLdef, div_pow, Real.sq_sqrt (by positivity)]; field_simp
  have hAL : (π / (1:ℝ) ^ 2) * (3 / L ^ 2) = 32 * π ^ 2 := by
    rw [hLsq]; field_simp
  have h1 := ((h 1 L one_pos hL).out 1 2).mpr hAL
  rw [one_mul, div_pow, one_pow, hLsq] at h1
  field_simp at h1
  nlinarith [sq_pos_of_pos hp]

-- M8b: the constants bridge with 16 pi^2 in the third slot
theorem M8b_constant_wrong :
    ∀ a0 L : ℝ, 0 < a0 → 0 < L → (1 / (a0 * L)) ^ 2 = 32 * π / 3 → (π / a0 ^ 2) * (3 / L ^ 2) = 16 * π ^ 2 := by
  intro a0 L ha hL h
  exact (Zsq_iff_A_Lambda ha hL).mp h

theorem M8b_refuted : ¬ (∀ a0 L : ℝ, 0 < a0 → 0 < L → (1 / (a0 * L)) ^ 2 = 32 * π / 3 → (π / a0 ^ 2) * (3 / L ^ 2) = 16 * π ^ 2) := by
  intro h
  have hp := Real.pi_pos
  set L := 1 / Real.sqrt (32 * π / 3) with hLdef
  have hpos : 0 < Real.sqrt (32 * π / 3) := Real.sqrt_pos.mpr (by positivity)
  have hL : 0 < L := by positivity
  have hLsq : L ^ 2 = 3 / (32 * π) := by
    rw [hLdef, div_pow, Real.sq_sqrt (by positivity)]; field_simp
  have hZ : (1 / ((1:ℝ) * L)) ^ 2 = 32 * π / 3 := by
    rw [one_mul, div_pow, one_pow, hLsq]; field_simp
  have h1 := h 1 L one_pos hL hZ
  have h2 := (Zsq_iff_A_Lambda one_pos hL).mp hZ
  rw [h1] at h2
  nlinarith [sq_pos_of_pos hp]

-- M8c: the free-fall relation with (3 pi/16) r_s^2 (wrong; it is 3 pi/32)
theorem M8c_tff_rs_wrong {G ρ r0 a0 : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hr : 0 < r0) (ha : 0 < a0)
    (h : G * ρ = 4 * a0 ^ 2) :
    tff G ((4 * π / 3) * ρ * r0 ^ 3) r0 ^ 2 = (3 * π / 16) * (1 / (2 * a0)) ^ 2 := by
  have hp := Real.pi_pos
  rw [tff_sq_uniform hG hρ hr]
  have : 32 * G * ρ = 128 * a0 ^ 2 := by nlinarith [h]
  rw [this]
  have : a0 ≠ 0 := ha.ne'
  field_simp; ring

theorem M8c_refuted {G ρ r0 a0 : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hr : 0 < r0) (ha : 0 < a0)
    (h : G * ρ = 4 * a0 ^ 2) :
    ¬ (tff G ((4 * π / 3) * ρ * r0 ^ 3) r0 ^ 2 = (3 * π / 16) * (1 / (2 * a0)) ^ 2) := by
  intro h2
  rw [tff_sq_over_rs_sq hG hρ hr ha h] at h2
  have hp := Real.pi_pos
  have ha0 : a0 ≠ 0 := ha.ne'
  field_simp at h2
  nlinarith [mul_pos hp (pow_pos ha 2)]

#print axioms M8a_refuted
#print axioms M8b_refuted
#print axioms M8c_refuted
#print axioms M8a_web_near_miss
#print axioms M8b_constant_wrong
#print axioms M8c_tff_rs_wrong
