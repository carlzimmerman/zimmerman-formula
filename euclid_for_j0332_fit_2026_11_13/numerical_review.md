# Independent image-likelihood numerical review

## Verdict and material finding

The Gaussian marginal-likelihood algebra, PSF convolution, released SIE/shear
coordinate convention, and fixed-geometry AQUAL scaling transform are correct
in the reviewed implementation. The original source-window gate creates a
real discontinuity and makes `image_fit_01` unsuitable for curvature-based
uncertainties. The versioned `inversion_continuous.py` fixes that discontinuity
correctly. Its `image_fit_02` objective is continuous, but the bilinear basis
still has derivative kinks: the checked local mass curvature remains strongly
step-dependent. A Gaussian uncertainty from the inverse Hessian is not
established. This does not by itself invalidate a posterior evaluated using
the continuous, explicitly stated image model.

This is an independent numerical/algebraic review of root-owned code. It
does not certify the full screened action, image noise model, posterior,
absolute field accuracy, or an empirical theory pass/fail. Root inputs and
model code were not edited by this review.

## Gaussian integration re-derived

Let l be the fixed unit-amplitude released convolved lens template, let
d0=d-l, and let c contain source coefficients, lens-amplitude offset delta,
and constant sky. Set D=[P A,l,1], C=diag(sigma²), and give c a zero-mean
proper Gaussian prior with precision

    Q = blockdiag(exp(z) R, 4, 100),
    R = L.T L + .01 I.

For W=C^(-1/2), y=W d0, H=(W D).T(W D)+Q, b=(W D).T y, and cbar=H^-1 b,
direct Gaussian integration gives

    log p(d | lens,z) = -1/2 [
        y.T y - b.T H^-1 b + logdet H - logdet Q
        + logdet C + N log(2 pi)].

At the posterior mean, y.T y-b.T cbar equals
||y-W D cbar||²+cbar.T Q cbar. This is exactly the implementation's chi2 plus
prior penalty. The data shift, lens coefficient sign, and returned total lens
amplitude 1+delta are mutually consistent. Cholesky diagonal log-determinants
are correct. logdetQ = ns²*z+logdetR+log(4*100), including nuisance priors.
The observed source-prior eigenvalues span .01 to 7.97846, so it is proper.

An orthogonal finite check compared this precision-form expression to a
direct 40-pixel covariance C+D Q^-1 D.T, using actual design rows and noise.
The log probabilities were 163.63345656188264 and 163.63345656188318,
respectively, a difference -5.4001e-13. This checks the finite numerical
normalization/sign implementation, not a universal observational likelihood.

The asymmetric mass prior is an equal-probability pair of half-normal
branches anchored at the catalog median, with sigma values equal to the
reported median-to-quantile errors. Its -log(sigma) factor correctly gives
equal integrated probability to the two halves; the density can jump at its
median. The omitted universal -log(sqrt(2pi)) does not change within-prior
parameter inference. Scores with versus without that prior are not model
Bayes factors or directly comparable absolute evidences.

## Convolution, interpolation, coordinate and scaling checks

- P's out/in indexing is ordinary zero-padded convolution with the supplied
  21x21 PSF centered at index10. A seeded random-image comparison with
  `scipy.signal.convolve2d(...,mode='same',boundary='fill')` differed by at
  most 1.9984e-15. The PSF sums to one and the likelihood-mask RMS is finite.
- Bilinear source interpolation uses surface brightness, not an integrated
  source-pixel flux; no source-pixel-area multiplier belongs in this forward
  image operator. Image supersampling averages subpixel brightness before
  PSF blurring. The released lens template is already convolved and correctly
  enters after that source convolution.
- Shear is the gradient of potential
  .5*g1*(X²-N²)+g2*X*N, giving (g1*X+g2*N,g2*X-g1*N). The SIE plus shear and
  angle/center conversions match all 102x102 released deflections with vector
  RMS 6.2537e-16 arcsec in the chosen west/north frame.
- The library transformation is exact for the restricted branch:
  alpha(M,k*a0)=k*alpha(M/k,a0). Thus the code's library mass
  logM-log10(k), followed by a factor k on its deflection, has the correct
  sign and scaling. Geometry and profile shape remain fixed. Shear and
  convergence are separate arguments and are not automatically scaled.
- All evaluated 2x2 image-subpixel radii at the fixed lens center span
  .0257115 to 7.37995 arcsec, inside the polar library's .006 to12 arcsec.
  Therefore radial nearest-mode clamping is inactive for these image rays.
  Other geometry/center choices would require a new check.
- `check_library_interpolation.py` compares a direct converged field at
  logM=12.03 to the canonical library, with the same320x64 field grid and
  256 LOS nodes. At35 off-map-grid positions (.5-7arcsec), max vector-relative
  error is 2.34745e-4 and max absolute error .000449185arcsec. At25 exact
  polar-map nodes, isolating mass interpolation, maxima are2.56547e-4 and
  .000622882arcsec. These are finite interpolation checks. The solver's
  ~1.93e-8 residual is not an absolute field-accuracy bound.

## Source-window defect, correction and remaining curvature issue

In `inversion.py`, the four bilinear weights are all gated by

    full = 0<=u<=ns-1 and 0<=v<=ns-1.

