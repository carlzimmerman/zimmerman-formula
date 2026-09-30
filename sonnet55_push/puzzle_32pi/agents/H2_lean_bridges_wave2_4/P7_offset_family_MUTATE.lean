import Mathlib
import P7_offset_family

/-! MUTATE controls for P7_offset_family.lean: each `M7*` is a FALSE variant re-using the true proof script with one wrong constant or
dropped hypothesis (must FAIL to compile); each `M7*_refuted` proves the negation from the true theorems plus an explicit instance (must COMPILE). -/

open Real MeasureTheory intervalIntegral OffsetFamily Set

theorem exists_cbrt7 {a : ℝ} (ha : 0 < a) : ∃ s : ℝ, 0 < s ∧ s ^ 3 = a := by
  refine ⟨a ^ ((1:ℝ) / 3), Real.rpow_pos_of_pos ha _, ?_⟩
  rw [← Real.rpow_natCast, ← Real.rpow_mul ha.le]; norm_num

-- M7a: G rho = 4 a0^2 iff c = 16 pi (wrong; true: 32 pi) -- false
theorem M7a_offset_wrong {G ρ a0 c : ℝ} (ha : a0 ≠ 0) (h : G * ρ / a0 ^ 2 = c / (8 * π)) : G * ρ = 4 * a0 ^ 2 ↔ c = 16 * π := by
  have hp := Real.pi_pos
  have hp0 : 8 * π ≠ 0 := by positivity
  have ha2 : a0 ^ 2 ≠ 0 := pow_ne_zero 2 ha
  rw [div_eq_div_iff ha2 hp0] at h
  constructor
  · intro h1
    have : a0 ^ 2 * (c - 16 * π) = 0 := by nlinarith [h, h1]
    rcases mul_eq_zero.mp this with h2 | h2
    · exact absurd h2 ha2
    · linarith
  · intro h1; rw [h1] at h; nlinarith [h]

theorem M7a_refuted : ¬ (∀ G ρ a0 c : ℝ, a0 ≠ 0 → G * ρ / a0 ^ 2 = c / (8 * π) → (G * ρ = 4 * a0 ^ 2 ↔ c = 16 * π)) := by
  intro h
  have hp := Real.pi_pos
  have h1 : (1:ℝ) * 4 / 1 ^ 2 = (32 * π) / (8 * π) := by field_simp; norm_num
  have h2 := (h 1 4 1 (32 * π) one_ne_zero h1).mp (by norm_num)
  nlinarith

-- M7b: c_req = 3 Z^2 = 32 pi iff Z^2 = 8 pi/3 (wrong; true: 32 pi/3) -- false
theorem M7b_cZ_wrong {Z : ℝ} : 3 * Z ^ 2 = 32 * π ↔ Z ^ 2 = 8 * π / 3 := by
  constructor <;> intro h <;> linarith

theorem M7b_refuted : ¬ (∀ Z : ℝ, 3 * Z ^ 2 = 32 * π ↔ Z ^ 2 = 8 * π / 3) := by
  intro h
  have hp := Real.pi_pos
  have h1 : Real.sqrt (32 * π / 3) ^ 2 = 32 * π / 3 := Real.sq_sqrt (by positivity)
  have h2 := (h (Real.sqrt (32 * π / 3))).mp (by rw [h1]; ring)
  rw [h1] at h2
  nlinarith

-- M7c: some rational equals 32 pi -- false (irrational_pi)
theorem M7c_rational_exists : ∃ q : ℚ, (q : ℝ) = 32 * π := by
  refine ⟨100, ?_⟩
  have := Real.pi_gt_three
  norm_num
  nlinarith

theorem M7c_refuted : ¬ (∃ q : ℚ, (q : ℝ) = 32 * π) := by
  rintro ⟨q, hq⟩
  exact poisson_no_rational q hq

