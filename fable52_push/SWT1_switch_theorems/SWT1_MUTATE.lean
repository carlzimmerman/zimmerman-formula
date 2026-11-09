/-
SWT1 MUTATE twin: false versions of five SWT1 statements, with the proofs that close the true ones. This file must FAIL to compile.
  exterior_mass_M : the uncompensated reading (the retained phantom counted outside the switch radius)
  wall_identity_M : the Legendre combination with the sign of the source term flipped
  W_le_y_M        : W <= y / 2
  qC_bound_M      : q_C <= f / (1 - f)
  crossover_M     : nu(y) = 1 + R iff y = 1 / R^2
kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace SWT1M

noncomputable def nu (y : ℝ) : ℝ := 1 / 2 + Real.sqrt (1 / 4 + 1 / y)
noncomputable def W (u : ℝ) : ℝ := u - Real.log (1 + u) - u ^ 2 / (2 * (1 + u) ^ 2)
noncomputable def gN (G Mb r : ℝ) : ℝ := G * Mb / r ^ 2
noncomputable def gS (G Mb a0 R r : ℝ) : ℝ :=
  if r < R then nu (gN G Mb r / a0) * gN G Mb r else gN G Mb r
noncomputable def Meff (G Mb a0 R r : ℝ) : ℝ := r ^ 2 * gS G Mb a0 R r / G

theorem exterior_mass_M (G Mb a0 R r : ℝ) (hG : 0 < G) (hr : 0 < r) (hRr : R ≤ r) :
    Meff G Mb a0 R r = Mb * nu (G * Mb / R ^ 2 / a0) := by
  unfold Meff gS gN
  simp only [not_lt.mpr hRr, ite_false]
  field_simp

theorem wall_identity_M (u : ℝ) (hu : 0 ≤ u) :
    (u - Real.log (1 + u)) - u ^ 2 / 2 - (u ^ 2 / (1 + u)) * u - (u ^ 2 / (1 + u)) ^ 2 / 2 = W u := by
  unfold W
  have h : (1 + u) ≠ 0 := by positivity
  field_simp
  ring

theorem W_le_y_M (u : ℝ) (hu : 0 ≤ u) : W u ≤ u ^ 2 / (1 + u) / 2 := by
  unfold W
  have hp : 0 < 1 + u := by linarith
  have hlog : 1 - (1 + u)⁻¹ ≤ Real.log (1 + u) := Real.one_sub_inv_le_log_of_pos hp
  have h2 : 0 ≤ u ^ 2 / (2 * (1 + u) ^ 2) := by positivity
  have h3 : u - (1 - (1 + u)⁻¹) = u ^ 2 / (1 + u) := by
    field_simp
    ring
  linarith

theorem qC_bound_M (f β : ℝ) (hf1 : f < 1) (hβ : -(f / 2) ≤ β) :
    (1 - β) / (1 + 2 * β) - 1 ≤ f / (1 - f) := by
  have h1 : 0 < 1 + 2 * β := by linarith
  have h2 : 0 < 1 - f := by linarith
  have h1' : (1 + 2 * β) ≠ 0 := h1.ne'
  have key : (1 - β) / (1 + 2 * β) - 1 = (1 - β - (1 + 2 * β)) / (1 + 2 * β) := by
    have h := div_mul_cancel₀ (1 - β) h1'
    rw [eq_div_iff h1']
    linear_combination h
  rw [key, div_le_div_iff₀ h1 h2]
  nlinarith

theorem crossover_M (y R : ℝ) (hy : 0 < y) (hR : 0 < R) : nu y = 1 + R ↔ y = 1 / R ^ 2 := by
  unfold nu
  have h0 : (0 : ℝ) ≤ 1 / 4 + 1 / y := by positivity
  have h1 : (0 : ℝ) ≤ 1 / 2 + R := by linarith
  have hRR : 0 < R ^ 2 := by positivity
  constructor
  · intro h
    have hs : Real.sqrt (1 / 4 + 1 / y) = 1 / 2 + R := by linarith
    have h2 := (Real.sqrt_eq_iff_mul_self_eq h0 h1).mp hs
    have hy' : 1 / y = R ^ 2 := by nlinarith
    rw [eq_div_iff hRR.ne', ← hy']
    field_simp
  · intro h
    have hs : Real.sqrt (1 / 4 + 1 / y) = 1 / 2 + R := by
      rw [Real.sqrt_eq_iff_mul_self_eq h0 h1, h]
      field_simp
      ring
    linarith

end SWT1M
