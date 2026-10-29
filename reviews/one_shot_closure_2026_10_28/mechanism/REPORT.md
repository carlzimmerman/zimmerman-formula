# Mechanism composition audit and a kinetic breathing reduction

Date: 2026-10-28. Owner: `/root/mechanism_closure`.
Requested base checkpoint: `44fd23a71c9888d9ea204c0ee832805829f9c090`.
The shared working tree advanced during this review, and the four principal
input directories are untracked. Therefore the base Git revision does **not**
identify their contents: `INPUT_PROVENANCE.json` records the actual SHA256
inputs and observed HEAD values. Writes are confined to this directory.

**Primary verdict on physical completion: incomplete, with the smallest missing
implication identified below.** The current files themselves correctly say that
they do not close the theory. There is a stronger obstruction to composing their
conditional successes: a mediator coupled only to total density and total
current cannot directly produce the random-energy exchange needed to turn the
constructed kinetic equilibrium into the assumed logarithmic material fluid.

There is also a useful positive result. The actual kinetic halo has a canonical
breathing reduction with potential `K0/a^2-2K0/a`. It has a global minimum and,
with the existing reciprocal outgoing outlet, converges for every negative-
mechanical-energy initial state of that reduction. This removes the previous
log-fluid reduction's inward collapse barrier. It does not select the starting
halo or prove that the full kinetic dynamics follows this reduction. The exact
Vlasov residual below proves that the latter implication fails in general.

The new analytic results were self-reviewed and independently reconstructed
by `/root/empirical_audit`; its separate review is retained by the coordinator.
They are not formally certified. The reviewer confirmed the force-trace,
closure mismatch, energy and Vlasov-residual algebra, and requested the wave
initial-data and bare-Newtonian scope qualifications now stated below.

## Target contract and the inherited dependency graph

The requested physical completion must derive, from one specified parent and
allowed initial data, a finite halo, its stress response and energy transport,
its selected amplitude and central state, and its normalization to one physical
gravitating vacuum. Adopted `kappa=1/2` and the canonical acceleration relation
are targets to be explained, not available derivations.

The actual existing chain is:

1. MC27 constructs a positive compact isotropic `f0(E)`, with finite moments and
   an exact inner equilibrium `p=A ln(rho/rho_ref)`; `A`, matching energy and
   central potential are free. This is an equilibrium statement.
2. MS27 assumes that pressure as a time-dependent fluid equation of state,
   proves a conditional radial mode is restoring, then damps that mode through
   a reciprocal mediator. Its boundary is fixed external pressure, not the
   full compact MC27 halo.
3. MP01 provides a local density-tracking parent for a density/current coupling
   and its compulsory kinetic companion. It leaves the medium EOS, couplings,
   finite-density-range health, field matching and static gradient cost open.
4. MC27's exact fixed-Lambda Vlasov scaling leaves the desired amplitude free.
   M6's latest separate closure checkpoint also remains undecided: it supplies
   neither a required cosmic population nor a calibrated forest response.

The missing arrow between 1 and 2 is a dynamical constitutive/transport theorem.
Writing down the equilibrium from 1 and attaching the outlet from 2 or 3 does
not prove that arrow. The following calculation tests that exact composition.

## A. Total-current couplings do not directly thermostat random kinetic energy

Consider nonrelativistic cold streams with positive mass densities `rho_b`,
velocities `v_b`, separately conserved masses, and finite moments. Put

    n=sum_b rho_b,       j=sum_b rho_b v_b,       u=j/n.

The smooth local matter Lagrangian is

    l=sum_b rho_b (|v_b|^2/2-Phi) + L0(n,fields) + j.A(n,fields).

Fields and their derivatives may appear in `L0,A`; there is no dependence on
individual relative stream velocities apart from the bare kinetic term.
For this theorem `A` does not depend independently on `j`; the uneliminated
MP01 tracker is sufficient. Gravity and any common scalar potential are allowed.
The kinetic metric is the ordinary mass metric. No relativistic multistream
limit or quantum-gradient closure is asserted.

Define `B0=partial_n L0+j.partial_n A`. Vary each conserved stream. Its momentum
and density derivative are

    p_b=v_b+A,
    delta l/delta rho_b=|v_b|^2/2-Phi+B0+v_b.A.

The displacement Euler equation is

    (partial_t+v_b.grad)p_b+(grad v_b)^T p_b
        =grad(delta l/delta rho_b).

