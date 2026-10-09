import Mathlib
/-! MUTATE for TORUS_YUKAWA: FALSE claims, must fail.
(1) the selection-rule mass matrix has three distinct masses (diag entries a, c, 2c).
(2) Koide with a pair iff y² - 6xy - 2x² = 0. -/
def m (a c : ℂ) : Matrix (Fin 3) (Fin 3) ℂ := !![a, 0, 0; 0, 0, c; 0, c, 0]
theorem mutate_distinct (a c : ℂ) :
    (m a c).conjTranspose * m a c = !![star a * a, 0, 0; 0, star c * c, 0; 0, 0, 2 * star c * c] := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [m, Matrix.mul_apply, Fin.sum_univ_three]
theorem mutate_pair (x y : ℝ) (h : 2 * x + y ≠ 0) :
    (2 * x ^ 2 + y ^ 2) / (2 * x + y) ^ 2 = 2 / 3 ↔ y ^ 2 - 6 * x * y - 2 * x ^ 2 = 0 := by
  rw [div_eq_iff (pow_ne_zero 2 h)]
  constructor <;> intro hq <;> linarith [hq]
