import Mathlib
import H2_s4_euler

open MeasureTheory Set Real

/-! Conventions: c = G = 1.  a0 > 0 a surface gravity; L > 0 the de Sitter radius; Lambda = 3/L^2; H = 1/L;
Z = 1/(a0 L) (a0 = H/Z); a Schwarzschild horizon of surface gravity a0 has r_s = 1/(2 a0) and area pi/a0^2 as stated in the puzzle
(area of the radius-r_s sphere is 4 pi r_s^2 = pi/a0^2: see `horizon_area`). rho_Lambda = Lambda/(8 pi). -/

/-- area of the horizon 2-sphere of a Schwarzschild black hole with surface gravity a0: r_s = 1/(2 a0) (kappa = 1/(4M), r_s = 2M) -/
theorem horizon_area {a0 : ℝ} (ha : 0 < a0) : 4 * π * (1 / (2 * a0)) ^ 2 = π / a0 ^ 2 := by
  have : a0 ≠ 0 := ha.ne'
  field_simp
  norm_num

/-- Schwarzschild: surface gravity 1/(4M) = a0 with r_s = 2M gives r_s = 1/(2 a0) -/
theorem schwarzschild_rs {M a0 : ℝ} (hM : 0 < M) (h : 1 / (4 * M) = a0) : 2 * M = 1 / (2 * a0) := by
  have : M ≠ 0 := hM.ne'
  rw [← h]; field_simp; norm_num

/-- (a) the constant: A_{a0} * Lambda = 32 pi^2  <->  Lambda = 32 pi a0^2 -/
theorem A_Lambda_iff {a0 Λ : ℝ} (ha : 0 < a0) : (π / a0 ^ 2) * Λ = 32 * π ^ 2 ↔ Λ = 32 * π * a0 ^ 2 := by
  have hp := Real.pi_pos
  have h : a0 ^ 2 ≠ 0 := by positivity
  constructor
  · intro h1
    field_simp at h1 ⊢
    nlinarith [h1]
  · intro h1; rw [h1]; field_simp

/-- (b) Lambda = 32 pi a0^2  <->  G rho = 4 a0^2 with rho = Lambda/(8 pi), G = 1  (no pi left) -/
theorem Lambda_iff_G_rho {a0 Λ : ℝ} : Λ = 32 * π * a0 ^ 2 ↔ Λ / (8 * π) = 4 * a0 ^ 2 := by
  have hp := Real.pi_pos
  have : (8 * π) ≠ 0 := by positivity
  rw [div_eq_iff this]
  constructor <;> intro h <;> linarith

/-- (c) G rho = 4 a0^2  <->  a0 = (1/2) sqrt(G rho)  (a0 > 0, rho >= 0) -/
theorem G_rho_iff_a0_half_sqrt {a0 ρ : ℝ} (ha : 0 < a0) (hρ : 0 ≤ ρ) : ρ = 4 * a0 ^ 2 ↔ a0 = (1 / 2) * Real.sqrt ρ := by
  constructor
  · intro h
    rw [h, show (4 : ℝ) * a0 ^ 2 = (2 * a0) ^ 2 by ring, Real.sqrt_sq (by positivity)]
    ring
  · intro h
    have h2 : Real.sqrt ρ = 2 * a0 := by linarith
    have := Real.sq_sqrt hρ
    rw [h2] at this
    nlinarith [this]

/-- (d) rho_Lambda r_s^2 = 1 (horizon Gauss curvature 1/r_s^2 equals rho_Lambda) <-> Lambda = 32 pi a0^2 -/
theorem Lambda_iff_curvature_density {a0 Λ : ℝ} (ha : 0 < a0) :
    Λ = 32 * π * a0 ^ 2 ↔ (Λ / (8 * π)) * (1 / (2 * a0)) ^ 2 = 1 := by
  have hp := Real.pi_pos
  have h : a0 ≠ 0 := ha.ne'
  constructor
  · intro h1; rw [h1]; field_simp; ring
  · intro h1
    field_simp at h1
    nlinarith [h1]

/-- (e) Z^2 = 32 pi/3  <->  A_{a0} Lambda = 32 pi^2, for Lambda = 3/L^2, Z = 1/(a0 L) -/
theorem Zsq_iff_A_Lambda {a0 L : ℝ} (ha : 0 < a0) (hL : 0 < L) :
    (1 / (a0 * L)) ^ 2 = 32 * π / 3 ↔ (π / a0 ^ 2) * (3 / L ^ 2) = 32 * π ^ 2 := by
  have hp := Real.pi_pos
  have h1 : a0 ≠ 0 := ha.ne'
  have h2 : L ≠ 0 := hL.ne'
  constructor
  · intro h
    have : 1 / (a0 * L) ^ 2 = 32 * π / 3 := by rw [← h]; field_simp
    field_simp at this ⊢
    nlinarith [this]
  · intro h
    field_simp at h ⊢
    nlinarith [h]

