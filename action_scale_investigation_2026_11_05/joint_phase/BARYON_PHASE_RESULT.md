# Baryonic loading and a matter-supported vacuum-phase boundary

## Verdict

The new calculation includes resolved baryons and pool self-gravity. It does
not select a unique pool mass. A separate explicit scalar model shows how
baryons can favor an interior vacuum phase, and how their declining density
can stabilize a phase boundary. These are constructive mechanisms, but neither
supplies the requested universal coefficient. In particular a vacuum bubble
is not itself the attractive material pool.

Base result: POOL_PRESSURE_RESULT.md at c28bc49408. Frozen scope:
BARYON_PHASE_CONTRACT.md at e6ad90fdc7. This is a conditional model calculation,
not an adopted fundamental action or a claim about all dark-sector theories.

## A. What gravity actually sets

For a material pool P=cs^2 rho_p, a prescribed spherical baryonic distribution
rho_b, and its own gravitational field,

    cs^2 d ln rho_p/dr = -G[Mb(r)+Mp(r)]/r^2,
    dMp/dr = 4 pi r^2 rho_p.

Ignoring self-gravity only to expose the integration constant, a Plummer
baryonic potential Phi_b=-G Mb/sqrt(r^2+a^2) gives exactly

    rho_p(r) = C exp[G Mb/(cs^2 sqrt(r^2+a^2))].

Gravity determines density contrast. The constant C (or the density at a
specified boundary) is a particle inventory/chemical-potential datum.
An infinite uniform reservoir cannot be treated as globally nongravitating;
this formula is a local test-fluid limit, not a global halo solution.

The numerical test retains self-gravity. With x=r/a,
m=G Mp/(a cs^2), d=4 pi G a^2 rho_p/cs^2, B=G Mb/(a cs^2),

    m'=x^2 d,
    (ln d)'=-(m+B x^3/(1+x^2)^(3/2))/x^2.

Set B=1 and boundary d_s=0.001. Hold a and cs fixed. Three regular central
densities give the following distinct equilibria at that same pressure:

| Central d | Surface x | Pool mass m (=Mp/Mb here) | Surface v_c^2/cs^2 |
| --- | ---: | ---: | ---: |
| 0.01 | 56.3483153034 | 97.7462388734 | 1.75241737231 |
| 0.03 | 54.8967904904 | 126.2550354840 | 2.31806881276 |
| 0.10 | 49.2706095050 | 118.9594730848 | 2.43469396283 |

Each is integrated at two tolerances, 1e-9 and 1e-11. These are dimensionless
counterexamples to equilibrium uniqueness, not selected galaxy parameters,
stability-certified objects, or observations. Both stable and unstable
branches may be present. A full formation/stability calculation could select
some subset; hydrostatics alone has not done so. The test deliberately grants
an independently fixed positive surface pressure; it does not assume that the
scalar construction below automatically supplies that pressure.

### Inventory conservation and exchange

For conserved pool particles, continuity gives

    dMp(<R)/dt = -4 pi R^2 rho_p(R) [u_p(R)-Rdot]

at a moving spherical boundary, in the nonrelativistic fixed-particle-mass
limit. Baryonic gravity changes u_p, not the conserved total inventory. A
finite pool's supply depends on initial density and boundary flux. A source
term requires a specified conversion or production process.

An isothermal ideal-gas reservoir would instead select a density through
chemical equilibrium:

    mu_res = m_p c^2 + kT ln(n_p/n_Q) + m_p Phi,
    n_p = n_Q exp[(mu_res-m_p c^2-m_p Phi)/(kT)].

It supplies the missing integration constant only after mu_res, T, particle
mass, and phase-dependent interactions are specified. Equating mu_res to zero
without a number-changing reaction and thermal state would be another imposed
condition. An isothermal free-energy variation at fixed N yields pressure
balance, but does not vary the conserved N into a predicted value.

## B. An explicit matter-dependent two-phase potential

For this section use energy-density units for the potential; canonical scalar
field formulas are written with c=hbar=1, restoring c in baryon rest energy.
Consider

    q(z)=(2+3z-z^3)/4,
    V(phi)=Vout + lambda(phi^2-v^2)^2/4 + DeltaV q(phi/v),
    E_b density = rho_b c^2 [1+epsilon q(phi/v)].

