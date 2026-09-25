import Mathlib

/-!
# I23 — No real image is sharper than its PSF (the basis of the QSO1 narrow-cube artifact test, L327)

SCOPE (per lean-math-certification): Lean certifies the probability statement; the physics reading is that an observed
image is the source brightness distribution convolved with the PSF, i.e. the photon position is X + Y with X ~ source
and Y ~ PSF independent, so the observed spatial variance is Var(X) + Var(Y) ≥ Var(Y).

* `observed_variance_ge_psf` — for independent X, Y with finite second moments on a probability space,
  Var[X + Y] ≥ Var[Y]: the observed image's second moment can never be below the PSF's, whatever the source.
* `gaussian_width_floor` — the Gaussian-profile special case used for fitted FWHMs:
  FWHM_obs² = FWHM_src² + FWHM_psf² ⟹ FWHM_obs ≥ FWHM_psf.
* `qso1_narrow_below_psf` — the measured numbers: the published narrow-only core (0.111 + 3·0.004) is below the PSF
  (0.190 − 3·0.005) measured from the same cube's broad line: an image the physics cannot produce.

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

open MeasureTheory ProbabilityTheory

theorem observed_variance_ge_psf {Ω : Type*} [MeasurableSpace Ω] {μ : Measure Ω} [IsProbabilityMeasure μ]
    {X Y : Ω → ℝ} (hX : MemLp X 2 μ) (hY : MemLp Y 2 μ) (hind : IndepFun X Y μ) :
    variance Y μ ≤ variance (X + Y) μ := by
  rw [hind.variance_add hX hY]
  linarith [variance_nonneg X μ]

theorem gaussian_width_floor {obs src psf : ℝ} (hobs : 0 ≤ obs) (hpsf : 0 ≤ psf)
    (h : obs ^ 2 = src ^ 2 + psf ^ 2) : psf ≤ obs := by
  nlinarith [sq_nonneg src, sq_nonneg (obs - psf), sq_nonneg (obs + psf)]

theorem qso1_narrow_below_psf : (0.111 : ℝ) + 3 * 0.004 < 0.190 - 3 * 0.005 := by norm_num

#print axioms observed_variance_ge_psf
#print axioms gaussian_width_floor
#print axioms qso1_narrow_below_psf
