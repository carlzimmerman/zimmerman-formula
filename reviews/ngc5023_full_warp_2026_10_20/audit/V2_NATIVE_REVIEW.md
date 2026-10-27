# Independent review of corrected native observation and arm quadrature

The inspected `forward_model_v2.py` has SHA256
`3ff79134be936f2a297d3cc948070ccee41df41ac657f106169076258b75a2aa`.
The first renderer and its earlier evidence are unchanged. The findings here
address finite observation/quadrature accuracy, not model adequacy or a full
206-parameter uncertainty posterior.

## Corrected native-grid refinement

V2 anchors the refined lattice exactly on native pixel/channel centers,
with shape`((Naxis-1)*f+1)` and source coordinates`native_coordinate*f`.
After deposition and beam/velocity convolution it restricts to native nodes
with`[::f,::f,::f]`, then applies the unchanged native-analysis interpolator.
This fixes the observation-operator change identified in the first version.

`audit/native_run002` evaluates four synthetic0.3Jy km/s clouds. The reference
independently calculates Cartesian inverse-tangent sky coordinates, NCP
projection, velocity coordinates, analytic spatial/velocity Gaussians and
eight-weight native trilinear sampling. It does not reuse the production
target-coordinate table, deposition or convolution. The production observer
is the object under test. No observed intensity data is read.

Relative L1 errors against that analytic native observation are:

| Cloud major,minor,u | Native f1 | Corrected f2 |
|---|---:|---:|
|0,0,0|0.01375|0.00337|
|0.7,1.3,2.1|0.01193|0.00504|
|13.7,-8.1,23.6|0.01633|0.00413|
|170.3,57.4,38.2|0.02175|0.00827|

The corrected f2 improves on f1 for all four tested fixtures; the original
direct-fine-grid f2 had errors0.0398–0.0456. The remaining f1–f2 differences
are0.0106–0.0297 in relative L1. These are numerical response errors, not
observed anomalies. Mean CIC-variance compensation is approximate and
subpixel-position dependent. A point-source test is not a uniform error
bound for every disk/arm family. Actual model refinement differences must
still enter the residual envelope.

The model metadata now records source flux, preconvolution deposited flux,
postconvolution native-ROI flux and sampled analysis-aperture flux separately.
This permits edge/aperture loss to be distinguished from source-normalization
errors. Native Gaussian restoring-beam response is treated consistently;
unavailable dirty-beam/CLEAN and exact spectral LSF uncertainties remain.

## Importance quadrature and half-disks

The arm rule uses inverse-CDF quadrature for a nearest-wrapped Gaussian
within phase+/-half-wedge. Its weights include
`sigma_phi sqrt(2pi) times truncated probability`; they must not be multiplied
by a second Gaussian. Zero width with finite peak gives zero integrated
arm flux, rather than an invented physical width floor.

Because side-specific PA/inclination/velocity can change at`cos(phi)=0`,
V2 splits the CDF integration at every such boundary. This addresses the
discontinuous half-disk geometry integrand. Direct side interpolation at
each resulting radius avoids assuming a fixed number of clouds per ring.

`audit/arm_run002` checks35 fixtures with widths0,1e-5,1,40,300arcsec at
radius100arcsec and phases15,89.99,90,90.01,270,-179,578degrees.
All35 pass. Independent analytic total/receding/approaching angular masses
have maximum normalized error9.0e-15. An independently integrated cosine
moment has maximum normalized error1.52e-5. This tests wide and narrow arms,
wraps and side boundaries; it does not prove full-cube morphology convergence.

`arm_run001` remains the failed first serialization attempt: numpy.bool_
was not JSON serializable. Its source and manifest are unchanged; the v2
checker casts the stored flag to a Python bool. No production formula was
changed to pass that test and no physical claim uses the failed record.

## Remaining inferential conditions

The published finite-peak width, source-amplitude and positive total-arm-mass
constraints are coupled. Collapsing an entire arm to zero width produces
zero flux and must be labelled a structural-limit diagnostic if the quoted
nonzero arm mass is also imposed. Making an arm extremely narrow while
renormalizing it to a fixed mass may require peak amplitudes outside the
digitized curve's range; such cases are sensitivity alternatives, not
automatically source-admissible posterior samples.

A family envelope is only over its executed members. Digitization error,
unknown vertical profile, published visual mismatch ranges and calibration
uncertainty remain distinct. An acceptable numerical observer does not
repair an inadequate reconstructed galaxy model or establish a robust
unexplained residual. Exact source/azimuth/width semantics and actual-data
training/validation diagnostics still govern interpretation.
