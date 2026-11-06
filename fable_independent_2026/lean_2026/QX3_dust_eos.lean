import Mathlib

/-!
# QX3 -- Lean certificate for the CMB-lensing / growth mechanisms (closure_2026_11_06/QX3_cmb_growth)

CERTIFIED (algebra / calculus only):
* `kq_energy`: for p(Q) = A (Q-1)^2, rho = Q p'(Q) - p = A (Q^2 - 1).
* `kq_pressure_le`: for A > 0, Q >= 1: p <= rho^2 / (4A)  (n = 1 polytrope bound, equality in the dilute limit).
* `kq_jeans`: with c_s^2 = rho/(2A), 4 pi G rho / c_s^2 = 8 pi G A (density-independent).
* `kq_jeans_mu`: with A = mu^2/(8 pi G) (units c = 1), k_J^2 = mu^2.
* `poly_radius`: with K = 2 pi G / mu^2, the n = 1 polytrope radius pi sqrt(K/(2 pi G)) = pi/mu.
* `lane_emden_n1_reduced`: u = sin solves u'' = -u (the n = 1 Lane-Emden equation for u = xi theta);
  `lane_emden_first_zero`, `lane_emden_positive`: sin vanishes at pi and is positive on (0, pi);
  `enclosed_fraction_at_R`: (sin xi - xi cos xi)/pi = 1 at xi = pi.
* `clock_jeans`: a c_s^2 = 1 component with 0 <= rho_phi <= rho_tot, 8 pi G rho_tot = 3 H^2 has
  k_J^2 = 4 pi G rho_phi <= (3/2) H^2: it clusters only on Hubble scales.
* `barotropic_beta`: for p ~ rho^(n/(n-1)) the Jeans length scales as rho^beta with beta = (2-n)/(2(n-1));
  `beta_zero_iff`: beta = 0 iff n = 2.
NOT CERTIFIED: that v3s's K(Q) sector is a perfect fluid at linear order (k-essence reading), the Newtonian
sub-horizon growth equation, any number graded against data. Zero sorry; axioms printed below.
-/

theorem kq_energy (A Q : ℝ) : Q * (2 * A * (Q - 1)) - A * (Q - 1) ^ 2 = A * (Q ^ 2 - 1) := by ring

theorem kq_pressure_le (A Q : ℝ) (hA : 0 < A) (hQ : 1 ≤ Q) :
    A * (Q - 1) ^ 2 ≤ (A * (Q ^ 2 - 1)) ^ 2 / (4 * A) := by
  rw [le_div_iff₀ (by positivity)]
  have h1 : 0 ≤ (Q - 1) * (Q + 3) := mul_nonneg (by linarith) (by linarith)
  have h2 : 0 ≤ A ^ 2 * (Q - 1) ^ 2 * ((Q - 1) * (Q + 3)) := by positivity
  nlinarith [h2]

theorem kq_jeans (G A ρ : ℝ) (hA : 0 < A) (hρ : 0 < ρ) :
    4 * Real.pi * G * ρ / (ρ / (2 * A)) = 8 * Real.pi * G * A := by
  field_simp; ring

theorem kq_jeans_mu (G μ : ℝ) (hG : 0 < G) :
    8 * Real.pi * G * (μ ^ 2 / (8 * Real.pi * G)) = μ ^ 2 := by
  have : (0:ℝ) < Real.pi := Real.pi_pos
  field_simp

theorem poly_radius (G μ : ℝ) (hG : 0 < G) (hμ : 0 < μ) :
    Real.pi * Real.sqrt ((2 * Real.pi * G / μ ^ 2) / (2 * Real.pi * G)) = Real.pi / μ := by
  have hp : (0:ℝ) < Real.pi := Real.pi_pos
  have e : (2 * Real.pi * G / μ ^ 2) / (2 * Real.pi * G) = (μ ^ 2)⁻¹ := by field_simp
  rw [e, Real.sqrt_inv, Real.sqrt_sq hμ.le, div_eq_mul_inv]

theorem lane_emden_n1_reduced : deriv (deriv Real.sin) = fun x => - Real.sin x := by
  rw [Real.deriv_sin]; exact Real.deriv_cos'

theorem lane_emden_first_zero : Real.sin Real.pi = 0 := Real.sin_pi

theorem lane_emden_positive (x : ℝ) (h0 : 0 < x) (h1 : x < Real.pi) : 0 < Real.sin x / x :=
  div_pos (Real.sin_pos_of_pos_of_lt_pi h0 h1) h0

theorem enclosed_fraction_at_R :
    (Real.sin Real.pi - Real.pi * Real.cos Real.pi) / Real.pi = 1 := by
  rw [Real.sin_pi, Real.cos_pi]; field_simp [Real.pi_pos.ne']; ring

theorem clock_jeans (G H ρφ ρt : ℝ) (hφ : 0 ≤ ρφ) (hle : ρφ ≤ ρt) (hG : 0 < G)
    (hF : 8 * Real.pi * G * ρt = 3 * H ^ 2) : 4 * Real.pi * G * ρφ ≤ 3 / 2 * H ^ 2 := by
  have hp : (0:ℝ) < Real.pi := Real.pi_pos
  have : 4 * Real.pi * G * ρφ ≤ 4 * Real.pi * G * ρt := by
    apply mul_le_mul_of_nonneg_left hle; positivity
  nlinarith

/-- exponent bookkeeping: p ~ rho^(n/(n-1)) => c_s^2 ~ rho^(n/(n-1) - 1), k_J^2 ~ rho^(1 - that),
lambda_J ~ rho^(-(1/2) (1 - that)). -/
theorem barotropic_beta (n : ℝ) (hn : n ≠ 1) :
    -(1 / 2) * (1 - (n / (n - 1) - 1)) = (2 - n) / (2 * (n - 1)) := by
  have : n - 1 ≠ 0 := sub_ne_zero.mpr hn
  field_simp; ring

theorem beta_zero_iff (n : ℝ) (hn : n ≠ 1) : (2 - n) / (2 * (n - 1)) = 0 ↔ n = 2 := by
  have : 2 * (n - 1) ≠ 0 := mul_ne_zero two_ne_zero (sub_ne_zero.mpr hn)
  rw [div_eq_zero_iff]; constructor
  · rintro (h | h); linarith; exact absurd h this
  · intro h; left; linarith

#print axioms kq_energy
#print axioms kq_pressure_le
#print axioms kq_jeans
#print axioms kq_jeans_mu
#print axioms poly_radius
#print axioms lane_emden_n1_reduced
#print axioms lane_emden_first_zero
#print axioms lane_emden_positive
#print axioms enclosed_fraction_at_R
#print axioms clock_jeans
#print axioms barotropic_beta
#print axioms beta_zero_iff
