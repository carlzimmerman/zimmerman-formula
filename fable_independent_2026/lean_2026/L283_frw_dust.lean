import Mathlib
/-!
L283 (CK12) -- algebraic core of the FRW background and the dust's fate (real_research/clock_2026/L283_frw_background_and_dust_fate.py).
(1) the scalar's energy density rho = F - Q F_Q for the quadratic well is -K2 (2 Q0 q + q^2): dust plus a stiff term of the SAME sign;
(2) for the quartic well F = -(Q-Q0)^4/L^2 it is (4 Q0 q^3 + 3 q^4)/L^2: dust plus a radiation-like term;
(3) the scaling exponent of the correction, -3n/(n-1): n = 2 -> -6 (stiff), n = 4 -> -4 (radiation);
(4) the static potential with the roll, from the three static equations (hypotheses = the machine's linear equations):
    Psi [(2-c14)(beta-beta0) k^2 + K2 Q0^2 beta] = -8 pi G beta rho, beta0 = (2-K_B)/(2-c14);
(5) the pincer is monotone in the product S = |K2| Q0^2: S >= S_min > 0 -> (2-c14)/S <= (2-c14)/S_min.
-/
namespace L283

theorem rho_quadratic (K2 Q0 q : ℝ) :
    let F := fun Q : ℝ => K2 * (Q - Q0) ^ 2
    let FQ := fun Q : ℝ => 2 * K2 * (Q - Q0)
    F (Q0 + q) - (Q0 + q) * FQ (Q0 + q) = -K2 * (2 * Q0 * q + q ^ 2) := by
  intro F FQ; simp only [F, FQ]; ring

theorem rho_quartic (L Q0 q : ℝ) (hL : L ≠ 0) :
    let F := fun Q : ℝ => -(Q - Q0) ^ 4 / L ^ 2
    let FQ := fun Q : ℝ => -4 * (Q - Q0) ^ 3 / L ^ 2
    F (Q0 + q) - (Q0 + q) * FQ (Q0 + q) = (4 * Q0 * q ^ 3 + 3 * q ^ 4) / L ^ 2 := by
  intro F FQ; simp only [F, FQ]; field_simp; ring

/-- if F_Q ∝ q^(n-1) ∝ a^-3 then q^n ∝ a^(-3n/(n-1)) -/
theorem correction_exponent_quadratic : (-3 : ℚ) * 2 / (2 - 1) = -6 := by norm_num
theorem correction_exponent_quartic : (-3 : ℚ) * 4 / (4 - 1) = -4 := by norm_num
theorem correction_exponent_cubic : (-3 : ℚ) * 3 / (3 - 1) = -9 / 2 := by norm_num

/-- the static lapse with the roll.  Hypotheses: the Hamiltonian constraint in Fourier space (Laplacian -> -k^2) with the
roll term, the traceless equation Phi = Psi, and the scalar's static equation beta P = Psi. -/
theorem static_lapse_with_roll (Psi Phi P k K2 Q0 KB c14 beta G π ρ : ℝ)
    (hH : -4 * k ^ 2 * Phi + 2 * c14 * k ^ 2 * Psi + 2 * (2 - KB) * k ^ 2 * P - 2 * K2 * Q0 ^ 2 * Psi = 16 * π * G * ρ)
    (hT : Phi = Psi) (hP : beta * P = Psi) :
    Psi * (((2 - c14) * beta - (2 - KB)) * k ^ 2 + K2 * Q0 ^ 2 * beta) = -8 * π * G * beta * ρ := by
  rw [hT] at hH
  linear_combination (-beta / 2) * hH + (2 - KB) * k ^ 2 * hP

/-- the same coefficient written with beta0 = (2-K_B)/(2-c14) -/
theorem coefficient_beta0 (KB c14 beta : ℝ) (hc : 2 - c14 ≠ 0) :
    (2 - c14) * (beta - (2 - KB) / (2 - c14)) = (2 - c14) * beta - (2 - KB) := by
  field_simp

/-- the pincer's monotonicity in the product S = |K2| Q0^2 -/
theorem length_bound (S Smin c14 : ℝ) (hS : Smin ≤ S) (hmin : 0 < Smin) (hc : 0 ≤ 2 - c14) :
    (2 - c14) / S ≤ (2 - c14) / Smin :=
  div_le_div_of_nonneg_left hc hmin hS

end L283
#print axioms L283.rho_quadratic
#print axioms L283.rho_quartic
#print axioms L283.static_lapse_with_roll
#print axioms L283.coefficient_beta0
#print axioms L283.length_bound
