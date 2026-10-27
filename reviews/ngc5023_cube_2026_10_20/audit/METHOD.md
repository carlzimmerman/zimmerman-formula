# Independent method audit: raw-cube inversion symmetry

Checkpoint `ngc5023-cube-2026-10-20`; assessment base
`be8fc76cb0e207b88710f130abf2aa937f0895a5`.
This derivation uses no cosmology, distance, mass model, acceleration law or
stellar population calibration. It does not predict a memory signature.

## Null and what it tests

Write `r=(x,z,u)`, `u=v-vsys`, and let `P I(r)=I(-r)`. A point-symmetric,
optically thin source whose line-of-sight velocity reverses under spatial
inversion has `P I=I`. Then `E=(1-P)I` vanishes. The requirements are on
the emitting tracer and observation, not merely the gravitational field.
An axisymmetric, midplane-reflection-symmetric rotating source qualifies.
An odd bending warp `z_w(-x)=-z_w(x)` can also qualify, as can a symmetric
vertical lag. No subtraction of a rotation curve or warp is necessary to
test this broad null. A symmetric retained-mass component is inside it.

An asymmetric warp, spiral/emissivity structure, fountain, absorption or
unequal gas on opposite lines of sight may violate the null while gravity
remains ordinary. A nonzero residual is therefore a tracer/observation
diagnostic, not a direct measurement of a nonaxisymmetric gravitational
force. A centrally symmetric warp cannot explain nonzero ideal E; this is
not an exclusion of all warp geometries.

For a centered convolution kernel `B(r)=B(-r)`, `P(B*I)=B*(P I)`.
This permits an elliptical Gaussian sky beam of any position angle and a
symmetric channel response. Separate x/z reflection symmetry of the beam
is unnecessary for *central* inversion. Direction-dependent/nonstationary
response, asymmetric PSF sidelobes, incomplete spectral support, registration
and beam variation with channel need independent controls. A restored clean
beam header alone does not authenticate all residual sidelobes.

## Finite support and statistics

Use the common support `M(r) M(-r)` and finite coverage, retaining negative
emission. The sum of `I-P I` over an exactly inversion-symmetric domain is
identically zero for **every** cube. It cannot be a detection statistic.
Count one representative per pair, such as `x>0` with a fixed boundary rule,
for a signed hemispheric contrast. Absolute residuals and squared power are
positive under noise and require an identically processed noise reference.
Do not count their positive sign as evidence.

Suitable bounded exploratory summaries are: (a) total opposite-side flux
contrast in one fixed paired sky/spectral aperture; (b) residual power in
fixed beam-sized sky and channel-resolution bins; (c) height/radius maps
of those same quantities. All candidate extraction and controls are one
search family. Freeze a discovered region, sign and summary before opening
independent data; otherwise replication selection is contaminated.

An emission-threshold mask chosen from the same cube conditions its noise.
Require both a fixed aperture and paired mask versions; do not estimate
unconditional sigma by dividing selected positive voxels by a blank sigma.
If source-finding masks are used, rerun their selection in synthetic/blank
controls or restrict inference to descriptive amplitudes.

## Center and systemic nuisance

For a truly symmetric cube and a small trial center displacement
`delta=(delta_x,delta_z,delta_u)`, reflection about the wrong center gives
`E_delta(r)=2 delta dot grad I(r)+O(delta^2)`. A small center error is
therefore a coherent derivative-shaped residual, not extra independent noise.
Declare a positional/velocity range from independent astrometry and published
measurement conventions, and report both the nominal result and its minimum
over that range. A freely optimized center may absorb genuine m=1 structure;
neither its optimum nor a visually selected center is an independent datum.
Check radio/optical velocity conventions and reference frames before treating
literature vsys differences as allowed physical shifts.

For moment velocity `U(x,z)=V_mom1-vsys`, central antisymmetry is
`U(-x,-z)=-U(x,z)`. A useful four-point projector is

`Q-- U = [U(x,z)-U(-x,z)-U(x,-z)+U(-x,-z)]/4`.

It vanishes for every centrally antisymmetric U. A constant systemic offset
cancels exactly. For a straight-disk reference U odd in x and even in z,
first-order major-axis-center and PA errors do not enter Q--; a vertical
center error contributes `delta_z partial_z U`. General warped maps contain
other parity sectors, so this protection is narrower and x-center errors can
also leak. Moment1 is a noisy ratio and line-of-sight mixture; test intensity
and first moment together and do not call its difference a circular-speed
anomaly. Integrate over matched mirrored channel support.

## Interpolation and covariance

An off-grid sample is a weighted native voxel sum. If A and B are the two
sampling weight vectors and C is native covariance, then

`Var(E) = A^T C A + B^T C B - 2 A^T C B`.

Only disjoint, un-interpolated, independent equal-noise samples have variance
`2 sigma^2`. Linear interpolation lowers marginal white-noise variance;
nearby opposite samples share noise, and the beam/spectral response correlates
voxels. An interpolated reflection need not satisfy `P^2=1`. Test symmetry
using an analytic source evaluated on the native grid and the exact proposed
resampler; compare integer-grid and subpixel cases or common extra smoothing.
Measure blank/reference regions through the **same** operator and support.
Use a channel and spatial covariance estimate or block-level empirical null;
do not convert millions of voxels into millions of degrees of freedom.

For a fixed linear contrast w, variance is `w^T C w`. An inversion comparison
shares both members of each pair, so duplicating the pair doubles neither
information nor significance. A collection of a few blank tiles gives an
empirical diagnostic, not a calibrated extreme-tail probability. Any reported
formal significance needs sufficient exchangeable noise draws and treatment
of all explored center/mask/aperture/statistic choices.

## Replication gate

HALOGAS HR and LR derive from the same observations: agreement is a
resolution/processing control only. A second cube must have independently
acquired visibilities/observations, usable shared sky and spectral support,
known calibration/frame, sufficient sensitivity and a matched effective
beam/channel response. Match the higher resolution data to the poorer
response; do not deconvolve the poorer data to manufacture sensitivity.
Use the frozen candidate definition and propagate the second cube's actual
noise and coverage. A shallower second observation may be inconclusive.
An integrated spectrum or moment map cannot replicate a three-dimensional
height/channel structure. A robust small residual still requires comparison
with published asymmetric warp/spiral/tracer explanations before novelty or
new-force language.
