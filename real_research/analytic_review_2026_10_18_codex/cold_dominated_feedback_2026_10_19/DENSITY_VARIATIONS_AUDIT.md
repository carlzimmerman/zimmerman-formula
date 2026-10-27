# Independent audit: exact-density variations and finite-threshold genericity

19 October 2026. Reviewer `/root/audit_density_variations`, a fresh delegated audit session. Analytic derivations and text/hash operations only. No scientific scripts, integrations, scientific arrays, or process operations were used. No repository file was changed.

## Normalized claim and verdict

Fix the positive warmth, target densities, potentials, orbit maps, and support of the exact two-species cold-dominated equilibrium in the raw candidate. For each species, let `H_low` have the candidate's weighted smooth half-strip topology and let `N_den=ker A_den`. The claim audited here is:

1. The exact inverse gives continuous linear maps `A_den:H_low -> X_infty` and `B_den:X_infty -> H_low` with `A_den B_den=I`; consequently `I-B_den A_den` is a continuous projection onto the exact density nullspace.
2. A sufficiently small open neighborhood in the product nullspace consists of actual smooth, self-consistent equilibria with the same physical support and individual densities, positive physical DFs, and strictly negative physical energy derivatives throughout the open occupied set.
3. If the scalar mode variation vanishes on this nullspace, it factors continuously through radial density, and its local distributional representative is the orbital average of a radial distribution.
4. Assuming the scalar transversality assertion (6.5), the locally constant nullity loci for the finitely many fixed circular fundamental thresholds form an open dense subset of this actual-equilibrium parameter neighborhood, and every kernel field there satisfies (CF).

**Primary verdict: conditional on the named scalar transversality input (6.5).** All assigned functional-space, actual-variation, factorization, and finite-threshold Fredholm steps pass. No further gap was found in those steps. The scalar pairing formula (3.1), its integration-by-parts identification (3.3), and the proof of (6.5) in Sections 5--6 are named inputs to this bounded verdict, not conclusions independently certified by this report. The raw source-boundary and kernel-to-energy theorems are also retained in their exact stated form below.

This supports an open dense subset **relative to the constructed family `U` of exact-density DFs**, not an assertion about a larger, unspecified topology on all equilibria. The candidate states the former scope explicitly.

## Exact revision and sources

The raw candidate audited is `/private/tmp/cold_force_trace_route_20261019.md`, SHA-256:

`fbe1782f5e165001e0979eca662da2d0ba7f4171bec74959e09e25c27e539112`.

Repository root: `/Users/carlzimmerman/new_physics/zimmerman-formula`.

Source pins actually checked:

| Source under `real_research/analytic_review_2026_10_18_codex/` | SHA-256 |
| --- | --- |
| `smooth_exact_2026_10_18/EXACT_SMOOTH_INVERSE.md` | `490b137269ea5c918dae517085974752a3e1bc3d9df4f3e88b99eeccde41a55b` |
| `cold_dominated_feedback_2026_10_19/BOUNDARY_PAIRING.md` | `5b5f2f73d54b034fa014b6efbeeb9acb5cadd9a30f2f40340745569610bba23d` |
| `cold_dominated_feedback_2026_10_19/REGULAR_INVERSE.md` | `4830712683b98b46a53b796b4bde109c618a4fd26fa910cd47176ebe9f3ddf80` |
| `cold_dominated_feedback_2026_10_19/GEOMETRY_AND_CAP.md` | `c40c5f63e533fe19e41b996e292d21892160bf2b4aa31ffb499313b64f54fc0d` |
| `cold_dominated_feedback_2026_10_19/HIGH_FREQUENCY_INVERSE.md` | `6111b7f0f2e2ea0ef1ea80b81c1a1227374bedc270614c50698db830ade8d49c` |
| `cold_dominated_feedback_2026_10_19/THRESHOLD_MODES.md` | `40304ae8d1c0495cdd7482202aa9dcdfa494f12287754b7e648dd2adf26a77b5` |

No applicable `AGENTS.md` or `.mathbox/` ledger was found in the inspected repository/ancestor instruction locations. The proof-audit skill and its general logic, duality, and source obligations were applied. Prior audit summaries were not used as evidence for the conclusions below; raw proofs were inspected.

## Dependency graph

