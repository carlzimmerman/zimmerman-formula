# FGF048 full independent audit of the frozen author proof

Primary verdict: **proved as written** for the author's bounded uniform-time
claim and the two stated feedback bounds. No correction to author proof bytes
is required. This verdict is a separate review; orchestrator acceptance remains
separate. The independent pre-exposure derivation is preserved unchanged.

## Normalized claim and exact reviewed revision

For each fixed positive coefficient set and each specified smooth hydrostatic
positive-g background, every integer N>=1 satisfying L/N^3<R/2 has an actual
classical solution of the original Q/scale/isothermal-fluid equations through
T_N=kappa(L/v0)N^-4 for one positive kappa independent of N. The initial
velocity is exactly the zero-extended C1,1 polynomial V(1-y^2)^2, V=v0 N,
y=(x-x*)/(L/N^3), with unchanged initial density and fields and zero field
velocities. On the explicit contained cone the density, a and g=phi_x retain
N-independent positive bounds. Matter and first field variables are spacetime
C1 and spatial C1,1 for each N; potentials are C2. Both constraints, local
uniqueness/exterior independence, full local energy and the zero-velocity
hydrostatic control hold. Actual feedback satisfies

    sup|g-g0|<=C_g N^-4,
    sup|partial_x(g-g0)|<=C_dx N^-1.

The constants are fixed background/extension norms specified in the author
proof. They are not universal over arbitrary extensions, backgrounds or an
unbounded frozen-reference family. A common kappa for the two prescribed a0
backgrounds can be their minimum. No upper lifespan, shock endpoint or global
claim is included.

Reviewed authoritative files:

- Author DERIVATION.md SHA256
  `010afcd5c5de6a1618272511e30371feae09f45195405373e15e68f8beb31de2`.
- Author result.json SHA256
  `661277e12a22bc33b4cac093dde1540f5a501f513eeb52d22230cb65e6a1bce2`.

Both hashes were checked before the first author read. Every one of the
11 author input hashes and 7 declared artifact hashes was then independently
checked and matched. Paths are recorded in the accompanying audit_result.json.
The full 479-line author derivation was read in two untruncated ranges.
FAILED_ESTIMATES.md, PROVENANCE.md, REPORT.md, and FREEZE.json were also read.
No new coordinator or other-reviewer mathematical proof was read.

## Independence and scope of the comparison

The reviewer derived a route independently from the pinned task/common/OLD
inputs and froze it at 2026-10-06T04:42:53.128733+00:00 before receiving author
final pins. The freeze hashes are in INDEPENDENT_FREEZE.json; its hash is
`0739426fec675a1e1df57ed586571508a6672bfae5a5886310e370976de45f31`.
The independent derivation hash remains
`514c20500a677b9bd15d764dc2ef59d4aa7d8b0b0c76037214c99fcfa4a6babe`.
AUTHOR_EXPOSURE.json records the later author exposure.

The frozen route obtained only an O(1) derivative-feedback estimate; it did
not independently predict the author's O(N^-1) derivative result. That sharper
result has been audited from the actual author equations after exposure,
specifically (6.2)-(6.4). It is not attributed to pre-exposure derivation.
Neither matching conclusions nor agent identity is itself mathematical proof.

## Dependency graph

Pinned FGF047 exact characteristic construction for each finite data set
  -> fixed positive-g field chart with full chi sources
  -> fixed coefficient bounds independent of velocity amplitude
  -> separate fluid/field first-gradient inequalities (3.1)
  -> direct continuity transport for log density and strict field displacement
  -> explicit N-independent kappa (4.1) and strict bootstrap (4.2)-(4.4)
  -> pair-flow C1,1 estimate (5.1), retaining N^7 initial seminorm
  -> uniform fixed-N time traces and compatible restart (5.3)
  -> existence through the entire N^-4 interval
  -> integrated actual g_t=p_x feedback and refined density-gradient estimate
  -> refined field seminorm and N^-1 derivative feedback.

Separate exact consequences are constraint propagation, physical cones and
local uniqueness, energy exchange cancellation, and hydrostatic control. All
load-bearing leaves are explicit algebra/inequalities or the pinned internal
FGF047 construction. There are no external-source, computation or observational
leaves requiring conditional acceptance.

