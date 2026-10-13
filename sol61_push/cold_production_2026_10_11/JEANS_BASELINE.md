# Self-gravity baseline for the stipulated kinetic bath

Status: a collisionless Vlasov-Poisson calculation identifies which of the
previous homogeneous bath's scales are gravitationally unstable. It provides
a timescale comparison, not a stability test for a finite equilibrium halo
and not the coupled collision-plus-gravity evolution.

## Explicit background prescription

Use the same illustrative density rho=1e-21 kg/m^3 and one-dimensional
Gaussian velocity dispersion sigma=200 km/s. Source particles initially
vanish. Gravity acts on the density perturbation through

    laplacian Phi = 4 pi G (rho(x)-rho_background).

The mean subtraction is part of this declared homogeneous/periodic Jeans
problem. An infinite uniform, static, isolated gravitating bath is not being
claimed as a physical equilibrium. No expansion, rotation or finite halo
boundary is included.

For a Maxwellian velocity distribution, the critical wavenumber is
kJ=sqrt(4pi G rho)/sigma. The growing-mode dispersion relation agrees with
[Chavanis, arXiv:1002.0291v1, equations 109–112](https://arxiv.org/pdf/1002.0291),
using his inverse temperature beta=1/sigma^2 and x=gamma/(k sigma). That
source also explicitly discusses the homogeneous-background limitation.
No theorem about an inhomogeneous halo is imported from this comparison.

## Independent time-domain calculation

For an initial density perturbation proportional to the background Gaussian
in velocity, integrating the linear Vlasov equation along free trajectories
and inserting Poisson's equation gives

    D(t)=exp[-(k sigma t)^2/2]
         +4pi G rho integral_0^t ds (t-s)
          exp[-(k sigma (t-s))^2/2] D(s).

Here D is the density amplitude divided by its initial amplitude. In units
z=sqrt(4pi G rho)t and a=k/kJ, its kernel is z exp(-a^2 z^2/2).
A growing exponential has dimensionless exponent g satisfying

    1=integral_0^infinity dz z exp(-a^2 z^2/2-g z),
    a^2=1-sqrt(pi) y erfcx(y),  y=g/(sqrt(2)a).

For a<1 there is a positive growth root; for a>1 the kernel's Laplace
transform at zero is 1/a^2<1 and decreases with positive g, so no positive
real growth root exists. At a=1, D(z)=1 exactly solves this initial-value
problem, providing a marginal benchmark. The homogeneous Maxwellian
stability classification is the one checked in the cited primary source;
the scalar positive-root test alone would not classify every possible
complex mode of an arbitrary velocity distribution.

`jeans_baseline.py` solves the dispersion relation, checks it by independent
Laplace-kernel quadrature, and evolves the Volterra equation on 2048 and
4096 time intervals up to z=12. Its growing rates are also measured from
the late-time logarithmic slope. This avoids importing the earlier angular
collision discretization into the gravity benchmark.

## Numerical scale comparison

The characteristic gravitational time is 34.601 Myr and the Jeans wavelength
is 44.468 kpc. Results for the initial stipulated bath are:

| Wavelength | Collisionless homogeneous result | Growth e-folding time |
|---|---|---:|
| 10 kpc | Stable against this Jeans instability | — |
| 50 kpc | Unstable | 201.24 Myr |
| 100 kpc | Unstable | 46.39 Myr |
| 1000 kpc | Unstable | 34.70 Myr |

The earlier fixed-bath source-mode relaxation time, 0.856 Gyr, is respectively
4.26, 18.46 and 24.68 times the three growth times. These compare two
conditional diagnostics; they do not prove that collisions leave the
threshold or eigenvalues unchanged. In particular near the marginal
wavelength the collisionless growth rate becomes small, so collisions need
not remain negligible there.

For the initial source-free example, the previously computed contact-pressure
speed squared is about 9.97e-15 times sigma^2. At a 10-kpc wavelength,
[hbar k/(m sigma)]^2 is about 3.63e-23 for m=1e-12 eV/c^2. These small
parameters support using a kinetic rather than contact-pressure- or
quantum-gradient-supported baseline for these illustrative scales. They do
not establish a condensate fraction or validate random phases.

All 12 checks pass. The largest time-grid difference, normalized by 1+|D|,
is below 1.9e-5. Measured unstable growth exponents agree with the dispersion
roots within 6e-7 in gravitational-time units. The marginal solution check
also passes. Very small stable-mode late amplitudes are not claimed to
have controlled relative accuracy. `jeans_baseline_run/manifest.json`
validates the script, inputs and output. This is self-reviewed evidence.

## Consequence for the route to the repo medium

The no-gravity 1-Mpc comparison in KINETIC_STREAMING.md is not a persistent
halo state at the stipulated density. In this baseline gravity changes such
a bath on a timescale much shorter than its earlier collision-mode response.
Long-time transport must be studied on a gravitationally evolving or bound
background, rather than attaching a local diffusion law to a homogeneous
bath and calling it a halo.

A Jeans wavelength is not a halo radius or a selected density profile.
Linear growth does not establish nonlinear collapse outcomes, a stable halo,
a baryonic scaling relation or the repo's vacuum-dependent acceleration.
A finite distribution in a consistent gravitational potential, with orbital
motion and the collision channel, is the next physical modeling requirement.
The proposed creation mechanism is still distinct from identification of
the full cold-energy medium.
