import Mathlib
import P5_ext_thermo

/-! MUTATE controls for P5_ext_thermo.lean: each `M5*` is a FALSE variant re-using the true proof script with one wrong constant
(must FAIL to compile); each `M5*_refuted` proves the negation from the true theorems plus an explicit instance (must COMPILE). -/

open Real ExtThermo

-- M5a: dM/dP = 4 pi r^3 (wrong thermodynamic volume; true: 4 pi r^3/3) -- false
theorem M5a_V_wrong {P r : ℝ} : HasDerivAt (fun P => Mext r P) (4 * π * r ^ 3) P := by
  unfold Mext
  have h := ((((hasDerivAt_id P).const_mul (4 * π)).mul_const (r ^ 3)).div_const 3).const_add (r / 2)
  simpa using h

theorem M5a_refuted : ¬ (∀ P r : ℝ, HasDerivAt (fun P => Mext r P) (4 * π * r ^ 3) P) := by
  intro h
  have hp := Real.pi_pos
  have h1 := (h 0 1).unique (first_law_P (P := 0) (r := 1))
  unfold Vth at h1
  nlinarith

-- M5b: Smarr M = 2 T S - P V (wrong: -2 P V) -- false
theorem M5b_smarr_wrong {P r : ℝ} (hr : r ≠ 0) : Mext r P = 2 * Ttemp r P * Sent r - P * Vth r := by
  have hp := Real.pi_pos
  unfold Mext Ttemp Sent Vth
  field_simp
  ring

theorem M5b_refuted : ¬ (∀ P r : ℝ, r ≠ 0 → Mext r P = 2 * Ttemp r P * Sent r - P * Vth r) := by
  intro h
  have hp := Real.pi_pos
  have h1 := h 1 1 one_ne_zero
  have h2 := smarr (P := 1) (r := 1) one_ne_zero
  have h3 : Vth 1 = 4 * π / 3 := by unfold Vth; ring
  rw [h1] at h2
  rw [h3] at h2
  nlinarith

-- M5c: |P| V/M = r^2/L^2 = 4 pi/3 <=> G rho r^2 = 1 (wrong; true: 8 pi/3) -- false
theorem M5c_ratio_wrong {L r : ℝ} (hL : L ≠ 0) : r ^ 2 / L ^ 2 = 4 * π / 3 ↔ (3 / (8 * π * L ^ 2)) * r ^ 2 = 1 := by
  have hp := Real.pi_pos
  have hL2 : L ^ 2 ≠ 0 := pow_ne_zero 2 hL
  rw [div_eq_iff hL2]
  constructor
  · intro h; rw [h]; field_simp
  · intro h; field_simp at h; nlinarith [h]

