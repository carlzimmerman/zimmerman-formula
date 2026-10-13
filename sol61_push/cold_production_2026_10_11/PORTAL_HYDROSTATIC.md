# Finite self-gravitating spheres from the nonlinear portal pressure

Status: hydrostatic equilibria and a restricted radial energy test in a
coherent, pressure-only Newtonian fluid. These are not full reacting-field
solutions, dynamically formed halos, or proven stable configurations.
They test whether the new interaction can actually balance gravity in a
finite object rather than only having a positive local sound speed.

## Retained equilibrium model

Take the softened interaction from NONLINEAR_PORTAL.md with the same
chosen parameters. Omit kinetic velocity-dispersion stress, quantum gradient
stress, baryons, cosmological vacuum acceleration and source/daughter
reactions. Use its coherent NR equation of state as an isolated fluid:

    x=rho/rho_0,  rho_0=1e-21 kg/m^3,
    H_0=c^2 A_*/(2m^2)=1.131370850e11 m^2/s^2,
    P=rho_0 H_0 [1-1/sqrt(1+x^2)],
    u=rho_0 H_0 [sqrt(1+x^2)-1].

Here u is the interaction energy density, excluding the linear rest energy.
The sound speed is dP/d rho=H_0 x/(1+x^2)^(3/2). Integrating dP/rho gives
an enthalpy per mass that vanishes at zero density,

    h=H_0 x/sqrt(1+x^2).

Its finite upper limit does not prove stability. It makes a useful variable
for solving hydrostatic equilibrium.

Set y=h/H_0, a=sqrt(H_0/(4 pi G rho_0)), xi=r/a, and
M(r)=4 pi rho_0 a^3 mu(xi). Then

    dy/dxi=-mu/xi^2,
    dmu/dxi=xi^2 y/sqrt(1-y^2),
    y(0)=x_c/sqrt(1+x_c^2),  mu(0)=0.

The surface is the first y=0. The regular central expansion initializes
y=y_c-x_c xi^2/6 and mu=x_c xi^3/3. The adopted a is 11.90266 kpc.
At low density the equation reduces to the n=1 polytrope,
y proportional to sin(xi)/xi, giving surface xi approximately pi.
The computed low-density radius agrees with that analytic limit.

## Equilibria with one common equation of state

| Central rho/rho_0 | Radius, kpc | Mass, solar masses | Surface circular speed, km/s |
|---|---:|---:|---:|
| 0.01 | 37.393 | 9.835e9 | 33.63 |
| 0.1 | 37.354 | 9.761e10 | 106.01 |
| 0.3 | 37.058 | 2.761e11 | 179.00 |
| 1 | 35.207 | 5.856e11 | 267.48 |
| 3 | 33.350 | 6.255e11 | 284.02 |
| 10 | 33.193 | 6.147e11 | 282.23 |
| 100 | 33.201 | 6.147e11 | 282.20 |

The quoted speed is sqrt(GM/R) at the surface. It is not a measured flat
rotation speed or evidence that the interior rotation curve is flat.
All scales follow from the previously chosen crossover and pressure
parameters. No baryonic mass appears in this model, so this table cannot
test or establish the requested baryonic V_f^4 relation.

The mass rises and then falls across the sampled family, with small further
changes at large central density. This is a reason to investigate radial
modes. No turning-point stability theorem is assumed here, and the scan
does not locate a precise extremum or count unstable modes.

## A restricted energy test and its limitation

The equilibrium virial identity is

    W+3 integral P dV=0.

It is checked with independent accumulated gravitational and pressure
integrals. For a mass-preserving homologous deformation
rho_lambda(r)=lambda^3 rho(lambda r), the gravitational energy is lambda W
and the interaction energy is lambda^-3 integral u(lambda^3 rho) dV.
The first derivative vanishes by the virial identity. The second derivative
at lambda=1 is

    E''=integral [9 rho (dP/d rho)-12P] dV
       =3 integral (3 Gamma-4)P dV,
    Gamma=(rho/P)(dP/d rho).

A negative value would identify an energy-lowering radial direction in this
retained fluid model. Positive E'' tests only uniform rescaling; other
radial perturbations can still lower the energy. Finite compact support
makes the homologous trial displacement's inertia finite.

The computed E''/|W| is positive for every sampled sphere: approximately
2.00 at x_c=0.01, 1.044 at x_c=1, 0.417 at x_c=3, and 0.393 at x_c=10.
It remains near 0.396 at x_c=100. Consequently this trial does not exhibit
an instability. It must not be read as a stability proof, especially given
the turnover in the equilibrium mass family. A core-localized displacement
can behave differently from a uniform contraction of the entire object.

## Checks and execution history

portal_hydrostatic_v2.py integrates the central-value equations to the
zero-pressure surface. It checks the virial identity, compares the analytic
homology curvature with direct finite differences of the deformed energy,
checks the low-density radius, and refines ODE tolerances from 2e-9 to
2e-11 for three central densities. All 32 checks pass; the v2 manifest
validates provenance. These are numerical consistency checks, not certified
error intervals or a full mode spectrum. The interpretation is self-reviewed.

The first run completed the calculations but failed JSON serialization of
a NumPy boolean. It is preserved as portal_hydrostatic_run. Version 2
converts that diagnostic to a native bool and writes a fresh result; no
physical equation was changed to make the run pass.

## Implication for the cold-energy construction

The nonlinear portal's mean-field pressure can support finite gravitational
equilibria in this reduced model. That advances the earlier local pressure
comparison to an actual boundary-value problem. It still leaves the
central density free, does not select a halo profile, and omits several
stress and reaction channels required by the microscopic carrier.

The next stability test should resolve radial displacements with different
core/envelope behavior, rather than infer stability from positive local
compressibility or this one trial. Production and the full multimode halo
remain separate unresolved tests. The original cold-energy goal remains
active and incomplete.
