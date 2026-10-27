# Independent tilted-ring forward-model and uncertainty audit

Checkpoint `ngc5023-full-warp-2026-10-20`, base
`c821a8bccc8a20e107b4c6771d31e02d05aa8b10`.
This is a derivation and finite synthetic validation, not an actual-data fit.
No cosmology, potential, acceleration law or stellar mass conversion occurs.

## Source measure and geometry

Use right-handed coordinates (east,north,line-of-sight-away). At each
intrinsic radius R, let a be the position angle measured north through
east and i the inclination. Define

`m = (sin(a),cos(a),0)`,
`q = (cos(a)cos(i),-sin(a)cos(i),sin(i))`,
`n = (cos(a)sin(i),-sin(a)sin(i),-cos(i))`.

The triad is orthonormal with `m cross q = n`. At intrinsic azimuth phi,

`r = R cos(phi) m + R sin(phi) q + z n`,

`v_los = v_sys + [V_rot(R) - L(R)|z|] sin(i)cos(phi)`.

Here positive cos(phi) is chosen receding. An approaching/receding geometry
can use separate a(R),i(R) on the two intrinsic half-disks, provided the
half-disk definition matches the source's exact TiRiFiC azimuth convention.
Changing geometry with radius or half-disk does not justify replacing
line-of-sight integration by a shifted projected midplane. Each ring's
vertical normal, velocity projection and overlaps change together.

Use a positive source measure

`dF = C Sigma(R,phi) R dR dphi f_z(z|R,phi) dz`,

where an exponential vertical profile is
`f_z = exp(-|z|/h)/(2h)`. If Sigma is dimensionless, C normalizes the
component to its integrated HI flux. A radial surface-brightness input has
its own verified units; it must not be multiplied by a fitted M/L or a
halo density. A convenient arm model is a wrapped azimuthal Gaussian
about phi_arm(R), but its width and whether amplitudes are peak or
azimuth-integrated values must come from the documented source convention.
Normalizing each arm independently to its quoted total flux avoids silently
changing its mass when its width varies.

**No additional 1/cos(i) multiplies individual source weights.** Projection
and overlapping rays create the increased brightness of an inclined disk.
Inserting that factor again would double count foreshortening and diverge
at edge-on inclination. Warped rings are a source parametrization; their
flux measure is not an inferred 3D mass density or a hydrostatic model.

Sky offsets and h may be angular units. Then L has units km/s/arcsec.
If the source reports h in kpc and L in km/s/kpc, their product Lh is
distance-independent under a consistent conversion. Converting the source's
physical lengths with its adopted nearby-galaxy distance is a local-scale
convention, not a LambdaCDM inference; record the value and its scope.

## Instrument and units

For a cloud with integrated flux dF, let g(v) be its normalized Gaussian
velocity profile. Its contribution to a channel is `dF integral_channel g dv`.
If the image stores flux density, divide by channel width; if it stores
channel-integrated flux, do not divide. Use CDF differences or a controlled
velocity quadrature, rather than nearest-channel assignment alone.

Convolve the projected image with a unit-integral spatial restoring beam.
For output Jy/arcsec2 divide each pixel's flux density by its solid angle;
for Jy/beam multiply that surface brightness by beam area
`Omega_B = pi Bmajor Bminor/(4 ln2)` in square arcsec. Do not apply a second
beam-area multiplier to already beam-normalized weights. A target Gaussian
beam uses covariance `Cextra = Ctarget - Cnative` only if positive semidefinite.
This matches restoring response, not the unknown dirty-beam/CLEAN transfer.

Kamphuis2013 section3 explicitly sets sigma=10km/s **including instrumental
effects**. Applying both that full sigma and the full native LSF again
double broadens the model. Two defensible named alternatives are: (1) treat
10km/s as the effective convolved linewidth and integrate it into channels;
(2) infer an intrinsic sigma only after an authenticated LSF is supplied,
then convolve that LSF. They are not equivalent to adding a new fitted
dispersion chosen to hide a residual. Missing exact LSF remains a model
uncertainty. Propagate old/new velocity conventions through the already
verified native spectral transformations.

