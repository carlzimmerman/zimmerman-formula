import Mathlib
import P6_dimension

/-! MUTATE controls for P6_dimension.lean: each `M6*` is a FALSE variant re-using the true proof script with one wrong constant
(must FAIL to compile); each `M6*_refuted` proves the negation from the true theorems plus an explicit instance (must COMPILE). -/

open Real Dimension

-- M6a: the acceleration coefficient at d = 3 is (rho + 3p)/3 (wrong; true: /6) -- false
theorem M6a_acc_wrong (ρ p : ℝ) : accCoeff 3 ρ p = (ρ + 3 * p) / 3 := by
  unfold accCoeff; ring

theorem M6a_refuted : ¬ (∀ ρ p : ℝ, accCoeff 3 ρ p = (ρ + 3 * p) / 3) := by
  intro h
  have h1 := h 1 0
  rw [acc_coeff_d3] at h1
  norm_num at h1

-- M6b: (d-2) rho + d p = rho + d p iff d = 4 (wrong; true: d = 3) -- false
theorem M6b_tolman_wrong {d ρ p : ℝ} (hρ : ρ ≠ 0) : (d - 2) * ρ + d * p = ρ + d * p ↔ d = 4 := by
  constructor
  · intro h
    have : (d - 3) * ρ = 0 := by linarith
    rcases mul_eq_zero.mp this with h1 | h1
    · linarith
    · exact absurd h1 hρ
  · intro h; rw [h]; ring

theorem M6b_refuted : ¬ (∀ d ρ p : ℝ, ρ ≠ 0 → ((d - 2) * ρ + d * p = ρ + d * p ↔ d = 4)) := by
  intro h
  have h1 := (tolman_naive_ne (d := 3) (ρ := 1) (p := 0) one_ne_zero).mpr rfl
  have h2 := (h 3 1 0 one_ne_zero).mp h1
  norm_num at h2

-- M6c: Z_V(d) = 6 iff d = 3 (wrong: d = 4 also gives 6) -- false
theorem M6c_ZV_wrong {d : ℝ} (hd : d ≠ 2) : d * (d - 1) / (d - 2) = 6 ↔ d = 3 := by
  have hd2 : d - 2 ≠ 0 := sub_ne_zero.mpr hd
  rw [div_eq_iff hd2]
  constructor
  · intro h
    have : (d - 3) * (d - 4) = 0 := by nlinarith [h]
    rcases mul_eq_zero.mp this with h1 | h1
    · linarith
    · linarith
  · intro h; rw [h]; norm_num

theorem M6c_refuted : ¬ (∀ d : ℝ, d ≠ 2 → (d * (d - 1) / (d - 2) = 6 ↔ d = 3)) := by
  intro h
  have h1 : (4 : ℝ) * (4 - 1) / (4 - 2) = 6 := by norm_num
  have h2 := (h 4 (by norm_num)).mp h1
  norm_num at h2

-- M6d: (4 pi)^2 2! = 16 pi^2 (wrong: 32 pi^2) -- false
theorem M6d_euler_wrong : (4 * π) ^ 2 * (Nat.factorial 2 : ℝ) = 16 * π ^ 2 := by
  simp [Nat.factorial]; ring

theorem M6d_refuted : ¬ ((4 * π) ^ 2 * (Nat.factorial 2 : ℝ) = 16 * π ^ 2) := by
  have hp := Real.pi_pos
  intro h
  rw [(euler_units).2.1] at h
  nlinarith [sq_pos_of_pos hp]

-- M6e: Z_f^2 at d = 3 is 16 pi/3 (wrong: 8 pi/3) -- false
theorem M6e_Zf_wrong : 16 * π / (3 * (3 - 1)) = 16 * π / 3 := by ring

theorem M6e_refuted : ¬ (16 * π / (3 * (3 - 1)) = 16 * π / 3) := by
  have hp := Real.pi_pos
  intro h; nlinarith

-- M6f: Z_d^2 dim SO(d) kappa^2 = 4 pi (wrong: 8 pi) -- false
theorem M6f_identity_wrong {d κ : ℝ} (hd : d * (d - 1) ≠ 0) (hκ : κ ≠ 0) :
    (16 * π / (d * (d - 1)) / κ ^ 2) * (d * (d - 1) / 2) * κ ^ 2 = 4 * π := by
  have hd1 : d ≠ 0 := left_ne_zero_of_mul hd
  have hd2 : d - 1 ≠ 0 := right_ne_zero_of_mul hd
  field_simp
  norm_num

