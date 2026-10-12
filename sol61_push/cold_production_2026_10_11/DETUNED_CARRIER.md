# Detuning the original carrier above halo conversion

## Result and scope

A conditional production candidate survives two separate finite checks: the
original charged carrier can be retuned so that inverse conversion is
kinematically inaccessible to the initial bound population of the chosen
Plummer halo, while vacuum-seeded homogeneous Gaussian production remains
efficient. This uses the original positive-square potential with repulsive
quartic, without the nonlinear four-form pressure portal.

This is not a completed realization of the repository's cold-energy proposal.
The source energy and charge are prescribed; spatial quantum evolution,
late-time survival, cosmological perturbations, halo formation and the vacuum
acceleration relation are unresolved. The calculated endpoint is a transient
charge fraction, not a predicted relic abundance.

## Parameter choice and halo kinematics

Hold the earlier source density at 9.7151061903e6 eV^4, production redshift
1e6 and epsilon=1e-7. Choose u=0.01 and choose m so that the tree-level
threshold elastic cross section per mass is 1 cm^2/g. This is an illustrative
interaction target, not a fit or an observationally validated parameter.

| Quantity | Value |
| --- | ---: |
| Daughter mass m | 193.5248917 eV |
| Source mass M=2m sqrt(1+u^2) | 387.0691354 eV |
| Circular source amplitude A | 5.69403636 eV |
| Cubic coupling g | 6.57738753e-4 eV |
| lambda_min=lambda_rep | 2.88784050e-8 |
| Total quartic | 5.77568101e-8 |
| Vacuum source lifetime | 1.48016122e-3 seconds |

For the chosen initial halo, v_escape(0)=692.820323 km/s. At leading
nonrelativistic order the pair COM momentum obeys p/m <= v_escape/c =
0.002311, below the on-shell threshold p/m=u. The relativistic correction
at this speed is negligible compared with the factor 4.3 margin; it does
not change threshold exclusion. This statement covers the initial bound
population of this halo, not arbitrary halos, unbound particles or subsequent
time-dependent potentials.

With x=(p/(m u))^2, the tree amplitude relative to its threshold value is
(1-2x)/(1-x). Over the stated bound interval x <= 0.0534072, the total
cross section is approximately 0.89034 to 1 times its threshold value,
including the two-body 1/s factor. Thus the threshold cross section is now
representative of this initial halo, unlike the earlier u=0.001 case.

The free initial daughters have P/E=3.33300e-5 and the circular source has
eta=4.99963e-5. These are nonrelativistic but do not meet the earlier stricter
eta<1e-5 benchmark. For unscattered daughters produced at the chosen redshift,
the present speed is 2.99792 m/s. The declared matter+radiation+Lambda
background gives a ballistic comoving distance 0.0331478 Mpc. This is not
a transfer function: scattering, inhomogeneity and source histories remain
outside that calculation.

## Production calculation and numerical failure retained

The first direct covariance integration is preserved in
`detuned_production_run`. It fails its endpoint quadrature comparison; one
run also develops negative occupations. Charge and energy conservation alone
therefore did not validate that calculation. Its early fractions through
x=50 agree closely, but its late endpoints must not be used as continuum
production evidence.

The replacement `detuned_bogoliubov.py` evolves equivalent pure Gaussian
Bogoliubov amplitudes. With mode weight w, write

    C = w alpha beta*, F = w |beta|^2,
    alpha' = -i normal alpha/2 - i pair beta,
    beta'  = +i normal beta/2 + i pair* alpha.

Starting alpha=1, beta=0 implies |alpha|^2-|beta|^2=1. Differentiation gives
C'=-i normal C-i pair(2F+w) and F'=-2 Im(pair* C), recovering the original
covariance equations, including their vacuum term. F is nonnegative by
construction. Source depletion, quartic normal and anomalous terms, and the
same imposed expansion are retained. The source stays homogeneous; this
is not an exact full quantum field calculation.

| Momentum nodes | Band half-width | Relative tolerance | Fraction at x=100 | Fraction at x=200 |
| ---: | ---: | ---: | ---: | ---: |
| 512 | 2 | 1e-10 | 0.997685460902 | 0.999999819316 |
| 1024 | 2 | 1e-10 | 0.997685460902 | 0.999999819316 |
| 1536 | 3 | 1e-10 | 0.997685461094 | 0.999999819326 |
| 1024 | 2 | 1e-11 | 0.997685460906 | 0.999999819322 |

Time is x=m epsilon t/hbar; x=200 is 6.80235e-9 seconds. Expansion is
negligible over this interval. The endpoint fraction is 99.9999819%, but
conversion oscillates, so this precision describes the declared numerical
surrogate and does not imply a comparably precise physical yield. All 27
checks pass. Maximum charge error is below 1.9e-11 and dimensionless
energy/work error below 5.5e-13. Absolute Bogoliubov normalization drift is
below 1.45e-6 despite large occupations; the recorded relative covariance
diagnostic is below 2.2e-10. Resolution and bandwidth agreement support the
finite interval only. Finite momentum grids can recur at longer times.

## Evidence and next discriminating step

- `detuned_carrier.py`, contract and `detuned_carrier_run/results.json`: six
  kinematic/parameter/quadrature checks pass.
- `detuned_production.py`, contract and run: failed preliminary calculation,
  retained without overwriting.
- `detuned_bogoliubov.py`, contract and run: refined finite production result,
  27 checks pass.
- Both successful run manifests validate against their current inputs and
  outputs. Manifest validation establishes provenance, not physical truth.

The next load-bearing test is spatial production and survival with these
parameters: moving source modes and non-Gaussian rescattering were excluded
from the Gaussian closure. The earlier spatial runs used different masses
and detuning and cannot establish this candidate's yield. Even a successful
spatial test would leave the origin of the charged source, abundance and
V_f^4=G M_b a0 with a0=(1/2)c sqrt(G rho_DE) to be derived.

Follow-up: [DETUNED_MOVING_RESPONSE.md](DETUNED_MOVING_RESPONSE.md) shows
why homogeneous conversion cannot yet be promoted to spatial survival: a
continuum forced-source response occupies momenta absent from the earlier
small spatial boxes. Its auxiliary shell result is not a nonlinear yield.
