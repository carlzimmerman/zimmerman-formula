import Mathlib
import P1_wall_dS

/-! MUTATE controls for P1_wall_dS.lean: each `M1*` is a FALSE variant re-using the true proof script with one wrong constant or
threshold (must FAIL to compile); each `M1*_refuted` proves the negation of the false claim from the true theorem plus an explicit
instance (must COMPILE, standard axioms). -/

open Real WallDS

-- M1a: the audited claim "wall acceleration^2 = 1/R^2" (the p06/p07 identification; correct only at H = 0) -- false
theorem M1a_wall_acc_wrong {R c L : ℝ} (hR : R ≠ 0) (hL : L ≠ 0) (hRL : R ^ 2 + c ^ 2 = L ^ 2) (τ : ℝ) :
    eta (Tw R c L τ) (Tw R c L τ) = 1 / R ^ 2 := by
  obtain ⟨hAA, hAX, _⟩ := wall_embedding_acc hR c τ
  have hXX := wall_on_hyperboloid R c τ
  rw [hRL] at hXX
  have hL2 : L ^ 2 ≠ 0 := pow_ne_zero 2 hL
  have hbil : ∀ k : ℝ, eta (fun i => Aw R τ i - k * Xw R c τ i) (fun i => Aw R τ i - k * Xw R c τ i)
      = eta (Aw R τ) (Aw R τ) - 2 * k * eta (Aw R τ) (Xw R c τ) + k ^ 2 * eta (Xw R c τ) (Xw R c τ) := by
    intro k; simp only [eta]; ring
  unfold Tw
  rw [hbil, hAA, hAX, hXX]; field_simp; ring

theorem M1a_refuted : ¬ (∀ (R c L : ℝ) (τ : ℝ), R ≠ 0 → L ≠ 0 → R ^ 2 + c ^ 2 = L ^ 2 →
    eta (Tw R c L τ) (Tw R c L τ) = 1 / R ^ 2) := by
  intro h
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hL : Real.sqrt 2 ≠ 0 := by positivity
  have hRL : (1:ℝ) ^ 2 + 1 ^ 2 = Real.sqrt 2 ^ 2 := by rw [h2]; norm_num
  have h1 := h 1 1 (Real.sqrt 2) 0 one_ne_zero hL hRL
  have h3 := (wall_covariant_acc_sq (R := 1) (c := 1) (L := Real.sqrt 2) one_ne_zero hL hRL 0).2
  rw [h1, h2] at h3
  norm_num at h3

-- M1b: the static observer's acceleration^2 = (c/L^2)^2/(1 - c^2/L^2) equals 1/R^2 (forgetting the -1/L^2) -- false
theorem M1b_static_wrong {L c R : ℝ} (hL : L ≠ 0) (hR : R ≠ 0) (hRL : R ^ 2 + c ^ 2 = L ^ 2) :
    (c / L ^ 2) ^ 2 / (1 - c ^ 2 / L ^ 2) = 1 / R ^ 2 := by
  have hc : c ^ 2 = L ^ 2 - R ^ 2 := by linarith
  have hL2 : L ^ 2 ≠ 0 := pow_ne_zero 2 hL
  have hR2 : R ^ 2 ≠ 0 := pow_ne_zero 2 hR
  have h1 : 1 - c ^ 2 / L ^ 2 = R ^ 2 / L ^ 2 := by rw [hc]; field_simp; ring
  rw [h1, div_pow, hc]
  field_simp

theorem M1b_refuted : ¬ (∀ (L c R : ℝ), L ≠ 0 → R ≠ 0 → R ^ 2 + c ^ 2 = L ^ 2 →
    (c / L ^ 2) ^ 2 / (1 - c ^ 2 / L ^ 2) = 1 / R ^ 2) := by
  intro h
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hL : Real.sqrt 2 ≠ 0 := by positivity
  have hRL : (1:ℝ) ^ 2 + 1 ^ 2 = Real.sqrt 2 ^ 2 := by rw [h2]; norm_num
  have h1 := h (Real.sqrt 2) 1 1 hL one_ne_zero hRL
  have h3 := static_eq_wall (L := Real.sqrt 2) (c := 1) (R := 1) hL one_ne_zero hRL
  rw [h1, h2] at h3
  norm_num at h3