## Obligation matrix

| Obligation | Status | Decisive evidence |
|---|---|---|
| Task and ancestry byte identity | passed | Task hash and eight OLD pins matched before derivation; all author pins rechecked |
| Exact quantifiers and fixed coefficients | passed | Author Sections 1,2,4,9; one kappa for all admissible N with fixed background |
| Original Q constitutive law and pressure | passed | Exact B,W,T and c>0 retained in (2.1) |
| Actual moving fields and scale terms | passed | H depends on q,z; both h_chi terms and B_chi k survive |
| Degenerating acoustic constants | passed | Author works with fixed unscaled c; bounds expose A/c and Hf/c |
| Density propagation | passed | D_v q=-v_x gives excursion <=a kappa<=1/2 |
| Uniform field gradients and state margin | passed | Bf<=beta and same-point displacement <=delta/2 |
| Exact C1,1 joins | passed | Pair-characteristic gradient differences, no classical f'' at joins |
| Uniform horizon rather than fixed-N start only | passed | Strict bootstrap plus finite-N endpoint trace/restart |
| N^7 higher norm | passed | Linear seminorm inequality with source O(N^8), time O(N^-4) |
| C1 endpoint trace and compatibility | passed | Equation (5.3), distributional time integration, continuous representatives |
| Force feedback O(N^-4) | passed | Actual g_t=p_x, ||p_x||<=beta on established interval |
| Force derivative feedback O(N^-1) | passed | q_x=O(N^3), Hz forcing O(N^7), double time integral |
| Physical units | passed | Fixed L,v0,nref normalization and restoration (8.1) |
| Physical cone containment | passed | S_N<=s0 N and S_N T<=R/4 |
| Exterior independence | passed | Common backward domains and max speed; no universal exterior norm claim |
| Constraints and reconstructed potentials | passed | Off-constraint term explicitly canceled only after chi_x=k |
| Full energy including boundary terms | passed | +np/-np and -Tw/+Tw cancel; both fluxes and Reynolds terms retained |
| Zero-velocity control | passed | Exact hydrostatic tuple satisfies all four original equations |
| Two a0 choices and distinct histories/laws | passed | Section 9; no evolving-reference work or law transfer |
| Numerical/external-source claims | out of scope | Zero mathematical executable runs and no literature mechanism |
| Fixed-force upper lifespan / endpoint transfer | out of scope | Explicitly excluded; remains a separate open implication |

## Critical inequalities reconstructed

1. **Block first derivatives.** For fluid invariants r,s, the speed derivative
is v_x=(r_x+s_x)/2, so |v_x|<=A. Differentiating the source -g gives at most
G Bf. Hence A'<=A^2+G Bf in the integral supremum sense. For each field
coordinate, the transport derivative contributes L1 Bf^2, while its source
contributes P max(|q_x|,Bf)<=P(A/c+Bf). The coefficients see no velocity
amplitude or velocity derivative except through q_x. This is the essential
reason beta need not grow with N.

2. **Strict uniform gate.** With P_N=N^4, t<=kappa/P_N, A<aP_N and
Bf<beta, the author's two estimates improve the bootstrap because every
numerator in (4.1) is positive. In particular beta>B0 and a>a0. Bounding
P_N^-1 by P_N where needed is conservative and valid for N>=1. Density uses
integral A<=a kappa<=1/2. The field chart uses integral(Lambda beta+F),
which is <=delta/2. The pressure is not discarded. Independent rectangular
r/s amplitudes are used only for speed, not for density.

3. **Higher norms and joins.** Differentiating once more in the a.e./pair-flow
sense gives three factors of first-gradient times second-gradient: two from
differentiated transport coefficients and one from the transported gradient.
For fluid speeds the Hessian vanishes, giving 3A Hf. For field speeds the
Hessian acts only on field gradients, giving 3L1 Bf Hz+L2 Bf^3. The source
chain rule gives P(Hz+Hf/c)+Q(Bf+A/c)^2. Therefore (5.1) is valid with the
author's maximum-component conventions. Initial Hf is at most
8N^7+c Lip(q0_x); initial Hz is fixed. Integrating the sum yields (5.2),
since the added O(N^8) source integrates to O(N^4), bounded by O(N^7).
No smooth approximation of f is needed.

