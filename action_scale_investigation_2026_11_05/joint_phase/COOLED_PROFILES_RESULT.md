# Solved cooled profiles and a conditional radial stability test

2026-11-06. Base49261f61f1fab308591dc8c50bf5ccc8abdded98.
Contracts578eda5417 and a9e2b1caf3. Continues RADIATIVE_EXPORT_RESULT.md.

**Outcome:** the coupled temperature, density, flow and gravitational profiles
have now been solved numerically for an explicitly confined fluid model with
excitation-line cooling. All reported sampled equilibria have damped modes in
the discretized radial linear-stability problem, including perturbed gravity;
selected modes and profiles converge under grid refinement. This is substantive
progress beyond a local thermostat calculation.

It is NOT a self-confined galaxy solution: the outer radius is prescribed and
its reflecting wall supplies whatever stress is required. Most sampled circular
speed curves rise; the strongest-gravity example flattens only toward its outer
region. The edge-speed normalization changes with boundary radius. No physical
value of a0, and no1/2, has been derived. No parameter was fitted to that target.

## 1. Exact conditional model being solved

The variables are dimensionless. With r_*, n_* and thermal energy theta_* as
reference scales, velocity is in units v_*=sqrt(theta_*/m), time in r_*/v_*,
and the gravity parameter is

    gamma=4pi G m n_* r_*^2/v_*^2.

mu(r)=integral_0^r n(s)s^2 ds is the dimensionless material mass integral, so
material acceleration is gamma mu/r^2. A dimensionless theta near unity does
NOT mean a relativistic temperature; theta_* must be much smaller than mc^2
for the physical interpretation used here. No reference scales have been
assigned galaxy values, and simultaneous microscopic viability has not been
established.

The baseline choices are

    R=3, K=0.001, C=0.001, kappa0=0.2,
    Delta=0.5, e_in=3, c_v=3/2,
    J(r)=0.001 S exp(-r/5)/(1+r^2),
    Lambda(theta)=C Delta/[2sqrt(theta)] exp(-x) K_1(x),
    x=Delta/(2theta),
    F=-kappa0 sqrt(theta) theta'.

K_1 is the modified Bessel function. C absorbs the amplitude of the excitation
cooling derived in the preceding report; it is not calculated from rho_DE.
The source is a prescribed, finite cored version of the mediator-like profile.
S is a source-strength multiplier, not a measured baryonic mass. The coefficients
were specified before the numerical run, not adjusted to obtain a desired speed.

There is no baryonic gravitational component in this experiment. Retained source
particles are assigned zero mean radial injection momentum and kinetic energy
e_in. That is an additional source assumption; the actual outward momentum of
ballistic mediator daughters was not derived to vanish. The source does not
respond to perturbations of the material. Annihilation remains present and its
particle losses are replaced by J; line cooling itself preserves heavy-particle
number. Radiation escapes without absorption or delayed excited-state dynamics.

The equations in RADIATIVE_EXPORT_RESULT.md are used with m scaled out and
Phi'=gamma mu/r^2. Both inertia and the source's momentum-dilution term are
retained. The zero mean injection momentum still contributes -J u/n in the
velocity equation and +u^2/2 in the relative injection energy. Density and
temperature profiles are solved; no inverse-square density profile is imposed.

At the origin, use regularity. At the fixed outer radius impose

    u(R)=0,     F(R)=0.

The material cannot cross the boundary and conduction cannot carry energy
through it, but emitted radiation can leave. This is an ideal reflecting,
thermally insulated material wall. Surface density and pressure are outputs,
not zero; the wall provides the confining stress. Its response is not perturbed.
This condition is deliberately stronger than a naturally selected vacuum phase
boundary and cannot establish that boundary's existence or stability.

## 2. Two spatial discretizations and the stability operator

First solve the five-variable boundary-value problem in log(n),u,log(theta),F,mu
with scipy.integrate.solve_bvp, tolerance2e-7 and at most6000 mesh nodes.
The central radius is epsilon=0.001, with leading regular series conditions

    mu(epsilon)=n(epsilon) epsilon^3/3,
    u(epsilon)=[J/n-Kn] epsilon/3,
    F(epsilon)=[J(e_in-c_p theta)+Kn^2 theta-n^2 Lambda] epsilon/3.

The outer conditions above complete the five boundary conditions. All requested
BVPs converged. The source is finite at the center; no singular1/r^2 source is
inserted there.