At all stages test total integrated flux, constant source-component flux
under width/inclination changes, channel normalization, projection signs,
beam covariance, convergence in azimuth/radius/vertical quadrature and finite
aperture losses. Numerical convergence uncertainty must be smaller than a
claimed surviving residual; otherwise the claim is only a numerical limit.

## Symmetry benchmark

If opposing source points have equal weights and
`(phi,z)->(phi+pi,-z)` leaves ring geometry and component emissivity invariant,
then `(r,v-vsys)->(-r,-(v-vsys))`. Thus the ideal cube is point symmetric.
This includes radius-dependent but centrally symmetric warped rings,
symmetric vertical lag and equal opposite arms. A centered elliptical beam
of any position angle and a symmetric LSF preserve this null. Side-dependent
warps or unequal arms need not. A symmetry test alone therefore does not
reject the actual asymmetric model family.

## Uncertainty and validation contract

The preferred model has about206 nuisance parameters. Published visual
one-parameter mismatch ranges are not a joint covariance. Independent
Gaussian draws from all those bars, all-independent ring jitter, or a
posterior probability inferred from digitization pixels would invent missing
information. Separate at least these levels:

1. Digitization: finite line/pixel/axis uncertainties for recovered profiles.
2. Source-family ambiguity: interpolation, side/azimuth conventions, width
   interpretation and vertical/LSF variants not uniquely authenticated.
3. Published physical nuisance ranges: coherent center/vsys, height, lag,
   masses and smooth radial shape variations with named correlations.
4. Calibration inference/noise: values estimated from the actual training
   region, plus correlated blank-sky measurement error.

A bounded named ensemble can vary these levels with endpoints, coherent
radial modes and deterministic space-filling samples. Its finite extrema
are a sensitivity envelope over the executed family, **not** a posterior
credible band or a certified uniform envelope over all206 parameters.
A pointwise linear envelope `|J| r` for bounded parameter changes only
controls the linearized model; nonlinearity and interpolation error require
separate checks. Avoid claiming all-model survival merely because a few
independent errors were sampled.

With digitized shapes fixed within each family, low-dimensional positive
disk/arm flux coefficients may be calibrated on an explicitly declared
bright-disk region. Do not fit all ring amplitudes/geometry and then use
the same residual voxels as an unseen test. Allowing enough azimuthal
components can fit any emission morphology and says nothing about gravity.
The measured surface brightness and velocities are ordinary tracer/model
nuisances; they are not new fundamental force parameters.

Protect extraplanar validation regions outside footprint/beam-expanded
known-feature masks before examining the reconstructed residual. Use common
paired masks when comparing symmetry residuals. A projected inner-radius cut
still receives outer warped-ring emission along the line of sight. Beam
leakage couples a bright-disk training strip to nearby validation strips;
use a spatial guard or propagate that covariance. An assumed 40arcsec beam
does not make adjacent40arcsec boxes statistically independent.

The full published fit used these HALOGAS observations. Thus published-shape
reuse is not a fresh holdout test even if this reconstruction's calibration
uses a training subset. WHISP intensities have already been examined in the
parent phase and cannot become blind data for a new selected candidate.
Distinct campaigns are verified; zero visibility overlap is not certified.

For each family report training adequacy before interpreting validation
residuals. A large model/data mismatch on ordinary disk data means the
reconstruction is inadequate; it cannot certify an anomalous remainder.
Conversely, removing a residual after tuning on it is not an absence proof.
Compare observed residual contrasts with identically processed real-blank
apertures and model-family scatter. Do not count correlated voxels or repeated
parameter members as independent detections. A robust coherent remainder
requires adequate training predictions, controlled numerical/instrument
errors, survival across the declared model family and a separately designed
validation/replication test. New gravity or memory requires an additional
distinguishing physical prediction.

## Preserved synthetic correction

`synthetic_run001` deliberately remains as the recorded failed first attempt.
The cross-product test caught a sign error in the initially written vertical
basis: the opposite normal was orthonormal but left-handed. All other fixture
checks passed because a symmetric vertical profile is invariant under
`n -> -n`. The original script/contract and failed manifest are unchanged.
`synthetic_forward_v2.py` uses `n=m cross q`; `synthetic_run002` is the corrected
finite evidence. This correction changes a coordinate convention, not any
actual observational result.
