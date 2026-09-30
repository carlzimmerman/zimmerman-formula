import Mathlib

open Real Polynomial

/-!
# P5: extended black-hole thermodynamics of Schwarzschild-de Sitter (lane X3, W03)

Conventions: G = c = hbar-free (T = kappa/(2 pi), S = pi r^2 = A/4).  L > 0 the de Sitter radius, Lambda = 3/L^2, the pressure P = -Lambda/(8 pi) = -3/(8 pi L^2) (= -rho_Lambda),
the thermodynamic volume V = 4 pi r^3/3, the mass (enthalpy) M(r, P) = r/2 + 4 pi P r^3/3 of the SdS horizon of radius r (INPUT: it is f(r) = 0 solved for M, see `Mext_eq_horizon_mass`).

CERTIFIED (premises => conclusions):
 (a) `first_law_r`, `first_law_P`, `first_law_path`: with T = (1 + 8 pi P r^2)/(4 pi r), S = pi r^2, V = 4 pi r^3/3: dM/dr = T dS/dr, dM/dP = V, and along any differentiable path (r(t), P(t)):
     d/dt M = T S'(r) r' + V P' (this IS dM = T dS + V dP).  `smarr`: M = 2 T S - 2 P V.  `U_eq`: M - P V = r/2 (Misner-Sharp).  `Gibbs_b`: M - T S = (r/4)(1 + r^2/L^2).
 (b) `Mext_eq_horizon_mass`: at P = -3/(8 pi L^2), M(r, P) = r (1 - r^2/L^2)/2 (the mass at which f(r) = 0); `T_eq_kappa`: T = kappa/(2 pi) with kappa = (1 - 3 r^2/L^2)/(2 r).
 (c) flat-probe ratios (Schwarzschild mass M = r/2 with the vacuum pressure): |P| V/M = r^2/L^2 = S/S_dS, which equals 8 pi/3 iff G rho_Lambda r^2 = 1 iff r^2 = Z^2 L^2/4 with Z^2 = 32 pi/3
     (`flat_probe_ratios`); `flat_TS`: T S = M/2 for Schwarzschild (T = 1/(8 pi M), S = 4 pi M^2).
 (d) the BH horizon at kappa_b = H (T_b = T_dS): x = r/L = 1/3, and then a0^2/(G rho_Lambda) = 8 pi/3 (`bath_point`, `bath_ratio`).  [NB: kappa = a0/sqrt(G rho_Lambda) = sqrt(8 pi/3) there, i.e. Z = 1;
     it is NOT the kappa = 1 kernel (Z = sqrt(8 pi/3)): the sentence "a0 = H is the forced kernel kappa = 1" in the lane README is a slip, the certified value is a0^2/(G rho_L) = 8 pi/3.]
 (e) `kappa_sq_over_absP`: kappa_b^2/|P| = 2 pi (1 - X)^2/X with X = Lambda r^2 = 3 r^2/L^2.  The puzzle condition kappa_b^2 = rho_Lambda/4 (a0^2/(G rho_Lambda) = 1/4 at the horizon) is 8 pi (1 - X)^2 = X:
     no RATIONAL X solves it (`puzzle_no_rational_x`, uses irrational_pi), and no ALGEBRAIC X solves it if pi is transcendental (`puzzle_no_algebraic_x`, EXPLICIT hypothesis Transcendental Q pi).
     The same for the cosmological horizon kappa_c.  ("A rational or algebraic principle gives kappa_b/H algebraic, never 1/Z.")
 (f) `horizon_ratios`: |P| V/M = x^2/(1 - x^2), T S/M = (1 - 3 x^2)/(2 (1 - x^2)), G/M = (1 + x^2)/(2 (1 - x^2)) (x = r/L); `T_deriv`, `CP_over_S`: C_P/S = -2 (1 - 3 x^2)/(1 + 3 x^2)
     (C_P = T S'(r)/(dT/dr)); `CP_puzzle_values`: at the roots of 8 pi (1 - X)^2 = X (the two a0-horizons) C_P/S = -2/sqrt(1 + 32 pi) (black hole, X < 1) and +2/sqrt(1 + 32 pi) (cosmological, X > 1)
     -- the lane's -0.19849; `barrier_height`: G_b = 5 L/54 at T_b = T_dS (x = 1/3).

NOT certified: that the SdS first law is the right thermodynamics, that the f-normalisation is physical, that any of these ratios is selected by a principle; kappa = 1/2 (FITTED).
-/

namespace ExtThermo

noncomputable def Mext (r P : ℝ) : ℝ := r / 2 + 4 * π * P * r ^ 3 / 3
noncomputable def Ttemp (r P : ℝ) : ℝ := (1 + 8 * π * P * r ^ 2) / (4 * π * r)
noncomputable def Sent (r : ℝ) : ℝ := π * r ^ 2
noncomputable def Vth (r : ℝ) : ℝ := 4 * π * r ^ 3 / 3

theorem first_law_r {P r : ℝ} : HasDerivAt (fun r => Mext r P) (1 / 2 + 4 * π * P * r ^ 2) r := by
  unfold Mext
  have h1 : HasDerivAt (fun r : ℝ => r / 2) (1 / 2) r := by simpa using (hasDerivAt_id r).div_const 2
  have h2 : HasDerivAt (fun r : ℝ => 4 * π * P * r ^ 3 / 3) (4 * π * P * (3 * r ^ 2) / 3) r := by
    have := ((hasDerivAt_pow 3 r).const_mul (4 * π * P)).div_const 3
    simpa using this
  have := h1.add h2
  refine this.congr_deriv ?_
  ring

/-- dM/dr = T dS/dr  (T = (1 + 8 pi P r^2)/(4 pi r), dS/dr = 2 pi r) -/
theorem first_law_r_TdS {P r : ℝ} (hr : r ≠ 0) : 1 / 2 + 4 * π * P * r ^ 2 = Ttemp r P * (2 * π * r) := by
  have hp := Real.pi_pos
  unfold Ttemp
  field_simp
  ring

theorem Sent_deriv {r : ℝ} : HasDerivAt Sent (2 * π * r) r := by
  unfold Sent
  have := (hasDerivAt_pow 2 r).const_mul π
  simpa [mul_comm, mul_assoc, mul_left_comm] using this

/-- dM/dP = V -/
theorem first_law_P {P r : ℝ} : HasDerivAt (fun P => Mext r P) (Vth r) P := by
  unfold Mext Vth
  have h := ((((hasDerivAt_id P).const_mul (4 * π)).mul_const (r ^ 3)).div_const 3).const_add (r / 2)
  simpa using h

/-- dM = T dS + V dP along any differentiable path (r(t), P(t)) -/
theorem first_law_path {rr PP : ℝ → ℝ} {r' P' t : ℝ} (hr : rr t ≠ 0) (h1 : HasDerivAt rr r' t) (h2 : HasDerivAt PP P' t) :
    HasDerivAt (fun t => Mext (rr t) (PP t)) (Ttemp (rr t) (PP t) * (2 * π * rr t) * r' + Vth (rr t) * P') t := by
  have hp := Real.pi_pos
  unfold Mext
  have h3 : HasDerivAt (fun t => rr t / 2) (r' / 2) t := h1.div_const 2
  have h4 : HasDerivAt (fun t => 4 * π * PP t * rr t ^ 3 / 3)
      ((4 * π * P' * rr t ^ 3 + 4 * π * PP t * (3 * rr t ^ 2 * r')) / 3) t := by
    have := (((h2.const_mul (4 * π)).mul (h1.pow 3)).div_const 3)
    simpa using this
  refine (h3.add h4).congr_deriv ?_
  unfold Ttemp Vth
  field_simp
  ring

/-- Smarr: M = 2 T S - 2 P V -/
theorem smarr {P r : ℝ} (hr : r ≠ 0) : Mext r P = 2 * Ttemp r P * Sent r - 2 * P * Vth r := by
  have hp := Real.pi_pos
  unfold Mext Ttemp Sent Vth
  field_simp
  ring

/-- U = M - P V = r/2 -/
theorem U_eq {P r : ℝ} : Mext r P - P * Vth r = r / 2 := by
  unfold Mext Vth; ring

/-- with P = -3/(8 pi L^2): M(r, P) = r (1 - r^2/L^2)/2, i.e. the mass at which f(r) = 1 - 2M/r - r^2/L^2 vanishes -/
theorem Mext_eq_horizon_mass {L r : ℝ} (hL : L ≠ 0) :
    Mext r (-(3 / (8 * π * L ^ 2))) = r * (1 - r ^ 2 / L ^ 2) / 2 := by
  have hp := Real.pi_pos
  unfold Mext
  field_simp
  ring

/-- T = kappa/(2 pi) with kappa = (1 - 3 r^2/L^2)/(2 r) (f-normalisation) at P = -3/(8 pi L^2) -/
theorem T_eq_kappa {L r : ℝ} (hL : L ≠ 0) (hr : r ≠ 0) :
    Ttemp r (-(3 / (8 * π * L ^ 2))) = ((1 - 3 * r ^ 2 / L ^ 2) / (2 * r)) / (2 * π) := by
  have hp := Real.pi_pos
  unfold Ttemp
  field_simp
  ring

/-- Gibbs: M - T S = (r/4)(1 + r^2/L^2) at the SdS pressure -/
theorem Gibbs_b {L r : ℝ} (hL : L ≠ 0) (hr : r ≠ 0) :
    Mext r (-(3 / (8 * π * L ^ 2))) - Ttemp r (-(3 / (8 * π * L ^ 2))) * Sent r = (r / 4) * (1 + r ^ 2 / L ^ 2) := by
  have hp := Real.pi_pos
  unfold Mext Ttemp Sent
  field_simp
  ring

/-- (c) flat probe: Schwarzschild mass r/2, |P| = rho_Lambda = 3/(8 pi L^2): |P| V/M = r^2/L^2 = S/S_dS;
    = 8 pi/3  <=>  G rho_Lambda r^2 = 1  <=>  r^2 = (Z^2/4) L^2 with Z^2 = 32 pi/3 -/
theorem flat_probe_ratios {L r : ℝ} (hL : L ≠ 0) (hr : r ≠ 0) :
    (3 / (8 * π * L ^ 2)) * Vth r / (r / 2) = r ^ 2 / L ^ 2 ∧ Sent r / (π * L ^ 2) = r ^ 2 / L ^ 2 ∧
    (r ^ 2 / L ^ 2 = 8 * π / 3 ↔ (3 / (8 * π * L ^ 2)) * r ^ 2 = 1) ∧
    (r ^ 2 / L ^ 2 = 8 * π / 3 ↔ r ^ 2 = ((32 * π / 3) / 4) * L ^ 2) := by
  have hp := Real.pi_pos
  have hL2 : L ^ 2 ≠ 0 := pow_ne_zero 2 hL
  refine ⟨?_, ?_, ?_, ?_⟩
  · unfold Vth; field_simp; ring
  · unfold Sent; field_simp
  · rw [div_eq_iff hL2]
    constructor
    · intro h; rw [h]; field_simp
    · intro h; field_simp at h; nlinarith [h]
  · rw [div_eq_iff hL2]
    constructor
    · intro h; rw [h]; ring
    · intro h; rw [h]; ring

/-- Schwarzschild T S = M/2 (T = 1/(8 pi M), S = 4 pi M^2) -/
theorem flat_TS {M : ℝ} (hM : M ≠ 0) : (1 / (8 * π * M)) * (4 * π * M ^ 2) = M / 2 := by
  have hp := Real.pi_pos
  field_simp
  ring

/-- (d) kappa_b = H (T_b = T_dS): (1 - 3x^2)/(2x) = 1 <=> x = 1/3 (x > 0), where then a0^2/(G rho_L) = H^2/(3 H^2/(8 pi)) = 8 pi/3 -/
theorem bath_point {x : ℝ} (hx : 0 < x) : (1 - 3 * x ^ 2) / (2 * x) = 1 ↔ x = 1 / 3 := by
  rw [div_eq_one_iff_eq (by positivity)]
  constructor
  · intro h
    have : (3 * x - 1) * (x + 1) = 0 := by nlinarith [h]
    rcases mul_eq_zero.mp this with h1 | h1
    · linarith
    · linarith
  · intro h; rw [h]; norm_num

theorem bath_ratio {L : ℝ} (hL : L ≠ 0) : (1 / L) ^ 2 / (3 / (8 * π * L ^ 2)) = 8 * π / 3 := by
  have hp := Real.pi_pos
  field_simp

/-- (e) kappa_b^2/|P| = 2 pi (1 - X)^2/X with X = Lambda r^2 = 3 r^2/L^2, |P| = 3/(8 pi L^2) -/
theorem kappa_sq_over_absP {L r : ℝ} (hL : L ≠ 0) (hr : r ≠ 0) :
    ((1 - 3 * r ^ 2 / L ^ 2) / (2 * r)) ^ 2 / (3 / (8 * π * L ^ 2)) = 2 * π * (1 - 3 * r ^ 2 / L ^ 2) ^ 2 / (3 * r ^ 2 / L ^ 2) := by
  have hp := Real.pi_pos
  field_simp
  ring

/-- the puzzle condition at a horizon: kappa^2/|P| = 1/4 with kappa^2/|P| = 2 pi (1 - X)^2/X, i.e. 8 pi (1 - X)^2 = X (X > 0) -/
theorem puzzle_condition_iff {X : ℝ} (hX : 0 < X) : 2 * π * (1 - X) ^ 2 / X = 1 / 4 ↔ 8 * π * (1 - X) ^ 2 = X := by
  have hX0 : X ≠ 0 := hX.ne'
  rw [div_eq_iff hX0]
  constructor <;> intro h <;> linarith

/-- no rational X solves it (irrational_pi) -/
theorem puzzle_no_rational_x (q : ℚ) : 8 * π * (1 - (q : ℝ)) ^ 2 ≠ q := by
  intro h
  by_cases h1 : (q : ℝ) = 1
  · rw [h1] at h; norm_num at h
  · have h2 : (1 - (q : ℝ)) ^ 2 ≠ 0 := pow_ne_zero 2 (sub_ne_zero.mpr (Ne.symm h1))
    have h3 : π = (q : ℝ) / (8 * (1 - (q : ℝ)) ^ 2) := by
      field_simp; linarith
    have h4 : π = ((q / (8 * (1 - q) ^ 2) : ℚ) : ℝ) := by
      rw [h3]; push_cast; ring
    exact irrational_pi ⟨_, h4.symm⟩

/-- no ALGEBRAIC X solves it if pi is transcendental (explicit hypothesis; Lindemann is not in Mathlib) -/
theorem puzzle_no_algebraic_x (hπ : Transcendental ℚ π) (X : ℝ) (hX : IsAlgebraic ℚ X) : 8 * π * (1 - X) ^ 2 ≠ X := by
  intro h
  by_cases h1 : X = 1
  · rw [h1] at h; norm_num at h
  · have h2 : (1 - X) ^ 2 ≠ 0 := pow_ne_zero 2 (sub_ne_zero.mpr (Ne.symm h1))
    have h3 : π = X / (8 * (1 - X) ^ 2) := by
      field_simp; linarith
    have hmem : X ∈ algebraicClosure ℚ ℝ := (mem_algebraicClosure_iff).mpr hX
    have h4 : π ∈ algebraicClosure ℚ ℝ := by
      rw [h3]
      have h8 : (8 : ℝ) ∈ algebraicClosure ℚ ℝ := by
        have : ((8 : ℚ) : ℝ) ∈ algebraicClosure ℚ ℝ := (algebraicClosure ℚ ℝ).algebraMap_mem _
        exact_mod_cast this
      have h1' : (1 : ℝ) ∈ algebraicClosure ℚ ℝ := (algebraicClosure ℚ ℝ).one_mem
      have h5 : (1 - X) ∈ algebraicClosure ℚ ℝ := (algebraicClosure ℚ ℝ).sub_mem h1' hmem
      have h6 : (8 * (1 - X) ^ 2) ∈ algebraicClosure ℚ ℝ :=
        (algebraicClosure ℚ ℝ).mul_mem h8 ((algebraicClosure ℚ ℝ).pow_mem h5 2)
      exact (algebraicClosure ℚ ℝ).div_mem hmem h6
    exact hπ ((mem_algebraicClosure_iff).mp h4)

/-! (f) ratios and the heat capacity at the horizon (lane X3 table), P = -3/(8 pi L^2), x^2 = r^2/L^2 -/

/-- |P| V/M = x^2/(1 - x^2), T S/M = (1 - 3 x^2)/(2 (1 - x^2)), G/M = (1 + x^2)/(2 (1 - x^2)) at the SdS horizon (M = r(1 - x^2)/2) -/
theorem horizon_ratios {L r : ℝ} (hL : L ≠ 0) (hr : r ≠ 0) (hx : r ^ 2 ≠ L ^ 2) :
    (-(-(3 / (8 * π * L ^ 2))) * Vth r) / Mext r (-(3 / (8 * π * L ^ 2))) = (r ^ 2 / L ^ 2) / (1 - r ^ 2 / L ^ 2) ∧
    (Ttemp r (-(3 / (8 * π * L ^ 2))) * Sent r) / Mext r (-(3 / (8 * π * L ^ 2))) =
      (1 - 3 * r ^ 2 / L ^ 2) / (2 * (1 - r ^ 2 / L ^ 2)) ∧
    (Mext r (-(3 / (8 * π * L ^ 2))) - Ttemp r (-(3 / (8 * π * L ^ 2))) * Sent r) / Mext r (-(3 / (8 * π * L ^ 2))) =
      (1 + r ^ 2 / L ^ 2) / (2 * (1 - r ^ 2 / L ^ 2)) := by
  have hp := Real.pi_pos
  have hL2 : L ^ 2 ≠ 0 := pow_ne_zero 2 hL
  have h1 : 1 - r ^ 2 / L ^ 2 ≠ 0 := by
    intro h; apply hx; field_simp at h; linarith
  have hM : Mext r (-(3 / (8 * π * L ^ 2))) = r * (1 - r ^ 2 / L ^ 2) / 2 := Mext_eq_horizon_mass hL
  have hG := Gibbs_b (L := L) (r := r) hL hr
  rw [hM]
  refine ⟨?_, ?_, ?_⟩
  · unfold Vth; field_simp; ring
  · unfold Ttemp Sent; field_simp; ring
  · rw [← hM, hG, hM]; field_simp; ring

/-- dT/dr at fixed P: T = 1/(4 pi r) + 2 P r, dT/dr = -1/(4 pi r^2) + 2 P -/
theorem T_deriv {P r : ℝ} (hr : r ≠ 0) : HasDerivAt (fun r => Ttemp r P) (-(1 / (4 * π * r ^ 2)) + 2 * P) r := by
  have hp := Real.pi_pos
  have h1 : HasDerivAt (fun r : ℝ => (1 / (4 * π)) * r⁻¹) ((1 / (4 * π)) * (-(r ^ 2)⁻¹)) r := (hasDerivAt_inv hr).const_mul _
  have h2 : HasDerivAt (fun r : ℝ => 2 * P * r) (2 * P) r := by simpa using (hasDerivAt_id r).const_mul (2 * P)
  have h3 := h1.add h2
  have hfun : (fun r => Ttemp r P) = fun r => (1 / (4 * π)) * r⁻¹ + 2 * P * r := by
    funext r
    unfold Ttemp
    rcases eq_or_ne r 0 with h | h
    · simp [h]
    · field_simp; ring
  rw [hfun]
  refine h3.congr_deriv ?_
  field_simp

/-- heat capacity at constant pressure C_P = T (dS/dr)/(dT/dr); C_P/S = -2 (1 - 3 x^2)/(1 + 3 x^2) at the SdS pressure -/
theorem CP_over_S {L r : ℝ} (hL : L ≠ 0) (hr : r ≠ 0) :
    (Ttemp r (-(3 / (8 * π * L ^ 2))) * (2 * π * r) / (-(1 / (4 * π * r ^ 2)) + 2 * (-(3 / (8 * π * L ^ 2))))) / Sent r
      = -2 * (1 - 3 * r ^ 2 / L ^ 2) / (1 + 3 * r ^ 2 / L ^ 2) := by
  have hp := Real.pi_pos
  have hL2 : L ^ 2 ≠ 0 := pow_ne_zero 2 hL
  have hpos : 0 < 1 + 3 * r ^ 2 / L ^ 2 := by positivity
  have hne : L ^ 2 + 3 * r ^ 2 ≠ 0 := by positivity
  have hden : -(1 / (4 * π * r ^ 2)) + 2 * (-(3 / (8 * π * L ^ 2))) = -(L ^ 2 + 3 * r ^ 2) / (4 * π * r ^ 2 * L ^ 2) := by
    field_simp; ring
  rw [hden]
  unfold Ttemp Sent
  field_simp
  ring

/-- for the black-hole horizon of the puzzle (X = 3 x^2 the root < 1 of 8 pi (1 - X)^2 = X): C_P/S = -2 (1 - X)/(1 + X) = -2/sqrt(1 + 32 pi);
    for the cosmological horizon (root X > 1): +2 (X - 1)/(X + 1) = +2/sqrt(1 + 32 pi) -/
theorem CP_puzzle_values {X : ℝ} (hX : 8 * π * (1 - X) ^ 2 = X) :
    (X < 1 → 2 * (1 - X) / (1 + X) = 2 / Real.sqrt (1 + 32 * π)) ∧ (1 < X → 2 * (X - 1) / (X + 1) = 2 / Real.sqrt (1 + 32 * π)) := by
  have hp := Real.pi_pos
  have hq : 0 < 1 + 32 * π := by positivity
  have hs := Real.sqrt_pos.mpr hq
  have hs2 := Real.sq_sqrt hq.le
  set q := Real.sqrt (1 + 32 * π) with hqdef
  have hX0 : 0 < X ∨ X = 0 := by
    rcases lt_trichotomy X 0 with h | h | h
    · exfalso; nlinarith [sq_nonneg (1 - X)]
    · exact Or.inr h
    · exact Or.inl h
  have hXpos : 0 < X := by
    rcases hX0 with h | h
    · exact h
    · exfalso; rw [h] at hX; norm_num at hX
  constructor
  · intro hlt
    have hw : 0 < 1 - X := by linarith
    -- w = 1 - X solves 8 pi w^2 + w - 1 = 0, so q w = 2 - w
    have h1 : q * (1 - X) = 1 + X := by
      have : (q * (1 - X) - (1 + X)) * (q * (1 - X) + (1 + X)) = 0 := by nlinarith [hX, hs2]
      rcases mul_eq_zero.mp this with h | h
      · linarith
      · exfalso; nlinarith [mul_pos hs hw]
    rw [div_eq_div_iff (by linarith) hs.ne']
    nlinarith [h1]
  · intro hgt
    have hw : 0 < X - 1 := by linarith
    have h1 : q * (X - 1) = X + 1 := by
      have : (q * (X - 1) - (X + 1)) * (q * (X - 1) + (X + 1)) = 0 := by nlinarith [hX, hs2]
      rcases mul_eq_zero.mp this with h | h
      · linarith
      · exfalso; nlinarith [mul_pos hs hw]
    rw [div_eq_div_iff (by linarith) hs.ne']
    nlinarith [h1]

/-- the barrier height of the off-shell free energy at T = T_dS (x = 1/3): G_b = 5 L/54 -/
theorem barrier_height {L : ℝ} (hL : L ≠ 0) :
    (L / 3 / 4) * (1 + (L / 3) ^ 2 / L ^ 2) = 5 * L / 54 := by
  field_simp; ring

end ExtThermo

#print axioms ExtThermo.first_law_r
#print axioms ExtThermo.first_law_P
#print axioms ExtThermo.first_law_path
#print axioms ExtThermo.smarr
#print axioms ExtThermo.Mext_eq_horizon_mass
#print axioms ExtThermo.T_eq_kappa
#print axioms ExtThermo.Gibbs_b
#print axioms ExtThermo.flat_probe_ratios
#print axioms ExtThermo.bath_point
#print axioms ExtThermo.kappa_sq_over_absP
#print axioms ExtThermo.puzzle_no_rational_x
#print axioms ExtThermo.puzzle_no_algebraic_x
#print axioms ExtThermo.horizon_ratios
#print axioms ExtThermo.T_deriv
#print axioms ExtThermo.CP_over_S
#print axioms ExtThermo.CP_puzzle_values
#print axioms ExtThermo.barrier_height