* Exact inverse's weighted source geometry, local Fourier identity, error bounds, and exponential endpoint flatness (internal source) -> continuous `A_den`, continuous smooth right inverse `B_den`, and exact nullspace projection.
* Exact source's strict low-tube relative height/derivative margins (internal source) + projection image in `H_low` -> an actual open family of positive monotone DFs with exactly fixed species densities and fixed potentials.
* Weighted smooth source estimates + fixed geometry + boundary source chart/tail estimates (internal source) -> one common Banach field space `Y=C^gamma(I)^2`, compact `K_F,+`, and affine norm-continuous dependence on `w=-F_E`.
* Continuous scalar pairing `B_phi` + annihilation of `ker A_den` + actual right inverse -> continuous radial-target functional -> radial distribution `chi`.
* Exact phase-space/action Jacobian + local radial-map submersion (internal definition/geometry) -> adjoint radial density extraction is the orbital average, including distributions -> (4.2), assuming (3.3).
* Compact Fredholm index zero + common-space norm continuity -> finite upper-semicontinuous nullity -> open dense locally constant loci.
* Fixed Fredholm complements + affine differentiability + locally constant nullity -> vanishing of every first kernel/cokernel entry.
* Scalar transversality (6.5), **not audited here**, + actual kernel/mode correspondence and cokernel identification (named internal source) -> (CF) on the finite intersection of those loci.

No dependency in these assigned steps returns to an assumed (CF), an assumed dynamic inverse at the threshold, or a full-rank perturbation matrix.

## Obligation matrix

| Obligation | Status | Decisive reason |
| --- | --- | --- |
| Signed right inverse is for every `X_infty` target | passed | Source identity and estimates are linear and target independent; residual positivity is not used. |
| Continuity of inverse on `X_infty` | passed | Bounded inverse on `X_5`, followed by the quantitative one-derivative-gain recurrence. |
| `B_den` takes values in `H_low` continuously | passed | Fourier costs are polynomial; a sufficiently high finite `X_s` controls each weighted source seminorm. |
| `A_den:H_low -> X_infty` continuous | passed | Uniform local tube geometry, finite intrinsic derivatives, and comparable nearby weights bound each output derivative by a finite source seminorm. |
| Projection is closed/exact/continuous | passed | `A_den B_den=I` gives the projection identities directly. |
| All small null directions are actual equilibria | passed | Exact densities and fixed potentials hold for the full linear variation; strict physical positivity/monotonicity follow from the relative margin. |
| Same physical support and smooth flat ends | passed | Variation is confined to the low tube; the high baseline stays positive, and exponential endpoint weight absorbs every fixed inverse-power coordinate cost. |
| Coercivity/energy norm stability | passed | Relative susceptibility control preserves norm equivalence and a strict coercive margin. |
| Common-space operator-norm continuity | passed | Boundary proof bounds are linear in finitely many smooth coefficient norms; those norms are controlled by finitely many `H_low` seminorms. |
| Continuous factorization through density | passed | The explicit right inverse supplies the quotient factorization, without a general quotient-space assertion. |
| Radial functional defines a distribution | passed | On every fixed compact radial interval, the test-function inclusion into `X_infty` is continuous. |
| Orbital-average adjoint with correct measure | passed | `dm=2*pi*C_Gamma*dJ*dL`; shell density is per `dr`, not per `dx`. |
| Distributional averaging near the circle | passed | At fixed positive `J`, `partial_s r=1+O(sqrt(J))` gives a submersion for every angle on a small chart. |
| Nullity upper semicontinuity and dense local constancy | passed | A fixed Fredholm Schur block proves upper semicontinuity; minimum integer nullity in any nonempty open set proves density. |
| Constant nullity forces zero first Schur pairing | passed | The remaining square matrix has dimension and nullity both `m`, so is identically zero along every small admissible line. |
| Scalar transversality and its local blow-up | out of scope | Separate auditor assigned; retained as named assumption. |
| Correctness of (3.1)/(3.3) | out of scope | The assigned factorization audit starts from this continuous scalar functional/distributional identification. |
| Full closed-support work theorem | out of scope | Not a consequence certified by this bounded audit. |

## Detailed decisive checks

### 1. The exact inverse is not restricted to the baseline residual

In `EXACT_SMOOTH_INVERSE.md:150--179`, `A_den R_delta=I+E_delta` is a linear operator identity on the weighted Sobolev spaces; the smallness is imposed only on `X_5`. For arbitrary `e in X_infty`, write `Qe=(I+E_delta)^(-1)e`. The base estimate is

`||Qe||_X5 <= 2 ||e||_X5`.

For every integer `s>=6`, the source's gain implies

`||Qe||_Xs <= ||e||_Xs + C_s ||Qe||_X(s-1)`.

Induction gives a continuous seminorm bound at every finite order. Thus the bootstrap proves continuity, not merely pointwise smoothness of the solution. It does not require one choice of delta making `E_delta` small in every norm.

