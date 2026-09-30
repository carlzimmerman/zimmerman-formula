import Mathlib

open Real

/-!
# P1: walls in de Sitter (audit H1): proper acceleration, Israel sides, pure tension

Conventions: G = c = 1.  L > 0 the de Sitter radius, H = 1/L.  dS_4 is the hyperboloid -X0^2 + X1^2 + X2^2 + X3^2 + X4^2 = L^2 in R^{1,4}
(coordinates ordered X0..X4; `eta` is the Minkowski form).  A wall at X4 = c is a dS_3 of radius R with R^2 + c^2 = L^2; its worldline is
X(tau) = (R sinh(tau/R), R cosh(tau/R), 0, 0, c).

CERTIFIED (premises => conclusions):
 (a) `wall_on_hyperboloid`, `wall_velocity_unit`: X lies on the hyperboloid iff R^2 + c^2 = L^2 (here: eta X X = R^2 + c^2), tau is proper time (eta U U = -1, U = dX/dtau
     proved as a derivative).
 (b) `wall_embedding_acc`: the embedding acceleration A = dU/dtau has eta A A = 1/R^2, eta A X = 1 (normal part 1/L).
 (c) `wall_covariant_acc_sq`: the tangential (covariant) part T = A - (eta A X / L^2) X is tangent (eta T X = 0) and eta T T = 1/R^2 - 1/L^2  (NOT 1/R^2).
 (d) `static_acc_sq`, `static_eq_wall`: the static observer at r = c in f = 1 - r^2/L^2 has acceleration^2 = (f'/2)^2/f = (c/L^2)^2/(1 - c^2/L^2), equal to 1/R^2 - 1/L^2.
 (e) Israel (A - B = 4 pi sigma, A^2 - B^2 = H_out^2 - H_in^2 as PREMISES, G = 1): A = DeltaP/(3 sigma) + 2 pi sigma, B = DeltaP/(3 sigma) - 2 pi sigma with
     H^2 = (8 pi/3) rho, DeltaP = e E - e^2/2, rho_in = (E - e)^2/2, rho_out = E^2/2  (`israel_sides`, `israel_sides_converse`); their mean is DeltaP/(3 sigma)
     (`israel_mean`); 1/R^2 = H_in^2 + A^2 = H_out^2 + B^2 (`israel_euclid_radius`).
 (f) pure tension (H_in = H_out = H): A = 2 pi sigma = -B, 1/R^2 = H^2 + (2 pi sigma)^2 (`pure_tension`); every a0 > 0 is the proper acceleration of a pure-tension wall,
     sigma = a0/(2 pi) (`wall_reaches_a0`).
 (g) the probe target: with E > 0 and e = r sigma, the mean side acceleration DeltaP/(3 sigma) = r E/3 - r^2 sigma/6 (`probe_mean_expand`) and rE/3 = H_out/Z with
     Z^2 = 32 pi/3 iff r^2 = 9/8, i.e. r = 3/(2 sqrt 2) (`probe_target_ratio`).

NOT certified: that Israel's junction equations are the right ones (they are the PREMISES A - B = 4 pi sigma, A^2 - B^2 = DeltaH^2, taken from the audit); that such a wall exists in nature;
anything about kappa = 1/2.  Lean certifies that the algebra follows.
-/

namespace WallDS

/-- the Minkowski form of signature (-,+,+,+,+) on R^5 -/
def eta (P Q : Fin 5 → ℝ) : ℝ := -(P 0 * Q 0) + P 1 * Q 1 + P 2 * Q 2 + P 3 * Q 3 + P 4 * Q 4

/-- worldline of the wall X4 = c in dS_4 (R^2 + c^2 = L^2) -/
noncomputable def Xw (R c τ : ℝ) : Fin 5 → ℝ := ![R * sinh (τ / R), R * cosh (τ / R), 0, 0, c]
/-- velocity dX/dtau -/
noncomputable def Uw (R τ : ℝ) : Fin 5 → ℝ := ![cosh (τ / R), sinh (τ / R), 0, 0, 0]
/-- embedding acceleration dU/dtau -/
noncomputable def Aw (R τ : ℝ) : Fin 5 → ℝ := ![sinh (τ / R) / R, cosh (τ / R) / R, 0, 0, 0]

theorem sinh_div_deriv (R τ : ℝ) : HasDerivAt (fun τ => sinh (τ / R)) (cosh (τ / R) / R) τ := by
  have h := ((hasDerivAt_id τ).div_const R).sinh
  simpa [div_eq_mul_inv, mul_comm] using h

theorem cosh_div_deriv (R τ : ℝ) : HasDerivAt (fun τ => cosh (τ / R)) (sinh (τ / R) / R) τ := by
  have h := ((hasDerivAt_id τ).div_const R).cosh
  simpa [div_eq_mul_inv, mul_comm] using h

/-- (a) the worldline is on the hyperboloid of radius L iff R^2 + c^2 = L^2: eta X X = R^2 + c^2 -/
theorem wall_on_hyperboloid (R c τ : ℝ) : eta (Xw R c τ) (Xw R c τ) = R ^ 2 + c ^ 2 := by
  have := Real.cosh_sq (τ / R)
  simp [eta, Xw]
  nlinarith [this]

/-- U = dX/dtau (a derivative, not a definition by fiat) -/
theorem wall_velocity_is_deriv {R : ℝ} (hR : R ≠ 0) (c τ : ℝ) : HasDerivAt (Xw R c) (Uw R τ) τ := by
  rw [hasDerivAt_pi]
  intro i
  fin_cases i
  · simp only [Xw, Uw]
    have := (sinh_div_deriv R τ).const_mul R
    simpa [mul_div_cancel₀ _ hR] using this
  · simp only [Xw, Uw]
    have := (cosh_div_deriv R τ).const_mul R
    simpa [mul_div_cancel₀ _ hR] using this
  · simp [Xw, Uw]
    exact hasDerivAt_const _ _
  · simp [Xw, Uw]
    exact hasDerivAt_const _ _
  · simp [Xw, Uw]
    exact hasDerivAt_const _ _

/-- A = dU/dtau -/
theorem wall_acc_is_deriv (R τ : ℝ) : HasDerivAt (Uw R) (Aw R τ) τ := by
  rw [hasDerivAt_pi]
  intro i
  fin_cases i
  · simp only [Uw, Aw]
    simpa using cosh_div_deriv R τ
  · simp only [Uw, Aw]
    simpa using sinh_div_deriv R τ
  · simp [Uw, Aw]
    exact hasDerivAt_const _ _
  · simp [Uw, Aw]
    exact hasDerivAt_const _ _
  · simp [Uw, Aw]
    exact hasDerivAt_const _ _

/-- tau is proper time: eta U U = -1 -/
theorem wall_velocity_unit (R τ : ℝ) : eta (Uw R τ) (Uw R τ) = -1 := by
  have := Real.cosh_sq (τ / R)
  simp [eta, Uw]
  nlinarith [this]

/-- (b) the embedding acceleration: eta A A = 1/R^2 (R != 0), eta A X = 1 (its normal part along X/L is 1/L), eta A U = 0 -/
theorem wall_embedding_acc {R : ℝ} (hR : R ≠ 0) (c τ : ℝ) :
    eta (Aw R τ) (Aw R τ) = 1 / R ^ 2 ∧ eta (Aw R τ) (Xw R c τ) = 1 ∧ eta (Aw R τ) (Uw R τ) = 0 := by
  have h := Real.cosh_sq (τ / R)
  refine ⟨?_, ?_, ?_⟩
  · simp [eta, Aw]
    field_simp
    nlinarith [h]
  · simp [eta, Aw, Xw]
    field_simp
    nlinarith [h]
  · simp [eta, Aw, Uw]
    ring

/-- the covariant (tangential) acceleration of the wall inside the hyperboloid of radius L -/
noncomputable def Tw (R c L τ : ℝ) : Fin 5 → ℝ :=
  fun i => Aw R τ i - (eta (Aw R τ) (Xw R c τ) / L ^ 2) * Xw R c τ i

/-- (c) T is tangent to the hyperboloid (eta T X = 0) and eta T T = 1/R^2 - 1/L^2, given R^2 + c^2 = L^2 -/
theorem wall_covariant_acc_sq {R c L : ℝ} (hR : R ≠ 0) (hL : L ≠ 0) (hRL : R ^ 2 + c ^ 2 = L ^ 2) (τ : ℝ) :
    eta (Tw R c L τ) (Xw R c τ) = 0 ∧ eta (Tw R c L τ) (Tw R c L τ) = 1 / R ^ 2 - 1 / L ^ 2 := by
  obtain ⟨hAA, hAX, _⟩ := wall_embedding_acc hR c τ
  have hXX := wall_on_hyperboloid R c τ
  rw [hRL] at hXX
  have hL2 : L ^ 2 ≠ 0 := pow_ne_zero 2 hL
  -- bilinear expansion of eta on T = A - k X
  have hbil : ∀ k : ℝ, eta (fun i => Aw R τ i - k * Xw R c τ i) (fun i => Aw R τ i - k * Xw R c τ i)
      = eta (Aw R τ) (Aw R τ) - 2 * k * eta (Aw R τ) (Xw R c τ) + k ^ 2 * eta (Xw R c τ) (Xw R c τ) := by
    intro k; simp only [eta]; ring
  have hbilX : ∀ k : ℝ, eta (fun i => Aw R τ i - k * Xw R c τ i) (Xw R c τ)
      = eta (Aw R τ) (Xw R c τ) - k * eta (Xw R c τ) (Xw R c τ) := by
    intro k; simp only [eta]; ring
  unfold Tw
  constructor
  · rw [hbilX, hAX, hXX]; field_simp; ring
  · rw [hbil, hAA, hAX, hXX]; field_simp; ring

/-- (d) static observer at r = c in f = 1 - r^2/L^2: acceleration^2 = g_rr (a^r)^2 = (f'/2)^2 / f with a^r = Gamma^r_tt (u^t)^2 = f'/2 -/
noncomputable def staticAccSq (f f' : ℝ) : ℝ := (f' / 2) ^ 2 / f

theorem f_dS_deriv (L r : ℝ) : HasDerivAt (fun r : ℝ => 1 - r ^ 2 / L ^ 2) (-(2 * r / L ^ 2)) r := by
  have h := ((hasDerivAt_pow 2 r).div_const (L ^ 2)).const_sub 1
  simpa using h

theorem static_acc_sq {L c : ℝ} (_hL : L ≠ 0) (_hc : c ^ 2 < L ^ 2) :
    staticAccSq (1 - c ^ 2 / L ^ 2) (-(2 * c / L ^ 2)) = (c / L ^ 2) ^ 2 / (1 - c ^ 2 / L ^ 2) := by
  unfold staticAccSq
  have : (-(2 * c / L ^ 2) / 2) ^ 2 = (c / L ^ 2) ^ 2 := by ring
  rw [this]

/-- (d') the static observer and the wall are the same worldline: (c/L^2)^2/(1 - c^2/L^2) = 1/R^2 - 1/L^2 with R^2 = L^2 - c^2 -/
theorem static_eq_wall {L c R : ℝ} (hL : L ≠ 0) (hR : R ≠ 0) (hRL : R ^ 2 + c ^ 2 = L ^ 2) :
    (c / L ^ 2) ^ 2 / (1 - c ^ 2 / L ^ 2) = 1 / R ^ 2 - 1 / L ^ 2 := by
  have hc : c ^ 2 = L ^ 2 - R ^ 2 := by linarith
  have hL2 : L ^ 2 ≠ 0 := pow_ne_zero 2 hL
  have hR2 : R ^ 2 ≠ 0 := pow_ne_zero 2 hR
  have h1 : 1 - c ^ 2 / L ^ 2 = R ^ 2 / L ^ 2 := by rw [hc]; field_simp; ring
  rw [h1, div_pow, hc]
  field_simp

/-- the wall X4 = c and the static observer at r = c: acceleration^2 of the wall equals 1/R^2 - 1/L^2 = eta T T (embedding route) -/
theorem wall_acc_two_routes {R c L : ℝ} (hR : R ≠ 0) (hL : L ≠ 0) (hRL : R ^ 2 + c ^ 2 = L ^ 2) (τ : ℝ) :
    eta (Tw R c L τ) (Tw R c L τ) = (c / L ^ 2) ^ 2 / (1 - c ^ 2 / L ^ 2) := by
  rw [(wall_covariant_acc_sq hR hL hRL τ).2, static_eq_wall hL hR hRL]

/-! (e) Israel.  G = 1.  A, B: the extrinsic curvatures (= proper accelerations of the wall relative to the two sides' geodesics). -/

/-- H^2 = (8 pi/3) rho -/
noncomputable def Hsq (ρ : ℝ) : ℝ := (8 * π / 3) * ρ

/-- exact sides: A - B = 4 pi sigma and A^2 - B^2 = H_out^2 - H_in^2 with rho_in = (E - e)^2/2, rho_out = E^2/2
    give A = DeltaP/(3 sigma) + 2 pi sigma and B = DeltaP/(3 sigma) - 2 pi sigma, DeltaP = e E - e^2/2 -/
theorem israel_sides {A B σ E e : ℝ} (hσ : 0 < σ)
    (h1 : A - B = 4 * π * σ) (h2 : A ^ 2 - B ^ 2 = Hsq (E ^ 2 / 2) - Hsq ((E - e) ^ 2 / 2)) :
    A = (e * E - e ^ 2 / 2) / (3 * σ) + 2 * π * σ ∧ B = (e * E - e ^ 2 / 2) / (3 * σ) - 2 * π * σ := by
  have hp := Real.pi_pos
  have hs : σ ≠ 0 := hσ.ne'
  have hpi : π ≠ 0 := hp.ne'
  unfold Hsq at h2
  have hsum : A + B = (2 * (e * E - e ^ 2 / 2)) / (3 * σ) := by
    have hprod : (A - B) * (A + B) = (8 * π / 3) * (E ^ 2 / 2) - (8 * π / 3) * ((E - e) ^ 2 / 2) := by
      nlinarith [h2]
    rw [h1] at hprod
    have : 4 * π * σ * (A + B) = 4 * π * σ * ((2 * (e * E - e ^ 2 / 2)) / (3 * σ)) := by
      rw [hprod]; field_simp; ring
    exact mul_left_cancel₀ (by positivity) this
  constructor
  · have : A = ((A + B) + (A - B)) / 2 := by ring
    rw [this, hsum, h1]; field_simp; ring
  · have : B = ((A + B) - (A - B)) / 2 := by ring
    rw [this, hsum, h1]; field_simp; ring

/-- converse: the closed forms satisfy both junction premises -/
theorem israel_sides_converse {σ E e : ℝ} (hσ : 0 < σ) :
    ((e * E - e ^ 2 / 2) / (3 * σ) + 2 * π * σ) - ((e * E - e ^ 2 / 2) / (3 * σ) - 2 * π * σ) = 4 * π * σ ∧
    ((e * E - e ^ 2 / 2) / (3 * σ) + 2 * π * σ) ^ 2 - ((e * E - e ^ 2 / 2) / (3 * σ) - 2 * π * σ) ^ 2
      = Hsq (E ^ 2 / 2) - Hsq ((E - e) ^ 2 / 2) := by
  have hs : σ ≠ 0 := hσ.ne'
  unfold Hsq
  constructor
  · ring
  · field_simp; ring

/-- the mean of the two side accelerations is DeltaP/(3 sigma) exactly, for ALL sigma (no a >> H needed) -/
theorem israel_mean {A B σ E e : ℝ} (hσ : 0 < σ)
    (h1 : A - B = 4 * π * σ) (h2 : A ^ 2 - B ^ 2 = Hsq (E ^ 2 / 2) - Hsq ((E - e) ^ 2 / 2)) :
    (A + B) / 2 = (e * E - e ^ 2 / 2) / (3 * σ) := by
  obtain ⟨hA, hB⟩ := israel_sides hσ h1 h2
  rw [hA, hB]; ring

/-- the Euclidean radius: 1/R^2 = H_in^2 + A^2 = H_out^2 + B^2 (the two definitions agree because A^2 - B^2 = H_out^2 - H_in^2) -/
theorem israel_euclid_radius {A B Hin Hout : ℝ} (h2 : A ^ 2 - B ^ 2 = Hout ^ 2 - Hin ^ 2) :
    Hin ^ 2 + A ^ 2 = Hout ^ 2 + B ^ 2 := by linarith

/-- (f) pure tension H_in = H_out = H: A = 2 pi sigma, B = -2 pi sigma, 1/R^2 = H^2 + (2 pi sigma)^2; the proper acceleration is 2 pi sigma for EVERY H -/
theorem pure_tension {A B σ H : ℝ} (hσ : 0 < σ)
    (h1 : A - B = 4 * π * σ) (h2 : A ^ 2 - B ^ 2 = H ^ 2 - H ^ 2) :
    A = 2 * π * σ ∧ B = -(2 * π * σ) ∧ H ^ 2 + A ^ 2 = H ^ 2 + (2 * π * σ) ^ 2 := by
  have hp := Real.pi_pos
  have hsum : A + B = 0 := by
    have : (A - B) * (A + B) = 0 := by nlinarith [h2]
    rw [h1] at this
    rcases mul_eq_zero.mp this with h | h
    · exfalso; have : 0 < 4 * π * σ := by positivity
      linarith
    · exact h
  have hA : A = 2 * π * σ := by linarith
  have hB : B = -(2 * π * σ) := by linarith
  refine ⟨hA, hB, ?_⟩
  rw [hA]

/-- every a0 > 0 is the proper acceleration of a pure-tension wall in every de Sitter of Hubble rate H (sigma = a0/(2 pi)); 1/R^2 = H^2 + a0^2 -/
theorem wall_reaches_a0 {a0 H : ℝ} (ha : 0 < a0) :
    ∃ σ : ℝ, 0 < σ ∧ 2 * π * σ = a0 ∧ H ^ 2 + (2 * π * σ) ^ 2 = H ^ 2 + a0 ^ 2 := by
  have hp := Real.pi_pos
  refine ⟨a0 / (2 * π), by positivity, ?_, ?_⟩
  · field_simp
  · have : 2 * π * (a0 / (2 * π)) = a0 := by field_simp
    rw [this]

/-- the puzzle a0 = H/Z (Z > 0 any) is reached: sigma = H/(2 pi Z), and a0 < H iff Z > 1 (so a0 < H is no obstruction) -/
theorem wall_reaches_H_over_Z {H Z : ℝ} (hH : 0 < H) (hZ : 0 < Z) :
    ∃ σ : ℝ, 0 < σ ∧ 2 * π * σ = H / Z := by
  have hp := Real.pi_pos
  refine ⟨(H / Z) / (2 * π), by positivity, ?_⟩
  field_simp

/-! (g) the probe target -/

/-- with e = r sigma: DeltaP/(3 sigma) = r E/3 - r^2 sigma/6; the exact sides are rE/3 + sigma (2 pi - r^2/6) and rE/3 - sigma (2 pi + r^2/6) -/
theorem probe_mean_expand {σ E r : ℝ} (hσ : 0 < σ) :
    ((r * σ) * E - (r * σ) ^ 2 / 2) / (3 * σ) = r * E / 3 - r ^ 2 * σ / 6 := by
  have hs : σ ≠ 0 := hσ.ne'
  field_simp
  ring

theorem probe_sides_expand {σ E r : ℝ} (hσ : 0 < σ) :
    ((r * σ) * E - (r * σ) ^ 2 / 2) / (3 * σ) + 2 * π * σ = r * E / 3 + σ * (2 * π - r ^ 2 / 6) ∧
    ((r * σ) * E - (r * σ) ^ 2 / 2) / (3 * σ) - 2 * π * σ = r * E / 3 - σ * (2 * π + r ^ 2 / 6) := by
  rw [probe_mean_expand hσ]
  constructor <;> ring

/-- the target ratio: with Z^2 = 32 pi/3, E > 0, r > 0: (r E/3)^2 = H_out^2/Z^2 (i.e. r E/3 = H_out/Z, H_out^2 = (8 pi/3)(E^2/2)) iff r^2 = 9/8 (r = 3/(2 sqrt 2)) -/
theorem probe_target_ratio {E r : ℝ} (hE : 0 < E) :
    (r * E / 3) ^ 2 = Hsq (E ^ 2 / 2) / (32 * π / 3) ↔ r ^ 2 = 9 / 8 := by
  have hp := Real.pi_pos
  have hE2 : E ^ 2 ≠ 0 := by positivity
  have hpi : π ≠ 0 := hp.ne'
  have key : Hsq (E ^ 2 / 2) / (32 * π / 3) = E ^ 2 / 8 := by
    unfold Hsq; field_simp; ring
  rw [key]
  constructor
  · intro h
    have : E ^ 2 * (r ^ 2 - 9 / 8) = 0 := by nlinarith [h]
    rcases mul_eq_zero.mp this with h' | h'
    · exact absurd h' hE2
    · linarith
  · intro h
    have : (r * E / 3) ^ 2 = r ^ 2 * E ^ 2 / 9 := by ring
    rw [this, h]; ring

theorem probe_ratio_value : (3 / (2 * Real.sqrt 2)) ^ 2 = (9 : ℝ) / 8 := by
  have : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  rw [div_pow, mul_pow, this]; norm_num

end WallDS

#print axioms WallDS.wall_on_hyperboloid
#print axioms WallDS.wall_velocity_is_deriv
#print axioms WallDS.wall_acc_is_deriv
#print axioms WallDS.wall_velocity_unit
#print axioms WallDS.wall_embedding_acc
#print axioms WallDS.wall_covariant_acc_sq
#print axioms WallDS.static_acc_sq
#print axioms WallDS.static_eq_wall
#print axioms WallDS.wall_acc_two_routes
#print axioms WallDS.israel_sides
#print axioms WallDS.israel_sides_converse
#print axioms WallDS.israel_mean
#print axioms WallDS.pure_tension
#print axioms WallDS.wall_reaches_a0
#print axioms WallDS.probe_target_ratio
