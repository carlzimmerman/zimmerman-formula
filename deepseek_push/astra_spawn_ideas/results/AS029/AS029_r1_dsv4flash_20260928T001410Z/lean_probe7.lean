import Mathlib
import Mathlib.Data.Real.Basic

open Polynomial
noncomputable section

def Ppoly (y : ℝ) : Polynomial ℝ := X^3 + C (4 - y) * X^2 - C (4 * y) * X - C (4 * y)

#check Polynomial.coeff_mul_X
#check Polynomial.coeff_X_pow_mul

lemma Ppoly_coeff3 (y : ℝ) : (Ppoly y).coeff 3 = 1 := by
  unfold Ppoly
  rw [coeff_sub, coeff_sub, coeff_add]
  rw [coeff_mul_X_pow (p := C (4 - y)) (n := 2) (d := 1)]
  rw [coeff_mul_X (p := C (4 * y)) (n := 2)]
  simp
