/-
EUC17R_MUTATE: the mutation twin of EUC17R.lean. Each theorem carries ONE false change (a sign, a factor or an
inequality direction) and the same proof script; every theorem here must fail to compile. They certify the algebra,
not the physics, and no number or label of the lane.

  boost_follows_product_mut   : B' = B / f in place of B' = B f.
  log_shift_mut               : minus log10 f in place of plus.
  correction_lowers_mut       : inequality direction reversed.
  margin_share_cannot_rise_mut : the inverted correction b - log10 f in the hypothesis.
  invert_twin_raises_mut      : inequality direction reversed.
  nomask_twin_identity_mut    : b + 1 in place of b.
  exp_share_bounds_mut        : the share below 0 in place of below 1.
  word_exclusive_mut          : the BROKEN line at 0.05 in place of 0.25.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

namespace EUC17R

theorem boost_follows_product_mut (B B' M f : ℝ) (hf : f ≠ 0) (hM : M ≠ 0) (h : B' * (M / f) = B * M) :
    B' = B / f := by
  have h1 : B' * (M / f) * f = B * M * f := by rw [h]
  rw [mul_assoc, div_mul_cancel₀ M hf] at h1
  have key : B' * M = (B * f) * M := by linarith
  exact mul_right_cancel₀ hM key

theorem log_shift_mut (B f : ℝ) (hB : 0 < B) (hf : 0 < f) :
    Real.logb 10 (B * f) = Real.logb 10 B - Real.logb 10 f := by
  exact Real.logb_mul (ne_of_gt hB) (ne_of_gt hf)

theorem correction_lowers_mut (b f : ℝ) (hf0 : 0 < f) (hf1 : f ≤ 1) : b ≤ b + Real.logb 10 f := by
  have h : Real.logb 10 f ≤ 0 := Real.logb_nonpos (by norm_num) (le_of_lt hf0) hf1
  linarith

theorem margin_share_cannot_rise_mut (b f : ℝ) (hf0 : 0 < f) (hf1 : f ≤ 1)
    (h : (1 : ℝ) / 4 < b - Real.logb 10 f) : (1 : ℝ) / 4 < b := by
  have h0 : Real.logb 10 f ≤ 0 := Real.logb_nonpos (by norm_num) (le_of_lt hf0) hf1
  linarith

theorem invert_twin_raises_mut (b f : ℝ) (hf0 : 0 < f) (hf1 : f ≤ 1) : b - Real.logb 10 f ≤ b := by
  have h : Real.logb 10 f ≤ 0 := Real.logb_nonpos (by norm_num) (le_of_lt hf0) hf1
  linarith

theorem nomask_twin_identity_mut (b : ℝ) : b + Real.logb 10 1 = b + 1 := by
  simp

theorem exp_share_bounds_mut (x : ℝ) (hx : 0 ≤ x) :
    0 ≤ 1 - (1 + x) * Real.exp (-x) ∧ 1 - (1 + x) * Real.exp (-x) < 0 := by
  have he : Real.exp x * Real.exp (-x) = 1 := by
    rw [← Real.exp_add]; simp
  have hpos : 0 < Real.exp (-x) := Real.exp_pos _
  have hle : x + 1 ≤ Real.exp x := Real.add_one_le_exp x
  constructor
  · nlinarith [mul_le_mul_of_nonneg_right hle (le_of_lt hpos)]
  · nlinarith

theorem word_exclusive_mut (lo hi : ℝ) (hlh : lo ≤ hi) :
    ¬ ((1 : ℝ) / 20 ≤ lo ∧ hi ≤ (1 : ℝ) / 10) ∧ ¬ ((1 : ℝ) / 4 ≤ lo ∧ hi ≤ (3 : ℝ) / 20) := by
  constructor
  · rintro ⟨h1, h2⟩
    linarith
  · rintro ⟨h1, h2⟩
    linarith

end EUC17R

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
