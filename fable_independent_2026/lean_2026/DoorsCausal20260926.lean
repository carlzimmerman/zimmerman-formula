import Mathlib

/-!
# Constant-coefficient causal-completion algebra, 2026-09-26

Target L = (z_t² + chi_t² - z_x² - chi_x² - m² chi²)/2 + g chi z_t.
The lemmas certify the Legendre square, energy positivity, scalar dispersion
root sign, low-momentum coefficient algebra, an elliptic resolvent identity,
and the one-dimensional energy-flux inequality. `m2` and `g2` stand for squared
parameters; when relating to the Lagrangian, g2 = g² must be imposed.

No PDE existence/uniqueness theorem, propagation-of-support theorem, global
constraint count, gravitational embedding or nonlinear extension is formalized
here. The low-root residual cancels the q and q² coefficients exactly; an
analytic Taylor/asymptotic interpretation additionally needs the root branch.
-/

namespace DoorsCausal20260926

theorem legendre_hamiltonian_square (pz pc zx cx chi g m2 : ℝ) :
    pz * (pz - g * chi) + pc ^ 2 -
      (((pz - g * chi) ^ 2 + pc ^ 2 - zx ^ 2 - cx ^ 2 - m2 * chi ^ 2) / 2 +
        g * chi * (pz - g * chi)) =
      ((pz - g * chi) ^ 2 + pc ^ 2 + zx ^ 2 + cx ^ 2 + m2 * chi ^ 2) / 2 := by
  ring

theorem hamiltonian_nonnegative (pz pc zx cx chi g m2 : ℝ) (hm : 0 ≤ m2) :
    0 ≤ ((pz - g * chi) ^ 2 + pc ^ 2 + zx ^ 2 + cx ^ 2 + m2 * chi ^ 2) / 2 := by
  positivity

theorem positive_dispersion_root (q m2 g2 r : ℝ)
    (hq : 0 < q) (hm : 0 < m2) (hg : 0 ≤ g2)
    (hroot : (r - q) * (r - q - m2) - g2 * r = 0) : 0 < r := by
  by_contra h
  have hr : r ≤ 0 := le_of_not_gt h
  have hp : 0 < (r - q) * (r - q - m2) := mul_pos_of_neg_of_neg (by linarith) (by linarith)
  have hn : g2 * r ≤ 0 := mul_nonpos_of_nonneg_of_nonpos hg hr
  linarith

theorem low_root_polynomial_residual (q m2 g2 : ℝ) (hA : m2 + g2 ≠ 0) :
    let A := m2 + g2
    let r := (m2 / A) * q + (g2 ^ 2 / A ^ 3) * q ^ 2
    (r - q) * (r - q - m2) - g2 * r =
      -2 * g2 ^ 3 / A ^ 4 * q ^ 3 + g2 ^ 4 / A ^ 6 * q ^ 4 := by
  dsimp
  field_simp
  ring

theorem prescribed_low_momentum_coefficients (s d : ℝ)
    (hs0 : 0 < s) (hs1 : s < 1) (hd : 0 < d) :
    let A := (1 - s) ^ 2 / d
    0 < A ∧ 0 < s * A ∧ 0 < (1 - s) * A ∧
      (s * A) / (s * A + (1 - s) * A) = s ∧
      ((1 - s) * A) ^ 2 / (s * A + (1 - s) * A) ^ 3 = d := by
  let A := (1 - s) ^ 2 / d
  have hs : 0 < 1 - s := by linarith
  have hsn : 1 - s ≠ 0 := ne_of_gt hs
  have ha : 0 < A := by dsimp [A]; positivity
  change 0 < A ∧ 0 < s * A ∧ 0 < (1 - s) * A ∧
    (s * A) / (s * A + (1 - s) * A) = s ∧
    ((1 - s) * A) ^ 2 / (s * A + (1 - s) * A) ^ 3 = d
  refine ⟨ha, mul_pos hs0 ha, mul_pos hs ha, ?_, ?_⟩
  · have hsum : s * A + (1 - s) * A = A := by ring
    rw [hsum]
    field_simp
  · have hsum : s * A + (1 - s) * A = A := by ring
    rw [hsum]
    dsimp [A]
    field_simp

theorem elliptic_inertia_positive (m2 q g : ℝ) (hm : 0 < m2) (hq : 0 ≤ q) :
    0 < 1 + g ^ 2 / (m2 + q) := by
  have hden : 0 < m2 + q := by linarith
  have hfrac : 0 ≤ g ^ 2 / (m2 + q) := div_nonneg (sq_nonneg g) hden.le
  linarith

theorem elliptic_acceleration_resolvent (ell m2 g2 : ℝ)
    (hell : 0 ≤ ell) (hm : 0 < m2) (hg : 0 ≤ g2) :
    -ell + g2 * ell / (m2 + g2 + ell) =
      -ell + g2 - g2 * (m2 + g2) / (m2 + g2 + ell) := by
  have hden : m2 + g2 + ell ≠ 0 := by positivity
  field_simp
  ring

theorem energy_flux_bound (a b c d e : ℝ) :
    |a * b + c * d| ≤ (a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 + e ^ 2) / 2 := by
  rw [abs_le]
  constructor <;>
    nlinarith [sq_nonneg (a - b), sq_nonneg (a + b),
      sq_nonneg (c - d), sq_nonneg (c + d), sq_nonneg e]

#print axioms legendre_hamiltonian_square
#print axioms hamiltonian_nonnegative
#print axioms positive_dispersion_root
#print axioms low_root_polynomial_residual
#print axioms prescribed_low_momentum_coefficients
#print axioms elliptic_inertia_positive
#print axioms elliptic_acceleration_resolvent
#print axioms energy_flux_bound

end DoorsCausal20260926
