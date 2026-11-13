# Source-redshift-free spherical bounds: interpretation hold

**Do not use this run's comparisons with ECLIPSE mass as a physical tension
or exclusion.** The numerical run treated that mass as the infinite total
stellar normalization. A subsequent primary-source audit established that
the SED flux is summed within the modelling circle. The matching aperture
fraction and extrapolation must be reconciled first. See
`interpretation_status.json`. Frozen `run_01` outputs preserve the original
conditional calculation and provenance; their mass-offset/error-unit/tail
columns are not currently admissible physical comparisons.

The mathematical total-mass bounds remain useful and independent of that
catalog interpretation. Work on corrected scenarios is deferred until the
mass definition is reconciled. The higher-priority FOR posterior transport
is reviewed in `for_aperture_prior_audit.md`.

## Exact conditional envelope

For an isolated spherical positive density with finite total baryonic mass M,
M3D(<r)<=M. The simple-mu force

    g(n,a) = [n+sqrt(n²+4an)]/2

is increasing in n>=0 at a>=0. Therefore the positive LOS integral is bounded
by the force of a point mass M at every ray impact R>0:

    alpha_hat(R) <= alpha_point(M,R,a0).

This argument assumes spherical isolated AQUAL and lensing=dynamics. It is
not a bound for arbitrary oblate/clumpy fields or external convergence.
For an effective Einstein radius from an elliptical model, replacing its
critical curve by the spherical equation theta=beta*alpha_hat is another
explicit model restriction.

With y=GM/(a0 R²), the exact point-mass deflection is

    alpha_point = [4GM/(c²R)] B(y),
    B(y) = .5 [1+sqrt(1+4/y) E(y/(y+4))],
    E(m) = integral_0^(pi/2) sqrt(1-m sin²t) dt.

The E argument is its parameter, as used by SciPy, rather than its modulus.
The formula follows by inserting the exact force into the LOS integral with
r=R sec(t). It tends to4GM/(c²R) at high y and2pi sqrt(GMa0)/c² at low y.
Adaptive quadrature checks span y=1e-10 through1e10 and agree with the elliptic
formula within1e-9 relative; the Newton and deep limits are checked separately.

A weaker closed upper bound follows from

    g(n,a) <= n+sqrt(an),
    alpha_point <= 4GM/(c²R)+2pi sqrt(GMa0)/c² = A M+B sqrt(M).

For positive betaMax, any spherical Einstein solution must satisfy

    M >= [(sqrt(B²+4A theta/betaMax)-B)/(2A)]².

The exact elliptic point-mass root is sharper than this algebraic necessary
floor. Both apply to **total** baryonic mass, not an unidentified photometric
aperture mass.

## Geometry and finite-source feasibility

In a single-plane flat FLRW geometry,

    beta=Dls/Ds=1-chi_l/chi_s < 1,
    beta_infinity=1-chi_l/chi_infinity.

For the adopted flat matter+Lambda background (H0=67.74,Omega_m=.3089),

    chi(z)=(c/H0) integral_(1/sqrt(1+z))^1
                         2 dt/sqrt(Omega_m+(1-Omega_m)t^6).

The infinity integral is finite. Radiation is omitted; the numerical horizon
is14454.36Mpc in this stated background. Since beta is monotone in source z,
required beta=theta/alpha_hat has one finite admissible source z only when
0<required beta<beta_infinity. Equality with the limiting cap would require
infinite source redshift, not a finite observed galaxy. The computed mass
floor is therefore an infimum over finite source redshifts.

For L015780, zl=.428270374 andtheta=2.449325arcsec give beta_infinity=.882437.
The exact point-mass **total** mass floor is log10(M/Msun)=11.862213;
using only beta<=1 gives11.793952. Finite source redshifts1,2,4,10 instead
give floors12.158765,12.000601,11.936261,11.899120. These are mathematical
fixtures, not a comparison with a reconciled observed total stellar mass.

| Target | Exact point-mass total-mass floor at source infinity | Spherical Sérsic floor using catalog radius as spherical scale |
|---|---:|---:|
|L001368|11.54195|12.01165|
|L002239|12.03194|12.16327|
|L000216|11.87200|12.35382|
|L015780|11.86221|12.22256|
|L018096|11.40846|11.70914|
|FOR/L014994|11.62378|11.84773|

Masses are log10(M/Msun), at canonical a0. The exact Sérsic diagnostic also
provides the larger major-axis-radius spherical convention. These spherical
fixtures do not reproduce the observed oblate projected density. L001368
lacks an ECLIPSE mass; L002239 is flagged as a multiple-galaxy lens and
L000216/L018096 lack model consensus. The calculations do not override those
data-quality limitations.

The frozen file's conditional mass tails assume independent reconstructed
geometry-summary errors, fixed stellar IMF/SPS and a two-half-normal mass
surrogate; those were never theory p-values. They are additionally on hold
because the aperture/total distinction was unresolved. Illustrative DESI
mass conversions are also not a matched deblended SED measurement. Official
[DESI documentation](https://data.desi.lbl.gov/doc/releases/dr1/vac/strong-lensing/)
states its mass convention is h=1 with a Chabrier IMF; the usual flux scaling
adds -2log10(h), while the+.2/.25dex IMF shifts in this run are assumptions.

At fixed redshift/SED shape, flux-based stellar mass scales as luminosity
distance squared, whereas angular physical radii scale as angular diameter
distance. Thus at fixed angular profile and fixed a0, gN is invariant under
an H0 rescaling when mass is rescaled consistently; alpha_hat still scales
as distance. Geometry beta is independent of H0. There is a partial
cancellation, not complete H0 independence of the stellar-versus-lens test.
Optional photo-to-spec flux rescalings require actual SED input-redshift
provenance and do not rerun K corrections or stellar-population inference.

## Reproduction and formal scope

`run_01` is a completed bounded v2 run and its manifest validates against
the declared inputs. It contains `result.json`, `summary.csv`, captured logs
and provenance. Contract: `contract.json`; script: `bounds.py`. The exact
Sérsic LOS/Abel ladder differs by less than2e-7 relative in the named checks.

`formal/PointEnvelope.lean` compiles with standard logical axioms only. It
certifies scalar-force monotonicity, the Newton-plus-deep upper envelope,
preservation of the enclosed-mass inequality by any nonnegative finite
quadrature, and the algebraic necessary mass root given stated geometry and
deflection-capacity hypotheses. It does not certify the continuous LOS
integral, FLRW cosmology, numerical quadrature error, catalog mass definition,
or any physical exclusion. No novelty or breakthrough claim is made.