-- M1c: Israel side A = DeltaP/(3 sigma) + pi sigma (wrong: 2 pi sigma) -- false
theorem M1c_israel_side_wrong {A B σ E e : ℝ} (hσ : 0 < σ)
    (h1 : A - B = 4 * π * σ) (h2 : A ^ 2 - B ^ 2 = Hsq (E ^ 2 / 2) - Hsq ((E - e) ^ 2 / 2)) :
    A = (e * E - e ^ 2 / 2) / (3 * σ) + π * σ := by
  have hp := Real.pi_pos
  have hs : σ ≠ 0 := hσ.ne'
  unfold Hsq at h2
  have hsum : A + B = (2 * (e * E - e ^ 2 / 2)) / (3 * σ) := by
    have hprod : (A - B) * (A + B) = (8 * π / 3) * (E ^ 2 / 2) - (8 * π / 3) * ((E - e) ^ 2 / 2) := by
      nlinarith [h2]
    rw [h1] at hprod
    have : 4 * π * σ * (A + B) = 4 * π * σ * ((2 * (e * E - e ^ 2 / 2)) / (3 * σ)) := by
      rw [hprod]; field_simp; ring
    exact mul_left_cancel₀ (by positivity) this
  have : A = ((A + B) + (A - B)) / 2 := by ring
  rw [this, hsum, h1]; field_simp; ring

theorem M1c_refuted : ¬ (∀ (A B σ E e : ℝ), 0 < σ → A - B = 4 * π * σ →
    A ^ 2 - B ^ 2 = Hsq (E ^ 2 / 2) - Hsq ((E - e) ^ 2 / 2) →
    A = (e * E - e ^ 2 / 2) / (3 * σ) + π * σ) := by
  intro h
  have hp := Real.pi_pos
  have h1 : (2 * π) - (-(2 * π)) = 4 * π * 1 := by ring
  have h2 : (2 * π) ^ 2 - (-(2 * π)) ^ 2 = Hsq (1 ^ 2 / 2) - Hsq ((1 - 0) ^ 2 / 2) := by
    unfold Hsq; ring
  have h3 := h (2 * π) (-(2 * π)) 1 1 0 one_pos h1 h2
  norm_num at h3

-- M1d: pure tension 1/R^2 = H^2 + (pi sigma)^2 (wrong: (2 pi sigma)^2) -- false
theorem M1d_pure_tension_wrong {A B σ H : ℝ} (hσ : 0 < σ)
    (h1 : A - B = 4 * π * σ) (h2 : A ^ 2 - B ^ 2 = H ^ 2 - H ^ 2) :
    H ^ 2 + A ^ 2 = H ^ 2 + (π * σ) ^ 2 := by
  have hp := Real.pi_pos
  have hsum : A + B = 0 := by
    have : (A - B) * (A + B) = 0 := by nlinarith [h2]
    rw [h1] at this
    rcases mul_eq_zero.mp this with h | h
    · exfalso; have : 0 < 4 * π * σ := by positivity
      linarith
    · exact h
  have hA : A = 2 * π * σ := by linarith
  rw [hA]; ring

theorem M1d_refuted : ¬ (∀ (A B σ H : ℝ), 0 < σ → A - B = 4 * π * σ → A ^ 2 - B ^ 2 = H ^ 2 - H ^ 2 →
    H ^ 2 + A ^ 2 = H ^ 2 + (π * σ) ^ 2) := by
  intro h
  have hp := Real.pi_pos
  have h1 : (2 * π) - (-(2 * π)) = 4 * π * 1 := by ring
  have h2 : (2 * π) ^ 2 - (-(2 * π)) ^ 2 = (0:ℝ) ^ 2 - 0 ^ 2 := by ring
  have h3 := h (2 * π) (-(2 * π)) 1 0 one_pos h1 h2
  nlinarith [sq_pos_of_pos hp]

-- M1e: the target ratio (r E/3)^2 = H_out^2/Z^2 iff r^2 = 9/4 (wrong: 9/8) -- false
theorem M1e_probe_ratio_wrong {E r : ℝ} (hE : 0 < E) :
    (r * E / 3) ^ 2 = Hsq (E ^ 2 / 2) / (32 * π / 3) ↔ r ^ 2 = 9 / 4 := by
  have hp := Real.pi_pos
  have hE2 : E ^ 2 ≠ 0 := by positivity
  have hpi : π ≠ 0 := hp.ne'
  have key : Hsq (E ^ 2 / 2) / (32 * π / 3) = E ^ 2 / 8 := by
    unfold Hsq; field_simp; ring
  rw [key]
  constructor
  · intro h
    have : E ^ 2 * (r ^ 2 - 9 / 4) = 0 := by nlinarith [h]
    rcases mul_eq_zero.mp this with h' | h'
    · exact absurd h' hE2
    · linarith
  · intro h
    have : (r * E / 3) ^ 2 = r ^ 2 * E ^ 2 / 9 := by ring
    rw [this, h]; ring

