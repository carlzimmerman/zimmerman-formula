# CD26-4 — conservative field transport and an action-derived density transition

**Result:** an explicit Cartesian field action supplies exact current transport,
conserved total stress, a cold wave limit with gradient stress, and a seeded
density transition with stable homogeneous end states. The transition is not
a derived Poisson decay law or a proof of halo evacuation. A bounded spatial
test actually retains more charge after the transition than the uncoupled
control. Conserved field
charge and energy cannot be removed by calling the configuration particle-free.

The common-action candidate uses the same physical metric and the campaign's
exponential carrier coupling. Its field kinetic coefficients are positive for
all finite gate values; uniform PDE control still needs gate bounds and the
full gravitational constraint analysis. No full nonlinear gravity, merger,
forest, or halo-clearing pass is asserted here. The operative target remains
filtered `nu_mono`, criterion B, with no new particle population assumed.

The constructive follow-through is in [CONVERSION.md](CONVERSION.md): a
different positive-square interaction with two complex fields and one real
field transfers conserved charge into an outgoing wave. It also admits a
global fixed-background energy-space continuation proof. Its five scalar
pairs, limited packet clearing and distinct parameter witnesses are explicit;
it does not erase the failed clearing advantage of the three-field route here.

## 1. What the previous transport lanes did and did not derive

The earlier `closure_doors_2026_09_26/transport/REPORT.md` found a genuine
crossing obstruction in a one-pair bounded-DBI fluid. Its Fisher follow-up
constructed a regular classical wave description through some crossings, but
showed why nodes and phase winding obstruct a global clock interpretation.
The `closure_push_2026_09_26/covariant_clock/RESULT.md` canonical complex field
adds a dynamical amplitude and proves a particular nonzero-charge homogeneous
clock branch. That branch is not an arbitrary-inhomogeneous clock theorem.
The IC27/28 bridge is a separate gravitational construction; its scalar and
constraint results are not imported into this field system.

L365 inserts a threshold, a probability `1-exp(-gamma H dt)`, a random direction
and a prescribed velocity kick. L377 retains this at lines 175–185 while adding
the phantom-inclusive trigger; its closing limitations explicitly say that the
trigger is posited without an action. L373 adds a uniform channel and a vacuum
gate at lines 171–189. L380 changes the clearing statistic and pool, not those
transport equations. These runs may use numerical tracers of a classical
field; the audit does not decide their ontology from the discretization. The
missing step is deriving their rates and momentum changes from a field action.

For a unit direction n, an imposed kick changes specific kinetic energy by
`Delta e=v_k v.n+v_k²/2`. An isotropic independent direction has mean change
`v_k²/2`; no compensating reservoir is evolved in those kick lines. A
conservative replacement must include that energy and momentum elsewhere.
No costly prior simulation was rerun for this audit.

## 2. A regular Cartesian field action

First derive the matter block on a prescribed physical metric, signature
`(-,+,+,+)`, with `c=hbar=1`. Write `R²=phi1²+phi2²` only as shorthand; the
fundamental fields are Cartesian `phi1,phi2,s`, all with canonical kinetic terms:

    L0 = -1/2 sum_A (grad phiA)² - 1/2 (grad s)² - V(R,s),
    V = m²R²/2 + lambda_R R⁴/4 + mu²s²/2 + lambda_s s⁴/4 - g²R²s²/2.

Assume `m²,mu²>0`, `lambda_R,lambda_s>0`, `g²>0` and
`lambda_R lambda_s>g⁴`. The exact square completion is

    V = m²R²/2 + mu²s²/2
        + lambda_s [s²-g²R²/lambda_s]²/4
        + [lambda_R-g⁴/lambda_s] R⁴/4 >= 0.

Thus the potential is coercive and bounded below. The velocity Hessian is
identity, with no ghost, pole or polar-coordinate singularity at `R=0`.
The three principal scalar operators are the physical metric wave operator.
The potential is deliberately not convex everywhere: its desired transition
has a negative mass eigenvalue on the unstable branch. A bounded potential
and positive principal kinetic terms do not forbid such an instability.

The exact equations are

    Box phiA - (m²+lambda_R R²-g²s²) phiA = 0,
    Box s - (mu²+lambda_s s²-g²R²) s = 0.

There are three independent scalar canonical pairs. Without `s`, the complex
field has two; no quantum particle states, quantization or relic abundance
are assumed. Independent classical field initial data remain. This report does
not identify the complex phase with the gravitational foliation clock.

## 3. Exact current, stress exchange and momentum transport

For rotations of `(phi1,phi2)`, choose the future charge orientation

    j^mu = phi2 grad^mu phi1 - phi1 grad^mu phi2,
    div j = 0.

