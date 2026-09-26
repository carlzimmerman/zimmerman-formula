import Mathlib

/-!
# DE1–DE2 — the vacuum gate read at four epochs: algebraic certificates

SCOPE. Lean certifies the algebra behind `real_research/dark_energy_2026/DE1_vacuum_gate_flagship.py` (the gated MOND
switch's edge against the flagship radius) and `real_research/dark_energy_2026/DE2_vacuum_gate_joint_window.py` (the
joint window of KiDS, cosmic shear, the flagship and the forest).  The numbers X_K, X_S, X_F and the forest table are
computed in those lanes, not here; the physics (that each gate reads the gate at one epoch, the monotonicity of the
cosmic-shear margin and of the forest deviation in the threshold) is established there numerically, not here.

The construction's gate: MOND acts in a bound region where x̃ [Ω_Λ(z)/Ω_Λ,0]^p ≥ x_c0, i.e. above the threshold
x_c,eff(z) = x_c0 e(z)^p with e(z) = E(z)² = H(z)²/H₀².

* `edge_closed_form` — for the isothermal deep-MOND phantom the switch variable at radius r is v²/(rH)² − x̄ (x̄ the
  mean-density term); it equals X exactly when r² = v²/(H²(X + x̄)).
* `flagship_speed_ratio` — with v² = √(GM)·√a₀ (deep MOND, v⁴ = G M a₀) and r_f² = G M/(a₀/10) (g_bar = a₀/10),
  v²/r_f² = a₀^{3/2}/(10 √(GM)): the flagship radius sits inside the MOND region iff X + x̄ ≤ a₀^{3/2}/(10 √(GM) H²).
* `flagship_survives_iff` — r_e² ≥ r_f² ⟺ X + x̄ ≤ v²/(H² r_f²).
* `y_edge_formula` — the deepest acceleration inside the region, y_edge = GM/(a₀ r_e²) = √(GM) H² (X + x̄)/a₀^{3/2}.
* `y_edge_mass_monotone` — y_edge grows with √(GM): the heaviest flagship galaxy binds.
* `window_iff` — (the DE2 window) a positive x_c0 with x_c0 e_K^p ≤ X_K, X_S ≤ x_c0 e_S^p and x_c0 e_F^p ≤ X_F exists
  iff X_S e_K^p ≤ X_K e_S^p and X_S e_F^p ≤ X_F e_S^p (take x_c0 = X_S/e_S^p).
* `window_p_interval` — with e_K < e_S < e_F the two conditions are the p-interval
  log(X_S/X_K)/log(e_S/e_K) ≤ p ≤ log(X_F/X_S)/log(e_F/e_S).
* `dominance` — for e ≥ 1, p' ≤ p and 0 ≤ x' ≤ x: x' e^{p'} ≤ x e^p (a gate above a passing gate at every epoch).
* `ungated_pincer` — with p = 0 one threshold must satisfy the forest floor X_f ≤ x and the KiDS cap x ≤ X_K; if
  X_K < X_f there is none (the L352/L358 pincer; MUTATE of DE2).
* `linear_gate_local` — the p = 1 gate is a local scalar of the foliation: with x̃ = 9 R/(4K²) and Ω_Λ = 3Λ/K²,
  x̃ Ω_Λ = 27 Λ R/(4 K⁴).

The vacuum sets the scale (the identities the clean path rests on; `THE_CLEAN_PATH_2026-09-26.md` §1–2):

* `a0_of_lambda` — with ρ_Λ = Λc²/(8πG), a₀ = ½ c √(G ρ_Λ) equals c² √(Λ/(32π)).
* `Z_is_kappa` — with H_Λ² = Λc²/3 and a₀² = κ² c⁴ Λ/(8π), Z² ≡ (c H_Λ)²/a₀² = 8π/(3κ²): Z is κ restated, not a
  second number; `Z_at_half` — κ = ½ gives Z² = 32π/3 (Z = 5.7888, never ~21).
* `four_form_energy`, `four_form_kappa`, `four_form_half` — for the four-form promotion (kappa_closure/k04) with
  P(q) = Z_q q²/2 + b β² q² and a₀²/G = β² q²: the gravitating energy is the Legendre form ε = q P′ − P =
  Z_q q²/2 + b β² q², the flux amplitude cancels from κ² = β²q²/ε = 2β²/(Z_q + 2bβ²), and κ = ½ ⟺ Z_q = (8 − 2b) β² — one
  free ratio.  Z_q (`Zq` below) is the four-form's stiffness, k04's "Z"; it is NOT the framework's Z = cH_Λ/a₀ =
  √(32π/3) = 5.7888 of `Z_is_kappa`.