Expanding and cancelling the velocity-gradient terms gives

    (partial_t+v_b.grad)v_b = E + v_b cross B,
    E=-grad Phi+grad B0-partial_t A,       B=curl A.                 (1)

`E` and `B` may depend self-consistently on the state; at a given point and
time they are the same for every stream. The same result follows directly for
characteristics of a Hamiltonian with a common scalar and vector potential.

Let `w_b=v_b-u`, `Pi_ij=sum rho_b w_bi w_bj`, `p=tr(Pi)/3` and
`q=(1/2)sum rho_b |w_b|^2 w_b`. Because `sum rho_b w_b=0`, the force contribution
to the random kinetic energy equation is exactly

    sum_b rho_b w_b.(E+v_b cross B)
      =sum_b rho_b w_b.(w_b cross B)=0.                           (2)

This requires neither isotropy nor a quiet mediator. Magnetic terms can rotate
the stress tensor, but they cannot change its trace directly. Consequently,

    D(3p/2)+(3p/2) div u+Pi:grad u+div q=0.                       (3)

At an instant with `Pi=p I`,

    Dp+(5/3)p div u+(2/3)div q=0.                                (4)

An additional collision operator conserving local random kinetic energy leaves
the trace equation unchanged. A collision operator that transfers random
energy to fields is outside the theorem and must supply its reciprocal ledger.

The density/current interaction used in MS27 is included explicitly:

    L_int=g n[n chi_t+j.grad chi],
    L0=g n^2 chi_t,       A=g n grad chi,
    B0=g[2n chi_t+j.grad chi].

For the uneliminated MP01 tracker, `A=h s grad chi`; its tracking potential
and `h s n chi_t` enter `L0`. Thus its natural total-current multistream
extension also obeys (2). This is an audit of that extension, not a claim that
MP01 had already derived a unique kinetic parent. Its material active-phase
label is constant on the inner plateau; the argument applies there regardless
of unresolved interface terms. Distinct stream-dependent labels/couplings
would change the hypothesis and require a new derivation.

The outlet can remove **collective** kinetic energy. It can also influence
random energy indirectly through changed strain, spatial transport, and
subsequent mixing. Equation (2) rules out only its use as an already supplied
local random-energy source. It does not prohibit a full nonlocal kinetic
mechanism or a different interaction involving velocity dispersion.

## B. An admissible compression immediately leaves the proposed log closure

Take any finite isotropic equilibrium `f0(r,v)=F(|v|^2/2+Phi0(r))` in the
compact MC27 family, and impose the arbitrarily small radial velocity boost

    f_H(r,v)=f0(r,v-Hr).                                         (5)

This is a canonical velocity shift generated by `H |r|^2/2`. It preserves
mass and all phase-space Casimirs, keeps density and central velocity moments
unchanged, and has finite energy for a finite halo. At the initial instant,

    u=Hr,       div u=3H,       Pi=p0 I,       q=0.

This is also admissible initial data for the stated nonrelativistic scalar
extension: take spatially constant `chi`, so the shared canonical vector
shift `A` vanishes, and keep the fields and their canonical momenta unchanged
while applying the matter boost. In the `g n^2 chi_t` case,
`pi_chi=chi_t+g n^2`; in the tracker case it is `chi_t+h s n`. Both offsets
are unchanged because `n,s` are unchanged. The real scalar has independent
initial position/momentum data, with no electromagnetic Gauss constraint;
the Newtonian Poisson constraint is unchanged because the mass density is
unchanged. This does not audit constraints of an unspecified relativistic
cold-field completion. A nonzero prescribed phase-space width is already
present in the equilibrium being perturbed.

The moment equations of the kinetic/current model therefore give exactly

    D rho=-3H rho,          Dp=-5H p0.                           (6)

A dynamical law `p=A ln(rho/rho_ref)` with fixed `A,rho_ref` instead requires

    Dp=-3H A.                                                   (7)

For every nonzero `H`, agreement requires `p0=3A/5`. In MC27's entire exact-log
inner interval, `0<x<=1`,

    p0/A=-ln x+2/3 >= 2/3 > 3/5.                                (8)

Thus the two derivatives disagree everywhere in that inner interval. This is
an exact counterexample to invariance of the log **material closure** under
the current-only kinetic dynamics; it is not merely a comparison between two
unrelated equilibrium states. A common field force cannot repair (6), even if
the finite tracker changes the static background, because it cancels in (2).

