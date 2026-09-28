import Mathlib
import Mathlib.Data.Real.Basic

open Polynomial
noncomputable section

#check Polynomial.card_roots
#check Polynomial.natDegree_le_card_roots
#check Polynomial.eq_zero_of_natDegree_lt_card_roots
#check Polynomial.mem_roots
#check Polynomial.root_lt_natDegree_iff
#check Polynomial.isRoot_iff_X_sub_C_dvd
#check Polynomial.X_sub_C_dvd_iff
#check Polynomial.degree_mul
#check Polynomial.natDegree_mul
#check Polynomial.roots
#check Polynomial.IsRoot

def Pprobe (y : ℝ) : Polynomial ℝ := X^3 + C (4 - y) * X^2 - C (4 * y) * X - C (4 * y)

example (y : ℝ) : eval 0 (Pprobe y) = -4 * y := by
  simp [Pprobe]

example (y : ℝ) : (Pprobe y).natDegree = 3 := by
  unfold Pprobe
  rw [natDegree_X_pow]
  rw [natDegree_add_eq_left_of_natDegree_lt]
  · rw [natDegree_X_pow]
    rw [natDegree_add_eq_left_of_natDegree_lt]
    · rw [natDegree_X_pow, natDegree_mul_X, natDegree_C, max_eq_left, sub_eq_add_neg, add_zero]
      · norm_num
      · exact bot_le
      · norm_num
    · rw [natDegree_mul_X, natDegree_C, max_eq_left, sub_eq_add_neg, add_zero]
      · norm_num
      · exact bot_le
      · norm_num
  · rw [natDegree_X_pow, natDegree_mul_X, natDegree_C, max_eq_left, sub_eq_add_neg, add_zero]
    · norm_num
    · exact bot_le
    · norm_num
