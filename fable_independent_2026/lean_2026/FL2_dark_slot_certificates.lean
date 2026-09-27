import Mathlib

/-!
# FL2 — V0's dark slot with FK1's kick potential: the algebra behind the field-side checks

SCOPE. `real_research/dark_fluid_2026/FL2_dark_slot_with_the_kick.py` puts FK1's potential
m²|Φ|² + ε Re(Φ²) + λ(K)(Im Φ²)² into V0's dark slot. The lane computes the Euler–Lagrange equations, the fast-phase
average and the numbers. Lean certifies the algebra they rest on.

* `cross_energy_square`, `cross_energy_nonneg`: with a + i b = ψ_H ψ_L*, the slow cross term per g_c,
  4|w|² + 2 Re(w²) = 4(a² + b²) + 2(a² − b²), equals 6a² + 2b² ≥ 0. The gated energy is never negative.
* `khronon_linear_response`: for L(x) = −(c₂S/2)K²x² − E(1 − 2qx + q(2q+1)x²), the stationary point is
  x = 2qE/(c₂SK² + 2q(2q+1)E).
* `khronon_stiffness_pos`: the second variation's coefficient c₂S/2 + q(2q+1)E/K² is positive whenever E ≥ 0. The
  K-gate adds stiffness.
* `splitting_energy_changes_sign`: the splitting's K-dependent energy (ε/2m)(n_H − n_L) is negative once n_L > n_H.
  That is why the splitting cannot carry the gate (the lane's MUTATE).
* `gate_block_det`: V0's Hessian ordered (Φ, u, Ψ, w, τ) with the multipliers Φ, Ψ linear has determinant a²b²Z. Every
  entry the gate can reach (X on the constrained fields, Y between them and the khronon) drops out.
-/

open Matrix

theorem cross_energy_square (a b : ℝ) : 4 * (a ^ 2 + b ^ 2) + 2 * (a ^ 2 - b ^ 2) = 6 * a ^ 2 + 2 * b ^ 2 := by
  ring

theorem cross_energy_nonneg (a b : ℝ) : 0 ≤ 4 * (a ^ 2 + b ^ 2) + 2 * (a ^ 2 - b ^ 2) := by
  rw [cross_energy_square]
  positivity

theorem khronon_linear_response (c2 S q E K x : ℝ) (hden : c2 * S * K ^ 2 + 2 * q * (2 * q + 1) * E ≠ 0)
    (hx : x = 2 * q * E / (c2 * S * K ^ 2 + 2 * q * (2 * q + 1) * E)) :
    -c2 * S * K ^ 2 * x + 2 * q * E - 2 * q * (2 * q + 1) * E * x = 0 := by
  have key : -c2 * S * K ^ 2 * x + 2 * q * E - 2 * q * (2 * q + 1) * E * x
      = 2 * q * E - x * (c2 * S * K ^ 2 + 2 * q * (2 * q + 1) * E) := by ring
  rw [key, hx, div_mul_cancel₀ _ hden, sub_self]

theorem khronon_stiffness_pos (c2 S q E K : ℝ) (hc : 0 < c2) (hS : 0 < S) (hq : 0 < q) (hE : 0 ≤ E) :
    0 < c2 * S / 2 + q * (2 * q + 1) * E / K ^ 2 := by
  have h1 : 0 < c2 * S / 2 := by positivity
  have h2 : 0 ≤ q * (2 * q + 1) * E / K ^ 2 := by positivity
  linarith

theorem splitting_energy_changes_sign (eps m nH nL : ℝ) (heps : 0 < eps) (hm : 0 < m) (h : nH < nL) :
    eps / (2 * m) * (nH - nL) < 0 := by
  have h1 : 0 < eps / (2 * m) := by positivity
  have h2 : nH - nL < 0 := by linarith
  exact mul_neg_of_pos_of_neg h1 h2

theorem gate_block_det (a b c X11 X12 X22 Y1 Y2 Z : ℝ) :
    det !![0, a, 0, 0, 0; a, X11, c, X12, Y1; 0, c, 0, b, 0; 0, X12, b, X22, Y2; 0, Y1, 0, Y2, Z]
      = a ^ 2 * b ^ 2 * Z := by
  simp (config := {decide := true}) [det_succ_row_zero, Fin.sum_univ_succ, Fin.succAbove]
  ring

#print axioms cross_energy_square
#print axioms cross_energy_nonneg
#print axioms khronon_linear_response
#print axioms khronon_stiffness_pos
#print axioms splitting_energy_changes_sign
#print axioms gate_block_det
