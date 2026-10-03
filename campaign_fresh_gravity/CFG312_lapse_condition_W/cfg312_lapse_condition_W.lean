import Mathlib

/-!
# CFG312: the algebraic core of the W <= 0 lapse-kernel condition

SCOPE. Lean certifies only the polynomial facts used by `cfg312_lapse_condition_W.py`. It certifies no analysis: not
the lapse-operator invertibility, not Hardy's inequality and not well-posedness.

Notation (X = u², fluid-frame ρ, p, c = c_s²):
  B = 2ρ − 3ρX + pX − 2pX² + (ρ + p) c X²,
  W = −2(Λ + 8πG V) − 8πG M, where M = Σ_i B_i/(1 − X_i)² ≥ 0 is the matter sum.

* `dust_pos`, `dust_neg`: for ρ > 0, the dust bracket ρ(2 − 3X) is > 0 for X < 2/3 and < 0 for X > 2/3 (C3a).
* `fluid_identity`: B = 2ρ(1 − X)² + (ρ + p) X (1 − (2 − c) X) (C3b).
* `fluid_bound`: if ρ ≥ 0, ρ + p ≥ 0, c ≥ 0, X ≥ 0 and (2 − c) X ≤ 1, then B ≥ 2ρ(1 − X)² ≥ 0 (C3b).
* `radiation_pos`: for p = ρ/3 and c = 1/3, X ≥ 0 with X² + 12X − 9 < 0 gives B > 0 when ρ > 0 (C3c).
* `W_nonpos`, `W_neg`: if Λ + 8πG V ≥ 0 and M ≥ 0 then W ≤ 0, and W < 0 if either is strict (C4); here k = 8πG > 0.
-/

theorem dust_pos (ρ X : ℝ) (hρ : 0 < ρ) (hX : X < 2 / 3) : 0 < ρ * (2 - 3 * X) := by
  apply mul_pos hρ; linarith

theorem dust_neg (ρ X : ℝ) (hρ : 0 < ρ) (hX : 2 / 3 < X) : ρ * (2 - 3 * X) < 0 := by
  apply mul_neg_of_pos_of_neg hρ; linarith

theorem fluid_identity (ρ p c X : ℝ) :
    2 * ρ - 3 * ρ * X + p * X - 2 * p * X ^ 2 + (ρ + p) * c * X ^ 2
      = 2 * ρ * (1 - X) ^ 2 + (ρ + p) * X * (1 - (2 - c) * X) := by ring

theorem fluid_bound (ρ p c X : ℝ) (hρ : 0 ≤ ρ) (hnec : 0 ≤ ρ + p) (_hc : 0 ≤ c) (hX : 0 ≤ X)
    (hth : (2 - c) * X ≤ 1) :
    2 * ρ * (1 - X) ^ 2 ≤ 2 * ρ - 3 * ρ * X + p * X - 2 * p * X ^ 2 + (ρ + p) * c * X ^ 2
    ∧ 0 ≤ 2 * ρ * (1 - X) ^ 2 := by
  rw [fluid_identity]
  refine ⟨?_, by positivity⟩
  have h1 : 0 ≤ 1 - (2 - c) * X := by linarith
  have h2 : 0 ≤ (ρ + p) * X * (1 - (2 - c) * X) := mul_nonneg (mul_nonneg hnec hX) h1
  linarith

theorem radiation_pos (ρ X : ℝ) (hρ : 0 < ρ) (_hX : 0 ≤ X) (hq : X ^ 2 + 12 * X - 9 < 0) :
    0 < 2 * ρ - 3 * ρ * X + (ρ / 3) * X - 2 * (ρ / 3) * X ^ 2 + (ρ + ρ / 3) * (1 / 3) * X ^ 2 := by
  have e : 2 * ρ - 3 * ρ * X + (ρ / 3) * X - 2 * (ρ / 3) * X ^ 2 + (ρ + ρ / 3) * (1 / 3) * X ^ 2
      = ρ * (2 / 9) * (9 - 12 * X - X ^ 2) := by ring
  rw [e]
  apply mul_pos (mul_pos hρ (by norm_num)); linarith

theorem W_nonpos (A M k : ℝ) (hA : 0 ≤ A) (hM : 0 ≤ M) (hk : 0 < k) : -2 * A - k * M ≤ 0 := by
  have := mul_nonneg hk.le hM; linarith

theorem W_neg (A M k : ℝ) (hA : 0 ≤ A) (hM : 0 ≤ M) (hk : 0 < k) (hs : 0 < A ∨ 0 < M) :
    -2 * A - k * M < 0 := by
  rcases hs with h | h
  · have := mul_nonneg hk.le hM; linarith
  · have := mul_pos hk h; linarith

#print axioms dust_pos
#print axioms dust_neg
#print axioms fluid_identity
#print axioms fluid_bound
#print axioms radiation_pos
#print axioms W_nonpos
#print axioms W_neg
