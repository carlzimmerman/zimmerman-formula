# Independent actual-cube computation review

Checkpoint `ngc5023-cube-2026-10-20`, 20 October 2026.
Assessment base `be8fc76cb0e207b88710f130abf2aa937f0895a5`.
Verdict: **the stated finite numerical measurements and additional diagnostic
controls are verified within the tested implementation/range. They do not
establish a new unexplained or strongly independently replicated signal.**

## Actual independent reconstruction

`actual_run001` is completed and its v2 manifest passes current-root
input/output validation. `check_actual.py` does not import either production
module. It uses a separate FITS reader; sky directions in a three-dimensional
Cartesian basis; direct NCP projection; a bounded Gaussian-convolved native
image patch; explicit bilinear sky interpolation followed by linear spectral
interpolation; and independent fixed-cell integration. It retains signed
intensities, applies WHISP int16 BLANK before BSCALE/BZERO and uses the declared
legacy secondary optical velocity reference. This checks all three actual
datasets at the frozen candidate and its inverse, not every source voxel or
nuisance trial.

The frozen region is 40 x 40 arcsec by 24.72 km/s, centered at projected
`x=160 arcsec, z=60 arcsec, u=37.08 km/s`. Direct raw-cube fluxes are:

| Cube | Positive-position bin | Inverse bin | Difference |
|---|---:|---:|---:|
| HALOGAS HR | 0.040770088 | 0.090742413 | -0.049972325 |
| HALOGAS LR | 0.033807567 | 0.083655662 | -0.049848095 |
| WHISP | 0.049198446 | 0.121362594 | -0.072164147 |

Units are Jy km/s. All three differences match the saved production values
to better than `1.5e-8 Jy km/s`. The independently recomputed native
background medians match exactly. Saved candidate blank means/scatters
and the global squared-asymmetry statistic were also reconstructed from
the archived arrays; their maximum absolute discrepancy is below `9e-10`.
Each dataset has 20 translated blank apertures, which overlap and are not
20 independent tail-probability trials.

## What the detection/replication numbers mean

The HR difference is large relative to the *empirical* blank scatter of
`0.004912 Jy km/s`. Dividing by it gives about ten scatter units. This is
not a ten-sigma discovery: the bin was selected from 120 exploratory bins,
the noise and CLEAN residuals need not be Gaussian/exchangeable between
empty sky and source regions, covariance is not independently known, and
the center/geometry/masks were also investigated. Absolute residual/power
statistics require their explicit noise reference.

LR repeats nearly the same difference, which is a useful processing/beam
check. It shares observations with HR, so the two cannot count as independent
replications. The independent WHISP value has the same sign and a compatible
amplitude, but its blank mean is `+0.008396` and its scatter is `0.033846
Jy km/s`: the blank-centered contrast is only `-2.38` empirical scatter
units. This is suggestive directional agreement, not secure replication of
a new small residual. No Gaussian-tail probability is authenticated here.

## The original feature mask did not isolate the candidate

The original mask tests bin *centers* against a 40-arcsec exclusion. The
candidate lies 48 arcsec in x and 32 arcsec in z from listed Feature 2.
Its spatial footprint `[140,180] x [40,80]` overlaps the nominal feature
box `[72,152] x [52,132]` over roughly 21% of its area before the 40-arcsec
beam is considered. Its velocities also overlap the feature's range.

The independent rectangle-intersection implementation in `additional_run001`
confirms that all footprint-aware 40/60/80-arcsec feature masks remove the
frozen candidate. They leave respectively 112, 106 and 104 paired search
bins. The candidate is therefore not authenticated as separated from known
structure. This overlap does not itself prove a physical identification or
that every residual is already explained.

## Centering cannot be dismissed with a single local cancellation

