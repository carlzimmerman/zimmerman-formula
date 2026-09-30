import Mathlib
import P2_sds_surface_gravity

/-! MUTATE controls for P2_sds_surface_gravity.lean: each `M2*` is a FALSE variant re-using the true proof script with one wrong constant or
threshold (must FAIL to compile); each `M2*_refuted` proves the negation from the true theorems plus an explicit instance (must COMPILE). -/

open Real SdS

theorem exists_cbrt {a : ℝ} (ha : 0 < a) : ∃ s : ℝ, 0 < s ∧ s ^ 3 = a := by
  refine ⟨a ^ ((1:ℝ) / 3), Real.rpow_pos_of_pos ha _, ?_⟩
  rw [← Real.rpow_natCast, ← Real.rpow_mul ha.le]; norm_num

-- M2a: kappa_b = (1 - r^2/L^2)/(2 r) at a root of f (the naive formula; the true one is (1 - 3 r^2/L^2)/(2 r)) -- false
theorem M2a_kappa_naive {M L r : ℝ} (hr : 0 < r) (hL : L ≠ 0) (hf : f M L r = 0) :
    (2 * M / r ^ 2 - 2 * r / L ^ 2) / 2 = (1 - r ^ 2 / L ^ 2) / (2 * r) := by
  have hr0 : r ≠ 0 := hr.ne'
  unfold f at hf
  have hM : 2 * M = r * (1 - r ^ 2 / L ^ 2) := by
    field_simp at hf ⊢
    nlinarith [hf]
  rw [hM]; field_simp; ring

theorem M2a_refuted : ¬ (∀ (M L r : ℝ), 0 < r → L ≠ 0 → f M L r = 0 →
    (2 * M / r ^ 2 - 2 * r / L ^ 2) / 2 = (1 - r ^ 2 / L ^ 2) / (2 * r)) := by
  intro h
  have hf : f (3 / 16) 1 (1 / 2) = 0 := by unfold f; norm_num
  have h1 := h (3 / 16) 1 (1 / 2) (by norm_num) one_ne_zero hf
  have h2 := (kappa_at_horizon (M := 3 / 16) (L := 1) (r := 1 / 2) (by norm_num) one_ne_zero hf).1
  rw [h1] at h2
  norm_num at h2

-- M2b: the brief's root x = -1/Z + sqrt(1 + 1/Z^2) solves kappa_b = H/Z -- false
theorem M2b_root_wrong {Z x : ℝ} (hZ : 0 < Z) (hx : 0 < x) :
    kb x = 1 / Z ↔ x = -1 / Z + Real.sqrt (1 + 1 / Z ^ 2) := by
  obtain ⟨hs, hs2, hs1⟩ := sqrt_facts hZ
  rw [kb_iff_poly hZ hx]
  constructor
  · intro h1
    have h2 : (3 * Z * x + 1) ^ 2 = Real.sqrt (1 + 3 * Z ^ 2) ^ 2 := by rw [hs2]; nlinarith [h1]
    have h3 : 3 * Z * x + 1 = Real.sqrt (1 + 3 * Z ^ 2) := by
      have hpos : 0 < 3 * Z * x + 1 := by positivity
      nlinarith [sq_nonneg (3 * Z * x + 1 - Real.sqrt (1 + 3 * Z ^ 2)), sq_nonneg (3 * Z * x + 1 + Real.sqrt (1 + 3 * Z ^ 2))]
    field_simp; linarith
  · intro h
    have hq : 0 < 1 + 1 / Z ^ 2 := by positivity
    have := Real.sq_sqrt hq.le
    have hZ0 : Z ≠ 0 := hZ.ne'
    field_simp at h ⊢
    nlinarith [this]

theorem M2b_refuted : ¬ (∀ (Z x : ℝ), 0 < Z → 0 < x → (kb x = 1 / Z ↔ x = -1 / Z + Real.sqrt (1 + 1 / Z ^ 2))) := by
  intro h
  have hk : kb (1 / 3) = 1 / 1 := by unfold kb; norm_num
  have h1 := (h 1 (1 / 3) one_pos (by norm_num)).mp hk
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have h3 : Real.sqrt (1 + 1 / (1:ℝ) ^ 2) = Real.sqrt 2 := by norm_num
  rw [h3] at h1
  nlinarith [h2]

