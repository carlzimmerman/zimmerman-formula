# A dynamical phase boundary: selected radii and radial stability

2026-11-06. Base00b8bd7dd535008404c97d49d244466639fdd31b.
Contracts89d5ecb6ea, bf4cfcdae5,3f3461bffd and84f08b2e27.
Continues COOLED_PROFILES_RESULT.md.

**Outcome:** the imposed fixed-radius wall has been replaced, within an explicit
phase-fluid model, by a dynamical interface whose tension and vacuum pressure
balance the material pressure. Radius is now solved, not assigned. With a
higher-energy vacuum inside, some sampled equilibria are numerically stable
against coupled radial fluid, gravitational AND boundary perturbations and
have roughly flat outer circular-speed curves. This is conditional
phase confinement, not an external rigid container.

The full requested theory is still incomplete. The vacuum ordering, tension,
energy difference, particle mass barrier and source are assumptions or free
parameters. Kinetic/nonspherical stability, formation and quantum lifetime are
not established. The source-family test does not produce a universal baryonic
mass-speed relation, and the coefficient1/2 is not derived.

## 1. A physical interface rather than an imposed radius

Use a phase scalar phi with two minima. An explicit illustrative potential is

    V(phi)=V0+(lambda_phi/4)phi^2(phi-v)^2
              +DeltaV[3(phi/v)^2-2(phi/v)^3].

Inside take phi=0; outside phi=v. Thus DeltaV=V_out-V_in is SIGNED. For
|DeltaV|<lambda_phi v^4/12 both vacuum extrema have positive curvature. In the
small-tilt thin-wall limit, the tension is

    Sigma=integral_0^v sqrt(lambda_phi/2) phi(v-phi)dphi
         =sqrt(lambda_phi/2) v^3/6.

This identifies what sets tension in a potential; it does not fix lambda_phi
or v from dark-energy density. Numerical Sigma and DeltaV below are explicit
phenomenological inputs, not a completed microscopic matching calculation.
Material backreaction on the wall profile must be small compared with the
barrier for this constant-tension approximation to hold.

Let heavy particles be lighter inside, for example

    m_chi^2(phi)=m^2+y_chi^2 phi^2.

A similar barrier can be assigned to the short-lived excited heavy state.
Particles below the normal transmission threshold reflect from this phase
interface. Light cooling radiation is assumed to remain effectively massless
and transparent across it. That transparency and the coupling hierarchy are
not automatically guaranteed by the previous interactions.

For a static planar interface, the outgoing normal momentum satisfies
q_normal^2=k_normal^2-(m_out^2-m_in^2). Subthreshold reflection therefore
requires no literal material wall. In the nonrelativistic Maxwell limit define

    B=(m_out^2-m_in^2)/(2m_in).

The outward number leakage is bounded above, even allowing unit transmission
above threshold, by

    F_leak <= n sqrt(theta/(2pi m)) exp(-B/theta).

This integrates the normal velocity distribution, rather than the total-energy
Jeans tail used earlier. A sufficiently large mass barrier gives long retention;
finite B never justifies a claim of exactly zero physical leakage. The numerical
runs use the high-barrier limit. For illustration B/theta>=30 suppresses this
flux by at least exp(-30), but no physical lifetime is inferred without the
actual density, radius and mass parameters.