Equivalently, a canonical material dilation gives

    f_a(r,v)=f0(r/a,a v),
    rho_a(a r)=a^-3 rho0(r),       p_a(a r)=a^-5 p0(r).

Its kinetic compression modulus is `5p0/3`; the log-fluid modulus is `A`.
The ratio is at least `10/9` throughout the log interval, and at the center
of any quarter-core-contained member (`x_c<=1/4`) it is at least

    (5/3)(ln 4+2/3)=3.4216017... .                               (9)

The necessary exchange relation, if an extra random-energy source `Q` is
added to (3), is

    div q-Q=[3A-5p] div u/2.                                    (10)

For `q=0`, `Q=[5p-3A] div u/2`: compression of this inner family requires
energy loss, while expansion requires energy gain. Neither current coupling
nor locally energy-conserving Maxwellianization supplies this local source.
Equation (10), together with the traceless stress equation, is the exact
remaining constitutive obligation. Nonlocal flux is an allowed escape, but
must be derived rather than replaced by the equilibrium pressure curve.

## C. Positive continuation: a kinetically consistent breathing energy

Instead of assigning the kinetic equilibrium the log-fluid internal energy,
retain its actual finite kinetic and gravitational energies `K0>0,W0<0` and
moment of inertia `I0=integral rho0 |r|^2 d^3r`. Consider the canonical ansatz

    r=a X,       v=adot X+V/a,       a>0.                         (11)

For each fixed `a,adot`, this is symplectic and preserves all Casimirs. The
equilibrium has zero local mean velocity, so the bulk/random cross energy
vanishes. Its exact energy restricted to this family is

    E=(I0/2) adot^2+K0/a^2+W0/a.                                 (12)

Here gravity is Newtonian, no baryonic external potential or Lambda force is
included, and the full compact halo has a regular zero-pressure vacuum edge.
This is the bare kinetic/gravitational energy plus a separately chosen
collective boundary outlet. It is not the MP01 finite-tracker Hamiltonian:
that parent's static density-gradient energy and complete spatial coupling
would have to be retained in a derivation from it.
The integrated stationary moment equation gives `2K0+W0=0`: multiply Jeans
balance by position, integrate, and use the vanishing outer surface pressure.
Thus the reduced potential is

    V(a)=K0(a^-2-2a^-1),
    V(a)+K0=K0(1/a-1)^2.                                        (13)

It has a unique global minimum at `a=1`, diverges positively as `a->0`, and
approaches zero from below as `a->infinity`. The positive `a^-2` term is the
canonical compression of random velocities. It was absent from the previous
MS27 log-fluid radius model because that model used a different energy.

Attach the existing positive-energy half-line wave outlet to this collective
coordinate. With field action `T/2 integral(psi_t^2/c_chi^2-psi_x^2) dx` and
boundary `psi(0,t)=g(a(t)-a_ref)`, the no-incoming-wave solution gives

    I0 addot+V'(a)+Gamma adot=0,       Gamma=T g^2/c_chi>0,
    dE/dt=-Gamma adot^2,              dE_out/dt=Gamma adot^2.      (14)

The static field origin `a_ref` affects neither reaction nor energy. Compatible
constant prehistory supplies a constant zero-energy initial field; no abrupt
boundary-value jump or infinite-energy pulse is assumed. For nonzero initial
speed, that choice gives a finite-energy weak outgoing wave with a derivative
jump at the outgoing front. It is not a C1-compatible classical corner datum.
One may instead prescribe a smooth past history and include its initial wave
energy. The mechanical energy law for positive times remains (14). Incoming
waves would add a driving term and invalidate its monotonicity.

**Reduction theorem.** Every solution of (14) with `a(0)>0` and `E(0)<0`
exists for all positive times and satisfies `a(t)->1`, `adot(t)->0`.

Proof: Since `V<=E<=E(0)<0` and `V` diverges at zero and tends to zero at
infinity, `a` stays in a compact positive interval. Equation (13) bounds
energy below by `-K0`, and the kinetic term bounds `adot`. Hence the smooth
ODE extends for all times, and `integral_0^infinity adot^2 dt` is finite.
Bounded acceleration makes `adot` uniformly continuous, so `adot->0`: otherwise
uniformly sized intervals with nonzero speed contradict that finite integral.
Any accumulation point of `a` with `V'!=0` would give acceleration of one fixed
nonzero sign during a uniformly sized interval once speed is small, again
contradicting `adot->0`. Therefore every accumulation point is the unique
critical point `a=1`. This proves the claim.

