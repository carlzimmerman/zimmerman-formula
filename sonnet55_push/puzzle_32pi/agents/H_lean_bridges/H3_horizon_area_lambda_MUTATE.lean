import Mathlib
import H2_s4_euler
import H3_horizon_area_lambda

/-! MUTATE controls for H3_horizon_area_lambda.lean: each `M3*` is a FALSE variant with the true proof script (must FAIL);
each `M3*_refuted` proves the negation of the false claim from the true theorem (must COMPILE). -/

open MeasureTheory Set Real

-- M3a: horizon area with r_s = 1/a0 (wrong: the Schwarzschild r_s is 1/(2 a0))
theorem M3a_horizon_area_wrong {a0 : ℝ} (ha : 0 < a0) : 4 * π * (1 / a0) ^ 2 = π / a0 ^ 2 := by
  have : a0 ≠ 0 := ha.ne'
  field_simp
  norm_num

theorem M3a_refuted : ¬ (4 * π * (1 / (1:ℝ)) ^ 2 = π / (1:ℝ) ^ 2) := by
  have := Real.pi_pos
  norm_num

-- M3b: A Lambda = 16 pi^2 (half the constant) <-> Lambda = 32 pi a0^2 -- false
theorem M3b_A_Lambda_half {a0 Λ : ℝ} (ha : 0 < a0) : (π / a0 ^ 2) * Λ = 16 * π ^ 2 ↔ Λ = 32 * π * a0 ^ 2 := by
  have hp := Real.pi_pos
  have h : a0 ^ 2 ≠ 0 := by positivity
  constructor
  · intro h1
    field_simp at h1 ⊢
    nlinarith [h1]
  · intro h1; rw [h1]; field_simp

theorem M3b_refuted : ¬ (∀ a0 Λ : ℝ, 0 < a0 → ((π / a0 ^ 2) * Λ = 16 * π ^ 2 ↔ Λ = 32 * π * a0 ^ 2)) := by
  intro h
  have hp := Real.pi_pos
  have h1 := (h 1 (32 * π) one_pos).mpr (by ring)
  norm_num at h1
  nlinarith [sq_pos_of_pos hp]

-- M3c: Z^2 = 8 pi/3 (the kappa^2 = rho_Lambda near-miss) <-> A Lambda = 32 pi^2 -- false
theorem M3c_Zsq_near_miss {a0 L : ℝ} (ha : 0 < a0) (hL : 0 < L) :
    (1 / (a0 * L)) ^ 2 = 8 * π / 3 ↔ (π / a0 ^ 2) * (3 / L ^ 2) = 32 * π ^ 2 := by
  have hp := Real.pi_pos
  have h1 : a0 ≠ 0 := ha.ne'
  have h2 : L ≠ 0 := hL.ne'
  constructor
  · intro h
    have : 1 / (a0 * L) ^ 2 = 8 * π / 3 := by rw [← h]; field_simp
    field_simp at this ⊢
    nlinarith [this]
  · intro h
    field_simp at h ⊢
    nlinarith [h]

theorem M3c_refuted : ¬ (∀ a0 L : ℝ, 0 < a0 → 0 < L →
    ((1 / (a0 * L)) ^ 2 = 8 * π / 3 ↔ (π / a0 ^ 2) * (3 / L ^ 2) = 32 * π ^ 2)) := by
  intro h
  have hp := Real.pi_pos
  -- a0 = 1, L = 1/sqrt(32 pi/3): A Lambda = 32 pi^2 holds but Z^2 = 32 pi/3 != 8 pi/3
  set L := 1 / Real.sqrt (32 * π / 3) with hLdef
  have hpos : 0 < Real.sqrt (32 * π / 3) := Real.sqrt_pos.mpr (by positivity)
  have hL : 0 < L := by positivity
  have hLsq : L ^ 2 = 3 / (32 * π) := by
    rw [hLdef, div_pow, Real.sq_sqrt (by positivity)]; field_simp
  have hAL : (π / (1:ℝ) ^ 2) * (3 / L ^ 2) = 32 * π ^ 2 := by
    rw [hLsq]; field_simp
  have := (h 1 L one_pos hL).mpr hAL
  rw [one_mul, div_pow, one_pow, hLsq] at this
  field_simp at this
  nlinarith [sq_pos_of_pos hp]