This coupling is a hypothesis under test, not a consequence of the analogy.
Take DeltaV>0, lambda>0, v>0; an interior phi=+v phase has a higher vacuum
energy than the exterior phi=-v. At fixed nonrelativistic baryon density,
replace DeltaV by D_eff=DeltaV+epsilon rho_b c^2 in the local potential.
Because q(-1)=0, q(+1)=1 and q' at both endpoints is zero, both phases are
stationary, with curvature

    V_eff''(+v)=2 lambda v^2-3 D_eff/(2 v^2),
    V_eff''(-v)=2 lambda v^2+3 D_eff/(2 v^2).

Both are local minima if |D_eff|<4 lambda v^4/3. A negative epsilon can favor
the interior phase where baryons are dense even when DeltaV>0 in empty space.
Baryonic effective mass must stay positive in the field range used; for the
thin-wall interpolation q in [0,1], -1<epsilon<0 suffices. The polynomial is
a local effective model, not a globally established matter theory.

### Pressure follows from varying the wall, including the baryons

In a spherical thin-wall approximation with tension Sigma and fixed baryon
profile, the energy difference is

    E_phase(R)=4 pi Sigma R^2 + (4 pi/3) DeltaV R^3
               + epsilon c^2 Mb(<R).

The pressure opposing a pool's expansion is therefore

    (dE_phase/dR)/(4 pi R^2)
      = DeltaV + 2 Sigma/R + epsilon rho_b(R)c^2.

With negligible external ordinary pressure, an interior material pool must
satisfy

    Ppool(R)=DeltaV+2 Sigma/R+epsilon rho_b(R)c^2.

A fully coupled equilibrium must also include material gravity, wall effects
on the metric, and any pool-scalar couplings. This equation is the local
weak-gravity, thin-wall phase contribution; it is not a full relativistic
junction-condition solution. Within a cold weak-gravity pool, gravitational
potential corrections to these energy terms are suppressed by |Phi|/c^2.

Two consequences matter:

1. If the wall lies outside the baryons, Mb(<R) is nearly constant. The
   baryonic phase-energy gain does not provide an extensive pressure there.
   The boundary responds to the local rho_b(R), not total Mb alone.
2. Adding the same constant to both vacua changes Vout but not DeltaV or
   this local pressure law. Cosmological gravity responds to that constant;
   the local phase model supplies no identity tying DeltaV to Vout=rho_DE c^2.

For a uniform environment with D_eff<0 and no pool, the stationary bubble is
Rcrit=-2 Sigma/D_eff. Direct differentiation gives E''(Rcrit)=-8 pi Sigma:
it is an unstable radial maximum, not a stable selected pool.

### A stable matter-supported boundary is nevertheless possible

A declining baryon density changes that conclusion. First neglect tension
as the leading large-radius limit. For a Plummer profile

    rho_b(R)=3 Mb/(4 pi a^3) [1+R^2/a^2]^(-5/2),

and epsilon<0, a wall without material pool obeys

    rho_b(R*) = DeltaV/(|epsilon|c^2),
    R* = a sqrt(K^(2/5)-1),
    K = 3 |epsilon| Mb c^2/(4 pi a^3 DeltaV),  K>1.

At this radius E''=4 pi R*^2 epsilon c^2 rho_b'(R*)>0. Thus the radius is a
local minimum. For a nondegenerate root at R*>0, a sufficiently small positive
tension preserves a nearby minimum by continuity; exactly zero tension is
only the reference limit. At finite tension the stability condition is

    epsilon c^2 rho_b'(R*) > 2 Sigma/R*^2.

This proves a conditional radial trapping mechanism, not full nonspherical,
quantum, or baryon-backreaction stability. At small radius tension can also
introduce a nucleation barrier. The radius depends on the baryonic size a,
the coupling epsilon and DeltaV, not just Mb and rho_DE. At K much greater
than one and fixed a, R* scales as Mb^(1/5), so the vacuum excess energy
DeltaV times volume scales as Mb^(3/5). This is not a universal baryonic
mass inventory or the desired rotation law.

