import Mathlib
open Real

/-! # AS206 -- Lean certificate

Certifies the algebraic cores of the numeric witnesses for the metric variation of the
intrinsic Laplacian (seed AS206, Tier-0):

* `coef2_id` / `coef_id_half`: the trigonometric coefficient identity underlying the 1D
  conformal-variation Fourier witness. With u = cos(Kx), sigma = cos((K-1)x) and the
  conformal variation k = 2*sigma*delta (flat leaf, 1D), the varied Laplacian
    2 K^2 sigma u + sigma' u'   (XC1-review kernel convention, delta Δ = -2 sigma Δ + <grad sigma, grad>)
  expands into the two Fourier modes
    ((3K^2 - K)/2) * cos x + ((K^2 + K)/2) * cos((2 K - 1) x).
  For K = 20 the coefficients are the witness values an1 = 590 and an39 = 210,
  i.e. the XC1 Fourier kernel (3|q|^2 - p q) sigma_{p-q} evaluated at q = K.

* `adjugate_2x2`: the 2x2 cofactor/adjugate algebra behind h^{-1} for the curved leaf
  metric h = [[a, b], [b, c]] used by the 2D control of the divergence form.

Theorems are stated over the reals; the coefficient forms avoid division-by-numeral issues
by proving the times-two version with pure `ring`, then cancelling the factor 2.
-/

-- (1) times-two coefficient identity, pure ring after cos_sub / cos_add
theorem coef2_id (K x : ℝ) :
    2 * (2 * K ^ 2 * (cos ((K - 1) * x) * cos (K * x))
        + K * (K - 1) * (sin ((K - 1) * x) * sin (K * x)))
    = (3 * K ^ 2 - K) * cos (K * x - (K - 1) * x)
      + (K ^ 2 + K) * cos ((K - 1) * x + K * x) := by
  rw [cos_sub, cos_add]
  ring

-- (2) the half-version stated in the witness form (division by numeral 2)
theorem coef_id_half (K x : ℝ) :
    2 * K ^ 2 * (cos ((K - 1) * x) * cos (K * x))
      + K * (K - 1) * (sin ((K - 1) * x) * sin (K * x))
    = ((3 * K ^ 2 - K) / 2) * cos (K * x - (K - 1) * x)
      + ((K ^ 2 + K) / 2) * cos ((K - 1) * x + K * x) := by
  rw [cos_sub, cos_add]
  ring_nf

-- (3) the K = 20 witness: coefficients 590 (mode 1) and 210 (mode 39 = 2K-1)
theorem witness_K20 (x : ℝ) :
    2 * (20 : ℝ) ^ 2 * (cos (19 * x) * cos (20 * x))
      + 20 * (19 : ℝ) * (sin (19 * x) * sin (20 * x))
    = 590 * cos x + 210 * cos (39 * x) := by
  have h := coef_id_half (20 : ℝ) x
  have a0 : ((20 : ℝ) - 1) * x = 19 * x := by ring
  have a1 : (20 : ℝ) * x - 19 * x = x := by ring
  have a2 : (19 : ℝ) * x + 20 * x = 39 * x := by ring
  rw [a0, a1, a2] at h
  norm_num at h
  norm_num
  exact h

-- (4) curved-leaf 2x2 machinery: adjugate/coractor inverse of h = [[a, b], [b, c]]
def M2 (a b c : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![a, b; b, c]

def Adj2 (a b c : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![c, -b; -b, a]

theorem det_M2 (a b c : ℝ) : (M2 a b c).det = a * c - b ^ 2 := by
  rw [Matrix.det_fin_two]
  simp [M2]
  ring

theorem adj_equiv (a b c : ℝ) : (M2 a b c).adjugate = Adj2 a b c := by
  rw [Matrix.adjugate_fin_two]
  simp [M2, Adj2]

theorem adjugate_2x2 (a b c : ℝ) :
    M2 a b c * Adj2 a b c = (a * c - b ^ 2) • 1 ∧
    Adj2 a b c * M2 a b c = (a * c - b ^ 2) • 1 := by
  constructor
  · have h := Matrix.mul_adjugate (M2 a b c)
    rw [adj_equiv a b c] at h
    rw [det_M2] at h
    simpa using h
  · have h := Matrix.adjugate_mul (M2 a b c)
    rw [adj_equiv a b c] at h
    rw [det_M2] at h
    simpa using h

-- the invertible form used by the curved-leaf machinery: h^{-1} = (1/det) * adjugate
theorem inv_entry_00 (a b c : ℝ) (hd : a * c - b ^ 2 ≠ 0) :
    (M2 a b c * ((a * c - b ^ 2)⁻¹ • Adj2 a b c)) 0 0 = 1 := by
  rw [Matrix.mul_apply, Fin.sum_univ_two]
  simp [M2, Adj2, Pi.smul_apply]
  field_simp [hd]
  ring

#print axioms coef2_id
#print axioms coef_id_half
#print axioms witness_K20
#print axioms det_M2
#print axioms adj_equiv
#print axioms adjugate_2x2
#print axioms inv_entry_00