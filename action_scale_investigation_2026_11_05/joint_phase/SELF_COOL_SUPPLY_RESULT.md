# Self-scattering, evaporative cooling and particle replenishment

2026-11-06. Base d02d18fad422cd88fed92de85127dcf209acc1d0;
frozen contract 60959d6edd. Continues SPECTRUM_THERMALIZATION_RESULT.md.

**Result:** there is a concrete conditional local mechanism: independent elastic
self-scattering redistributes kinetic energy; an escaping high-energy tail
cools the remaining material; injection replaces both evaporated and annihilated
particles. The resulting fixed-volume, fixed-potential equations have a unique
positive equilibrium and locally restoring density and temperature modes for
prescribed source data. This is net inventory maintenance, not preservation of
every individual particle. It is not yet a finite self-gravitating halo solution.
The required source profile and power remain unselected and do not yield1/2.

Natural units c=hbar=kB=1 are used unless explicitly restored. theta is the
material temperature expressed as energy. All formulas describe the specified
illustrative scalar model, not established dark-sector physics.

## 1. Compute self-scattering rather than assume instantaneous capture

Take the independent interaction -lambda_self chi^4/4!. Its constant tree
amplitude, including the identical-final-particle factor1/2, gives

    sigma_self(s)=lambda_self^2/(32 pi s).

A chi particle with kinetic energy Q hitting an identical stationary target has
s=4m^2+2mQ, hence

    sigma_self(Q)=lambda_self^2/[64 pi m(2m+Q)],
    sigma_self(0)=lambda_self^2/(128 pi m^2).

This is the pure contact contribution. Exchange of the existing S mediator and
interference must be negligible for it to describe the total cross section;
otherwise the actual amplitude must include them. Perturbativity and the
homogeneity/cold-target approximations must also hold.

The center-of-mass scattering is isotropic. In the target rest frame, one
labeled final kinetic energy q is uniform on[0,Q], with the other Q-q. Thus

    <max(q,Q-q)>=3Q/4,
    <ln[max(q,Q-q)/Q]>=ln2-1.

A sequence along the more energetic daughter suggests roughly
ln(Q/B)/(1-ln2) collisions to reduce that branch toward binding energy B. This
is a logarithmic-drift estimate, not an exact stopping-time result: it omits
overshoot, geometry, angular trajectories and the other branches. The early
mean free path is [n sigma_self(Q)]^-1; checking only the larger cold cross
section overestimates stopping. Each later branch needs enough column before
reaching the outer surface.

One collision illustrates the retention limitation precisely. For0<B<Q, the
expected fraction of initial kinetic energy carried by final particles with
kinetic energy below B is

    [2 integral_0^B q dq/Q]/Q = (B/Q)^2.

Both daughters can be bound only if Q<2B. For B<Q<2B the probability that both
are below B is2B/Q-1; for Q<=B it is one, and for Q>=2B it is zero up to endpoints.
Multiple collisions can distribute energy over more initially cold particles,
but cannot remove it. At least order Q/B final particles are needed if each
is to carry less than B. Gravitational potential changes and thermal background
energies are excluded from this kinematic estimate.

The cold collision hierarchy is

    Gamma_self/Gamma_ann
      = [lambda_self^2/(2 lambda^2)] v_rel/c.

It can be large while radiation opacity stays small, by a sufficiently large
lambda_self/lambda ratio. This evades the previous SAME-coupling radiation
trapping obstruction; it does not fix that ratio. A complete capture calculation
requires the energy-dependent stopping column and a source distribution inside
it. We have derived the scattering law, not proved halo-wide retention.

## 2. An explicit way to export heat: the escaping Maxwell tail

Assume collisions maintain a Maxwell distribution at a specified last-scattering
surface, above which propagation is collisionless. Let n and theta be its
material density and temperature; let B=m v_escape^2/2 be the fixed local escape
energy. Integrating outward radial velocities with kinetic energy above B gives

    F_N=n sqrt(theta/(2 pi m)) (1+x) exp(-x),   x=B/theta.

This is the Jeans-tail number flux. The energy-weighted velocity integral gives
the mean LOCAL kinetic energy per escaping particle,

    e_escape=theta (x^2+2x+2)/(x+1)
            =B+theta+theta^2/(B+theta).

The kinetic energy reaching infinity is e_escape-B. For a local fixed-potential
energy balance, use e_escape, not the energy at infinity; the difference does
work against the potential. A whole-halo gravitational budget must include it.
The escaping population is hotter than the mean material particle:

    b=e_escape-(3/2)theta
      =theta [x^2+x/2+1/2]/(x+1)>0.

