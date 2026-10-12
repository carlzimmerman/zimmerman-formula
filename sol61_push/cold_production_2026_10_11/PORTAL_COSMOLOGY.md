# The nonlinear portal has a cosmological pressure crossover

Status: a controlled single-fluid linear-growth screen, not a Boltzmann
cosmology calculation or observational exclusion. With the same parameters
used for halo support, the coherent pressure law strongly affects growth
as the cosmic mean density passes through its crossover. Dense-source
coldness does not by itself establish successful structure formation.

## Declared background and connection to production

Use the inherited source density at the imposed redshift z=1e6 and dilute
its leading conserved rest mass as a^-3. This yields

    rho_m,0=2.254009940e-27 kg/m^3.

This amount remains an input inherited from preparation, not a derived
cosmic abundance. Treat the entire matter density as one coherent
barotropic fluid for this screen. Declare homogeneous radiation mass-
equivalent density rho_r,0=8e-31 kg/m^3 and vacuum mass density
rho_Lambda=6e-27 kg/m^3. These are illustrative inputs, not a parameter fit.

The background is

    H^2=(8 pi G/3)(rho_m,0 a^-3+rho_r,0 a^-4+rho_Lambda).

The interaction energy changes the material rest energy by at most
H_sound/c^2=1.25882e-6, where H_sound=A_* c^2/(2m^2). That small correction
is omitted from this declared background. Omitting it from background
expansion does not justify omitting its pressure-gradient force.

With x=rho_m/(1e-21 kg/m^3), the same EOS gives

    c_s^2=H_sound x/(1+x^2)^(3/2).

The mean density reaches x=1 at z=75.2690. The sound-speed maximum occurs
at x=1/sqrt(2), or z=66.9480, with c_s=208.678 km/s. The coupling is a
function of local field density, so an expanding homogeneous fluid crosses
this region too; the action does not restrict its pressure to bound halos.

## A controlled growth comparison

For the subhorizon Newtonian one-fluid approximation, combine linear
continuity, Euler and Poisson equations. For comoving wavenumber k and
prime denoting d/d ln a,

    D''+[2+d ln H/d ln a]D'
       +[c_s^2 k^2/(a^2 H^2)-4 pi G rho_m/H^2]D=0.

Radiation and vacuum enter the background only. Radiation perturbations,
baryonic perturbations, source/daughter reactions, quantum gradient stress
and incoherent kinetic stress are absent. The coherent EOS has not been
derived as a closure for the actual produced multimode field.

Start at a_i=0.001 with D=1 and D'=1, shared by the pressure and pressureless
runs. This is an imposed growing-like initial condition, not a prediction
from production or a complete radiation-era adiabatic mode. D is a growth
factor: its overall perturbation normalization can be chosen infinitesimal
so the comparison remains linear. A negative D indicates a Fourier phase
reversal, not a negative physical background density.

| k, Mpc^-1 | Comoving wavelength, Mpc | D_portal(1)/D_pressureless(1) | Squared ratio |
|---|---:|---:|---:|
| 0.1 | 62.83 | 0.99772 | 0.99544 |
| 0.3 | 20.94 | 0.97956 | 0.95953 |
| 1 | 6.283 | 0.78704 | 0.61942 |
| 3 | 2.094 | -0.08645 | 0.007474 |
| 10 | 0.6283 | -0.02703 | 0.0007307 |

These are model-to-control ratios for the stipulated initial data. The
squared ratio is not a measured matter power spectrum or a likelihood.
Its strong scale dependence is nevertheless a concrete problem for treating
this coherent interaction as an innocuous halo-only pressure source.

Two independent characteristic scales help explain the behavior:

    k_J(a)=a sqrt(4 pi G rho_m/c_s^2),
    r_sound=integral c_s/(a H) d ln a.

The minimum comoving Jeans wavenumber over the calculation is
1.63887 Mpc^-1 near z=60.8971. The comoving sound distance from a_i to
a=1 is 1.254585 Mpc. Integrating the same sound law from a=1e-6 to a_i
adds only 3.20e-5 Mpc; this latter integral is a background travel-distance
check, not a perturbation evolution outside the subhorizon regime.
An instantaneous Jeans criterion is not a transfer function: accumulated
pressure also changes modes that never exceed that instantaneous threshold.

## Verification and limits

portal_cosmology.py compares ODE tolerances 2e-9 and 2e-11 for each mode,
checks that k=0 removes the pressure term, verifies the analytic sound-speed
peak, and reproduces the Einstein-de Sitter pressureless growing solution
D proportional to a in an independent control. All eight checks pass;
the manifest validates provenance. The derivation and interpretation are
self-reviewed. No external observational bound is asserted.

The computed pressureless growth is 671.9684 for the declared background
and initial data. It is only the common control, not a replacement for a
standard cosmological transfer function. A full comparison would require
radiation and baryon perturbations, appropriate initial modes and the
actual produced field's stress response.

## Decision for the cold-energy route

The last turn established dense spatial conversion compatible with this
interaction. This turn shows why that result and a static pressure-supported
halo cannot simply be joined into a successful cosmological history: the
intermediate density regime can suppress growth before halo formation.

The current coherent, all-matter implementation therefore needs more than
a halo equilibrium or radial stability calculation. Possible changes must
come from the actual field state or a specified dynamical interaction;
turning pressure on only in halos by fiat would insert missing physics.
In particular, the produced field is multimode, and its coarse-grained
response to the nonlinear U(S) should be derived before accepting or
rejecting the full model using this coherent screen. No stable halo
selection, baryonic scaling, vacuum-flux origin or complete cold-energy
construction is established.
