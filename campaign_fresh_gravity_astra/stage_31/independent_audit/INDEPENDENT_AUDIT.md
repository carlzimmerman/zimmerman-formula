# FGF044 author audit recovered after interruption

Normalized claim: on the fixed Q background, for every sufficiently large
dimensionless N, the prescribed right-side velocity with amplitude v0 N and
width L/N^3 transports the original density exactly. On each fixed finite slab
it has uniformly vanishing relative entropy and full excess energy, vanishing
full spacetime energy current and declared weak equation/local-energy
residuals. It nevertheless violates the exact global energy inequality near
t=0. The fixed-time flux at zero, positive fixed times, and scaled initial
times have distinct limits. This is an exact continuity solution and a coupled
residual ansatz, not a coupled solution.

**Primary mathematical verdict: proved as written**, within precisely those
hypotheses and topologies. No correction to the author's raw derivation was
required. Final package verification is recorded separately in audit_result.json.

## Provenance and independence

This is a new recovery audit by `/root/fgf044_author_review_recovery`, dated
2026-10-05 local time (2026-10-06 UTC). It is not a claim that the interrupted reviewer finished an audit.
The inherited `FROZEN_DERIVATION.md` and `DERIVATION_FROZEN.json` existed before
this recovery. Their bytes were preserved. The inherited frozen proof hash is
`2240566ca05c2efdf90b70d4b6acceed993595c996a7fea4bc9a0387c5169e23`.
Its recorded author/root-unread status belongs to that earlier freeze, not to
the present reviewer. I read that inherited independent reconstruction before
the raw author proof and rechecked its critical identities; this recovery is
not a second newly blinded freeze. I have not read the stage31 root proof or
its reviewer output. Agreement between actors is not treated as mathematical
evidence in place of the calculations below.

The audited raw author file is
`deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-044/fgf044_run_001/DERIVATION.md`,
SHA256 `5603934d74e5f9236a388aee63adfe714ad6fb8e218f95de4a5436fec7c5d9fb`.
The task hash is `4f17b753567fb4f98dafa241195dac0bf24fd0107ab1b06b4c1486db4fcde023`.
All nine ancestry pins in that task and all eight source pins in the inherited
reviewer freeze matched. Old stage30 root artifacts were hash-checked only.
The raw FGF032, FGF040, FGF042, FGF043 and FGF023 derivations, common framework,
result contract and FGF042/043 reconciliations supply the local definitions.
There is no .mathbox ledger and no external literature dependency needed for
this bounded audit. The background is an inherited fixed object satisfying
the stated equations, not an existence theorem newly proved here.

## Dependency graph

1. Internal background identities: signed B0'=C rho, cs^2 rho'=-rho g0,
   J chi0''=U'-T0, and cs^2 log(rho/rho_ref)+phi0=mu constant.
2. Explicit C1,1 profile and its separated-variable flow imply an increasing
   finite-time map, positive Jacobian, exact pushforward continuity and fixed
   support/wall traces.
3. Polynomial Jacobian control and finite participating mass imply entropy,
   density and kinetic bounds. The hydrostatic identity gives the full energy
   cancellation, retaining interaction.
4. Finite trajectory displacement implies spacetime current bounds directly.
   Full current/density bounds imply the local-energy distribution estimate.
5. Actual field/momentum formulas imply residual estimates only in the stated
   spacetime first-derivative test norm. They do not use unproved dynamics.
6. A separate initial derivative gives exact-energy failure; a separate flow
   limit gives the initial-layer/fixed-time distinction.

All six branches are internal analytic arguments; none depends on numerical
sampling or on assuming the desired energy inequality.

## Critical reconstruction and adversarial checks

