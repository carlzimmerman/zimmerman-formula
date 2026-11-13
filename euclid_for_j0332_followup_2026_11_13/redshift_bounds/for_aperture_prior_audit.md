# Independent FOR aperture-prior transport audit

The proposed correction is mathematically correct at **fixed light geometry,
modelling circle and constant stellar M/L**, once its aperture fraction is
validated. It changes the stellar-mass prior applied to the existing total-mass
parameter; it leaves the conditional image likelihood and association gate
unchanged. It is not a new joint photometric/SED/morphology fit.

The audited root implementation is
`euclid_for_j0332_followup_2026_11_13/mass_convention/reweight_for.py`, importing
the exact original prior from `fit_images_v2.py`. The original samples are the
four independent gated chains in `gated_posterior_02`, after the original
500-step burn-in. The corrected script was reviewed after its lower-side
survival-probability and representative-scenario labeling fixes.

## Target density and sign

Write m=log10(M_total), f=M_ap/M_total with0<f<1, and ell=log10(f). Then

    m_ap = m + ell,
    d m_ap / d m = 1.

Thus a prior density supplied per logarithmic mass interval transforms to
p_SED(m+ell); no additional f or1/f factor belongs in these log-coordinate
weights. With an optional fixed-M/L luminosity-distance shift delta of the
SED prior location, the exact ratio is

    log w = log p_SED(m+ell | mu+delta) - log p_original(m | mu).

Equivalently the numerator evaluates the unshifted prior at m+ell-delta.
The denominator must be the exact prior that generated the old samples,
including its original center, side scales and original hard support. The
reviewed implementation does this, with delta0 or+.00653358dex. Its numerical
weights use logsumexp normalization correctly.

The fitted parameter remains total stellar mass. Multiplying the posterior
mass by f changes the *reported aperture mass*, not the lensing field at that
sample. A correction with argument m-log10(f) would have the wrong sign.

## Original asymmetric surrogate

The preserved original function is

    log p(m) = -.5[(m-mu)/sigma_side]² - log(sigma_side) + constant,
    mu=11.8310873126,
    sigma_minus=.1041923878, sigma_plus=.0863788677.

With constant -log(sqrt(2pi)), each half has probability1/2. It has medianmu
and a possible density discontinuity atmu; it is **not** the usual continuous
two-piece/split-normal density. Changing it to a continuous split normal
would change the prior, not merely correct the aperture interpretation.
The quoted side errors are used as standard deviations exactly as in the
original code; this is not a new exact reconstruction of the catalog's joint
SED posterior or all of its marginal quantiles.

For a scalar required mass x, survival under this preserved surrogate is
norm.sf((x-mu-delta)/sigma_side), choosing the lower scale belowmu+delta and
the upper scale above it. The first reviewed revision always used the upper
scale; the root fixed that latent bug. Its output called
`median_difference_in_upper_SED_error_units` deliberately uses the upper
quoted scale and must not be promoted to a calibrated exclusion significance.
Survival is a conditional prior-tail diagnostic, not a theory p-value.

## Quantiles, representative image and checks

The weighted empirical CDF interpolation is a conventional finite weighted
quantile estimator. For constantell, q_ap=q_total+ell is exact as a monotone
translation. Exponentiating logarithmic quantiles gives the corresponding
linear-mass quantiles; the script does not confuse these with means.
Every parameter and shear-amplitude summary uses the same normalized weights.

The representative image is the highest new-target value **among the sampled
points**, using the catalog-redshift scenario. It is not a newly optimized
global MAP. The revised result labels that scenario explicitly. Recomputing
five original image targets verifies matching likelihood/prior conventions;
the representative gate check verifies the reported image's association.
These checks supplement, rather than replace, provenance of the original
sampler and its gate on the full chain.

Raw importance ESS>90% of sample count and per-chain median agreement support
stable transport of the represented posterior bulk. They do not establish
new global convergence, exclude missed modes, or provide autocorrelation-
corrected ESS. The original four-chain diagnostics still matter; weighted
Monte Carlo uncertainty is not identical to1/sqrt(raw importance ESS).
The script's nonclaims correctly distinguish these issues. Retaining the
original hard parameter bounds defines the same restricted-support target.

## Physical premises still required

1. The aperture fraction must match the SED normalization: unconvolved lens
   model summed in the actual modelling circle, with matching coordinates,
   profile parameters and flux conventions. It must not silently use a
   different circular aperture, PSF-convolved image or analytic elliptical
   aperture. The primary evidence now supports finite-mask SED flux; the
   numerical fraction is a separate obligation.
2. The scalar mapping assumes constant stellar M/L from the measured aperture
   to the extrapolated infinite Sérsic profile. Color/M/L gradients, IMF
   variation and unobserved outer light remain conditional assumptions.
3. At fixed geometry, f has no mass dependence and the log Jacobian is1.
   If n,Re,q,center or the circle are later marginalized, f varies and can be
   correlated with the original photometric/SED uncertainty. A single-factor
   reweight is not that expanded joint analysis.
4. The+.00653358dex case is only a distance-only sensitivity. The primary
   methods audit says Prospector uses spectroscopic redshift when available,
   otherwise photo-z. A catalog photo-z column alone does not identify the
   actual SED input redshift for FOR. The shift must not be called mandatory
   without that provenance; aperture-only transport is unaffected.
5. The correction does not address diagonal-noise approximations, source
   positivity, oblate deprojection/inclination, environmental convergence,
   screened-v3s completeness or any other unchanged likelihood premise.

No new numerical posterior results are asserted by this review before the
root's validated aperture factor and bounded correction run are available.
