import Mathlib

/-!
# KOIDE_HOLONOMY -- the holonomy door: the Koide phase as a flux through the three-generation ring

KOIDE_PHASE showed the hierarchy phase enters only through the Z3 invariant 3δ, which a lattice direction cannot
set, and that a rational-radian value has to come from a holonomy or a logarithm, not a potential minimum.
Here: the three generations as a 3-site ring, H = a·1 + c·P + c'·Pᵀ (P the cyclic shift; Hermitian when
c' = conj c = t e^{-iφ}).  Source: scratch hol.py.

CERTIFIED:
(A) `ring_eigen`: for any z with z^3 = 1, the Fourier vector (1, z, z^2) is an eigenvector of H with eigenvalue
    a + c z + c' z^2.  With c = t e^{iφ}, c' = t e^{-iφ}, z = e^{2πik/3} this is a + 2t cos(φ + 2πk/3)
    (`eigen_cos`): exactly the Koide/Brannen form √m_k = A(1 + r cos(δ + 2πk/3)) with δ = φ and r = 2t/a.
    So Koide's r = √2 is hopping/on-site = 1/√2, and the phase is the hopping phase.
(B) `holonomy_gauge_invariant`: under any rephasing of the three generations (d_j ≠ 0), the product of the
    three link amplitudes around the ring, H01·H12·H20 = c^3, is unchanged.  The link phase φ is gauge, the
    Wilson loop e^{3iφ} is physical: Koide's Z3 invariant 3δ IS the flux Φ through the generation triangle.
(C) `degenerate_iff`: λ(z) - λ(z²) = (c - c')(z - z²), so the k = 1, 2 levels are degenerate exactly when
    c = c' (for Hermitian H: a real hopping, flux 0 or π).  Three distinct masses in this ring REQUIRE a flux
    that is not 0 or π, i.e. a T-odd (complex) hopping in the generation basis.
(D) Two of the eight pre-declared geometric fluxes (holonomy = monopole charge × solid angle), checked exactly:
    `octant_misses`: the geodesic triangle through the three basis axes (an octant, Ω = π/2) with g = 1/2
    gives π/4, more than 0.1 above the target 3δ = 0.666666141 (Koide-exact value, KOIDE_PHASE);
    `koide_cap_misses`: the 45° cap with g = 1/2 gives π(1 - √2/2), more than 0.25 above it.
NOT CERTIFIED: the other six candidates (scratch, all miss by ≥ 0.12); the target value itself (scratch,
from m_μ/m_e with r = √2); that the circulant basis is physical (for charged leptons alone the flux is
basis-dependent unless the S3 basis is fixed by other physics).  The door turns Koide into a concrete model,
it does NOT derive the flux: the flux is still an input, now with a gauge-invariant meaning.
-/

namespace KoideHolonomy

/-- the ring Hamiltonian: on-site a, forward hop c, backward hop c'. -/
def H (a c c' : ℂ) : Matrix (Fin 3) (Fin 3) ℂ := !![a, c, c'; c', a, c; c, c', a]

theorem ring_eigen (a c c' z : ℂ) (hz : z ^ 3 = 1) :
    (H a c c').mulVec ![1, z, z ^ 2] = (a + c * z + c' * z ^ 2) • ![1, z, z ^ 2] := by
  ext i
  fin_cases i <;> simp [H, Matrix.mulVec, dotProduct, Fin.sum_univ_three]
  · linear_combination (-c') * hz
  · linear_combination (-c - c' * z) * hz

theorem eigen_cos (a t φ θ : ℝ) :
    (a : ℂ) + (t * Complex.exp (φ * Complex.I)) * Complex.exp (θ * Complex.I)
      + (t * Complex.exp (-(φ * Complex.I))) * Complex.exp (-(θ * Complex.I))
      = ((a + 2 * t * Real.cos (φ + θ) : ℝ) : ℂ) := by
  have e1 : Complex.exp (φ * Complex.I) * Complex.exp (θ * Complex.I)
      = Complex.exp (((φ + θ : ℝ) : ℂ) * Complex.I) := by
    rw [← Complex.exp_add]; push_cast; ring_nf
  have e2 : Complex.exp (-(φ * Complex.I)) * Complex.exp (-(θ * Complex.I))
      = Complex.exp (-(((φ + θ : ℝ) : ℂ) * Complex.I)) := by
    rw [← Complex.exp_add]; push_cast; ring_nf
  have hc : Complex.exp (((φ + θ : ℝ) : ℂ) * Complex.I) + Complex.exp (-(((φ + θ : ℝ) : ℂ) * Complex.I))
      = 2 * (Real.cos (φ + θ) : ℂ) := by
    rw [Complex.ofReal_cos, Complex.cos]; ring_nf
  calc (a : ℂ) + (t * Complex.exp (φ * Complex.I)) * Complex.exp (θ * Complex.I)
        + (t * Complex.exp (-(φ * Complex.I))) * Complex.exp (-(θ * Complex.I))
      = a + t * (Complex.exp (φ * Complex.I) * Complex.exp (θ * Complex.I)
          + Complex.exp (-(φ * Complex.I)) * Complex.exp (-(θ * Complex.I))) := by ring
    _ = a + t * (2 * (Real.cos (φ + θ) : ℂ)) := by rw [e1, e2, hc]
    _ = ((a + 2 * t * Real.cos (φ + θ) : ℝ) : ℂ) := by push_cast; ring

/-- rephasing generation j by d_j: H_ij ↦ d_i H_ij / d_j.  The ring product is invariant. -/
theorem holonomy_gauge_invariant (a c c' d0 d1 d2 : ℂ) (h0 : d0 ≠ 0) (h1 : d1 ≠ 0) (h2 : d2 ≠ 0) :
    (d0 * (H a c c' 0 1) / d1) * (d1 * (H a c c' 1 2) / d2) * (d2 * (H a c c' 2 0) / d0)
      = (H a c c' 0 1) * (H a c c' 1 2) * (H a c c' 2 0) ∧
    (H a c c' 0 1) * (H a c c' 1 2) * (H a c c' 2 0) = c ^ 3 := by
  refine ⟨?_, ?_⟩
  · field_simp
  · simp [H]; ring

theorem degenerate_iff (a c c' z : ℂ) (hz : z ^ 3 = 1) :
    (a + c * z + c' * z ^ 2) - (a + c * z ^ 2 + c' * (z ^ 2) ^ 2) = (c - c') * (z - z ^ 2) := by
  linear_combination (-c' * z) * hz

theorem octant_misses : (1 / 2 : ℝ) * (Real.pi / 2) - 0.666666141 > 0.1 := by
  have := Real.pi_gt_d2; norm_num at this ⊢; linarith

theorem koide_cap_misses :
    (1 / 2 : ℝ) * (2 * Real.pi * (1 - Real.sqrt 2 / 2)) - 0.666666141 > 0.25 := by
  have hp := Real.pi_gt_d2
  have h2 : Real.sqrt 2 < 1.4143 := by
    rw [show (1.4143 : ℝ) = Real.sqrt (1.4143 ^ 2) from (Real.sqrt_sq (by norm_num)).symm]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  nlinarith

end KoideHolonomy

#print axioms KoideHolonomy.ring_eigen
#print axioms KoideHolonomy.eigen_cos
#print axioms KoideHolonomy.holonomy_gauge_invariant
#print axioms KoideHolonomy.degenerate_iff
#print axioms KoideHolonomy.octant_misses
#print axioms KoideHolonomy.koide_cap_misses
