/-
AS043 — Smoothing kernel statistical interpretation.
Lean certificate: the Gaussian kernel integral identity in 1D and 3D.

Claim certified (the algebraic core of the statistical reading of
S = exp[(xi^2/2) Delta]):
  (T1)  ∫_ℝ exp(-x²/(2ξ²)) dx = √(2π) · ξ            (ξ > 0)
  (T2)  ∫_ℝ K_ξ(x) dx = 1,  K_ξ(x) = (2πξ²)^{-1/2} exp(-x²/(2ξ²))
        — the 1D Gaussian smoothing kernel is a probability kernel (normalization)
  (T3)  ∫_{ℝ³} K_ξ(x)K_ξ(y)K_ξ(z) dx dy dz = 1
        — the 3D kernel (2πξ²)^{-3/2} exp(-|x|²/(2ξ²)) integrates to 1 on ℝ³
        (product separability of the isotropic Gaussian).

These are exactly the identities behind "S is a Gaussian smoothing kernel of
width ξ in Euclidean measure": the heat kernel of exp(tΔ) at t = ξ²/2 is the
isotropic Gaussian density K_ξ, which is a probability measure on ℝ³.
-/
import Mathlib

open scoped Real
open MeasureTheory

noncomputable section

namespace AS043

/-- 1D Gaussian smoothing kernel of width ξ (std ξ), Euclidean measure. -/
def K (xi x : ℝ) : ℝ :=
  (Real.sqrt (2 * Real.pi * xi ^ 2))⁻¹ * Real.exp (-(x ^ 2 / (2 * xi ^ 2)))

/-- T1: the unnormalized Gaussian integral in 1D. -/
theorem gaussian_integral_1d (xi : ℝ) (hxi : 0 < xi) :
    (∫ x : ℝ, Real.exp (-(x ^ 2 / (2 * xi ^ 2)))) = Real.sqrt (2 * Real.pi) * xi := by
  have hsq : Real.sqrt (2 * Real.pi * xi ^ 2) = Real.sqrt (2 * Real.pi) * xi := by
    rw [show 2 * Real.pi * xi ^ 2 = (2 * Real.pi) * xi ^ 2 by ring]
    rw [Real.sqrt_mul (by positivity : 0 ≤ 2 * Real.pi) (xi ^ 2)]
    rw [Real.sqrt_sq hxi.le]
  calc
    (∫ x : ℝ, Real.exp (-(x ^ 2 / (2 * xi ^ 2)))) =
        ∫ x : ℝ, Real.exp (-(1 / (2 * xi ^ 2)) * x ^ 2) := by
      apply integral_congr_ae
      filter_upwards with x
      congr 1
      field_simp [hxi.ne']
    _ = Real.sqrt (Real.pi / (1 / (2 * xi ^ 2))) := by
      rw [integral_gaussian (1 / (2 * xi ^ 2))]
    _ = Real.sqrt (2 * Real.pi) * xi := by
      rw [show Real.pi / (1 / (2 * xi ^ 2)) = 2 * Real.pi * xi ^ 2 by
        field_simp [hxi.ne']]
      rw [hsq]

/-- T2: the 1D Gaussian smoothing kernel is normalized (probability kernel, unit mass). -/
theorem kernel_normalized_1d (xi : ℝ) (hxi : 0 < xi) : (∫ x : ℝ, K xi x) = 1 := by
  unfold K
  rw [integral_const_mul]
  rw [gaussian_integral_1d xi hxi]
  have hsq : Real.sqrt (2 * Real.pi * xi ^ 2) = Real.sqrt (2 * Real.pi) * xi := by
    rw [show 2 * Real.pi * xi ^ 2 = (2 * Real.pi) * xi ^ 2 by ring]
    rw [Real.sqrt_mul (by positivity : 0 ≤ 2 * Real.pi) (xi ^ 2)]
    rw [Real.sqrt_sq hxi.le]
  rw [hsq]
  -- (√(2π) ξ)⁻¹ · (√(2π) · ξ) = 1
  rw [inv_mul_cancel₀]
  positivity

/-- T3: the 3D isotropic Gaussian kernel integrates to 1 over ℝ³ (product separability:
the 3D kernel is K_ξ(x)·K_ξ(y)·K_ξ(z), and ∫_{ℝ³} = (∫_ℝ)³ by Fubini). -/
theorem kernel_normalized_3d (xi : ℝ) (hxi : 0 < xi) :
    (∫ p : ℝ × ℝ × ℝ, K xi p.1 * K xi p.2.1 * K xi p.2.2) = 1 := by
  have h1 := integral_prod_mul
    (μ := (volume : Measure ℝ)) (ν := (volume : Measure (ℝ × ℝ)))
    (f := K xi)
    (g := fun q : ℝ × ℝ => K xi q.1 * K xi q.2)
  -- h1 : ∫ z : ℝ × (ℝ × ℝ), K xi z.1 * (K xi z.2.1 * K xi z.2.2) ∂(volume.prod volume)
  --      = (∫ x : ℝ, K xi x) * ∫ q : ℝ × ℝ, K xi q.1 * K xi q.2
  have h2 := integral_prod_mul
    (μ := (volume : Measure ℝ)) (ν := (volume : Measure ℝ))
    (f := K xi) (g := K xi)
  -- h2 : ∫ z : ℝ × ℝ, K xi z.1 * K xi z.2 = (∫ K xi) * ∫ K xi
  calc
    (∫ p : ℝ × ℝ × ℝ, K xi p.1 * K xi p.2.1 * K xi p.2.2)
        = ∫ z : ℝ × (ℝ × ℝ), K xi z.1 * (K xi z.2.1 * K xi z.2.2) := by
          apply integral_congr_ae
          filter_upwards with z
          ring
    _ = (∫ x : ℝ, K xi x) * ∫ q : ℝ × ℝ, K xi q.1 * K xi q.2 := by
          simpa [MeasureTheory.Measure.volume_eq_prod] using h1
    _ = (∫ x : ℝ, K xi x) * ((∫ x : ℝ, K xi x) * ∫ x : ℝ, K xi x) := by
          rw [MeasureTheory.Measure.volume_eq_prod]
          rw [← h2]
    _ = 1 := by
          rw [kernel_normalized_1d xi hxi]
          ring

end AS043

#print axioms AS043.gaussian_integral_1d
#print axioms AS043.kernel_normalized_1d
#print axioms AS043.kernel_normalized_3d
