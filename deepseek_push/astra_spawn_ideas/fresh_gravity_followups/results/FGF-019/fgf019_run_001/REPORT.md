# FGF-019: real SZ mask and finite pressure-gradient ambiguity

**Worker outcome: supports_scoped_claim.** For the declared ZW1215 spherical,
12-annulus finite pressure model using the actual cached mask geometry and
cached beam, the gradient at the nominal 1252 kpc target is not uniquely
identified when outer pressure and a map-background offset are free. Freezing
those nuisance quantities gives a full-rank positive control. An explicit
pair of positive, decreasing synthetic pressures gives identical model bins
but target gradients differing by **0.631677% of the baseline gradient**.

**This is an exhibited non-uniqueness width, not a sharp bound. It does not
show that a correction large enough to close the cluster force discrepancy
is feasible, and does not imply that all gradients are unconstrained.** The
synthetic pair is not fitted to the observed map. Actual annular observations,
finite-model identifiability, and missing likelihood/covariance information
remain distinct. No claim is made about the full map or unrestricted
continuum pressure functions.

This is an Astra execution by `/root/catalogue_audit`, not DeepSeek. It uses
no new downloads, literature mechanism, theory closure or novelty claim.
A separate orchestrator review must pin this returned result before promotion.

## Actual geometry and full-annulus mask audit

Fifteen pinned source hashes match the earlier catalog evidence, including
the 1.78 GB SZ map, its mask, the beam, six original X-COP profile files,
eRASS catalogue, source coordinates and FGF-012 result. The FGF-012 reviewed
scope licenses the conditional geometry/data comparison, not a probability
interpretation or independent thermal likelihood. Stage five supplies the
question about local pressure information; no continuum compensation-rank
hypothesis is assumed authenticated for the instrument.

A fiducial flat distance conversion uses H0=70 km/s/Mpc, Omega_m=.315 and
Omega_Lambda=.685 with X-COP redshifts. This added convention gives:

| Object | z | Fiducial DA, Mpc | Target radius, kpc | Target angle, arcmin |
|---|---:|---:|---:|---:|
| A644 | 0.0704 | 276.932804 | 1331 | 16.522568 |
| ZW1215 | 0.0766 | 299.129313 | 1252 | 14.388623 |

Both target radii lie inside the original gas/star/hydro profile supports.
This does not authenticate common angular/cosmology/center conventions in
those reductions. No X-COP profile is extrapolated to construct outer pressure;
the outer pressure is explicitly a free finite model, not an observed profile.

The mask audit inspects **all pixel centers in every complete annulus**:
twelve equal-width rings from 0 to 2 target radii, plus rings 2–3, 3–4 and
4–5. Both complete radial domains fit inside their extracted 512-square
patches. It finds:

- **A644: every inspected pixel is masked zero**, including all rings out to
  5 target radii (82.61 arcmin). This is stronger than the earlier center-only
  warning. The calculation does not treat A644 as a usable pressure target.
- **ZW1215: every inspected pixel has mask one**, in all fifteen rings out to
  71.94 arcmin. The twelve analysis rings contain 73–1662 pixels each, and all
  their y values are finite. Pixel counts are not independent sample counts.

The actual mask-weighted y means range from 4.566150573e-5 in the innermost
ring to -2.674516799e-7 in the last analysis ring. The further three coverage
rings have means -2.707803526e-7, -5.585680029e-7 and -3.445909604e-7. These
are descriptive map reductions, not background estimates, thermal gradients,
error bars or significance. Outer-ring measurements were not used as additional
rows in this finite identifiability test.

`annular_coverage.json` preserves every ring's counts, mask extrema/mean,
weighted normalization, angular boundaries and y mean. `geometry.json` pins
positions, distance assumption, map origins and support. There is no assumption
that a usable center alone establishes annular coverage.

## The explicit finite observation model

Electron pressure is projected as
 y(theta)=sigma_T/(m_e c²) integral Pe(sqrt[(DA theta)²+l²]) dl.
Let x=r/Rt, Rt=1252 kpc, and p(x)=sigma_T Rt Pe(Rt x)/(m_e c²).
The Abel projection is integrated analytically for continuous linear hats at
nodes

    0,.18,.36,.54,.72,.90,1.10,1.28,1.46,1.64,1.82,2,2.5,3,4,5.

The final node is fixed to zero, leaving 15 pressure amplitudes. The target
L p=[p(1.10)-p(.90)]/.20 is the exact derivative on this model's interval
(.90,1.10), which contains x=1. It is not a derivative assigned at a radial
knot and is not an unrestricted physical derivative observable.

Projection is evaluated at actual map pixel centers. The beam operation uses
the cached b_ell, with explicit ell<=17000 cutoff motivated by the local
provenance note. It applies a tangent-plane FFT with local CAR pixel spacing,
a 512-square source patch, and zero padding to 1024 before convolution. The
projected support x<=5 lies inside the patch; its nearest edge is at x=8.83.
The finite operator is an explicit flat-sky, discretized approximation; the
complete instrument filtering, pixel response and lowpass conventions are
not newly authenticated. The cached beam has b0=1 and b17000=0.0035360375.

After beam application, the same mask-normalized weights used on data produce
a 12x15 pressure matrix A. A constant **map offset after convolution** adds a
column of ones, producing H=[A,1], of size 12x16. This background is not a
physical pressure constant and is not a zero-padded constant patch passed
through the FFT. Therefore its transfer has no artificial patch-edge loss.
The annular weights preserve a constant map offset to 2.22e-16. A beam b0=1
check alone would not justify a finite-patch pressure-background equivalence.

