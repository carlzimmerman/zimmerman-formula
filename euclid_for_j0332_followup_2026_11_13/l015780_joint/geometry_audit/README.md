# L015780 source-position capacity audit

The supplied oblate AQUAL fields at the aperture-corrected nominal stellar
mass cannot satisfy the released four-marker association gate at zero
external convergence, even after allowing any source redshift and very
flexible constant shear. This is a **conditional finite-field association
diagnostic**, not an image likelihood, calibrated rejection probability or
full-theory exclusion. Unknown environmental convergence remains material.

The authoritative numerical record is `run_01/result.json`, `summary.csv`
and its validated v2 manifest. `capacity.py` is frozen. The formal certificate
is separate; use `formal/run_02` for its accepted and genuine negative-control
compile provenance. An earlier formal verifier's negative-control path error
is preserved and explicitly superseded.

## Actual markers, transforms and control

The released pipeline positions(y,x), in arcseconds, are
(1.85,-1.95),(2.65,-.55),(.75,2.65),(-1.75,-.55). Transform to
west/north by(X,N)=(x,-y). The four west/north coordinates are therefore
(-1.95,-1.85),(-.55,-2.65),(2.65,-.75),(-.55,1.75).

`positions_meta.json` records version2.1, statuskeep, no dropped points,
SNR approximately21.5,13.6,15.4,8.0, and source-plane diameter threshold
.3arcsec. The finder used preliminary SIE information when choosing/checking
the association. Its threshold is conditional source-association information,
not four independent Gaussian astrometric errors. Pixel-scale rounding and
SNR do not supply a native positional covariance.

The final released SIE+shear maps the markers to a source diameter
.08868239arcsec; the preliminary Sersic-stage SIE gives.21066920arcsec.
Both pass the documented.3gate. The final analytic SIE+shear matches every
released102x102deflection vector to numerical precision. Its exact critical-
curve area gives effective radius2.44927079arcsec, versus released posterior
median2.44932531arcsec. Their small difference is consistent with comparing
point/MAP and median summaries.

The CSV PyAutoLens SIE radius2.51196251 and COOLEST radius2.45188493 use
different profile normalizations; neither should silently replace the area
radius. COOLEST angles convert to west→north angles by pi/2+phi. The light
point model has center(.09204773,-.02768958), q=.66709582,
n=7.14873235, geometric-mean Re=3.59311869arcsec and PA≈1.33361rad.
The supplied field-table coordinates are checked against the markers exactly
to the stated float tolerance. No FOR-specific polar map is reused.

## Capacity equation and convex check

For fixed unreduced deflection vectors a_i at marker positions theta_i,

    b_i = (1-kappa)theta_i - beta*a_i - Gamma theta_i,
    Gamma = [[g1,g2],[g2,-g1]].

At kappa=0, unknown source center cancels from each pair:

    b_i-b_j = Delta theta - beta*Delta a
               - g1*(Delta X,-Delta N) - g2*(Delta N,Delta X).

The objective max_(i<j)||b_i-b_j|| is convex in beta,g1,g2. The scan minimizes
it over0<=beta<=betaMax and sqrt(g1²+g2²)<=gammaMax, with gammaMax fixtures
0,.1,.2,.3. Geometry fixtures use betaMax=.882437110426175 in the adopted
flat matter+Lambda background and the more conservative beta<=1 bound.
Both permit limiting endpoints to produce optimistic closed-set capacities;
physical finite source redshifts require0<beta<beta_infinity.

SLSQP uses an epigraph formulation and analytic derivatives from two starts.
Independent supporting-plane dual bounds check global objective values. For
unit pair vectorsu_k and nonnegative weightslambda_k summing to1,

    D >= c-betaMax*max(h,0)-gammaMax*||s||,
    c=sum lambda_k u_k.Delta theta_k,
    h=sum lambda_k u_k.Delta a_k,
    s=sum lambda_k [u_k.h1_k,u_k.h2_k].

Any such coefficients give a lower bound, regardless of optimizer convergence.
The bounded scan asserts primal/dual gaps below2e-6arcsec and two-start
agreement below1e-6arcsec. For the main gamma=.2/.3 fixtures gaps are below
6e-8arcsec. These are numerical finite-array checks, not absolute PDE bounds.

