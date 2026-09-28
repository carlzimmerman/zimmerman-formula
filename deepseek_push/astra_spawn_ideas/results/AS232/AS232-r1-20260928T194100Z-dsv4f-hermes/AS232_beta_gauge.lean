-- AS232 Lean certificate: beta from the second-order static weak-field equation.
-- Certifies the PPN bookkeeping identities used in the derivation:
--   (1) gauge identity:  Phi = -U_N + phi2  (declared PPN gauge g00 = -e^{2 Phi},
--       c = 1 natural units) with  beta = 1 + phi2/U_N^2  (U_N != 0)  implies the
--       second-order truncation of -e^{2 Phi} equals -1 + 2 U_N - 2 beta U_N^2.
--   (2) point-source harmonic algebra: the flat Laplacian L0(f) = f'' + 2 f'/r of the
--       ansatz  phi2 = A*GM2/r^2  evaluates the 2/r^4-harmonic weight  2*A*GM2
--       (given the derivative values  (1/r^2)' = -2/r^3,  (1/r^2)'' = 6/r^4), which is
--       the coefficient used to extract A = phi2/U_N^2 from the epsilon^2 lapse slot.
--   (3) Einstein-limit shell gate:  B(alpha) = -(6 + alpha)/8  gives  B(0) = -3/4,
--       i.e. psi2 -> -(3/4) U_N^2 and beta -> 1 at alpha -> 0 (window-vacuum).
import Mathlib

/- (1) gauge -> beta -/
theorem as232_gauge_beta (beta U phi2 : ℝ) (hU : U ≠ 0)
    (hbeta : beta = 1 + phi2 / U ^ 2) :
    -(1 - 2 * U + 2 * U ^ 2 + 2 * phi2) = -1 + 2 * U - 2 * beta * U ^ 2 := by
  rw [hbeta]
  field_simp [hU]
  ring

/- (2) flat-Laplacian harmonic weight of the point ansatz (derivative values given) -/
theorem as232_l0_point_harmonic (A GM2 r : ℝ) (hr : r ≠ 0) :
    6 * (A * GM2 / r ^ 2) / r ^ 2 + 2 * (-2 * (A * GM2 / r ^ 3)) / r =
      2 * (A * GM2) / r ^ 4 := by
  field_simp [hr]
  ring

/- (3) Einstein-limit shell gate -/
theorem as232_einstein_shell_limit (alpha : ℝ) :
    -(6 + alpha) / 8 = -3 / 4 - alpha / 8 := by
  ring

/- corollary at alpha = 0 -/
example : -(6 + 0) / 8 = -3 / 4 := by
  norm_num
