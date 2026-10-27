# Free mass, reciprocal response, and the retained galaxy law

20 October 2026. Checkpoint FCP-2026-10-20-R1. Assessment base:
`f659e6d8e`. This is a new analytic work package, not a revision of a frozen
candidate. It extends the existing reciprocal deep-cubic calculation in
`real_research/analytic_review_2026_10_18_codex/KINETIC_PARTITION.md` to the
canonical saturating remainder and separates cold rest from warm support.
No novelty claim is made for reciprocity or the deep-cubic parent.

## Target and scope

Can a free cold component attract the tethered component's mass in the
ordinary way, yet leave that component at its baryon-only cold rest state?
Use spherical symmetry, Newtonian gravity, positive separately conserved
baryonic/tethered/free densities, ordinary inertial masses, the ID critical
self-gravity cancellation, and the canonical remainder potential. Do not add
a second independent polarization population. All integrals and variations
are taken on regular finite profiles; local rest statements apply on an
occupied annulus. They do not assert an infinite-stock global equilibrium.
Stiffness is omitted here, so the algebraic law applies in its zero-stiffness
limit. A finite-stiffness candidate needs its own boundary-value calculation.

Write enclosed masses B(r), T(r), F(r), K=4 pi G,

    u=G T/r^2,    R(u)=K W_rem'(u)=u^2/(a0-u),   0<=u<a0.

F denotes enclosed free mass, not a distribution function. Physical particle
distributions below are denoted f_t. The acceleration sign is outward positive.

The result below concerns a specified class of instantaneous reciprocal
energies. It does not exclude a warm solution, a dynamical reservoir, a new
interaction, a constrained history variable, or another relativistic action.

## 1. The counted energy and both variations

Add ordinary free mass to the existing critical-ID energy. Up to a fixed
baryon self-energy, its potential energy is

    U = -G/2 integral [(B+T+F)^2-T^2]/r^2 dr
        + integral 4 pi r^2 W_rem(G T/r^2) dr.

This counts each gravitational pair once. The +T^2 counterterm cancels only
the tethered self-gravity. In particular the cross energy
`-G integral T F/r^2 dr` remains. This is a declared two-population extension;
the original frozen S2 action does not already specify it.

For a small outward displacement of material at r, enclosed mass decreases
over the traversed interval. Therefore `a_i=partial U_integrand/partial M_i`,
and direct differentiation gives

    a_t = -G(B+F)/r^2 + R(u),
    a_f = -G(B+T+F)/r^2,
    a_b = -G(B+T+F)/r^2

when baryons are also varied. The remainder derivative is
`4 pi G W_rem'(u)=R(u)`, with no second full-potential contribution.
For `u<<a0` this recovers the earlier reciprocal deep-cubic model exactly
at leading order. At F=0 it recovers the canonical cold rest equation.

## 2. Exact cold-rest source response

On an occupied annulus with zero material stress and no external pinning,
`a_t=0` requires

    R(u)=s,    s=G(B+F)/r^2.

For s>0 there is exactly one admissible root,

    u(s) = [sqrt(s^2+4 a0 s)-s]/2,
    g(s) = s+u(s) = [s+sqrt(s^2+4 a0 s)]/2.

The limit s=0 has the root u=0. These equations imply
`s=g^2/(g+a0)`, the same algebraic interpolation but sourced by baryons
**plus free mass**. This is the total inward force on an ordinary tracer in
the relaxed extension, not law-boosted self-gravity of the free particles in
isolation: the extra response is carried by the tethered stock.

Conversely let `u_b=u(G B/r^2)` be the baryon-only cold rest profile. Retaining
it after adding free mass produces exactly

    a_t[u_b,F]=-G F/r^2.

It is not a cold rest state wherever F>0. Small initial perturbations or an
unchanged label do not remove this acceleration. An imposed immobile density
must supply a constraint reaction or another stress/force and its energy.

At fixed B and r the fully relaxed tracer force exceeds the prescription
`g(G B/r^2)+G F/r^2` by

    Delta g = u(G(B+F)/r^2)-u(G B/r^2)>0   (F>0).

Implicit differentiation gives

    du/ds=(a0-u)^2/[u(2a0-u)],
    dg/ds=a0^2/[u(2a0-u)]>1.

The derivative is for s>0; it diverges as s decreases to zero and approaches
one for g at high s. Thus the missing response can be appreciable in the
deep regime. Its actual magnitude needs the available tethered stock,
transport, material stress and stiffness. The static formula cannot be
applied after exhausting the finite stock, and supplies no settling time.

## 3. Why one-way removal is not a conservative repair

For any twice differentiable instantaneous density energy, its two mixed
variations commute. If the free population feels the Newtonian attraction of
the tethered mass, the mixed kernel is

    delta h_f(x)/delta rho_t(y)=-G/|x-y|

