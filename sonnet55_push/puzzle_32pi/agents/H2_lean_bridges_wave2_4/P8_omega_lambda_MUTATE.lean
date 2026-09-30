import Mathlib
import P8_omega_lambda

/-! MUTATE controls for P8_omega_lambda.lean: each `M8*` is a FALSE variant re-using the true proof script with one wrong constant
(must FAIL to compile); each `M8*_refuted` proves the negation from the true theorems plus an explicit instance (must COMPILE). -/

open Real OmegaLambda

-- M8a: Omega = 8 pi a0^2/(3 H0^2 c^2) <=> Lambda c^4 = 32 pi a0^2 (wrong constant) -- false
theorem M8a_omega_wrong {c H0 Ω a0 Λ : ℝ} (hc : 0 < c) (hH : 0 < H0) (hΛ : Λ = 3 * H0 ^ 2 * Ω / c ^ 2) :
    Λ = 32 * π * a0 ^ 2 / c ^ 4 ↔ Ω = 8 * π * a0 ^ 2 / (3 * H0 ^ 2 * c ^ 2) := by
  have hc0 : c ≠ 0 := hc.ne'
  have hH0 : H0 ≠ 0 := hH.ne'
  rw [hΛ]
  constructor
  · intro h
    field_simp at h ⊢
    nlinarith [h]
  · intro h
    rw [h]; field_simp

theorem M8a_refuted : ¬ (∀ c H0 Ω a0 Λ : ℝ, 0 < c → 0 < H0 → Λ = 3 * H0 ^ 2 * Ω / c ^ 2 →
    (Λ = 32 * π * a0 ^ 2 / c ^ 4 ↔ Ω = 8 * π * a0 ^ 2 / (3 * H0 ^ 2 * c ^ 2))) := by
  intro h
  have hp := Real.pi_pos
  have h1 := (omega_iff (c := 1) (H0 := 1) (Ω := 32 * π / 3) (a0 := 1) (Λ := 3 * 1 ^ 2 * (32 * π / 3) / 1 ^ 2) one_pos one_pos rfl).mpr
    (by norm_num)
  have h2 := (h 1 1 (32 * π / 3) 1 (3 * 1 ^ 2 * (32 * π / 3) / 1 ^ 2) one_pos one_pos rfl).mp h1
  nlinarith

-- M8b: the Z-form: Omega = 32 pi a0^2/(3 H0^2 c^2) <=> Z^2 = 8 pi/3 (wrong; true: 32 pi/3) -- false
theorem M8b_Z_wrong {c H0 Ω a0 Z : ℝ} (hc : 0 < c) (hH : 0 < H0) (hΩ : 0 < Ω) (hZ : 0 < Z)
    (ha : a0 = c * H0 * Real.sqrt Ω / Z) :
    Ω = 32 * π * a0 ^ 2 / (3 * H0 ^ 2 * c ^ 2) ↔ Z ^ 2 = 8 * π / 3 := by
  have hp := Real.pi_pos
  have hc0 : c ≠ 0 := hc.ne'
  have hH0 : H0 ≠ 0 := hH.ne'
  have hZ0 : Z ≠ 0 := hZ.ne'
  have hs := Real.sq_sqrt hΩ.le
  have hsq : a0 ^ 2 = c ^ 2 * H0 ^ 2 * Ω / Z ^ 2 := by
    rw [ha, div_pow, mul_pow, mul_pow, hs]
  rw [hsq]
  have : 32 * π * (c ^ 2 * H0 ^ 2 * Ω / Z ^ 2) / (3 * H0 ^ 2 * c ^ 2) = 32 * π * Ω / (3 * Z ^ 2) := by
    field_simp
  rw [this]
  have hZ2 : 0 < Z ^ 2 := by positivity
  rw [eq_div_iff (by positivity)]
  constructor
  · intro h
    have : Ω * (3 * Z ^ 2 - 8 * π) = 0 := by nlinarith [h]
    rcases mul_eq_zero.mp this with h1 | h1
    · exact absurd h1 hΩ.ne'
    · linarith
  · intro h
    nlinarith [h]

