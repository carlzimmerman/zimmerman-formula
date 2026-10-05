import Mathlib

/-! CFG344 certificate: decisive offset inequalities (rule S, per-object R_acc, primary z_f = 8, z_inf = 2).
Values from cfg344_accretion_results.json / _MUTATE_results.json, rounded outward to 1e-6. Interval reasoning only. -/

theorem abs_le_of_bounds {s lo hi T : ℚ} (h1 : lo ≤ s) (h2 : s ≤ hi) (h3 : -T ≤ lo) (h4 : hi ≤ T) : |s| ≤ T :=
  abs_le.mpr ⟨le_trans h3 h1, le_trans h2 h4⟩

/-- zf8_zinf2 nfw canonical: |s_UFD| = |-0.024498| ≤ 2 e_law = 0.171953 -/
theorem ufd_within_main_nfw_canonical (s : ℚ) (h1 : (-24499 / 1000000 : ℚ) ≤ s) (h2 : s ≤ (-12249 / 500000 : ℚ)) : |s| ≤ (171953 / 1000000 : ℚ) :=
  abs_le_of_bounds h1 h2 (by norm_num) (by norm_num)

theorem other_P2a_main_nfw_canonical (z : ℚ) (h1 : (318899 / 1000000 : ℚ) ≤ z) (h2 : z ≤ (3189 / 10000 : ℚ)) : |z| < 2 :=
  abs_lt.mpr ⟨by linarith [show (-2 : ℚ) < (318899 / 1000000 : ℚ) by norm_num], by linarith [show (3189 / 10000 : ℚ) < (2 : ℚ) by norm_num]⟩

theorem other_P2b_main_nfw_canonical (z : ℚ) (h1 : (192517 / 250000 : ℚ) ≤ z) (h2 : z ≤ (770069 / 1000000 : ℚ)) : |z| < 2 :=
  abs_lt.mpr ⟨by linarith [show (-2 : ℚ) < (192517 / 250000 : ℚ) by norm_num], by linarith [show (770069 / 1000000 : ℚ) < (2 : ℚ) by norm_num]⟩

theorem other_P2c_main_nfw_canonical (z : ℚ) (h1 : (704509 / 1000000 : ℚ) ≤ z) (h2 : z ≤ (70451 / 100000 : ℚ)) : |z| < 2 :=
  abs_lt.mpr ⟨by linarith [show (-2 : ℚ) < (704509 / 1000000 : ℚ) by norm_num], by linarith [show (70451 / 100000 : ℚ) < (2 : ℚ) by norm_num]⟩

theorem other_P2d_main_nfw_canonical (z : ℚ) (h1 : (-149541 / 250000 : ℚ) ≤ z) (h2 : z ≤ (-598163 / 1000000 : ℚ)) : |z| < 2 :=
  abs_lt.mpr ⟨by linarith [show (-2 : ℚ) < (-149541 / 250000 : ℚ) by norm_num], by linarith [show (-598163 / 1000000 : ℚ) < (2 : ℚ) by norm_num]⟩

/-- zf8_zinf2 nfw alt: |s_UFD| = |-0.024317| ≤ 2 e_law = 0.171664 -/
theorem ufd_within_main_nfw_alt (s : ℚ) (h1 : (-24317 / 1000000 : ℚ) ≤ s) (h2 : s ≤ (-6079 / 250000 : ℚ)) : |s| ≤ (10729 / 62500 : ℚ) :=
  abs_le_of_bounds h1 h2 (by norm_num) (by norm_num)

theorem other_P2a_main_nfw_alt (z : ℚ) (h1 : (11259 / 125000 : ℚ) ≤ z) (h2 : z ≤ (90073 / 1000000 : ℚ)) : |z| < 2 :=
  abs_lt.mpr ⟨by linarith [show (-2 : ℚ) < (11259 / 125000 : ℚ) by norm_num], by linarith [show (90073 / 1000000 : ℚ) < (2 : ℚ) by norm_num]⟩

theorem other_P2b_main_nfw_alt (z : ℚ) (h1 : (551181 / 1000000 : ℚ) ≤ z) (h2 : z ≤ (275591 / 500000 : ℚ)) : |z| < 2 :=
  abs_lt.mpr ⟨by linarith [show (-2 : ℚ) < (551181 / 1000000 : ℚ) by norm_num], by linarith [show (275591 / 500000 : ℚ) < (2 : ℚ) by norm_num]⟩

theorem other_P2c_main_nfw_alt (z : ℚ) (h1 : (226099 / 500000 : ℚ) ≤ z) (h2 : z ≤ (452199 / 1000000 : ℚ)) : |z| < 2 :=
  abs_lt.mpr ⟨by linarith [show (-2 : ℚ) < (226099 / 500000 : ℚ) by norm_num], by linarith [show (452199 / 1000000 : ℚ) < (2 : ℚ) by norm_num]⟩

theorem other_P2d_main_nfw_alt (z : ℚ) (h1 : (-13211 / 15625 : ℚ) ≤ z) (h2 : z ≤ (-845503 / 1000000 : ℚ)) : |z| < 2 :=
  abs_lt.mpr ⟨by linarith [show (-2 : ℚ) < (-13211 / 15625 : ℚ) by norm_num], by linarith [show (-845503 / 1000000 : ℚ) < (2 : ℚ) by norm_num]⟩

/-- zf8_zinf2 sis canonical: |s_UFD| = |-0.136450| ≤ 2 e_law = 0.171953 -/
theorem ufd_within_main_sis_canonical (s : ℚ) (h1 : (-136451 / 1000000 : ℚ) ≤ s) (h2 : s ≤ (-2729 / 20000 : ℚ)) : |s| ≤ (171953 / 1000000 : ℚ) :=
  abs_le_of_bounds h1 h2 (by norm_num) (by norm_num)