-- M7d: bathtub bound c >= 1/2 (wrong; true: 1/3) -- false
theorem M7d_bathtub_wrong {μ : ℝ → ℝ} (hc : ContinuousOn μ (Set.Ici 0)) (hle : ∀ x, 0 ≤ x → μ x ≤ x) (h1 : ∀ x, 0 ≤ x → μ x ≤ 1)
    {T : ℝ} (hT : 1 ≤ T) : 1 / 2 ≤ ∫ x in (0:ℝ)..T, (1 - μ x) * (2 * x) := by
  have hint : ∀ a b : ℝ, 0 ≤ a → a ≤ b → IntervalIntegrable (fun x => (1 - μ x) * (2 * x)) volume a b := by
    intro a b ha hab
    apply ContinuousOn.intervalIntegrable
    have hsub : Set.uIcc a b ⊆ Set.Ici 0 := by
      intro y hy
      rw [Set.uIcc_of_le hab] at hy
      exact Set.mem_Ici.mpr (le_trans ha hy.1)
    exact ((continuousOn_const.sub (hc.mono hsub)).mul (continuousOn_const.mul continuousOn_id))
  have hsplit := intervalIntegral.integral_add_adjacent_intervals (hint 0 1 le_rfl zero_le_one) (hint 1 T zero_le_one hT)
  rw [← hsplit]
  have hA : 1 / 2 ≤ ∫ x in (0:ℝ)..1, (1 - μ x) * (2 * x) := by
    rw [← int_lin_one]
    apply intervalIntegral.integral_mono_on zero_le_one
    · exact (continuous_const.sub continuous_id).mul (continuous_const.mul continuous_id) |>.intervalIntegrable _ _
    · exact hint 0 1 le_rfl zero_le_one
    · intro x hx
      have := hle x hx.1
      have hx0 : 0 ≤ 2 * x := by linarith [hx.1]
      nlinarith
  have hB : 0 ≤ ∫ x in (1:ℝ)..T, (1 - μ x) * (2 * x) := by
    apply intervalIntegral.integral_nonneg hT
    intro x hx
    have := h1 x (le_trans zero_le_one hx.1)
    have hx0 : 0 ≤ 2 * x := by linarith [hx.1]
    have : 0 ≤ 1 - μ x := by linarith
    positivity
  linarith

theorem M7d_refuted : ¬ (∀ (μ : ℝ → ℝ), ContinuousOn μ (Set.Ici 0) → (∀ x, 0 ≤ x → μ x ≤ x) → (∀ x, 0 ≤ x → μ x ≤ 1) →
    ∀ T : ℝ, 1 ≤ T → 1 / 2 ≤ ∫ x in (0:ℝ)..T, (1 - μ x) * (2 * x)) := by
  intro h
  have hc : ContinuousOn (fun x : ℝ => min x 1) (Set.Ici 0) := (continuous_id.min continuous_const).continuousOn
  have h1 := h (fun x => min x 1) hc (fun x _ => min_le_left _ _) (fun x _ => min_le_right _ _) 1 le_rfl
  rw [sharp_value le_rfl] at h1
  norm_num at h1

-- M7e: the hypothesis mu <= x (i.e. slope <= 1) dropped: still c >= 1/3 -- false
theorem M7e_bathtub_nohyp {μ : ℝ → ℝ} (hc : ContinuousOn μ (Set.Ici 0)) (h1 : ∀ x, 0 ≤ x → μ x ≤ 1)
    {T : ℝ} (hT : 1 ≤ T) : 1 / 3 ≤ ∫ x in (0:ℝ)..T, (1 - μ x) * (2 * x) := by
  exact bathtub_bound hc (fun x hx => by have := h1 x hx; nlinarith) h1 hT

theorem M7e_refuted : ¬ (∀ (μ : ℝ → ℝ), ContinuousOn μ (Set.Ici 0) → (∀ x, 0 ≤ x → μ x ≤ 1) →
    ∀ T : ℝ, 1 ≤ T → 1 / 3 ≤ ∫ x in (0:ℝ)..T, (1 - μ x) * (2 * x)) := by
  intro h
  have hc : ContinuousOn (fun x : ℝ => min (2 * x) 1) (Set.Ici 0) :=
    ((continuous_const.mul continuous_id).min continuous_const).continuousOn
  have h1 := h (fun x => min (2 * x) 1) hc (fun x _ => min_le_right _ _) 1 le_rfl
  rw [steep_value (by norm_num)] at h1
  norm_num at h1