The general possibility of phase trapping is established research context:
[First-order phase transition and fate of false vacuum remnants]
(https://arxiv.org/abs/2206.09923) discusses thermal and other particle-supported
remnants. Its abstract was checked only for context, not used as a stability
proof for this source-driven, cooled halo. No novelty claim is made for
particle trapping by a vacuum phase boundary.

## 2. Wall force, inertia and energy accounting

With negligible external material pressure, the outward force per area is

    F_wall=P_inside+DeltaV-2Sigma/R.

For DeltaV>0 the interior vacuum is lower energy and vacuum pressure pushes
outward. For DeltaV<0 the interior is higher energy and the vacuum difference
confines inward. These are physically distinct choices, not interchangeable
sign conventions.

The relativistic thin-wall equation supplies inertia Sigma/c^2 per area.
At the nonrelativistic order used in the numerical model,

    I (W_dot+W^2/R)=P_inside+DeltaV-2Sigma/R,
    R_dot=W,                 I=Sigma/c^2.

In the previous dimensionless fluid units, I=Sigma epsilon^2, with
 epsilon^2=(v_scale/c)^2=1e-6 in these runs. No stabilizing wall drag is inserted.
Gas pressure transfers momentum and energy between fluid and wall; radiation
carries cooling energy away. Wall/vacuum contributions to gravity are neglected
at the small relativistic-energy ratios of this illustrative scaling. Physical
units and an absolute cosmological background have not been matched.

Per4pi, the wall-plus-vacuum energy through this order is

    E_wall=Sigma R^2+(I/2)R^2 W^2-DeltaV R^3/3,
    E_wall_dot=P_inside R^2 W.

The W^2/R term is required by this work identity. The numerical and symbolic
checks verify it. This is pressure work, not a new source of radiative energy.
The bulk source must still supply particles/rest energy as before.

A useful restricted stiffness test is P proportional R^-alpha. At equilibrium,

    dF_wall/dR=[DeltaV-(alpha-1)P]/R.

An empty lower-energy bubble has the familiar expanding/collapsing instability;
a sufficiently responsive material pressure can stabilize a branch. This
one-coordinate stiffness is a diagnostic only. Actual stability below is tested
with fluid temperature, density, flow, gravity and wall motion coupled.

## 3. Steady profiles and a moving-boundary stability calculation

Keep the previous dimensionless cooling/source model:

    K=C=0.001, kappa0=0.2, Delta_excitation=0.5, e_in=3,
    J(r)=0.001 S exp(-r/5)/(1+r^2).

The phase energy difference DeltaV is NOT the excitation gap. The zero mean
radial momentum of the deposited source and instantaneous thin-radiation escape
remain assumptions. Baryonic gravity, actual source luminosity and microscopic
rate/opacity matching are still not supplied by the analogy.

For each trial R solve the coupled regular fluid boundary-value problem with
u(R)=0 and zero conductive flux, then evaluate
P(R)+DeltaV-2Sigma/R. A zero selects an equilibrium radius. This procedure uses
a boundary only as a shooting location; the mechanical force condition now
selects that location. Multiple roots are retained.

For stability, introduce a comoving coordinate x=r/R(t). Faces move with grid
velocity x W. The material velocity at the phase wall equals W in the
high-barrier limit. The number equation on moving shells is

    n_dot|x = -div[n(u-xW)]+J-Kn^2-3(W/R)n.

Velocity advection uses u-xW. Temperature advection likewise uses the relative
velocity, but compressional heating uses divergence of the PHYSICAL velocity u.
Poisson mass is recomputed from density and moving shell volumes. The dynamic
unknowns are log n,log theta,internal face velocities,log R and W. The full
radial Jacobian includes the phase force and both extra boundary variables.
No fixed-radius mode is substituted for a moving-wall mode.

The outer-cell pressure is used consistently in wall pressure work and fluid
compression. It is only a first-order boundary-pressure representation. Thus
free-boundary radii converge more slowly than the previous rigid-wall profiles.
We explicitly compare the discrete radii with the separate continuum BVP roots.
The wall work identity and moving-volume number identity are verified. The
fluid discretization retains the previous approximate, not exact, total-energy
conservation; no new claim of an exactly energy-conserving moving-fluid scheme
is made. Radius and eigenvalue refinement are essential evidence, not optional.

## 4. Both vacuum orderings were tested

The initial parameters were fixed before execution:

    (gamma,Sigma,DeltaV)=(1,0.6,+0.03),(1,0.6,+0.05),(8,0.4,+0.03).

These produced seven detected branches in R=0.5..40. Two have damped discrete
radial modes; the others have growing modes. The stable positive-DeltaV branches
still have substantially rising circular speeds. Flatter branches in this
sample are unstable, illustrating why mechanical force balance is insufficient.

The observed failure motivated a distinct physical alternative, frozen before
its run: a higher-energy interior, with

    (4,0.1,-0.03),(8,0.1,-0.03),(8,0.2,-0.03).

It yielded phase-confined, radially damped branches with flatter outer curves.
The following are representative results; eigenvalues belong to the FINITE-GRID
radius R_N, not to an asserted exact continuum radius:

| gamma | Sigma | DeltaV | continuum BVP R | N | R_N | largest Re(eigenvalue) | dln(v_c)/dln(r) at0.8R_N |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.6 | +0.03 | 4.37101 | 144 | 4.42040 | -5.521e-5 | 0.717 |
| 1 | 0.6 | +0.05 | 5.57323 | 144 | 5.64278 | -4.844e-5 | 0.624 |
| 8 | 0.4 | +0.03 | 4.64058 | 192 | 4.48781 | +1.965e-5 | 0.0148 |
| 4 | 0.1 | -0.03 | 7.81627 | 144 | 7.88144 | -5.239e-5 | -0.0102 |
| 8 | 0.2 | -0.03 | 7.47300 | 144 | 7.58179 | -3.367e-5 | -0.0520 |

For the last example, circular speed varies by approximately2.2% over the
resolved outer half of the halo. Its density ranges0.01912..1.93260 and
temperature4.32922..4.33541. Maximum mean-flow Mach number is0.000330.
The phase boundary is free to move in its stability test. Thus a roughly flat
outer speed curve and conditional radial damping coexist in an example with
no externally assigned radius. It is not a fit to an observed galaxy.

The higher-energy interior is a substantive additional assumption. The exterior
phase has lower vacuum energy; particle trapping and pressure support the
interior domain. Radial mechanical stability does not establish its quantum
vacuum lifetime, formation history or stability to nonspherical distortions.
Fast wall modes may also exceed the validity of a collisional fluid description;
a kinetic wall/fluid analysis is still required for a complete physical claim.

### Refinement and numerical limitations

For gamma8,Sigma0.2,DeltaV=-0.03:

| radial cells | R_N | largest Re(eigenvalue) |
|---:|---:|---:|
| 48 | 7.83999 | -3.40025e-5 |
| 96 | 7.64110 | -3.37664e-5 |
| 144 | 7.58179 | -3.36693e-5 |

The radii approach the independent BVP root7.47300; the144-cell radius is still
about1.46% high. The mode remains negative and its96-to144 change is about0.29%.
Halving the Jacobian step at48 cells changes its leading real part by8.6e-12.
For the gamma8 positive-DeltaV branch, the192-cell radius is still3.29% below
the BVP value, so quantitative continuum growth rates remain less well resolved.
Its positive-mode sign persists through refinement. No exact continuum
stability theorem is inferred from these samples.

Two high-gravity scan points initially failed to converge. In the first
negative-DeltaV run, a further BVP failure inside a valid root bracket returned
None to brentq and caused a TypeError. That incomplete attempt is preserved;
it is not evidence that the equilibrium does not exist. A new run using radial
continuation from converged profiles repaired the attempt and found the
Sigma0.1 branch at BVP R=11.12175. Its144-cell leading mode is-4.126e-5, and its
outer-half speed variation is about4.5%. The continued scans converged at all
sampled radii. This is still not an exhaustive enumeration of every branch.

## 5. The source family does not select a universal normalization

To test more than one favorable example, freeze gamma=8,Sigma=0.2,DeltaV=-0.03
and vary the source multiplier S. Follow the radially damped branch:

| S | continuum BVP R | R_144 | v_edge^4 | v_edge^4/S | outer-half speed variation |
|---:|---:|---:|---:|---:|---:|
| 0.5 | 2.44088 | 2.48408 | 16.8995 | 33.7989 | 25.3% |
| 1 | 7.47300 | 7.58179 | 108.926 | 108.926 | 2.2% |
| 2 | 14.64616 | 14.75892 | 273.134 | 136.567 | 6.3% |

All three have negative sampled leading radial eigenvalues. The S=0.5 case
also has a separate small-radius unstable branch, which is retained in the
results. The damped family is not uniformly flat and v_edge^4/S is not constant.
S is a prescribed source amplitude, not measured baryonic mass. Even if a
separate theory made S proportional to M_b, this sample would not supply the
universal desired relation. The integrated source INSIDE the halo also changes
with the selected radius, so it must not be silently equated with S.

At S=1, changing Sigma from0.2 to0.1 changes the selected BVP radius from7.47300
to11.12175 and the144-cell v_edge^4 from108.926 to137.254. Mechanical selection
of radius has therefore not removed dependence on phase parameters.

The exact steady number-budget identity from the previous report remains

    v_edge^4/S_total=gamma^2 R f/(3K),
    S_total=integral_0^R J r^2 dr,
    f=3 mu(R)^2/[R^3 integral_0^R n^2 r^2 dr],   0<f<=1.

R is now selected by phase pressure, but depends on Sigma,DeltaV,source and
cooling; f changes with the profile. The microscopic parameters and source
normalization remain in the answer. Nothing has selected the coefficient of
c sqrt(G rho_DE). Identifying a vacuum DIFFERENCE with an absolute cosmological
vacuum density would itself be an extra postulate. Even that identification
would not fix tension, mass barrier, cooling or the baryonic source relation.
The factors2 and1/2 in curvature, kinetic energy or reaction counting are not
the requested MOND coefficient.

## 6. What is established and what remains open

Established within the stated effective model: a physical mass-step trapping
mechanism, a wall force and work law, pressure-selected radii, numerical
phase-confined equilibria, and examples with damped resolved radial modes and
roughly flat outer curves. This replaces the arbitrary fixed-radius boundary
at the model level; it does not replace unknown phase microphysics by a
prediction. The configurations are continuously supplied and cooled, not
closed systems that manufacture their own energy.

Still needed: microscopic matching of the phase potential and mass barrier,
a derived source tied to baryonic matter/vacuum supply, sufficient retention and
radiation escape, wall formation/lifetime and kinetic/nonspherical stability,
and a successful galaxy family with an absolute acceleration normalization.
No such normalization is derived here, and none was fitted. The current
source-family calculation is a concrete limitation, not a proof against all
possible phase-confined halo models.

[Figures](phase_boundary_profiles.png) and [PDF](phase_boundary_profiles.pdf)
show the saved source-family profiles, radial refinement and normalization
variation. plot_phase_boundary.py reproduces them without rerunning solvers.

## Evidence and review

phase_boundary.py records the initial seven branches; phase_boundary_refinement.py
refines them through144 cells and the high-gravity branch through192.
false_phase_boundary.py tests the opposite vacuum ordering and preserves its
failed root attempt. phase_source_followup.py uses continuation to recover that
branch and tests S=0.5,2. phase_boundary_checks.py passes eight exact symbolic
checks of potential endpoints, curvature, tension, wall work, pressure stiffness
and mass-barrier leakage. The vacuum-sign negative control intentionally fails
only equilibrium consistency. All other reported solves pass their scoped
residual, moving-number-budget and wall-work checks.

Six evidence directories preserve commands, inputs, hashes and results:
phase_boundary, phase_boundary_refinement, phase_boundary_checks,
phase_boundary_mutate, false_phase_boundary and phase_source_followup, under
joint_phase/evidence. Frozen executed inputs were not edited. Initial scan
failures and the root TypeError remain visible, with the numerical cause and
continuation remedy distinguished from physical instability.

Self-audit verdict: **numerical evidence in the stated sampled phase-fluid
models**, conditional on the thin wall, high barrier, transparent radiation,
source and fluid closures. Radial wall motion was actually included. Review
is by the author, not an independent kinetic or field-theory validation.
The full stable-galaxy/1/2 research objective is not complete.
