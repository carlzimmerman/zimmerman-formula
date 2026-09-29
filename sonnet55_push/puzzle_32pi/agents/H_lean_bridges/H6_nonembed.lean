import Mathlib

open Real Set

/-- the framework's Z = 1/(a0 L) = sqrt(32 pi/3) (a0 = H/Z, H = 1/L) -/
noncomputable def Zpuz : ℝ := Real.sqrt (32 * π / 3)

theorem Zpuz_sq : Zpuz ^ 2 = 32 * π / 3 := by
  have := Real.pi_pos
  unfold Zpuz; rw [Real.sq_sqrt (by positivity)]

theorem Zpuz_pos : 0 < Zpuz := by
  have := Real.pi_pos
  unfold Zpuz; exact Real.sqrt_pos.mpr (by positivity)

theorem Zpuz_gt_two : 2 < Zpuz := by
  have hp := Real.pi_gt_d2
  have h := Zpuz_sq
  have hz := Zpuz_pos
  nlinarith [h, hz]

/-! ### the puzzle's horizon vs its own de Sitter radius -/

/-- r_s = 1/(2 a0) with a0 = 1/(Z L) is Z L/2 -/
theorem rs_eq {Z L : ℝ} (hZ : 0 < Z) (hL : 0 < L) : 1 / (2 * (1 / (Z * L))) = Z * L / 2 := by
  field_simp

/-- r_s > L  <->  Z > 2  (and r_s <= L <-> Z <= 2: the embeddability criterion) -/
theorem rs_gt_L_iff {Z L : ℝ} (hL : 0 < L) : L < Z * L / 2 ↔ 2 < Z := by
  constructor
  · intro h; nlinarith
  · intro h; nlinarith

theorem rs_le_L_iff {Z L : ℝ} (hL : 0 < L) : Z * L / 2 ≤ L ↔ Z ≤ 2 := by
  constructor
  · intro h; nlinarith
  · intro h; nlinarith

/-- the puzzle's horizon does not fit inside its own de Sitter radius: r_s > L -/
theorem puzzle_rs_gt_L {L : ℝ} (hL : 0 < L) : L < Zpuz * L / 2 :=
  (rs_gt_L_iff hL).mpr Zpuz_gt_two

/-- Mass M_s = r_s/2 = Z L/4 (Schwarzschild r_s = 2M); Nariai mass L/(3 sqrt 3): M_s/M_N = 3 sqrt3 Z/4 -/
theorem mass_ratio_formula {Z L : ℝ} (hL : 0 < L) :
    (Z * L / 4) / (L / (3 * Real.sqrt 3)) = 3 * Real.sqrt 3 * Z / 4 := by
  have : Real.sqrt 3 ≠ 0 := by positivity
  have : L ≠ 0 := hL.ne'
  field_simp

/-- for the puzzle Z: M_s/M_N = 3 sqrt(32 pi)/4 > 7.5 > 1 -/
theorem mass_ratio_puzzle : 3 * Real.sqrt 3 * Zpuz / 4 = 3 * Real.sqrt (32 * π) / 4 ∧ 7.5 < 3 * Real.sqrt (32 * π) / 4 := by
  have hp := Real.pi_gt_d2
  have hp0 := Real.pi_pos
  have e : Real.sqrt 3 * Zpuz = Real.sqrt (32 * π) := by
    unfold Zpuz
    rw [← Real.sqrt_mul (by norm_num)]
    congr 1; ring
  refine ⟨?_, ?_⟩
  · have : 3 * Real.sqrt 3 * Zpuz / 4 = 3 * (Real.sqrt 3 * Zpuz) / 4 := by ring
    rw [this, e]
  · have h10 : (10 : ℝ) < Real.sqrt (32 * π) := by
      rw [show (10:ℝ) = Real.sqrt 100 by rw [show (100:ℝ) = 10 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]]
      exact Real.sqrt_lt_sqrt (by norm_num) (by linarith)
    linarith

/-- M_s = r_s/2 = Z L/4 exceeds the Nariai mass L/(3 sqrt 3) -/
theorem puzzle_mass_exceeds_nariai {L : ℝ} (hL : 0 < L) : L / (3 * Real.sqrt 3) < Zpuz * L / 4 := by
  have h := mass_ratio_formula (Z := Zpuz) hL
  have h2 := mass_ratio_puzzle
  have hb : 0 < L / (3 * Real.sqrt 3) := by positivity
  have h1 : 1 < (Zpuz * L / 4) / (L / (3 * Real.sqrt 3)) := by rw [h, h2.1]; linarith [h2.2]
  exact (one_lt_div hb).mp h1