-- M7f: the sharp mu = min(x, 1) has partial integral 1/2 (true: 1/3) -- false
theorem M7f_sharp_wrong {T : ℝ} (hT : 1 ≤ T) : ∫ x in (0:ℝ)..T, (1 - min x 1) * (2 * x) = 1 / 2 := by
  have hc1 : Continuous fun x : ℝ => (1 - min x 1) * (2 * x) :=
    (continuous_const.sub (continuous_id.min continuous_const)).mul (continuous_const.mul continuous_id)
  rw [← intervalIntegral.integral_add_adjacent_intervals (hc1.intervalIntegrable 0 1) (hc1.intervalIntegrable 1 T)]
  have h1 : ∫ x in (0:ℝ)..1, (1 - min x 1) * (2 * x) = 1 / 2 := by
    rw [show (1:ℝ) / 2 = 1 / 3 from ?_]
    · rw [← int_lin_one]
      apply intervalIntegral.integral_congr
      intro x hx
      rw [Set.uIcc_of_le zero_le_one] at hx
      simp [min_eq_left hx.2]
    · norm_num
  have h2 : ∫ x in (1:ℝ)..T, (1 - min x 1) * (2 * x) = 0 := by
    have : ∫ x in (1:ℝ)..T, (1 - min x 1) * (2 * x) = ∫ x in (1:ℝ)..T, (0:ℝ) := by
      apply intervalIntegral.integral_congr
      intro x hx
      rw [Set.uIcc_of_le hT] at hx
      simp [min_eq_right hx.1]
    rw [this]; simp
  rw [h1, h2]; ring

theorem M7f_refuted : ¬ (∀ T : ℝ, 1 ≤ T → ∫ x in (0:ℝ)..T, (1 - min x 1) * (2 * x) = 1 / 2) := by
  intro h
  have h1 := h 1 le_rfl
  rw [sharp_value le_rfl] at h1
  norm_num at h1

-- M7g: c(N) = 8 pi N^2 iff (N - 1)(N - 2) = 1/(2 pi) (wrong; true: 1/(4 pi)) -- false
theorem M7g_cN_wrong {N : ℝ} (hN : 2 < N) : cN N = 8 * π * N ^ 2 ↔ (N - 1) * (N - 2) = 1 / (2 * π) := by
  have hp := Real.pi_pos
  have h1 : 0 < N - 1 := by linarith
  have h2 : 0 < N - 2 := by linarith
  have hq : (N - 1) * (N - 2) ≠ 0 := by positivity
  have hN2 : 0 < N ^ 2 := by positivity
  unfold cN
  rw [div_eq_iff hq, eq_div_iff (by positivity)]
  constructor
  · intro h
    have : N ^ 2 * (4 * π * ((N - 1) * (N - 2)) - 1) = 0 := by nlinarith [h]
    rcases mul_eq_zero.mp this with h3 | h3
    · exact absurd h3 hN2.ne'
    · nlinarith [h3]
  · intro h
    nlinarith [h, hN2]

theorem M7g_refuted : ¬ (∀ N : ℝ, 2 < N → (cN N = 8 * π * N ^ 2 ↔ (N - 1) * (N - 2) = 1 / (2 * π))) := by
  intro h
  have hp := Real.pi_pos
  obtain ⟨h2, h3, _⟩ := Nstar_props
  have h4 := (cN_eq_iff h2).mpr h3
  have h5 := (h Nstar h2).mp h4
  rw [h3] at h5
  field_simp at h5
  nlinarith

-- M7h: N* lies in (2.08, 2.09) (wrong; true: (2.0740, 2.0742)) -- false
theorem M7h_Nstar_wrong : 2.08 < Nstar := by
  have hp := Real.pi_pos
  have h1 := Real.pi_gt_d4
  have h2 := Real.pi_lt_d4
  have hq : 0 ≤ 1 + 1 / π := by positivity
  have ht2 := Real.sq_sqrt hq
  set t := Real.sqrt (1 + 1 / π) with htdef
  have ht0 : 0 ≤ t := Real.sqrt_nonneg _
  have hinv1 : 0.3183 < 1 / π := by rw [lt_div_iff₀ hp]; nlinarith
  have htl : 1.1481 < t := by nlinarith
  unfold Nstar; rw [← htdef]; linarith

theorem M7h_refuted : ¬ (2.08 < Nstar) := by
  have := Nstar_props.2.2.2.1
  intro h; linarith