The linear gate inside DE2's window (numbers are DE2's computed bounds, entered as data):

* `linear_gate_cell_in_window` — the cell p = 1, x_c0 = 5/2 with L359's background (e(0.25) = 1.299090625,
  e(2.5) = 14.1404) and GP3's mock epoch (e(0.5) ≥ 1.7452) meets the KiDS cap (x_c,eff(0.25) ≤ 3.86, a grid point that
  passes both footings, so the exact cap is at least this), the cosmic-shear floor at 600 km/s (x_c,eff(0.5) ≥ 3.5, the
  computed floor being 3.499) and the flagship cap (x_c,eff(2.5) ≤ 364.5), and dominates L359's weakest committed
  forest-passing cell (p ≥ 1/2, x_c0 ≥ 3/2).
-/

theorem edge_closed_form (v H X xb r : ℝ) (hv : 0 < v) (hH : 0 < H) (hr : 0 < r) (hX : 0 < X + xb) :
    v ^ 2 / (r * H) ^ 2 - xb = X ↔ r ^ 2 = v ^ 2 / (H ^ 2 * (X + xb)) := by
  have hr2 : 0 < r ^ 2 := by positivity
  have hH2 : 0 < H ^ 2 := by positivity
  constructor
  · intro h
    have h1 : v ^ 2 / (r * H) ^ 2 = X + xb := by linarith
    rw [mul_pow] at h1
    field_simp at h1 ⊢
    nlinarith [h1]
  · intro h
    rw [mul_pow, h]
    field_simp
    ring

theorem flagship_speed_ratio (s t : ℝ) (hs : 0 < s) (ht : 0 < t) :
    (s * t) / (s ^ 2 / (t ^ 2 / 10)) = t ^ 3 / (10 * s) := by
  field_simp

theorem flagship_survives_iff (v H X xb rf2 : ℝ) (_hv : 0 < v) (hH : 0 < H) (hX : 0 < X + xb) (hrf : 0 < rf2) :
    rf2 ≤ v ^ 2 / (H ^ 2 * (X + xb)) ↔ X + xb ≤ v ^ 2 / (H ^ 2 * rf2) := by
  have hH2 : 0 < H ^ 2 := by positivity
  rw [le_div_iff₀ (by positivity), le_div_iff₀ (by positivity)]
  constructor <;> intro h <;> nlinarith [h]

