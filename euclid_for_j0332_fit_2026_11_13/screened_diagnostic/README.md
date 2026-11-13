# Actual spherical weak-field screening calculation

For one smooth spherical Sérsic profile matching the scale of the conditional
image fit, the adopted screened P sector changes leading weak-field lens
deflections very little at the tested screening lengths. This is an actual
radial boundary-value solve with the adopted charge blend, rather than an
estimate from (Lstar/r)². It remains a **spherical weak-field diagnostic**,
not a full-action oblate fit or a rigorous bound for every allowed Lstar.

The profile has stellar mass1.1e12Msun, radial scale10.366696kpc, and Sérsic
n=5.8687191. The radial scale is the measured major-axis scale used as a
spherical diagnostic; this does not reproduce the full oblate density.
Canonical a0=9.3603e-11m/s² is held fixed, mu_K=0, and rho_DE is set by the
postulated kappa=1/2 relation. No empirical lens likelihood enters this solve.

## Equation and normalization

The source equations are QX17C's weak spherical reduction, with the adopted
general-F correction in QX17D. Use physical K=4piG and gamma_L=K Lstar²/2:

    Pi = div P,
    laplacian Phi = K(rho_b + Pi),
    grad Phi + gamma_L grad F'(Pi) = K W'(K|P|) P_hat,
    K W'(K|P|)/a0 = Y/(1-Y),  Y=K|P|/a0,
    F(Pi)=b² f(Pi/b), b=rho_DE.

This is leading weak field: it omits the covariant constitutive prefactor
1+gamma_L F'/c² and the PN energy/stress/metric contributions. It uses the
precise Legendre-sector normalization of QX17/QX17D rather than adding the
one-page action's J and Legendre terms as independent copies.

For s=r/Lstar, z_b=K Lstar b/a0, and Z=Y'+2Y/s,

    g/a0 = gN/a0 + Y,
    d/ds [ z_b f'(Z/z_b) ] = 2 [Y/(1-Y)-gN/a0-Y].

The first identity follows by integrating Poisson with a regular center;
it is the phantom-mass feedback, not an algebraic MOND approximation.
The finite-volume Z on each radial interval is

    Z_(i+1/2) = (s_(i+1)² Y_(i+1)-s_i²Y_i)/(h_i * mean(s²)_i),
    mean(s²)_i=(s_i²+s_i s_(i+1)+s_(i+1)²)/3.

Its integrated phantom mass telescopes to r²P to floating precision. A
tridiagonal damped Newton solve enforces the constitutive equation. The center
has Y(0)=0; the outer endpoint has the isolated law-S value. For radii beyond
the numerical endpoint the deflection integral uses isolated unscreened force.
The outer radius is varied30→100Mpc to test that approximation for named runs.
The Sérsic mass comes from512-node Abel density quadrature and a24000-node
logarithmic radial integration, not a PS density approximation.

The adopted f'' is evaluated in a stable factored form using the exact rational
parameters in AC21 iter_6's `form.json`. Its degree13 pieces are integrated
with8-node Gauss-Legendre quadrature, which integrates these polynomials
exactly apart from floating arithmetic. The checks give f'(1)=1 and
f(1)=1/2 within4e-15. Thus F becomes Pi²/2 for Pi>=b and is the correct
adopted Pi6 branch near zero, with the matched intermediate layer.

For numerical stability the restoring term uses the exactly equivalent

    2 (Y-Y_S) [1/((1-Y)(1-Y_S))-1],

where Y_S/(1-Y_S)=gN/a0+Y_S. Direct subtraction of large central terms in
the raw formula suffers roundoff; its unscaled difference is recorded rather
than concealed. The stopping test uses the roundoff-aware sum-of-term-magnitudes
scale, analogous to QX17C, and the deflections receive independent grid checks.

## Measured changes

At angular impacts .5,1,1.5,2,3arcsec, corresponding to4.10–24.62kpc:

| Lstar | fractional deflection change at1.5arcsec | largest magnitude over named impacts |
|---:|---:|---:|
|21.7pc| -1.9742e-8 |3.0805e-8|
|100pc| -4.1924e-7 |6.5418e-7|
|1000pc| -4.1940e-5 |6.5426e-5|

The charge Pi/b at the impact radii ranges from about2.8e5 down to2.9e4;
the near-lens portion is exactly in the quadratic branch. The adopted blend
is still included in the low-charge distant tail. Replacing it by the raw
positive quadratic stiffness at the floor length changes the five fractional
deflections by at most3.9e-13 in this calculation.

Radial350→700nodes per decade changes the largest-length deflection fractions
by at most8.7e-10 absolute. At the floor length the change is below7e-13.
The512→1024LOS comparison is recorded for every run; floor differences are
below5.8e-13. The .1pc known-small-length fixture agrees with unscreened
deflections to6.6e-13 at these impacts. The30→100Mpc endpoint test is provided
at21.7pc and1000pc. A separate check extends the inner numerical radius
inward100x while preserving every prior outer node: both tested lengths give
identical named deflections to recorded float precision.

At the five impact radii, mass-table enclosed fractions agree with a separate
direct Abel angular-kernel mass integral to1.42e-7 relative. A separate local
small-L expansion also predicts the measured force corrections:

    deltaY ~= (Lstar²/2) [Y_S'' + 2Y_S'/r - 2Y_S/r²]
               / [1/(1-Y_S)²-1].

For example, at1.5arcsec and21.7pc the measured fractional force change is
-1.12640e-8 and the expansion predicts -1.12636e-8. This checks the factor,
sign and source feedback independently of the boundary-value solver.

## Meaning and limits

These results support using unscreened AQUAL as the **leading smooth spherical
force-sector approximation at these fixed length fixtures**. They do not
establish a1e-8 full-action error budget. Omitted PN terms can exceed that tiny
screening correction. For example the maximum constitutive prefactor
gamma_L F'/c² across the entire radial domain is1.34e-7 at the floor length;
this is a diagnostic of one omitted term, not a bound on all omitted metric
terms or on the total lens deflection. The full stress/metric equations and
physical stellar stress tensor have not been solved here.

The record supplies a lower bound on Lstar, not a unique value or the upper
bound needed to turn these fixtures into a uniform theorem. No oblate
screened solver, arbitrary inclination, stellar granularity, external field,
cosmological embedding or nonzero dust sector is covered. The calculations
therefore narrow one approximation question without upgrading the conditional
image fit into a full screened-v3s empirical pass.

## Evidence and reproduction

The authoritative bounded run is `run_01/result.json` with the same folder's
`manifest.json`, `stdout.txt`, and `stderr.txt`. Its v2 manifest records status
`completed` and validates against current source/input hashes. Contract:
`contract.json`. `result.json` at this folder's top level is an earlier
exploratory output and should not replace the bounded-run record.

The runner command and all execution artifacts are recorded in the manifest.
The direct equivalent is:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /private/tmp/forj0332-fit-venv/bin/python -B euclid_for_j0332_fit_2026_11_13/screened_diagnostic/spherical_screen.py --output NEW_OUTPUT_DIRECTORY

The independent inner-boundary check is:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /private/tmp/forj0332-fit-venv/bin/python -B euclid_for_j0332_fit_2026_11_13/screened_diagnostic/check_inner_boundary.py

It records the main solver source hash and asserts the source remains unchanged.
All outputs and new code stay in `screened_diagnostic/`; canonical solvers and
the image-run inputs were not modified.
