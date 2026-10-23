import Mathlib

/-!
# KAPPA_LOGIC_2026_10_20_MUTATE -- must FAIL to compile

Same definitions as KAPPA_LOGIC_2026_10_20.lean. There are two declared mutations, each run through the true file's own tactics:
* M1: `p32_iff` claims κ² = 1/2 in place of 1/4. Its proof must fail.
* M2: `win_pc1b` claims the C1b value 8π/3 is INSIDE the window, using win_ph's tactic block. Its proof must fail.
-/

open Real

structure Framework (b0 c G ρ a0 Λ H β Z κ : ℝ) : Prop where
  pos : 0 < c ∧ 0 < G ∧ 0 < ρ ∧ 0 < a0 ∧ 0 < H ∧ 0 < β ∧ 0 < Z ∧ 0 < κ ∧ 0 < b0
  einstein : Λ = 8 * π * G * ρ / c ^ 2
  friedmann : H ^ 2 = 8 * π * G * ρ / 3
  tie : a0 ^ 2 = κ ^ 2 * G * ρ * c ^ 2
  fourform : κ ^ 2 = 2 * β ^ 2 / (Z + 2 * b0 * β ^ 2)

theorem p32_iff_MUTATE {b0 c G ρ a0 Λ H β Z κ : ℝ} (h : Framework b0 c G ρ a0 Λ H β Z κ) :
    Λ * (π * (c ^ 2 / a0) ^ 2) = 32 * π ^ 2 ↔ κ ^ 2 = 1 / 2 := by
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

def Win (k2 : ℝ) : Prop :=
  (2280 / 10000 : ℝ) ^ 2 ≤ k2 ∧ k2 ≤ (6064 / 10000 : ℝ) ^ 2 ∧
  (1886 / 10000 : ℝ) ^ 2 ≤ k2 * (137 / 200) ∧ k2 * (137 / 200) ≤ (5018 / 10000 : ℝ) ^ 2

theorem win_pc1b_MUTATE : Win (8 * π / 3) := by
  have h3 := pi_gt_three
  have h4 := pi_le_four
  refine ⟨?_, ?_, ?_, ?_⟩ <;> nlinarith