-- M7i: N = 2 solves (N - 1)(N - 2) = 1/(4 pi) -- false
theorem M7i_two_solves : (2 - 1) * (2 - 2 : ℝ) = 1 / (4 * π) := by
  have hp := Real.pi_pos
  norm_num
  positivity

theorem M7i_refuted : ¬ ((2 - 1) * (2 - 2 : ℝ) = 1 / (4 * π)) := N_two_marginal

-- M7j: c(N) stays bounded as N -> 2+ (wrong: it blows up) -- false
theorem M7j_bounded : ∃ M : ℝ, ∀ N : ℝ, 2 < N → cN N ≤ M := by
  refine ⟨100, fun N hN => ?_⟩
  unfold cN
  have h1 : 0 < N - 1 := by linarith
  have h2 : 0 < N - 2 := by linarith
  rw [div_le_iff₀ (by positivity)]
  nlinarith

theorem M7j_refuted : ¬ (∃ M : ℝ, ∀ N : ℝ, 2 < N → cN N ≤ M) := by
  rintro ⟨M, hM⟩
  obtain ⟨δ, hδ, h⟩ := cN_blowup M
  have h1 := h (2 + δ / 2) (by linarith) (by linarith)
  have h2 := hM (2 + δ / 2) (by linarith)
  linarith

-- M7k: rho_Lambda A_dS = 3 F_max (wrong: 6) -- false
theorem M7k_F_wrong {L : ℝ} (hL : L ≠ 0) : (3 / (8 * π * L ^ 2)) * (4 * π * L ^ 2) = 3 * (1 / 4) := by
  have hp := Real.pi_pos
  field_simp
  ring

theorem M7k_refuted : ¬ (∀ L : ℝ, L ≠ 0 → (3 / (8 * π * L ^ 2)) * (4 * π * L ^ 2) = 3 * (1 / 4)) := by
  intro h
  have h1 := h 1 one_ne_zero
  rw [F_Lambda one_ne_zero] at h1
  norm_num at h1

