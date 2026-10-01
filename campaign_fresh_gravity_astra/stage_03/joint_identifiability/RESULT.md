# Joint inference: one nuisance can be identified; three map scales have a symmetry

Base: AFG-008, Git eccd1c0e59459b5ec1acf2e916fb7a05a7f67971.
Exact code and inherited-input hashes are in `run_002/manifest.json`.
This is synthetic identification work, not an observed gravity measurement.

## 1. Spatial second moments can separate scale from a width multiplier

Let the source width variance be lambda s0_i² with known shape and one unknown
positive multiplier. For fixed baryonic, emissivity and geometry maps,

    M2(a,lambda) = P[I q F(B;a)] + lambda P[I s0²].       (J1)

The two response columns are

    J_a=P[I q partial_a F],   J_lambda=P[I s0²].          (J2)

They distinguish the two parameters locally whenever they are linearly
independent. For Q, partial_a F=B/(2sqrt(B²+aB)); for RAR, with t=sqrt(B/a),

    partial_a F = B t exp(-t)/[2a(1-exp(-t))²].           (J3)

Both derivatives are positive. A single aperture supplies one second moment
and cannot identify two free parameters. Multiple spatial elements can, if
their geometry/field and broadening responses have different shapes after P.
This is a Jacobian/local statement, not global uniqueness.

The executable check evaluates 36 combinations: Q and RAR, three PSF widths,
64/16/one observed pixels and a=1/E(3). The injected width multiplier is 1.44,
equivalent to a 20% width increase. All 24 spatial cases have rank two and
recover both parameters from four starting points; all 12 aperture cases have
rank one, with an explicit alternative positive-width scale solution. Fixed
design weights are used; no true-parameter covariance is supplied to the fit.
This recovers a noiseless model. It is not a finite-noise observational error
forecast or a proof that other remote solutions are impossible.

Fixing lambda incorrectly at one produces a biased scale. The complete bias
table is saved, rather than counted as support for either redshift branch.
The result is compatible with the previous coarsening obstruction: that earlier
estimator cancelled arbitrary latent velocities and allowed a specified varying
width map; this fit restricts velocities by the gravity law and restricts the
unknown width to one common multiplier. Those are additional model assumptions.

## 2. Local rank is not enough

The previous two-scale second/fourth-moment example has a nonsingular local
Jacobian at BOTH solutions. The determinant is approximately +0.001573 at
a=1 and -0.0004324 at a=E(3). Column-normalized smallest singular values are
0.001517 and 0.0007917. Thus both fits can have local inverse maps while
remaining globally ambiguous. An assertion based only on a nonsingular Fisher
matrix would overclaim identification.

The first bounded run failed because a test required an arbitrary dimensional
determinant magnitude >0.001, excluding the second nonzero determinant. Replaced
that unsuitable threshold with a column-normalized numerical rank check and
saved both determinant/singular values. The failed run remains on disk. This
was a test-definition error, not a physical counterexample suppressed in fitting.

## 3. An exact full-spectrum symmetry when map calibrations float

Both core functions are homogeneous:

    F(cB;ca) = c F(B;a),  c>0.                           (J4)

For Q this follows by factoring c² from the square root. For RAR the ratio
B/a in the exponential is unchanged and its prefactor scales by c.

Introduce a common baryonic normalization beta and geometric normalization
gamma relative to specified map shapes. The source velocities obey

    u_i² = gamma q_i F(beta B_i;a).

The transformation

    (a,beta,gamma) -> (ca,c beta,gamma/c)                 (J5)

leaves every u_i² invariant. With signs unchanged, the same line broadening,
emissivity and angular PSF, it leaves the ENTIRE predicted spectral cube
unchanged. No sixth moment or increase in photon count can distinguish points
on that orbit without an independent constraint on the maps.

The three logarithmic response columns therefore obey the exact dependence

    J_log(a) + J_log(beta) - J_log(gamma) = 0.            (J6)

This is stronger than the earlier unknown-width two-moment example, but it
also permits more nuisance freedom. The finite test applies c=.5, E(3), 10
to both Q and RAR on a 64-pixel, 701-channel cube. The spectra agree to floating
precision. The universal statement rests on (J4), not that grid.

**Physical restriction:** beta and gamma are test calibration freedoms, not
established uncertainties. Gamma can formally represent a common distance
factor at fixed angular geometry: r scales with distance, while a common
photometric mass-conversion beta rescales baryonic acceleration. But changing
distance, inclination or gas/stellar conversion may also change other maps and
has independent observational constraints. A stellar M/L change alone does
not uniformly rescale a gas-rich baryonic map. Likewise the core cosmological
scale is externally constrained under a specified hypothesis. Nothing here
claims factors of 4.57 are plausible measurement errors or that observed
redshift evolution can always be dismissed.

## Decision

Spatial information can remove the one-width ambiguity conditional on known
source/geometry maps. Absolute scale identification still requires independent
calibration that breaks (J5), or physically restrictive map models. A complete
measurement likelihood must include this dependence. The calculation improves
the inference contract; it does not derive dynamics or close the cluster gap.
