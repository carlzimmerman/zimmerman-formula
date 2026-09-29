import Mathlib
import H7_p09_reduction

/-! MUTATE controls for H7_p09_reduction.lean: each `M7*` is a FALSE variant with the true proof script (must FAIL);
each `M7*_refuted` proves its negation (must COMPILE). -/

open Real Polynomial

-- M7a: G rho = 4 a0^2 <-> U_v = 8 pi (wrong; it is 32 pi)
theorem M7a_selfconsistency_wrong {a0 Uv : ℝ} (ha : a0 ≠ 0) : (a0 ^ 2 * Uv) / (8 * π) = 4 * a0 ^ 2 ↔ Uv = 8 * π := by
  have hp := Real.pi_pos
  have h8 : (8 * π) ≠ 0 := by positivity
  have h2 : a0 ^ 2 ≠ 0 := by positivity
  rw [div_eq_iff h8]
  constructor
  · intro h
    have : a0 ^ 2 * (Uv - 8 * π) = 0 := by linarith
    rcases mul_eq_zero.mp this with h3 | h3
    · exact absurd h3 h2
    · linarith
  · intro h; rw [h]; ring

theorem M7a_refuted : ¬ (∀ a0 Uv : ℝ, a0 ≠ 0 → ((a0 ^ 2 * Uv) / (8 * π) = 4 * a0 ^ 2 ↔ Uv = 8 * π)) := by
  intro h
  have hp := Real.pi_pos
  have := (h 1 (32 * π) one_ne_zero).mp (by field_simp; ring)
  linarith

-- M7b: a quadratic potential with REAL coefficients cannot give 32 pi (false: take gamma = 32 pi)
theorem M7b_real_coefficients_wrong (α β γ : ℝ) (hα : α ≠ 0) (u : ℝ)
    (hcrit : 2 * α * u + β = 0) : α * u ^ 2 + β * u + γ ≠ 32 * π := by
  have hu : u = -β / (2 * α) := by
    field_simp; linarith
  intro h
  rw [hu] at h
  exact Uv_not_rational (0 : ℚ) (by push_cast; linarith)

theorem M7b_refuted : ¬ (∀ (α β γ : ℝ) (u : ℝ), α ≠ 0 → 2 * α * u + β = 0 → α * u ^ 2 + β * u + γ ≠ 32 * π) := by
  intro h
  exact h 1 0 (32 * π) 0 one_ne_zero (by norm_num) (by norm_num)

-- M7c: 32 pi is rational (false)
theorem M7c_Uv_rational : ∃ q : ℚ, (q : ℝ) = 32 * π := by
  refine ⟨32 * 3, ?_⟩
  push_cast
  have := Real.pi_gt_three
  linarith

theorem M7c_refuted : ¬ (∃ q : ℚ, (q : ℝ) = 32 * π) := by
  rintro ⟨q, hq⟩
  exact Uv_not_rational q hq

-- M7d: the vacuum Friedmann relation with 3/8 pi instead of 8 pi/3
theorem M7d_friedmann_wrong {a0 Uv : ℝ} : (3 / (8 * π)) * ((a0 ^ 2 * Uv) / (8 * π)) = (a0 ^ 2 * Uv) / 3 := by
  have hp := Real.pi_pos
  field_simp

theorem M7d_refuted : ¬ (∀ a0 Uv : ℝ, (3 / (8 * π)) * ((a0 ^ 2 * Uv) / (8 * π)) = (a0 ^ 2 * Uv) / 3) := by
  intro h
  have hp := Real.pi_pos
  have h1 := h 1 1
  have h3 := Real.pi_gt_three
  field_simp at h1
  nlinarith [mul_pos hp hp]

#print axioms M7a_refuted
#print axioms M7b_refuted
#print axioms M7c_refuted
#print axioms M7d_refuted
#print axioms M7a_selfconsistency_wrong
#print axioms M7b_real_coefficients_wrong
#print axioms M7c_Uv_rational
#print axioms M7d_friedmann_wrong