Put w=L/N^3, V=v0 N and s=Vt/w. Direct differentiation verifies
H'(y)=(1-y^2)^(-2), with H tending to opposite infinities at the two endpoints.
Hence Y_s=H^{-1}(H(y)+s) stays interior at every finite s and has
partial_y Y_s=f(Y_s)/f(y)>0. The endpoint extension is not obtained by dividing
zero by zero: the variational formula J=exp(integral v'(X_u)du) gives J=1 at
the fixed endpoints because v'=0 there. Since f' is globally Lipschitz, the
flow and inverse have Lipschitz first derivatives for fixed N,T. The pushed
density is continuous and locally Lipschitz on the perturbed patch, and its
weak first derivatives are integrable. Jumps of f'' create no mass sheet.
The unchanged weak crossing is outside this patch. The mass pushforward
identity proves continuity and its initial trace without requiring C-infinity.

To check polynomial compression independently, take g(y)=1-y^2 inside the
support. Along the flow d(1/g(Y_s))/ds=2Y_s. Applying the bound |2Y_s|<=2 in
both time directions, and using 0<g<=1, gives
(1+2s)^(-1)<=g(Y_s)/g(y)<=(1+2s). Thus
(1+2s)^(-2)<=J<=(1+2s)^2, which also verifies the author's looser 1+8s bound.
The log-density ratio is bounded by 2 log(1+8s)+2w Lip(log rho). Equal mass
cancels the linear entropy terms. Consequently D<=m_N h_N and
sup_t D=O(N^-3 log N), with m_N=integral_support rho=O(N^-3).
K<=V^2 m_N/2=O(N^-1). No uniform density bound is inferred.

Full internal plus interaction energy is exactly
cs^2 h(n,rho)+mu(n-rho), so its integrated linear term vanishes. With all
field energies unchanged, Erel=K+cs^2 D and the full relative density has
L1 bound epsilon_N+2|mu|m_N. This checks interaction, rather than discarding
it. At time zero the entropy derivative vanishes. Material differentiation
of K gives K'(0)=integral rho v^2 v'=-(1/3)integral rho'v^3>0 because the
support was explicitly chosen on the positive regular side. This refutes
the exact global inequality for each sufficiently large N, even while
Erel(t)<=Erel(0)+epsilon_N with epsilon_N->0. The proof does not specify
the duration of the positive-energy interval or equate it with the separate
t~N^-4 flux scale.

No outside particle can supply current: uniqueness fixes both support edges
and every exterior point. Fubini and the material identity give
integral_0^T integral n v=integral rho(b)(X_T(b)-b)<=2w m_N.
More directly, the cubic integral equals
(1/2)integral rho(b) integral_b^{X_T(b)} v(x)^2 dx db,
bounded by V^2 w m_N=O(N^-4). The bound is finite-slab and does not exchange
N with an infinite-time limit. The full current is cubic plus
n v[cs^2 log(n/rho_ref)+phi0], with enthalpy bounded using the actual log
Jacobian. Its spacetime L1 bound is O(N^-4)+O(N^-6 log N).

At t=0 the cubic spatial mass tends to
rho(x*)v0^3 L integral f^3/2>0. At t=s w/V with fixed finite s its coefficient
is instead rho(x*)v0^3 L integral f(Y_s(y))^3 dy/2, also positive. At each
fixed t>0, pointwise Y_{Vt/w}(y)->1 and dominated convergence gives zero.
For uniformity on [t0,T], dominate the supremum over s>=Vt0/w: for each
interior y it tends to zero once the trajectory reaches the decreasing side
of f. This supplies the detail behind the author's uniform-away-from-zero
statement. The spacetime L1 estimate rules out a time-delta flux despite
the nonzero initial spatial flux. No uniform-on-[0,T] flux limit is claimed.

Actual residuals are Rc=0, Rchi=0 and Rphi=C(n-rho). Matter momentum is
j_t+partial_x(nv^2+cs^2(n-rho))+(n-rho)g0. Combined momentum omits exactly
the last term, using the unchanged constant background stress. The signed
source residual is O(N^-3) in L-infinity_t L1_x. For compact spacetime tests,
integrated norms of j,nv^2,n-rho are respectively O(N^-6), O(N^-5), O(N^-3),
giving the claimed momentum rate. Tests reaching t=0 add O(N^-2) initial
momentum, still vanishing. These estimates do not prove uniform-time spatial
residual smallness.

The inherited frozen reviewer in fact exhibits why that stronger topology
fails. For G(s)=integral f(Y_s(y))dy, integration by parts yields
G'(0)=0 and G''(0)=-integral f(f')^2<0. A spatial test equal to one on the
support detects d/dt integral j asymptotic to rho(x*)V^2 G'(s) at small fixed
s>0, hence order N^2. The f'' jumps do not obstruct these integral derivatives:
f' is Lipschitz and the finite interior trajectories are smooth. This checked
supplement supports the author's careful refusal to claim the old topology;
it is not required to strengthen the author claim.