For the reconstruction, a `t` derivative of order `a` and a `y` derivative of order `b` cost at most a constant (depending on the fixed delta and order) times `<n>^(2a+b+2)` in the Fourier summand. A finite `X_s` with `s>2a+b+5/2` controls the absolute coefficient sum by Cauchy--Schwarz. Finite chart overlap and `u(j)~u(y)` on each chart give the candidate's weighted supremum seminorms. This also applies to all derivatives at physical `t=0`. Each summand is flat at its upper support endpoint; at the common endpoint `delta^2/4` only the largest-width summand reaches the endpoint, and it is flat there. Uniform differentiated convergence supplies the same property for the sum. This establishes continuous `B_den=R_delta Q:X_infty -> H_low`.

The source integral at `EXACT_SMOOTH_INVERSE.md:65--99` has no remote tube pieces: on its support `|x-y|<=C delta`, and the rescaled velocity range is uniformly bounded. Its `x` derivatives are finite sums of derivatives of `H` times uniformly bounded intrinsic derivatives of `W`. Nearby `u(y)` and `u(x)` are comparable. Thus every localized weighted `H^s` output norm is bounded by a finite `p_m(H)`. This proves the claimed continuous `A_den` mapping.

Consequently `Pi=I-B_den A_den` satisfies `A_den Pi=0`, `Pi^2=Pi`, and `Pi V=V` for `V in ker A_den`. Its image equals the closed kernel of continuous `A_den`. All identities hold for signed real targets and seeds.

The candidate explicitly uses physical half-strip smoothness at `t=0`, with an extension through that edge and no lower vanishing condition. That reading is necessary and is already stated at raw lines 60--70. Reading `H_low` as globally smooth functions supported in `t>=0` would incorrectly impose flatness at `t=0` and would not contain `R_delta`; the candidate expressly excludes that reading.

### 2. The perturbation family contains actual equilibria

At fixed delta, sufficiently small `p_1(V)` gives both `|V|` and `|V_t|` smaller than fixed fractions of the margins in raw line 85, with the appropriate delta factors. Multiplication by the fixed positive conversion prefactor and division by `sigma=kappa^2 h^2` preserve the signs. Thus `F_*+F_V>0` and `-(F_*+F_V)_E>0` throughout the physical low tube. Above it the baseline is unchanged. Positivity extends through `t=0`; it is strict in the original occupied physical set and zero only at its support boundary. There is no positive uniform lower bound in unweighted physical coordinates near the flat radial ends, nor is one needed.

For every null parameter, `mu_(F_*+F_V)=mu_*` is an exact linear identity, not a first-order identity. Each species' cumulative density and therefore the actual coupled potentials remain fixed. A smooth invariant distribution `F(E,L)` in those same potentials is stationary. The positive high-tube baseline and the preserved low-tube signs leave exactly the same occupied physical support. All derivatives introduced by converting `(t,y)` to `(E,L)` cost only finitely many inverse powers of `h` or endpoint distance. Source line 49 and lines 220--228 show that `u` absorbs these costs and gives smooth zero extensions at the physical ends. This reasoning applies to every source in `H_low`, not just to Fourier-reconstructed ones, because all its derivatives have the same relative weight.

On the low tube, `|delta w|<=epsilon w_*` follows from the derivative margin; elsewhere `delta w=0`. Hence `1/w` changes by a uniformly small relative factor. The original strict coercive energy inequality therefore persists after reducing the neighborhood. This provides the actual common geometric/source hypotheses for all parameters in `U`.

The signs and support here concern the physical invariant domain. As in the exact source, a smooth continuation to inaccessible values below `t=0` is auxiliary and does not impose an artificial physical cutoff.

### 3. The boundary pencil varies continuously on one fixed space

The common field space is `Y=C^gamma([r_0,R])^2`, `0<gamma<1/2`, fixed independently of the DF. At fixed potentials the boundary source formula `BOUNDARY_PAIRING.md:75--80` is linear in `w`. Its local chart estimates (lines 141--179) depend on finitely many smooth coefficient norms of `w`; the nonresonant tail (lines 239--270) is controlled linearly by its finite integral/supremum bounds. Signed coefficient differences are permitted in these norm estimates: positivity is used later for the optical zero, not for this continuity estimate.

For any prescribed finite ordinary-action derivative order of `delta w`, the chain rule gives a bound by a finite `H_low` seminorm times `u` and finitely many inverse powers of `h` and endpoint distance. Exponential flatness makes the resulting unweighted coefficient bound finite. In particular there are finite `M` and `C` at the fixed geometry/delta such that

`||K_(F+V),+(nu_c)-K_F,+(nu_c)||_(Y->Y) <= C p_M(V)`.

The same construction remains affine in `V`, so every parameter line is differentiable in operator norm. `P:Y^x -> C^(1-gamma)` and compact inclusion into `Y` are the fixed maps proved at `BOUNDARY_PAIRING.md:320--358`. Thus each `I-K_F,+` is Fredholm of index zero on this one common space. Comparing varying energy norms is not being substituted for field-space operator-norm continuity.

### 4. Density factorization and the adjoint have the claimed types

