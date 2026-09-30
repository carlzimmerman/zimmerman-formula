import Mathlib
import P3_record_iff

/-! MUTATE controls for P3_record_iff.lean: each `M3*` is a FALSE variant re-using the true proof script with one wrong constant or
threshold (must FAIL to compile); each `M3*_refuted` proves the negation from the true theorems plus an explicit instance (must COMPILE). -/

open Real MeasureTheory intervalIntegral RecordIff

-- M3a: kappa = 1/2 <=> M1 = (5/3) t_Lambda (wrong moment; true: 4/3) -- false
theorem M3a_iff_wrong {κ c G ρ : ℝ} (hκ : 0 < κ) (hc : 0 < c) (hG : 0 < G) (hρ : 0 < ρ) :
    M1of c (a0of κ c G ρ) = (5 / 3) * tLam G ρ ↔ κ = 1 / 2 := by
  have hs := sqrt_pos' hG hρ
  unfold M1of a0of tLam
  rw [div_eq_iff (by positivity)]
  constructor
  · intro h
    field_simp at h
    nlinarith [h]
  · intro h; rw [h]; field_simp; ring

theorem M3a_refuted : ¬ (∀ κ c G ρ : ℝ, 0 < κ → 0 < c → 0 < G → 0 < ρ →
    (M1of c (a0of κ c G ρ) = (5 / 3) * tLam G ρ ↔ κ = 1 / 2)) := by
  intro h
  have h1 := (enthalpy_family (κ := 2 / 5) (c := 1) (G := 1) (ρ := 1) (w := 2 / 3) (by norm_num) one_pos one_pos one_pos
    (by norm_num)).mpr (by norm_num)
  have h2 := (h (2 / 5) 1 1 1 (by norm_num) one_pos one_pos one_pos).mp
    (by rw [show (5 : ℝ) / 3 = 1 + 2 / 3 by norm_num]; exact h1)
  norm_num at h2

-- M3b: enthalpy family kappa = 1/(1 + w) (wrong; true: 2/(3(1 + w))) -- false
theorem M3b_family_wrong {κ c G ρ w : ℝ} (hκ : 0 < κ) (hc : 0 < c) (hG : 0 < G) (hρ : 0 < ρ) (hw : -1 < w) :
    M1of c (a0of κ c G ρ) = (1 + w) * tLam G ρ ↔ κ = 1 / (1 + w) := by
  have hs := sqrt_pos' hG hρ
  have hw1 : 0 < 1 + w := by linarith
  unfold M1of a0of tLam
  rw [div_eq_iff (by positivity)]
  constructor
  · intro h
    field_simp at h ⊢
    nlinarith [h]
  · intro h; rw [h]; field_simp

theorem M3b_refuted : ¬ (∀ κ c G ρ w : ℝ, 0 < κ → 0 < c → 0 < G → 0 < ρ → -1 < w →
    (M1of c (a0of κ c G ρ) = (1 + w) * tLam G ρ ↔ κ = 1 / (1 + w))) := by
  intro h
  have h1 := (enthalpy_family (κ := 2 / 3) (c := 1) (G := 1) (ρ := 1) (w := 0) (by norm_num) one_pos one_pos one_pos
    (by norm_num)).mpr (by norm_num)
  have h2 := (h (2 / 3) 1 1 1 0 (by norm_num) one_pos one_pos one_pos (by norm_num)).mp h1
  norm_num at h2

-- M3c: kappa(w) = 1/2 <=> w = 1/2 (wrong; true: w = 1/3) -- false
theorem M3c_w_wrong {w : ℝ} (hw : -1 < w) : 2 / (3 * (1 + w)) = 1 / 2 ↔ w = 1 / 2 := by
  have hw1 : 0 < 1 + w := by linarith
  rw [div_eq_div_iff (by positivity) (by norm_num)]
  constructor <;> intro h <;> linarith

theorem M3c_refuted : ¬ (∀ w : ℝ, -1 < w → (2 / (3 * (1 + w)) = 1 / 2 ↔ w = 1 / 2)) := by
  intro h
  have h1 := (kappa_half_iff_w (w := 1 / 3) (by norm_num)).mpr rfl
  have h2 := (h (1 / 3) (by norm_num)).mp h1
  norm_num at h2

