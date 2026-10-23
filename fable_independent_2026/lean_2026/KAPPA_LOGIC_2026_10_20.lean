import Mathlib

/-!
# KAPPA_LOGIC_2026_10_20 -- what logic alone can and cannot say about κ in a₀ = κ c √(G ρ_Λ)

Builds on `PUZZLE_32pi_postulate_status_2026_10_05.lean` (κ is independent of the 10-05 ingredients). This file extends
that result to the current framework, which adds k04's four-form promotion of a₀.

Premises (all quantities positive; b0 is k04's kernel constant, b0 = (2 - K_B) I/(16 π) = 0.018):
* `einstein`  : Λ = 8 π G ρ / c²
* `friedmann` : H² = 8 π G ρ / 3                 (the dark-energy de Sitter rate)
* `tie`       : a0² = κ² G ρ c²                  (the form a0 = κ c √(G ρ); κ is the unknown)
* `fourform`  : κ² = 2 β² / (Z + 2 b0 β²)        (k04 F2; the flux amplitude has cancelled)

Proved (standard axioms, no sorry):
1. `every_kappa`: every κ > 0 with κ² b0 < 1 has a model. κ is a free modulus of the premises.
2. `half_not_derivable`: at k04's b0 = 9/500, models exist with κ = ½ and with κ ≠ ½. So κ = ½ is independent.
   `half_not_derivable_with_data`: this stays true after the measured window is added as a premise.
3. Candidate principles. Each one is a NEW premise, and each forces a definite κ²:
   * `p32_iff`  : Λ · π (c²/a0)² = 32 π²  ⟺  κ² = 1/4. This is the 32π puzzle itself, so the premise IS κ = ½.
   * `ph_val`   : 2 π a0 = c H  ⟹  κ² = 2/(3π). Here the Rindler length c²/a0 equals the horizon circumference 2πc/H.
   * `pc1b_val` : a0 = c H  ⟹  κ² = 8π/3. This is p63's C1b, the patch bootstrap with Z = 1.
   * `pc1_val`  : 3 H a0 = 4 π c G ρ  ⟹  κ² = 2π/3. This is p63's C1, the saturated dual polarization in de Sitter.
   * `pc2_val`  : ρ = N² ρ1 and a0² = κ1² G ρ1 c²  ⟹  κ² = κ1²/N². This is p63's C2, the flux lattice.
4. `Win` is CFG493's measured window: 2σ, both footings, written in κ².
   * Inside: ½ (`win_half`) and the 2π form (`win_ph`).
   * Outside: C1b (`not_win_pc1b`) and C1 (`not_win_pc1`).
   * The lattice with κ1 = 1 is inside for N = 2, 3, 4 and outside for N = 1 and for N ≥ 5.
5. `window_does_not_select`: two different principles (κ² = 1/4 and κ² = 2/(3π)) both satisfy the window.

Logic certifies only that premises imply conclusions. It cannot supply a physical premise. κ = ½ stays FITTED.
-/

open Real

structure Framework (b0 c G ρ a0 Λ H β Z κ : ℝ) : Prop where
  pos : 0 < c ∧ 0 < G ∧ 0 < ρ ∧ 0 < a0 ∧ 0 < H ∧ 0 < β ∧ 0 < Z ∧ 0 < κ ∧ 0 < b0
  einstein : Λ = 8 * π * G * ρ / c ^ 2
  friedmann : H ^ 2 = 8 * π * G * ρ / 3
  tie : a0 ^ 2 = κ ^ 2 * G * ρ * c ^ 2
  fourform : κ ^ 2 = 2 * β ^ 2 / (Z + 2 * b0 * β ^ 2)

/-- every κ with κ² b0 < 1 is realised: c = G = ρ = 1, a0 = κ, Λ = 8π, H = √(8π/3), β = 1, Z = 2/κ² - 2 b0 -/
theorem every_kappa (b0 κ : ℝ) (hb : 0 < b0) (hκ : 0 < κ) (hκb : κ ^ 2 * b0 < 1) :
    ∃ c G ρ a0 Λ H β Z : ℝ, Framework b0 c G ρ a0 Λ H β Z κ := by
  have hk2 : 0 < κ ^ 2 := pow_pos hκ 2
  have hZ : 0 < 2 / κ ^ 2 - 2 * b0 := by
    rw [sub_pos, lt_div_iff₀ hk2]
    nlinarith [hκb]
  refine ⟨1, 1, 1, κ, 8 * π, Real.sqrt (8 * π / 3), 1, 2 / κ ^ 2 - 2 * b0,
    ⟨⟨one_pos, one_pos, one_pos, hκ, Real.sqrt_pos.mpr (by positivity), one_pos, hZ, hκ, hb⟩, ?_, ?_, ?_, ?_⟩⟩
  · ring
  · rw [Real.sq_sqrt (by positivity)]; ring
  · ring
  · have hden : 2 / κ ^ 2 - 2 * b0 + 2 * b0 * 1 ^ 2 = 2 / κ ^ 2 := by ring
    rw [hden, div_div_eq_mul_div]; ring

theorem half_not_derivable :
    (∃ c G ρ a0 Λ H β Z κ : ℝ, Framework (9 / 500) c G ρ a0 Λ H β Z κ ∧ κ = 1 / 2) ∧
    (∃ c G ρ a0 Λ H β Z κ : ℝ, Framework (9 / 500) c G ρ a0 Λ H β Z κ ∧ κ ≠ 1 / 2) := by
  obtain ⟨c, G, ρ, a0, Λ, H, β, Z, h⟩ := every_kappa (9 / 500) (1 / 2) (by norm_num) (by norm_num) (by norm_num)
  obtain ⟨c', G', ρ', a0', Λ', H', β', Z', h'⟩ := every_kappa (9 / 500) (1 / 3) (by norm_num) (by norm_num) (by norm_num)
  exact ⟨⟨c, G, ρ, a0, Λ, H, β, Z, 1 / 2, h, rfl⟩, ⟨c', G', ρ', a0', Λ', H', β', Z', 1 / 3, h', by norm_num⟩⟩

theorem p32_iff {b0 c G ρ a0 Λ H β Z κ : ℝ} (h : Framework b0 c G ρ a0 Λ H β Z κ) :
    Λ * (π * (c ^ 2 / a0) ^ 2) = 32 * π ^ 2 ↔ κ ^ 2 = 1 / 4 := by
  obtain ⟨⟨hc, hG, hρ, ha, -, -, -, hκ, -⟩, he, -, ht, -⟩ := h
  have hc0 := hc.ne'; have hG0 := hG.ne'; have hρ0 := hρ.ne'; have hκ0 := hκ.ne'
  have key : Λ * (π * (c ^ 2 / a0) ^ 2) = 8 * π ^ 2 / κ ^ 2 := by
    rw [he, div_pow, ht]
    field_simp
  rw [key, div_eq_iff (pow_pos hκ 2).ne']
  constructor
  · intro h1
    have h2 : π ^ 2 * (32 * κ ^ 2 - 8) = 0 := by linear_combination (-1 : ℝ) * h1
    rcases mul_eq_zero.mp h2 with h3 | h3
    · exact absurd h3 (pow_pos pi_pos 2).ne'
    · linarith
  · intro h1; rw [h1]; ring

theorem ph_val {b0 c G ρ a0 Λ H β Z κ : ℝ} (h : Framework b0 c G ρ a0 Λ H β Z κ)
    (hp : 2 * π * a0 = c * H) : κ ^ 2 = 2 / (3 * π) := by
  obtain ⟨⟨hc, hG, hρ, -, -, -, -, -, -⟩, -, hf, ht, -⟩ := h
  have hsq : 4 * π ^ 2 * a0 ^ 2 = c ^ 2 * H ^ 2 := by
    calc 4 * π ^ 2 * a0 ^ 2 = (2 * π * a0) ^ 2 := by ring
      _ = (c * H) ^ 2 := by rw [hp]
      _ = c ^ 2 * H ^ 2 := by ring
  rw [ht, hf] at hsq
  have h2 : (G * ρ * c ^ 2 * π) * (κ ^ 2 * (3 * π) - 2) = 0 := by
    linear_combination (3 / 4 : ℝ) * hsq
  rw [eq_div_iff (mul_pos (by norm_num : (0:ℝ) < 3) pi_pos).ne']
  rcases mul_eq_zero.mp h2 with h3 | h3
  · exact absurd h3 (mul_pos (mul_pos (mul_pos hG hρ) (pow_pos hc 2)) pi_pos).ne'
  · linarith

theorem pc1b_val {b0 c G ρ a0 Λ H β Z κ : ℝ} (h : Framework b0 c G ρ a0 Λ H β Z κ)
    (hp : a0 = c * H) : κ ^ 2 = 8 * π / 3 := by
  obtain ⟨⟨hc, hG, hρ, -, -, -, -, -, -⟩, -, hf, ht, -⟩ := h
  have hsq : a0 ^ 2 = c ^ 2 * H ^ 2 := by rw [hp]; ring
  rw [ht, hf] at hsq
  have h2 : (G * ρ * c ^ 2) * (κ ^ 2 - 8 * π / 3) = 0 := by linear_combination hsq
  rcases mul_eq_zero.mp h2 with h3 | h3
  · exact absurd h3 (mul_pos (mul_pos hG hρ) (pow_pos hc 2)).ne'
  · linarith

theorem pc1_val {b0 c G ρ a0 Λ H β Z κ : ℝ} (h : Framework b0 c G ρ a0 Λ H β Z κ)
    (hp : 3 * H * a0 = 4 * π * c * G * ρ) : κ ^ 2 = 2 * π / 3 := by
  obtain ⟨⟨hc, hG, hρ, -, -, -, -, -, -⟩, -, hf, ht, -⟩ := h
  have hsq : 9 * H ^ 2 * a0 ^ 2 = 16 * π ^ 2 * c ^ 2 * G ^ 2 * ρ ^ 2 := by
    calc 9 * H ^ 2 * a0 ^ 2 = (3 * H * a0) ^ 2 := by ring
      _ = (4 * π * c * G * ρ) ^ 2 := by rw [hp]
      _ = 16 * π ^ 2 * c ^ 2 * G ^ 2 * ρ ^ 2 := by ring
  rw [ht, hf] at hsq
  have h2 : (G ^ 2 * ρ ^ 2 * c ^ 2 * π) * (κ ^ 2 - 2 * π / 3) = 0 := by
    linear_combination (1 / 24 : ℝ) * hsq
  rcases mul_eq_zero.mp h2 with h3 | h3
  · exact absurd h3 (mul_pos (mul_pos (mul_pos (pow_pos hG 2) (pow_pos hρ 2)) (pow_pos hc 2)) pi_pos).ne'
  · linarith

theorem pc2_val {b0 c G ρ a0 Λ H β Z κ : ℝ} (h : Framework b0 c G ρ a0 Λ H β Z κ)
    {N ρ1 κ1 : ℝ} (hN : 0 < N) (hρ1 : 0 < ρ1) (hsplit : ρ = N ^ 2 * ρ1)
    (hq : a0 ^ 2 = κ1 ^ 2 * G * ρ1 * c ^ 2) : κ ^ 2 = κ1 ^ 2 / N ^ 2 := by
  obtain ⟨⟨hc, hG, -, -, -, -, -, -, -⟩, -, -, ht, -⟩ := h
  rw [hsplit] at ht
  have h2 : (G * ρ1 * c ^ 2) * (κ ^ 2 * N ^ 2 - κ1 ^ 2) = 0 := by linear_combination hq - ht
  rw [eq_div_iff (pow_pos hN 2).ne']
  rcases mul_eq_zero.mp h2 with h3 | h3
  · exact absurd h3 (mul_pos (mul_pos hG hρ1) (pow_pos hc 2)).ne'
  · linarith

/-- CFG493's measured window (2σ, both footings), in κ²: κ_Λ ∈ [0.2280, 0.6064]; κ_crit = κ √Ω_Λ ∈ [0.1886, 0.5018], Ω_Λ = 0.685 -/
def Win (k2 : ℝ) : Prop :=
  (2280 / 10000 : ℝ) ^ 2 ≤ k2 ∧ k2 ≤ (6064 / 10000 : ℝ) ^ 2 ∧
  (1886 / 10000 : ℝ) ^ 2 ≤ k2 * (137 / 200) ∧ k2 * (137 / 200) ≤ (5018 / 10000 : ℝ) ^ 2

theorem win_half : Win (1 / 4) := by unfold Win; norm_num

theorem win_ph : Win (2 / (3 * π)) := by
  have h3 := pi_gt_three
  have h4 := pi_le_four
  have hp : (0 : ℝ) < 3 * π := by positivity
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [le_div_iff₀ hp]; nlinarith
  · rw [div_le_iff₀ hp]; nlinarith
  · rw [div_mul_eq_mul_div, le_div_iff₀ hp]; nlinarith
  · rw [div_mul_eq_mul_div, div_le_iff₀ hp]; nlinarith

theorem not_win_pc1b : ¬ Win (8 * π / 3) := by
  intro h; obtain ⟨-, h2, -, -⟩ := h; have := pi_gt_three; nlinarith

theorem not_win_pc1 : ¬ Win (2 * π / 3) := by
  intro h; obtain ⟨-, h2, -, -⟩ := h; have := pi_gt_three; nlinarith

theorem win_lattice : Win (1 / 2 ^ 2) ∧ Win (1 / 3 ^ 2) ∧ Win (1 / 4 ^ 2) := by
  refine ⟨?_, ?_, ?_⟩ <;> (unfold Win; norm_num)

theorem not_win_lattice_one : ¬ Win (1 / 1 ^ 2) := by unfold Win; norm_num

theorem not_win_lattice_ge5 : ∀ N : ℝ, 5 ≤ N → ¬ Win (1 / N ^ 2) := by
  intro N hN h
  obtain ⟨h1, -, -, -⟩ := h
  have hN2 : (25 : ℝ) ≤ N ^ 2 := by nlinarith
  have h5 : 1 / N ^ 2 ≤ 1 / 25 := one_div_le_one_div_of_le (by norm_num) hN2
  nlinarith

theorem half_not_derivable_with_data :
    ∃ c G ρ a0 Λ H β Z κ : ℝ, Framework (9 / 500) c G ρ a0 Λ H β Z κ ∧ Win (κ ^ 2) ∧ κ ≠ 1 / 2 := by
  obtain ⟨c, G, ρ, a0, Λ, H, β, Z, h⟩ := every_kappa (9 / 500) (1 / 3) (by norm_num) (by norm_num) (by norm_num)
  exact ⟨c, G, ρ, a0, Λ, H, β, Z, 1 / 3, h, by unfold Win; norm_num, by norm_num⟩

theorem window_does_not_select : Win (1 / 4) ∧ Win (2 / (3 * π)) ∧ (1 / 4 : ℝ) ≠ 2 / (3 * π) := by
  refine ⟨win_half, win_ph, ?_⟩
  intro h
  rw [eq_div_iff (by positivity)] at h
  have := pi_gt_three
  nlinarith

#print axioms every_kappa
#print axioms half_not_derivable
#print axioms half_not_derivable_with_data
#print axioms p32_iff
#print axioms ph_val
#print axioms pc1b_val
#print axioms pc1_val
#print axioms pc2_val
#print axioms win_ph
#print axioms not_win_pc1b
#print axioms not_win_lattice_ge5
#print axioms window_does_not_select