theorem M8b_refuted : ¬ (∀ c H0 Ω a0 Z : ℝ, 0 < c → 0 < H0 → 0 < Ω → 0 < Z → a0 = c * H0 * Real.sqrt Ω / Z →
    (Ω = 32 * π * a0 ^ 2 / (3 * H0 ^ 2 * c ^ 2) ↔ Z ^ 2 = 8 * π / 3)) := by
  intro h
  have hp := Real.pi_pos
  have hZp : 0 < Real.sqrt (32 * π / 3) := Real.sqrt_pos.mpr (by positivity)
  have hZ2 : Real.sqrt (32 * π / 3) ^ 2 = 32 * π / 3 := Real.sq_sqrt (by positivity)
  have h1 := (omega_Z (c := 1) (H0 := 1) (Ω := 1) (a0 := 1 * 1 * Real.sqrt 1 / Real.sqrt (32 * π / 3)) (Z := Real.sqrt (32 * π / 3))
    one_pos one_pos one_pos hZp rfl).mpr hZ2
  have h2 := (h 1 1 1 _ _ one_pos one_pos one_pos hZp rfl).mp h1
  rw [hZ2] at h2
  nlinarith

-- M8c: Omega_pred > 0.99 for the record's a0 and H0 = 67.4 -- false
theorem M8c_pred_wrong {a0 H0 c : ℝ} (ha : a0 = 1.0766e-10) (hH : H0 = 2.1843e-18) (hc : c = 299792458) :
    0.99 < 32 * π * a0 ^ 2 / (3 * H0 ^ 2 * c ^ 2) := by
  have h1 := Real.pi_gt_d4
  have h2 := Real.pi_lt_d4
  subst ha hH hc
  have hd : (0:ℝ) < 3 * (2.1843e-18) ^ 2 * (299792458:ℝ) ^ 2 := by norm_num
  rw [lt_div_iff₀ hd]; nlinarith

theorem M8c_refuted : ¬ (∀ a0 H0 c : ℝ, a0 = 1.0766e-10 → H0 = 2.1843e-18 → c = 299792458 →
    0.99 < 32 * π * a0 ^ 2 / (3 * H0 ^ 2 * c ^ 2)) := by
  intro h
  have h1 := h _ _ _ rfl rfl rfl
  have h2 := (omega_pred_bounds (a0 := 1.0766e-10) (H0 := 2.1843e-18) (c := 299792458) rfl rfl rfl).2
  linarith