4. **Endpoint trace.** For each fixed N, all speeds, states, first gradients
and spatial gradient Lipschitz seminorms are finite up to the proposed endpoint.
Equation (5.3) thus bounds the distributional time derivative of U_x in
L-infinity. Integrating gives time-Lipschitz continuous spatial representatives.
The uniform state and gradient limits define a C1,1 trace by integration in x.
The initial gradient constraints pass to the limit; the field potentials have
compatible traces by time integration. FGF047's actual construction accepts
such compatible C1,1 data and does not require zero restart velocities or
hydrostatic restart data. Its local restart length can depend on N. Uniqueness
glues intervals and excludes an endpoint at or before the controlled horizon.

5. **The sharper derivative feedback.** The transported derivative identity
D_v q_x=-v_x q_x-v_xx gives (6.2) using |v_xx|<=Hf<=C_H N^7 and
integral |v_x|<=a kappa. Hence q_x=O(N^3), rather than the crude O(N^4).
In the field seminorm equation, this replaces only the quadratic source term
by O(N^6); the linear Hf/c term remains O(N^7). Thus (6.3) is justified
without an unsupported q_xx improvement. Since Lip(p_x)<=Hz,

  ||g_x(t)-g0_x|| <= integral_0^t Hz(u)du
   <=exp(E_z kappa)[Hz(0)t+(D_z/2)N^7 t^2].

At t<=kappa N^-4, the second term is O(N^-1), and the first is O(N^-4),
which is bounded by O(N^-1) for N>=1. Weak spatial differentiation is enough;
the resulting g_x difference is continuous, so the a.e. bound extends to
every point. This verifies the author's sharper result without replacing its
argument by the weaker pre-exposure route.

6. **Units and sign margin.** Physical g has unit v0^2/L and physical x has
unit L, so (8.1)'s factors v0^3/L^2 multiplying physical time, and v0^2/L^2
multiplying the derivative estimate, are correct. The guaranteed positive
potential gradient is g>0. A positive g0_x is not implied; the author correctly
states its preservation only conditionally on a separately supplied margin.

7. **Cones and energy.** S_N<=s0 N and kappa<=R/(4s0) imply
S_N t<=R/4, even for the smallest admissible N. Backward characteristic and
vertical reconstruction paths stay inside shrinking K_t, preserving local
physical meaning. All flux terms in the energy are needed and have the correct
signs. Local conservation is compatible with moving-boundary energy changes;
no shrinking-cone integral is declared constant.

## Source/computation checks, failed attempts, remaining gap

Administrative commands used source `cat`/`sed`, `shasum -a 256`, and a Python
SHA256/JSON validation loop. They performed no mathematical computation.
The loop verified all 11 author input and 7 artifact hashes. There were zero
numerical samples, PDE runs, downloads, services, installs or commits. Writes
were confined to this independent_audit directory.

The author's five failed estimates are accurately limited: old displacement
cutoffs can cost an extra N, rectangular invariants overestimate density,
pressureless inversion hides N/c, generic cubic estimates lose the useful
N^7 envelope, and initial jets do not establish finite-interval control. None
is misreported as an existence counterexample. They remain preserved.

No missing implication is identified within the stated bounded theorem.
The next genuinely unproved mathematical implication is persistence of the
old fixed-force upper-lifespan/endpoint mechanism under actual coupled field
feedback. The accepted early-time bounds do not establish it. The cheapest
next scientific step is a separate explicitly scoped analysis of that mechanism,
not another duplicate local-existence task or a numerical family asserted to
prove large-N behavior.

## Proofreading review-only result

Coverage: entire author derivation and result claim, report, failed estimates
and provenance. No mathematical-token edits and no author-file edits. The
author overloads beta for a constant and later an integration endpoint, but
the contexts explicitly distinguish them; this causes no unresolved mathematical
ambiguity. No objective LaTeX, notation, unit or quantifier correction is needed.
Validation is analytic reading plus byte/metadata checks; no LaTeX document
was requested or compiled. The preserved independent derivation was not revised
to match the author's stronger derivative estimate.
