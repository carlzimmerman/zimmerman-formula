import Mathlib
/-!
L298 -- the phantom's stress tensor; the algebraic core of the null-tangential theorem and the EoS window
(real_research/clock_2026/L298_phantom_stress_tensor.py, 4/4).  The static deep-MOND ball of THE_ACTION's
scalar:  rho = (2-K_B) J,  p_r = (2-K_B)(2 J_Y Y - J) = (2-K_B)(B Y + (4/3) u Y),  p_t = -(2-K_B) J
with J = B Y + (2/3) u Y, u = sqrt(Y)/a0t > 0, B = beta0 > 0, K_B < 2: the same forms as the machine lane.
-/
namespace L298

theorem null_tangential (K J : ℝ) : (2 - K) * J + (-(2 - K) * J) = 0 := by
  ring

theorem w_num_form (B u Y J : ℝ) (hJ : J = B * Y + (2 : ℝ) / 3 * u * Y) :
  (2 : ℝ) * (B + u) * Y - J = B * Y + (4 : ℝ) / 3 * u * Y := by
  rw [hJ]
  ring

theorem w_ge_one (B u Y : ℝ) (hB : 0 < B) (hu : 0 ≤ u) (hY : 0 < Y) :
  1 ≤ (B * Y + (4 : ℝ) / 3 * u * Y) / (B * Y + (2 : ℝ) / 3 * u * Y) := by
  have hBY : 0 < B * Y := mul_pos hB hY
  have hu2 : 0 ≤ (2 : ℝ) / 3 * u * Y := by positivity
  have hd : 0 < B * Y + (2 : ℝ) / 3 * u * Y := by nlinarith
  have hnum : 0 ≤ B * Y + (4 : ℝ) / 3 * u * Y - (B * Y + (2 : ℝ) / 3 * u * Y) := by
    have : (2 : ℝ) / 3 * u * Y ≥ 0 := by positivity
    nlinarith
  have hle : (1 : ℝ) * (B * Y + (2 : ℝ) / 3 * u * Y) ≤ B * Y + (4 : ℝ) / 3 * u * Y := by
    nlinarith
  exact (le_div_iff₀ hd).2 hle

theorem w_lt_two (B u Y : ℝ) (hB : 0 < B) (hu : 0 ≤ u) (hY : 0 < Y) :
  (B * Y + (4 : ℝ) / 3 * u * Y) / (B * Y + (2 : ℝ) / 3 * u * Y) < 2 := by
  have hd : 0 < B * Y + (2 : ℝ) / 3 * u * Y := by positivity
  have hlt : B * Y + (4 : ℝ) / 3 * u * Y < 2 * (B * Y + (2 : ℝ) / 3 * u * Y) := by
    have hBY : 0 < B * Y := mul_pos hB hY
    nlinarith
  exact (div_lt_iff₀ hd).2 hlt

theorem beta_ani_gt_one (K B u Y Jp : ℝ) (hK : K < 2) (hB : 0 < B) (hu : 0 ≤ u) (hY : 0 < Y)
    (hJ : Jp = B * Y + (2 : ℝ) / 3 * u * Y) :
  1 < 1 - (-(2 - K) * Jp) / ((2 - K) * (2 * (B + u) * Y - Jp)) := by
  -- p_t = -(2-K) J < 0, p_r > 0:  beta_ani = 1 - p_t/p_r > 1
  have h2K : 0 < 2 - K := by linarith
  have hJp : 0 < Jp := by
    rw [hJ]
    have : (2 : ℝ) / 3 * u * Y ≥ 0 := by positivity
    nlinarith
  have hpr : 0 < (2 - K) * (2 * (B + u) * Y - Jp) := by
    rw [w_num_form B u Y Jp hJ]
    have : (4 : ℝ) / 3 * u * Y ≥ 0 := by positivity
    nlinarith [h2K, hB, hY, hu]
  have hp2 : 0 < ((2 - K) * Jp) / ((2 - K) * (2 * (B + u) * Y - Jp)) := by
    exact div_pos (by nlinarith [h2K, hJp]) hpr
  have hrew : (1 - (-(2 - K) * Jp) / ((2 - K) * (2 * (B + u) * Y - Jp)) : ℝ) =
      1 + ((2 - K) * Jp) / ((2 - K) * (2 * (B + u) * Y - Jp)) := by
    ring
  rw [hrew]
  linarith

end L298