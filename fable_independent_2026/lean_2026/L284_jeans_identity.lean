import Mathlib
/-!
L284 (CK12, perturbations I) -- the algebraic core (real_research/clock_2026/L284_dust_perturbations.py).
For a Q-well F with slope F1 = F_Q(Qbar) and curvature F2 = F_QQ(Qbar) at the rolling background Qbar:
(1) the dust density 16 pi G rho_d = -Qbar F1 (the well's value F0 = O(q^2) dropped);
(2) the k-essence sound speed c_s^2 = F1/(Qbar F2) (delta p/delta rho of the well);
(3) the static pole of the lapse in the Newtonian regime, mu^2 = -F2 Qbar^2/(2 (2 - c14))  (L283's pole with K2 -> F2/2, J_Y -> infinity);
(4) THE JEANS IDENTITY: mu^2 c_s^2 = 4 pi G_N rho_d with G_N = G/(1 - c14/2)  -- L283's 'mass of the Newtonian potential' is the dust's
    Jeans wavenumber (pressure support below 1/mu, collapse above), so a SMALL 1/mu is what structure formation wants.
(5) the well scalings: c_s^2 = q/((n-1) Qbar) for F = -(Q-Q0)^n/L^(n-2), so the quadratic well (n = 2) has c_s^2 = q/Qbar.
-/
namespace L284

/-- (4) the Jeans identity, as a ring identity on the defining expressions -/
theorem jeans_identity (F1 F2 Qbar c14 G π : ℝ) (hF2 : F2 ≠ 0) (hQ : Qbar ≠ 0) (hc : 2 - c14 ≠ 0) :
    let mu2 := -F2 * Qbar ^ 2 / (2 * (2 - c14))
    let cs2 := F1 / (Qbar * F2)
    let rho_d := -Qbar * F1 / (16 * π * G)
    let GN := G / (1 - c14 / 2)
    (hG : G ≠ 0) → (hπ : π ≠ 0) → mu2 * cs2 = 4 * π * GN * rho_d := by
  intro mu2 cs2 rho_d GN hG hπ
  simp only [mu2, cs2, rho_d, GN]
  have h1 : (1 - c14 / 2) ≠ 0 := by
    intro h; apply hc; linarith
  field_simp
  ring

/-- (5) the sound speed of the power-law well: F = -(Q-Q0)^n / L^(n-2) at Q = Q0 + q gives F_Q/(Q F_QQ) = q/((n-1) Q) -/
theorem power_well_sound_speed (q Q L : ℝ) (n : ℕ) (hn : 2 ≤ n) (hq : q ≠ 0) (hQ : Q ≠ 0) (hL : L ≠ 0) :
    let FQ := -(n : ℝ) * q ^ (n - 1) / L ^ (n - 2)
    let FQQ := -(n : ℝ) * ((n : ℝ) - 1) * q ^ (n - 2) / L ^ (n - 2)
    FQ / (Q * FQQ) = q / (((n : ℝ) - 1) * Q) := by
  intro FQ FQQ
  simp only [FQ, FQQ]
  have hn1 : ((n : ℝ) - 1) ≠ 0 := by
    have : (2 : ℝ) ≤ n := by exact_mod_cast hn
    intro h; linarith
  have hn0 : (n : ℝ) ≠ 0 := by
    have : (2 : ℝ) ≤ n := by exact_mod_cast hn
    intro h; linarith
  have hpow : q ^ (n - 1) = q ^ (n - 2) * q := by
    rw [← pow_succ]; congr 1; omega
  rw [hpow]
  field_simp

/-- the quadratic well: c_s^2 = q/Qbar, so at the BBN floor of L283 (q/Qbar = 3 Om_dm H0^2/(|K2| Q0^2) <= 3 Om_dm/1.8e23) the dust is
    cold at every epoch that matters: c_s^2 (z) = (q0/Qbar) (1+z)^3 -/
theorem quadratic_well_cold (q0 Qbar z : ℝ) (hq : 0 ≤ q0 / Qbar) (hz : 0 ≤ z) (hb : q0 / Qbar ≤ 3 * 0.26 / 1.783e23) (hz1 : z ≤ 1100) :
    (q0 / Qbar) * (1 + z) ^ 3 ≤ 1e-9 := by
  have h3 : (1 + z) ^ 3 ≤ (1101 : ℝ) ^ 3 := by
    have hz' : 1 + z ≤ 1101 := by linarith
    have hz0 : 0 ≤ 1 + z := by linarith
    gcongr
  calc (q0 / Qbar) * (1 + z) ^ 3 ≤ (3 * 0.26 / 1.783e23) * (1101 : ℝ) ^ 3 :=
        mul_le_mul hb h3 (by positivity) (by norm_num)
    _ ≤ 1e-9 := by norm_num

end L284
#print axioms L284.jeans_identity
#print axioms L284.power_well_sound_speed
#print axioms L284.quadratic_well_cold