### Why a vacuum bubble alone is not the attractive pool

A locally uniform vacuum excess has rho_E=DeltaV and p=-DeltaV. Its weak-field
active mass density is (rho_E+3p)/c^2=-2 DeltaV/c^2. Its *vacuum contribution*
inside the sphere is outward acceleration 8 pi G DeltaV r/(3 c^2).
Wall and baryonic coupling stresses must be added for the full field; one
cannot infer its total mass by counting only the positive vacuum energy.
It does not supply the material rho_p proportional to 1/r^2 that gave an
attractive flat tail in MATERIAL_POOL_DERIVATION.md.

The matter coupling also produces a force:

    a_phi = -c^2 grad ln[1+epsilon q(phi/v)].

It vanishes deep in either constant phase and acts through a varying field,
especially at the wall. The thin-wall model therefore does not supply an
extended MOND force by this coupling either. Treating baryons as a prescribed
profile is an approximation; that new force requires a coupled stellar/gas
analysis before any viable galaxy claim.

## C. Could a conserved baryonic charge fix the inventory?

As a distinct possible closure, suppose a microscopic theory imposes exact
local neutrality q_b N_b+q_p N_p=0 with oppositely signed charges. Then

    Mp/Mb = -(m_p/m_b)(q_b/q_p).

That is a real mathematical mass-linking mechanism *if* the charge law,
neutrality, species and supply exist. It still requires particle masses and
charges. Baryonic mass includes stars and gas with multiple constituents;
one must specify what carries the proposed charge. An additional long-range
interaction and its constraints cannot be ignored. Nothing in the pool analogy
or the present scalar potential provides this law. This route is conditional,
not an adopted force or a derived mass ratio.

Even if the earlier pure-pool critical isothermal formula were provisionally
used, it would contain

    kappa_flat,formal=(4/1.1822265885)(Mp/Mb)
                      sqrt(Pext/(rho_DE c^2)).

Neither the charge ratio nor the phase-pressure ratio is fixed here. In the
baryon-loaded problem the original pure-pool critical coefficient itself must
be recomputed; substituting the charge relation into it is not a complete
solution. The finite surface velocity also remains distinct from an infinite
flat tail. No input was chosen to force kappa=1/2.

## Evidence, review, and route dispositions

baryon_phase.py: 27 checks pass, including six ODE solutions and symbolic phase,
wall and thermodynamic identities. The negative control reverses DeltaV in
the wall-pressure formula and fails exactly that derivative identity. Both
manifests are retained and validated; failed-control evidence is intentional.
The stable-boundary Plummer formula and inventory/charge arguments above are
analytic derivations, not outputs of the ODE experiment. Their derivatives,
dimensions, signs and limits were self-reviewed; no independent review claimed.
The cold material equations and the scalar wall calculation were not silently
merged into a single numerically solved theory.

Related literature check: the abstract of Hinterbichler et al.,
[Symmetron Cosmology](https://arxiv.org/abs/1107.2112), explicitly describes a
matter-density-dependent scalar coupling and the need for an additional
cosmological constant for its simplest potential. This is adjacent prior art,
not verification of this constructed potential or a novelty claim. No theorem
in this calculation relies on that abstract.

Route A: equilibrium-only inventory selection refuted for the stated inputs;
formation/particle exchange remains open. Route B: matter-supported phase
boundary established conditionally; pressure normalization and attractive
material production remain open. Route C: conditional charge closure identified;
no microscopic charge law or masses supplied. None derives the target.

Next discriminating work would require an explicit *new* microscopic reaction
or conserved-charge model that creates/supplies the material pool and fixes its
chemical potential, together with phase energies from that same theory. A
reservoir/coupling scan of the present model cannot answer that question:
those are independent parameters already visible analytically. Formation
simulations and a full coupled stability calculation are deferred until such
inputs are specified; they could test a model but cannot remove its free
normalizations by numerical effort alone. This is a documented selection gap,
not a proof that every possible pool theory is impossible.
