/-
QX6 (closure_2026_11_06/QX6_clock_depth, criteria 3edba4879f): the algebra behind the route labels.
Route 2: the khronon-frame rho_DE tie gives a0_eff/a0 <= N^-2 <= 1 + 2.1 d (d = Q - 1 <= 0.01), so
F - 1 <= 2.1 d, far below the >= 1.1 X-COP needs at d <= 1.2e-4. Route 1: no mu_K satisfies both the
S4 galaxy bound (<= 0.1 Mpc^-1) and the CMB-lensing need (>= 3.98e4), and the clusters' mean-zero
mu_K (>= 1.74) exceeds the galaxy bound. Route 3: sqrt(a0 Lstar / c^2) lies in the window (k_g, k_x)
(arithmetic only; a coincidence, not a derivation). kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace QX6

/-- Clock energy share: with X/rho <= 1 and 0 < N <= 1, rho_loc/rho_bg <= N^-2. -/
theorem rho_share {x N : ℝ} (hx0 : 0 ≤ x) (hx1 : x ≤ 1) (hN0 : 0 < N) (hN1 : N ≤ 1) :
    1 + x * (1 / N ^ 2 - 1) ≤ 1 / N ^ 2 := by
  have hN2 : 0 < N ^ 2 := by positivity
  have hge : 1 ≤ 1 / N ^ 2 := by
    rw [le_div_iff₀ hN2]; nlinarith
  nlinarith

/-- N^-2 <= 1 + 2.1 d for N = 1 - d, 0 <= d <= 1/100. -/
theorem lapse_bound {d : ℝ} (h0 : 0 ≤ d) (h1 : d ≤ 1 / 100) :
    1 / (1 - d) ^ 2 ≤ 1 + 21 / 10 * d := by
  have hpos : 0 < (1 - d) ^ 2 := by
    have : 0 < 1 - d := by linarith
    positivity
  rw [div_le_iff₀ hpos]
  nlinarith [mul_nonneg h0 h0, mul_nonneg (mul_nonneg h0 h0) h0]

/-- Route 2 is short: F - 1 <= 2.1 d with d <= 1.2e-4 cannot reach the needed 1.1. -/
theorem route2_short {F d : ℝ} (hF : F - 1 ≤ 21 / 10 * d) (hd : d ≤ 12 / 100000) : F - 1 < 11 / 10 := by
  linarith

/-- Route 1 window: no mu_K meets the S4 galaxy bound and the CMB-lensing need together. -/
theorem route1_no_window {mu : ℝ} (hgal : mu ≤ 1 / 10) (hcmb : 39800 ≤ mu) : False := by
  linarith

/-- Route 1: the clusters' mean-zero mu_K violates the S4 galaxy bound. -/
theorem route1_cluster_vs_galaxy {mu : ℝ} (hcl : 174 / 100 ≤ mu) : ¬ mu ≤ 1 / 10 := by
  intro h; linarith

/-- Route 3 arithmetic (canonical): k_g < sqrt(G1) < k_x with G1 = 6.97e-10, k_g = 4.615e-6, k_x = 4.53e-5. -/
theorem route3_window_canonical :
    (4615 / 1000000000 : ℝ) < Real.sqrt (697 / 1000000000000) ∧
    Real.sqrt (697 / 1000000000000) < (453 / 10000000 : ℝ) := by
  constructor
  · rw [Real.lt_sqrt (by norm_num)]; norm_num
  · rw [Real.sqrt_lt' (by norm_num)]; norm_num

/-- Route 3 arithmetic (alt): k_g < sqrt(G1) < k_x with G1 = 8.89e-10, k_g = 4.764e-6, k_x = 4.658e-5. -/
theorem route3_window_alt :
    (4764 / 1000000000 : ℝ) < Real.sqrt (889 / 1000000000000) ∧
    Real.sqrt (889 / 1000000000000) < (4658 / 100000000 : ℝ) := by
  constructor
  · rw [Real.lt_sqrt (by norm_num)]; norm_num
  · rw [Real.sqrt_lt' (by norm_num)]; norm_num

end QX6

#print axioms QX6.rho_share
#print axioms QX6.lapse_bound
#print axioms QX6.route2_short
#print axioms QX6.route1_no_window
#print axioms QX6.route1_cluster_vs_galaxy
#print axioms QX6.route3_window_canonical
#print axioms QX6.route3_window_alt
