import Mathlib

/-! VR1 MUTATE twin: false versions of the certified statements. EACH must FAIL to compile.
  M1 the Jeans option of V1 (q = π) gives κ² = ¼ (false: κ² = 1/(4π));
  M2 V2's no-root bound also holds at A* = 2cH, f² = 4 (false: a root exists, κ ≈ 11.18 in vr1.out);
  M3 V3 at r = 1 gives κ² = ¼ (false: κ² = 4π/(1 - ln 2));
  M4 KA-1 with the response factor 1 instead of 2 still gives κ·2ξ = 1 (false: κ ξ = 1). -/

open Real

namespace VR1Mutate

theorem M1_jeans_gives_half (κ : ℝ) (hk : κ ^ 2 * (4 * π) = 1) : κ ^ 2 = 1 / 4 := by
  nlinarith [pi_gt_three]

theorem h_le_sq (u : ℝ) (hu : 0 ≤ u) : u - Real.log (1 + u) ≤ u ^ 2 := by
  have h1 : 0 < 1 + u := by linarith
  have hl := Real.one_sub_inv_le_log_of_pos h1
  have hinv : (1 + u)⁻¹ ≤ 1 - u + u ^ 2 := by
    rw [inv_le_iff_one_le_mul₀' h1]; nlinarith [pow_nonneg hu 3, sq_nonneg u]
  linarith

theorem M2_no_root_at_2cH (κ u : ℝ) (hu : 0 ≤ u)
    (h1 : 4 * π = κ ^ 2 * (u - Real.log (1 + u))) (h2 : κ ^ 2 * u ^ 2 = 4 * (8 * π / 3)) : False := by
  have hb := h_le_sq u hu
  have hk : 0 ≤ κ ^ 2 := sq_nonneg κ
  have : κ ^ 2 * (u - Real.log (1 + u)) ≤ κ ^ 2 * u ^ 2 := mul_le_mul_of_nonneg_left hb hk
  have hp := pi_pos
  nlinarith

theorem M3_equipartition_half (κ : ℝ) (h : κ ^ 2 * (1 - Real.log 2) = 4 * π) : κ ^ 2 = 1 / 4 := by
  have hl : 0 < Real.log 2 := Real.log_pos (by norm_num)
  nlinarith [pi_gt_three]

theorem M4_factor_one (κ ξ a0 ℓ c G ρ : ℝ) (hκ : 0 < κ) (hξ : 0 < ξ) (hc : 0 < c)
    (ht : a0 ^ 2 = κ ^ 2 * G * ρ * c ^ 2) (hl : ℓ ^ 2 * (G * ρ) = c ^ 2) (resp : ξ * ℓ * a0 = c ^ 2) :
    κ * (2 * ξ) = 1 := by
  have hsq : (ξ * ℓ * a0) ^ 2 = (c ^ 2) ^ 2 := by rw [resp]
  have e1 : ξ ^ 2 * (ℓ ^ 2 * (G * ρ)) * κ ^ 2 * c ^ 2 = (c ^ 2) ^ 2 := by
    rw [← hsq, mul_pow, ht]; ring
  rw [hl] at e1
  nlinarith [e1, hκ, hξ, hc]

end VR1Mutate
