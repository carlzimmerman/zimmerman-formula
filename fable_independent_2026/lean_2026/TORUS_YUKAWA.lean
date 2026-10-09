import Mathlib

/-!
# TORUS_YUKAWA -- magnetized-torus Yukawas (criteria TORUS_YUKAWA_CRITERIA.md, commit c650a9ddb): KILL

Numeric (TORUS_YUKAWA.py / .out): M_L = M_R = 3, M_H = 6, overlap integrals of theta-function zero modes
(orthonormality and periodicity gates pass at 1e-14).  All 14 pre-declared natural points (τ ∈ {i, e^{2πi/3}},
Higgs in one mode or uniform, no Wilson lines) give TWO EXACTLY EQUAL masses, Q = 0.406-0.430.  The only
crossing of 2/3 on τ = i t (Higgs mode 0, t ≈ 2.05) still has the degenerate pair.

CERTIFIED (the mechanism):
(A) `selection_degenerate`: the selection rule i + j ≡ k (mod 3) plus the reflection symmetry m_12 = m_21 gives a
    mass matrix with entries only at (0,0), (1,2), (2,1) equal off-diagonal; then m†m = diag(|a|², |c|², |c|²):
    two equal masses, whatever τ is.
(B) `koide_with_pair`: a spectrum (x, x, y) satisfies Koide iff y² - 8xy - 2x² = 0, i.e. y = (4 ± 3√2) x —
    an irrational ratio (cf. KOIDE_TRIALITY_45 `koide_cone_no_integer`), and in any case two equal lepton
    masses are excluded by data.
Breaking the degeneracy needs Wilson lines (continuous moduli): that is a fit, not a derivation.
-/

namespace TorusYukawa

def m (a c : ℂ) : Matrix (Fin 3) (Fin 3) ℂ := !![a, 0, 0; 0, 0, c; 0, c, 0]

theorem selection_degenerate (a c : ℂ) :
    (m a c).conjTranspose * m a c = !![star a * a, 0, 0; 0, star c * c, 0; 0, 0, star c * c] := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [m, Matrix.mul_apply, Fin.sum_univ_three]

theorem koide_with_pair (x y : ℝ) (h : 2 * x + y ≠ 0) :
    (2 * x ^ 2 + y ^ 2) / (2 * x + y) ^ 2 = 2 / 3 ↔ y ^ 2 - 8 * x * y - 2 * x ^ 2 = 0 := by
  rw [div_eq_iff (pow_ne_zero 2 h)]
  constructor <;> intro hq <;> linarith [hq]

end TorusYukawa

#print axioms TorusYukawa.selection_degenerate
#print axioms TorusYukawa.koide_with_pair