-- M2c: the black-hole root is the '+' root (sqrt(1 + 3 Z^2) + 1)/(3 Z) (that is the cosmological root) -- false
theorem M2c_root_plus {Z x : ℝ} (hZ : 0 < Z) (hx : 0 < x) :
    kb x = 1 / Z ↔ x = (Real.sqrt (1 + 3 * Z ^ 2) + 1) / (3 * Z) := by
  obtain ⟨hs, hs2, hs1⟩ := sqrt_facts hZ
  have hZ0 : Z ≠ 0 := hZ.ne'
  rw [kb_iff_poly hZ hx]
  constructor
  · intro h1
    have h2 : (3 * Z * x + 1) ^ 2 = Real.sqrt (1 + 3 * Z ^ 2) ^ 2 := by rw [hs2]; nlinarith [h1]
    have h3 : 3 * Z * x + 1 = Real.sqrt (1 + 3 * Z ^ 2) := by
      have hpos : 0 < 3 * Z * x + 1 := by positivity
      nlinarith [sq_nonneg (3 * Z * x + 1 - Real.sqrt (1 + 3 * Z ^ 2)), sq_nonneg (3 * Z * x + 1 + Real.sqrt (1 + 3 * Z ^ 2))]
    field_simp; linarith
  · intro h
    have h3 : 3 * Z * x = Real.sqrt (1 + 3 * Z ^ 2) + 1 := by rw [h]; field_simp
    have h4 : 3 * Z * (Z * (1 - 3 * x ^ 2) - 2 * x) = 0 := by nlinarith [h3, hs2]
    rcases mul_eq_zero.mp h4 with h5 | h5
    · exfalso; have : 0 < 3 * Z := by positivity
      linarith
    · linarith

theorem M2c_refuted : ¬ (∀ (Z x : ℝ), 0 < Z → 0 < x → (kb x = 1 / Z ↔ x = (Real.sqrt (1 + 3 * Z ^ 2) + 1) / (3 * Z))) := by
  intro h
  have hk : kb (1 / 3) = 1 / 1 := by unfold kb; norm_num
  have h1 := (h 1 (1 / 3) one_pos (by norm_num)).mp hk
  have h2 : Real.sqrt (1 + 3 * (1:ℝ) ^ 2) = 2 := by
    rw [show (1 + 3 * (1:ℝ) ^ 2) = 2 ^ 2 by norm_num]; exact Real.sqrt_sq (by norm_num)
  rw [h2] at h1
  norm_num at h1

-- M2d: the mass of a horizon exceeds the Nariai mass: Mm x >= MN -- false
theorem M2d_mass_wrong {x : ℝ} (hx : 0 ≤ x) : MN ≤ Mm x := by
  have h : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have h0 : 0 ≤ Real.sqrt 3 := Real.sqrt_nonneg 3
  unfold Mm MN
  have key : Real.sqrt 3 / 9 - x * (1 - x ^ 2) / 2 = (x - Real.sqrt 3 / 3) ^ 2 * (x + 2 * (Real.sqrt 3 / 3)) / 2 := by
    have : Real.sqrt 3 ^ 3 = 3 * Real.sqrt 3 := by nlinarith [h]
    nlinarith [h, this]
  have : 0 ≤ (x - Real.sqrt 3 / 3) ^ 2 * (x + 2 * (Real.sqrt 3 / 3)) / 2 := by positivity
  linarith

theorem M2d_refuted : ¬ (∀ x : ℝ, 0 ≤ x → MN ≤ Mm x) := by
  intro h
  have h1 := h (1 / 2) (by norm_num)
  have h3l : 1.732 < Real.sqrt 3 := (Real.lt_sqrt (by norm_num)).mpr (by norm_num)
  unfold Mm MN at h1
  norm_num at h1
  nlinarith [h3l]

