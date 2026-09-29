import Mathlib

/-!
# PUZZLE_32pi_reductions -- exact algebra behind "A * Lambda = 32 pi^2" (c = G = 1)

Source: sonnet55_push/puzzle_32pi/p01_exact_reductions.py (sympy checks of the curvature integrals) and p02_matching_scan.py.

Certified here (premises => conclusions; pure algebra and one elementary integral):
* `puzzle_equiv_Lambda`  : for a0 > 0,  (pi/a0^2) * Lambda = 32 pi^2  <->  Lambda = 32 pi a0^2.
* `puzzle_equiv_density` : for a0 > 0,  Lambda = 32 pi a0^2  <->  rho_Lambda * r_s^2 = 1  with rho_Lambda = Lambda/(8 pi), r_s = 1/(2 a0)
  (the Schwarzschild radius of the black hole of surface gravity a0): i.e. the horizon's Gauss curvature 1/r_s^2 equals rho_Lambda.
* `gb_constant_factorisation` : 32 pi^2 = (8 pi)(4 pi) = 2 (4 pi)^2 = 12 * (8 pi^2/3): Einstein's 8 pi times a solid angle 4 pi; the unit S^4 integral of R.
* `Zsq_from_curvature_match` : if 1/r_s^2 = Lambda/(8 pi) with r_s = 1/(2 a0) and L^2 = 3/Lambda then (1/(a0 L))^2 = 32 pi/3;
  `Zsq_from_kappa_match` : the near-miss kappa^2 = rho_Lambda gives 8 pi/3, exactly four times smaller.
* `Zsq_irrational` : 32 pi/3 is irrational (so no rational-coefficient relation between a0 and Lambda can reproduce it).
* the static-slice Euler charge Q = int E4 dV3 = 32 pi kappa: `charge_dS` (E4 = 24/L^4 on a ball of volume 4 pi L^3/3),
  `charge_Schwarzschild` (48 M^2 / r^6 integrated over r > 2M, the improper integral proved), `charge_kappa` (Q = 32 pi kappa for both),
  and `gb_from_charge` (beta Q = 64 pi^2 with beta = 2 pi/kappa: scale-free).
NOT certified: the Riemann-tensor computation of E4 (sympy in p01), any physical reason to prefer kappa = a0, or any derivation of kappa = 1/2.
-/

open MeasureTheory Set Real

theorem puzzle_equiv_Lambda {a0 Λ : ℝ} (ha : 0 < a0) : (π / a0 ^ 2) * Λ = 32 * π ^ 2 ↔ Λ = 32 * π * a0 ^ 2 := by
  have hp := Real.pi_pos
  have h : a0 ^ 2 ≠ 0 := by positivity
  constructor
  · intro h1
    field_simp at h1 ⊢
    nlinarith [h1]
  · intro h1; rw [h1]; field_simp

theorem puzzle_equiv_density {a0 Λ : ℝ} (ha : 0 < a0) :
    Λ = 32 * π * a0 ^ 2 ↔ (Λ / (8 * π)) * (1 / (2 * a0)) ^ 2 = 1 := by
  have hp := Real.pi_pos
  have h : a0 ≠ 0 := ha.ne'
  constructor
  · intro h1; rw [h1]; field_simp; ring
  · intro h1
    field_simp at h1
    nlinarith [h1]

theorem gb_constant_factorisation :
    (32 * π ^ 2 = (8 * π) * (4 * π)) ∧ (32 * π ^ 2 = 2 * (4 * π) ^ 2) ∧ (32 * π ^ 2 = 12 * (8 * π ^ 2 / 3)) := by
  refine ⟨by ring, by ring, by ring⟩

theorem Zsq_from_curvature_match {a0 Λ L : ℝ} (ha : 0 < a0) (hL : L ^ 2 = 3 / Λ)
    (h : 1 / (1 / (2 * a0)) ^ 2 = Λ / (8 * π)) : (1 / (a0 * L)) ^ 2 = 8 * π / 3 := by
  have hp := Real.pi_pos
  have h1 : Λ = 32 * π * a0 ^ 2 := by
    have : 4 * a0 ^ 2 = Λ / (8 * π) := by rw [← h]; field_simp; norm_num
    field_simp at this; nlinarith [this]
  have hL2 : L ^ 2 = 3 / (32 * π * a0 ^ 2) := by rw [hL, h1]
  have : (1 / (a0 * L)) ^ 2 = 1 / (a0 ^ 2 * L ^ 2) := by field_simp
  rw [this, hL2]; field_simp

theorem Zsq_from_kappa_match {a0 Λ L : ℝ} (ha : 0 < a0) (hΛ : 0 < Λ) (hL : L ^ 2 = 3 / Λ)
    (h : a0 ^ 2 = Λ / (8 * π)) : (1 / (a0 * L)) ^ 2 = 8 * π / 3 := by
  have hp := Real.pi_pos
  have hL2 : L ^ 2 = 3 / (8 * π * a0 ^ 2) := by
    rw [hL]; have : Λ = 8 * π * a0 ^ 2 := by rw [h]; field_simp
    rw [this]
  have : (1 / (a0 * L)) ^ 2 = 1 / (a0 ^ 2 * L ^ 2) := by field_simp
  rw [this, hL2]; field_simp

theorem Zsq_irrational : Irrational (32 * π / 3) := by
  have h : Irrational π := irrational_pi
  have h1 : Irrational (32 * π) := by
    have := h.ratCast_mul (q := 32) (by norm_num)
    simpa using this
  have := h1.div_ratCast (q := 3) (by norm_num)
  simpa using this

theorem charge_dS {L : ℝ} (hL : L ≠ 0) : (24 / L ^ 4) * (4 * π * L ^ 3 / 3) = 32 * π / L := by
  field_simp; ring

theorem charge_Schwarzschild_integral {M : ℝ} (hM : 0 < M) :
    ∫ r in Ioi (2 * M), r ^ (-4 : ℝ) = 1 / (3 * (2 * M) ^ 3) := by
  have h2 : 0 < 2 * M := by positivity
  rw [integral_Ioi_rpow_of_lt (by norm_num) h2]
  rw [show (-4 : ℝ) + 1 = -3 by norm_num]
  rw [Real.rpow_neg h2.le, show ((3 : ℝ)) = ((3 : ℕ) : ℝ) by norm_num, Real.rpow_natCast]
  field_simp

theorem charge_Schwarzschild {M : ℝ} (hM : 0 < M) :
    4 * π * (48 * M ^ 2) * (1 / (3 * (2 * M) ^ 3)) = 8 * π / M := by
  have : M ≠ 0 := hM.ne'
  field_simp; ring

theorem charge_kappa {M : ℝ} (hM : 0 < M) :
    8 * π / M = 32 * π * (1 / (4 * M)) := by
  have : M ≠ 0 := hM.ne'
  field_simp; ring

theorem gb_from_charge {κ : ℝ} (hκ : κ ≠ 0) : (2 * π / κ) * (32 * π * κ) = 64 * π ^ 2 := by
  field_simp; ring

#print axioms puzzle_equiv_Lambda
#print axioms puzzle_equiv_density
#print axioms gb_constant_factorisation
#print axioms Zsq_from_curvature_match
#print axioms Zsq_from_kappa_match
#print axioms Zsq_irrational
#print axioms charge_dS
#print axioms charge_Schwarzschild_integral
#print axioms charge_Schwarzschild
#print axioms charge_kappa
#print axioms gb_from_charge
