import Mathlib

/-!
# VR1 (2026-11-08): vacuum-response identities for κ in a₀ = κ c √(G ρ)

`Framework` is copied verbatim from `KAPPA_LOGIC_2026_10_20.lean` (premises einstein, friedmann, tie, fourform).
Each candidate below ADDS one premise to it. Proved (standard axioms, no sorry):

* `ka1_reduction`  (KA-1, KF1): a₀ = c²/(2 ξ ℓ), ℓ² G ρ = c²  ⟹  κ = 1/(2ξ). κ = ½ iff ξ = 1: RESTATEMENT.
* `vr_not_derivable`: adding the kinematic response length L_v = c²/(2 a₀) (AC2q: grad ln X = -2A/c²) leaves κ free.
* `v1_general`: response length = a vacuum length with ℓ_v² G ρ = q c²  ⟹  κ² = 1/(4q); `v1_half_iff`: κ² = ¼ ⟺ q = 1.
  `v1_options_not_half`: none of the six declared GR/Newtonian vacuum lengths has q = 1.
* `v2_no_root`: J(Y*) = 0 at A* = f c H with f² ≤ 1 has no solution for any κ > 0 (covers c H and c H/2π).
* `v3_not_half`: switch equipartition |ε_J(1)| = r ρ c² with r ≥ ½ forces κ² ≥ 2π, never ¼.
Logic certifies premises ⟹ conclusions only. κ = ½ FITTED; not theory closed.
-/

open Real

namespace VR1

structure Framework (b0 c G ρ a0 Λ H β Z κ : ℝ) : Prop where
  pos : 0 < c ∧ 0 < G ∧ 0 < ρ ∧ 0 < a0 ∧ 0 < H ∧ 0 < β ∧ 0 < Z ∧ 0 < κ ∧ 0 < b0
  einstein : Λ = 8 * π * G * ρ / c ^ 2
  friedmann : H ^ 2 = 8 * π * G * ρ / 3
  tie : a0 ^ 2 = κ ^ 2 * G * ρ * c ^ 2
  fourform : κ ^ 2 = 2 * β ^ 2 / (Z + 2 * b0 * β ^ 2)

/-- KA-1: the KF1 reduction. -/
theorem ka1_reduction {b0 c G ρ a0 Λ H β Z κ ξ ℓ : ℝ} (h : Framework b0 c G ρ a0 Λ H β Z κ)
    (hξ : 0 < ξ) (_hℓ : 0 < ℓ) (hl : ℓ ^ 2 * (G * ρ) = c ^ 2) (resp : 2 * ξ * ℓ * a0 = c ^ 2) :
    κ * (2 * ξ) = 1 := by
  obtain ⟨⟨hc, hG, hρ, ha, -, -, -, hκ, -⟩, -, -, ht, -⟩ := h
  have hsq : (2 * ξ * ℓ * a0) ^ 2 = (c ^ 2) ^ 2 := by rw [resp]
  have e1 : 4 * ξ ^ 2 * (ℓ ^ 2 * (G * ρ)) * κ ^ 2 * c ^ 2 = (c ^ 2) ^ 2 := by
    rw [← hsq]; rw [mul_pow, ht]; ring
  rw [hl] at e1
  have hc4 : 0 < (c ^ 2) ^ 2 := by positivity
  have e2 : (κ * (2 * ξ)) ^ 2 = 1 := by
    have : (c ^ 2) ^ 2 * ((κ * (2 * ξ)) ^ 2 - 1) = 0 := by linear_combination e1
    rcases mul_eq_zero.mp this with h0 | h0
    · exact absurd h0 hc4.ne'
    · linarith
  have hp : 0 < κ * (2 * ξ) := by positivity
  nlinarith [e2, hp]

theorem ka1_half_iff (ξ κ : ℝ) (_hξ : 0 < ξ) (hk : κ * (2 * ξ) = 1) : κ = 1 / 2 ↔ ξ = 1 := by
  constructor
  · intro h; rw [h] at hk; linarith
  · intro h; rw [h] at hk; linarith