-- M3d: radiation in d spatial dimensions gives kappa = 1/2 iff d = 4 (wrong; true: d = 3) -- false
theorem M3d_dim_wrong {d : ℝ} (hd : 0 < d) : 2 / (3 * (1 + 1 / d)) = 1 / 2 ↔ d = 4 := by
  have hd0 : d ≠ 0 := hd.ne'
  have hd1 : 0 < d + 1 := by linarith
  have hd10 : d + 1 ≠ 0 := hd1.ne'
  have h1 : 2 / (3 * (1 + 1 / d)) = (2 / 3) * (d / (d + 1)) := by field_simp
  rw [h1]
  constructor
  · intro h
    field_simp at h
    linarith
  · intro h
    rw [h]; norm_num

theorem M3d_refuted : ¬ (∀ d : ℝ, 0 < d → (2 / (3 * (1 + 1 / d)) = 1 / 2 ↔ d = 4)) := by
  intro h
  have h1 := ((kappa_dim (d := 3) (by norm_num)).2).mpr rfl
  have h2 := (h 3 (by norm_num)).mp h1
  norm_num at h2

-- M3e: the sharp-kernel first moment is T/2 (that is the UNIFORM kernel's value; true: 2T/3) -- false
theorem M3e_moment_wrong {T : ℝ} (hT : 0 < T) : ∫ τ in (0:ℝ)..T, τ * (2 * τ / T ^ 2) = T / 2 := by
  have hT0 : T ≠ 0 := hT.ne'
  have : (fun τ : ℝ => τ * (2 * τ / T ^ 2)) = fun τ => (2 / T ^ 2) * τ ^ 2 := by funext τ; ring
  rw [this, intervalIntegral.integral_const_mul, integral_pow]
  field_simp; ring

theorem M3e_refuted : ¬ (∀ T : ℝ, 0 < T → ∫ τ in (0:ℝ)..T, τ * (2 * τ / T ^ 2) = T / 2) := by
  intro h
  have h1 := h 1 one_pos
  rw [kernel_first_moment one_pos] at h1
  norm_num at h1

-- M3f: the sharp kernel has total weight 2 (true: 1) -- false
theorem M3f_norm_wrong {T : ℝ} (hT : 0 < T) : ∫ τ in (0:ℝ)..T, 2 * τ / T ^ 2 = 2 := by
  have hT0 : T ≠ 0 := hT.ne'
  have : (fun τ : ℝ => 2 * τ / T ^ 2) = fun τ => (2 / T ^ 2) * τ := by funext τ; ring
  rw [this, intervalIntegral.integral_const_mul, integral_id]
  field_simp; ring

theorem M3f_refuted : ¬ (∀ T : ℝ, 0 < T → ∫ τ in (0:ℝ)..T, 2 * τ / T ^ 2 = 2) := by
  intro h
  have h1 := h 1 one_pos
  rw [kernel_norm one_pos] at h1
  norm_num at h1

-- M3g: Sciama's integral at the Hubble radius is 1/2 (true: 3/4) -- false
theorem M3g_hubble_wrong {G ρ c H : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hc : 0 < c) (hH : 0 < H) (hF : H ^ 2 = 8 * π * G * ρ / 3) :
    Isc G ρ c (c / H) = 1 / 2 := by
  have hp := Real.pi_pos
  unfold Isc
  have hH0 : H ≠ 0 := hH.ne'
  have hc0 : c ≠ 0 := hc.ne'
  have : 2 * π * G * ρ * (c / H) ^ 2 / c ^ 2 = 2 * π * G * ρ / H ^ 2 := by field_simp
  rw [this, hF]
  field_simp; ring

theorem M3g_refuted : ¬ (∀ G ρ c H : ℝ, 0 < G → 0 < ρ → 0 < c → 0 < H → H ^ 2 = 8 * π * G * ρ / 3 →
    Isc G ρ c (c / H) = 1 / 2) := by
  intro h
  have hp := Real.pi_pos
  have hH : 0 < Real.sqrt (8 * π / 3) := Real.sqrt_pos.mpr (by positivity)
  have hF : Real.sqrt (8 * π / 3) ^ 2 = 8 * π * 1 * 1 / 3 := by rw [Real.sq_sqrt (by positivity)]; ring
  have h1 := h 1 1 1 _ one_pos one_pos one_pos hH hF
  rw [sciama_hubble one_pos one_pos one_pos hH hF] at h1
  norm_num at h1

-- M3h: Sciama's integral at R* is pi (true: 2 pi) -- false
theorem M3h_Rstar_wrong {G ρ c : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hc : 0 < c) :
    Isc G ρ c (c / Real.sqrt (G * ρ)) = π := by
  have hs := sqrt_pos' hG hρ
  have h2 := Real.sq_sqrt (show 0 ≤ G * ρ by positivity)
  unfold Isc
  have hc0 : c ≠ 0 := hc.ne'
  have : 2 * π * G * ρ * (c / Real.sqrt (G * ρ)) ^ 2 / c ^ 2 = 2 * π * (G * ρ) / Real.sqrt (G * ρ) ^ 2 := by
    field_simp
  rw [this, h2]; field_simp

theorem M3h_refuted : ¬ (∀ G ρ c : ℝ, 0 < G → 0 < ρ → 0 < c → Isc G ρ c (c / Real.sqrt (G * ρ)) = π) := by
  intro h
  have hp := Real.pi_pos
  have h1 := h 1 1 1 one_pos one_pos one_pos
  rw [sciama_Rstar one_pos one_pos one_pos] at h1
  linarith

-- M3i: Sciama's integral at 2R* is 4 pi (true: 8 pi) -- false
theorem M3i_2Rstar_wrong {G ρ c : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hc : 0 < c) :
    Isc G ρ c (2 * (c / Real.sqrt (G * ρ))) = 4 * π := by
  have hs := sqrt_pos' hG hρ
  have h2 := Real.sq_sqrt (show 0 ≤ G * ρ by positivity)
  unfold Isc
  have hc0 : c ≠ 0 := hc.ne'
  have : 2 * π * G * ρ * (2 * (c / Real.sqrt (G * ρ))) ^ 2 / c ^ 2 = 8 * π * (G * ρ) / Real.sqrt (G * ρ) ^ 2 := by
    field_simp; ring
  rw [this, h2]; field_simp

theorem M3i_refuted : ¬ (∀ G ρ c : ℝ, 0 < G → 0 < ρ → 0 < c → Isc G ρ c (2 * (c / Real.sqrt (G * ρ))) = 4 * π) := by
  intro h
  have hp := Real.pi_pos
  have h1 := h 1 1 1 one_pos one_pos one_pos
  rw [sciama_2Rstar one_pos one_pos one_pos] at h1
  linarith

-- M3j: the Rindler-converted ratio at 2R* is 1/2 (true: 1/4) -- false
theorem M3j_rindler_wrong {G ρ c : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hc : 0 < c) :
    rindlerRatio G ρ c (2 * (c / Real.sqrt (G * ρ))) = 1 / 2 := by
  have hs := sqrt_pos' hG hρ
  have h2 := Real.sq_sqrt (show 0 ≤ G * ρ by positivity)
  have hc0 : c ≠ 0 := hc.ne'
  unfold rindlerRatio
  have : (c ^ 2 / (2 * (c / Real.sqrt (G * ρ)))) ^ 2 / (G * ρ * c ^ 2) = c ^ 2 * Real.sqrt (G * ρ) ^ 2 / (4 * (G * ρ * c ^ 2)) := by
    field_simp; norm_num
  rw [this, h2]; field_simp

theorem M3j_refuted : ¬ (∀ G ρ c : ℝ, 0 < G → 0 < ρ → 0 < c → rindlerRatio G ρ c (2 * (c / Real.sqrt (G * ρ))) = 1 / 2) := by
  intro h
  have hp := Real.pi_pos
  have hH : 0 < Real.sqrt (8 * π / 3) := Real.sqrt_pos.mpr (by positivity)
  have hF : Real.sqrt (8 * π / 3) ^ 2 = 8 * π * 1 * 1 / 3 := by rw [Real.sq_sqrt (by positivity)]; ring
  have h1 := h 1 1 1 one_pos one_pos one_pos
  rw [(rindler_conversion one_pos one_pos one_pos hH hF).2.2.2] at h1
  norm_num at h1

-- M3k: kappa = 1 <=> R_c = 2 R* (true: kappa = 1/2) -- false
theorem M3k_Rc_wrong {κ c G ρ : ℝ} (hκ : 0 < κ) (hc : 0 < c) (hG : 0 < G) (hρ : 0 < ρ) :
    c ^ 2 / a0of κ c G ρ = 2 * (c / Real.sqrt (G * ρ)) ↔ κ = 1 := by
  have hs := sqrt_pos' hG hρ
  unfold a0of
  rw [div_eq_iff (by positivity)]
  constructor
  · intro h
    field_simp at h
    nlinarith [h]
  · intro h; rw [h]; field_simp

theorem M3k_refuted : ¬ (∀ κ c G ρ : ℝ, 0 < κ → 0 < c → 0 < G → 0 < ρ →
    (c ^ 2 / a0of κ c G ρ = 2 * (c / Real.sqrt (G * ρ)) ↔ κ = 1)) := by
  intro h
  have h1 := (Rc_eq_two_Rstar_iff (κ := 1 / 2) (c := 1) (G := 1) (ρ := 1) (by norm_num) one_pos one_pos one_pos).mpr rfl
  have h2 := (h (1 / 2) 1 1 1 (by norm_num) one_pos one_pos one_pos).mp h1
  norm_num at h2

-- M3l: mu'(0) = (N + 1)/s (true: N/s) -- false
theorem M3l_slope_wrong {s N : ℝ} (hs : 0 < s) : HasDerivAt (fun g : ℝ => 1 - (1 - (g / s) / (1 + g / s)) ^ N) ((N + 1) / s) 0 := by
  have h1 := mu_p_deriv N
  have h2 := p_g_deriv hs
  have h3 : HasDerivAt ((fun p : ℝ => 1 - (1 - p) ^ N) ∘ (fun g : ℝ => (g / s) / (1 + g / s))) (N * (1 / s)) 0 := by
    have h1' : HasDerivAt (fun p : ℝ => 1 - (1 - p) ^ N) N ((fun g : ℝ => (g / s) / (1 + g / s)) 0) := by
      simpa using h1
    exact h1'.comp 0 h2
  refine h3.congr_deriv ?_
  ring

theorem M3l_refuted : ¬ (∀ s N : ℝ, 0 < s → HasDerivAt (fun g : ℝ => 1 - (1 - (g / s) / (1 + g / s)) ^ N) ((N + 1) / s) 0) := by
  intro h
  have h1 := h 1 0 one_pos
  have h2 := mu_slope (s := 1) (N := 0) one_pos
  have := h1.unique h2
  norm_num at this

-- M3m: the coupling factor for a0^2/(G rho c^2) = 1/4 is 1/(4 pi) (true: 1/(8 pi)) -- false
theorem M3m_coupling_wrong {g : ℝ} : 2 * π * g = 1 / 4 ↔ g = 1 / (4 * π) := by
  have hp := Real.pi_pos
  rw [eq_div_iff (by norm_num : (4:ℝ) ≠ 0), eq_div_iff (by positivity : (4 * π) ≠ 0)]
  constructor <;> intro h <;> nlinarith [h]

theorem M3m_refuted : ¬ (∀ g : ℝ, 2 * π * g = 1 / 4 ↔ g = 1 / (4 * π)) := by
  intro h
  have hp := Real.pi_pos
  have h1 := (h (1 / (8 * π))).mp ((coupling_puzzle).mpr rfl)
  field_simp at h1
  nlinarith

-- M3n: the potential of a uniform ball is int_0^R 4 pi r^2 (1/r) dr = 4 pi R^2 (true: 2 pi R^2) -- false
theorem M3n_potential_wrong (R : ℝ) : ∫ r in (0:ℝ)..R, 4 * π * r ^ 2 * (1 / r) = 4 * π * R ^ 2 := by
  have : (fun r : ℝ => 4 * π * r ^ 2 * (1 / r)) = fun r => (4 * π) * r := by
    funext r
    rcases eq_or_ne r 0 with h | h
    · simp [h]
    · field_simp
  rw [this, intervalIntegral.integral_const_mul, integral_id]
  ring

theorem M3n_refuted : ¬ (∀ R : ℝ, ∫ r in (0:ℝ)..R, 4 * π * r ^ 2 * (1 / r) = 4 * π * R ^ 2) := by
  intro h
  have hp := Real.pi_pos
  have h1 := h 1
  rw [sciama_potential] at h1
  nlinarith

#print axioms M3a_refuted
#print axioms M3b_refuted
#print axioms M3c_refuted
#print axioms M3d_refuted
#print axioms M3e_refuted
#print axioms M3f_refuted
#print axioms M3g_refuted
#print axioms M3h_refuted
#print axioms M3i_refuted
#print axioms M3j_refuted
#print axioms M3k_refuted
#print axioms M3l_refuted
#print axioms M3m_refuted
#print axioms M3n_refuted
#print axioms M3a_iff_wrong
#print axioms M3b_family_wrong
#print axioms M3c_w_wrong
#print axioms M3d_dim_wrong
#print axioms M3e_moment_wrong
#print axioms M3f_norm_wrong
#print axioms M3g_hubble_wrong
#print axioms M3h_Rstar_wrong
#print axioms M3i_2Rstar_wrong
#print axioms M3j_rindler_wrong
#print axioms M3k_Rc_wrong
#print axioms M3l_slope_wrong
#print axioms M3m_coupling_wrong
#print axioms M3n_potential_wrong