The theorem concerns the declared collective-coordinate ODE. Six finite checks
include rest radii `0.55,0.8,1.2,3` and two nonzero-speed states, all with
negative mechanical energy. The normalization is `K0=1/2,I0=1,Gamma=0.4`.
The output gives the actual return and energy-ledger errors. Their convergence
does not replace the preceding analytical argument. The six final radius
errors are below `2.4e-14`; the largest absolute ledger error is `6.22e-13`
in the declared dimensionless units. All eight checks pass, and the bounded
run has status `completed`; its manifest passes current-input validation.

This is a better reduced basin than the previous frozen-shape log-fluid
example, and it uses the actual kinetic energy and zero-pressure full-halo
boundary. It still returns to the **chosen** halo: the column along the ansatz
is `Sigma(a)=Sigma0/a^2`, so the endpoint inherits arbitrary `Sigma0`.

## D. Exact residual: why the breathing reduction does not finish formation

Even with no outlet, (11) is not an invariant family for a general stationary
kinetic halo. Define `X=r/a`, `V=a v-adot r`, and the gravity potential
`Phi_a(r)=a^-1 Phi0(X)`. Direct substitution in the collisionless Vlasov
equation, using stationarity of `f0`, gives the exact residual

    R=[(a^-2-a^-1) grad_X Phi0-a addot X].grad_V f0.              (15)

For `f0=F(|V|^2/2+Phi0)` this is

    R=F'(E0) V.[(1-a) grad_X Phi0/a^2-a addot X].                (16)

Away from distribution-derivative cusps, the MC27 DF has `F'<0`. Since allowed
velocities contain all directions, a nontrivial breathing interval would
require `grad Phi0` proportional to `X` throughout the occupied region.
That is a harmonic interior force, equivalent through Poisson to uniform
density there. The MC27 compact log halo is not uniform. The cusps do not
rescue the ansatz: the nonzero residual already occurs on smooth open regions.

At a single instant `a=1,addot=0` the residual can vanish; this does
not make an interval of nontrivial evolution exact. Adding the outlet also
requires its spatial field and reaction, so its mode projection cannot by
itself remove the already explicit non-homologous residual. The next real
formation calculation must allow shape, anisotropy, heat flux and envelope
degrees of freedom. Equation (15) is a useful diagnostic for that calculation.

## Obligation matrix, route disposition and handoff

| Obligation | Result and status |
|---|---|
| Finite exact-log inner kinetic equilibrium | Inherited constructive MC27 proof; not rerun here |
| Total-current mediator directly exchanges random kinetic energy | Refuted under section A hypotheses by exact cancellation (2) |
| That equilibrium retains a material log closure under small breathing | Refuted for the stated current-only kinetic extension by (5)-(8) |
| Positive restoring kinetic radius energy with reciprocal damping | Proved for the explicit reduction (11)-(14); six finite checks support implementation |
| Reduced radius motion is exact Vlasov evolution | Refuted for this nonuniform halo by (15)-(16) |
| Nonlinear stability/formation of the full finite kinetic halo | Not addressed by the reduction; open |
| Vacuum-normalized amplitude and central-density selection | Open; inherited fixed-Lambda scaling survives this work |
| Cosmic population/forest closure | Outside this derivation; latest M6 checkpoint remains undecided |

The three executed routes have distinct outcomes: the composition route gives
a no-go for the claimed local closure within a specified interaction class;
the energy route gives a useful conditional reduced attractor; the exact-
substitution route locates the full kinetic obstruction to treating that
attractor as a formation proof. None is a new microscopic completion.

The most useful next move is to specify one actual mechanism outside the
current-only local theorem: a reciprocal relative-velocity interaction, a
derived nonlocal third-moment transport law, or a specified primordial state
whose evolution selects a different constitutive response. Derive (10) and
stress isotropization from it; then use the full finite halo and its real
energy, not the substituted fluid energy. Independently, that same parent
must break MC27's fixed-Lambda scaling and select `A` and the terminal central
state. The exact-log benchmark remains `A/(rho_Lambda c^2)=0.0023294580123`
only under the adopted canonical normalization and quarter-density convention.

No long job, external message, manuscript edit, commit or push was performed.
The write scope contains the report, actual input hashes, exact check code,
contract and bounded run. The only used external tools are local code and
filesystem tools; no unverified external theorem is a load-bearing leaf.