Finally, the local-energy residual estimate follows by distributional
integration by parts using the full relative density and full current just
bounded. Initial energy contributes O(N^-1), and terminal traces, if tested,
are covered by the same uniform bound. Near physical walls every perturbation
vanishes, mass/energy currents are zero, and background momentum traction is
unchanged rather than asserted zero. Continuity is exact, and at finite N the
local identity RE=v Rm can be checked a.e.; no product of limiting weak
residuals is used. Setting velocity identically zero gives the identity flow,
original density, zero full relative energy/current and every residual zero.

## Obligation matrix

| Obligation | Status | Scope |
| --- | --- | --- |
| C1 endpoints and declared weaker regularity | passed | Finite N,T; no uniform smoothness |
| Positive map, density and exact mass | passed | Exact pushforward; no incoming supply |
| Entropy and kinetic energy | passed | Uniform fixed-slab bounds |
| Full field/interaction energy | passed | All unchanged field terms retained |
| Decision on exact global inequality | passed | Strict failure on chosen right side |
| Cubic and full spacetime current | passed | Strong L1 vanishing on fixed slab |
| Fixed-time and initial-layer limits | passed | Not uniform through t=0 |
| Dynamic signed Q and scale residuals | passed | Source residual retained explicitly |
| Matter and combined momentum residuals | passed | Spacetime C1-test dual, not uniform spatial |
| Full local-energy residual | passed | Weak limit zero; finite-N residual nonzero |
| Initial and wall terms | passed | Relative traces and zero mass/energy wall flux |
| Zero-velocity control | passed | Exact identity state |
| Exact coupled evolution/admissibility | out of scope | Not established; global inequality fails |
| Physical theory, cosmology or observations | out of scope | No transfer or closure claim |

## Verification, gap and safe conclusion

Read-only shell inspection and Python standard-library SHA256/JSON checks
verified provenance. These are bookkeeping commands, not mathematical runs.
No numerical experiment, library installation, service, network access,
literature search or repository-wide mutation was performed. The proof was
checked analytically from the actual equations. Final package hashes and
contract verification belong to the accompanying audit result.

There is no remaining gap in the scoped author claim. The unresolved next
implication is a same-action construction satisfying actual coupled dynamics
and a justified energy admissibility rule simultaneously. This prescribed
velocity family cannot itself supply that implication because its exact global
energy inequality fails. A new profile/moment sweep is not needed to validate
this conclusion. Both a0 hypotheses, fixed vacuum versus frozen-H versus
evolving-H histories, fixed coefficients and signed MOND sources remain
separate. No physical reservoir, metric/photon/DOF, instrument evidence,
historical novelty or nonlinear stability follows.

## Final recovered package verification

The recovery author subsequently froze the package. I read its final result,
report and input mapping, and independently verified all 19 required contract
fields, all 13 input hashes and all 3 artifact hashes; the input mapping agrees
exactly with result.json. The explicit failed exact-energy check is appropriate
evidence for the proved negative subclaim and must not be converted to a pass.
The package continues to mark orchestrator acceptance unreviewed; this separate
audit supplies scoped review evidence without modifying the author record.

- `result.json`: `5472cc19350935a6a09c18a69e10914211c7fb2e7cf3876f3e0054f062d2341c`
- `REPORT.md`: `e66c58db90981bc37f42c552782db53567e84c879dfa7a246bf76a81d8f33b2b`
- `input_sha256.json`: `8f6608c19ed0a16de28dab0bfffb71b7ba09c25083ce4ebf9d126badeb4073d8`
- Original author `DERIVATION.md`: unchanged at the hash recorded above.

The final report/result explicitly disclose that this reviewer sent two scope
cues after the package agent had completed its own reconstruction and initial
report: no blocking correction, and separation of energy-increase timing and
initial-trace rates from the flux transient/interior rates. This disclosure
does not turn that package self-review into another independent derivation.
No mathematical correction, author proof rewrite or additional run occurred.
