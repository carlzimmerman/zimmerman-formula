# Independent audit of the FGF045 root derivation

Normalized claim: for the specified positive-side hydrostatic background, fixed
positive physical parameters, and C1,1 polynomial initial velocity, all sufficiently
large N exclude a positive C1 solution of the fixed-potential isothermal fluid
equations on the complete specified cone through
T_N=(S L/v0)N^-4. The result is an a priori obstruction conditional on a supplied
solution, with no existence or continuation theorem. The local fluid energy
identity includes the fixed-potential interaction; the gravitational source
residual generally remains nonzero.

**Primary verdict: correct only after a stated restriction.** Equations (1)-(12)
prove the cone obstruction. The original sentence classifying an earlier maximal
endpoint as forced gradient loss is unsupported. The separately pinned
CORRECTION.md withdraws that sentence and also disambiguates a force-bound/Newton
constant notation collision. The corrected, restricted result passes this audit.
This verdict does not promote the uncorrected document as proved as written.

## Scope and immutable sources

Audit actor: isolated subagent `fgf045_root_audit`, 2026-10-06. The raw proof and
proof record were supplied without the new stage32 author or reviewer verdicts.
No new stage32 author/reviewer proof or conclusion was read. The two issues below
were sent to the root before the corresponding corrections were read. Reading
and checking that subsequent correction is a revision check, not a claim that
the correction itself was independently authored.

Primary artifact pins:

| Artifact in this directory | SHA256 |
| --- | --- |
| ROOT_DERIVATION.md | e4c94d7b9019d61c91499bcc818d1f88f2b434a04c35533dace7061e853dd58d |
| PROOF_RECORD.json | 4e3bad37e0f52955c9029883194d0d58b12561fe835beb7c496dd445adafea70 |
| CORRECTION.md, final checked revision | 3d7f3a319de9db22fba6afadf58d66229e11b4a8a211066a18db002bd111cf21 |

The task, common execution framework, pinned FGF044 reconciliation, pinned
FGF044 author derivation, and stage31 exact-continuity root derivation were read
for conventions and ancestry. All nine input hashes in PROOF_RECORD.json were
recomputed and matched. Files checked only by hash are distinguished from files
read in audit_result.json. The framework hash is
ff0d2873065578b0bd8aa50907e0a39495ff8da775bf2b4890768d83775fd750.
No .mathbox ledger or applicable AGENTS.md was found by the performed checks.
The proof-audit skill and its general-logic, computation and source checklists
were read. No literature, network, service, installation, mathematical executable
experiment, parameter scan, or numerical shock simulation was used.

## Claim card and dependency graph

The objects are real-valued n,v on a closed shrinking cone, C1 up to its
boundaries with positive n; equivalently the necessary identities can be
established on interior compact subcones and continued to the stated traces.
The initial n is smooth positive rho and v=v0 N f((x-x*)/(L/N^3)), with
v0,L>0 as expressly inherited from the pinned initial-data definition. The
fixed regular interval U lies strictly on the g>0 side and away from the
crossing and walls. The prescribed force is g=phi0_x, with g,g' bounded on U,
and cs^2 rho_x=-rho g. No vacuum, cs=0, evolving force, or wall existence claim
belongs to this theorem. The case M=0 is included by continuous interpretation.

The dependency graph is:

1. PDE plus C1 regularity -> characteristic invariants and differentiable
   characteristic-label formulas -> weighted-gradient ODEs.
2. Initial invariant bounds plus force bound -> strict speed bootstrap ->
   backward cone containment for both acoustic families and material paths.
3. Weighted-gradient ODEs plus containment -> positive-gradient envelope and
   material reciprocal-density envelope -> Volterra comparison -> Wbar(s).
4. Hydrostatics plus the exact profile -> initial compression z(0)>=d.
5. Explicit N gates -> forward compressive characteristic containment and
   domination of the force-gradient term -> reciprocal contradiction.
6. PDE plus time-independent potential -> local energy identity; supplied
   boundary flux hypotheses -> conditional integrated energy conservation.
7. Pinned frozen-field source convention -> Rphi=C(n-rho), Rchi=0.

Leaves 1-6 are internal calculations and fixed-domain hypotheses. Leaf 7 uses
the pinned stage31 source convention, not a new theorem. Neither the proof nor
this audit has a local-existence or continuation leaf; consequently neither can
deduce the mechanism at an earlier maximal endpoint. There is no circular use
of a density or positive-gradient cap.

## Independent reconstruction of the critical implications