Let `Lambda(V)=B_phi(F_V)` be the continuous scalar functional from (3.1). Continuity follows either from its identification as a kernel/cokernel entry of the continuous linear pencil variation, or directly from relative `delta w/w` control and the fixed mode's energy integrability. Suppose `Lambda` annihilates `N_den`. The exact decomposition

`V=Pi V+B_den A_den V`

then gives `Lambda=L A_den` with continuous `L(rho)=Lambda(B_den rho)` on `X_infty`. This uses the actual right inverse rather than an unproved closed-range/quotient identification.

For a compact radial interval `K` in the open shell, `f(r) -> rho(x)=f(r(x))` is a continuous map from tests supported in `K` to `X_infty`: only finitely many intrinsic charts meet its transformed compact support, and all coordinate/weight factors are smooth and bounded there. Consequently `f -> L(f composed with r)` defines a radial distribution `chi`. Its action is paired with shell density per `dr`, as required by `EXACT_SMOOTH_INVERSE.md:78`.

For ordinary smooth `chi`, the exact identity is

`integral chi(r) delta mu(r) dr = C_Gamma integral chi(r) delta F(E,L) dr dv dL`

`=2*pi*C_Gamma integral delta F(J,L) average_theta chi(r(theta,J,L)) dJ dL`.

Thus there is no missing `h`, `Omega`, or `2*pi` in (4.1). For distributions, a sufficiently small circular chart has `partial_s r=1+O(sqrt(J))`, uniformly in angle, so this derivative is bounded away from zero. On `J>0` all maps are smooth. The pullback of `chi` by this submersion and its angle integral are therefore defined by ordinary test-function changes of variables. Compact tests in this chart correspond to allowed low-tube source seeds after multiplication by the smooth invariant prefactor. Assuming (3.3), testing against all such seeds yields precisely `S_phi=chi_bar` as distributions on that chart. The smooth positive `L_c'(s)` density when changing `L` to `s` does not alter this equality.

This audit establishes the factorization implication; it does not supply the separate weak circular limit or blow-up contradiction.

### 5. Scalar transversality is enough; matrix surjectivity is unnecessary

For fixed `nu_c`, use complements for the Fredholm operator at one parameter. Its complement-to-range block stays invertible in an operator-norm neighborhood, and kernel nullity equals the nullity of the finite `m by m` Schur block. This proves upper semicontinuity. Given any nonempty open parameter set, the nonempty set of integer nullities has an attained minimum. At a minimizing point upper semicontinuity provides a smaller open neighborhood with that same value. Hence the locally constant locus is open dense without a Baire theorem. A finite intersection of such loci is open dense, including coincident threshold frequencies, which are simply one member of the finite frequency set.

At a point of local constant nullity `m`, choose kernel/range complements at that point. The Schur block has nullity `m` throughout a small parameter neighborhood, so it is the zero `m by m` matrix there. Its derivative along every null-DF line vanishes. Since the off-diagonal blocks vanish at the base parameter, its derivative is exactly the projected `A'_F` kernel/cokernel block; the quadratic entry associated with any mode is therefore zero. The concrete cokernel identification by `ell_h` is the raw source theorem at `REGULAR_INVERSE.md:237--250`.

If (6.5) holds for every actual bad-force-trace mode at every parameter of `U`, any such mode would supply a direction with a nonzero derivative entry, a contradiction. The case `m=0` is vacuous. Multiple modes, multiple circles at the same frequency, and species-specific null variations cause no loss: the contradiction needs only one nonzero scalar entry associated with the alleged bad mode. This establishes the exact genericity conclusion conditional on (6.5).

## Remaining gap, strongest safe statement, and cheapest next check

No additional missing implication was found in the assigned Sections 2, 4, and 7. The remaining new mathematical obligation for the full candidate is the independent verification of (3.1), (3.3), and scalar transversality (6.5), especially the weak circular limit and the distributional blow-up comparison. This report does not convert those separately assigned steps into assumptions silently.

The strongest safe statement from this bounded audit is: **the raw candidate's exact-density parameter family is an actual open family of equilibria, its density-null factorization is valid, and if its stated scalar transversality holds, an open dense subset relative to that family satisfies (CF).** The cheapest next check is to combine this report with the separately assigned raw-proof audit of the scalar functional and Sections 5--6. No numerical experiment is needed or probative for those steps.

## Commands and provenance

The artifact and source hashes above were read with `shasum -a 256`. Source text was inspected with `cat`, `nl -ba`, `sed`, and `rg`; instruction/ledger discovery was read-only. The only written artifact is this report. No scientific calculation was delegated to code. This is an independent bounded derivation by a fresh subagent from the raw proof and exact source artifacts; it is not an independent certificate for the full candidate or its scalar transversality leaf.