On `phi1=R cos(theta), phi2=R sin(theta)`, it is
`j^mu=-R² grad^mu theta`, so `j^0=R² theta_dot`. This polar expression is only
a local chart; the Cartesian current is valid also at zeros. The exact total
stress tensor is

    T_mn = sum_A d_m phiA d_n phiA + d_m s d_n s
           - g_mn [1/2 sum_A (grad phiA)² + 1/2 (grad s)² + V],
    nabla_mu T^mu_nu = 0.

For an explicit exchange convention, split `V=V_phi+V_s+V_int`, with
`V_int=-g²R²s²/2`, and use the bare complex/real stress tensors. Then

    div T_phi = -g² s² R dR,
    div T_s   = -g² R² s ds,
    div(-g V_int) = +g² s² R dR + g² R² s ds.

The sum vanishes. Assigning interaction stress to one component changes the
individual exchange convention, not total conservation. In flat coordinates,
with flux `F_i=-sum dot(field) d_i(field)`, energy obeys

    partial_t E + div F = 0,
    E = 1/2 sum [dot(field)²+|D field|²] + V.

The bare homogeneous balances are

    Ephi_dot = g²s² R Rdot,
    Es_dot = g²R² s sdot,
    Vint_dot = -Ephi_dot-Es_dot.

The exact momentum density is `P_i=-sum dot(field) d_i(field)` and its flux is
the spatial stress `T_ij`; `partial_t P_i+partial_j T_ji=0`. In curved spacetime
these are components of the covariant conservation law, not a globally
conserved coordinate energy on an arbitrary expanding background.

## 4. The actual common-action interface

The minimal block above is **not** silently substituted into L361's
carrier-invisible force law. The historical L361 rewrite has carrier potential `Phi-Z`, with
`Z=f(psi-chi)` and Phi the physical baryon potential. The main projected host
changes that regional construction: its independent auxiliary `Z_raw` enters
through `z=Z_raw-<Z_raw>_h`, and the carrier potential is `Phi-z`. In the
transport displays below, uppercase Z denotes that physical projected z,
not a reimposition of the historical regional constraint. The selected
completion is, for all three fields,

    Ld = A K - B W,
    A=exp(Z), B=exp(-Z),
    K=1/2 sum(n.grad field)²,
    W=1/2 sum|D field|²+V.

Here `n` is the independently specified physical unit foliation normal;
`D` is its spatial derivative. Equivalently the scalar kinetic tensor is
`C^mn=B h^mn-A n^m n^n`, and the equations are
`nabla_m(C^mn d_n field)-B V_field=0`. This uses a composite carrier lapse
`N_d=N exp(-Z)` with the same spatial metric. It does not add an independently
varied second metric or identify the field phase with the foliation.

At fixed composite Z, the physical lapse density and gate derivative coincide:

    rho_d = A K+B W = partial Ld/partial Z >= 0.

Both coefficients are positive for every finite Z, and the scalar speed
relative to the physical foliation is `c_d²=B/A=exp(-2Z)`. Criterion B does not
by itself reject a speed exceeding one. It still requires an appropriate
initial-value formulation. As `Z` becomes unbounded, no uniform coercivity or
uniform speed bound follows from pointwise positivity alone.

In a unit-lapse, zero-shift flat chart with possibly varying Z, the exact
current and equations are

    n_charge=A(phi1 phi2_dot-phi2 phi1_dot),
    J_i=-B(phi1 d_i phi2-phi2 d_i phi1),
    partial_t n_charge+div J=0,
    partial_t(A field_dot)-div(B D field)+B V_field=0.

They give the local energy identity

    partial_t rho_d + div[-B sum field_dot D field]
       = -A_dot K + B_dot W = -Z_dot rho_d.

A fixed spatial gate changes forces without an external time-energy input;
a time-varying gate exchanges energy with its defining fields/constraints.
The **whole** action must supply the opposite exchange. Treating a changing
Z as a prescribed field would reintroduce a reservoir external to this block.
The action lane retains the full Z, metric and foliation variations. The
minimal stress formula in section 3 must not be used as the physical stress
of this nonminimal block without those variations.

For constant Z, rescale time by `tau=exp(-Z)t`. Every canonical field equation
below is then recovered exactly; charge is unchanged, energy is multiplied
by `exp(-Z)`, and frequencies/speeds in physical t acquire `exp(-Z)`.
No cosmological Z evolution is inferred from this frozen identity.

## 5. Cold limit and the stress missed by a dust closure