-- M2e: the cosmological root has positive mass iff Z > 2 (wrong threshold; true: Z > 1) -- false
theorem M2e_threshold_wrong {Z : ℝ} (hZ : 0 < Z) : xc Z < 1 ↔ 2 < Z := by
  obtain ⟨hs, hs2, hs1⟩ := sqrt_facts hZ
  have hZ0 : Z ≠ 0 := hZ.ne'
  unfold xc
  rw [div_lt_one (by positivity)]
  constructor
  · intro h
    have hlt : Real.sqrt (1 + 3 * Z ^ 2) < 3 * Z - 1 := by linarith
    have hsq : Real.sqrt (1 + 3 * Z ^ 2) ^ 2 < (3 * Z - 1) ^ 2 := by
      have h0 : 0 ≤ Real.sqrt (1 + 3 * Z ^ 2) := hs.le
      exact pow_lt_pow_left₀ hlt h0 (by norm_num)
    rw [hs2] at hsq
    nlinarith
  · intro h
    have : Real.sqrt (1 + 3 * Z ^ 2) < 3 * Z - 1 := by
      rw [Real.sqrt_lt' (by linarith)]
      nlinarith
    linarith

theorem M2e_refuted : ¬ (∀ Z : ℝ, 0 < Z → (xc Z < 1 ↔ 2 < Z)) := by
  intro h
  have h1 := (xc_lt_one_iff (Z := 3 / 2) (by norm_num)).mpr (by norm_num)
  have h2 := (h (3 / 2) (by norm_num)).mp h1
  norm_num at h2

-- M2f: BH normalisation kappa_b^2 >= 4 H^2 f(r*) (wrong constant; true: 3) -- false
theorem M2f_bh_wrong {x s : ℝ} (hx : 0 < x) (hs : 0 < s) (hc : x ^ 3 - x + 2 * s ^ 3 = 0) (h3 : 3 * x ^ 2 < 1) :
    4 * (1 - 3 * s ^ 2) ≤ kb x ^ 2 := by
  obtain ⟨hxs, hD⟩ := bh_x_lt_s hx hs hc h3
  have hx0 : x ≠ 0 := hx.ne'
  have hQ : 0 ≤ (x ^ 2 + x * s + s ^ 2) ^ 2 - 4 * x ^ 3 * (x + 2 * s) := by
    nlinarith [mul_pos hx hs, hxs]
  have hP : x ^ 2 * ((1 - 3 * x ^ 2) ^ 2 - 16 * x ^ 2 * (1 - 3 * s ^ 2))
      = 4 * (s - x) ^ 2 * ((x ^ 2 + x * s + s ^ 2) ^ 2 - 4 * x ^ 3 * (x + 2 * s)) := by
    linear_combination (-2 * s ^ 3 + 17 * x ^ 3 - x) * hc
  have hP0 : 0 ≤ (1 - 3 * x ^ 2) ^ 2 - 16 * x ^ 2 * (1 - 3 * s ^ 2) := by
    have h4 : 0 ≤ x ^ 2 * ((1 - 3 * x ^ 2) ^ 2 - 16 * x ^ 2 * (1 - 3 * s ^ 2)) := by rw [hP]; positivity
    nlinarith [h4, sq_pos_of_pos hx]
  unfold kb
  rw [div_pow, le_div_iff₀ (by positivity)]
  nlinarith [hP0]

theorem M2f_refuted : ¬ (∀ x s : ℝ, 0 < x → 0 < s → x ^ 3 - x + 2 * s ^ 3 = 0 → 3 * x ^ 2 < 1 →
    4 * (1 - 3 * s ^ 2) ≤ kb x ^ 2) := by
  intro h
  obtain ⟨s, hs, hs3⟩ := exists_cbrt (a := (3 : ℝ) / 16) (by norm_num)
  have hc : (1 / 2 : ℝ) ^ 3 - 1 / 2 + 2 * s ^ 3 = 0 := by rw [hs3]; norm_num
  have h1 := h (1 / 2) s (by norm_num) hs hc (by norm_num)
  have hkb : kb (1 / 2) = 1 / 4 := by unfold kb; norm_num
  rw [hkb] at h1
  -- s^3 = 3/16 gives s > 0.5724 hence 4(1 - 3 s^2) < 1/16
  have hs_lb : 0.5724 < s := by
    by_contra hcon
    have hcon := not_lt.mp hcon
    have : s ^ 3 ≤ 0.5724 ^ 3 := pow_le_pow_left₀ hs.le hcon 3
    nlinarith [hs3]
  nlinarith [hs_lb, sq_nonneg s]

-- M2g: BH-normalised cosmological surface gravity kappa_c^2 <= 2 H^2 f(r*) (wrong constant; true: 3) -- false
theorem M2g_bh_c_wrong {y s : ℝ} (hy : 0 < y) (hs : 0 < s) (hc : y ^ 3 - y + 2 * s ^ 3 = 0) (h3 : 1 < 3 * y ^ 2) :
    kc y ^ 2 ≤ 2 * (1 - 3 * s ^ 2) := by
  have hy0 : y ≠ 0 := hy.ne'
  have h1 : s ^ 3 < y ^ 3 := by nlinarith [mul_pos hy (sub_pos.2 h3)]
  have hsy : s < y := lt_of_pow_lt_pow_left₀ 3 hy.le h1
  have hP : y ^ 2 * (8 * y ^ 2 * (1 - 3 * s ^ 2) - (3 * y ^ 2 - 1) ^ 2)
      = 4 * (y - s) ^ 2 * ((y - s) * (s ^ 3 + 3 * s ^ 2 * y + 6 * s * y ^ 2 + 2 * y ^ 3)) := by
    linear_combination (2 * s ^ 3 - 17 * y ^ 3 + y) * hc
  have hpos : 0 ≤ (y - s) ^ 2 * ((y - s) * (s ^ 3 + 3 * s ^ 2 * y + 6 * s * y ^ 2 + 2 * y ^ 3)) := by
    have : 0 ≤ y - s := by linarith
    positivity
  have h4 : 0 ≤ y ^ 2 * (8 * y ^ 2 * (1 - 3 * s ^ 2) - (3 * y ^ 2 - 1) ^ 2) := by rw [hP]; nlinarith [hpos]
  have h5 : 0 ≤ 8 * y ^ 2 * (1 - 3 * s ^ 2) - (3 * y ^ 2 - 1) ^ 2 := nonneg_of_mul_nonneg_right h4 (by positivity)
  unfold kc
  rw [div_pow, div_le_iff₀ (by positivity)]
  nlinarith [h5]

theorem M2g_refuted : ¬ (∀ y s : ℝ, 0 < y → 0 < s → y ^ 3 - y + 2 * s ^ 3 = 0 → 1 < 3 * y ^ 2 →
    kc y ^ 2 ≤ 2 * (1 - 3 * s ^ 2)) := by
  intro h
  obtain ⟨s, hs, hs3⟩ := exists_cbrt (a := (24 : ℝ) / 125) (by norm_num)
  have hc : (3 / 5 : ℝ) ^ 3 - 3 / 5 + 2 * s ^ 3 = 0 := by rw [hs3]; norm_num
  have h1 := h (3 / 5) s (by norm_num) hs hc (by norm_num)
  have hkc : kc (3 / 5) = 1 / 15 := by unfold kc; norm_num
  rw [hkc] at h1
  have hs_lb : 0.5767 < s := by
    by_contra hcon
    have hcon := not_lt.mp hcon
    have : s ^ 3 ≤ 0.5767 ^ 3 := pow_le_pow_left₀ hs.le hcon 3
    nlinarith [hs3]
  nlinarith [hs_lb, sq_nonneg s]

-- M2h: the puzzle horizon radius x_b lies in (0.53, 0.54) (wrong; true: (0.5226, 0.5227)) -- false
theorem M2h_xb_wrong : 0.53 < xb Zpuz ∧ xb Zpuz < 0.54 := by
  obtain ⟨hZl, hZu⟩ := Zpuz_bounds
  have hZ : 0 < Zpuz := by linarith
  obtain ⟨hx, hx3⟩ := xb_black_hole hZ
  have hpoly := (kb_iff_poly hZ hx).mp ((kb_eq_iff hZ hx).mpr rfl)
  set x := xb Zpuz with hxdef
  constructor
  · by_contra hcon
    have hcon := not_lt.mp hcon
    have h1 : 1 - 3 * (0.53:ℝ) ^ 2 ≤ 1 - 3 * x ^ 2 := by nlinarith
    have h2 : Zpuz * (1 - 3 * (0.53:ℝ) ^ 2) ≤ Zpuz * (1 - 3 * x ^ 2) := mul_le_mul_of_nonneg_left h1 hZ.le
    nlinarith
  · linarith

theorem M2h_refuted : ¬ (0.53 < xb Zpuz ∧ xb Zpuz < 0.54) := by
  intro h
  have := xb_puzzle_bounds.2
  linarith [h.1]

-- M2i: at the a0-horizon A_b Lambda = 32 pi^2 (the puzzle's area relation would hold there) -- false
theorem M2i_area_wrong {Z : ℝ} (hZ : 0 < Z) : (4 * π * xb Z ^ 2) * 3 = 32 * π ^ 2 := by
  have hp := Real.pi_pos
  obtain ⟨hx, hx3⟩ := xb_black_hole hZ
  have h1 : 12 * π * xb Z ^ 2 < 4 * π := by nlinarith
  nlinarith

theorem M2i_refuted : ¬ (∀ Z : ℝ, 0 < Z → (4 * π * xb Z ^ 2) * 3 = 32 * π ^ 2) := by
  intro h
  exact (area_Lambda_at_a0_horizon (Z := 1) one_pos).2.2.2 (h 1 one_pos)

-- M2j: M*/M_N > 0.99 at the puzzle Z (true: 0.986 < ratio < 0.988) -- false
theorem M2j_ratio_wrong : 0.99 < Mm (xb Zpuz) / MN := by
  obtain ⟨hxl, hxu⟩ := xb_puzzle_bounds
  have h3l : 1.732 < Real.sqrt 3 := (Real.lt_sqrt (by norm_num)).mpr (by norm_num)
  set x := xb Zpuz
  have hMN : 0 < MN := by unfold MN; positivity
  have hg1 : 0.3798 < x * (1 - x ^ 2) := by nlinarith [mul_pos (sub_pos.2 hxl) (sub_pos.2 hxu)]
  unfold Mm
  rw [lt_div_iff₀ hMN]; unfold MN; nlinarith

theorem M2j_refuted : ¬ (0.99 < Mm (xb Zpuz) / MN) := by
  intro h
  have := puzzle_mass_ratio_bounds.2
  linarith

-- M2k: kb is strictly INCREASING on (0, infinity) -- false
theorem M2k_kb_mono : StrictMonoOn kb (Set.Ioi 0) := by
  intro x hx y hy hxy
  simp only [Set.mem_Ioi] at hx hy
  have h : kb y - kb x = (y - x) * (1 / (2 * x * y) + 3 / 2) := by
    unfold kb; field_simp; ring
  have : 0 < kb y - kb x := by rw [h]; have : 0 < y - x := by linarith
                               positivity
  linarith

theorem M2k_refuted : ¬ StrictMonoOn kb (Set.Ioi 0) := by
  intro h
  have h1 := h (Set.mem_Ioi.mpr (by norm_num : (0:ℝ) < 1 / 2)) (Set.mem_Ioi.mpr (by norm_num : (0:ℝ) < 1)) (by norm_num)
  have h2 : kb (1 / 2) = 1 / 4 := by unfold kb; norm_num
  have h3 : kb 1 = -1 := by unfold kb; norm_num
  rw [h2, h3] at h1
  norm_num at h1

-- M2l: the maximum of Mm is sqrt 3/10 (true: sqrt 3/9 = 1/(3 sqrt 3)) -- false
theorem M2l_max_wrong {x : ℝ} (hx : 0 ≤ x) : Mm x ≤ Real.sqrt 3 / 10 := by
  have h : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have h0 : 0 ≤ Real.sqrt 3 := Real.sqrt_nonneg 3
  unfold Mm
  have key : Real.sqrt 3 / 10 - x * (1 - x ^ 2) / 2 = (x - Real.sqrt 3 / 3) ^ 2 * (x + 2 * (Real.sqrt 3 / 3)) / 2 := by
    have : Real.sqrt 3 ^ 3 = 3 * Real.sqrt 3 := by nlinarith [h]
    nlinarith [h, this]
  have : 0 ≤ (x - Real.sqrt 3 / 3) ^ 2 * (x + 2 * (Real.sqrt 3 / 3)) / 2 := by positivity
  linarith

theorem M2l_refuted : ¬ (∀ x : ℝ, 0 ≤ x → Mm x ≤ Real.sqrt 3 / 10) := by
  intro h
  have h1 := h (Real.sqrt 3 / 3) (by positivity)
  have h3 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have h0 : 0 < Real.sqrt 3 := Real.sqrt_pos.mpr (by norm_num)
  unfold Mm at h1
  nlinarith [h3, h0]


-- M2m: dimensionful BH-normalised bound kappa_b^2 >= 4 H^2 f(r*) (wrong constant; true: 3) -- false
theorem M2m_bh_dim_wrong {M L r s : ℝ} (hL : 0 < L) (hr : 0 < r) (hs : 0 < s) (hM : M = s ^ 3 * L) (hf : f M L r = 0)
    (h3 : 3 * r ^ 2 < L ^ 2) :
    4 * (1 / L) ^ 2 * f M L (s * L) ≤ ((2 * M / r ^ 2 - 2 * r / L ^ 2) / 2) ^ 2 := by
  have hL0 : L ≠ 0 := hL.ne'
  have hr0 : r ≠ 0 := hr.ne'
  obtain ⟨_, hfs⟩ := rstar_props hL hs hM
  rw [hfs]
  have hk := (kappa_at_horizon hr hL0 hf).1
  rw [hk]
  set x := r / L with hx
  have hxpos : 0 < x := by positivity
  have hrx : r = L * x := by rw [hx]; field_simp
  have hx3 : 3 * x ^ 2 < 1 := by
    rw [hx, div_pow, ← mul_div_assoc, div_lt_one (by positivity)]; exact h3
  have hc : x ^ 3 - x + 2 * s ^ 3 = 0 := by
    unfold f at hf
    subst hM
    rw [hrx] at hf
    field_simp at hf
    have : L ^ 2 * (x ^ 3 - x + 2 * s ^ 3) = 0 := by nlinarith [hf]
    rcases mul_eq_zero.mp this with h | h
    · exact absurd h (pow_ne_zero 2 hL0)
    · exact h
  have hb := (bh_bound_b hxpos hs hc hx3).le
  have hkb : (1 - 3 * r ^ 2 / L ^ 2) / (2 * r) = kb x / L := by
    rw [hrx]; exact kb_dimensionful hL hxpos
  rw [hkb]
  have hL2 : 0 < L ^ 2 := by positivity
  have e1 : 4 * (1 / L) ^ 2 * (1 - 3 * s ^ 2) = 4 * (1 - 3 * s ^ 2) / L ^ 2 := by field_simp
  have e3 : (kb x / L) ^ 2 = kb x ^ 2 / L ^ 2 := div_pow _ _ _
  rw [e1, e3]
  exact div_le_div_of_nonneg_right hb hL2.le

theorem M2m_refuted : ¬ (∀ M L r s : ℝ, 0 < L → 0 < r → 0 < s → M = s ^ 3 * L → f M L r = 0 → 3 * r ^ 2 < L ^ 2 →
    4 * (1 / L) ^ 2 * f M L (s * L) ≤ ((2 * M / r ^ 2 - 2 * r / L ^ 2) / 2) ^ 2) := by
  intro h
  obtain ⟨s, hs, hs3⟩ := exists_cbrt (a := (3 : ℝ) / 16) (by norm_num)
  have hM : (3 / 16 : ℝ) = s ^ 3 * 1 := by rw [hs3]; ring
  have hf : f (3 / 16) 1 (1 / 2) = 0 := by unfold f; norm_num
  have h1 := h (3 / 16) 1 (1 / 2) s one_pos (by norm_num) hs hM hf (by norm_num)
  obtain ⟨_, hfs⟩ := rstar_props (M := 3 / 16) (L := 1) (s := s) one_pos hs hM
  rw [hfs] at h1
  have hk : (2 * (3 / 16 : ℝ) / (1 / 2) ^ 2 - 2 * (1 / 2) / 1 ^ 2) / 2 = 1 / 4 := by norm_num
  rw [hk] at h1
  have hs_lb : 0.5724 < s := by
    by_contra hcon
    have hcon := not_lt.mp hcon
    have : s ^ 3 ≤ 0.5724 ^ 3 := pow_le_pow_left₀ hs.le hcon 3
    nlinarith [hs3]
  nlinarith [hs_lb, sq_nonneg s]

-- M2n: dimensionful cosmological bound kappa_c^2 <= 2 H^2 f(r*) (wrong constant; true: 3) -- false
theorem M2n_bh_c_dim_wrong {M L r s : ℝ} (hL : 0 < L) (hr : 0 < r) (hs : 0 < s) (hM : M = s ^ 3 * L) (hf : f M L r = 0)
    (h3 : L ^ 2 < 3 * r ^ 2) :
    (-((2 * M / r ^ 2 - 2 * r / L ^ 2) / 2)) ^ 2 ≤ 2 * (1 / L) ^ 2 * f M L (s * L) := by
  have hL0 : L ≠ 0 := hL.ne'
  have hr0 : r ≠ 0 := hr.ne'
  obtain ⟨_, hfs⟩ := rstar_props hL hs hM
  rw [hfs]
  have hk := (kappa_at_horizon hr hL0 hf).2
  rw [hk]
  set x := r / L with hx
  have hxpos : 0 < x := by positivity
  have hrx : r = L * x := by rw [hx]; field_simp
  have hx3 : 1 < 3 * x ^ 2 := by
    rw [hx, div_pow, ← mul_div_assoc, one_lt_div (by positivity)]; exact h3
  have hc : x ^ 3 - x + 2 * s ^ 3 = 0 := by
    unfold f at hf
    subst hM
    rw [hrx] at hf
    field_simp at hf
    have : L ^ 2 * (x ^ 3 - x + 2 * s ^ 3) = 0 := by nlinarith [hf]
    rcases mul_eq_zero.mp this with h | h
    · exact absurd h (pow_ne_zero 2 hL0)
    · exact h
  obtain ⟨_, hb0, _⟩ := bh_bounds_c hxpos hs hc hx3
  have hb := hb0.le
  have hkc : (3 * r ^ 2 / L ^ 2 - 1) / (2 * r) = kc x / L := by
    rw [hrx]; unfold kc; field_simp
  rw [hkc]
  have hL2 : 0 < L ^ 2 := by positivity
  have e2 : 2 * (1 / L) ^ 2 * (1 - 3 * s ^ 2) = 2 * (1 - 3 * s ^ 2) / L ^ 2 := by field_simp
  have e3 : (kc x / L) ^ 2 = kc x ^ 2 / L ^ 2 := div_pow _ _ _
  rw [e2, e3]
  exact div_le_div_of_nonneg_right hb hL2.le

theorem M2n_refuted : ¬ (∀ M L r s : ℝ, 0 < L → 0 < r → 0 < s → M = s ^ 3 * L → f M L r = 0 → L ^ 2 < 3 * r ^ 2 →
    (-((2 * M / r ^ 2 - 2 * r / L ^ 2) / 2)) ^ 2 ≤ 2 * (1 / L) ^ 2 * f M L (s * L)) := by
  intro h
  obtain ⟨s, hs, hs3⟩ := exists_cbrt (a := (24 : ℝ) / 125) (by norm_num)
  have hM : (24 / 125 : ℝ) = s ^ 3 * 1 := by rw [hs3]; ring
  have hf : f (24 / 125) 1 (3 / 5) = 0 := by unfold f; norm_num
  have h1 := h (24 / 125) 1 (3 / 5) s one_pos (by norm_num) hs hM hf (by norm_num)
  obtain ⟨_, hfs⟩ := rstar_props (M := 24 / 125) (L := 1) (s := s) one_pos hs hM
  rw [hfs] at h1
  have hk : -((2 * (24 / 125 : ℝ) / (3 / 5) ^ 2 - 2 * (3 / 5) / 1 ^ 2) / 2) = 1 / 15 := by norm_num
  rw [hk] at h1
  have hs_lb : 0.5767 < s := by
    by_contra hcon
    have hcon := not_lt.mp hcon
    have : s ^ 3 ≤ 0.5767 ^ 3 := pow_le_pow_left₀ hs.le hcon 3
    nlinarith [hs3]
  nlinarith [hs_lb, sq_nonneg s]

#print axioms M2a_refuted
#print axioms M2b_refuted
#print axioms M2c_refuted
#print axioms M2d_refuted
#print axioms M2e_refuted
#print axioms M2f_refuted
#print axioms M2g_refuted
#print axioms M2h_refuted
#print axioms M2i_refuted
#print axioms M2j_refuted
#print axioms M2k_refuted
#print axioms M2l_refuted
#print axioms M2m_refuted
#print axioms M2n_refuted
#print axioms M2a_kappa_naive
#print axioms M2b_root_wrong
#print axioms M2c_root_plus
#print axioms M2d_mass_wrong
#print axioms M2e_threshold_wrong
#print axioms M2f_bh_wrong
#print axioms M2g_bh_c_wrong
#print axioms M2h_xb_wrong
#print axioms M2i_area_wrong
#print axioms M2j_ratio_wrong
#print axioms M2k_kb_mono
#print axioms M2l_max_wrong
#print axioms M2m_bh_dim_wrong
#print axioms M2n_bh_c_dim_wrong