Second, use a staggered radial time-dependent discretization extending to r=0.
Density and temperature are at cell centers, velocity at internal faces,
with u=0 at both end faces. Number fluxes use spherical face areas and exact
shell volumes; conduction is a face flux with zero boundary values. Enclosed
mass is recomputed from density on every residual evaluation, so gravitational
perturbations are included rather than frozen. Central spatial differences
approximate velocity and temperature advection and pressure forces.

Solve this discretization's steady residual separately, using the BVP as the
initial guess. Then differentiate its full time-dependent residual in
(log n,log theta,u) by centered finite differences and compute every eigenvalue
of the resulting matrix. A positive real part would mean a growing resolved
radial mode. This is a finite-dimensional linear test, not nonlinear evolution
or a proof about all continuum modes.

The discrete number budget is exact up to numerical roundoff. The primitive
thermal/momentum discretization is NOT exactly conservative in total energy;
its integrated kinetic-energy error is measured and decreases under refinement.
This distinction is material to the interpretation of the results.

## 3. Solved profiles

The main run samples gamma=0,0.5,1,2,4,8 at S=1 and S=0.5,2 at gamma=1.
The follow-up changes R to2 and4, and e_in to6, at gamma=S=1, and refines gamma8.
There are11 distinct parameter configurations and25 successful discrete solves,
including a repeated gamma8,48-cell solve. No claim covers all parameter choices.

Representative finest-grid values, all at R=3 and S=1:

| gamma | cells | density min..max | temperature min..max | largest Re(eigenvalue) |
|---|---:|---|---|---:|
| 1 | 72 | 0.30414..0.48322 | 1.337913..1.338209 | -0.000510033 |
| 2 | 72 | 0.23661..0.68442 | 1.352021..1.352177 | -0.000613779 |
| 8 | 96 | 0.09041..2.29572 | 2.438436..2.441141 | -0.000589734 |

These temperatures are nearly, but not exactly, constant. The small gradients
carry the conductive flux needed to match the spatially varying source,
compression and radiation. The density has a resolved finite core rather than
an imposed cusp. The source, annihilation and flow balance point by point.
The gamma1 case has slow outward redistribution; gamma8 has inward flow.
In the latter, the resolved mean velocity ranges from approximately-0.0004834
to-0.00000817, approaching zero at the actual faces. All reported flows are
very subsonic, with maximum sampled Mach number below0.001.

The radiation integral is positive while material flux at the outer wall is
zero. Thus this model does export heat radiatively without evaporating its
material inventory. Existing annihilation still destroys individual particles;
source replacement keeps the steady inventory, not the identities of particles.

[Profile and stability figure](cooled_profiles.png) and
[standalone PDF](cooled_profiles.pdf) are generated from the preserved results
by plot_cooled_profiles.py. The curves use dimensionless variables and are not
fits to observations.

## 4. What the stability evidence supports

Every reported discrete equilibrium has largest Re(eigenvalue)<0. The slowest
modes in the representative cases are real, damped reaction/thermal modes;
resolved oscillatory modes are also damped. This tests coupled radial density,
velocity, temperature and self-gravity perturbations with the prescribed wall
and fixed source, rather than merely the earlier two-variable local thermostat.

Refinement of the slowest mode gives

| gamma | N=24 | N=48 | N=72 | N=96 |
|---|---:|---:|---:|---:|
| 1 | -0.000510287 | -0.000510073 | -0.000510033 | — |
| 2 | -0.000614695 | -0.000613922 | -0.000613779 | — |
| 8 | — | -0.000589870 | -0.000589769 | -0.000589734 |

For gamma1,N48, halving the Jacobian step from2e-6 to1e-6 changes the leading
real part by1.7e-10, much smaller than its distance from zero. The gamma1
maximum log-density difference from the BVP decreases from5.97e-4 at24 cells
to6.64e-5 at72 cells. For gamma8 it decreases to3.57e-4 at96 cells; its maximum
log-temperature difference is2.12e-4. The second discretization thus approaches
the independently solved steady BVP profiles.

Steady residuals are below1e-7 (typically1e-13). Source and annihilation number
integrals agree to roundoff or solve tolerance, and an arbitrary small test
perturbation preserves the discrete global number identity.
The measured integrated kinetic-energy balance is

    injection + gravitational work - annihilation energy - radiation = 0

up to spatial truncation error. In the strongest-gravity case, the relative
error decreases from2.53e-4 to1.12e-4 to6.32e-5 at48,72,96 cells. Errors for the
other refined follow-up cases are below6e-6 at72 cells. Including gravitational
work matters: inward material can radiate more than its net injected kinetic
energy after annihilation losses.

