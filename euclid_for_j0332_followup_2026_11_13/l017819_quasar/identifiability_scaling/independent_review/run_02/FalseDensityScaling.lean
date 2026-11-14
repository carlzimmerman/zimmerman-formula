import Mathlib.Analysis.Normed.Module.Basic
import Mathlib.Topology.Algebra.Module.Basic
import Mathlib.Tactic

/-!
Conditional fixed-geometry AQUAL / lens mass-sheet identities.
The divergence, boundary operator and deflection projection below are supplied
linear maps, not analytic constructions. This file neither solves a PDE nor
realizes an external sheet as a self-consistent AQUAL matter distribution.
-/

namespace ConditionalScaling

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- The dimensionless field argument is invariant under positive joint scaling.
    Positive a explicitly excludes Lean's total-division extension at a=0. -/
theorem argument_invariant (a k : ℝ) (g : E) (ha : 0 < a) (hk : 0 < k) :
    ‖k • g‖ / (k * a) = ‖g‖ / a := by
  rw [norm_smul, Real.norm_eq_abs, abs_of_pos hk]
  field_simp [ne_of_gt ha, ne_of_gt hk]

noncomputable def flux (mu : ℝ → ℝ) (a : ℝ) (g : E) : E :=
  (mu (‖g‖ / a)) • g

/-- No differentiability, monotonicity or particular simple-mu choice is needed
    for this algebra. Physical applicability of mu is a separate premise. -/
theorem flux_scales (mu : ℝ → ℝ) (a k : ℝ) (g : E)
    (ha : 0 < a) (hk : 0 < k) :
    flux mu (k*a) (k • g) = k • flux mu a g := by
  unfold flux
  rw [argument_invariant a k g ha hk]
  rw [smul_smul, smul_smul, mul_comm]

variable {X : Type*}

noncomputable def fieldFlux (mu : ℝ → ℝ) (a : ℝ) (g : X → E) : X → E :=
  fun x => flux mu a (g x)

theorem field_flux_scales (mu : ℝ → ℝ) (a k : ℝ) (g : X → E)
    (ha : 0 < a) (hk : 0 < k) :
    fieldFlux mu (k*a) (k • g) = k • fieldFlux mu a g := by
  funext x
  exact flux_scales mu a k (g x) ha hk

/-- An abstract linear divergence equation with fixed unit-mass profile remains
    satisfied. A normalization such as 4*pi*G can be included in unitSource.
    This is conditional algebra, not analytic PDE existence or uniqueness. -/
theorem source_equation_scales
    (divergence : (X → E) →ₗ[ℝ] (X → ℝ))
    (mu : ℝ → ℝ) (a k M : ℝ) (g : X → E) (unitSource : X → ℝ)
    (ha : 0 < a) (hk : 0 < k)
    (h : divergence (fieldFlux mu a g) = M • unitSource) :
    divergence (fieldFlux mu (k*a) (k • g)) = (k*M) • unitSource := by
  rw [field_flux_scales mu a k g ha hk, map_smul, h, smul_smul]

/-- Compatible linear boundary data must scale too. Fixed nonzero boundary data
    are not covered unless they remain compatible with the transformation. -/
theorem boundary_scales {Y : Type*} [AddCommGroup Y] [Module ℝ Y]
    (boundary : (X → E) →ₗ[ℝ] Y) (g : X → E) (b : Y) (k : ℝ)
    (h : boundary g = b) : boundary (k • g) = k • b := by
  rw [map_smul, h]

/-- This projection includes all held-fixed distance and weak-field factors. -/
theorem deflection_scales
    (project : (X → E) →ₗ[ℝ] (E → E)) (g : X → E) (k : ℝ) :
    project (k • g) = k • project g := by
  exact map_smul project k g

noncomputable def lensMap (alpha : E → E) (shear : E →ₗ[ℝ] E)
    (kappa : ℝ) (theta : E) : E :=
  (1-kappa) • theta - alpha theta - shear theta

