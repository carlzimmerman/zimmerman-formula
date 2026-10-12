# Orbital residence of the newly formed source population

Status: orbital averaging in the fixed Plummer potential preserves the
central concentration of source births. It modestly reduces their RMS radius
and increases their velocity dispersion. This is a dilute-tracer residence
calculation, not irreversible settling or an evolved self-consistent halo.

## From the reaction kernel to an orbit population

Use the initial source-birth kernel from BOUND_HALO_REACTIONS.md. At each
birth radius x=r/b, integrate over source speed q=vchi/(u c) and the allowed
parent energies. The source momentum direction is isotropic because the
parent distribution is isotropic. A Gauss integral over mu, the cosine of
the source velocity's angle to the local radius, supplies angular momenta.

In units of b for radius and sqrt(G Mh/b) for speed, each source has

    E = v^2/2 - 1/sqrt(1+x^2),
    L^2 = x^2 v^2 (1-mu^2),
    vr^2(r) = 2[E+1/sqrt(1+r^2)]-L^2/r^2.

The positive turning points rp and ra bracket the birth radius. The binding
bound from the reaction requires E<-1/(2 esc0), and ra never exceeds the
previous active-region radius 5.24626 b. Numerical roots check this support
for every quadrature orbit.

The source-birth weights include the same radial density, phase-space
measure and parent occupation product as the prior initial-rate integral.
They reproduce its fraction born inside b. No radial density profile is
imposed on the subsequent source tracers.

## Residence weighting

For a bound orbit the radial residence measure is dr/|vr|. The radial period
is twice its integral from rp to ra. The fraction of time spent inside R is

    integral_(rp)^min(R,ra) dr/|vr| / integral_(rp)^ra dr/|vr|,

with values zero or one when R lies outside the radial interval. The change
r=rp+(ra-rp)sin^2(theta) removes the leading endpoint square-root singularities.
Gauss quadrature in theta computes residence moments and radial periods.

Averaging this measure over source births is a formal orbital-phase average.
It does not say that a continuously produced population reaches this profile
after one mean radial period. Individual energies and angular momenta remain
unchanged in the assumed fixed potential.

## Results for the chosen test halo

The halo scale is b=30.0267 kpc. The finest calculation uses 27,648 weighted
birth orbits, with 64-point quadrature along each radial interval.

| Quantity | At birth | Orbital residence average |
|---|---:|---:|
| Fraction inside b | 0.90581 | 0.92549 |
| RMS radius / b | 0.66613 | 0.63370 |
| One-dimensional velocity dispersion | 118.73 km/s | 125.25 km/s |

Thus the RMS radius decreases by about 4.87 percent, while the velocity
second moment rises. This is consistent with sources spending more time
deeper in the potential and converting orbital potential energy to kinetic
energy. It is not loss of total orbital energy or a cooling prescription.
The birth-weighted mean radial period is 264.90 Myr.

The fraction inside b is particularly well tested because the birth-radius
quadrature is explicitly split there. Raw output also contains CDF values
at other cuts, but their *birth* fractions use unsplit indicator quadrature
and show larger differences, especially at r/b=0.25. They should not be
read as equally converged measurements. Smooth RMS and velocity moments
avoid that discontinuous-integrand issue.

## Verification and scope

The 8192-orbit calculation gives residence fraction 0.925477 inside b; the
27,648-orbit calculation gives 0.925495. Increasing the radial-orbit
quadrature from 32 to 64 changes that last fraction by less than 1e-12.
This is a finite refinement comparison, not a certified continuum error.

The orbital virial identity

    <v^2> = <r^2/(1+r^2)^(3/2)>

provides a check independent of the density CDF. In the finest run the
birth-weighted absolute residual is below 2.1e-12; the largest individual
residual is below 2.5e-8. Turning-point residuals are below 6.5e-10 in the
dimensionless radial-speed-squared equation. All 28 checks pass, including
birth-kernel normalization against the prior independent rate integral.
`source_orbits.py` and `source_orbits_run/manifest.json` preserve the run;
the manifest validates. Evidence is self-reviewed.

The calculation treats sources as tracers. Their later decays, stimulated
reaction losses, continued injection, daughter depletion and changing gravity
are omitted. It therefore establishes the direction of orbital redistribution
for the initial source population, not the final mixed-species density or a
stable core. In particular the chosen microscopic rates need not leave the
central bath unchanged over several radial periods.

The Plummer potential remains an input, and no baryonic mass or vacuum-density
selector has appeared. The repo's final halo and acceleration relation are
still unproved; this result supplies one orbit-resolved ingredient for a
future self-consistent evolution.