theorem y_edge_formula (s t H X' : ℝ) (hs : 0 < s) (ht : 0 < t) (hH : 0 < H) (hX : 0 < X') :
    s ^ 2 / (t ^ 2 * ((s * t) / (H ^ 2 * X'))) = s * H ^ 2 * X' / t ^ 3 := by
  field_simp

theorem y_edge_mass_monotone (s1 s2 t H X' : ℝ) (h12 : s1 ≤ s2) (ht : 0 < t) (hH : 0 < H) (hX : 0 < X') :
    s1 * H ^ 2 * X' / t ^ 3 ≤ s2 * H ^ 2 * X' / t ^ 3 := by
  have hc : 0 < H ^ 2 * X' / t ^ 3 := by positivity
  have := mul_le_mul_of_nonneg_right h12 (le_of_lt hc)
  calc s1 * H ^ 2 * X' / t ^ 3 = s1 * (H ^ 2 * X' / t ^ 3) := by ring
    _ ≤ s2 * (H ^ 2 * X' / t ^ 3) := this
    _ = s2 * H ^ 2 * X' / t ^ 3 := by ring

theorem window_iff (eK eS eF XK XS XF p : ℝ) (heK : 0 < eK) (heS : 0 < eS) (heF : 0 < eF)
    (_hXK : 0 < XK) (hXS : 0 < XS) (_hXF : 0 < XF) :
    (∃ x0 : ℝ, 0 < x0 ∧ x0 * eK ^ p ≤ XK ∧ XS ≤ x0 * eS ^ p ∧ x0 * eF ^ p ≤ XF) ↔
      (XS * eK ^ p ≤ XK * eS ^ p ∧ XS * eF ^ p ≤ XF * eS ^ p) := by
  have aK : 0 < eK ^ p := Real.rpow_pos_of_pos heK p
  have aS : 0 < eS ^ p := Real.rpow_pos_of_pos heS p
  have aF : 0 < eF ^ p := Real.rpow_pos_of_pos heF p
  constructor
  · rintro ⟨x0, hx0, hK, hS, hF⟩
    constructor
    · have h1 : XS * eK ^ p ≤ x0 * eS ^ p * eK ^ p := mul_le_mul_of_nonneg_right hS (le_of_lt aK)
      have h2 : x0 * eK ^ p * eS ^ p ≤ XK * eS ^ p := mul_le_mul_of_nonneg_right hK (le_of_lt aS)
      nlinarith [h1, h2]
    · have h1 : XS * eF ^ p ≤ x0 * eS ^ p * eF ^ p := mul_le_mul_of_nonneg_right hS (le_of_lt aF)
      have h2 : x0 * eF ^ p * eS ^ p ≤ XF * eS ^ p := mul_le_mul_of_nonneg_right hF (le_of_lt aS)
      nlinarith [h1, h2]
  · rintro ⟨hK, hF⟩
    refine ⟨XS / eS ^ p, div_pos hXS aS, ?_, ?_, ?_⟩
    · rw [div_mul_eq_mul_div, div_le_iff₀ aS]; linarith
    · rw [div_mul_cancel₀ XS (ne_of_gt aS)]
    · rw [div_mul_eq_mul_div, div_le_iff₀ aS]; linarith

theorem window_p_interval (eK eS eF XK XS XF p : ℝ) (heK : 0 < eK) (hKS : eK < eS) (hSF : eS < eF)
    (hXK : 0 < XK) (hXS : 0 < XS) (hXF : 0 < XF) :
    (XS * eK ^ p ≤ XK * eS ^ p ∧ XS * eF ^ p ≤ XF * eS ^ p) ↔
      (Real.log (XS / XK) / Real.log (eS / eK) ≤ p ∧ p ≤ Real.log (XF / XS) / Real.log (eF / eS)) := by
  have heS : 0 < eS := by linarith
  have heF : 0 < eF := by linarith
  have aK : 0 < eK ^ p := Real.rpow_pos_of_pos heK p
  have aS : 0 < eS ^ p := Real.rpow_pos_of_pos heS p
  have aF : 0 < eF ^ p := Real.rpow_pos_of_pos heF p
  have lSK : 0 < Real.log (eS / eK) := Real.log_pos ((one_lt_div heK).mpr hKS)
  have lFS : 0 < Real.log (eF / eS) := Real.log_pos ((one_lt_div heS).mpr hSF)
  -- first condition in logs
  have c1 : XS * eK ^ p ≤ XK * eS ^ p ↔ Real.log (XS / XK) ≤ p * Real.log (eS / eK) := by
    have e1 : XS * eK ^ p ≤ XK * eS ^ p ↔ XS / XK ≤ (eS / eK) ^ p := by
      rw [Real.div_rpow (le_of_lt heS) (le_of_lt heK), div_le_div_iff₀ hXK aK]
      constructor <;> intro h <;> linarith
    rw [e1, ← Real.log_rpow (div_pos heS heK)]
    exact (Real.log_le_log_iff (div_pos hXS hXK) (Real.rpow_pos_of_pos (div_pos heS heK) p)).symm
  have c2 : XS * eF ^ p ≤ XF * eS ^ p ↔ p * Real.log (eF / eS) ≤ Real.log (XF / XS) := by
    have e2 : XS * eF ^ p ≤ XF * eS ^ p ↔ (eF / eS) ^ p ≤ XF / XS := by
      rw [Real.div_rpow (le_of_lt heF) (le_of_lt heS), div_le_div_iff₀ aS hXS]
      constructor <;> intro h <;> linarith
    rw [e2, ← Real.log_rpow (div_pos heF heS)]
    exact (Real.log_le_log_iff (Real.rpow_pos_of_pos (div_pos heF heS) p) (div_pos hXF hXS)).symm
  rw [c1, c2, div_le_iff₀ lSK, le_div_iff₀ lFS]

theorem dominance (e p p' x x' : ℝ) (he : 1 ≤ e) (hp : p' ≤ p) (hx' : 0 ≤ x') (hx : x' ≤ x) :
    x' * e ^ p' ≤ x * e ^ p := by
  have h1 : e ^ p' ≤ e ^ p := Real.rpow_le_rpow_of_exponent_le he hp
  have h0 : 0 ≤ e ^ p' := Real.rpow_nonneg (by linarith) p'
  calc x' * e ^ p' ≤ x * e ^ p' := mul_le_mul_of_nonneg_right hx h0
    _ ≤ x * e ^ p := mul_le_mul_of_nonneg_left h1 (le_trans hx' hx)

theorem ungated_pincer (XK Xf : ℝ) (h : XK < Xf) : ¬ ∃ x : ℝ, Xf ≤ x ∧ x ≤ XK := by
  rintro ⟨x, h1, h2⟩
  linarith

theorem linear_gate_local (R K Λ : ℝ) (hK : K ≠ 0) :
    (9 * R / (4 * K ^ 2)) * (3 * Λ / K ^ 2) = 27 * Λ * R / (4 * K ^ 4) := by
  field_simp
  ring

theorem a0_of_lambda (c G Λ : ℝ) (hc : 0 < c) (hG : 0 < G) (hΛ : 0 < Λ) :
    (1 / 2) * c * Real.sqrt (G * (Λ * c ^ 2 / (8 * Real.pi * G))) = c ^ 2 * Real.sqrt (Λ / (32 * Real.pi)) := by
  have hpi : 0 < Real.pi := Real.pi_pos
  have h1 : G * (Λ * c ^ 2 / (8 * Real.pi * G)) = c ^ 2 * (Λ / (8 * Real.pi)) := by
    field_simp
  have h2 : Λ / (32 * Real.pi) = (1 / 2) ^ 2 * (Λ / (8 * Real.pi)) := by
    field_simp
    ring
  rw [h1, h2, Real.sqrt_mul (by positivity), Real.sqrt_mul (by positivity), Real.sqrt_sq (le_of_lt hc),
    Real.sqrt_sq (by norm_num)]
  ring

theorem Z_is_kappa (c HΛ a0 κ Λ : ℝ) (hc : 0 < c) (hΛ : 0 < Λ) (hκ : 0 < κ)
    (hH : HΛ ^ 2 = Λ * c ^ 2 / 3) (ha : a0 ^ 2 = κ ^ 2 * c ^ 4 * Λ / (8 * Real.pi)) :
    (c * HΛ) ^ 2 / a0 ^ 2 = 8 * Real.pi / (3 * κ ^ 2) := by
  have hpi : 0 < Real.pi := Real.pi_pos
  rw [mul_pow, hH, ha]
  field_simp

theorem Z_at_half : 8 * Real.pi / (3 * (1 / 2 : ℝ) ^ 2) = 32 * Real.pi / 3 := by
  ring

theorem four_form_energy (Zq b β q : ℝ) :
    q * (Zq * q + 2 * b * β ^ 2 * q) - (Zq * q ^ 2 / 2 + b * β ^ 2 * q ^ 2) = Zq * q ^ 2 / 2 + b * β ^ 2 * q ^ 2 := by
  ring

theorem four_form_kappa (Zq b β q : ℝ) (hq : q ≠ 0) (hden : 0 < Zq + 2 * b * β ^ 2) :
    β ^ 2 * q ^ 2 / (Zq * q ^ 2 / 2 + b * β ^ 2 * q ^ 2) = 2 * β ^ 2 / (Zq + 2 * b * β ^ 2) := by
  have hq2 : 0 < q ^ 2 := by positivity
  have hne : Zq * q ^ 2 / 2 + b * β ^ 2 * q ^ 2 ≠ 0 := by
    have : Zq * q ^ 2 / 2 + b * β ^ 2 * q ^ 2 = q ^ 2 * (Zq + 2 * b * β ^ 2) / 2 := by ring
    rw [this]; positivity
  field_simp

theorem four_form_half (Zq b β : ℝ) (_hβ : 0 < β) (hden : 0 < Zq + 2 * b * β ^ 2) :
    2 * β ^ 2 / (Zq + 2 * b * β ^ 2) = 1 / 4 ↔ Zq = (8 - 2 * b) * β ^ 2 := by
  rw [div_eq_iff (ne_of_gt hden)]
  constructor <;> intro h <;> linarith

theorem linear_gate_cell_in_window :
    (5 / 2 : ℝ) * 1.299090625 ≤ 3.86 ∧ (3.5 : ℝ) ≤ 5 / 2 * 1.7452 ∧ (5 / 2 : ℝ) * 14.1404 ≤ 364.5 ∧
      (1 / 2 : ℝ) ≤ 1 ∧ (3 / 2 : ℝ) ≤ 5 / 2 := by
  norm_num

#print axioms edge_closed_form
#print axioms flagship_speed_ratio
#print axioms flagship_survives_iff
#print axioms y_edge_formula
#print axioms y_edge_mass_monotone
#print axioms window_iff
#print axioms window_p_interval
#print axioms dominance
#print axioms ungated_pincer
#print axioms linear_gate_local
#print axioms a0_of_lambda
#print axioms Z_is_kappa
#print axioms Z_at_half
#print axioms four_form_energy
#print axioms four_form_kappa
#print axioms four_form_half
#print axioms linear_gate_cell_in_window