/-- The kinematic response length is κ-free: adding it keeps κ = ½ and κ = ⅓ both realised. -/
theorem vr_not_derivable :
    (∃ c G ρ a0 Λ H β Z κ Lv : ℝ, Framework (9 / 500) c G ρ a0 Λ H β Z κ ∧ Lv * (2 * a0) = c ^ 2 ∧ κ = 1 / 2) ∧
    (∃ c G ρ a0 Λ H β Z κ Lv : ℝ, Framework (9 / 500) c G ρ a0 Λ H β Z κ ∧ Lv * (2 * a0) = c ^ 2 ∧ κ ≠ 1 / 2) := by
  have mk : ∀ κ : ℝ, 0 < κ → κ ^ 2 * (9 / 500) < 1 →
      Framework (9 / 500) 1 1 1 κ (8 * π) (Real.sqrt (8 * π / 3)) 1 (2 / κ ^ 2 - 2 * (9 / 500)) κ := by
    intro κ hκ hκb
    have hk2 : 0 < κ ^ 2 := pow_pos hκ 2
    have hZ : 0 < 2 / κ ^ 2 - 2 * (9 / 500 : ℝ) := by
      rw [sub_pos, lt_div_iff₀ hk2]; nlinarith [hκb]
    refine ⟨⟨one_pos, one_pos, one_pos, hκ, Real.sqrt_pos.mpr (by positivity), one_pos, hZ, hκ, by norm_num⟩,
      ?_, ?_, ?_, ?_⟩
    · ring
    · rw [Real.sq_sqrt (by positivity)]; ring
    · ring
    · have hden : 2 / κ ^ 2 - 2 * (9 / 500 : ℝ) + 2 * (9 / 500) * 1 ^ 2 = 2 / κ ^ 2 := by ring
      rw [hden, div_div_eq_mul_div]; ring
  refine ⟨⟨1, 1, 1, 1 / 2, 8 * π, _, 1, _, 1 / 2, 1, mk (1 / 2) (by norm_num) (by norm_num), by norm_num, rfl⟩,
    ⟨1, 1, 1, 1 / 3, 8 * π, _, 1, _, 1 / 3, 3 / 2, mk (1 / 3) (by norm_num) (by norm_num), by norm_num, by norm_num⟩⟩

/-- V1: response length c²/(2a₀) equals a vacuum length with ℓ_v² G ρ = q c². -/
theorem v1_general {b0 c G ρ a0 Λ H β Z κ ℓv q : ℝ} (h : Framework b0 c G ρ a0 Λ H β Z κ)
    (_hq : 0 < q) (hl : ℓv ^ 2 * (G * ρ) = q * c ^ 2) (resp : 2 * ℓv * a0 = c ^ 2) :
    κ ^ 2 * (4 * q) = 1 := by
  obtain ⟨⟨hc, hG, hρ, ha, -, -, -, hκ, -⟩, -, -, ht, -⟩ := h
  have hsq : (2 * ℓv * a0) ^ 2 = (c ^ 2) ^ 2 := by rw [resp]
  have e1 : 4 * (ℓv ^ 2 * (G * ρ)) * κ ^ 2 * c ^ 2 = (c ^ 2) ^ 2 := by
    rw [← hsq, mul_pow, ht]; ring
  rw [hl] at e1
  have hc4 : 0 < (c ^ 2) ^ 2 := by positivity
  have : (c ^ 2) ^ 2 * (κ ^ 2 * (4 * q) - 1) = 0 := by linear_combination e1
  rcases mul_eq_zero.mp this with h0 | h0
  · exact absurd h0 hc4.ne'
  · linarith

theorem v1_half_iff (κ q : ℝ) (_hq : 0 < q) (hk : κ ^ 2 * (4 * q) = 1) : κ ^ 2 = 1 / 4 ↔ q = 1 := by
  constructor
  · intro h; rw [h] at hk; linarith
  · intro h; rw [h] at hk; linarith

/-- the six declared vacuum lengths: q = 3/(8π) (c/H), 1/(4π) (Poisson), 3π/32 (c t_ff), π (Jeans),
1/(8π) (1/√Λ), 3π/2 (2πc/H). None equals 1. -/
theorem v1_options_not_half :
    (3 / (8 * π) ≠ 1) ∧ (1 / (4 * π) ≠ 1) ∧ (3 * π / 32 ≠ 1) ∧ (π ≠ 1) ∧ (1 / (8 * π) ≠ 1) ∧ (3 * π / 2 ≠ 1) := by
  have h3 := pi_gt_three
  have h4 := pi_le_four
  have hp : 0 < π := pi_pos
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · rw [ne_eq, div_eq_one_iff_eq (by positivity)]; intro h; linarith
  · rw [ne_eq, div_eq_one_iff_eq (by positivity)]; intro h; linarith
  · intro h; linarith [show 3 * π = 32 by linarith [(div_eq_one_iff_eq (by norm_num : (32:ℝ) ≠ 0)).mp h]]
  · intro h; linarith
  · rw [ne_eq, div_eq_one_iff_eq (by positivity)]; intro h; linarith
  · intro h; linarith [show 3 * π = 2 by linarith [(div_eq_one_iff_eq (by norm_num : (2:ℝ) ≠ 0)).mp h]]

