# Can a pool erase its formation history?

## Outcome

Two explicit mechanisms were evaluated. A particle reservoir can erase initial
abundance in a convex fixed-potential problem, but sets the answer through its
own temperature and chemical potential. Baryon-powered heating/cooling can
produce an outer 1/r^2 material density and, conditionally, v_flat^4 proportional
to baryonic mass. However the cooling law giving that scaling under linear
mass-dependent heating has a marginal isobaric thermal mode. It is not a proved
history-erasing halo attractor. Its coefficient also depends on independent
heating, absorption and cooling physics, not dark-energy density.

This changes the question from merely finding an equilibrium to finding a
stable, normalized equilibrium. No 1/2 is derived. Base: aa12697db1; fixed
contract RELAXATION_CONTRACT.md committed as 99c97903d5. These are conditional
extensions, not a validated completion of the two-field action.

## A. What relaxation can and cannot erase

Let n be material particle number density, m its mass, Phi_b a fixed baryonic
potential, and Phi_p the pool's self-potential. For a classical isothermal gas,
a grand free-energy functional is

    Omega[n] = integral { kB T n[ln(n/nQ)-1]
                       +(m c^2-mu_res)n + m n Phi_b } dV
               + (1/2) integral m n Phi_p dV,
    nabla^2 Phi_p=4 pi G m n.

Its variational chemical potential is

    mu_loc = kB T ln(n/nQ)+m c^2-mu_res+m(Phi_b+Phi_p).

For a hypothetical dissipative dynamics

    partial_t n = div[M(n) grad mu_loc] - Gamma(n) mu_loc,

with positive mobilities and vanishing boundary terms,

    dOmega/dt = -integral M |grad mu_loc|^2 dV
               -integral Gamma mu_loc^2 dV <= 0.

This is a derived dissipation identity, not an invented assertion that entropy
must somehow select the desired answer. The transport-only case Gamma=0
conserves total particle number: collisions can erase velocity information
without erasing initial inventory. Gamma>0 represents actual reservoir exchange
or reactions; it cannot be added without supplying their physical mechanism.
Its rate and available reservoir also determine whether relaxation happens
within a galaxy's lifetime.

Without self-gravity, at fixed T and reservoir chemical potential, strict local
convexity kB T/n gives the unique stationary density

    n_eq=nQ exp[(mu_res-m c^2-m Phi_b)/(kB T)].

Thus an appropriate reservoir can remove initial-state dependence while leaving
an answer dependent on *reservoir parameters*. Homogeneous exchange
n_dot=gamma(n_eq-n), for example, converges exponentially to n_eq, but that is
not a microscopic derivation of n_eq. Dark energy was not shown to be such a
particle reservoir or to fix its temperature/chemical potential.

Including self-gravity adds a negative quadratic contribution:

    delta^2 Omega = integral (kB T/n)(delta n)^2 dV
        -G m^2 double_integral delta n(x) delta n(y)/|x-y| dVx dVy.

It need not be positive. Decreasing free energy alone therefore proves neither
a unique global equilibrium nor resistance to gravitational collapse. Boundary
conditions, finite size, reactions, and stress support matter. One cannot infer
a unique galaxy mass from thermalization alone.

A common fixed-temperature bath has an additional scaling problem: for an
isothermal halo v_flat^2=2 kB T/m. With universal particle mass and bath T,
all halos have the same asymptotic speed, rather than v^4 proportional to Mb.
A galaxy-dependent temperature law would have to be derived separately.

## B. Baryon-powered feedback that does produce a flat tail

Assume a spherical optically thin outer region, constant particle mass m,
absorption cross section sigma_abs, approximately central heating luminosity L,
and cooling function Lambda(T). Let

    H = n sigma_abs L/(4 pi r^2),
    C = n^2 Lambda(T).

These are energy per volume per time. They are *not* particle source and sink
terms. Setting H=C gives

    n(r)=A/r^2,   A=sigma_abs L/[4 pi Lambda(T)].

For constant T and a halo-dominated region this yields

    rho_p=m A/r^2,
    v_flat^2=4 pi G m A = G m sigma_abs L/Lambda(T).

Hydrostatic balance d(n kB T)/dr=-m n v_flat^2/r then requires

    T=m v_flat^2/(2 kB).

Thus heating, cooling and hydrostatic equilibrium jointly provide a conditional
steady outer profile rather than putting the 1/r^2 density in as an input.
The infinite ideal tail needs a core and outer boundary; it has divergent total
mass otherwise. A central baryonic mass adds a 1/r correction to v_c^2 and
spoils exact constant-temperature balance in the inner region. The derivation
is an outer asymptotic approximation, not a full rotation-curve fit.

The optically thin assumption must hold over the range used. Absorption,
finite-source geometry, temperature gradients, and a low heating luminosity
can change this profile. A galaxy with little current stellar heating cannot
be assumed to have the same L/Mb as an actively star-forming one.

### Mass exponent and normalization

Take Lambda(T)=Lambda_q T^q with constant cross section over the relevant
range, and L=L0 Mb^p. Combining the two equations for speed gives

    (v_flat^2)^(q+1)
       = G m sigma_abs L (2 kB/m)^q / Lambda_q,
    v_flat^4 proportional to Mb^[2p/(q+1)].

For the baryonic fourth-power law the required relation is p=(q+1)/2.
For example, *if* L=ell Mb and Lambda=Lambda_1 T, then

    v_flat^4 = 2 G kB sigma_abs ell Mb/Lambda_1,
    a_eff = 2 kB sigma_abs ell/Lambda_1,
    kappa = 2 kB sigma_abs ell/[Lambda_1 c sqrt(G rho_DE)].