Write h=log(n/nref). Continuity gives D0 h=-v_x; momentum gives
D0 v=-cs^2 h_x-g. Thus D+ r=-g and D- l=-g. Also
D+ h=-beta and D- h=-alpha. These signs retain the pressure terms.

For a plus characteristic X(t,q), let J=partial_q X. Since v is C1,
J_t=v_x(t,X)J and J(0)=1. Differentiating the integral invariant formula in
q gives

    alpha(t,X) J = alpha(0,q) - integral_0^t g'(X(u,q)) J(u,q) du.

The right side and J are differentiable in time and J>0. Division by J
therefore gives the gradient ODE along X even when alpha is merely continuous
as a spacetime function. No alpha_x or v_xx is required. The minus family is
identical with beta. Since D+ w=w beta/2 and D- w=w alpha/2,
multiplication cancels the mixed product and yields exactly

    D+ a=-a^2/(2w)-w g',   D- b=-b^2/(2w)-w g'.
    D0 w=(a+b)/4.

This verifies the claimed regularity route rather than formally differentiating
a C1 PDE twice. The joins of f have continuous first derivative; their jumps
in f'' create no term in these identities.

For cone closure, let C0=B+G_force T0+cs+u*, so C_N=V+C0. At time zero all
three speeds have a strict margin from the inward boundary speeds +/-C_N.
Suppose this strict bound first fails before the target time. On every earlier
slice the backward vector fields point into the wider earlier intervals K_s;
their trajectories reach time zero without meeting a lateral boundary.
Integrating the invariants there gives |r|,|l|<=V+B+G_force t, hence
|v|+cs<=C_N-u*. Continuity on the compact truncated cone preserves the same
strict margin at the alleged first failure, a contradiction. This simultaneous
bootstrap establishes containment before using the global speed estimate; it
does not presume a solution outside U. Material speed obeys the same bound.
For each finite N this also yields

    nref exp[-(V+B+G_force T0)/cs] <= n
      <= nref exp[(V+B+G_force T0)/cs].

These bounds are intentionally not uniform in N.

On a contained acoustic path, a(t)<=a(0)+M integral W, and similarly for b;
taking positive parts proves the P inequality. On a material path,
w(t)<=W0+(1/2) integral P. Substitution yields

    W(t)<=W0+P0 t/2+(M/2) integral_0^t (t-u)W(u)du.

Iteration of this nonnegative scalar kernel gives the stated hyperbolic-function
comparison. Compact-cone continuity supplies locally bounded envelopes for the
iteration remainder. When M=0 it is precisely W0+P0 t/2. The initial bounds
alpha0=A f'-g/cs and beta0=A f'+g/cs give P0<=W0(DA+G_force/cs)<=p A.
For k t<=1, W<=2W0+p A t. This is a derived lower bound on density and does
not claim an N-uniform upper bound on density.

Directly, f'=-4y(1-y^2) in its support; its minimum is -8/(3 sqrt(3)) at
y=1/sqrt(3). Thus alpha0=-DA-g/cs and -a0/A>=w0 D=d. Under the force gate,
for z>=d and 0<=s<=S,

    z_s >= z^2/(2 Wbar(s)) - M Wbar(s)/A^2
        >= z^2/(2 Wbar(s)) - d^2/(4 Wbar(s))
        >= z^2/(4 Wbar(s)) > 0.

There is no sign reversal in the reciprocal inequality. A first-downcrossing
argument keeps z>=d. Its integrated reciprocal is bounded above by
1/z(0)-(1/(4p))log(1+p s/(2W0)); the chosen S makes the logarithmic term
equal 2/d. This is incompatible with finite positive z at S. In fact this
comparison would already exclude persistence to the smaller scaled time
(2W0/p)(exp(4p/d)-1), with the original gates still sufficient. No sharpness
claim is implied.

The gates are achievable with fixed physical coefficients. Besides the force
and time gates, the final geometric left side is exactly

    L(1/sqrt(3)+2S)/N^3 + 2 C0 S L/(v0 N^4),

which tends to zero. Before any putative exit, the selected forward path has
|X(t)-x*|<=ell/sqrt(3)+C_N t; the gate makes this strictly less than
R-C_N t. Thus its containment uses a valid first-exit argument, not an assumed
invariant velocity support. The very large finite S does not obstruct
eventual N thresholds and is not represented as a useful physical estimate.

## Energy, source, units and controls