/-- u - log(1+u) ≤ u² for u ≥ 0. -/
theorem h_le_sq (u : ℝ) (hu : 0 ≤ u) : u - Real.log (1 + u) ≤ u ^ 2 := by
  have h1 : 0 < 1 + u := by linarith
  have hl := Real.one_sub_inv_le_log_of_pos h1
  have hinv : (1 + u)⁻¹ ≤ 1 - u + u ^ 2 := by
    rw [inv_le_iff_one_le_mul₀' h1]; nlinarith [pow_nonneg hu 3, sq_nonneg u]
  linarith

/-- V2 bridge: einstein + tie + friedmann + cancellation J(Y*) = 0 at u* a₀ = f c H give the reduced pair. -/
theorem v2_reduce {b0 c G ρ a0 Λ H β Z κ u f : ℝ} (h : Framework b0 c G ρ a0 Λ H β Z κ)
    (cancel : Λ = 2 * (a0 / c ^ 2) ^ 2 * (u - Real.log (1 + u))) (hu : u * a0 = f * c * H) :
    4 * π = κ ^ 2 * (u - Real.log (1 + u)) ∧ κ ^ 2 * u ^ 2 = f ^ 2 * (8 * π / 3) := by
  obtain ⟨⟨hc, hG, hρ, ha, -, -, -, hκ, -⟩, he, hf, ht, -⟩ := h
  have hc0 := hc.ne'
  constructor
  · rw [he, div_pow, ht] at cancel
    field_simp at cancel
    linarith [cancel]
  · have hsq : u ^ 2 * a0 ^ 2 = f ^ 2 * c ^ 2 * H ^ 2 := by
      calc u ^ 2 * a0 ^ 2 = (u * a0) ^ 2 := by ring
        _ = (f * c * H) ^ 2 := by rw [hu]
        _ = f ^ 2 * c ^ 2 * H ^ 2 := by ring
    rw [ht, hf] at hsq
    have : (G * ρ * c ^ 2) * (κ ^ 2 * u ^ 2 - f ^ 2 * (8 * π / 3)) = 0 := by linear_combination hsq
    rcases mul_eq_zero.mp this with h0 | h0
    · exact absurd h0 (by positivity)
    · linarith

/-- V2: no root for f² ≤ 1 (A* = cH, cH/2π). -/
theorem v2_no_root (κ u f : ℝ) (hu : 0 ≤ u) (hf : f ^ 2 ≤ 1)
    (h1 : 4 * π = κ ^ 2 * (u - Real.log (1 + u))) (h2 : κ ^ 2 * u ^ 2 = f ^ 2 * (8 * π / 3)) : False := by
  have hb := h_le_sq u hu
  have hk : 0 ≤ κ ^ 2 := sq_nonneg κ
  have : κ ^ 2 * (u - Real.log (1 + u)) ≤ κ ^ 2 * u ^ 2 := mul_le_mul_of_nonneg_left hb hk
  have hp := pi_pos
  nlinarith

/-- V3: |ε_J(1)| = (a₀²/4πG)(1 - ln 2) = r ρ c² with r ≥ ½ gives κ² (1 - ln 2) = 4π r, so κ² ≥ 2π > ¼. -/
theorem v3_not_half (κ r : ℝ) (hr : 1 / 2 ≤ r) (h : κ ^ 2 * (1 - Real.log 2) = 4 * π * r) : κ ^ 2 ≠ 1 / 4 := by
  intro hk
  rw [hk] at h
  have hl : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have hp := pi_gt_three
  nlinarith

end VR1

#print axioms VR1.ka1_reduction
#print axioms VR1.vr_not_derivable
#print axioms VR1.v1_general
#print axioms VR1.v1_options_not_half
#print axioms VR1.v2_reduce
#print axioms VR1.v2_no_root
#print axioms VR1.v3_not_half
