# FGF046 independent root audit

Primary verdict: **proved as written**, in the auxiliary fixed-potential fluid
class and local physical-patch scope stated in the root candidate.

Claim audited: for each fixed smooth hydrostatic background on a regular
positive-side neighborhood of the prescribed x*, and fixed positive c, nref,
L, v0, the exact compact C1,1 velocity V f((x-x*)/ell), with V=v0 N,
ell=L/N^3 and f=(1-y^2)^2 on |y|<1, zero elsewhere, has a positive C1 fluid
evolution. After a fixed hydrostatic extension to the line the solution is
bounded C1, uniformly C1,1 in space on each compact existence interval, unique
in the bounded-gradient classical class, and exists at least through the
explicit time (2). This gives a lower bound k0 N^-4. Its restriction to
interior characteristic cones is independent of exterior data/force choices.
For the maximal constructed auxiliary branch, bounded first gradients suffice
for continuation. The pinned FGF045 obstruction then gives a finite maximal
time between k0 N^-4 and B L/(v0 N^4), with unbounded first-gradient limsup
localized in the regular physical patch. Exact fluid energy balance and
compactly supported relative-energy conservation hold before that endpoint.

## Revision, exposure, and checks

- Auditor: `/root/fgf046_root_audit`, a separately dispatched proof-audit agent.
- Root SHA256: `79bb774b90b1dd381ad65836a380c775307e69ad6b3202ac985cf1691db01037`.
- PROOF_RECORD.json SHA256: `7d95ef893f5c32524edf5282699c8c43673301496a97492fba820d2d56183bf5`.
- All nine input hashes recorded in PROOF_RECORD.json matched their current
  bytes, including the task, FGF045 proof/reconciliation and corrected old root.
- No new stage33 author/reviewer proof or conclusion was read. The mathematical
  sources read were the root candidate, FGF046 task, pinned FGF045 author proof
  and reconciliation, and pinned stage32 root plus its correction. Framework
  and result-contract instructions were also read. Other pinned files were
  byte-hashed where their contents were not needed.
- The root explicitly admits an author route preview before its file freeze.
  This audit does **not** describe the root as a blinded frozen derivation.
  Independence of this audit is procedural, not evidence by agreement.
- Administrative commands: `cat`/`rg`/`ls` for permitted instructions and
  artifacts, `shasum -a 256` for the root, and Python standard-library
  `hashlib`/`json` for pin checks and report serialization/validation. There
  were zero mathematical executable computations, no numerical experiments,
  network requests, services, installations, commits, or outside writes.

## Dependency graph and obligation matrix

The dependency chain is: smooth positive hydrostatic patch -> fixed smooth
hydrostatic auxiliary extension -> exact-data linear characteristic iteration
-> uniform C1,1 bounds plus C0 contraction -> C1 classical limit -> uniqueness
and cone localization -> first-gradient-controlled higher regularity ->
finite-endpoint trace/restart -> maximal auxiliary branch -> pinned FGF045
upper obstruction -> localized first-gradient divergence. Fluid energy is an
independent algebraic consequence of the constructed equations.

| Obligation | Status | Decisive evidence |
|---|---|---|
| Exact profile and hydrostatic extension | Passed | f' is continuous, f'' is bounded a.e.; cutoff acts on background only |
| Linear flow existence/invertibility | Passed | Bounded speed, spatial Lipschitz coefficient, positive bounded Jacobian |
| First- and second-derivative iteration bounds | Passed | Equations (3)-(4), with TPbar<=1/8 |
| Actual C0 contraction | Passed | Difference source bounded by Pbar times preceding difference |
| C1 limit and exact trace | Passed | Square-root interpolation makes derivative increments summable |
| Positive-density fluid reconstruction | Passed | Exponential reconstruction and both Riemann equations |
| Explicit lifespan and dimensions | Passed | P0=O(N^4), Q0=O(N^7), but only P* enters time gate |
| Uniqueness and exterior independence | Passed | Difference integral inequality on contained backward cones |
| Hydrostatic control/finite propagation | Passed | Stationary extended solution and local uniqueness |
| First-gradient bound implies Q bound | Passed separately | Characteristic difference-quotient reconstruction below |
| Finite-endpoint trace and restart | Passed separately | Uniform time-Lipschitz estimates for U and U_x |
| Maximal branch/upper bound/gradient divergence | Passed | Uniqueness, restart, pinned FGF045, compact disturbance |
| Local and relative energy | Passed | Pressure/force cancellation; actual boundary terms retained |
| Coupled gravity or post-breakdown solution | Out of scope | Frozen-field residual remains; no such theorem claimed |

Leaves are internal analytic derivations, exact definitions/conventions, and the
hash-pinned FGF045 local obstruction. No literature existence, continuation,
shock, or transport-regularity theorem is supplied as an unchecked leaf. The
old root's withdrawn endpoint classification is not used as a premise.

## Reconstruction of construction and limit

