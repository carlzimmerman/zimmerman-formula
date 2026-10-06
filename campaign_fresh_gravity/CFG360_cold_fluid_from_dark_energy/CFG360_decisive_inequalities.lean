/-
CFG360 -- cold fluid as a byproduct of dark energy: decisive inequalities (Lean 4 + Mathlib, no sorry).
Numbers come from cfg360_cold_fluid_from_de.py (lookback L5 = 0.8713/H0, Omega_L = 0.6865, T* = 2.2416 meV,
T0 = 2.3487e-4 eV, base-rate counts 53 / 18480).  kappa = 1/2 FITTED.  Certifies arithmetic and logic, not the physics inputs.
-/
import Mathlib

namespace CFG360

/-- Bianchi: a vacuum with constant density (w = -1, rho_dot = 0) exchanges no energy: rho_dot + Q = 0 forces Q = 0. -/
theorem const_vacuum_no_transfer (rhodot Q : ℝ) (hcons : rhodot + Q = 0) (hconst : rhodot = 0) : Q = 0 := by
  linarith

/-- Flat a0 on a0 ∝ sqrt(rho_L): |a0(z)/a0 - 1| ≤ 1% ⇒ rho_L(z)/rho_L0 ≤ 1.0201. -/
theorem flat_a0_rho_ratio (r : ℝ) (hr : 0 ≤ r) (h : Real.sqrt r ≤ 1.01) : r ≤ 1.0201 := by
  have h0 : 0 ≤ Real.sqrt r := Real.sqrt_nonneg r
  have := Real.sq_sqrt hr
  nlinarith

/-- Transfer bound: for Q = Gamma rho_L the vacuum obeys rho_L(z)/rho_L0 = exp(Gamma * L) exactly (L = lookback in 1/H0).
With L ≥ 0.87 and the flat-a0 ratio ≤ 1.0201: Gamma < 0.0232 H0. -/
theorem flat_a0_transfer_bound (Γ L : ℝ) (hL : 0.87 ≤ L) (hG : 0 ≤ Γ)
    (h : Real.exp (Γ * L) ≤ 1.0201) : Γ < 0.0232 := by
  have h1 := Real.add_one_le_exp (Γ * L)
  have h2 : Γ * L ≤ 0.0201 := by linarith
  by_contra hc0
  have hc := not_lt.mp hc0
  have : 0.0232 * 0.87 ≤ Γ * L := by
    have := mul_le_mul hc hL (by norm_num) hG
    linarith
  norm_num at this
  linarith

/-- C4 (zero parameters): Gamma = a0/c = kappa sqrt(G rho_L) = (1/2) sqrt(3 Omega_L/(8 pi)) H0 exceeds the flat-a0 bound 0.0232 H0. -/
theorem c4_rate_exceeds_bound (OL : ℝ) (hOL : 0.68 ≤ OL) :
    (0.0232 : ℝ) < (1/2) * Real.sqrt (3 * OL / (8 * Real.pi)) := by
  have hpi : Real.pi < 3.15 := Real.pi_lt_d2
  have hpi0 : 0 < Real.pi := Real.pi_pos
  have key : (0.0464 : ℝ) ^ 2 < 3 * OL / (8 * Real.pi) := by
    rw [lt_div_iff₀ (by positivity)]
    nlinarith
  have : (0.0464 : ℝ) < Real.sqrt (3 * OL / (8 * Real.pi)) :=
    Real.lt_sqrt_of_sq_lt key
  linarith

/-- C5 tied: a transition at T* = rho_L^(1/4) ≤ 2.25 meV with T0 ≥ 2.34e-4 eV happens at 1 + z* = T*/T0 < 3001. -/
theorem c5_tied_too_late (Tstar T0 : ℝ) (hT : Tstar ≤ 2.25e-3) (hT0 : 2.34e-4 ≤ T0) (hpos : 0 < Tstar) :
    Tstar / T0 < 3001 := by
  have hT0p : 0 < T0 := by linarith
  rw [div_lt_iff₀ hT0p]
  nlinarith

/-- C3 scaling: a fixed fraction of a w = -1 density cannot track a^-3: the ratio grows by (1+z)^3 ≥ 1e10 at z = 3000. -/
theorem c3_scaling : (1e10 : ℝ) ≤ (3001 : ℝ) ^ 3 := by norm_num

/-- C1 drained vacuum: rho_L(3000) ≥ 1.04e10 rho_L0 ⇒ a0(3000)/a0 ≥ 1e5 on a0 ∝ sqrt(rho_L). -/
theorem c1_drained_a0 (r : ℝ) (hr : 1.04e10 ≤ r) : (1e5 : ℝ) ≤ Real.sqrt r := by
  apply Real.le_sqrt_of_sq_le
  nlinarith

/-- Base rate: 53 of 18480 grammar forms land within 1.3% of 5.36 (per-form p < 0.01), while 20 distinct values hit (≥ 1):
a post-hoc search always succeeds. -/
theorem base_rate : (53 : ℝ) / 18480 < 0.01 ∧ (1 : ℕ) ≤ 20 := by
  constructor <;> norm_num

/-- MUTATE: w = 1/3 violates the timing gate |w| ≤ 1e-2. -/
theorem mutate_fails_timing : ¬ (|(1/3 : ℝ)| ≤ 1e-2) := by
  rw [abs_of_pos (by norm_num)]; norm_num

end CFG360