theorem M5c_refuted : ¬ (∀ L r : ℝ, L ≠ 0 → (r ^ 2 / L ^ 2 = 4 * π / 3 ↔ (3 / (8 * π * L ^ 2)) * r ^ 2 = 1)) := by
  intro h
  have hp := Real.pi_pos
  have hr : Real.sqrt (8 * π / 3) ^ 2 = 8 * π / 3 := Real.sq_sqrt (by positivity)
  have h1 : (Real.sqrt (8 * π / 3)) ^ 2 / (1:ℝ) ^ 2 = 8 * π / 3 := by rw [hr]; ring
  have h2 := ((flat_probe_ratios (L := 1) (r := Real.sqrt (8 * π / 3)) one_ne_zero
    (Real.sqrt_pos.mpr (by positivity)).ne').2.2.1).mp h1
  have h3 := (h 1 (Real.sqrt (8 * π / 3)) one_ne_zero).mpr h2
  rw [h1] at h3
  nlinarith

-- M5d: kappa_b^2/|P| = pi (1 - X)^2/X (wrong: 2 pi) -- false
theorem M5d_kappa_wrong {L r : ℝ} (hL : L ≠ 0) (hr : r ≠ 0) :
    ((1 - 3 * r ^ 2 / L ^ 2) / (2 * r)) ^ 2 / (3 / (8 * π * L ^ 2)) = π * (1 - 3 * r ^ 2 / L ^ 2) ^ 2 / (3 * r ^ 2 / L ^ 2) := by
  have hp := Real.pi_pos
  field_simp
  ring

theorem M5d_refuted : ¬ (∀ L r : ℝ, L ≠ 0 → r ≠ 0 →
    ((1 - 3 * r ^ 2 / L ^ 2) / (2 * r)) ^ 2 / (3 / (8 * π * L ^ 2)) = π * (1 - 3 * r ^ 2 / L ^ 2) ^ 2 / (3 * r ^ 2 / L ^ 2)) := by
  intro h
  have hp := Real.pi_pos
  have h1 := h 1 (1 / 2) one_ne_zero (by norm_num)
  have h2 := kappa_sq_over_absP (L := 1) (r := 1 / 2) one_ne_zero (by norm_num)
  rw [h1] at h2
  field_simp at h2
  nlinarith

-- M5e: Gibbs M - T S = (r/4)(1 + 3 r^2/L^2) (wrong: 1 + r^2/L^2) -- false
theorem M5e_gibbs_wrong {L r : ℝ} (hL : L ≠ 0) (hr : r ≠ 0) :
    Mext r (-(3 / (8 * π * L ^ 2))) - Ttemp r (-(3 / (8 * π * L ^ 2))) * Sent r = (r / 4) * (1 + 3 * r ^ 2 / L ^ 2) := by
  have hp := Real.pi_pos
  unfold Mext Ttemp Sent
  field_simp
  ring

theorem M5e_refuted : ¬ (∀ L r : ℝ, L ≠ 0 → r ≠ 0 →
    Mext r (-(3 / (8 * π * L ^ 2))) - Ttemp r (-(3 / (8 * π * L ^ 2))) * Sent r = (r / 4) * (1 + 3 * r ^ 2 / L ^ 2)) := by
  intro h
  have h1 := h 1 1 one_ne_zero one_ne_zero
  have h2 := Gibbs_b (L := 1) (r := 1) one_ne_zero one_ne_zero
  rw [h1] at h2
  norm_num at h2

-- M5f: kappa_b = H at x = 1/2 (wrong; true: x = 1/3) -- false
theorem M5f_bath_wrong {x : ℝ} (hx : 0 < x) : (1 - 3 * x ^ 2) / (2 * x) = 1 ↔ x = 1 / 2 := by
  rw [div_eq_one_iff_eq (by positivity)]
  constructor
  · intro h
    have : (3 * x - 1) * (x + 1) = 0 := by nlinarith [h]
    rcases mul_eq_zero.mp this with h1 | h1
    · linarith
    · linarith
  · intro h; rw [h]; norm_num

theorem M5f_refuted : ¬ (∀ x : ℝ, 0 < x → ((1 - 3 * x ^ 2) / (2 * x) = 1 ↔ x = 1 / 2)) := by
  intro h
  have h1 := (bath_point (x := 1 / 3) (by norm_num)).mpr rfl
  have h2 := (h (1 / 3) (by norm_num)).mp h1
  norm_num at h2

-- M5g: a rational X solves 8 pi (1 - X)^2 = X -- false (irrational_pi)
theorem M5g_rational_x_exists : ∃ q : ℚ, 8 * π * (1 - (q : ℝ)) ^ 2 = q := by
  refine ⟨0, ?_⟩
  norm_num

theorem M5g_refuted : ¬ (∃ q : ℚ, 8 * π * (1 - (q : ℝ)) ^ 2 = q) := by
  rintro ⟨q, hq⟩
  exact puzzle_no_rational_x q hq

-- M5h: T = kappa/pi (wrong: kappa/(2 pi)) at the SdS pressure -- false
theorem M5h_T_wrong {L r : ℝ} (hL : L ≠ 0) (hr : r ≠ 0) :
    Ttemp r (-(3 / (8 * π * L ^ 2))) = ((1 - 3 * r ^ 2 / L ^ 2) / (2 * r)) / π := by
  have hp := Real.pi_pos
  unfold Ttemp
  field_simp
  ring

theorem M5h_refuted : ¬ (∀ L r : ℝ, L ≠ 0 → r ≠ 0 → Ttemp r (-(3 / (8 * π * L ^ 2))) = ((1 - 3 * r ^ 2 / L ^ 2) / (2 * r)) / π) := by
  intro h
  have hp := Real.pi_pos
  have h1 := h 1 (1 / 2) one_ne_zero (by norm_num)
  have h2 := T_eq_kappa (L := 1) (r := 1 / 2) one_ne_zero (by norm_num)
  rw [h1] at h2
  field_simp at h2
  nlinarith

-- M5i: U = M - P V = r (wrong: r/2) -- false
theorem M5i_U_wrong {P r : ℝ} : Mext r P - P * Vth r = r := by
  unfold Mext Vth; ring

theorem M5i_refuted : ¬ (∀ P r : ℝ, Mext r P - P * Vth r = r) := by
  intro h
  have h1 := h 0 2
  rw [U_eq] at h1
  norm_num at h1

-- M5j: dM/dr = T dS/dr with dS/dr = pi r (wrong: 2 pi r) -- false
theorem M5j_TdS_wrong {P r : ℝ} (hr : r ≠ 0) : 1 / 2 + 4 * π * P * r ^ 2 = Ttemp r P * (π * r) := by
  have hp := Real.pi_pos
  unfold Ttemp
  field_simp
  ring

theorem M5j_refuted : ¬ (∀ P r : ℝ, r ≠ 0 → 1 / 2 + 4 * π * P * r ^ 2 = Ttemp r P * (π * r)) := by
  intro h
  have hp := Real.pi_pos
  have h1 := h 0 1 one_ne_zero
  have h2 := first_law_r_TdS (P := 0) (r := 1) one_ne_zero
  rw [h1] at h2
  unfold Ttemp at h2
  field_simp at h2
  nlinarith

-- M5k: T S/M = (1 - x^2)/(2 (1 - 3 x^2)) at the horizon (wrong; true: (1 - 3 x^2)/(2 (1 - x^2))) -- false
theorem M5k_TS_wrong {L r : ℝ} (hL : L ≠ 0) (hr : r ≠ 0) (hx : r ^ 2 ≠ L ^ 2) :
    (Ttemp r (-(3 / (8 * π * L ^ 2))) * Sent r) / Mext r (-(3 / (8 * π * L ^ 2))) =
      (1 - r ^ 2 / L ^ 2) / (2 * (1 - 3 * r ^ 2 / L ^ 2)) := by
  have hp := Real.pi_pos
  have hL2 : L ^ 2 ≠ 0 := pow_ne_zero 2 hL
  have h1 : 1 - r ^ 2 / L ^ 2 ≠ 0 := by
    intro h; apply hx; field_simp at h; linarith
  have hM : Mext r (-(3 / (8 * π * L ^ 2))) = r * (1 - r ^ 2 / L ^ 2) / 2 := Mext_eq_horizon_mass hL
  rw [hM]
  unfold Ttemp Sent; field_simp; ring

theorem M5k_refuted : ¬ (∀ L r : ℝ, L ≠ 0 → r ≠ 0 → r ^ 2 ≠ L ^ 2 →
    (Ttemp r (-(3 / (8 * π * L ^ 2))) * Sent r) / Mext r (-(3 / (8 * π * L ^ 2))) =
      (1 - r ^ 2 / L ^ 2) / (2 * (1 - 3 * r ^ 2 / L ^ 2))) := by
  intro h
  have h1 := h 1 (1 / 2) one_ne_zero (by norm_num) (by norm_num)
  have h2 := (horizon_ratios (L := 1) (r := 1 / 2) one_ne_zero (by norm_num) (by norm_num)).2.1
  rw [h1] at h2
  norm_num at h2

-- M5l: C_P/S = -2 (1 - 3 x^2)/(1 + x^2) (wrong; true: (1 + 3 x^2) in the denominator) -- false
theorem M5l_CP_wrong {L r : ℝ} (hL : L ≠ 0) (hr : r ≠ 0) :
    (Ttemp r (-(3 / (8 * π * L ^ 2))) * (2 * π * r) / (-(1 / (4 * π * r ^ 2)) + 2 * (-(3 / (8 * π * L ^ 2))))) / Sent r
      = -2 * (1 - 3 * r ^ 2 / L ^ 2) / (1 + r ^ 2 / L ^ 2) := by
  have hp := Real.pi_pos
  have hL2 : L ^ 2 ≠ 0 := pow_ne_zero 2 hL
  have hne : L ^ 2 + 3 * r ^ 2 ≠ 0 := by positivity
  have hden : -(1 / (4 * π * r ^ 2)) + 2 * (-(3 / (8 * π * L ^ 2))) = -(L ^ 2 + 3 * r ^ 2) / (4 * π * r ^ 2 * L ^ 2) := by
    field_simp; ring
  rw [hden]
  unfold Ttemp Sent
  field_simp
  ring

theorem M5l_refuted : ¬ (∀ L r : ℝ, L ≠ 0 → r ≠ 0 →
    (Ttemp r (-(3 / (8 * π * L ^ 2))) * (2 * π * r) / (-(1 / (4 * π * r ^ 2)) + 2 * (-(3 / (8 * π * L ^ 2))))) / Sent r
      = -2 * (1 - 3 * r ^ 2 / L ^ 2) / (1 + r ^ 2 / L ^ 2)) := by
  intro h
  have h1 := h 1 (1 / 2) one_ne_zero (by norm_num)
  have h2 := CP_over_S (L := 1) (r := 1 / 2) one_ne_zero (by norm_num)
  rw [h1] at h2
  norm_num at h2

-- M5m: at the puzzle black-hole horizon C_P/S = -1/sqrt(1 + 32 pi) (wrong: -2/sqrt(1 + 32 pi)) -- false
theorem M5m_CPvalue_wrong {X : ℝ} (hX : 8 * π * (1 - X) ^ 2 = X) (hlt : X < 1) :
    2 * (1 - X) / (1 + X) = 1 / Real.sqrt (1 + 32 * π) := by
  have hp := Real.pi_pos
  have hq : 0 < 1 + 32 * π := by positivity
  have hs := Real.sqrt_pos.mpr hq
  have hs2 := Real.sq_sqrt hq.le
  set q := Real.sqrt (1 + 32 * π) with hqdef
  have hXpos : 0 < X := by
    rcases lt_trichotomy X 0 with h | h | h
    · exfalso; nlinarith [sq_nonneg (1 - X)]
    · exfalso; rw [h] at hX; norm_num at hX
    · exact h
  have hw : 0 < 1 - X := by linarith
  have h1 : q * (1 - X) = 1 + X := by
    have : (q * (1 - X) - (1 + X)) * (q * (1 - X) + (1 + X)) = 0 := by nlinarith [hX, hs2]
    rcases mul_eq_zero.mp this with h | h
    · linarith
    · exfalso; nlinarith [mul_pos hs hw]
  rw [div_eq_div_iff (by linarith) hs.ne']
  nlinarith [h1]

theorem M5m_refuted : ¬ (∀ X : ℝ, 8 * π * (1 - X) ^ 2 = X → X < 1 → 2 * (1 - X) / (1 + X) = 1 / Real.sqrt (1 + 32 * π)) := by
  intro h
  have hp := Real.pi_pos
  have hq : 0 < 1 + 32 * π := by positivity
  have hs := Real.sqrt_pos.mpr hq
  have hs2 := Real.sq_sqrt hq.le
  set q := Real.sqrt (1 + 32 * π) with hqdef
  have hq1 : 1 < q := by nlinarith
  -- the black-hole root X0 = 1 - (q - 1)/(16 pi)
  have hX0 : 8 * π * (1 - (1 - (q - 1) / (16 * π))) ^ 2 = 1 - (q - 1) / (16 * π) := by
    field_simp; nlinarith [hs2]
  have hlt : 1 - (q - 1) / (16 * π) < 1 := by
    have : 0 < (q - 1) / (16 * π) := by apply div_pos <;> linarith
    linarith
  have h1 := h _ hX0 hlt
  have h2 := (CP_puzzle_values hX0).1 hlt
  rw [h1] at h2
  field_simp at h2
  linarith

-- M5n: the barrier height at T_b = T_dS is 5 L/27 (wrong: 5 L/54) -- false
theorem M5n_barrier_wrong {L : ℝ} (hL : L ≠ 0) : (L / 3 / 4) * (1 + (L / 3) ^ 2 / L ^ 2) = 5 * L / 27 := by
  field_simp; ring

theorem M5n_refuted : ¬ (∀ L : ℝ, L ≠ 0 → (L / 3 / 4) * (1 + (L / 3) ^ 2 / L ^ 2) = 5 * L / 27) := by
  intro h
  have h1 := h 1 one_ne_zero
  rw [barrier_height one_ne_zero] at h1
  norm_num at h1


#print axioms M5a_refuted
#print axioms M5b_refuted
#print axioms M5c_refuted
#print axioms M5d_refuted
#print axioms M5e_refuted
#print axioms M5f_refuted
#print axioms M5g_refuted
#print axioms M5h_refuted
#print axioms M5i_refuted
#print axioms M5j_refuted
#print axioms M5k_refuted
#print axioms M5l_refuted
#print axioms M5m_refuted
#print axioms M5n_refuted
#print axioms M5a_V_wrong
#print axioms M5b_smarr_wrong
#print axioms M5c_ratio_wrong
#print axioms M5d_kappa_wrong
#print axioms M5e_gibbs_wrong
#print axioms M5f_bath_wrong
#print axioms M5g_rational_x_exists
#print axioms M5h_T_wrong
#print axioms M5i_U_wrong
#print axioms M5j_TdS_wrong
#print axioms M5k_TS_wrong
#print axioms M5l_CP_wrong
#print axioms M5m_CPvalue_wrong
#print axioms M5n_barrier_wrong
