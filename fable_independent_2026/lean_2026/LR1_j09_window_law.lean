import Mathlib

/-!
# LR1 — J09 central window law, Lean certificate (M-roads Lean roadmap)

SCOPE (I-series precedent, e.g. I20): Lean certifies the ALGEBRA. The physics input —
that the framework's central-source window reads `W(q) = (1 + q/3) / (1/2 + q/4)` —
is a hypothesis; its Monte-Carlo verification (J09, 27/27, `J09_two_component_law.py`
exit 0) is the empirical leg and is NOT re-proven here.

Content:
* `denom_pos` — the window denominator `1/2 + q/4` is positive for `q ≥ 0`.
* `W_le_two` — `W(q) ≤ 2` for all `q ≥ 0` (the q = 0 endpoint: `(1)/(1/2) = 2`).
* `W_ge_four_thirds` — `4/3 ≤ W(q)` for all `q ≥ 0` (the q → ∞ limit: `(q/3)/(q/4) = 4/3`).
* `W_strict_antitone` — W is strictly decreasing on `[0, ∞)`: for `0 ≤ a < b`,
  `W(b) < W(a)`; the cross-difference is exactly `(b - a)/12`.
* `W_mem_window` — the registered band: for all `q ≥ 0`, `4/3 ≤ W(q) ≤ 2` (the J09
  central window law; measured ratio outside `[4/3, 2]` at ≥ 3σ is the falsifier).

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

open Real

noncomputable def W (q : ℝ) : ℝ := (1 + q / 3) / (1 / 2 + q / 4)

theorem denom_pos (q : ℝ) (hq : 0 ≤ q) : 0 < 1 / 2 + q / 4 := by linarith

theorem W_le_two (hq : 0 ≤ q) : W q ≤ 2 := by
  have hden : 0 < 1 / 2 + q / 4 := denom_pos q hq
  rw [W]
  field_simp
  linarith [hq]

theorem W_ge_four_thirds (hq : 0 ≤ q) : 4 / 3 ≤ W q := by
  have hden : 0 < 1 / 2 + q / 4 := denom_pos q hq
  have h1 : (2:ℝ) / 3 ≤ 1 := by norm_num
  rw [W]
  field_simp
  linarith [h1]

theorem W_strict_antitone {a b : ℝ} (hab : 0 ≤ a) (hab' : a < b) : W b < W a := by
  have hb : 0 < 1 / 2 + b / 4 := denom_pos b (by linarith)
  have ha : 0 < 1 / 2 + a / 4 := denom_pos a hab
  have hp1 : 0 < 1 + a / 3 := by linarith
  have h12 : (0:ℝ) < 12 := by norm_num
  have hba : 0 < b - a := by linarith
  rw [W, W, div_lt_div_iff₀ hb ha]
  have hd : (1 + a / 3) * (1 / 2 + b / 4)
      = (1 + b / 3) * (1 / 2 + a / 4) + (b - a) / 12 := by ring
  nlinarith [hd, hba, h12, hp1, hb]

theorem W_mem_window (hq : 0 ≤ q) : 4 / 3 ≤ W q ∧ W q ≤ 2 :=
  ⟨W_ge_four_thirds hq, W_le_two hq⟩

#print axioms denom_pos
#print axioms W_le_two
#print axioms W_ge_four_thirds
#print axioms W_strict_antitone
#print axioms W_mem_window
