import Mathlib

/-!
# CFG347 -- certificates for the theta_b-reading switch (slaved and dynamical)

* T1 mirror lemma: a gate W with W'(0) = 0 that drops between 0 and 1 has W'' < 0 somewhere in (0,1).
* T2 slaved ghost: with W'' = -a < 0 the compressive kinetic coefficient rho + B W'' k^2/T is negative above k_g.
* T3/T3d gyroscopic health: the R3 dispersion (A - w)(b - w) = G w has a non-negative discriminant and only
  positive roots above the Jeans scale; T4: below it, every root obeys w >= A >= -Gamma^2 (growth <= Jeans).
* T5 fidelity bound: a <= 10% shift of the gas mode forces G <= b/9 + A/10; T5n its contrapositive.
* T6 a luminal switch (c_sigma = c) with any trigger coupling g > 0 has a strictly superluminal characteristic.
* T7 luminal range: M <= N H and N H r < 3.89 c imply ell = c/M > r/3.89 (the switch cannot resolve r).
* T8 FRW-off neighbourhood; T8n the numeric margin 3 H0 c / a0 > 17.
-/

open Set

theorem T1_mirror (W W' W'' : ℝ → ℝ) (hW : ∀ x, HasDerivAt W (W' x) x)
    (hW' : ∀ x, HasDerivAt W' (W'' x) x) (h0 : W' 0 = 0) (hdrop : W 1 < W 0) :
    ∃ x ∈ Ioo (0:ℝ) 1, W'' x < 0 := by
  obtain ⟨c, hc, hcW⟩ := exists_hasDerivAt_eq_slope W W' (by norm_num : (0:ℝ) < 1)
    (fun x _ => (hW x).continuousAt.continuousWithinAt) (fun x _ => hW x)
  have hneg : W' c < 0 := by rw [hcW]; apply div_neg_of_neg_of_pos <;> linarith
  obtain ⟨d, hd, hdW⟩ := exists_hasDerivAt_eq_slope W' W'' hc.1
    (fun x _ => (hW' x).continuousAt.continuousWithinAt) (fun x _ => hW' x)
  refine ⟨d, ⟨hd.1, lt_trans hd.2 hc.2⟩, ?_⟩
  rw [hdW, h0]; apply div_neg_of_neg_of_pos <;> linarith [hd.1, hc.1]

theorem T2_slaved_ghost (ρ B a T k : ℝ) (_hB : 0 < B) (_ha : 0 < a) (hT : 0 < T)
    (hk : ρ * T < B * a * k ^ 2) : ρ + B * (-a) * k ^ 2 / T < 0 := by
  have : ρ + B * (-a) * k ^ 2 / T = (ρ * T - B * a * k ^ 2) / T := by field_simp; ring
  rw [this]; exact div_neg_of_neg_of_pos (by linarith) hT

theorem T3_roots_positive (A b G w : ℝ) (hA : 0 < A) (hb : 0 < b) (hG : 0 ≤ G)
    (hroot : (A - w) * (b - w) = G * w) : 0 < w := by
  by_contra h; push Not at h
  have h1 : A * b ≤ (A - w) * (b - w) := by nlinarith
  have h2 : G * w ≤ 0 := mul_nonpos_of_nonneg_of_nonpos hG h
  nlinarith [mul_pos hA hb]

theorem T3d_discriminant (A b G : ℝ) (hA : 0 < A) (hb : 0 < b) (hG : 0 ≤ G) :
    0 ≤ (A + b + G) ^ 2 - 4 * A * b := by
  nlinarith [sq_nonneg (A - b), mul_nonneg hG (by linarith : (0:ℝ) ≤ A + b), sq_nonneg G]

theorem T4_jeans_bound (A b G w : ℝ) (hA : A < 0) (hb : 0 < b) (hG : 0 ≤ G)
    (hroot : (A - w) * (b - w) = G * w) : A ≤ w := by
  by_contra h; push Not at h
  have h1 : 0 < (A - w) * (b - w) := mul_pos (by linarith) (by linarith)
  have h2 : G * w ≤ 0 := mul_nonpos_of_nonneg_of_nonpos hG (by linarith)
  linarith

theorem T5_fidelity (A b G w : ℝ) (hA : 0 < A) (hb : 0 ≤ b) (hG : 0 ≤ G)
    (hroot : (A - w) * (b - w) = G * w) (hfid : |w - A| ≤ A / 10) : G ≤ b / 9 + A / 10 := by
  have hw : 9 * A / 10 ≤ w := by linarith [(abs_le.mp hfid).1]
  have hwpos : 0 < w := by linarith
  have h1 : G * w ≤ A / 10 * (b + w) := by
    rw [← hroot]
    calc (A - w) * (b - w) ≤ |(A - w) * (b - w)| := le_abs_self _
      _ = |A - w| * |b - w| := abs_mul _ _
      _ ≤ A / 10 * (b + w) := by
        apply mul_le_mul _ _ (abs_nonneg _) (by linarith)
        · rw [abs_sub_comm]; exact hfid
        · rw [abs_le]; constructor <;> linarith
  have h2 : A / 10 * (b + w) ≤ (b / 9 + A / 10) * w := by nlinarith [mul_le_mul_of_nonneg_left hw hb]
  exact le_of_mul_le_mul_right (le_trans h1 h2) hwpos

theorem T5n_no_fidelity (A b G w : ℝ) (hA : 0 < A) (hb : 0 ≤ b) (hG : 0 ≤ G)
    (hroot : (A - w) * (b - w) = G * w) (hbig : b / 9 + A / 10 < G) : A / 10 < |w - A| := by
  by_contra h; push Not at h
  linarith [T5_fidelity A b G w hA hb hG hroot h]

theorem T6_luminal_superluminal (cs2 c2 g : ℝ) (hcs : 0 < cs2) (hlt : cs2 < c2) (hg : 0 < g) :
    ∃ v, c2 < v ∧ (cs2 - v) * (c2 - v) = g * v := by
  set p : ℝ → ℝ := fun v => (cs2 - v) * (c2 - v) - g * v with hp
  have hcont : ContinuousOn p (Icc c2 (cs2 + c2 + g)) := (by continuity : Continuous p).continuousOn
  have hlo : p c2 < 0 := by simp only [hp]; nlinarith
  have hhi : 0 < p (cs2 + c2 + g) := by simp only [hp]; nlinarith
  obtain ⟨v, hv, hpv⟩ := intermediate_value_Icc (by linarith) hcont ⟨hlo.le, hhi.le⟩
  refine ⟨v, lt_of_le_of_ne hv.1 ?_, by simp only [hp] at hpv; linarith⟩
  rintro rfl; linarith

theorem T7_luminal_range (c M H r N : ℝ) (hM : 0 < M) (hH : 0 < H) (hr : 0 < r) (hN : 0 < N)
    (hMle : M ≤ N * H) (hc : N * H * r < 3.89 * c) : r / 3.89 < c / M := by
  rw [lt_div_iff₀ hM]
  have h1 : r / 3.89 * M ≤ r / 3.89 * (N * H) := mul_le_mul_of_nonneg_left hMle (by positivity)
  have h2 : r / 3.89 * (N * H) < c := by
    have e : r / 3.89 * (N * H) = N * H * r / 3.89 := by ring
    rw [e, div_lt_iff₀ (by norm_num)]; linarith
  linarith

theorem T8_frw_off (f : ℝ → ℝ) (hf : ∀ s, 1 ≤ s → f s = 0) (s d : ℝ) (hs : 17 ≤ s) (hd : |d| ≤ 16) :
    f (s + d) = 0 := hf _ (by linarith [(abs_le.mp hd).1])

theorem T8n_frw_margin (H0 a0 : ℝ) (hH : 2.18e-18 ≤ H0) (ha : 0 < a0) (ha' : a0 ≤ 1.128e-10) :
    17 < 3 * H0 * 299792458 / a0 := by
  rw [lt_div_iff₀ ha]; nlinarith

#print axioms T1_mirror
#print axioms T5_fidelity
#print axioms T6_luminal_superluminal
#print axioms T8n_frw_margin
