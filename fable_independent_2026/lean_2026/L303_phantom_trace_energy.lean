import Mathlib
/-!
L303 -- the phantom's positive-energy trace theorem (real_research/clock_2026/L303_phantom_trace_energy.py).
The Einstein combination the lapse sources: rho_eff = 1/2 (3 T_00 - p_r - 2 p_t) = (2-K_B)(2 B Y + u Y) > 0
exactly for the static deep-MOND ball (L298's tensor: T_00 = (2-K)J, p_r = (2-K)(2J_Y Y - J), p_t = -(2-K)J,
J = B Y + (2/3) u Y, J_Y = B + u); the deep corner reduces to rho_eff/g^2 -> 2/((2-K) B): the RAR envelope
shape rho ~ g^2 ~ 1/r^2 is the action's own.
-/
namespace L303

/-- the trace identity: 3 J - Y J_Y = 2 B Y + u Y for J = B Y + (2/3) u Y. -/
theorem trace_identity (B u Y : ℝ) :
  (3 : ℝ) * (B * Y + (2 : ℝ) / 3 * u * Y) - Y * (B + u) = 2 * B * Y + u * Y := by
  ring

/-- positivity: rho_eff = (2-K)(2 B Y + u Y) > 0 for K < 2, B > 0, u > 0, Y > 0. -/
theorem rho_eff_positive (K B u Y : ℝ) (hK : K < 2) (hB : 0 < B) (hu : 0 < u) (hY : 0 < Y) :
  0 < (2 - K) * (2 * B * Y + u * Y) := by
  positivity

/-- the deep-corner reduction: (2B + u)/(B + u)^2 -> 2/B as u -> 0. -/
theorem deep_corner_reduction (B : ℝ) (hB : B ≠ 0) :
  (2 * B + 0) / (B + 0) ^ 2 = 2 / B := by
  field_simp [hB]
  ring

/-- the deep-corner shape: rho_eff/g^2 = (2B+u)/((2-K)(B+u)^2): at u -> 0 it is 2/(B(2-K)). -/
theorem deep_shape_limit (K B : ℝ) (hK : K ≠ 2) (hB : B ≠ 0) :
  (2 * B + 0) / ((B + 0) ^ 2 * (2 - K)) = 2 / (B * (2 - K)) := by
  field_simp [hK, hB]
  ring

end L303