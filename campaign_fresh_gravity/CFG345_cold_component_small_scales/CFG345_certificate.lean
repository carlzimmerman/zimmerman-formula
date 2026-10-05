import Mathlib

/-! CFG345 certificate. Wave field: M_1/2 = A m22^(-4/3) (HBG, T^2 = 1/2) <= M_need  <=>  m22^4 * M_need^3 >= A^3.
Road S: M_J(z_eq) = B M^-6 (M in eV) <= M_need  <=>  M^6 * M_need >= B. A = 5.35307e+10, B = 2.70961e+17, M_need = 3.83275e+07 Msun,
all rounded outward to 4 significant figures. Values from cfg345_small_scales_results.json and CFG344's JSON. -/

/-- m = 2e-20 eV (record window floor): M_1/2 > M_need -/
theorem wave_floor_2e20_suppresses : (200 : ℚ)^4 * (38330000 : ℚ)^3 < (53530000000 : ℚ)^3 := by norm_num

/-- m22 = 228 still above M_need -/
theorem wave_228_fails : (228 : ℚ)^4 * (38330000 : ℚ)^3 < (53530000000 : ℚ)^3 := by norm_num

/-- bound: m >= 2.29e-20 eV suffices -/
theorem wave_229_passes : (53540000000 : ℚ)^3 ≤ (229 : ℚ)^4 * (38320000 : ℚ)^3 := by norm_num

/-- L383 floor 2e-19 eV passes -/
theorem wave_L383_floor_passes : (53540000000 : ℚ)^3 ≤ (2000 : ℚ)^4 * (38320000 : ℚ)^3 := by norm_num

/-- road S at its G-DUST minimum 4.24 eV suppresses -/
theorem roadS_gdust_min_suppresses : (424 / 100 : ℚ)^6 * (38330000 : ℚ) < (270900000000000000 : ℚ) := by norm_num

/-- road S bound: M >= 44 eV suffices -/
theorem roadS_44eV_passes : (271000000000000000 : ℚ) ≤ (44 : ℚ)^6 * (38320000 : ℚ) := by norm_num

/-- the record's own onset requirement 3.3 keV passes -/
theorem roadS_onset_passes : (271000000000000000 : ℚ) ≤ (3300 : ℚ)^6 * (38320000 : ℚ) := by norm_num