## Independent unrestricted-shear witness

Centering the markers and projecting perpendicular to the two shear columns
gives vectorsy_perp,a_perp. Minimizing
||y_perp-beta*a_perp||² over the allowed beta interval gives a one-dimensional
necessary condition. For four sources,

    sum_i ||b_i-mean(b)||² = (1/4)sum_(i<j)||b_i-b_j||²,
    D² >= (2/3)sum_i ||b_i-mean(b)||².

A stronger stored witness uses vectorsw_i that annihilate both source offsets
and both shear components exactly. For N=4,

    N sum_i w_i.b_i = sum_(i<j)(w_i-w_j).(b_i-b_j),
    D >= N*min_beta|c-beta*h| / sum_(i<j)||w_i-w_j||.

The null basis is constructed with exact rational arithmetic from the released
.05arcsec marker coordinates. Numerical coefficients select a useful witness,
then are converted to exact rationals. Its field values are the exact binary
numbers in the stored table; outward square-root rounding and a downward
rounded final ratio give conservative finite-array lower values. This
certificate eliminates **unrestricted constant shear**, not arbitrary
spatially varying environmental deflection.

At nearest nominal grid mass11.925, the unrestricted-shear diameter lower
bounds are1.547–1.641arcsec for the horizon cap and1.228–1.334arcsec for
beta<=1 across the three inclinations. Even at logM12.05, the conservative
beta<=1 lower bounds are.594–.712arcsec. All exceed the.3association gate.

## Finite mass scan and environment fixture

For gammaMax=.3, all lower sampled masses are numerically infeasible up to
the failing endpoint of each following bracket:

| Inclination | Horizon-cap fail/pass logM bracket | beta<=1 fail/pass bracket |
|---:|---:|---:|
|90|12.175 /12.200|12.100 /12.125|
|60|12.175 /12.200|12.100 /12.125|
|50|12.175 /12.200|12.125 /12.150|

The linear-alpha interpolation crossings are approximately12.18,12.19,12.20
for the horizon cap and12.11,12.12,12.13 for beta<=1. They are crossings of
the finite interpolation, not rigorously certified continuum mass floors.
Root's separately recorded direct fields give diameters.30024–.30115arcsec
at those interpolated roots, just above.3; reporting many mass decimals would
overstate accuracy. No zero-shear fixture passes at any tested mass from11.7to12.55.

At nominal corrected SED total mass11.9268788861, linearly interpolating the
neighboring fields and allowing nonnegative constant kappa instead gives:

| Inclination | Minimum-kappa horizon fixture | Minimum-kappa beta<=1 fixture |
|---:|---:|---:|
|90|.3294|.2492|
|60|.3390|.2601|
|50|.3533|.2763|

Convex primal/dual gaps for these fixtures are below8e-12. Independent exact
unrestricted-shear witnesses give slightly weaker kappa lower bounds. These
are conditional requirements/infima, not measured environment convergence.
The optimum saturates the geometry cap; finite actual source redshift would
generally require more convergence. The nominal field interpolation is not a
separate exact nominal-mass solve; root's direct nominal inc90 check gives
diameter1.764625(horizon) or1.404730(beta<=1), confirming the large zero-
convergence discrepancy.

The mass-sheet transformation beta'=lambda beta, Gamma'=lambda Gamma,
kappa'=1-lambda+lambda kappa, b'=lambda b shows why unknown convergence can
change a fixed angular source-size gate. No source-redshift measurement or
independent environmental constraint is manufactured by optimizing beta.

## Physical limits and reuse

These results concern fixed smooth oblate profiles, their supplied numerical
fields and inclinations90,60,50, the adopted source association, and constant
external shear/convergence. Shape, M/L gradients, additional baryons, stellar
population assumptions, nonuniform neighboring deflections and absolute
PDE errors are separate obligations. The source gate is not an image fit.
The pipeline association itself is not certified as physical truth. There is
no calibrated significance or full screened-v3s exclusion in this artifact.

`formal/README.md` states exactly what the machine-checked finite-array result
adds. The frozen capacity contract records all consumed fields and released
control inputs. Root's direct-field and combined analyses have their own
records; they do not overwrite the bounded scan here.
