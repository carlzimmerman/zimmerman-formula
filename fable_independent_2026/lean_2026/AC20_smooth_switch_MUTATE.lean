/-
AC20 MUTATE twin: the five declared false variants (M1, M3, M4, M5, M6) must fail; two true sanity
statements (S2, S4) must pass. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace AC20M

/-- M1 (false): swapped symmetrizer H = diag(Π, g). -/
theorem M1_symmetrizer_swapped (v P g : ℝ) :
    !![P, 0; 0, g] * !![v, P; g, v] - Matrix.transpose !![v, P; g, v] * !![P, 0; 0, g] = 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two, Matrix.transpose_apply] <;> ring

/-- S2 (true): the L2 bound. -/
theorem S2_bound (c h : ℝ) (m : ℕ) : |(max (c * h) 0) ^ m| ≤ |c| ^ m * |h| ^ m := by
  have hb : |max (c * h) 0| ≤ |c * h| := by
    rcases le_total (c * h) 0 with h1 | h1
    · rw [max_eq_right h1, abs_zero]; exact abs_nonneg _
    · rw [max_eq_left h1]
  rw [abs_pow, ← mul_pow, ← abs_mul]
  exact pow_le_pow_left₀ (abs_nonneg _) hb m

/-- M3 (false): wrong convexity numerator. -/
theorem M3_numerator (u : ℝ) :
    (4 * u ^ 3 + 6 * u ^ 2) * (u + 1) - 3 * u ^ 3 * (u + 2) = u ^ 2 * (u ^ 2 + 4 * u + 5) := by ring

/-- S4 (true): the L4 identity. -/
theorem S4_identity (Q a : ℝ) :
    Q ^ 3 * (Q + 2 * a) = Q * (Q + a) ^ 3 - a * Q * (Q ^ 2 + 3 * a * Q + a ^ 2) := by ring

/-- M4 (false): deviation bound by Q³. -/
theorem M4_le (Q a : ℝ) (hQ : 0 ≤ Q) (ha : 0 ≤ a) :
    Q * (Q ^ 2 + 3 * a * Q + a ^ 2) ≤ Q ^ 3 := by
  nlinarith [mul_nonneg (mul_nonneg ha ha) hQ, pow_nonneg ha 3]

/-- M5 (false): no kink growth. -/
theorem M5_kink (d t : ℝ) (h1 : 1 + d * t ≠ 0) (h2 : 1 - d * t ≠ 0) :
    d / (1 + d * t) + (-d) / (1 - d * t) = 0 := by
  field_simp
  ring

/-- M6 (false): sign error in the spline polynomial. -/
theorem M6_spline (q : ℝ) (h0 : 0 ≤ q) (h1 : q ≤ 1) :
    0 ≤ -q ^ 2 * (84 * q ^ 3 - 225 * q ^ 2 + 200 * q + 60) := by
  have hp : 84 * q ^ 3 - 225 * q ^ 2 + 200 * q + 60 ≤ 0 := by
    nlinarith [mul_nonneg h0 (sub_nonneg.2 h1), sq_nonneg (q - 9 / 10), sq_nonneg (q - 5 / 6),
      mul_nonneg h0 (sq_nonneg (q - 9 / 10)), mul_nonneg (sub_nonneg.2 h1) (sq_nonneg (q - 9 / 10)),
      mul_nonneg (sub_nonneg.2 h1) (sq_nonneg (q - 5 / 6)), mul_nonneg h0 (sq_nonneg (q - 5 / 6))]
  nlinarith [sq_nonneg q]

end AC20M
