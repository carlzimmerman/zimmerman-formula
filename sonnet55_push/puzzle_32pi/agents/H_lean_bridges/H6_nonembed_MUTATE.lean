import Mathlib
import H6_nonembed

/-! MUTATE controls for H6_nonembed.lean: each `M6*` is a FALSE variant with the true proof script (must FAIL);
each `M6*_refuted` proves its negation from the true theorems (must COMPILE). -/

open Real Set

-- M6a: the puzzle's Z is below 2 (wrong)
theorem M6a_Z_lt_two : Zpuz < 2 := by
  have hp := Real.pi_gt_d2
  have h := Zpuz_sq
  have hz := Zpuz_pos
  nlinarith [h, hz]

theorem M6a_refuted : ¬ (Zpuz < 2) := not_lt.mpr Zpuz_gt_two.le

-- M6b: r_s > L iff Z > 1 (wrong threshold; it is Z > 2)
theorem M6b_threshold_wrong {Z L : ℝ} (hL : 0 < L) : L < Z * L / 2 ↔ 1 < Z := by
  constructor
  · intro h; nlinarith
  · intro h; nlinarith

theorem M6b_refuted : ¬ (∀ Z L : ℝ, 0 < L → (L < Z * L / 2 ↔ 1 < Z)) := by
  intro h
  have h1 := (h (3 / 2) 1 one_pos).mpr (by norm_num)
  norm_num at h1

-- M6c: M_s/M_N = 3 sqrt3 Z/2 (wrong; it is /4)
theorem M6c_mass_ratio_wrong {Z L : ℝ} (hL : 0 < L) :
    (Z * L / 4) / (L / (3 * Real.sqrt 3)) = 3 * Real.sqrt 3 * Z / 2 := by
  have : Real.sqrt 3 ≠ 0 := by positivity
  have : L ≠ 0 := hL.ne'
  field_simp

theorem M6c_refuted : ¬ (∀ Z L : ℝ, 0 < L → (Z * L / 4) / (L / (3 * Real.sqrt 3)) = 3 * Real.sqrt 3 * Z / 2) := by
  intro h
  have h1 := h 1 1 one_pos
  rw [mass_ratio_formula one_pos] at h1
  have : Real.sqrt 3 > 0 := by positivity
  nlinarith

-- M6d: SdS has no horizon already for M > L/(6 sqrt 3) (wrong threshold; it is L/(3 sqrt 3))
theorem M6d_sds_threshold_wrong {L M : ℝ} (hL : 0 < L) (hM : L / (6 * Real.sqrt 3) < M) :
    ∀ r : ℝ, 0 < r → r - 2 * M - r ^ 3 / L ^ 2 < 0 := by
  intro r hr
  have hs3 : 0 < Real.sqrt 3 := by positivity
  have hs2 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  set c := L / Real.sqrt 3 with hc
  have hc0 : 0 < c := by positivity
  have hL2 : L ^ 2 = 3 * c ^ 2 := by
    rw [hc, div_pow, hs2]; field_simp
  have hMc : c / 3 < M := by
    have : L / (6 * Real.sqrt 3) = c / 6 := by rw [hc]; field_simp
    linarith
  have hkey : r ^ 3 - 3 * c ^ 2 * r + 2 * c ^ 3 ≥ 0 := by
    nlinarith [mul_nonneg (sq_nonneg (r - c)) (by linarith : 0 ≤ r + 2 * c)]
  have hL2' : L ^ 2 ≠ 0 := by positivity
  rw [hL2]
  have h3c : 3 * c ^ 2 ≠ 0 := by positivity
  have : r - 2 * M - r ^ 3 / (3 * c ^ 2) = (3 * c ^ 2 * r - 6 * c ^ 2 * M - r ^ 3) / (3 * c ^ 2) := by
    field_simp; ring
  rw [this, div_neg_iff]
  right
  refine ⟨?_, by positivity⟩
  nlinarith [mul_pos hc0 hc0]

theorem M6d_refuted : ¬ (∀ L M : ℝ, 0 < L → L / (6 * Real.sqrt 3) < M →
    ∀ r : ℝ, 0 < r → r - 2 * M - r ^ 3 / L ^ 2 < 0) := by
  intro h
  have hs3 : 0 < Real.sqrt 3 := by positivity
  have hM : (1:ℝ) / (6 * Real.sqrt 3) < 1 / (3 * Real.sqrt 3) := by
    apply one_div_lt_one_div_of_lt (by positivity); nlinarith
  obtain ⟨r, hr, hr0⟩ := sds_horizon_exists (L := 1) (M := 1 / (3 * Real.sqrt 3)) one_pos (by positivity) le_rfl
  have := h 1 (1 / (3 * Real.sqrt 3)) one_pos hM r hr
  linarith