A deliberately incorrect control retains a converged cooled profile but omits
radiative cooling from its evolution residual. The stationarity check fails,
while the ordinary residual and particle-budget checks pass. This establishes
that cooling is load-bearing in these solutions, not an unused term.

The safe stability statement is numerical evidence for linear radial stability
of these confined fluid equilibria with the stated closures. Nonspherical modes,
nonlinear disturbances, moving-boundary modes, kinetic escape, radiation-opacity
perturbations, source feedback and full microscopic feasibility are untested.
It is not a theorem of unconditional global stability for real galaxies.

## 5. Rotation curves and normalization

The circular speed is computed from the solved enclosed mass:

    v_c^2(r)=gamma mu(r)/r.

Most examples are not flat. At r=0.8R, the logarithmic speed slope is about0.88
for gamma1,S0.5 and0.74 for gamma1,S2. The gamma8 example has slope0.1003 there
and becomes flatter toward the edge, but it is not an extended universal flat
family. There is no observational rotation-curve fit.

For a normalization comparison use the actual boundary speed
v_edge^2=gamma mu(R)/R, not the last cell-center speed, and let
S_total=integral_0^R J r^2 dr. With gamma=1 and the other baseline parameters,

| imposed radius | v_edge^4/S_total |
|---|---:|
| 2 | 663.340 |
| 3 | 984.936 |
| 4 | 1291.086 |

These are dimensionless model ratios, NOT measured accelerations. They change
substantially with an unselected boundary even though all three models remain
radially damped in the sampled tests. Doubling injection energy at R=3 changes
temperature from about1.338 to2.909 and gives v_edge^4/S_total=997.242.

There is a simple reason for an approximately fourth-power source scaling in
the weakly concentrated examples. The reflecting boundary enforces

    S_total=K integral_0^R n^2 r^2 dr.

Cauchy-Schwarz gives mu(R)^2 <= (R^3/3) integral n^2 r^2 dr. Define the shape
factor f=3 mu(R)^2/[R^3 integral n^2 r^2 dr], with0<f<=1. Exactly at steady state,

    v_edge^4/S_total=gamma^2 R f/(3K).

For nearly uniform profiles f is near one. At fixed R this can mimic a
v^4-proportional-to-supply relation through annihilation balance, without being
MOND and without yielding an extended flat rotation curve. In the S=0.5,1,2
scan at gamma=1,R=3, v_edge^4/S is1.1980,1.1881,1.1654 respectively. The variation
of f and, especially, the unselected R and K remain in the normalization.

Neither S nor S_total has been derived to be proportional to baryonic mass.
rho_DE is absent from the selected confinement/source parameters. Converting
units cannot supply the missing physical relation. There is therefore no
computed universal acceleration coefficient to identify with1/2; choosing a
radius, source normalization or unit mapping to obtain it would be calibration.

## 6. What has and has not been landed

We now have solved, finite, radiatively cooled, coupled spatial profiles and
convergent numerical evidence of radial damping in a stated model. The previous
pointwise failure of the exactly isothermal flat ansatz is bypassed by solving
nonconstant density and temperature instead of insisting on that ansatz.

The external wall is doing indispensable work: its surface pressure is positive
and no phase-front law derives its radius or response. The deposited source
spectrum/momentum and the joint microscopic rate/opacity hierarchy are still
assumptions. Removing the wall or changing its response requires a different
boundary-value and stability problem. A source/vacuum-selected finite boundary,
a broad flat-curve family and its absolute normalization remain unresolved.

## Reproduction and provenance

cooled_profiles.py and cooled_profiles_followup.py contain the full equations,
solvers, parameters and deterministic grids. The follow-up preserves the first
executed file and uses the same equations with its frozen extensions.
Their corresponding *_computation.json files record assertions, conventions,
software and bounds. Runs use the installed computation-audit runner with
--timeout180 --max-threads1; exact commands and input hashes are in
 evidence/cooled_profiles/manifest.json,
 evidence/cooled_profiles_followup/manifest.json and
 evidence/cooled_profiles_mutate/manifest.json.
The first two runs completed; the negative control intentionally failed one
stationarity check. No executed solver input was edited afterward.

Review provenance: author self-review, not an independent simulation audit.
The equations were checked against the preceding conservative continuum
identities; discrete number conservation, energy truncation error, independent
steady discretizations and eigenvalue/profile refinement were assessed.
Verdict: **computationally verified only in the stated sampled models and
resolutions**, with the physical interpretation conditional on the specified
wall, fluid and radiation assumptions. This checkpoint does not mark the
stable-galaxy/1/2 research objective complete.
