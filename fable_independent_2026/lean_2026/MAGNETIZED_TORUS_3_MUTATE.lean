import Mathlib

/-! MUTATE for MAGNETIZED_TORUS_3: both claims are FALSE and must fail.
(1) Z² = 32π/3 is 5 flux quanta.
(2) commuting with the shift alone forces a multiple of the identity (false: P itself commutes with P). -/

theorem mutate_Z2_five : (32 * Real.pi / 3 : ℝ) = 2 * Real.pi * 5 := by
  field_simp; ring

def P : Matrix (Fin 3) (Fin 3) ℂ := !![0, 1, 0; 0, 0, 1; 1, 0, 0]

theorem mutate_shift_scalar (X : Matrix (Fin 3) (Fin 3) ℂ) (hP : X * P = P * X) :
    X = X 0 0 • (1 : Matrix (Fin 3) (Fin 3) ℂ) := by
  have f := fun i j => congrFun (congrFun hP i) j
  simp [P, Matrix.mul_apply, Fin.sum_univ_three] at f
  ext i j; fin_cases i <;> fin_cases j <;> simp_all