theorem M1e_refuted : ¬ (∀ (E r : ℝ), 0 < E → ((r * E / 3) ^ 2 = Hsq (E ^ 2 / 2) / (32 * π / 3) ↔ r ^ 2 = 9 / 4)) := by
  intro h
  have hr : (3 / (2 * Real.sqrt 2)) ^ 2 = (9 : ℝ) / 8 := probe_ratio_value
  have h1 := (probe_target_ratio (E := 1) (r := 3 / (2 * Real.sqrt 2)) one_pos).mpr hr
  have h2 := (h 1 (3 / (2 * Real.sqrt 2)) one_pos).mp h1
  rw [hr] at h2
  norm_num at h2

-- M1f: the mean of the two Israel sides is DeltaP/(2 sigma) (wrong: DeltaP/(3 sigma)) -- false
theorem M1f_mean_wrong {A B σ E e : ℝ} (hσ : 0 < σ)
    (h1 : A - B = 4 * π * σ) (h2 : A ^ 2 - B ^ 2 = Hsq (E ^ 2 / 2) - Hsq ((E - e) ^ 2 / 2)) :
    (A + B) / 2 = (e * E - e ^ 2 / 2) / (2 * σ) := by
  obtain ⟨hA, hB⟩ := israel_sides hσ h1 h2
  rw [hA, hB]
  have hs : σ ≠ 0 := hσ.ne'
  field_simp; ring

theorem M1f_refuted : ¬ (∀ (A B σ E e : ℝ), 0 < σ → A - B = 4 * π * σ →
    A ^ 2 - B ^ 2 = Hsq (E ^ 2 / 2) - Hsq ((E - e) ^ 2 / 2) → (A + B) / 2 = (e * E - e ^ 2 / 2) / (2 * σ)) := by
  intro h
  have hp := Real.pi_pos
  obtain ⟨h1, h2⟩ := israel_sides_converse (σ := 1) (E := 1) (e := 1) one_pos
  have h3 := h _ _ 1 1 1 one_pos h1 h2
  norm_num at h3

-- M1g: embedding acceleration eta A A = 1/R (wrong: 1/R^2) -- false
theorem M1g_embedding_wrong {R : ℝ} (hR : R ≠ 0) (τ : ℝ) : eta (Aw R τ) (Aw R τ) = 1 / R := by
  have h := Real.cosh_sq (τ / R)
  simp [eta, Aw]
  field_simp
  nlinarith [h]

theorem M1g_refuted : ¬ (∀ (R τ : ℝ), R ≠ 0 → eta (Aw R τ) (Aw R τ) = 1 / R) := by
  intro h
  have h1 := h 2 0 (by norm_num)
  have h2 := (wall_embedding_acc (R := 2) (by norm_num) 0 0).1
  rw [h1] at h2
  norm_num at h2

-- M1h: tau is proper time with eta U U = +1 (wrong sign) -- false
theorem M1h_unit_wrong (R τ : ℝ) : eta (Uw R τ) (Uw R τ) = 1 := by
  have := Real.cosh_sq (τ / R)
  simp [eta, Uw]
  nlinarith [this]

theorem M1h_refuted : ¬ (∀ (R τ : ℝ), eta (Uw R τ) (Uw R τ) = 1) := by
  intro h
  have h1 := h 1 0
  rw [wall_velocity_unit] at h1
  norm_num at h1

#print axioms M1a_refuted
#print axioms M1b_refuted
#print axioms M1c_refuted
#print axioms M1d_refuted
#print axioms M1e_refuted
#print axioms M1f_refuted
#print axioms M1g_refuted
#print axioms M1h_refuted
#print axioms M1a_wall_acc_wrong
#print axioms M1b_static_wrong
#print axioms M1c_israel_side_wrong
#print axioms M1d_pure_tension_wrong
#print axioms M1e_probe_ratio_wrong
#print axioms M1f_mean_wrong
#print axioms M1g_embedding_wrong
#print axioms M1h_unit_wrong