Let K=nv^2/2. Continuity and momentum give
K_t+(vK)_x=-cs^2 v n_x-nv g, while
e_t+(ve)_x=-cs^2 n v_x. The fixed-potential term satisfies
(n phi0)_t+(nv phi0)_x=nv g. Summation proves (13), including enthalpy and
potential. On a moving interval [a(t),b(t)] the integral derivative is
Q(a)-Q(b)+b' H(b)-a' H(a); hence the cone alone does not conserve integrated
energy. The original proof correctly keeps this distinction.

From the pinned convention Rphi=tau phi_tt-B_x+C n and B0_x=C rho,
freezing the field gives Rphi=C(n-rho), with C=4pi G_Newton after correction.
Rchi=0 follows because its fixed-field equation is still the background one.
No later smallness estimate or exact coupled source law follows. The fluid
momentum equation itself is exact under the supplied solution hypothesis.

A,k,alpha,beta,a,b have inverse-time units; w,p,d,S,N are dimensionless;
g and G_force are accelerations; g' and M are inverse-time squared; speeds
and lengths have their declared physical units. phi0 and cs^2 have units of
specific energy, so H is energy density and Q energy flux. For mass density n,
G_Newton n has inverse-time-squared units, unlike G_force n. The correction
therefore repairs a real notation/type collision in the uncorrected source
paragraph without changing the inherited gravitational normalization.

With v=0,n=rho, hydrostatics solves the fluid equations and Q=0. The order-A
compressive premise is absent. Each of the two a_ref backgrounds supplies its
own constants; the proof uses their common structural hypotheses and does not
derive their numerical calibrations. Constant-vacuum, frozen-H and evolving-H
branches remain distinct, with no transfer to dynamical gravity or other
physical closure claims.

## Obligation matrix and original failures

| Obligation | Status | Evidence / limit |
| --- | --- | --- |
| Invariants and gradient equations for positive C1 solutions | passed | Label-Jacobian reconstruction above; no C2 assumption |
| Weighted-gradient cancellation and material w identity | passed | Direct substitution |
| Noncircular backward cone closure | passed | Strict-margin first-failure argument |
| Density/positive-gradient control | passed | Closed Volterra inequality; M=0 checked |
| Initial compression and profile regularity | passed | Exact f' and hydrostatic signs |
| N gates and forward selected path | passed | Explicit N^-3 and N^-4 geometric terms |
| Riccati reciprocal contradiction | passed | Positive denominator, retained forcing, logarithmic integral |
| No complete positive C1 cone through T_N | passed | Contradiction under precisely that hypothesis |
| Original classification of an earlier maximal endpoint | failed | Root lines 121-124 require an unproved continuation input |
| Corrected endpoint scope | passed | CORRECTION.md withdraws classification; existence remains unproved |
| Full local energy and conditional global flux statement | passed | Direct balance with n phi0 |
| Original use of G in source and force bounds | failed | Root lines 49, 148, 157 collide in dimensions |
| Corrected source notation, residual and units | passed | G_force versus G_Newton; pinned source sign |
| Hydrostatic control and both background branches | passed | Structural conditional checks; no calibration claim |
| Local existence, earlier-endpoint mechanism, weak continuation | not addressed | Neither supplied nor accepted |
| Exact coupled gravity, observational/physical closure | out of scope | Explicitly excluded |

The smallest missing implication in the original endpoint interpretation is:
bounded positive state and bounded first derivatives at an earlier endpoint
imply extension of this solution with the required domain and regularity.
It was not established. The correction removes the need for that implication;
it does not prove it. A density bound alone cannot replace it.

## Source checks, commands and safe conclusion

Commands used were read-only `cat`, `rg --files`, `ls`, `nl -ba`, `shasum -a 256`,
and a Python stdlib hashlib/json pass over the declared input paths. The Python
pass performed metadata hashing only. All nine declared hashes matched; the
primary frozen raw-proof hash matched before review and was rechecked after
the correction. No mathematical executable computations were performed. Only
this audit and its JSON record were written by this auditor.

The strongest accepted statement is the corrected explicit cone obstruction
T_N=(S L/v0)N^-4 and the conditional energy identity. An N-independent time
interval of positive C1 evolution on a fixed neighborhood covering these cones
is therefore impossible for this data family. This is not an existence theorem,
an actual shock construction, or a classification of every earlier endpoint.
No additional check is needed for the corrected bounded claim. The cheapest
next check for any stronger endpoint claim is an explicitly scoped continuation
criterion; the exact coupled-gravity problem additionally requires new force
and field control and is not settled here.
