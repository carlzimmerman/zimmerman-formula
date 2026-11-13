import Mathlib.Analysis.Normed.Module.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-!
Exact positive scaling of the simple-mu AQUAL flux and a fixed finite-volume
residual. This file certifies algebra under explicit linearity hypotheses,
not a PDE solution, solver accuracy, statistical fit, or screened v3s action.
-/

namespace ForJ0332

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- Physical flux, including g=0 without a separate exception. -/
noncomputable def flux (a : ℝ) (g : E) : E :=
  (‖g‖ / (a + ‖g‖)) • g

/-- Scaling field and acceleration scale together preserves mu and scales flux. -/
theorem flux_positive_homogeneous (a k : ℝ) (g : E) (hk : 0 < k) :
    flux (k*a) (k • g) = (k*k) • flux a g := by
  have hk0 : k ≠ 0 := ne_of_gt hk
  have hr : k * ‖g‖ / (k*a + k*‖g‖) = ‖g‖ / (a + ‖g‖) := by
    rw [← mul_add, mul_div_mul_left _ _ hk0]
  simp only [flux, norm_smul, Real.norm_eq_abs, abs_of_pos hk]
  rw [hr, smul_smul, smul_smul, mul_comm]

variable {F V : Type*} [Fintype F]

/-- One finite-volume row: fixed linear gradients and normal projection maps.
    Weights can encode oriented areas and volumes on arbitrary fixed geometry. -/
noncomputable def residual
    (grad : (V → ℝ) →ₗ[ℝ] (F → E)) (normal : F → E →ₗ[ℝ] ℝ)
    (weight : F → ℝ) (a : ℝ) (potential : V → ℝ) (source : ℝ) : ℝ :=
  (∑ f, weight f * normal f (flux a (grad potential f))) - source

/-- No symmetry, spherical geometry, or density profile is assumed.
    Boundary contributions must be homogeneous: the supplied gradient is linear. -/
theorem residual_positive_homogeneous
    (grad : (V → ℝ) →ₗ[ℝ] (F → E)) (normal : F → E →ₗ[ℝ] ℝ)
    (weight : F → ℝ) (a k : ℝ) (potential : V → ℝ) (source : ℝ)
    (hk : 0 < k) :
    residual grad normal weight (k*a) (k • potential) (k*source) =
      k * residual grad normal weight a potential source := by
  unfold residual
  simp only [map_smul, Pi.smul_apply]
  simp only [flux_positive_homogeneous a k _ hk, map_smul, smul_eq_mul]
  rw [mul_sub, Finset.mul_sum]
  congr 1
  apply Finset.sum_congr rfl
  intro f hf
  ring

/-- An exact zero residual remains zero under the joint positive scaling. -/
theorem solution_scales
    (grad : (V → ℝ) →ₗ[ℝ] (F → E)) (normal : F → E →ₗ[ℝ] ℝ)
    (weight : F → ℝ) (a k : ℝ) (potential : V → ℝ) (source : ℝ)
    (hk : 0 < k)
    (h : residual grad normal weight a potential source = 0) :
    residual grad normal weight (k*a) (k • potential) (k*source) = 0 := by
  rw [residual_positive_homogeneous grad normal weight a k potential source hk, h, mul_zero]

/-- Holding a0 fixed does not obey the joint-scaling identity, even in R. -/
theorem fixed_acceleration_scale_is_different :
    flux (1 : ℝ) (2 : ℝ) ≠ (2 : ℝ) • flux (1 : ℝ) (1 : ℝ) := by
  norm_num [flux, Real.norm_eq_abs]

/-- A fixed-geometry linear LOS projection scales the reduced deflection.
    The projection includes all chosen physical distance factors. -/
theorem deflection_projection_scales
    (project : (V → ℝ) →ₗ[ℝ] (E → E)) (potential : V → ℝ)
    (k : ℝ) (theta : E) :
    project (k • potential) theta = k • project potential theta := by
  simp only [map_smul, Pi.smul_apply]

/-- Lens source coordinate for an arbitrary total reduced deflection. -/
def lensMap (alpha : E → E) (theta : E) : E := theta - alpha theta

/-- A mass-sheet transformation includes scaling the entire original deflection. -/
def massSheet (k : ℝ) (alpha : E → E) (theta : E) : E :=
  k • alpha theta + (1-k) • theta

/-- The lens equation transforms by rescaling source coordinates. -/
theorem mass_sheet_lens_equation (k : ℝ) (alpha : E → E) (theta : E) :
    lensMap (massSheet k alpha) theta = k • lensMap alpha theta := by
  simp only [lensMap, massSheet]
  module

/-- External convergence must transform too; stellar/AQUAL scaling alone is
    not an image-preserving mass-sheet transformation. -/
theorem external_convergence_transform
    (k kappa : ℝ) (alpha : E → E) (theta : E) :
    k • alpha theta + (k*kappa+1-k) • theta =
      massSheet k (fun x => alpha x + kappa • x) theta := by
  unfold massSheet
  module

/-- Images are unchanged only after the stated source-brightness redefinition.
    No source-size/brightness prior or external-convergence constraint is assumed. -/
theorem mass_sheet_surface_brightness
    (k : ℝ) (hk : k ≠ 0) (alpha : E → E) (source : E → ℝ) (theta : E) :
    source (k⁻¹ • lensMap (massSheet k alpha) theta) =
      source (lensMap alpha theta) := by
  rw [mass_sheet_lens_equation, smul_smul, inv_mul_cancel₀ hk, one_smul]

/-- For the postulated a0 = coefficient*sqrt(rho), positive a0 scaling
    corresponds to rho scaling by k². This is an algebraic consequence of
    that postulate, not a derivation or measurement of its coefficient. -/
theorem vacuum_density_scaling
    (coefficient rho k : ℝ) (hk : 0 < k) :
    coefficient * Real.sqrt (k^2*rho) =
      k * (coefficient * Real.sqrt rho) := by
  rw [Real.sqrt_mul (sq_nonneg k), Real.sqrt_sq_eq_abs, abs_of_pos hk]
  ring

end ForJ0332

#print axioms ForJ0332.flux_positive_homogeneous
#print axioms ForJ0332.residual_positive_homogeneous
#print axioms ForJ0332.solution_scales
#print axioms ForJ0332.fixed_acceleration_scale_is_different
#print axioms ForJ0332.deflection_projection_scales
#print axioms ForJ0332.mass_sheet_lens_equation
#print axioms ForJ0332.external_convergence_transform
#print axioms ForJ0332.mass_sheet_surface_brightness
#print axioms ForJ0332.vacuum_density_scaling