/-- (f) A_{a0} = 4 Vol(S^4_L)/L^2  <->  Z^2 = 32 pi/3 -/
theorem A_eq_4Vol_iff {a0 L : ℝ} (ha : 0 < a0) (hL : 0 < L) :
    π / a0 ^ 2 = 4 * volS4 L / L ^ 2 ↔ (1 / (a0 * L)) ^ 2 = 32 * π / 3 := by
  have hp := Real.pi_pos
  have h1 : a0 ≠ 0 := ha.ne'
  have h2 : L ≠ 0 := hL.ne'
  rw [volS4_eq]
  constructor
  · intro h
    have : 1 / (a0 * L) ^ 2 = 32 * π / 3 := by
      field_simp at h ⊢
      nlinarith [h]
    rw [← this]; field_simp
  · intro h
    have : 1 / (a0 * L) ^ 2 = 32 * π / 3 := by rw [← h]; field_simp
    field_simp at this ⊢
    nlinarith [this]

/-- (g) A_{a0} = (4/3) Lambda Vol(S^4_L) with Lambda = 3/L^2  <->  A = 4 Vol/L^2 (same statement) -/
theorem four_thirds_Lambda_Vol {L : ℝ} (hL : L ≠ 0) : (4 / 3) * (3 / L ^ 2) * volS4 L = 4 * volS4 L / L ^ 2 := by
  field_simp

/-- the value: when Z^2 = 32 pi/3, A_{a0} = 32 pi^2 L^2/3 and A_{a0} Lambda = 32 pi^2 (forward, explicit numbers) -/
theorem A_value {a0 L : ℝ} (ha : 0 < a0) (hL : 0 < L) (hZ : (1 / (a0 * L)) ^ 2 = 32 * π / 3) :
    π / a0 ^ 2 = 32 * π ^ 2 * L ^ 2 / 3 := by
  have hp := Real.pi_pos
  have h1 : a0 ≠ 0 := ha.ne'
  have h2 : L ≠ 0 := hL.ne'
  have : 1 / (a0 * L) ^ 2 = 32 * π / 3 := by rw [← hZ]; field_simp
  field_simp at this ⊢
  nlinarith [this]

/-- the A/S_dS reading: A_{a0}/(4 pi L^2) = Z^2/... : A_{a0} / (4 pi L^2) = 8 pi/3 (ratio to the de Sitter horizon area), given Z^2 = 32 pi/3 -/
theorem area_ratio_to_dS {a0 L : ℝ} (ha : 0 < a0) (hL : 0 < L) (hZ : (1 / (a0 * L)) ^ 2 = 32 * π / 3) :
    (π / a0 ^ 2) / (4 * π * L ^ 2) = 8 * π / 3 := by
  have hp := Real.pi_pos
  have h2 : L ≠ 0 := hL.ne'
  rw [A_value ha hL hZ]; field_simp; ring

/-- Z^2 = 32 pi/3 is irrational (Mathlib's irrational_pi; transcendence of pi is NOT in Mathlib) -/
theorem Zsq_irrational : Irrational (32 * π / 3) := by
  have h : Irrational π := irrational_pi
  have h1 : Irrational (32 * π) := by
    have := h.ratCast_mul (q := 32) (by norm_num)
    simpa using this
  have := h1.div_ratCast (q := 3) (by norm_num)
  simpa using this

theorem Zsq_kappa_match_gives_8pi_over_3 {a0 Λ L : ℝ} (ha : 0 < a0) (hΛ : 0 < Λ) (hL : L ^ 2 = 3 / Λ)
    (h : a0 ^ 2 = Λ / (8 * π)) : (1 / (a0 * L)) ^ 2 = 8 * π / 3 := by
  have hp := Real.pi_pos
  have hL2 : L ^ 2 = 3 / (8 * π * a0 ^ 2) := by
    rw [hL]; have : Λ = 8 * π * a0 ^ 2 := by rw [h]; field_simp
    rw [this]
  have : (1 / (a0 * L)) ^ 2 = 1 / (a0 ^ 2 * L ^ 2) := by field_simp
  rw [this, hL2]; field_simp

#print axioms horizon_area
#print axioms schwarzschild_rs
#print axioms A_Lambda_iff
#print axioms Lambda_iff_G_rho
#print axioms G_rho_iff_a0_half_sqrt
#print axioms Lambda_iff_curvature_density
#print axioms Zsq_iff_A_Lambda
#print axioms A_eq_4Vol_iff
#print axioms four_thirds_Lambda_Vol
#print axioms A_value
#print axioms area_ratio_to_dS
#print axioms Zsq_irrational
#print axioms Zsq_kappa_match_gives_8pi_over_3