theorem M6f_refuted : ¬ (∀ d κ : ℝ, d * (d - 1) ≠ 0 → κ ≠ 0 →
    (16 * π / (d * (d - 1)) / κ ^ 2) * (d * (d - 1) / 2) * κ ^ 2 = 4 * π) := by
  intro h
  have hp := Real.pi_pos
  have h1 := h 3 1 (by norm_num) one_ne_zero
  have h2 := Z_d_sq (d := 3) (κ := 1) (by norm_num) one_ne_zero
  rw [h1] at h2
  nlinarith

-- M6g: Tangherlini kappa = (d - 1)/2 (wrong: (d - 2)/2) -- false
theorem M6g_tangherlini_wrong {d G ρ : ℝ} (hG : 0 < G) (hρ : 0 < ρ) :
    (d - 2) / (2 * (1 / Real.sqrt (G * ρ))) = ((d - 1) / 2) * Real.sqrt (G * ρ) := by
  have hs : 0 < Real.sqrt (G * ρ) := Real.sqrt_pos.mpr (by positivity)
  field_simp

theorem M6g_refuted : ¬ (∀ d G ρ : ℝ, 0 < G → 0 < ρ →
    (d - 2) / (2 * (1 / Real.sqrt (G * ρ))) = ((d - 1) / 2) * Real.sqrt (G * ρ)) := by
  intro h
  have hs : 0 < Real.sqrt ((1:ℝ) * 1) := Real.sqrt_pos.mpr (by norm_num)
  have h1 := h 3 1 1 one_pos one_pos
  have h2 := kappa_tangherlini (d := 3) (G := 1) (ρ := 1) one_pos one_pos
  rw [h1] at h2
  have : Real.sqrt ((1:ℝ) * 1) = 1 := by simp
  rw [this] at h2
  norm_num at h2

-- M6h: fixed-Z kappa_d^2 = 3/(d(d-1)) (wrong: 3/(2 d (d-1))) -- false
theorem M6h_fixedZ_wrong {d : ℝ} (hd : d * (d - 1) ≠ 0) :
    (16 * π / (d * (d - 1))) / (32 * π / 3) = 3 / (d * (d - 1)) := by
  have hp := Real.pi_pos
  have hd1 : d ≠ 0 := left_ne_zero_of_mul hd
  have hd2 : d - 1 ≠ 0 := right_ne_zero_of_mul hd
  field_simp
  ring

theorem M6h_refuted : ¬ (∀ d : ℝ, d * (d - 1) ≠ 0 → (16 * π / (d * (d - 1))) / (32 * π / 3) = 3 / (d * (d - 1))) := by
  intro h
  have h1 := h 3 (by norm_num)
  have h2 := kappa_fixedZ_sq (d := 3) (by norm_num)
  rw [h1] at h2
  norm_num at h2

-- M6i: Euler/Chern = n^2 (wrong: 2^n) -- false
theorem M6i_ratio_wrong (n : ℕ) : (4 * π) ^ n * (Nat.factorial n : ℝ) / ((2 * π) ^ n * (Nat.factorial n : ℝ)) = (n : ℝ) ^ 2 := by
  have hp := Real.pi_pos
  have hf : (Nat.factorial n : ℝ) ≠ 0 := by positivity
  rw [show (4 * π) ^ n = 2 ^ n * (2 * π) ^ n by rw [← mul_pow]; ring_nf]
  field_simp

theorem M6i_refuted : ¬ (∀ n : ℕ, (4 * π) ^ n * (Nat.factorial n : ℝ) / ((2 * π) ^ n * (Nat.factorial n : ℝ)) = (n : ℝ) ^ 2) := by
  intro h
  have h1 := h 3
  rw [euler_over_chern] at h1
  norm_num at h1

#print axioms M6a_refuted
#print axioms M6b_refuted
#print axioms M6c_refuted
#print axioms M6d_refuted
#print axioms M6e_refuted
#print axioms M6f_refuted
#print axioms M6g_refuted
#print axioms M6h_refuted
#print axioms M6i_refuted
#print axioms M6a_acc_wrong
#print axioms M6b_tolman_wrong
#print axioms M6c_ZV_wrong
#print axioms M6d_euler_wrong
#print axioms M6e_Zf_wrong
#print axioms M6f_identity_wrong
#print axioms M6g_tangherlini_wrong
#print axioms M6h_fixedZ_wrong
#print axioms M6i_ratio_wrong