For a nonzero edge coefficient, a ray crossing u=0 has a nonzero interior
limit and zero exterior limit. The prior's ridge does not set boundary
coefficients to zero. A constant-source synthetic ray crossing from
u=-1-1e-7 to -1+1e-7 in the three-node check produced brightness [0,1],
a unit jump. This is a defined hard-edged statistical model, but it produces
unphysical numerical boundary locking in a purported smoothly sampled source.

`inversion_continuous.py` correctly retains each valid neighboring node
individually without the `full` gate. It is the continuous tensor-product
tent basis of a zero-padded grid; supports extend one source spacing beyond
the outside node centers. The same synthetic check produced brightness
[.9999999,1], a difference1.0000e-7 as expected. At the original fit's optimum,
edge coefficients were not zero: max absolute edge value .0406000, versus
median image RMS .00362861.

The footprint attribute still counts rays inside the nominal node-center
square. After the fix it is not the fraction of rays with any nonzero basis
support; label it as a nominal-grid coverage diagnostic.

With other parameters held fixed, the mass-step diagnostic is:

| mass step in dex | original negative log-evidence curvature | continuous-basis curvature |
|---:|---:|---:|
| 1e-5 | 6.4611e9 | 2.4855e7 |
| 1e-4 | 6.7137e7 | 2.7137e6 |
| .0008 | 2.7262e6 | 7.0024e5 |
| .0032 | 6.5862e5 | 3.8807e5 |

The original +1e-5dex step lost .63715 log-likelihood units despite a
-1e-5dex step losing only .00896. The corrected fit's +1e-6dex step loses
.00016278 versus .00005991 on its negative side; its curvature is2.2269e8
at that step. The finite jump is fixed, but the piecewise bilinear source
basis has derivative kinks. The optimizer's success flag certifies its
stopping criterion, not differentiability, global optimality or posterior
convergence. Neither Hessian can currently serve as a final uncertainty.

At the checked continuous fit,234/625 source coefficients are negative, but
none are negative by more than3 conditional posterior standard deviations.
The original fit likewise has no >3SD negative source pixels. This is a
limited conditional check; it does not establish physical source positivity
or its stability when lens/regularization parameters vary.

## Checks needed before scientific likelihood or posterior claims

1. Keep original artifacts frozen and use the continuous basis for subsequent
   inference. Profile or sample the nonquadratic objective; check multiple
   initial points and posterior boundary sensitivity. Treat local Hessians as
   diagnostics only.
2. Repeat actual inference over larger source extent, shifted source-grid
   center, source sampling and image supersampling. A finite fixed source
   window and its normalized Gaussian prior can constrain lens parameters.
   The source-grid center is a computational assumption, not independently
   measured source position. Resolution changes also change the source prior;
   cross-resolution scores are not literal same-prior Bayes factors.
3. Propagate or bound map/interpolation and field-solver errors at the image
   level. A small discrete PDE residual does not bound the inferred mass/a0
   error. The actual fixed-field interpolation errors above can matter if
   quoting sub-millidex conditional parameter precision.
4. Verify residuals by spatial region and held-out counterimage pixels for
   the fitted AQUAL model, not only for the SIE control. Include the PSF
   leakage caveat when withholding adjacent pixels. Check substantial
   posterior negative brightness where the source is detected.
5. Quantify noise correlations and background-template dependence. The
   diagonal released-RMS Gaussian is a coherent conditional objective; the
   observed correlations and broad-background residual structure prevent
   a calibrated chi-square rejection probability from that objective alone.
6. Treat the released convolved lens-light morphology and fixed n,Re,q,
   center, edge-on inclination and constant M/L as conditional assumptions.
   A Gaussian lens amplitude and uniform sky only marginalize those two
   template directions. They do not cover shape errors, M/L gradients,
   residual source/lens deblending error or the fixed photo-z SED-mass model.
7. Regularization is optimized, not integrated. The reported conditional
   coefficient-marginal log likelihood is not fully marginalized gravity-model
   evidence. The published SIE baseline has fixed published mass/shear values,
   while AQUAL mass/shear are optimized: raw score differences are a useful
   control comparison, not a calibrated model-selection result.
8. External convergence is fixed to zero in these fits. The exact mass-sheet
   obstruction derived in the formal certificate is broken by that
   assumption; it is not empirically measured away. External field, screened
   v3s terms, and the admissible stellar IMF/mass prior remain separately
   disclosed physical limitations.

## Reproduction and provenance

The check scripts and complete observed diagnostic values are under
`numerical_review/`, including `raw_diagnostics.log` and
`image_numerics_check.json`. Both check JSONs record input SHA-256 values
before and after and assert they are unchanged. The image finite checks use
seed173 for a random test image and40 selected design rows.

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /private/tmp/forj0332-fit-venv/bin/python -B euclid_for_j0332_fit_2026_11_13/numerical_review/check_image_numerics.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /private/tmp/forj0332-fit-venv/bin/python -B euclid_for_j0332_fit_2026_11_13/numerical_review/check_library_interpolation.py

The first run completed in4.67seconds and the second in2.28seconds in the
current fit environment. All expected finite assertions passed. The
step-curvature result is deliberately an inadequacy finding, not a passing
uncertainty calculation. No root model code, image input or library was changed.
