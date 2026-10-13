# Averaging the produced density fluctuations does not remove the pressure crossover

Status: an empirical average of the nonlinear interaction pressure and a
conditional frozen-distribution growth screen. This improves on inserting
the mean density into a nonlinear pressure function, but it is not a
derivation of the evolving multimode field's dynamical sound speed.

## Recovering the produced state

portal_intensity.py repeats the fine 24^3, dt=0.005, x=30 classical portal
production run and saves all 13,824 local total intensities. It reproduces
the previous endpoint daughter fraction to the required 1e-12 tolerance.
Normalize the local leading charge density by its spatial mean and call
it Z, so E[Z]=1. The endpoint sample has

    E[Z^2]=1.754347198,
    min Z=0.01143236,   max Z=7.93304219.

These are endpoint values, not the minimum over every evolution stage
reported in PORTAL_PRODUCTION.md. They describe one seeded periodic box,
not an ensemble or a continuum probability law. All three reproduction,
charge and energy checks pass; the saved result includes the intensity
samples and its manifest records their provenance.

## Exact average at fixed intensity shape

Let x=mean rho/rho_0. If the distribution of Z is held fixed while the
mean density changes, the mean interaction pressure is

    Pbar=A_* S_0 E[1-1/sqrt(1+x^2 Z^2)].

Its partial derivative with respect to the mean rest-mass density is

    C_frozen = H_sound x E[Z^2/(1+x^2 Z^2)^(3/2)],
    H_sound=A_* c^2/(2m^2).

This is positive for a nonempty distribution. In general it differs from
the coherent-density expression H_sound x/(1+x^2)^(3/2). At low density,
C_frozen/H_sound approaches x E[Z^2], so bunching increases the response
by the second moment. In the finite sample's high-density limit it tends
to E[1/Z]/x^2; the finite sample does not establish the low-intensity tail
or inverse moment of an infinite-volume ensemble.

For the empirical production sample:

| Mean rho/rho_0 | Frozen response / coherent response |
|---|---:|
| 0.001 | 1.7543 |
| 0.1 | 1.5707 |
| 1 | 0.6864 |
| 10 | 1.5666 |
| 100 | 2.2137 |

The peak moves to x=0.453638 and sqrt(C_frozen)=184.680 km/s. Its height
is lower than the coherent peak, but the response is larger in portions
of the wings. A lower maximum alone therefore does not imply less
integrated suppression during dilution.

As a comparison only, two independent equal-mean complex Gaussian fields
would give a normalized total-intensity density w(Z)=4Z exp(-2Z). Its
response at x=1 is C/H_sound=0.260897, versus 0.242687 for the simulated
sample and 0.353553 for uniform intensity. The produced sample is not
assumed to have this Gaussian distribution.

## Conditional growth comparison

Insert C_frozen as the pressure derivative in exactly the declared
single-fluid linear growth equation and background of PORTAL_COSMOLOGY.md.
Keep the sample shape fixed throughout dilution. The final amplitudes
relative to the same pressureless control are:

| k, Mpc^-1 | Uniform-intensity EOS | Frozen produced-intensity average |
|---|---:|---:|
| 0.1 | 0.99772 | 0.99739 |
| 0.3 | 0.97956 | 0.97669 |
| 1 | 0.78704 | 0.76033 |
| 3 | -0.08645 | -0.09882 |
| 10 | -0.02703 | 0.02474 |

Signs encode Fourier phase, not negative total density. This remains a
model/control amplitude comparison with imposed initial data, not an
observed power spectrum or cosmological exclusion. The frozen sample does
not eliminate the strong pressure effect found in the earlier screen.

## Why this is still not the full stress closure

If the normalized intensity distribution w(Z) evolves with density or
history, the pressure derivative also contains

    A_* S_0 integral [1-1/sqrt(1+x^2 Z^2)]
                         (partial w/partial mean rho) dZ.

That term is absent from the frozen-distribution calculation. Reactions,
streaming, phase correlations, gradients and gravity can change w; the
perturbation response need not be instantaneous or barotropic. Kinetic
stress and its transport add further contributions. The production
simulation supplies an initial sample, not its evolution from z~1e6
through the crossover near z~75.

Accordingly, C_frozen is explicitly a partial constitutive response under
a stated rescaling, not the proven adiabatic sound speed of the actual
produced medium. The result rules out only the simple suggestion that
averaging the existing spatial fluctuations automatically removes the
coherent pressure problem. It does not rule out state evolution changing
that response, nor establish such a change.

## Verification and next implication

portal_averaged_stress.py checks sample normalization and positivity,
compares the analytic partial derivative with finite differences of mean
pressure at seven densities, verifies the dilute second-moment limit,
and refines the interpolated response grid from 301 to 601 points for the
conditional growth calculation. All 15 checks pass; both this manifest
and the intensity-reproduction manifest validate. The calculation and
interpretation are self-reviewed; neither numerical count nor manifest
validation establishes a dynamical closure.

The previous turn found a coherent cosmological growth problem. This turn
uses the actual produced classical intensity sample to test an averaging
loophole and finds that the problem persists under frozen-shape dilution.
The unresolved requirement is an evolving kinetic/correlation response,
or a revised interaction with an explicitly derived environmental or state
dependence. The repo's halo law and full cold-energy construction remain
unproved.
