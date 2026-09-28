import Mathlib
import Mathlib.Data.Real.Basic

#check intermediate_value_Icc
#check intermediate_value_uIcc
#check Polynomial.card_roots_le_natDegree
#check Polynomial.continuous
#check zpow_neg
#check zpow_natCast
#check Polynomial.natDegree_X_pow
#check Polynomial.mem_roots
#check Polynomial.roots_ne_zero_of_natDegree_pos

def Pprobe (y : ℝ) : Polynomial ℝ := X^3 + C (4 - y) * X^2 - C (4 * y) * X - C (4 * y)

example (y : ℝ) : (Pprobe y).natDegree = 3 := by
  compute_degree

example (y : ℝ) : True := by
  have hc : Continuous (fun t : ℝ => eval t (Pprobe y)) := by
    fun_prop
  trivial

example {x y : ℝ} (hx : 0 < x) (hy : 0 < y) : True := by
  have h2 : (1 + x / 2 : ℝ) ^ (-2 : ℤ) = ((1 + x / 2 : ℝ) ^ (2 : ℕ))⁻¹ := by
    simpa using (zpow_neg (a := (1 + x / 2 : ℝ)) (n := (2 : ℤ)))
  have h : (1 + x / 2 : ℝ) ^ (-2 : ℤ) = 4 / (x + 2)^2 := by
    rw [h2]
    have hx2 : x + 2 ≠ 0 := by linarith
    field_simp [hx2]
    ring
  trivial
