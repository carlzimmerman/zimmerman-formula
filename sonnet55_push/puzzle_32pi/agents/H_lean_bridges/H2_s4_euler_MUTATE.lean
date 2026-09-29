import Mathlib
import H1_bpst
import H2_s4_euler

/-! MUTATE controls for H2_s4_euler.lean: each `M2*` is a FALSE variant with the true proof script (must FAIL);
each `M2*_refuted` proves its negation from the true theorem (must COMPILE). -/

open MeasureTheory Set Real

-- M2a: Vol(S^4_L) = 8 pi^2 L^4/3, not 4 pi^2 L^4/3
theorem M2a_volS4_wrong (L : ℝ) : volS4 L = 4 * π ^ 2 * L ^ 4 / 3 := by
  unfold volS4; rw [int_sin_cube, int_sin_sq, int_sin]; ring

theorem M2a_refuted : ¬ (∀ L : ℝ, volS4 L = 4 * π ^ 2 * L ^ 4 / 3) := by
  intro h
  have h1 := h 1
  rw [volS4_eq] at h1
  have := Real.pi_pos
  nlinarith [sq_pos_of_pos this]

-- M2b: the Euler density of the round S^4 is 24 k^2 (not 12 k^2): the Riem^2 contraction is 24 k^2
theorem M2b_riem2_wrong (k : ℝ) : riem2 k = 12 * k ^ 2 := by
  simp [riem2, riem, dl, Fin.sum_univ_four]; ring

theorem M2b_refuted : ¬ (riem2 1 = 12 * 1 ^ 2) := by
  rw [riem2_eq]; norm_num

theorem M2c_E4_wrong (k : ℝ) : E4 k = 12 * k ^ 2 := by
  unfold E4; rw [scal_eq, ric2_eq, riem2_eq]; ring

theorem M2c_refuted : ¬ (E4 1 = 12 * 1 ^ 2) := by
  rw [E4_eq]; norm_num

-- M2d: the integral is 64 pi^2, not 32 pi^2 (chi = 2 already inside), for every L
theorem M2d_integral_wrong {L : ℝ} (hL : L ≠ 0) : E4 (1 / L ^ 2) * volS4 L = 32 * π ^ 2 := by
  rw [E4_eq, volS4_eq]; field_simp; ring

theorem M2d_refuted {L : ℝ} (hL : L ≠ 0) : ¬ (E4 (1 / L ^ 2) * volS4 L = 32 * π ^ 2) := by
  intro h; rw [s4_euler_integral hL] at h
  have := Real.pi_pos
  nlinarith [sq_pos_of_pos this]

-- M2e: chi = 2 (not 3)
theorem M2e_chi_wrong {L : ℝ} (hL : L ≠ 0) : E4 (1 / L ^ 2) * volS4 L = 32 * π ^ 2 * 3 := by
  rw [s4_euler_integral hL]; ring

theorem M2e_refuted {L : ℝ} (hL : L ≠ 0) : ¬ (E4 (1 / L ^ 2) * volS4 L = 32 * π ^ 2 * 3) := by
  intro h; rw [s4_euler_integral hL] at h
  have := Real.pi_pos
  nlinarith [sq_pos_of_pos this]

-- M2f: the general-dimension identity with a wrong factor
theorem M2f_general_dim_wrong (n : ℝ) :
    (n * (n - 1)) ^ 2 - 4 * (n * (n - 1) ^ 2) + 2 * (n * (n - 1)) = n * (n - 1) * (n - 2) * (n - 2) := by ring

theorem M2f_refuted : ¬ (∀ n : ℝ, (n * (n - 1)) ^ 2 - 4 * (n * (n - 1) ^ 2) + 2 * (n * (n - 1)) = n * (n - 1) * (n - 2) * (n - 2)) := by
  intro h; have := h 4; norm_num at this

-- M2g: 32 pi^2 = int R dV needs the factor 12: 10 Vol(S^4_1) is wrong
theorem M2g_wrong : 10 * volS4 1 = 32 * π ^ 2 := by
  rw [volS4_eq]; ring

theorem M2g_refuted : ¬ (10 * volS4 1 = 32 * π ^ 2) := by
  intro h; rw [volS4_eq] at h
  have := Real.pi_pos
  nlinarith [sq_pos_of_pos this]

#print axioms M2a_refuted
#print axioms M2b_refuted
#print axioms M2c_refuted
#print axioms M2d_refuted
#print axioms M2e_refuted
#print axioms M2f_refuted
#print axioms M2g_refuted
#print axioms M2a_volS4_wrong
#print axioms M2b_riem2_wrong
#print axioms M2c_E4_wrong
#print axioms M2d_integral_wrong
#print axioms M2e_chi_wrong
#print axioms M2f_general_dim_wrong
#print axioms M2g_wrong
