# FGF045 author report and self-review

Normalized claim: for each fixed inherited positive regular-side background
neighborhood and prescribed C1,1 polynomial data, there are fixed B,N0 such
that N>=N0 rules out a positive-density C1 solution covering the local
characteristic domain through T_N=B L/(v0 N^4). The claim is an a priori
lifespan obstruction for the actual isothermal fluid in the fixed potential;
it does not construct a local or maximal branch. Primary self-review verdict:
**proved as written**, in precisely that nonexistence-through-time scope.
This is author self-review, not independent acceptance.

The derivation retains pressure and bounded force and force derivative.
Weighted characteristic gradients y=n^(-1/2)(v+c_s log(n/n_ref))_x and
z=n^(-1/2)(v-c_s log(n/n_ref))_x cancel the raw mixed product exactly. Their
upper envelope controls h=n^(-1/2), and the initial negative y on the right
flank gives a closed reciprocal inequality. All coefficient and containment
thresholds are explicit in DERIVATION Sections 3–5. The polynomial is unchanged;
its C1,1 endpoints require no second derivative in the characteristic-flow
argument. No pressureless substitution, limiting equation, numerical run,
external theorem, or literature mechanism is used.

## Dependency graph and decisive evidence

- Pinned FGF044 ancestry supplies the fixed background, units and exact profile;
  the FGF035/FGF023 ancestry supplies hydrostatic and signed-Q conventions.
  These are inherited inputs, not newly audited existence theorems.
- Fluid PDE plus positive C1 regularity implies the two characteristic
  transport identities and their differentiated-flow gradient identities.
  Evidence: internal exact derivation, Sections 2–3.
- Initial data plus upper envelope inequalities implies
  h<=h0+A omega t on the characteristic cone. Evidence: internal bootstrap,
  Section 4, all force contributions bounded by G1.
- This density lower bound and a large negative initial weighted gradient
  imply w'>=w^2/[4(h0+A omega t)]. Evidence: exact inequality, Section 5.
- Reciprocal integration contradicts positive finite w by an explicit time
  O(N^-4). Every used characteristic remains away from crossing and walls.
- Fluid PDE independently implies the full kinetic/internal/potential energy
  identity. Zero wall flux implies conditional integrated conservation;
  local cone boundaries retain their flux terms. Evidence: Section 6.
- No edge in this graph supplies local PDE existence or maximal-branch
  continuation. Those remain explicit separate obligations.

## Obligation matrix

| Obligation | Self-review status | Evidence / restriction |
|---|---|---|
| Eight ancestry pins | passed | All exact SHA256 values match the task |
| Same profile, units and coefficients | passed | (1), (2), Section 7; no smoothing |
| Pressure included | passed | Speeds v +/- c_s, characteristic variables, energy pressure work |
| Force included with either derivative sign | passed | -g0 in (4), -g0' h in (6), absolute bounds in (12) |
| C1 gradient identities | passed | Differentiate characteristic integral by label; no C2 assumption |
| Mixed-gradient cancellation | passed | (5) to (6), using D+q=-beta and D-q=-alpha |
| Density coefficient controlled | passed | (13)–(15), includes all positive-gradient regions |
| Domain and target characteristic stay regular | passed | (7)–(8), (12), (16); O(N^-3) displacement |
| Closed compression inequality | passed | (17)–(19), force threshold and first-exit argument |
| N-independent time excluded | passed | T_N=B/omega tends to zero; constants fixed |
| Local existence / continuation criterion | not addressed | No such theorem imported; endpoint classification conditional |
| Vacuum / density infinity distinction | passed with stated scope | (9),(15) bound density inside the cone for each fixed N while C1 estimates hold |
| Fixed-potential full energy | passed | (21),(22), cancellation of pressure and force work |
| Zero-flux global identity | conditional | Requires an actual solution with compatible stationary impermeable walls |
| Zero-velocity control | passed | Hydrostatic n=rho,v=0 solves both PDE and has zero flux |
| Q field residual distinct from energy | passed | Rphi=C(n-rho), no claimed cancellation from fluid conservation |
| Both a0 and model-history branches | passed | Separate fixed backgrounds, no evolving-H transfer |
| Exact coupled / empirical / physical closure | out of scope | No claims made |

## Failed route, limitations and exact remaining gap

The unweighted equation D+alpha=-alpha^2/2-alpha beta/2-g0' does not have a
closed compression sign from alpha alone. This was an analytic route
obstruction, not a failed numerical experiment or evidence of singularity.
The exact density weight removes that mixed term, and Sections 4–5 then
close the proposed bound without assuming density coefficients.

The estimate is deliberately conservative; B may be very large and N0
correspondingly large. It proves neither a sharp shock time nor a limiting
shock profile. The theorem rules out a positive-C1 slab. To assert that a
constructed maximal branch has a specific first gradient singularity requires
local existence and a continuation theorem, neither supplied here. If such a
branch continues up to the reciprocal obstruction, its gradients cannot stay
bounded; this conditional statement is not a substitute for those obligations.
No global wall evolution, support invariance, exact coupled gravity, weak
continuation, physical reservoir, empirical source mass, or observational and
historical claim is made. In particular energy conservation is conditional on
an actual fluid solution and does not solve the frozen-field source equation.

One discriminating next task, only if needed: construct local C1 evolution and
prove a continuation criterion directly for this exact C1,1 profile in the
regular fixed-potential region, then attach the a priori bound to that branch.
Do not transfer this result to dynamically coupled gravity.

## Provenance, commands and conservative proofreading

Proof-only. There were zero mathematical executable computations, simulations,
random samples, numerical tolerances or computation manifests. Shell reads,
SHA256 checks, artifact writes and JSON field/hash validation were administrative
operations only. Accordingly result.json commands is empty with that reason;
no numerical wall, memory or thread limit is claimed. No network, installation,
service, commit or new stage32 root/reviewer read occurred. The first recorded
proof/package timestamp is 2026-10-06T01:38:36Z; preliminary source reads and
pin checks preceded that recorded timestamp, and their exact start was not
captured. This uncertainty is disclosed instead of inventing an earlier time.

Proofread: all newly written DERIVATION.md and REPORT.md. Routine edits:
clarified that the characteristic displacement, not the fixed-width cone, is
O(N^-3); distinguished force bounds G0,G1 from Newton's G; removed a stray
leading space. Mathematical-token changes: none. Unresolved proofreading
issues: none found. Scientific validation: direct symbolic self-review only;
JSON fields and byte hashes checked administratively. External independent
review remains required before acceptance.