up to the relevant self-energy conventions; reciprocity requires its transpose
in `delta h_t(y)/delta rho_f(x)`. Setting this latter response to zero while
retaining the former cannot come from that energy. Locally eliminating an
auxiliary field through a differentiable stationary branch preserves
symmetry of the reduced Hessian. Stability alone does not ensure that this
smooth reduction exists. An explicitly
retarded or open-system reduction is outside this instantaneous theorem and
must include the omitted field or receiver energy and momentum.

The same statement survives separate mass conservation. Take thin spherical
shell rearrangements

    delta rho_t: unit mass moved from r=1 to r=3,
    delta rho_f: unit mass moved from r=2 to r=4.

Each has zero total mass; choose sufficiently large positive base stocks so
small rectangular variations remain nonnegative. The gravitational cross
coefficient is

    C=-G[1/4-1/3-1/4+1/2]=-G/6.

A generalized chemical-potential one-form assigning zero free-to-tethered
response and retaining `C q_t` in the free response has a nonzero integral
`C A B` around the oriented amplitude rectangle `[0,A] x [0,B]`. It is not
an exact differential. Thin shells can be mollified on disjoint nearby
intervals; the cross coefficient remains nonzero by kernel continuity. This
is not an astrophysical fit or an exclusion of every capture rule.

A counterterm cancelling this cross kernel cancels **both** reciprocal
interactions. A new species-selective force is possible in principle, but
cannot retain the same two ordinary forces without recounting the mediator.

## 4. A real remaining escape: warm support

The cold-rest conclusion must not be promoted to a no-go for all equilibrium
profiles. At the baryon-only target, the actual tethered acceleration is
`a_t=-g_f`. A stationary isotropic tethered component can formally balance it
with a pressure obeying

    dp_t/dr=-rho_t g_f,
    p_t(r)=integral_r^infinity rho_t(s) g_f(s) ds

when the integral converges and the outer pressure vanishes. For a regular
finite system the exact scalar virial identity is

    2 K_t = B_boundary + integral r g_f(r) dT(r).

For zero boundary stress and overlapping positive mass this demands
nonzero kinetic energy. It is an actual energetic requirement, not an
inconsistency. Positive pressure alone does not establish a nonnegative
collisionless distribution, nonlinear stability, or selection by formation.
The existing warm kinetic families are therefore legitimate continuations,
but are separate candidates from a cold density projection.

## Consequence and next discriminating task

The cold law and an added Newtonian free core cannot simply be combined as a
fully relaxed state of this particular reciprocal energy. The available
continuations are explicit: evolve the changed tethered response; construct
a positive warm distribution and count its kinetic energy; or add and vary
the reaction/stress mechanism that holds the old profile. The first task
before another empirical score is to choose one of these actual equations.

The analytic parent already establishes reciprocity in the deep limit. This
note's additional result is the full-remainder rest response and the exact
distinction between cold rest, asymmetric force deletion, and warm support.
It neither modifies CFG888/916's frozen verdicts nor transfers their data
passes to the extension. Metric/lensing, cosmological abundance, kappa,
formation and conversion remain open.

## Verification contract

`POSITIVE_WARM_COMPARISON.md` now supplies one formal nonnegative isotropic
distribution for the untruncated baryon-only target under a central free
mass. It has infinite total mass and fails the required global monotone
energy slope, so the finite regular stable continuation remains open.

`check.py` uses exact rational arithmetic to reconstruct the counted
quadratic energy, its two mixed variations, the zero-mass shell coefficient,
and 36 rational admissible saturation points. `contract.json` declares the
finite assertion; the bounded runner stores the observed manifest and
results. `run_cpu/manifest.json` records completed execution: 120/120 exact
checks pass. `mutation_cpu/manifest.json` records the intended failed run:
119/120 pass after deleting the reciprocal response. The initial `run/` and
`mutation/` records retain launch failures: on this macOS host lowering
RLIMIT_AS raises `ValueError: current limit exceeds maximum limit`. The
successful reruns enforce CPU/time/output limits and one conventional thread;
no hard address-space cap was applied. The small stdlib arithmetic program
has no integration, array allocation, process fanout or simulation.
The mathematical statements for continuous profiles rely on the
derivation above, not the finite grid. A sign/deletion mutation must fail the
mixed-variation check. Its originally assigned mixed-derivative constants are
supplemented by `mixed_variation_control.py` and `mixed_run/manifest.json`:
both derivatives are reconstructed from the energy and the asymmetric-force
control, and the shell coefficient is reconstructed from four pair kernels.
A separate-agent audit is recorded in `AUDIT.md`; it is not a blind external
review or a formal proof certificate.