For the canonical block let
`calPhi=(phi1-i phi2)/sqrt(2)=exp(-i m t) psi/sqrt(2m)`, `n=|psi|²`.
The exact envelope equation is

    i psi_dot = -Delta psi/(2m)
                + [lambda_R n/(2m²)-g²s²/(2m)] psi
                + psi_ddot/(2m).

Dropping the last term requires a slow envelope. The retained equation is a
classical nonlinear Schrodinger approximation, not a particle assumption.
Its exact approximate-theory charge density is n; the relativistic current
has envelope-time corrections, so this n is not its exact density outside
the slow-envelope limit. Include a weak gravitational carrier potential
`Phi_eff` as `m Phi_eff psi`; the common-action weak-field construction uses
`Phi_eff=Phi-Z`, subject to that action's normalization.

On a node-free chart, `psi=sqrt(n) exp(i S)`, `v=DS/m`, `rho=m n` give

    rho_dot + div(rho v) = 0,
    partial_t(rho v_i) + partial_j(rho v_i v_j+p delta_ij+Q_ij)
       = -rho d_i Phi_eff + [g² rho/(2m²)] d_i(s²),
    p=lambda_R n²/(4m²),
    Q_ij=[(d_i rho d_j rho)/rho-d_i d_j rho]/(4m²).

The quantum/gradient stress is a derived spatial-field stress. Removing it is
an additional long-scale approximation; after interference or near a node,
that approximation can fail even when the underlying Cartesian fields are
regular. The full relativistic theory supplies finite characteristic speeds;
the Schrodinger approximation is not a fundamental arbitrarily-high-k law.

The cold domain requires `k/m << 1`, slow envelope frequency relative to m,
`lambda_R R²/m² << 1`, `g²s²/m² << 1`, small velocity, and gradient pressure
small on the chosen resolved scale. No single perfect-fluid pressure law is
assumed to encode arbitrary multistream stresses. Since the force from s is
`toward increasing s²`, this attractive interaction does **not** automatically
push carrier charge out of a high-s region.

## 6. An action-derived trigger and its stable end branch

Consider a homogeneous circular solution on fixed Minkowski space,
`R=R0`, `theta=Omega t`, `s=0`, with

    Omega²=m²+lambda_R R0².

The real-field fluctuation has

    omega_s²(k)=k²+mu²-g²R0².

The branch becomes unstable precisely when `g²R0²>mu²`; modes with
`k²<g²R0²-mu²` grow at rate `sqrt(g²R0²-mu²-k²)`. This is a calculated
amplitude threshold and band. It is not the repository's geometric
`x_tilde>5` trigger, not a fitted `Gamma=10H`, and not a monoenergetic kick.
The fastest linear growth is at k=0, not a preferred nonzero kick momentum.

**A classical seed is essential.** `s=0, s_dot=0` is an exact invariant
solution even above threshold. Classical deterministic equations do not
spontaneously select a fluctuation distribution. Spatial seeds and their
initial spectrum are physical initial data.

Above threshold the rotating broken branch has

    s0²=(g²R0²-mu²)/lambda_s,
    Omega²=m²+lambda_R R0²-g²s0².

For radial `chi`, phase `z=R0 delta theta`, and `sigma=delta s`, the quadratic
Lagrangian has canonical kinetic/gradient terms, gyroterm `2Omega chi zdot`
and mass matrix on `(chi,sigma)`

    M=[[2lambda_R R0², -2g²R0s0],[-2g²R0s0, 2lambda_s s0²]],
    det M=4R0²s0²(lambda_R lambda_s-g⁴)>0.

Both diagonal entries are positive. The Hamiltonian is a sum of
`(p_z-2Omega chi)²/2`, the other kinetic/gradient squares, and the positive
mass form. Thus this frozen branch has positive energy and real nonnegative
squared frequencies; nonzero k removes the homogeneous phase zero mode.
This argument covers every k for that constant background, not just the four
sampled normal-mode checks. It is not the full gravitational perturbation
Hamiltonian or stability through every possible time-dependent transition.

## 7. Unique homogeneous radial ground state at fixed charge

There is a stronger constructive statement than a one-tangent fit. Put
`u=R²>0`, fixed charge magnitude `q>0`, and `u_t=mu²/g²`. Minimizing s at each u
reduces the homogeneous charge-constrained energy to

    E0(u)=q²/(2u)+m²u/2+lambda_R u²/4,                 u<=u_t,
    E1(u)=q²/(2u)+m_eff² u/2+lambda_eff u²/4-mu⁴/(4lambda_s), u>u_t,
    m_eff²=m²+g²mu²/lambda_s,
    lambda_eff=lambda_R-g⁴/lambda_s>0.