-- M3d: G rho = 2 a0^2 (wrong) <-> Lambda = 32 pi a0^2
theorem M3d_G_rho_wrong {a0 Λ : ℝ} : Λ = 32 * π * a0 ^ 2 ↔ Λ / (8 * π) = 2 * a0 ^ 2 := by
  have hp := Real.pi_pos
  have : (8 * π) ≠ 0 := by positivity
  rw [div_eq_iff this]
  constructor <;> intro h <;> linarith

theorem M3d_refuted : ¬ (∀ a0 Λ : ℝ, Λ = 32 * π * a0 ^ 2 ↔ Λ / (8 * π) = 2 * a0 ^ 2) := by
  intro h
  have hp := Real.pi_pos
  have h1 := (h 1 (32 * π)).mp (by ring)
  field_simp at h1
  nlinarith

-- M3e: A_a0 = 8 Vol(S^4)/L^2 (wrong factor 8) <-> Z^2 = 32 pi/3
theorem M3e_A_eq_wrong {a0 L : ℝ} (ha : 0 < a0) (hL : 0 < L) :
    π / a0 ^ 2 = 8 * volS4 L / L ^ 2 ↔ (1 / (a0 * L)) ^ 2 = 32 * π / 3 := by
  have hp := Real.pi_pos
  have h1 : a0 ≠ 0 := ha.ne'
  have h2 : L ≠ 0 := hL.ne'
  rw [volS4_eq]
  constructor
  · intro h
    have : 1 / (a0 * L) ^ 2 = 32 * π / 3 := by
      field_simp at h ⊢
      nlinarith [h]
    rw [← this]; field_simp
  · intro h
    have : 1 / (a0 * L) ^ 2 = 32 * π / 3 := by rw [← h]; field_simp
    field_simp at this ⊢
    nlinarith [this]

theorem M3e_refuted : ¬ (∀ a0 L : ℝ, 0 < a0 → 0 < L →
    (π / a0 ^ 2 = 8 * volS4 L / L ^ 2 ↔ (1 / (a0 * L)) ^ 2 = 32 * π / 3)) := by
  intro h
  have hp := Real.pi_pos
  set L := 1 / Real.sqrt (32 * π / 3) with hLdef
  have hpos : 0 < Real.sqrt (32 * π / 3) := Real.sqrt_pos.mpr (by positivity)
  have hL : 0 < L := by positivity
  have hLsq : L ^ 2 = 3 / (32 * π) := by
    rw [hLdef, div_pow, Real.sq_sqrt (by positivity)]; field_simp
  have hZ : (1 / ((1:ℝ) * L)) ^ 2 = 32 * π / 3 := by
    rw [one_mul, div_pow, one_pow, hLsq]; field_simp
  have h1 := (h 1 L one_pos hL).mpr hZ
  have h2 := (A_eq_4Vol_iff (a0 := 1) (L := L) one_pos hL).mpr hZ
  have h3 : 8 * volS4 L / L ^ 2 = 4 * volS4 L / L ^ 2 := h1.symm.trans h2
  have hv : 0 < volS4 L := by rw [volS4_eq]; positivity
  have hL0 : L ^ 2 ≠ 0 := by positivity
  field_simp at h3
  linarith

#print axioms M3a_refuted
#print axioms M3b_refuted
#print axioms M3c_refuted
#print axioms M3d_refuted
#print axioms M3e_refuted
#print axioms M3a_horizon_area_wrong
#print axioms M3b_A_Lambda_half
#print axioms M3c_Zsq_near_miss
#print axioms M3d_G_rho_wrong
#print axioms M3e_A_eq_wrong
