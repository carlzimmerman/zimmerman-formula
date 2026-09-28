import Mathlib

/-!
# AS151 — two-cell trace-mean system: trivial kernel

Certificate for the c2-mean inversion in AS151 step 2/3.  In the two-cell
model of the localized density the trace-sector velocity-momentum system
(with the leaf mean ⟨K⟩ = (K1+K2)/2 and the N-weighted mean A_K =
(N1(K1-⟨K⟩)+N2(K2-⟨K⟩))/2) reads, for zero momentum pi = 0,

    (8 A N1 + 3 B S) K1 = 3 B S K2          (h1)
    3 B S K1 = (8 A N2 + 3 B S) K2          (h2)

with S = N1 + N2, A = M_P²√h/2 > 0, B = c2 M_P²√h/2 ≥ 0 and lapses
N1, N2 > 0 (derivation: multiply the continuum equations
-(2A+3B)K_i + 3B⟨K⟩ + 3B A_K/N_i = pi_i by 4 N_i and use
A_K = (N1-N2)(K1-K2)/4).

Claim: (h1 ∧ h2) ⇒ K1 = 0 ∧ K2 = 0.  Determinant of the cleared system:
    det = 64 A² N1 N2 + 24 A B S² > 0.
This proves the velocity-momentum map of the metric trace sector is
invertible (no hidden primary constraint from the c2 mean terms).
-/

noncomputable section

namespace AS151

/-- The cleared-system determinant of the two-cell trace-mean system. -/
def meanDet (A B N1 N2 : ℝ) : ℝ :=
  64 * A^2 * N1 * N2 + 24 * A * B * (N1 + N2)^2

/-- The homogeneous two-cell trace-mean system has only the zero solution
    for A > 0, B ≥ 0, N1 > 0, N2 > 0. -/
theorem two_cell_mean_kernel (A B N1 N2 K1 K2 : ℝ)
    (hA : 0 < A) (hB : 0 ≤ B) (hN1 : 0 < N1) (hN2 : 0 < N2)
    (h1 : (8*A*N1 + 3*B*(N1+N2)) * K1 = 3*B*(N1+N2) * K2)
    (h2 : 3*B*(N1+N2) * K1 = (8*A*N2 + 3*B*(N1+N2)) * K2) :
    K1 = 0 ∧ K2 = 0 := by
  set S := N1 + N2
  have hNS : 0 < S := by
    nlinarith
  have hSpos : 0 ≤ S := le_of_lt hNS
  have hBS : 0 ≤ 3 * B * S := by positivity
  have hA1 : 0 < 8 * A * N1 := by nlinarith
  have hA2 : 0 < 8 * A * N2 := by nlinarith
  have h1c : 8 * A * N1 ≠ 0 := ne_of_gt hA1
  have h2c : 8 * A * N2 ≠ 0 := ne_of_gt hA2
  have hD1 : 8 * A * N1 + 3 * B * S > 0 := by
    nlinarith
  have hD2 : 8 * A * N2 + 3 * B * S > 0 := by
    nlinarith
  by_cases hB0 : B = 0
  · -- B = 0: the system decouples
    have h1z : (8 * A * N1) * K1 = 0 := by simpa [hB0] using h1
    have h2z : (8 * A * N2) * K2 = 0 := by simpa [hB0] using h2
    constructor
    · exact (mul_eq_zero.mp h1z).resolve_left h1c
    · exact (mul_eq_zero.mp h2z).resolve_left h2c
  · -- B ≠ 0: multiply and subtract (Cramer elimination)
    have hBp : 0 < B := lt_of_le_of_ne' hB hB0
    have hC : 3 * B * S ≠ 0 := by positivity
    have hD : 64 * A^2 * N1 * N2 + 24 * A * B * S^2 > 0 := by
      have h1t : 0 ≤ 64 * A^2 * N1 * N2 := by positivity
      have h2t : 0 < 24 * A * B * S^2 := by positivity
      nlinarith
    have hDne : 64 * A^2 * N1 * N2 + 24 * A * B * S^2 ≠ 0 := ne_of_gt hD
    have hmul1 : (64 * A^2 * N1 * N2 + 24 * A * B * S^2) * K1 = 0 := by
      -- (M11*M22 - M12^2) * K1 = M22*(h1) - M12*(h2)  with M12 = 3BS
      calc
        (64 * A^2 * N1 * N2 + 24 * A * B * S^2) * K1
            = (8*A*N2 + 3*B*S) * ((8*A*N1 + 3*B*S) * K1)
              - (3*B*S) * (3*B*S * K1) := by ring
        _ = (8*A*N2 + 3*B*S) * (3*B*S * K2)
              - (3*B*S) * ((8*A*N2 + 3*B*S) * K2) := by rw [h1, h2]
        _ = 0 := by ring
    have hK1 : K1 = 0 := (mul_eq_zero.mp hmul1).resolve_left hDne
    have hK2 : K2 = 0 := by
      have h1r : (8*A*N1 + 3*B*S) * 0 = 3 * B * S * K2 := by simpa [hK1] using h1
      have h2r : 3 * B * S * K2 = 0 := by
        calc
          3 * B * S * K2 = (8*A*N1 + 3*B*S) * 0 := h1r.symm
          _ = 0 := by ring
      exact (mul_eq_zero.mp h2r).resolve_left hC
    exact ⟨hK1, hK2⟩

/-- Explicit statement that the cleared-system determinant is strictly positive
    on the domain (A>0, B≥0, N1>0, N2>0). -/
theorem mean_det_pos (A B N1 N2 : ℝ)
    (hA : 0 < A) (hB : 0 ≤ B) (hN1 : 0 < N1) (hN2 : 0 < N2) :
    0 < meanDet A B N1 N2 := by
  unfold meanDet
  have h1t : 0 ≤ 64 * A^2 * N1 * N2 := by positivity
  have h2t : 0 ≤ 24 * A * B * (N1 + N2)^2 := by positivity
  have h3t : 0 < 64 * A^2 * N1 * N2 := by positivity
  nlinarith

-- Axiom audits (hard bar: subseteq {propext, Classical.choice, Quot.sound})
#print axioms two_cell_mean_kernel
#print axioms mean_det_pos

end AS151