/-- no positive horizon of Schwarzschild-de Sitter when M > L/(3 sqrt 3): r f(r) = r - 2M - r^3/L^2 < 0 for all r > 0 -/
theorem sds_no_horizon {L M : ℝ} (hL : 0 < L) (hM : L / (3 * Real.sqrt 3) < M) :
    ∀ r : ℝ, 0 < r → r - 2 * M - r ^ 3 / L ^ 2 < 0 := by
  intro r hr
  have hs3 : 0 < Real.sqrt 3 := by positivity
  have hs2 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  set c := L / Real.sqrt 3 with hc
  have hc0 : 0 < c := by positivity
  have hL2 : L ^ 2 = 3 * c ^ 2 := by
    rw [hc, div_pow, hs2]; field_simp
  have hMc : c / 3 < M := by
    have : L / (3 * Real.sqrt 3) = c / 3 := by rw [hc]; field_simp
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

/-- Schwarzschild-de Sitter with M_s = r_s/2 = Z L/4 (the puzzle's black hole) has no horizon at all -/
theorem puzzle_no_sds_horizon {L : ℝ} (hL : 0 < L) :
    ∀ r : ℝ, 0 < r → r - 2 * (Zpuz * L / 4) - r ^ 3 / L ^ 2 < 0 :=
  sds_no_horizon hL (puzzle_mass_exceeds_nariai hL)

/-- the same statement as "f(r) = 1 - 2M/r - r^2/L^2 < 0 for every r > 0" -/
theorem sds_f_negative {L M : ℝ} (hL : 0 < L) (hM : L / (3 * Real.sqrt 3) < M) :
    ∀ r : ℝ, 0 < r → 1 - 2 * M / r - r ^ 2 / L ^ 2 < 0 := by
  intro r hr
  have h := sds_no_horizon hL hM r hr
  have : 1 - 2 * M / r - r ^ 2 / L ^ 2 = (r - 2 * M - r ^ 3 / L ^ 2) / r := by
    field_simp
  rw [this]
  exact div_neg_of_neg_of_pos h hr

/-- control: for 0 < M <= L/(3 sqrt 3) a horizon does exist (intermediate value theorem) -/
theorem sds_horizon_exists {L M : ℝ} (hL : 0 < L) (hM0 : 0 < M) (hM : M ≤ L / (3 * Real.sqrt 3)) :
    ∃ r : ℝ, 0 < r ∧ r - 2 * M - r ^ 3 / L ^ 2 = 0 := by
  have hs3 : 0 < Real.sqrt 3 := by positivity
  have hs2 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  set c := L / Real.sqrt 3 with hc
  have hc0 : 0 < c := by positivity
  have hL2 : L ^ 2 = 3 * c ^ 2 := by
    rw [hc, div_pow, hs2]; field_simp
  have hMc : M ≤ c / 3 := by
    have : L / (3 * Real.sqrt 3) = c / 3 := by rw [hc]; field_simp
    linarith
  set p : ℝ → ℝ := fun r => r - 2 * M - r ^ 3 / L ^ 2 with hp
  have hcont : ContinuousOn p (Icc 0 c) := by
    apply Continuous.continuousOn
    simp only [hp]; fun_prop
  have p0 : p 0 = -2 * M := by simp [hp]
  have pc : p c = 2 * c / 3 - 2 * M := by
    simp only [hp]; rw [hL2]; field_simp; ring
  have h0 : (0:ℝ) ∈ Icc (p 0) (p c) := by
    constructor <;> [skip; skip] <;> nlinarith [p0, pc]
  obtain ⟨r, hr, hpr⟩ := intermediate_value_Icc hc0.le hcont h0
  refine ⟨r, ?_, hpr⟩
  rcases hr.1.eq_or_lt with h | h
  · exfalso; rw [← h] at hpr; rw [p0] at hpr; linarith
  · exact h

/-- area ratio A_s/A_dS = 4 pi (Z L/2)^2 / (4 pi L^2) = Z^2/4 = 8 pi/3 > 1 -/
theorem area_ratio_puzzle {L : ℝ} (hL : 0 < L) :
    (4 * π * (Zpuz * L / 2) ^ 2) / (4 * π * L ^ 2) = 8 * π / 3 ∧ 1 < 8 * π / 3 := by
  have hp := Real.pi_gt_d2
  have hp0 := Real.pi_pos
  refine ⟨?_, by linarith⟩
  have : L ≠ 0 := hL.ne'
  have h := Zpuz_sq
  field_simp
  nlinarith [h]

/-- in the framework's normalisation Z(kappa) = sqrt(8 pi/3)/kappa (kappa = 1/2 gives sqrt(32 pi/3)):
embeddable (Z <= 2)  <->  kappa >= sqrt(2 pi/3) ~ 1.447 ; kappa = 1/2 and kappa = 1 are both NOT embeddable -/
theorem embeddable_iff_kappa {κ : ℝ} (hκ : 0 < κ) :
    Real.sqrt (8 * π / 3) / κ ≤ 2 ↔ Real.sqrt (2 * π / 3) ≤ κ := by
  have hp := Real.pi_pos
  have e : Real.sqrt (8 * π / 3) = 2 * Real.sqrt (2 * π / 3) := by
    rw [show 8 * π / 3 = 2 ^ 2 * (2 * π / 3) by ring, Real.sqrt_mul (by norm_num), Real.sqrt_sq (by norm_num)]
  rw [e, div_le_iff₀ hκ]
  constructor <;> intro h <;> linarith

theorem kappa_one_not_embeddable : 2 < Real.sqrt (8 * π / 3) / 1 := by
  have hp := Real.pi_gt_d2
  rw [div_one]
  rw [show (2:ℝ) = Real.sqrt 4 by rw [show (4:ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]]
  exact Real.sqrt_lt_sqrt (by norm_num) (by linarith)

theorem kappa_half_gives_Zpuz : Real.sqrt (8 * π / 3) / (1 / 2) = Zpuz := by
  have hp := Real.pi_pos
  unfold Zpuz
  have : 32 * π / 3 = 2 ^ 2 * (8 * π / 3) := by ring
  rw [this, Real.sqrt_mul (by norm_num), Real.sqrt_sq (by norm_num), one_div, div_inv_eq_mul]
  ring

/-! ### Israel thin-wall: 1/R^2 >= max(H_in^2, H_out^2) -/

/-- junction: A - B = x = 4 pi sigma > 0 with A^2 = 1/R^2 - H_in^2, B^2 = 1/R^2 - H_out^2 -/
theorem israel_closed_form {Hi Ho x A B : ℝ} (hx : 0 < x) (hAB : A - B = x) (h : Hi ^ 2 + A ^ 2 = Ho ^ 2 + B ^ 2) :
    A = ((Ho ^ 2 - Hi ^ 2) / x + x) / 2 := by
  have h1 : x * (A + B) = Ho ^ 2 - Hi ^ 2 := by
    have : A ^ 2 - B ^ 2 = Ho ^ 2 - Hi ^ 2 := by linarith
    rw [← this, ← hAB]; ring
  have h2 : A + B = (Ho ^ 2 - Hi ^ 2) / x := by
    rw [eq_div_iff hx.ne']; linarith
  linarith

theorem israel_bound {Hi Ho A B u : ℝ} (hu_i : u = Hi ^ 2 + A ^ 2) (hu_o : u = Ho ^ 2 + B ^ 2) :
    max (Hi ^ 2) (Ho ^ 2) ≤ u := by
  refine max_le ?_ ?_
  · rw [hu_i]; nlinarith [sq_nonneg A]
  · rw [hu_o]; nlinarith [sq_nonneg B]

/-- pure tension: 1/R^2 = H^2 + (2 pi sigma)^2 -/
theorem israel_pure_tension {H σ A B : ℝ} (hσ : 0 < σ) (hAB : A - B = 4 * π * σ)
    (h : H ^ 2 + A ^ 2 = H ^ 2 + B ^ 2) : H ^ 2 + A ^ 2 = H ^ 2 + (2 * π * σ) ^ 2 := by
  have hp := Real.pi_pos
  have hx : 0 < 4 * π * σ := by positivity
  have h1 := israel_closed_form (Hi := H) (Ho := H) hx hAB h
  have : A = 2 * π * σ := by rw [h1]; simp; ring
  rw [this]

/-- a real wall of pure tension has 1/R >= H: no wall has the acceleration a0 = H/Z < H (Z > 1); it would need sigma^2 < 0 -/
theorem no_wall_at_a0 {H Z σ : ℝ} (hH : 0 < H) (hZ : 1 < Z) :
    H ^ 2 + (2 * π * σ) ^ 2 ≠ (H / Z) ^ 2 := by
  intro h
  have hZ0 : 0 < Z := by linarith
  have h1 : (H / Z) ^ 2 < H ^ 2 := by
    rw [div_pow]
    have : Z ^ 2 > 1 := by nlinarith
    rw [div_lt_iff₀ (by positivity)]
    nlinarith [sq_pos_of_pos hH]
  nlinarith [sq_nonneg (2 * π * σ)]

theorem no_wall_at_a0_puzzle {H σ : ℝ} (hH : 0 < H) : H ^ 2 + (2 * π * σ) ^ 2 ≠ (H / Zpuz) ^ 2 :=
  no_wall_at_a0 hH (by linarith [Zpuz_gt_two])

#print axioms Zpuz_gt_two
#print axioms puzzle_rs_gt_L
#print axioms rs_gt_L_iff
#print axioms rs_le_L_iff
#print axioms mass_ratio_formula
#print axioms mass_ratio_puzzle
#print axioms puzzle_mass_exceeds_nariai
#print axioms sds_no_horizon
#print axioms puzzle_no_sds_horizon
#print axioms sds_f_negative
#print axioms sds_horizon_exists
#print axioms area_ratio_puzzle
#print axioms embeddable_iff_kappa
#print axioms kappa_one_not_embeddable
#print axioms kappa_half_gives_Zpuz
#print axioms israel_closed_form
#print axioms israel_bound
#print axioms israel_pure_tension
#print axioms no_wall_at_a0
#print axioms no_wall_at_a0_puzzle