-- M8d: the shift a0'/a0 lies in (0.90, 0.95) (wrong; true: (0.868, 0.871)) -- false
theorem M8d_shift_wrong {a0 a0' H0 c : ℝ} (ha : a0 = 1.0766e-10) (hH : H0 = 2.1843e-18) (hc : c = 299792458)
    (ha' : 0 < a0') (hΩ : 32 * π * a0' ^ 2 / (3 * H0 ^ 2 * c ^ 2) = 0.685) :
    0.90 < a0' / a0 := by
  have h1 := Real.pi_gt_d4
  have h2 := Real.pi_lt_d4
  have hp := Real.pi_pos
  subst ha hH hc
  have hd : (0:ℝ) < 3 * (2.1843e-18) ^ 2 * (299792458:ℝ) ^ 2 := by norm_num
  rw [div_eq_iff hd.ne'] at hΩ
  by_contra hcon
  have hcon := not_lt.mp hcon
  have h3 : a0' ≤ 0.90 * 1.0766e-10 := by rwa [div_le_iff₀ (by norm_num)] at hcon
  have h4 : a0' ^ 2 ≤ (0.90 * 1.0766e-10) ^ 2 := pow_le_pow_left₀ ha'.le h3 2
  nlinarith

theorem M8d_refuted : ¬ (∀ a0 a0' H0 c : ℝ, a0 = 1.0766e-10 → H0 = 2.1843e-18 → c = 299792458 → 0 < a0' →
    32 * π * a0' ^ 2 / (3 * H0 ^ 2 * c ^ 2) = 0.685 → 0.90 < a0' / a0) := by
  intro h
  have hp := Real.pi_pos
  -- a0' = sqrt(0.685 x 3 H0^2 c^2/(32 pi)) satisfies the premise, and lies below 0.871 a0
  set K : ℝ := 3 * (2.1843e-18) ^ 2 * (299792458:ℝ) ^ 2 with hK
  have hKp : 0 < K := by rw [hK]; norm_num
  set a1 : ℝ := Real.sqrt (0.685 * K / (32 * π)) with ha1
  have ha1p : 0 < a1 := Real.sqrt_pos.mpr (by positivity)
  have ha12 : a1 ^ 2 = 0.685 * K / (32 * π) := Real.sq_sqrt (by positivity)
  have hΩ : 32 * π * a1 ^ 2 / K = 0.685 := by rw [ha12]; field_simp
  have h1 := h 1.0766e-10 a1 2.1843e-18 299792458 rfl rfl rfl ha1p (by rw [← hK]; exact hΩ)
  have h2 := (omega_shift_bounds (a0 := 1.0766e-10) (a0' := a1) (H0 := 2.1843e-18) (c := 299792458) rfl rfl rfl ha1p
    (by rw [← hK]; exact hΩ)).2
  linarith

-- M8e: Lambda = 32 pi a0^2/c^2 (wrong power of c) <=> Omega = 32 pi a0^2/(3 H0^2 c^2) -- false
theorem M8e_units_wrong {c H0 Ω a0 Λ : ℝ} (hc : 0 < c) (hH : 0 < H0) (hΛ : Λ = 3 * H0 ^ 2 * Ω / c ^ 2) :
    Λ = 32 * π * a0 ^ 2 / c ^ 2 ↔ Ω = 32 * π * a0 ^ 2 / (3 * H0 ^ 2 * c ^ 2) := by
  have hc0 : c ≠ 0 := hc.ne'
  have hH0 : H0 ≠ 0 := hH.ne'
  rw [hΛ]
  constructor
  · intro h
    field_simp at h ⊢
    nlinarith [h]
  · intro h
    rw [h]; field_simp

theorem M8e_refuted : ¬ (∀ c H0 Ω a0 Λ : ℝ, 0 < c → 0 < H0 → Λ = 3 * H0 ^ 2 * Ω / c ^ 2 →
    (Λ = 32 * π * a0 ^ 2 / c ^ 2 ↔ Ω = 32 * π * a0 ^ 2 / (3 * H0 ^ 2 * c ^ 2))) := by
  intro h
  have hp := Real.pi_pos
  -- c = 2, H0 = 1, a0 = 1, Omega = 32 pi/12: the true iff gives Lambda = 32 pi/16 while the wrong one needs 32 pi/4
  have h1 := (omega_iff (c := 2) (H0 := 1) (Ω := 32 * π * 1 ^ 2 / (3 * 1 ^ 2 * 2 ^ 2)) (a0 := 1)
    (Λ := 3 * 1 ^ 2 * (32 * π * 1 ^ 2 / (3 * 1 ^ 2 * 2 ^ 2)) / 2 ^ 2) (by norm_num) one_pos rfl).mpr rfl
  have h2 := (h 2 1 (32 * π * 1 ^ 2 / (3 * 1 ^ 2 * 2 ^ 2)) 1 (3 * 1 ^ 2 * (32 * π * 1 ^ 2 / (3 * 1 ^ 2 * 2 ^ 2)) / 2 ^ 2)
    (by norm_num) one_pos rfl).mpr rfl
  rw [h1] at h2
  nlinarith

#print axioms M8a_refuted
#print axioms M8b_refuted
#print axioms M8c_refuted
#print axioms M8d_refuted
#print axioms M8e_refuted
#print axioms M8a_omega_wrong
#print axioms M8b_Z_wrong
#print axioms M8c_pred_wrong
#print axioms M8d_shift_wrong
#print axioms M8e_units_wrong
