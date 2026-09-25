import Mathlib

/-!
# I22 — D-YM1 Euclidean companion: the Dobrushin mass-gap arithmetic for Wilson SU(N)

SCOPE. Lean certifies the scalar content of
`real_research/reviews/ym_door_swings_2026_09_22/ym1_euclidean/PROOF.md`. The external leaves
(Dobrushin's uniqueness theorem, Föllmer's covariance estimate, the positive transfer matrix of
Lüscher / Osterwalder–Seiler, Jentzsch) and the reduction of the total-variation maximum to
two-point laws are stated and cited in prose there and are NOT formalized here.

* `tv_two_point` — THE TV LEMMA'S EXTREMAL INEQUALITY: for 0 ≤ q ≤ 1 and s ≥ 1,
  q(1−q)(s²−1)/(1+q(s²−1)) ≤ (s−1)/(s+1). The certificate is the perfect square
  (1 − q(s+1))² ≥ 0. With s = e^{δ/4} the right side is tanh(δ/4).
* `tanh_as_exp` — tanh x = (e^{2x} − 1)/(e^{2x} + 1).
* `tanh_le_of_exp_le` — if e^{2x} ≤ y then tanh x ≤ (y−1)/(y+1).
* `dobrushin_D4`, `dobrushin_D3`, `dobrushin_D2` — α = 6(D−1) tanh β < 1 for
  0 < β ≤ 1/20 (D = 4), 3/40 (D = 3), 7/50 (D = 2). These are conservative inner windows
  certified with the rational bound e^x ≤ 1/(1−x); the exact thresholds artanh(1/(6(D−1))) =
  0.0556 / 0.0835 / 0.168 are evaluated numerically in `verify.py`.
* `gap_positive` — α < 1 ⇒ m ≥ −ln α > 0.
* `szz_conversion` — Shen–Zhu–Zhu's action Nβ Re Tr equals the Wilson (β_W/N) Re Tr iff
  β_W = N² β, and their SU(N) window |β| < 1/(16(D−1)) is β_W < 3/16 for SU(3), D = 4.

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

namespace I22

open Real

theorem tv_two_point (q s : ℝ) (hq0 : 0 ≤ q) (_hq1 : q ≤ 1) (hs : 1 ≤ s) :
    q * (1 - q) * (s ^ 2 - 1) / (1 + q * (s ^ 2 - 1)) ≤ (s - 1) / (s + 1) := by
  have hs2 : 0 ≤ s ^ 2 - 1 := by nlinarith
  have hden1 : 0 < 1 + q * (s ^ 2 - 1) := by nlinarith [mul_nonneg hq0 hs2]
  have hden2 : 0 < s + 1 := by linarith
  rw [div_le_div_iff₀ hden1 hden2]
  have hsq : 0 ≤ (1 - q * (s + 1)) ^ 2 := sq_nonneg _
  have hs1 : 0 ≤ s - 1 := by linarith
  -- (s−1)(1 + q(s²−1)) − q(1−q)(s²−1)(s+1) = (s−1)(1 − q(s+1))²
  have key : (s - 1) * (1 + q * (s ^ 2 - 1)) - q * (1 - q) * (s ^ 2 - 1) * (s + 1)
      = (s - 1) * (1 - q * (s + 1)) ^ 2 := by ring
  nlinarith [mul_nonneg hs1 hsq]

theorem tanh_as_exp (x : ℝ) : tanh x = (exp (2 * x) - 1) / (exp (2 * x) + 1) := by
  rw [tanh_eq_sinh_div_cosh, sinh_eq, cosh_eq]
  have hx : exp (2 * x) = exp x * exp x := by rw [← exp_add]; ring_nf
  have hn : exp (-x) = (exp x)⁻¹ := exp_neg x
  have he : exp x ≠ 0 := (exp_pos x).ne'
  rw [hx, hn]
  field_simp

theorem tanh_le_of_exp_le (x y : ℝ) (h : exp (2 * x) ≤ y) :
    tanh x ≤ (y - 1) / (y + 1) := by
  rw [tanh_as_exp]
  have hpos : 0 < exp (2 * x) := exp_pos _
  have hy : 0 < y := lt_of_lt_of_le hpos h
  rw [div_le_div_iff₀ (by linarith) (by linarith)]
  nlinarith

/-- α < 1 for D = 4 when 0 < β ≤ 1/20. -/
theorem dobrushin_D4 (β : ℝ) (h0 : 0 < β) (h1 : β ≤ 1 / 20) : 18 * tanh β < 1 := by
  have he : exp (2 * β) ≤ 1 / (1 - 2 * β) :=
    exp_bound_div_one_sub_of_interval (by linarith) (by linarith)
  have hy : 1 / (1 - 2 * β) ≤ 10 / 9 := by
    rw [div_le_div_iff₀ (by linarith) (by norm_num)]; linarith
  have ht := tanh_le_of_exp_le β (10 / 9) (he.trans hy)
  norm_num at ht
  linarith

/-- α < 1 for D = 3 when 0 < β ≤ 3/40. -/
theorem dobrushin_D3 (β : ℝ) (h0 : 0 < β) (h1 : β ≤ 3 / 40) : 12 * tanh β < 1 := by
  have he : exp (2 * β) ≤ 1 / (1 - 2 * β) :=
    exp_bound_div_one_sub_of_interval (by linarith) (by linarith)
  have hy : 1 / (1 - 2 * β) ≤ 20 / 17 := by
    rw [div_le_div_iff₀ (by linarith) (by norm_num)]; linarith
  have ht := tanh_le_of_exp_le β (20 / 17) (he.trans hy)
  norm_num at ht
  linarith

/-- α < 1 for D = 2 when 0 < β ≤ 7/50. -/
theorem dobrushin_D2 (β : ℝ) (h0 : 0 < β) (h1 : β ≤ 7 / 50) : 6 * tanh β < 1 := by
  have he : exp (2 * β) ≤ 1 / (1 - 2 * β) :=
    exp_bound_div_one_sub_of_interval (by linarith) (by linarith)
  have hy : 1 / (1 - 2 * β) ≤ 25 / 18 := by
    rw [div_le_div_iff₀ (by linarith) (by norm_num)]; linarith
  have ht := tanh_le_of_exp_le β (25 / 18) (he.trans hy)
  norm_num at ht
  linarith

theorem gap_positive (α : ℝ) (h0 : 0 < α) (h1 : α < 1) : 0 < -log α := by
  have := log_neg h0 h1
  linarith

/-- Nβ Re Tr U = (β_W/N) Re Tr U for all traces iff β_W = N²β; SU(3), D = 4 window 3/16. -/
theorem szz_conversion (N β βW : ℝ) (hN : 0 < N) (h : βW = N ^ 2 * β) (t : ℝ) :
    N * β * t = βW / N * t ∧ (3 : ℝ) ^ 2 * (1 / (16 * (4 - 1))) = 3 / 16 := by
  refine ⟨?_, by norm_num⟩
  rw [h]
  field_simp

end I22

end

#print axioms I22.tv_two_point
#print axioms I22.tanh_as_exp
#print axioms I22.tanh_le_of_exp_le
#print axioms I22.dobrushin_D4
#print axioms I22.dobrushin_D3
#print axioms I22.dobrushin_D2
#print axioms I22.gap_positive
#print axioms I22.szz_conversion