-- M6e: the embeddability threshold is kappa >= 1 (this is the parenthetical claimed in the peer notes; it is wrong)
theorem M6e_kappa_ge_one_wrong {κ : ℝ} (hκ : 0 < κ) : Real.sqrt (8 * π / 3) / κ ≤ 2 ↔ 1 ≤ κ := by
  have hp := Real.pi_pos
  have e : Real.sqrt (8 * π / 3) = 2 * Real.sqrt (2 * π / 3) := by
    rw [show 8 * π / 3 = 2 ^ 2 * (2 * π / 3) by ring, Real.sqrt_mul (by norm_num), Real.sqrt_sq (by norm_num)]
  rw [e, div_le_iff₀ hκ]
  constructor <;> intro h <;> linarith

theorem M6e_refuted : ¬ (∀ κ : ℝ, 0 < κ → (Real.sqrt (8 * π / 3) / κ ≤ 2 ↔ 1 ≤ κ)) := by
  intro h
  have h1 := (h 1 one_pos).mpr le_rfl
  have h2 := kappa_one_not_embeddable
  linarith

-- M6f: a pure-tension wall has 1/R^2 = H^2 + (pi sigma)^2 (wrong; it is (2 pi sigma)^2)
theorem M6f_pure_tension_wrong {H σ A B : ℝ} (hσ : 0 < σ) (hAB : A - B = 4 * π * σ)
    (h : H ^ 2 + A ^ 2 = H ^ 2 + B ^ 2) : H ^ 2 + A ^ 2 = H ^ 2 + (π * σ) ^ 2 := by
  have hp := Real.pi_pos
  have hx : 0 < 4 * π * σ := by positivity
  have h1 := israel_closed_form (Hi := H) (Ho := H) hx hAB h
  have : A = π * σ := by rw [h1]; simp; ring
  rw [this]

theorem M6f_refuted {H σ A B : ℝ} (hσ : 0 < σ) (hAB : A - B = 4 * π * σ)
    (h : H ^ 2 + A ^ 2 = H ^ 2 + B ^ 2) : ¬ (H ^ 2 + A ^ 2 = H ^ 2 + (π * σ) ^ 2) := by
  intro h2
  rw [israel_pure_tension hσ hAB h] at h2
  have hp := Real.pi_pos
  have : 0 < (π * σ) ^ 2 := by positivity
  nlinarith

-- M6g: no wall at a0 = H/Z only for Z > 1/2 (wrong; Z = 1 gives a wall with sigma = 0)
theorem M6g_no_wall_wrong {H Z σ : ℝ} (hH : 0 < H) (hZ : 1 / 2 < Z) :
    H ^ 2 + (2 * π * σ) ^ 2 ≠ (H / Z) ^ 2 := by
  intro h
  have hZ0 : 0 < Z := by linarith
  have h1 : (H / Z) ^ 2 < H ^ 2 := by
    rw [div_pow]
    have : Z ^ 2 > 1 := by nlinarith
    rw [div_lt_iff₀ (by positivity)]
    nlinarith [sq_pos_of_pos hH]
  nlinarith [sq_nonneg (2 * π * σ)]

theorem M6g_refuted : ¬ (∀ H Z σ : ℝ, 0 < H → 1 / 2 < Z → H ^ 2 + (2 * π * σ) ^ 2 ≠ (H / Z) ^ 2) := by
  intro h
  exact h 1 1 0 one_pos (by norm_num) (by norm_num)

#print axioms M6a_refuted
#print axioms M6b_refuted
#print axioms M6c_refuted
#print axioms M6d_refuted
#print axioms M6e_refuted
#print axioms M6f_refuted
#print axioms M6g_refuted
#print axioms M6a_Z_lt_two
#print axioms M6b_threshold_wrong
#print axioms M6c_mass_ratio_wrong
#print axioms M6d_sds_threshold_wrong
#print axioms M6e_kappa_ge_one_wrong
#print axioms M6f_pure_tension_wrong
#print axioms M6g_no_wall_wrong