The coarse HR trial `(dx,dz,dv)=(8arcsec,-8arcsec,4km/s)` nearly cancels
this one bin, giving difference `+0.001126 Jy km/s`. It raises the *global*
noise-corrected squared asymmetry from `0.003315` to `0.06150`. The nominal
center is the minimum of that global statistic on the declared coarse grid.
Thus the local cancellation is not evidence that a globally acceptable
center correction explains the candidate. Conversely, the global symmetry
minimum is not an independently measured physical center or a joint center
likelihood; intrinsic source asymmetry can affect it. Report both behaviors
and retain the need for independent centering/geometry calibration.

## Additional operator and shape controls

The independent additional audit has 23 passing finite checks. It reconstructs
feature-mask intersections and substitutes least squares/SVD for the root
code's QR projection. All four-column designs have rank four; projected
template discrepancies are below `1e-9`, with orthogonality errors below
`5e-18`. Fixed-template amplitudes and their blank means/scatters agree to
better than `1.5e-8`.

HR/WHISP dewarp, extra 20/40-km/s spectral smoothing and background controls
were reproduced with source and blank apertures passing through the same
operator. This part shares the already audited production spatial sampler;
spectral filtering is independently implemented as an explicit symmetric
matrix including the nearest-edge rule. Maximum scalar differences are
below `2.6e-8 Jy km/s`. Cubic and LR ancillary transformed operators were
code-inspected but not independently reprocessed in this additional audit.

The empirical dewarp leaves HR `-0.03897` with blank scatter `0.00483`,
and WHISP `-0.05985` with scatter `0.03410 Jy km/s`. Additional spectral
smoothing and omitting the measured sky baseline do not remove the sign.
This establishes finite numerical persistence under those operations, not
exclusion of the published asymmetric warp/spiral model or source-dependent
deconvolution effects.

The later fixed-HR-template comparison is explicitly an exploratory extension
after the first frozen-bin comparison. In the original 120-bin search region,
the WHISP amplitude against the raw HR template is `1.3307`, with empirical
blank mean `-0.1451` and scatter `0.3624`. Projecting the HR template off
three linear center derivatives and one empirically derived warp shape
leaves 31.46% of its squared norm. WHISP's amplitude against that remainder
is `0.2490`, blank mean `-0.0231`, scatter `0.5023`: the remaining contrast
is below one empirical scatter unit. The strict-40 counterpart is `0.3724`,
blank mean `-0.0266`, scatter `0.6745`, likewise weak. HR amplitude one is
true by construction and is not independent validation.

This projection demonstrates that much of the *repeated shape in this
diagnostic* lies in the selected geometry-sensitive template directions.
It does not fit the complete physical warp/spiral/emissivity model, derive
priors or a joint center covariance, or prove the remaining signal absent.
The templates are data-derived and the fit uses unweighted Euclidean
projection, so it is not a universal nuisance-free likelihood statistic.

## Remaining physical/observational limits

- The common 40-arcsec restoring Gaussian is checked; full dirty-beam,
  CLEAN and direction-dependent instrumental response are not reproduced.
- Additional common spectral smoothing is a sensitivity control, not an
  exact native LSF match. HALOGAS history indicates Hanning smoothing.
- HALOGAS has optical-barycentric history and `SPECSYS=BARYCENT`; WHISP
  uses legacy optical-heliocentric coordinates. The small reference
  difference is not an exact equality, despite similar 4.12-km/s channels.
- The central 40-arcsec major-axis bin is omitted by `HALF=XX>0`.
  Reported paired fluxes are aperture summaries, not total galaxy fluxes.
- Empty-sky scatter does not capture all brightness-dependent calibration,
  deconvolution and tracer-geometry uncertainty near a real source.
- Symmetric extra mass and a symmetric memory-bearing component remain
  inside this symmetry null. Neither a nonzero residual nor a null result
  identifies or excludes such a component.

The data analysis genuinely avoids LambdaCDM, the project's acceleration
law and stellar M/L. Its bounded result is a measured raw asymmetry,
processing consistency and weak independent directional agreement, followed
by concrete known-feature/geometry limitations. It does not yet deliver a
new unexplained, independently replicated physical signal.