The mass exponent is obtained conditionally without inserting a0. The coefficient
is not fixed. ell, sigma_abs and Lambda_1 are independent inputs here, and
rho_DE does not enter their equations. To obtain the target one would need
an independently derived identity

    Lambda_1 = 4 kB sigma_abs ell/[c sqrt(G rho_DE)].

Choosing this identity as a parameter constraint would put the answer in by
hand. No microscopic derivation of a universally linear cooling function or
universal L/Mb has been supplied. In particular this cooling interaction was
not already present in the earlier free chi-particle production calculation.

## C. Does this feedback actually erase memory?

A thermal stability test distinguishes fixed-density and fixed-pressure
perturbations. For fixed n, the heating per particle is constant while cooling
per particle scales as T^q; the local thermal mode is restoring for q>0.
At fixed pressure, n=P/(kB T), so cooling per particle instead scales as
T^(q-1). For a monatomic ideal gas the enthalpy equation is

    (5/2) kB T_dot = sigma_abs L/(4 pi r^2)
                     -(P/kB) Lambda_q T^(q-1).

At an equilibrium, with theta=T/T_eq and an appropriate positive time unit,

    theta_dot=1-theta^(q-1),
    derivative_at_theta1 = 1-q.

Consequently q>1 restores isobaric thermal perturbations; q<1 amplifies them;
q=1 is marginal. At q=1 and the equilibrium pressure, the RHS is zero for
every positive theta. Local thermal feedback alone does not select a unique
T or n along this constant-pressure family. Gravity, conduction, transport and
particle reactions could change the full mode spectrum; this local result
is not a proof that every global q=1 halo is unstable or impossible.

The tension is precise: for linear heating L proportional to Mb, q=1 gives
the desired mass exponent but no isobaric thermal restoring term. A strictly
restoring q>1 gives a shallower fourth-power mass exponent under that same
heating law. One could also change p, include a varying opacity, or add
conduction/reaction feedback, but those modifications require a joint physical
derivation. Merely selecting p=(q+1)/2 would not derive universality.

As a finite relaxation check, q=2 gives the exact solution

    theta(t)=1+[theta(0)-1] exp(-t).

Numerical trajectories starting at 0.1 and 10 reach 0.9999944702 and
1.0000552979 by t=12, agreeing with the exact solution within 1.1e-9.
This explicitly shows thermal history erasure in that local mode. It does not
show particle-number erasure, halo formation, or a MOND coefficient. Its
conditional fourth-power mass exponent for p=1 is 2/3, not 1.

## D. A phase-pressure boundary still requires its own selector

If the ideal halo-dominated tail is truncated by a positive, independently
supplied Pext, then

    P(R)=rho_p(R) kB T/m=v_flat^4/(8 pi G R^2),
    R=v_flat^2/sqrt(8 pi G Pext),
    Mp approximately v_flat^2 R/G
       =v_flat^4/[G sqrt(8 pi G Pext)].

If v_flat^4=G Mb a_eff, this would imply

    Mp/Mb approximately a_eff/sqrt(8 pi G Pext).

These are conditional radius/inventory relations, not a new mass creation law.
The initial supply or exchange process must allow the halo to reach them.
The pressure remains the phase difference plus wall and matter contributions,
as derived in BARYON_PHASE_RESULT.md; it is not automatically rho_DE c^2.

A useful consistency test: if one grants Pext=rho_DE c^2 and inserts the target
kappa=1/2 solely to test its consequences, the mass ratio would be
1/[2 sqrt(8 pi)], about 0.10. That violates the halo-dominance approximation
used to derive the outer tail at this boundary. It cannot be presented as a
self-consistent successful match. This is a diagnostic consequence, not a
parameter choice or input to the computation. The algebraic boundary relation
also matches the critical-edge identity in POOL_PRESSURE_RESULT.md and does
not independently derive its missing coefficient.

## Evidence, scope, and next discriminator

relaxation.py passes 19 checks. The negative control deliberately omits the
isobaric density response and fails exactly the stability derivative check.
Both manifests are validated. The free-energy identity, gravitational second
variation and interpretation are analytic, self-reviewed arguments; the
ODE evidence verifies only the stated local mode. No full hydrodynamic
attractor, age comparison, microscopic interaction rate or galaxy data fit
is claimed.

Adjacent literature, checked at abstract level:
[Foot, Dissipative dark matter halos: The steady state solution](https://arxiv.org/abs/1707.02528)
already studies supernova heating and dissipative halo cooling. Thus the broad
feedback mechanism is not a novelty claim. Its abstract does not establish
our simplified model's normalization or stability; those were derived here.

Route A: conditional reservoir history erasure established, but reservoir
normalization and self-gravitating stability unselected. Route B: conditional
flat tail and baryonic mass scaling established, with independent normalization
and a marginal local thermal mode in the linear/linear case. Route C: finite
boundary inventory relation established conditionally; pressure selection,
supply and halo-dominance consistency remain unresolved.

A useful continuation must derive actual absorption/cooling/reaction rates and
stellar energy transfer from a specified extension of the shared interaction,
then test the full coupled mode spectrum and supply. Conduction alone cannot
fix a uniform thermal mode or create missing particles. More relaxation runs
with freely selected reservoirs, exponents or rates would not answer the
coefficient question. Such microscopic closure and fully coupled formation
remain open; this calculation does not prove all possible attractors fail.