theorem other_P2a_main_sis_canonical (z : ℚ) (h1 : (318899 / 1000000 : ℚ) ≤ z) (h2 : z ≤ (3189 / 10000 : ℚ)) : |z| < 2 :=
  abs_lt.mpr ⟨by linarith [show (-2 : ℚ) < (318899 / 1000000 : ℚ) by norm_num], by linarith [show (3189 / 10000 : ℚ) < (2 : ℚ) by norm_num]⟩

theorem other_P2b_main_sis_canonical (z : ℚ) (h1 : (744261 / 1000000 : ℚ) ≤ z) (h2 : z ≤ (372131 / 500000 : ℚ)) : |z| < 2 :=
  abs_lt.mpr ⟨by linarith [show (-2 : ℚ) < (744261 / 1000000 : ℚ) by norm_num], by linarith [show (372131 / 500000 : ℚ) < (2 : ℚ) by norm_num]⟩

theorem other_P2c_main_sis_canonical (z : ℚ) (h1 : (592301 / 1000000 : ℚ) ≤ z) (h2 : z ≤ (296151 / 500000 : ℚ)) : |z| < 2 :=
  abs_lt.mpr ⟨by linarith [show (-2 : ℚ) < (592301 / 1000000 : ℚ) by norm_num], by linarith [show (296151 / 500000 : ℚ) < (2 : ℚ) by norm_num]⟩

theorem other_P2d_main_sis_canonical (z : ℚ) (h1 : (-149541 / 250000 : ℚ) ≤ z) (h2 : z ≤ (-598163 / 1000000 : ℚ)) : |z| < 2 :=
  abs_lt.mpr ⟨by linarith [show (-2 : ℚ) < (-149541 / 250000 : ℚ) by norm_num], by linarith [show (-598163 / 1000000 : ℚ) < (2 : ℚ) by norm_num]⟩

/-- zf8_zinf2 sis alt: |s_UFD| = |-0.127885| ≤ 2 e_law = 0.171664 -/
theorem ufd_within_main_sis_alt (s : ℚ) (h1 : (-25577 / 200000 : ℚ) ≤ s) (h2 : s ≤ (-31971 / 250000 : ℚ)) : |s| ≤ (10729 / 62500 : ℚ) :=
  abs_le_of_bounds h1 h2 (by norm_num) (by norm_num)

theorem other_P2a_main_sis_alt (z : ℚ) (h1 : (11259 / 125000 : ℚ) ≤ z) (h2 : z ≤ (90073 / 1000000 : ℚ)) : |z| < 2 :=
  abs_lt.mpr ⟨by linarith [show (-2 : ℚ) < (11259 / 125000 : ℚ) by norm_num], by linarith [show (90073 / 1000000 : ℚ) < (2 : ℚ) by norm_num]⟩

theorem other_P2b_main_sis_alt (z : ℚ) (h1 : (267999 / 500000 : ℚ) ≤ z) (h2 : z ≤ (535999 / 1000000 : ℚ)) : |z| < 2 :=
  abs_lt.mpr ⟨by linarith [show (-2 : ℚ) < (267999 / 500000 : ℚ) by norm_num], by linarith [show (535999 / 1000000 : ℚ) < (2 : ℚ) by norm_num]⟩

theorem other_P2c_main_sis_alt (z : ℚ) (h1 : (39527 / 100000 : ℚ) ≤ z) (h2 : z ≤ (395271 / 1000000 : ℚ)) : |z| < 2 :=
  abs_lt.mpr ⟨by linarith [show (-2 : ℚ) < (39527 / 100000 : ℚ) by norm_num], by linarith [show (395271 / 1000000 : ℚ) < (2 : ℚ) by norm_num]⟩

theorem other_P2d_main_sis_alt (z : ℚ) (h1 : (-13211 / 15625 : ℚ) ≤ z) (h2 : z ≤ (-845503 / 1000000 : ℚ)) : |z| < 2 :=
  abs_lt.mpr ⟨by linarith [show (-2 : ℚ) < (-13211 / 15625 : ℚ) by norm_num], by linarith [show (-845503 / 1000000 : ℚ) < (2 : ℚ) by norm_num]⟩

/-- zf8_zinf8 nfw canonical: s_UFD = +0.255293 > 2 e_law = 0.171953 -/
theorem ufd_outside_mutate_nfw_canonical (s : ℚ) (h1 : (255293 / 1000000 : ℚ) ≤ s) : (85977 / 500000 : ℚ) < s :=
  lt_of_lt_of_le (by norm_num) h1

/-- zf8_zinf8 nfw alt: s_UFD = +0.276531 > 2 e_law = 0.171664 -/
theorem ufd_outside_mutate_nfw_alt (s : ℚ) (h1 : (27653 / 100000 : ℚ) ≤ s) : (34333 / 200000 : ℚ) < s :=
  lt_of_lt_of_le (by norm_num) h1

/-- zf8_zinf8 sis canonical: s_UFD = +0.315443 > 2 e_law = 0.171953 -/
theorem ufd_outside_mutate_sis_canonical (s : ℚ) (h1 : (157721 / 500000 : ℚ) ≤ s) : (85977 / 500000 : ℚ) < s :=
  lt_of_lt_of_le (by norm_num) h1

/-- zf8_zinf8 sis alt: s_UFD = +0.295421 > 2 e_law = 0.171664 -/
theorem ufd_outside_mutate_sis_alt (s : ℚ) (h1 : (295421 / 1000000 : ℚ) ≤ s) : (34333 / 200000 : ℚ) < s :=
  lt_of_lt_of_le (by norm_num) h1

