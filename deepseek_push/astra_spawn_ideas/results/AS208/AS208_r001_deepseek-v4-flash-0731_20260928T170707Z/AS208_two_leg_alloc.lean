import Mathlib

/-! ## AS208 -- Lean certificate: two-leg smoothing-allocation control
The Tier-0 Duhamel bound needs the joint r-allocation estimate: the naive
one-leg r^{-1} bounds diverge log^2 at BOTH endpoints, but the complementary
two-leg estimate is finite near either endpoint.  The algebraic core is the
AM-GM reduction

    1 / sqrt(r (b - r))  <=  (1/r + 1/(b-r)) / 2      (0 < r < b)

which is the exact identity used in the two complementary allocations
(r -> 0 side: S_{b-r} leg; r -> b side: S_r leg).  Certified here in Lean 4:
zero [sorry], axioms subseteq {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

open scoped Real

lemma sq_sum_sq_ge_four_mul : ∀ x y : ℝ, (x + y)^2 ≥ 4 * (x * y) := by
  intro x y
  nlinarith [sq_nonneg (x - y)]

lemma am_gm_sqrt (x y : ℝ) (hx : 0 ≤ x) (hy : 0 ≤ y) :
    Real.sqrt (x * y) ≤ (x + y) / 2 := by
  have hxy : 0 ≤ x * y := by nlinarith
  have h1 : 0 ≤ Real.sqrt (x * y) := Real.sqrt_nonneg _
  have h2 : 0 ≤ (x + y) / 2 := by nlinarith
  rw [← abs_of_nonneg h1, ← abs_of_nonneg h2, ← sq_le_sq, Real.sq_sqrt hxy]
  nlinarith [sq_sum_sq_ge_four_mul x y]

lemma two_leg_alloc (r b : ℝ) (hr : 0 < r) (hrb : r < b) :
    (Real.sqrt (r * (b - r)))⁻¹ ≤ (1 / r + 1 / (b - r)) / 2 := by
  have hbrm : 0 < b - r := by nlinarith
  have hrbp : 0 ≤ r * (b - r) := by nlinarith
  have hpos : 0 < r * (b - r) := by nlinarith
  have hx : 0 ≤ 1 / r := by positivity
  have hy : 0 ≤ 1 / (b - r) := by positivity
  have hpre := am_gm_sqrt (1 / r) (1 / (b - r)) hx hy
  have hmul : (1 / r) * (1 / (b - r)) = 1 / (r * (b - r)) := by field_simp [hr.ne', hbrm.ne']
  have hsqrt : Real.sqrt ((1 / r) * (1 / (b - r))) = (Real.sqrt (r * (b - r)))⁻¹ := by
    rw [hmul]
    rw [Real.sqrt_div (by positivity : 0 ≤ (1 : ℝ)) (r * (b - r))]
    simp
  rw [← hsqrt]
  exact hpre

end