Write U=(R,S), a=(R_x+S_x)/2, lambda_i=(R+S)/2 +/- c. For a bounded
C1 spatial velocity with bounded derivative, Picard iteration of its integral
ODE has factorial error bounds, hence a unique complete flow on the proposed
finite slab. Differentiating in the initial label gives J'=lambda_x J,
J(0)=1. Consequently J>0, J and 1/J are bounded, and bounded displacement
makes the flow onto the line. The characteristic source integral defines the
next U. Its first derivative is continuous; Lipschitz data derivatives and
Lipschitz coefficient derivatives preserve spatial Lipschitz derivatives.
This last assertion can be checked by finite differences of the formula for
U_x, without assigning values to f'' at its two joins.

For the next iterate, p=U_x obeys along the frozen flow

    D_m p = -lambda_x^m p - g_e'.

Thus P_next <= (P0+tF1) exp(Pbar t). Differentiating by spatial difference
quotients gives the a.e. second-derivative equation

    D_m z = -2 lambda_x^m z - lambda_xx^m p - g_e''.

Equivalently, compare the p formulas on two nearby frozen characteristics;
the variation of lambda_x is bounded by Qbar times their separation. This
yields precisely (Q0+tF2+t Qbar Pbar) exp(2Pbar t). The constants check:
T Pbar<=1/8, 2T Pbar<=1/4, Q0+TF2<=Q*=Qbar/4, and
(1/4+1/8)exp(1/4)<1. The base iterate obeys all three bounds. If Q*=0,
bounded affine initial data and bounded affine force are spatial constants,
and the zero-second-derivative special case is consistent.

For m>=1, the difference equation uses the m-th velocity, has zero initial
data, and has source -(lambda^m-lambda^(m-1)) U_x^m. The map U->lambda_i
has max-component Lipschitz constant one, so the slab contraction constant
is <=T Pbar<=1/8. The first increment is bounded. No contraction in the
derivative norm is claimed or needed.

For each spatial scalar increment d, Taylor's integral formula and
Lip(d_x)<=2Qbar give

    |d_x| <= 2||d||inf/h + Qbar h.

Minimization yields 2 sqrt(2Qbar ||d||inf); hence the geometric C0 increments
give a summable series of first-derivative increments with ratio sqrt(1/8).
This is uniform in t,x for each fixed N, although its prefactor may grow with
N. Integration in x identifies the limiting derivative. The equations make
the time derivatives converge uniformly too, and integration in t identifies
the time derivative. Both are continuous. The limit therefore solves the
equations pointwise with the exact, unsmoothed trace and retained spatial
C1,1 bound. The exponential for n is strictly positive. Adding/subtracting
the two Riemann equations yields q_t+v q_x=-v_x and
v_t+v v_x+c^2 q_x=-g_e, which recover both requested fluid equations.

More explicitly, with d=8/(3 sqrt(3)),

    P0 <= d(v0/L)N^4 + c||q_e'||inf,
    Q0 <= 8(v0/L^2)N^7 + c||q_e''||inf.

The bound on Q0 uses f''=-4+12y^2 inside its support and zero outside;
the jumps at +/-1 do not produce derivative atoms because f' is continuous.
For N>=1 let A=d v0/L and D=c||q_e'||inf+tau F1+1/tau. Then
P*<=(A+D)N^4, so k0=min(tau,1/[16(A+D)]) is one admissible positive
lower constant in T>=k0 N^-4. All added terms in P* have inverse-time
units. This is an analytic lower bound, not an evaluated sharp lifespan.

## Separate audit of Q propagation from P

This is load-bearing: keeping the initial iteration's fixed Qbar alone would
not justify a maximal-endpoint classification. On any compact interval of the
constructed branch, set P(t)=max_i||U_i,x(t)||inf and
Q(t)=max_i Lip_x(U_i,x(t)). Both are finite there by local construction.
Let p_i=U_i,x. Along its own characteristic family,

    d p_i(t,X_i)/dt = -a(t,X_i) p_i(t,X_i)-g_e'(X_i).

Compare two distinct labels in this same family. Their distance D(t) stays
positive and satisfies |D'|<=P D. Their gradient difference E satisfies the
upper absolute-value inequality

    E' <= P E + (P Q+F2)D.

Indeed |a|<=P, |p_i|<=P, and Lip(a)<=Q. Therefore W=E/D satisfies

    D^+ W <= 2P W + P Q + F2.

The upper derivative notation accommodates zeros of E; the integrated
inequality follows directly by the integrating factor. Taking the supremum
over pairs and both characteristic families gives, with I(t)=integral_0^t P,

    Q(t) <= Q(0)e^(2I(t))
          + integral_0^t (P(s)Q(s)+F2)e^(2[I(t)-I(s)]) ds.

Apply the scalar integrating-factor/iterated integral inequality to
e^(-2I)Q. It gives

    Q(t) <= e^(3I(t)) [Q(0)+integral_0^t F2 e^(-3I(s)) ds]
          <= [Q(0)+F2 t]e^(3I(t)).