/-- The explicit convergence and shear transformation is essential. -/
theorem lens_map_scales (alpha : E → E) (shear : E →ₗ[ℝ] E)
    (kappa k : ℝ) (theta : E) :
    lensMap (k • alpha) (k • shear) (k*kappa+1-k) theta =
      k • lensMap alpha shear kappa theta := by
  simp only [lensMap, Pi.smul_apply, LinearMap.smul_apply]
  module

noncomputable def sourceRescale (k : ℝ) (source : E → ℝ) : E → ℝ :=
  fun beta => source (k⁻¹ • beta)

/-- The equality actually holds for any brightness function, hence for every
    continuous source without a fixed-size, fixed-flux or fixed-grid prior. -/
theorem surface_brightness_invariant (alpha : E → E) (shear : E →ₗ[ℝ] E)
    (kappa k : ℝ) (source : E → ℝ) (theta : E) (hk : 0 < k) :
    sourceRescale k source
      (lensMap (k • alpha) (k • shear) (k*kappa+1-k) theta) =
      source (lensMap alpha shear kappa theta) := by
  rw [lens_map_scales]
  unfold sourceRescale
  rw [smul_smul, inv_mul_cancel₀ (ne_of_gt hk), one_smul]

theorem rescaled_source_continuous (k : ℝ) (source : E → ℝ)
    (h : Continuous source) : Continuous (sourceRescale k source) := by
  unfold sourceRescale
  exact h.comp (continuous_const.smul continuous_id)

/-- Any fixed image formation operator, including fixed PSF convolution and
    pixels, preserves this equality. No discretized source prior is asserted
    invariant: an arbitrary fixed source grid need not admit sourceRescale. -/
theorem observed_image_invariant {P : Type*}
    (observe : (E → ℝ) → P) (alpha : E → E) (shear : E →ₗ[ℝ] E)
    (kappa k : ℝ) (source : E → ℝ) (hk : 0 < k) :
    observe (fun theta => sourceRescale k source
      (lensMap (k • alpha) (k • shear) (k*kappa+1-k) theta)) =
      observe (fun theta => source (lensMap alpha shear kappa theta)) := by
  apply congrArg observe
  funext theta
  exact surface_brightness_invariant alpha shear kappa k source theta hk

/-- Algebraic preservation of the user's squared a0-density postulate.
    Distances and all lensing geometry above are held fixed; no Friedmann or
    cosmological-distance equations are asserted along this family. -/
theorem density_relation_scales (a c G rho k : ℝ)
    (h : a^2 = (c^2*G/4)*rho) :
    (k*a)^2 = (c^2*G/4)*(k^3*rho) := by
  rw [mul_pow, h]
  ring

/-- Nontrivial positive scaling changes positive density. -/
theorem density_changes (rho k : ℝ) (hrho : 0 < rho) (hk : 0 < k)
    (hne : k ≠ 1) : k^2*rho ≠ rho := by
  intro h
  have hsquare : k^2 = 1 := by
    apply (mul_right_cancel₀ (ne_of_gt hrho))
    simpa using h
  have : k = 1 := by nlinarith
  exact hne this

/-- A fixed-tracer linear force functional scales a second moment. This only
    applies if a chosen Jeans/projection construction really is that linear
    functional with compatible boundary data; no such construction is proved. -/
theorem conditional_second_moment_scales
    (moment : (X → E) →ₗ[ℝ] ℝ) (g : X → E) (k : ℝ) :
    moment (k • g) = k * moment g := by
  simpa using map_smul moment k g

end ConditionalScaling

#print axioms ConditionalScaling.argument_invariant
#print axioms ConditionalScaling.flux_scales
#print axioms ConditionalScaling.field_flux_scales
#print axioms ConditionalScaling.source_equation_scales
#print axioms ConditionalScaling.boundary_scales
#print axioms ConditionalScaling.deflection_scales
#print axioms ConditionalScaling.lens_map_scales
#print axioms ConditionalScaling.surface_brightness_invariant
#print axioms ConditionalScaling.rescaled_source_continuous
#print axioms ConditionalScaling.observed_image_invariant
#print axioms ConditionalScaling.density_relation_scales
#print axioms ConditionalScaling.density_changes
#print axioms ConditionalScaling.conditional_second_moment_scales
