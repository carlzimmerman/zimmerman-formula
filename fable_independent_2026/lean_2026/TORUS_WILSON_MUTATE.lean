import Mathlib
/-! MUTATE for TORUS_WILSON: FALSE claims, must fail.
(1) the clock is unitary for ANY ω (false for |ω| ≠ 1).
(2) the shift squared is the identity (false: P² ≠ 1, P³ = 1). -/
def C (ω : ℂ) : Matrix (Fin 3) (Fin 3) ℂ := !![1, 0, 0; 0, ω, 0; 0, 0, ω ^ 2]
def P : Matrix (Fin 3) (Fin 3) ℂ := !![0, 1, 0; 0, 0, 1; 1, 0, 0]
theorem mutate_clock_any (ω : ℂ) : (C ω).conjTranspose * C ω = 1 := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [C, Matrix.mul_apply, Fin.sum_univ_three]
theorem mutate_shift_sq : P * P = 1 := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [P, Matrix.mul_apply, Fin.sum_univ_three]
