import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

namespace LocalScalarSlip

/-
  Pure algebra for the restricted action S_chi = ∫ sqrt(-g) F(Y),
  Y = |grad chi|^2 on a three-dimensional flat leaf.  The variational
  calculation and the Einstein slip equation are documented and checked by
  scalar_slip_gate.py; these lemmas certify the orientation-independent
  algebraic implication used there.
-/

theorem traceless_sum_of_squares
    (x y z Y : ℝ)
    (hY : x ^ 2 + y ^ 2 + z ^ 2 = Y) :
    (x ^ 2 - Y / 3) ^ 2 +
        (y ^ 2 - Y / 3) ^ 2 +
        (z ^ 2 - Y / 3) ^ 2 +
        2 * (x * y) ^ 2 +
        2 * (x * z) ^ 2 +
        2 * (y * z) ^ 2 = 2 * Y ^ 2 / 3 := by
  rw [← hY]
  ring

theorem zero_traceless_stress_forces_zero
    (fy x y z Y : ℝ)
    (hYpos : 0 < Y)
    (hY : x ^ 2 + y ^ 2 + z ^ 2 = Y)
    (hxx : fy * (x ^ 2 - Y / 3) = 0)
    (hyy : fy * (y ^ 2 - Y / 3) = 0)
    (hzz : fy * (z ^ 2 - Y / 3) = 0)
    (hxy : fy * (x * y) = 0)
    (hxz : fy * (x * z) = 0)
    (hyz : fy * (y * z) = 0) :
    fy = 0 := by
  have hsum :
      (fy * (x ^ 2 - Y / 3)) ^ 2 +
          (fy * (y ^ 2 - Y / 3)) ^ 2 +
          (fy * (z ^ 2 - Y / 3)) ^ 2 +
          2 * (fy * (x * y)) ^ 2 +
          2 * (fy * (x * z)) ^ 2 +
          2 * (fy * (y * z)) ^ 2 = 0 := by
    rw [hxx, hyy, hzz, hxy, hxz, hyz]
    norm_num
  have hid := traceless_sum_of_squares x y z Y hY
  have hprod : fy ^ 2 * (2 * Y ^ 2 / 3) = 0 := by
    calc
      fy ^ 2 * (2 * Y ^ 2 / 3) =
          fy ^ 2 * ((x ^ 2 - Y / 3) ^ 2 +
            (y ^ 2 - Y / 3) ^ 2 +
            (z ^ 2 - Y / 3) ^ 2 +
            2 * (x * y) ^ 2 +
            2 * (x * z) ^ 2 +
            2 * (y * z) ^ 2) := by rw [hid]
      _ = (fy * (x ^ 2 - Y / 3)) ^ 2 +
          (fy * (y ^ 2 - Y / 3)) ^ 2 +
          (fy * (z ^ 2 - Y / 3)) ^ 2 +
          2 * (fy * (x * y)) ^ 2 +
          2 * (fy * (x * z)) ^ 2 +
          2 * (fy * (y * z)) ^ 2 := by ring
      _ = 0 := hsum
  have hYsq : 0 < Y ^ 2 := sq_pos_of_pos hYpos
  rcases mul_eq_zero.mp hprod with hfy | hYfactor
  · nlinarith [sq_nonneg fy]
  · nlinarith

theorem mond_matching_incompatible_with_zero_slip
    (fy C mu : ℝ)
    (hC : C ≠ 0)
    (hmu : 0 < mu)
    (hmatch : 2 * fy = C * mu)
    (hzero : fy = 0) :
    False := by
  have hCmu : C * mu ≠ 0 := mul_ne_zero hC (ne_of_gt hmu)
  apply hCmu
  rw [← hmatch, hzero]
  norm_num

#print axioms traceless_sum_of_squares
#print axioms zero_traceless_stress_forces_zero
#print axioms mond_matching_incompatible_with_zero_slip

end LocalScalarSlip