This is also the bound obtained by the root's a.e. equation
D_i U_i,xx=-2a U_i,xx-a_x p_i-g_e''. It verifies its factor 3 and does not
use a pointwise value of U_xx at a transported join. The root's integral
version (6) is justified by integrating that bounded a.e. transport equation;
the pairwise derivation supplies an equivalent regularity-safe route to its
stated bound. These arguments only use already finite Q on compact local
intervals, then bound it uniformly when P is bounded on a finite full horizon.
There is no circular assumption of the desired endpoint Q bound.

## Restart, maximality, and localization

Suppose the branch ends at t*<infinity and P is bounded on [0,t*). Along
characteristics |U|<=U0+t*F0, so speed is bounded by M=U0+t*F0+c. The
preceding estimate gives a uniform Q bound. Comparing a value at (t,x) with
its backward characteristic at time s gives

    ||U(t)-U(s)||inf <= (M P+F0)|t-s|,
    ||U_x(t)-U_x(s)||inf <= (M Q+P^2+F1)|t-s|,

where the right-hand P,Q denote uniform bounds. The second estimate follows
from the first-gradient ODE and the spatial Q bound, so it does not require
a classical mixed second derivative. Thus U and U_x have uniform limits at
t*. Integrating in x identifies the trace derivative; it is Lipschitz with
the same bound. The trace is admissible C_b^{1,1} data. Equations (2)-(5),
with time reset, construct a further positive interval. The left/right time
derivatives agree by the PDE at the trace. Uniqueness patches the solutions.
This verifies both the conservative three-norm gate and the stronger P gate.

Unions of compatible intervals give the maximal auxiliary branch, with finite
norms on each compact subinterval. Uniqueness follows from the exact
difference equation and an iterated integral inequality; no small-time
condition is needed for uniqueness. On a shrinking cone whose inward sides
outrun both solutions' characteristic speeds, the same inequality has no
lateral-data term. This proves exterior independence only on its stated
common cones, which is the needed local meaning.

The stationary pair (R,S)=(c q_e,-c q_e) satisfies both extended equations
because g_e=-c^2 q_e'. Comparing it to U on backward cones gives exact
equality outside the expanding cone of the original velocity support. On a
fixed horizon H containing B L/(v0 N^4), all auxiliary speeds are bounded
by C_N=U0+HF0+c+epsilon_v=O(N). The disturbance cone has radius at most
ell+C_N B L/(v0 N^4)=O(N^-3), so it is contained strictly in the regular
patch for sufficiently large N. The FGF045 comparison cone is also contained
in the same physical patch, and its hypothesis is met if the auxiliary branch
survives through the comparison endpoint. Its pinned contradiction therefore
implies tmax<=B L/(v0 N^4). No old claim of existence was imported.

If P stayed bounded up to this finite tmax, restart would contradict
maximality. Hence limsup P=infinity. Outside the disturbance cone the solution
equals the fixed smooth background, whose gradient has a fixed finite global
bound. All divergent gradients must consequently occur inside the regular
patch; a distant cutoff cannot be their source. The invariant bounds give
finite-N upper and strictly positive lower density bounds even as t approaches
tmax. This establishes precisely the claimed first-gradient classification,
not a jump profile, entropy continuation, or a theorem at the excluded cusp.

## Energy, controls, and remaining scope

Set e=c^2 n(log(n/nref)-1), p=c^2 n. Multiplying the actual momentum equation
by nv and using continuity gives

    K_t+(vK)_x=-v p_x-nv g_e,
    e_t+(ve)_x=-p v_x,
    (n phi_e)_t+(nv phi_e)_x=nv g_e.

Their sum is exactly the root's H_t+Q_energy,x=0. These products require
only C1 regularity and positive density. Here Q_energy is the energy flux,
distinguished from the Lipschitz norm Q above. Subtracting the static
background and mu times mass balance gives

    Erel = nv^2/2+c^2[n log(n/rho_e)-n+rho_e],
    Frel = nv[v^2/2+c^2 log(n/rho_e)].

Both relative fields vanish outside the compact disturbance cone. Integration
on a fixed interval containing that cone yields conserved relative mass and
energy without an infinite background integral. At time zero Erel integrates
to (V^2 ell/2) integral_{-1}^1 rho_e(x*+ell y)f(y)^2 dy=O(N^-1).
Fixed boundaries have the usual flux difference; moving boundaries additionally
have Reynolds terms. The hydrostatic zero-velocity control has zero current.

No failed mathematical implication was found, and no correction was made to
the frozen root or PROOF_RECORD. There is no remaining gap for this scoped
fixed-potential classical construction. The strongest safe conclusion is the
claim card above. Coupled field evolution, the source residual
4pi G_Newton(n-rho), evolving-H dynamics, post-breakdown weak solutions,
observations, and physical closure remain outside that result. The two a0
normalizations and the distinct reference histories remain separate.

The cheapest next acceptance check is byte-pin validation of this audit and
the unchanged candidate; no additional experiment is called for. A conservative
proofread-math self-review covered this report: no mathematical-token correction
to the candidate, no unresolved notation or scope issue, and no document build
needed for Markdown.