## Rank, positive control and explicit null witnesses

The twelve inner pressure columns (through x=2) form a nonsingular matrix.
The smallest/largest singular values are 0.00856580/4.77447, condition number
557.388. The full 12x16 matrix has smallest nonzero singular value 0.00862792
and largest 11.68846. These are far above the scale-dependent default rank
thresholds, approximately 1.27e-14 and 4.15e-14 respectively. This records
rank in the explicitly dimensionless coefficient scaling; it is not a noise
or likelihood threshold. The target row's relative residual after projection
into row(H) is 0.009480543, well above the numerical 1e-8 guard.

With the **correct known** outer/background amplitudes frozen, the inner
pressure amplitudes recover from noiseless synthetic data with maximum relative
error 1.7542e-14. This positive control establishes finite-basis identifiability
under that boundary assumption, not the truth of the assumption. The condition
number warns that noiseless recovery does not imply a stable empirical gradient
estimate without covariance or regularization analysis.

For each of the outer nodes x=2.5,3,4 and the background offset, solving for
compensating inner coefficients yields an explicit null vector. All relative
operator residuals are <=5.57e-17. The three outer-node modes separately admit
positive decreasing pressure pairs with demonstrated gradient separations
0.2153%, 0.4035% and 0.2866% of the common synthetic baseline. Thus ambiguity
does not depend solely on the background mode. These are individual witnesses,
not extrema or a sweep of physically preferred models.

The largest of the four constructed pairs uses the background direction.
Starting from p_i=1e-5 exp(-x_i), it gives:

| Synthetic quantity | Plus witness | Minus witness |
|---|---:|---:|
| Target dp/dx | -3.6965672309e-6 | -3.6732903734e-6 |
| Electron-pressure derivative, Pa/m, under the fiducial scaling | -3.0481551877e-36 | -3.0289613061e-36 |

Both profiles have positive free pressure nodes and decrease strictly to the
fixed zero outer boundary. Their gradient difference is 2.327685748e-8 in
normalized units, or 0.631677% of the baseline. Their maximum binned y difference
is 3.3881e-21 and relative difference is 1.1326e-16. The independent analytic
projection-versus-line-of-sight quadrature control agrees to 4.44e-15.

This pair shows global noninjectivity within the positive, decreasing finite
model on the measured geometry. It does **not** prove that two such profiles
fit the actual observed y vector, nor that positivity would leave a large
ambiguity for that particular data vector. It does not exclude information in
finer annuli, azimuthal pixels, the measured outer rings, different bases or
additional independently justified outer/background constraints.

## Reusable artifact and next discriminator

`numeric_001/operator_and_witness.npz` is a small hashed scientific artifact.
It explicitly contains `nodes`, `A`, `H`, `A_unblurred`, target row `L`,
`baseline`, `null_vector`, `pressure_plus`, `pressure_minus`, both synthetic
binned predictions, and the actual `observed_annular_y`. Coefficients are the
15 dimensionless pressure nodes followed by the post-convolution background;
the outer endpoint x=5 is fixed at zero. This is sufficient to reproduce the
linear checks or formulate constrained extrema without rerunning the map read.

The changed-premise next test is to find **sharp minimum/maximum gradients**
under positivity and monotonicity for a clearly declared data-consistency set,
with primal witnesses and dual certificates. Synthetic exact-data extrema can
first establish finite-model capability; actual data require a justified
response/error set rather than fabricated per-bin errors. Additional outer
annuli or background constraints change the model and should be declared as
such. Another small null witness would not answer whether discrepancy-sized
pressure changes are feasible.

## Framework, execution and limits

The core remains a=kappa c sqrt(G rho_Lambda), kappa adopted, with both
9.3619e-11 and 1.1279e-10 m/s² footings. Constant-vacuum history and separate
H(z) history remain distinct, as do Q, R and registered M. No force or Newtonian
missing mass is calculated here: observation-map identifiability precedes and
is independent of those choices. A force comparison still needs matched local
density, pressure/composition conversion and the applicable branch. Integrated
SZ, inferred gas mass and hydrostatic-equivalent M_FORW are not substitutions.

Setup began 2026-09-27T20:29:05Z. The scientific run began
2026-09-27T20:34:48.858364Z and completed in 3.001161 seconds. The runner enforced
120 s wall, 110 s per-process CPU and 1 MiB logs, with cooperative one-thread
numerical libraries. No memory or affinity cap is claimed. Python 3.13.9,
NumPy 1.26.4, SciPy 1.14.1 and Astropy 7.2.0 were used. There was no randomness
or failed numerical attempt. The runner recorded actual dirty checkout HEAD
48905ae11213afcb9ff1b7726530bb5dd1933fe3; scientific parentage is given by the
pinned source bytes, not by that concurrent checkout state.

The computation manifest validates with current input/output hashes. The result
contract includes exact argv, actual bounds and all artifact hashes. All writes
are confined to the assigned FGF-019 run directory. Mathematical proofreading
self-review covered the new derivation and report, with no mathematical-token
corrections required; it does not stand in for independent scientific review.

There is no joint foreground/noise/calibration covariance, independent thermal
likelihood, or audited cross-covariance with Planck inputs to X-COP. ACT+Planck
and PSZ2 cannot be counted as independent merely because they are different
files. The map-mask inspection and finite nullspace result do not close those
empirical gaps or the general cluster discrepancy.
