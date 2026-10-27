# The sharper empirical door in the newly landed AG4h result

The additional local results at `177591c05` change the empirical priority.
CFG926 conditionally reduces the red-lens excess with an independently
calibrated stellar-mass correction. AG4h rejects coherent distance/inclination
shifts as explanations for its large pulls, and identifies five positive-pull
Q=1 profiles as a follow-up set. These are neither five detections of cold
mass nor five demonstrated failures of every mass-to-light prescription.
[Updated source reconciliation](recent/UPDATE.md).

The operation missing from AG4h's fitted constant stellar mass-to-light
ratio and coherent acceleration offset is a **physical profile-feasibility
test**: can an allowed positive gravitating remnant produce the actual
radial residual while independently allowed stellar profiles cannot?
This does not infer a new fundamental coupling from the residual.

## A quick conditional spherical diagnostic

Fix the adopted baryonic profile, distance, inclination, acceleration law
and observational units. In the existing class-A *additive Newtonian surplus*
comparison let

\[
 \Delta g(R)=V_{\rm obs}^2(R)/R-g_{\rm baseline}(R).
\]

For an additional centered spherical component its required enclosed mass is

\[
 M_x(<R)={R^2\Delta g(R)\over G},\qquad
 \rho_x(R)={1\over4\pi G R^2}{d\over dR}[R^2\Delta g(R)].
 \tag{1}
\]

Positive spherical mass requires `M_x>=0` and nondecreasing `M_x`.
Beyond a finite remnant, `R^2 Delta g` must plateau. These conditions are
necessary and, for a specified smooth radial field with suitable origin
and outer extension, reconstruct the corresponding spherical mass.
Noise makes differentiating raw points inappropriate; interval or covariance
constraints on adjacent enclosed masses must be propagated first.

This is a diagnostic of the *declared additive spherical surplus*, not a
universal test of the full theory. In a jointly responding nonlinear
polarization action, the baseline itself changes when free mass is added;
that coupled field problem must be solved rather than applying (1) as its
exact inverse. A negative result in (1) rejects this spherical comparison
only. The scalar state must also use its own predicted shape and scale.

## The nonlocal geometry and stellar alternative must be retained

At fixed geometry the Newtonian acceleration from nonnegative trial mass
elements can be written

\[
 g_{x,i}=\sum_j A_{ij}m_j,\qquad m_j\geq0.
 \tag{2}
\]

`A` is the force kernel for specified rings, shells or state-derived volume
elements at the measured radii. Positive disk rings can pull *outward* at
radii inside them. Therefore `A_ij` need not be positive, and pointwise
signs or the spherical derivative in (1) do not test all positive disks.
Radial kinematics also leave a vertical-force degeneracy.

Use independently specified support/height, resolution, finite supply
and outer-profile constraints. An unrestricted collection of arbitrarily
thin rings with unlimited mass can be too flexible to discriminate a
mechanism. Smoothing or support chosen after seeing the residual would
be additional inference assumptions, not parameter-free predictions.
For an actual proposed collective state, derive those restrictions from
its existing action and its measured host/state inputs.

For a fixed finite discretization and an exact residual vector `d`, the
basic positive-mass feasibility question is `A m=d, m>=0`. A useful
negative certificate is a vector `y` with

\[
 A^T y\geq0,\qquad y^T d<0:
 \quad y^T A m\geq0\text{ for all }m\geq0.
 \tag{3}
\]

Only this direct implication is asserted; no claim of exhaustive continuum
exclusion follows from a finite grid. With observational uncertainty,
the negative inequality must hold over the admitted residual/error set,
and source/nuisance uncertainties change the relevant kernels or residuals.
A feasible mass profile is an allowed inverse solution, not a prediction
of formation or proof of its uniqueness.

The competing stellar explanation must allow *independently constrained*
radial stellar mass-to-light variation, gas and bulge geometry, and
radius-dependent kinematic systematics. AG4h's coherent-offset rejection
does not exclude them. Compare those alternatives in the same observational
space and propagate their errors; do not fit a stellar gradient merely to
remove a desired residual or relabel an arbitrary extra profile as memory.

## Why this advances the original collective-state question

The five candidate profiles provide a smaller and better defined empirical
target than one common pressure-support amplitude. UGC08286 is a useful
first candidate in the inspected AG4h result because its positive Q=1
profile also has TRGB and CF4 distance agreement; this does not establish
perfect kinematics or a known stellar profile. UGC00731 has a larger
reported shape discrepancy but lacks that independent-distance control.

If the residual is not admissible as the proposed physical remnant, that
candidate cannot supply the requested memory there. If an admissible
remnant survives the independently constrained stellar alternatives, it
specifies a density/scale target for the same-operator response test in
[SPECTRAL_RECEIPT.md](SPECTRAL_RECEIPT.md). It still owes the canonical
polarization action, physical release mechanism and retention dynamics.
Static rotation profiles alone cannot measure those three implications.

This packet derives the feasibility gate and reconciles the new evidence;
it does **not** execute a radial reconstruction, infer a new mass profile,
fit a stellar gradient, or predict a lifetime. AG4h already identifies the
five objects; the sharper addition is the constrained physical force-profile
test, including its geometry and identifiability limits. The local search
found prior positivity checks for an ideal QUMOND disk, not this measured
five-profile problem. No literature-wide novelty is claimed.
