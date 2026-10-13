# Spatial temperature-mode response: streaming versus collisions

Status: linear Fourier-mode evolution combines spatial streaming with the
same angular collision operator. At the stipulated density and dispersion,
the tested 10-kpc mode evolves close to the collisionless result over its
short dephasing interval. This does not model a bound halo: gravity and
boundaries are absent. It tests whether a local-diffusion assumption is
already supported by the microscopic collision rate.

## Evolution and initial condition

Expand the perturbation at spatial wave number kx as

    delta f = A exp(i kx x) sum_l (-i)^l h_phi,l(e,tau) P_l(mu),

and likewise for the source. This convention makes the amplitudes h real
for the chosen initial cosine perturbation. Define q=kx u c t_unit, with
t_unit=0.278436678 Gyr from COUPLED_KINETICS.md. Streaming obeys

    dh_l/dtau = q v [l h_(l-1)/(2l-1)
                     -(l+1) h_(l+1)/(2l+3)] + C_l.

Dimensionless speeds are sqrt(2e) for daughters and sqrt(ec-1) for sources.
The collision operator C_l is the linearization around the evolving
isotropic bath. The l=1 triangle factors in KINETIC_HEAT_CURRENT.md become
P_l(c12), P_l(c1), P_l(c2) for general l, by azimuthal averaging. The
isotropic bath itself still evolves by the nonlinear collision operator.

Initially only daughter h_0 is nonzero:

    h_0(e)=a(e) [e/r^2-C],
    r = sigma/(u c),
    C = sum wp a e / [r^2 sum wp a].

This is the finite-grid analogue of a temperature perturbation at fixed
number density. C ensures exactly zero initial charge-density perturbation
on this grid. Sources initially vanish. The finite perturbation amplitude
is infinitesimal; these equations are not nonlinear spatial evolution.

The l=0 moments satisfy the Fourier continuity equations

    delta Q' + q P1/3 = 0,
    delta Eexcess' + q J1/3 = 0,

where P1 and J1 are the leading-order momentum and excess-energy current
moments from the preceding dipole calculation. These are checked directly
on the full streaming-plus-collision RHS, not inferred from background
conservation alone.

## Collisionless benchmark

With collisions disabled, each energy shell's angular average is exactly
j0(q v tau). The discrete energy contrast is therefore an independently
computable weighted spherical-Bessel sum. A 24-multipole evolution matches
that benchmark to better than 2.2e-12 in initial-amplitude units over the
tested interval. Spatial dephasing in this control is reversible streaming,
not collisional thermalization or demonstrated diffusion.

## Scale comparison

Keep the existing illustrative daughter density 1e-21 kg/m^3 and initial
one-dimensional dispersion 200 km/s. Use 64 daughter energy bins up to e=8,
and compare angular truncations lmax=12 and 24. Stop each case at
kx sigma t=3, so the physical durations differ with wavelength.

| Wavelength | Duration | Largest collisional change from free streaming, in initial energy-amplitude units | Final energy contrast, collisions | Final free-streaming contrast |
|---|---:|---:|---:|---:|
| 10 kpc | 0.023343 Gyr | 0.005908 | 0.038234 | 0.042581 |
| 1000 kpc | 2.334307 Gyr | 0.151961 | -0.036552 | 0.042581 |

The 0.005908 value is 0.59 percent of the **initial** energy perturbation,
not a fractional error relative to the much smaller endpoint. A negative
Fourier coefficient means reversal of the perturbation's phase; it does not
mean negative local energy density.

The 1-Mpc run keeps the same homogeneous bath solely to compare streaming
and collision times. It is not asserted to represent a stable astronomical
system at that density. In particular, gravitational stability was not
checked and cannot be inferred from this calculation.

The angular-refinement differences in energy contrast are below 2.8e-7 for
both wavelengths. All 23 checks pass, including integration success,
background charge/energy conservation, Fourier continuity and the independent
free-streaming benchmark. Continuity residuals are below 1.8e-15 in the
script's dimensionless normalization. The energy grid was held at N=64;
there is no new energy-grid convergence result for these spatial runs.
`kinetic_streaming.py` and `kinetic_streaming_run/manifest.json` preserve the
calculation; the manifest validates. Evidence is self-reviewed.

## Research consequence

At these parameters and for the tested perturbation, rapid local collisional
isotropization does not precede spatial motion on the 10-kpc scale. A
near-collisionless orbital treatment is better motivated than simply inserting
a diffusion coefficient obtained from the earlier single-mode response time.
This is a statement about this example, not a no-go result for all densities,
velocities, perturbations or nonlinear states.

A gravitational halo can repeatedly redirect and confine streaming particles;
the no-gravity result cannot be interpreted as halo evaporation or as a halo
thermalization time. The next relevant dynamics must combine gravity, orbital
motion and the collision channel. This analysis still does not select a
universal density profile or connect any acceleration to vacuum density.
