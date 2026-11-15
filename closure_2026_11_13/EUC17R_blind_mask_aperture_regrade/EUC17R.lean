/-
EUC17R: Lean statements for the algebra of the aperture-mass correction as the blind re-grade of EUC17 applies it
(euc17r.py, criteria section 2 of EUC17). They certify the algebra, not the physics, and no number or label of the
lane. TEST lane; adopts nothing.

  boost_follows_product  : the boost solves for the product B M (the law sees only B M), so a body of mass M / f
                           needs the boost B f to reach the same product (f, M nonzero).
  log_shift              : in log10 the corrected boost is b + log10 f: logb 10 (B f) = logb 10 B + logb 10 f.
  correction_lowers      : with the in-mask share 0 < f <= 1 the corrected boost b + log10 f never exceeds b.
  margin_share_cannot_rise : a lens above the 0.25 dex margin after the correction was above it before, so the
                           share above the margin cannot rise under the correction.
  invert_twin_raises     : the invert twin's b - log10 f is never below b (0 < f <= 1).
  nomask_twin_identity   : the no-mask twin (f = 1) returns b unchanged.
  exp_share_bounds       : the n = 1 (exponential) share inside x = b1 R / R_e, 1 - (1 + x) e^(-x), lies in [0, 1).
  word_exclusive         : CEILING BROKEN (lower bound >= 0.25) and CEILING HOLDS (upper bound <= 0.10) cannot
                           both apply when lower <= upper; the same for LENS GATE HOLDS (upper <= 0.15) and
                           LENS GATE FAILS (lower >= 0.25).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

namespace EUC17R

theorem boost_follows_product (B B' M f : ℝ) (hf : f ≠ 0) (hM : M ≠ 0) (h : B' * (M / f) = B * M) :
    B' = B * f := by
  have h1 : B' * (M / f) * f = B * M * f := by rw [h]
  rw [mul_assoc, div_mul_cancel₀ M hf] at h1
  have key : B' * M = (B * f) * M := by linarith
  exact mul_right_cancel₀ hM key

theorem log_shift (B f : ℝ) (hB : 0 < B) (hf : 0 < f) :
    Real.logb 10 (B * f) = Real.logb 10 B + Real.logb 10 f := by
  exact Real.logb_mul (ne_of_gt hB) (ne_of_gt hf)

theorem correction_lowers (b f : ℝ) (hf0 : 0 < f) (hf1 : f ≤ 1) : b + Real.logb 10 f ≤ b := by
  have h : Real.logb 10 f ≤ 0 := Real.logb_nonpos (by norm_num) (le_of_lt hf0) hf1
  linarith

theorem margin_share_cannot_rise (b f : ℝ) (hf0 : 0 < f) (hf1 : f ≤ 1)
    (h : (1 : ℝ) / 4 < b + Real.logb 10 f) : (1 : ℝ) / 4 < b := by
  have h0 : Real.logb 10 f ≤ 0 := Real.logb_nonpos (by norm_num) (le_of_lt hf0) hf1
  linarith

theorem invert_twin_raises (b f : ℝ) (hf0 : 0 < f) (hf1 : f ≤ 1) : b ≤ b - Real.logb 10 f := by
  have h : Real.logb 10 f ≤ 0 := Real.logb_nonpos (by norm_num) (le_of_lt hf0) hf1
  linarith

theorem nomask_twin_identity (b : ℝ) : b + Real.logb 10 1 = b := by
  simp

theorem exp_share_bounds (x : ℝ) (hx : 0 ≤ x) :
    0 ≤ 1 - (1 + x) * Real.exp (-x) ∧ 1 - (1 + x) * Real.exp (-x) < 1 := by
  have he : Real.exp x * Real.exp (-x) = 1 := by
    rw [← Real.exp_add]; simp
  have hpos : 0 < Real.exp (-x) := Real.exp_pos _
  have hle : x + 1 ≤ Real.exp x := Real.add_one_le_exp x
  constructor
  · nlinarith [mul_le_mul_of_nonneg_right hle (le_of_lt hpos)]
  · nlinarith

theorem word_exclusive (lo hi : ℝ) (hlh : lo ≤ hi) :
    ¬ ((1 : ℝ) / 4 ≤ lo ∧ hi ≤ (1 : ℝ) / 10) ∧ ¬ ((1 : ℝ) / 4 ≤ lo ∧ hi ≤ (3 : ℝ) / 20) := by
  constructor
  · rintro ⟨h1, h2⟩
    linarith
  · rintro ⟨h1, h2⟩
    linarith

end EUC17R

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