The two pieces and their first derivatives join. Their second derivatives are
`q²/u³+lambda_branch/2>0`. The reduced energy is strictly convex and coercive
at u=0 and infinity, hence has exactly one radial minimizer. The two signs
of a nonzero s and the overall complex phase remain symmetries. The broken
minimum occurs exactly when

    q>q_crit=u_t sqrt(m²+lambda_R u_t).

On it `q²=u²(m_eff²+lambda_eff u)`, a strictly increasing function of u.
This fixes an action-derived **charge-density** threshold. Translating it to
the repository's geometric/environment trigger needs a derived relation
between local charge and that geometry, not a naming substitution.

The adiabatic broken-branch pressure and sound speed are

    p=lambda_eff u²/4+mu⁴/(4lambda_s),
    c_s²=lambda_eff u/(2m_eff²+3lambda_eff u),  0<c_s²<1/3.

This integrating-out limit applies below both radial/real-field gaps. At the
transition the real-field gap vanishes, so it cannot be used as one uniform
single-fluid theory through the threshold. A constant Z multiplies the fixed
charge energy by exp(-Z), preserves the minimizer and q_crit, and multiplies
physical squared sound speeds by exp(-2Z).

## 8. Energy available for a slow outflow is not an outflow calculation

At fixed R, the largest potential decrease obtained by changing s from zero
to a minimum is

    Delta V_R=(g²R²-mu²)²/(4lambda_s),  R²>u_t.

It is a fixed-R landscape budget, **not** a maximum over a freely changing
R trajectory or a proof that this energy becomes carrier kinetic energy.
On the initial circle `q=Omega R²`. If a fraction eta_transfer were converted
into nonrelativistic carrier motion, an energetic necessary budget is

    v²/2 <= eta_transfer Delta V_R/(m q).

With `eta=g⁴/(lambda_s lambda_R)<1`,
`epsilon=lambda_R R²/m² << 1`, and `r=mu²/(g²R²)<1`, the available ratio is

    Delta V_R/(m q) = eta epsilon (1-r)²/[4 sqrt(1+epsilon)].

For ideal unit efficiency, `v/c≈0.002` requires approximately
`eta epsilon(1-r)² >= 8e-6`. An exact rational cold witness uses
`m²=R²=lambda_s=1`, `lambda_R=1/10000`, `g²=1/125`, `mu²=1/250`.
It has positive quartic margin `9/250000`, `Delta V_R=1/250000`,
`q=sqrt(10001)/100`, and ideal budget speed `0.0028283564`.
This is an unfitted dimensionless energy comparison. Transfer efficiency,
spatial spectrum, outgoing flux, recapture and cosmological normalization
have not been calculated from it.

U(1) charge remains in the complex field because s is neutral. Energy can
leave a region as s radiation or complex-field waves, but charge evacuation
requires an actual outward charge flux. Homogeneous energy exchange alone
cannot accomplish it. Adding a second charged field could exchange charge
between species, at the cost of further pairs; it still would not destroy
total charge or derive random kicks without a spatial calculation.

## 9. Reversibility, nodes and the global-health boundary

An autonomous conservative Hamiltonian evolution is reversible. For a
velocity-even state observable F, its derivative changes sign under reversing
all momenta. Therefore a strictly one-way law `Fdot=-Gamma F`, with fixed
positive Gamma throughout both time-reversed states, cannot be an exact
closed description of those states unless the derivative vanishes. Outgoing
radiation, a continuum bath, coarse graining or selected boundary conditions
can yield an effective decay law. Each needs a derivation and an energy ledger.
This does not forbid local dispersal in an infinite conservative field system.

The finite homogeneous control below grows from a seed and reverses accurately;
it does not approach an irreversible deleted-carrier state. Its energy and
charge are bounded, and the coercive polynomial gives global homogeneous ODE
existence. Those facts do not establish global smoothness of the coupled
inhomogeneous gravitational system or uniform bounds on its lapse/gate.

Cartesian regularity also does not make the phase a timelike clock. Already
in the free complex field, the exact solution

    calPhi=exp(-i omega t)[A exp(i kx)+B exp(-i kx)],
    omega²=m²+k², A>B>0,

is node-free, but its phase gradient is spacelike at destructive interference
when `k(A+B)>omega(A-B)`. The checked example `A=1,B=3/4,k=m=1` satisfies this.
At A=B there are actual nodes. The full Cartesian field stays regular in both
controls. The gravitational foliation must therefore have its own admissible
domain and evolution proof; it cannot simply be declared to be this phase.

## 10. Spatial test of whether the transition helps clearing