Therefore evaporation cools remaining material while losing particles. It can
maintain inventory only with replacement. For x much greater than one, losses
are exponentially small, but so is this cooling channel. It cannot remove an
arbitrarily large heat load while losing essentially no particles.

The surface location is not arbitrary in a real halo: it depends on the density,
cross section and scale height. Rapid evaporation can deplete the Maxwell tail
or become a bulk outflow. For contextual primary-source support, the kinetic
study [Volkov et al., transition from hydrodynamic to Jeans escape]
(https://arxiv.org/abs/1009.5110) reports different regimes as the binding-to-
thermal-energy ratio changes. Its abstract was checked, not its numerical model
transferred to this halo. The flux and moments above are integrated here and
remain conditional on the stated Maxwell and collisionless-exterior assumptions.

## 3. Couple cooling and replacement with conserved energy

Consider a local, well-mixed fixed-volume reservoir with effective escape area
S_b and volume V. Its loss rate per particle is

    a(theta)=(S_b/V) sqrt(theta/(2 pi m)) (1+B/theta) exp(-B/theta).

This reduction assumes surface density and temperature equal the reservoir
values. It is not a radial density profile. Let J>0 be a fixed number injection
rate per volume, e_in>0 the mean retained injection kinetic energy, and K>0 the
constant cold annihilation coefficient. Annihilation radiation escapes; the
radiation-thin regime is compatible with independently strong self-scattering.
Let c_v=3/2. Number and kinetic energy obey

    n_dot=J-K n^2-a n,
    d(c_v n theta)/dt=J e_in-c_v theta K n^2-a n e_escape.

Rest energy satisfies its separate balance m n_dot=m(J-Kn^2-an); adding it
restores full local particle energy. The source must pay for rest mass as well
as kinetic energy. Because annihilation at constant K removes mean-energy
particles, its direct temperature term cancels when number changes are included:

    c_v n theta_dot=J(e_in-c_v theta)-a n(e_escape-c_v theta).

Elastic self-scattering enables this moment closure but contributes no net
energy sink. Omitting the changing-number term gives an incorrect temperature
law; the deliberately mutated computation fails energy conservation.

At equilibrium,

    J=n*(K n*+a),
    n*(theta)=2J/[a+sqrt(a^2+4KJ)],
    e_in=[c_v theta K n*+a e_escape]/(K n*+a).

The selected injection energy is between c_v theta and e_escape. Thus for a
given desired cold temperature there is a finite compatible energy budget.
A highly energetic source cannot be made cold simply by increasing elastic
collisions; injection energy must leave through annihilation radiation and the
escaping population at the rates allowed by these equations.

For fixed positive J,K,B,S_b/V the mathematical model has exactly one positive
equilibrium for each e_in>0. To see this, a increases with theta, n* decreases,
and w=a/(K n*+a) increases. The required energy is

    e_required=(1-w)c_v theta+w e_escape.

Both c_v theta and e_escape are strictly increasing, and e_escape>c_v theta;
therefore e_required is strictly increasing. It tends to zero as theta tends
to zero and grows without bound as theta tends to infinity. The high-temperature
limit is used only to establish the mathematical continuation of the equations;
a physically valid equilibrium must lie in their nonrelativistic, evaporation
rather than wind regime. Uniqueness does not prove global attraction.

### The local stability calculation

At equilibrium write A=a(theta*), A'=da/dtheta, e'=de_escape/dtheta, b as above.
Direct differentiation yields

    A'/A=[1/2+x^2/(1+x)]/theta >0,
    e'=1+theta/(B+theta)+B theta/(B+theta)^2 >0.

For the two-variable(n,theta) Jacobian,

    trace=-3K n*-A-(A' b+A e')/c_v <0,
    determinant=(2K n*+A)K n*
                +[2K n* A' b+(2K n*+A)A e']/c_v >0.

Both eigenvalues have negative real part. The fixed-potential local reservoir
therefore returns toward its equilibrium after sufficiently small abundance
and temperature perturbations. This is a derived local restoring mechanism,
not the earlier postulated global feedback law.

But B, area/volume, J and e_in are held fixed. A self-gravitating halo changes
its potential, radius and density profile when heated or depleted. The negative
heat capacity and transport modes from the previous report are not included
in this Jacobian. It cannot be used to claim a stable galaxy.

## 4. What replenishment a flat halo would actually require

For an attempted stationary isothermal tail n=A_h/r^2 over r_c<r<R, no bulk
radial flow and negligible local evaporation inside the surface, continuity
requires the VOLUME source

    J(r)=K A_h^2/r^4.

The previously derived ballistic mediator-decay source instead scales as
exp(-r/l)/r^2. They cannot agree over an extended radial interval with fixed
parameters. The source must be changed physically, or transport and its energy
budget solved; assigning J=Kn^2 is a requirement, not a mechanism generating it.

The number replacement rate required by annihilation in this tail alone is

    Ndot_ann=4 pi K A_h^2(1/r_c-1/R).

It depends strongly on the inner cutoff, whose core solution is not given.
Additional core losses are not included. Hydrostatic self-gravity for the ideal
isothermal tail gives v_h^2=4 pi G m A_h and theta=m v_h^2/2. Consequently the
minimum rest-energy supply to this tail is

    P_rest=m Ndot_ann
          =[K v_h^4/(4 pi G^2 m)](1/r_c-1/R).

If the same tail density reaches a specified Maxwell escape surface, an
additional replacement requirement is

    Ndot_evap=4 pi A_h sqrt(theta/(2 pi m)) (1+x) exp(-x).

This is conditional on the surface assumptions; it is not a selected truncation
radius. Source power for retained injected particles is at least
(m+e_in)(Ndot_ann+Ndot_evap), with further power lost in inefficient production
and capture. Gravity and bulk transport can require additional terms.

In the interior no-flow, no-conduction limit, local energy balance also selects
e_in=c_v theta. Combining this with hydrostatic equilibrium gives

    v_h^2=4 e_in/(3m).

A fixed injection spectrum would then select the same speed across objects,
not v_h^4 proportional to baryonic mass. This excludes only that restricted
no-transport closure, not all replenished halos.

Even optimistically neglecting evaporation and taking a source with luminosity
L_src deposited entirely into this tail, the power balance would give

    v_h^4=4 pi G^2 m^2 L_src /
          [K (m+e_in)(1/r_c-1/R)].

An imposed L_src proportional to M_b can mimic the desired exponent, but its
coefficient depends on K,m,e_in, the source normalization and the core/outer
radii. There is no equation here relating this combination to rho_DE. The
previous front energy budget still leaves its conversion power and deposition
unselected; elastic self-scattering does not supply either.

## 5. Scope of the result and next missing implication

The constructive result is a conditional local density/temperature attractor
from explicit evaporation and particle/energy conservation. It repairs neither
the unknown physical replacement source nor the global halo boundary. It keeps
a steady inventory by replacing lost particles; it cannot maintain all original
particles indefinitely while exporting energy by their escape.

The target a0=(c/2)sqrt(G rho_DE) remains unproved. No parameter was calibrated
to obtain1/2. A full solution would have to derive J(r),e_in and energy export
from the chosen interactions/reservoir, solve capture and a moving exobase with
gravity, and verify the coupled spatial equilibrium and stability. The present
source has the wrong profile for the simplest no-flow flat tail. Permitting
transport is an open route, but its source and boundary data must be supplied
rather than chosen to reproduce the answer.

## Evidence and self-review

self_cool_supply.py passes15 exact symbolic checks of cross-section limits,
energy partition, escaping-tail moments, energy conservation, the local
Jacobian and tail replacement power. The mutation omits the changing-number
term and fails exactly kinetic-energy conservation(14/15 pass). Both runs and
hashed inputs are preserved in evidence/self_cool_supply and
 evidence/self_cool_supply_mutate. These tests are not Monte Carlo cascade
capture or a self-gravitating halo simulation.

Self-audit verdict: **conditional on named inputs**. Tree contact kinematics,
Maxwell moments and conservation identities passed the checks. Positivity of
the Jacobian trace/determinant expressions establishes local stability under
the fixed-potential reduction. Equilibrium uniqueness follows from the stated
monotonicity argument; it is not a claim of global convergence. Contact dominance,
Maxwell-tail replenishment, actual source power, capture fraction and global
potential response remain assumptions or unresolved obligations. The local
stability does not inherit a proof for the global model. Proofreading and units
review covered this report and its status entry; frozen executed inputs were
not changed. This is author self-review, not independent verification.

Route disposition: self-scattering has a derived energy-dependent law but
retention awaits spatial transport; evaporative local stabilization is derived
conditionally; the existing no-flow mediator-fed flat-tail construction fails
its source-profile discriminator. Nonlocal transport remains open with its
source/boundary inputs unselected. The broader research goal is not complete.