-- M7l: Sigma_Lambda = 4 pi Sigma_M iff rho = a0^2 (wrong; true: rho = 4 a0^2) -- false
theorem M7l_sheet_wrong {ρ a0 : ℝ} (hρ : 0 < ρ) (ha : 0 < a0) : ρ * (1 / Real.sqrt ρ) = 4 * π * (a0 / (2 * π)) ↔ ρ = a0 ^ 2 := by
  have hp := Real.pi_pos
  have hs : 0 < Real.sqrt ρ := Real.sqrt_pos.mpr hρ
  have h2 := Real.sq_sqrt hρ.le
  have hL : ρ * (1 / Real.sqrt ρ) = Real.sqrt ρ := by
    rw [mul_one_div, div_eq_iff hs.ne']; nlinarith [h2]
  have hR : 4 * π * (a0 / (2 * π)) = 2 * a0 := by field_simp; ring
  rw [hL, hR]
  constructor
  · intro h; rw [← h2, h]; ring
  · intro h
    have : Real.sqrt ρ ^ 2 = (2 * a0) ^ 2 := by rw [h2, h]; ring
    exact (sq_eq_sq₀ hs.le (by positivity)).mp this

theorem M7l_refuted : ¬ (∀ ρ a0 : ℝ, 0 < ρ → 0 < a0 → (ρ * (1 / Real.sqrt ρ) = 4 * π * (a0 / (2 * π)) ↔ ρ = a0 ^ 2)) := by
  intro h
  have hp := Real.pi_pos
  have h1 : Real.sqrt (4:ℝ) = 2 := by
    rw [show (4:ℝ) = 2 ^ 2 by norm_num]; exact Real.sqrt_sq (by norm_num)
  have h2 := (sheet (ρ := 4) (a0 := 1) (by norm_num) one_pos).mpr (by norm_num)
  have h3 := (h 4 1 (by norm_num) one_pos).mp h2
  norm_num at h3

-- M7m: a0^2 = G rho/4 iff G m/l = 1/2 (wrong: 1/4) -- false
theorem M7m_lattice_wrong {G m l : ℝ} (hG : 0 < G) (hm : 0 < m) (hl : 0 < l) :
    (G * m / l ^ 2) ^ 2 = G * (m / l ^ 3) / 4 ↔ G * m / l = 1 / 2 := by
  have hl0 : l ≠ 0 := hl.ne'
  have hpos : 0 < G * (m / l ^ 3) := by positivity
  have e : (G * m / l ^ 2) ^ 2 = G * (m / l ^ 3) * (G * m / l) := by field_simp
  rw [e]
  constructor
  · intro h
    have : G * (m / l ^ 3) * (G * m / l - 1 / 2) = 0 := by nlinarith [h]
    rcases mul_eq_zero.mp this with h1 | h1
    · exact absurd h1 hpos.ne'
    · linarith
  · intro h; rw [h]; ring

theorem M7m_refuted : ¬ (∀ G m l : ℝ, 0 < G → 0 < m → 0 < l → ((G * m / l ^ 2) ^ 2 = G * (m / l ^ 3) / 4 ↔ G * m / l = 1 / 2)) := by
  intro h
  have h1 := ((lattice (G := 1) (m := 1 / 4) (l := 1) one_pos (by norm_num) one_pos).2).mpr (by norm_num)
  have h2 := (h 1 (1 / 4) 1 one_pos (by norm_num) one_pos).mp h1
  norm_num at h2

-- M7n: the zero-force sphere has mean density 4 rho_Lambda (wrong; true: 2) -- false
theorem M7n_thresholds_wrong {G M Λ r : ℝ} (hG : 0 < G) (hM : 0 < M) (hΛ : 0 < Λ) (h : r ^ 3 = 3 * G * M / Λ) :
    3 * M / (4 * π * r ^ 3) = 4 * (Λ / (8 * π * G)) := by
  have hp := Real.pi_pos
  rw [h]; field_simp; ring

theorem M7n_refuted : ¬ (∀ G M Λ r : ℝ, 0 < G → 0 < M → 0 < Λ → r ^ 3 = 3 * G * M / Λ →
    3 * M / (4 * π * r ^ 3) = 4 * (Λ / (8 * π * G))) := by
  intro h
  have hp := Real.pi_pos
  obtain ⟨r, hr, hr3⟩ := exists_cbrt7 (a := (3 : ℝ)) (by norm_num)
  have hh : r ^ 3 = 3 * 1 * 1 / 1 := by rw [hr3]; ring
  have h1 := h 1 1 1 r one_pos one_pos one_pos hh
  have h2 := (thresholds (G := 1) (M := 1) (Λ := 1) (r := r) one_pos one_pos one_pos).1 hh
  rw [h1] at h2
  field_simp at h2
  nlinarith

-- M7o: at N = 2 the offset integrand IS integrable -- false
theorem M7o_N2_integrable : IntegrableOn (fun x : ℝ => (1 + x / 2) ^ (-(2:ℝ)) * (2 * x)) (Ioi 0) :=
  (offset_integral (N := 2) (by norm_num)).1

theorem M7o_refuted : ¬ IntegrableOn (fun x : ℝ => (1 + x / 2) ^ (-(2:ℝ)) * (2 * x)) (Ioi 0) := offset_N2_not_integrable

-- M7p: the offset integral equals N^2/((N-1)(N-2)) (wrong: 2 N^2/(...)) -- false
theorem M7p_integral_wrong {N : ℝ} (hN : 2 < N) :
    ∫ x in Ioi (0:ℝ), (1 + x / N) ^ (-N) * (2 * x) = N ^ 2 / ((N - 1) * (N - 2)) := by
  rw [(offset_integral hN).2]
  have hN1 : N - 1 ≠ 0 := by linarith
  have hN2 : N - 2 ≠ 0 := by linarith
  unfold cN
  field_simp

theorem M7p_refuted : ¬ (∀ N : ℝ, 2 < N → ∫ x in Ioi (0:ℝ), (1 + x / N) ^ (-N) * (2 * x) = N ^ 2 / ((N - 1) * (N - 2))) := by
  intro h
  have h1 := h 3 (by norm_num)
  rw [(offset_integral (N := 3) (by norm_num)).2] at h1
  unfold cN at h1
  norm_num at h1

-- M7q: the OR shape satisfies mu_N <= x/2 (wrong; true: mu_N <= x) -- false
theorem M7q_orMu_wrong {N x : ℝ} (hN : 0 < N) (hx : 0 ≤ x) : 1 - (1 + x / N) ^ (-N) ≤ x / 2 := by
  have hu : 0 < 1 + x / N := by positivity
  have h1 : 1 + x / N ≤ Real.exp (x / N) := by linarith [Real.add_one_le_exp (x / N)]
  have h2 : (1 + x / N) ^ N ≤ (Real.exp (x / N)) ^ N := Real.rpow_le_rpow hu.le h1 hN.le
  have h3 : (Real.exp (x / N)) ^ N = Real.exp x := by
    rw [← Real.exp_mul]; congr 1; field_simp
  rw [h3] at h2
  have h4 : (Real.exp x)⁻¹ ≤ ((1 + x / N) ^ N)⁻¹ := inv_anti₀ (Real.rpow_pos_of_pos hu N) h2
  rw [← Real.exp_neg] at h4
  have h5 : (1 + x / N) ^ (-N) = ((1 + x / N) ^ N)⁻¹ := Real.rpow_neg hu.le N
  have h6 : -x + 1 ≤ Real.exp (-x) := Real.add_one_le_exp (-x)
  linarith

theorem M7q_refuted : ¬ (∀ N x : ℝ, 0 < N → 0 ≤ x → 1 - (1 + x / N) ^ (-N) ≤ x / 2) := by
  intro h
  have h1 := h 1 (1 / 2) one_pos (by norm_num)
  have h2 : (1 + (1 / 2 : ℝ) / 1) ^ (-(1:ℝ)) = 2 / 3 := by
    rw [Real.rpow_neg_one]; norm_num
  rw [h2] at h1
  norm_num at h1

-- M7r: the offset coefficient of admissible shapes is bounded above -- false
theorem M7r_bounded : ∃ M : ℝ, ∀ N : ℝ, 2 < N → ∫ x in Set.Ioi (0:ℝ), (1 - (1 - (1 + x / N) ^ (-N))) * (2 * x) ≤ M := by
  refine ⟨100, fun N hN => ?_⟩
  have e : (fun x : ℝ => (1 - (1 - (1 + x / N) ^ (-N))) * (2 * x)) = fun x => (1 + x / N) ^ (-N) * (2 * x) := by funext x; ring
  rw [e, (offset_integral hN).2]
  unfold cN
  have h1 : 0 < N - 1 := by linarith
  have h2 : 0 < N - 2 := by linarith
  rw [div_le_iff₀ (by positivity)]
  nlinarith

theorem M7r_refuted : ¬ (∃ M : ℝ, ∀ N : ℝ, 2 < N → ∫ x in Set.Ioi (0:ℝ), (1 - (1 - (1 + x / N) ^ (-N))) * (2 * x) ≤ M) := by
  rintro ⟨M, hM⟩
  obtain ⟨N, hN, _, _, _, hgt⟩ := no_upper_bound M
  exact absurd (hM N hN) (not_le.mpr hgt)


#print axioms M7a_refuted
#print axioms M7b_refuted
#print axioms M7c_refuted
#print axioms M7d_refuted
#print axioms M7e_refuted
#print axioms M7f_refuted
#print axioms M7g_refuted
#print axioms M7h_refuted
#print axioms M7i_refuted
#print axioms M7j_refuted
#print axioms M7k_refuted
#print axioms M7l_refuted
#print axioms M7m_refuted
#print axioms M7n_refuted
#print axioms M7o_refuted
#print axioms M7p_refuted
#print axioms M7q_refuted
#print axioms M7r_refuted
#print axioms M7a_offset_wrong
#print axioms M7b_cZ_wrong
#print axioms M7c_rational_exists
#print axioms M7d_bathtub_wrong
#print axioms M7e_bathtub_nohyp
#print axioms M7f_sharp_wrong
#print axioms M7g_cN_wrong
#print axioms M7h_Nstar_wrong
#print axioms M7i_two_solves
#print axioms M7j_bounded
#print axioms M7k_F_wrong
#print axioms M7l_sheet_wrong
#print axioms M7m_lattice_wrong
#print axioms M7n_thresholds_wrong
#print axioms M7o_N2_integrable
#print axioms M7p_integral_wrong
#print axioms M7q_orMu_wrong
#print axioms M7r_bounded