The new finite-difference Hamiltonian test evolves the exact Cartesian field
equations on a prescribed flat metric, frozen `Z=0`, without gravity. This is
a controlled slice of the exponential matter block. It cannot test the full
auxiliary gate, gravitational recapture or cosmological matching.

Use a periodic box of length 128, `m²=1,mu²=.5,lambda_R=lambda_s=2`,
`R(x)=.1+.9 exp[-(x/12)^8]`, initial `phi1=R,phi2=0`, velocities
`phi1_dot=0,phi2_dot=sqrt(3)R`, and `s=.001 exp[-(x/12)^8],s_dot=0`.
Compare `g²=1` against `g²=0` with the same initial fields and charge. The
stored initial gradients, coherent rotation and real-field seed are paid
initial energy; they are not energy created by the transition. Switching the
interaction changes the initial Hamiltonian by its explicitly accounted
`-g²R²s²/2` term. This strong-interaction numerical control is not the cold
parameter witness of section 8.

The spatial discretization derives from the positive discrete gradient
energy. Velocity Verlet evolves its Hamiltonian. Let
`I_(j+1/2)=(phi1_j phi2_(j+1)-phi2_j phi1_(j+1))/dx`; the exact semidiscrete
charge equation is `qdot_j=(I_(j+1/2)-I_(j-1/2))/dx`, with physical flux `J=-I`.
Accumulating the boundary flux through both Verlet half kicks exactly
accounts for the change in charge of the fixed region `|x|<10` up to rounding.
This is a local transport test, not merely global conservation.

At time 30 the retained fraction of initial region charge is:

| N | g²=0 | g²=1, seeded transition | extra retention from transition |
|---:|---:|---:|---:|
| 256 | .5016945633 | .5078707681 | .0061762048 |
| 512 | .4987585853 | .5050178755 | .0062592902 |
| 1024 | .4980246516 | .5043066061 | .0062819545 |

Successive resolution differences shrink by factors 4.0003 and 4.0110 for
the two branches. Finest-grid energy drift is at most `6.82e-6`; global charge
error is at most `2.27e-14`; the local boundary-flux ledger error is below
`2.73e-15` relative to initial region charge. The transition grows to
`max|s|=.72397`, versus `.001296` without coupling. Thus growth and conservative
energy transfer occur, but **this packet clears less efficiently**. This
agrees with the attractive force toward increasing s² derived in section 5;
it is a scoped negative result for this potential and initial packet, not a
no-go theorem for other interactions or spatial data.

The exact zero-seed control has identical complex-field evolution for both
couplings. Raising the seed to .01 at N=512 changes retained fraction to
`.5102621`; seed data matter. An independent complex-coordinate integrator
and fixed-grid half-timestep audit are recorded separately, together with
the complete initial-energy ledger.

## 11. Evidence and the remaining discriminating calculation

`run_001` accepts 41 exact/finite controls. The homogeneous run uses
`m²=1,mu²=.5,lambda_R=lambda_s=2,g²=1`, initial
`(phi1,phi2,s)=(1,0,.001)`, velocities `(0,sqrt(3),0)`, times 0–60,
3,001 sampled outputs, DOP853 rtol `2e-12`, atol `2e-13`. It reaches
`max|s|=0.7313133`, relative energy error `9.67e-11`, relative charge error
`8.06e-11`, and time-reversal maximum error `3.63e-8`. The exact unseeded
control stays at s=0. A separate broken-branch witness has three positive
frequency squares at sampled nonzero `k²=.01,1,100`; the all-k argument above
uses its Hamiltonian instead of extrapolating those samples.

`run_charge_001` separately checks eleven exact fixed-charge transition,
pressure and sound identities. The Lean file certifies thirteen stated
algebraic positivity/conservation/threshold bridges, not variational calculus,
PDE evolution, a full gravity theory or halo clearing. Accepted source/run
hashes and validator results are in `EVIDENCE.md`. Failed or superseded runs,
if any, must remain separate from accepted evidence.

`run_spatial_001` records the spatial control, both conservation ledgers,
refinement, zero-seed and seed-size controls. `run_spatial_energy_001` records
the independent coordinate implementation, timestep check and explicit
initial energy accounting. Neither imports an empirical decay or kick.

The next discriminating test is a spatial evolution with **dynamically varied
gate/auxiliary equations and gravity**, stated cold
initial charge and seed spectrum, and measured inward/outward current and
energy flux. Compare its derived coarse-grained transport against the
specific L373/L380 prescription. The present exact construction makes that
test concrete. Its simpler spatial control gives no clearing advantage, so
the present potential should not be advertised as an evacuation solution.
