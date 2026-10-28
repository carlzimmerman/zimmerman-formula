# Independent audit of the coarse-reduction candidate

**Primary verdict: proved as written.** This verdict applies to the finite-coordinate comparison theorems, exact examples, and explicitly conditional normalized-Schur statements in the precise revision below. It does **not** establish the requested actual Yang--Mills whole-layer estimate, a bound uniform under physical rescaling, or a mass gap. The actual-vacuum successive-marginal score bounds and the stated infinite-dimensional graph/domain inputs remain assumptions.

Reviewer: `/root/audit_layer_coarse`, a fresh audit subagent distinct from the author. Date: 2026-10-28. The reviewer reconstructed the main inequalities and the normalized-subspace identification from the raw candidate. This is an AI-assisted independent derivation within the same overall project, not independent human peer review or a formal proof-assistant verification.

## Exact revision and normalized claims

Audited file: `../coarse/PROOF.md`.

SHA-256: `9b5e3ab243086577f40546d6a7e1aced55d8c53f981f7b19856a685075a5eb05`.

The project HEAD observed during the audit was `1180f5e8a4dae9b0513a6e40e453c58b19760a40`; concurrent unrelated work has changed HEAD since the program checkpoint. The file hash, rather than that moving HEAD, identifies this review's mathematical target. No candidate file was edited by this reviewer.

The claims audited are:

1. For a smooth strictly positive density on a finite compact product, a conditional gradient Poincare bound `lambda` and a centered-score covariance bound `M^2` imply the one-step form comparison (3)--(5), with `beta=M^2/lambda` and fixed energy coefficient `t`.
2. For finitely many nested coordinate conditional expectations, those inputs imply (6)--(9). The metric-normalized identification and (10)--(11) are finite-dimensional statements, with the explicitly named additional bounded-graph and closed-form-domain hypotheses required in infinite dimension.
3. A uniform pointwise density-ratio bound for a fixed original block is inherited by every coordinate marginal with exactly the same ratio. Consequently the published actual-vacuum bounded-block inequality applies to all such marginals, at the original `x,a,N,b` and original block geometry.
4. Uniform successive-marginal bounded-block Poincare inequalities and score bounds (13) imply the triangular influence estimate (14)--(16), including the stated whole-layer conditional application.
5. The specified four-state reversible form yields a Schur form and normalized Schur form which fail the Markov contraction property.
6. The boundary-trace example shows that an energy bound on a graph map alone does not imply its closability in the retained `L^2` norm.

All gradient inequalities are over the indicated full coordinate spaces. They therefore also bound any gauge-invariant subspace to which the relevant projections and forms restrict; they do not manufacture a nontrivial terminal physical excited sector.

## Dependency graph

- Original actual-vacuum oscillation estimate -> pointwise bound for `psi(u,v,z)^2` -> integration in the same `v` variables -> marginal ratio (19) -> Haar Poincare comparison -> (20)--(21).
- Conditional Poincare + centered-score covariance -> differentiation of conditional expectation -> (3) -> constrained minimization -> (4)--(5).
- One-step estimate + tower property of the original conditional expectations -> associativity of variational reductions -> (6)--(8) -> orthogonality of martingale differences -> (9).
- Bounded graph maps and the stated exact closed-form domain decomposition -> normalized isometric graph representation -> the changed discarded subspaces `W_i` -> (10) and unitary equivalence of successive normalized reductions -> arithmetic identity (11).
- Successive-marginal score bounds + repeated conditional differentiation -> triangular inequalities for `w_i` -> a nonnegative nilpotent inverse -> (15), then the matrix norm bound gives (16).
- Exact finite weighted form and partition -> its block matrices -> exact Schur and metric matrices -> a positive off-diagonal entry and an absolute-value contraction violation.
- Trace boundedness on `H^1` + boundary-layer sequence converging to zero only in `L^2` -> the graph-map nonclosability example.

There is no circular use of a global gap to establish the local hypotheses. The needed score hypotheses are not claimed to follow from the original oscillation estimate.

## Obligation matrix

| Obligation | Result | Reason and scope |
|---|---|---|
| Conditional derivative identity | Passed | Differentiating both numerator and conditional normalization gives the centered score, with the displayed positive covariance term. |
| Operator covariance norm versus trace | Passed | Cauchy--Schwarz is applied after pairing with a unit tangent vector; a trace estimate is unnecessary. The same operator bound extends to complex functions by complexification. |
| One-step constant and physical coefficient | Passed | `sqrt(E|grad_Y f|^2)+M sqrt(Var_X f)` is bounded by `sqrt(1+M^2/lambda)` times the full gradient norm. The common coefficient is exactly `t`. |
| Minimizer existence and form domain | Passed | On `ker P`, the conditional Poincare bound controls `L^2` by energy. Smooth positive densities on each fixed compact product give the required Sobolev equivalences; the affine constrained minimization is coercive. |
| Graph-energy identity | Passed | Form orthogonality of `u-Cu` to `ker P` gives `e[Cu]=e[u]-s[u]`; no incorrect `L^2` orthogonality is substituted. |
| Nested associativity | Passed | `E_{i+1}=P_i E_i` and minimization over the intermediate constraint yield the exact variational identity. |
| Accumulated metric bound | Passed | Each increment lies in `H_i` orthogonal to `H_{i+1}`. All its relevant minimized energies equal the final `s_j[u]`, so the squared norms add as in (9). |
| Normalized discarded-subspace identification | Passed under the displayed analytic conditions | The discarded space changes to `G_i^(1/2) Q_i`; it is not the original coordinate projection on `K_i`. See the reconstruction below. |
| Infinite-dimensional bounded graph/domain hypotheses for actual Yang--Mills | Not established by this candidate | The manuscript explicitly leaves them as additional inputs. Equation (8) does not prove them. |
| Density-ratio inheritance | Passed | The numerator inequality holds for each identical integrated configuration `v`; integration preserves it. Conditional normalization cancels. |
| Successive-marginal triangular recurrence | Passed | Conditional derivative identities telescope in `L^2`; each covariance error is bounded by `M_ki w_k`. |
| Dimension-independent matrix conclusion | Passed under its stated hypotheses | Nilpotence justifies the finite nonnegative inverse; the norm estimate uses `||R||<1`, not entrywise smallness alone. |
| Actual weak-coupling score-matrix bound | Not established by this candidate | It is the principal missing actual-model input. Fixed-block density oscillation does not supply it. |
| Four-state normalization and Markov witness | Passed | The transformed weighted mass is `I/3`, and the specified generator and Schur matrices have the stated signs and eigenvalues. |
| Unbounded graph-map example | Passed | The closed fine form coexists with `u_n -> 0` in `L^2` and `Cu_n -> 1`; the claimed nonclosability follows directly. |
| Continuum limit, coupling trajectory, novelty | Out of scope / not asserted | None is inferred from the valid comparison theorems. |

## Decisive reconstructions

### Marginal inheritance

For all `u,u',v,z`, the predecessor gives

`psi(u,v,z)^2 <= R_B^2 psi(u',v,z)^2`.

Integrating in `v` against the same product Haar measure yields (19) immediately. The two sides use the same original `x,a,N,b`, the same set of original links `B`, and the same original plaquette count. Comparing the resulting conditional density to product Haar gives a factor `R_B^2/C_F`, not a new factor per eliminated coordinate or per marginalization step. This establishes a genuine unconditional stability property of the actual finite-volume vacuum under **coordinate marginalization**. It says nothing about a transformed coarse holonomy, a newly rescaled lattice, or a normalized Schur operator.

### Triangular recurrence

For `i>k`, let `b_i^(k)=||grad_{X_i} f_k||_{L^2(mu_k)}`. The conditional derivative identity and (13) give

`b_i^(k+1) <= b_i^(k)+M_ki ||f_k-f_(k+1)||`.

The covariance is with `f_k-f_(k+1)`, so its variance is precisely the conditional contribution whose integrated norm is `w_k`. Telescoping gives the displayed bound before (14). Conditional Poincare then gives `w <= D a + Rw`, with `D=diag(lambda_i^(-1/2))`. Because `R` is finite, strictly lower triangular, and nonnegative, iteration gives `w <= (I-R)^(-1)Da` componentwise. Orthogonal martingale differences give the variance identity. These steps establish (15). If `||R||<=r<1`, the Neumann norm bound and `lambda_i>=lambda_*` establish (16). The same derivation can be run at each fixed layer exterior when every hypothesis is uniform in that exterior.

### Correct normalized subspaces

Since the global minimizing lift `J_i` preserves its coordinate conditional mean, `J_i^*J_i >= I`, and `J_i 1=1` also implies `G_i 1=1`. For bounded `J_i`, its graph metric is bounded and boundedly invertible. In the normalized coordinates,

`W_i = G_i^(1/2) Ran Q_i`,

`W_i^perp = G_i^(-1/2) H_(i+1)`.

Writing a retained representative as `r=G_i^(-1/2)p` with `p in H_(i+1)`, its image after applying `G_i^(-1/2)` has retained coordinate `P_i G_i^(-1)p`. The compression `P_i G_i^(-1) P_i` on `H_(i+1)` is positive and boundedly invertible. Thus every coordinate constraint is represented exactly once, while varying by `W_i` becomes varying by `Ran Q_i`. Minimization therefore produces the same graph subspace `J_(i+1)H_(i+1)` in the original Hilbert space. The two normalized constructions are isometric parametrizations of that subspace and are unitarily equivalent. This verifies the finite-dimensional assertion and its stated domain-qualified extension; it does not remove those domain conditions.

For `w=G_i^(1/2)q`, (9) gives

`||w||^2 <= ||q||^2 + E_i s_i[q] <= (d_i^(-1)+E_i) s_i[q]`,

which proves (10). Summing the accumulated `E_i` counts each `epsilon_k` exactly `n-1-k` times, as in (11).

### Exact finite obstruction

Direct substitution into the original four-state form gives

`3 h = (a-b)^2+(a-c)^2+2r(c-b)+4r^2`.

Thus `B=(0,-1,1)`, `D=4`, and the stated `S` and `G` follow. On `u=(0,1,-1)`, the normalized form is `8/27`; on `|u|=(0,1,1)`, it is `2/3`. A Dirichlet form cannot increase under this normal contraction. The counterexample therefore refutes automatic Markov closure in the retained probability representation, while preserving the constant zero-energy vector. It is not a counterexample to Yang--Mills itself.

## Source and computation checks

The predecessor's ground-state form, oscillation bound, and Haar comparison were read in:

`../../papers/yang_mills_bounds_2026/sections/vacuum.tex`

SHA-256: `45b33bb7448c25ba0323b38478febd63ccc34958271cd1869e5facd09df872e0`.

The stated closed-form Schur domain assumptions were checked against:

`../../papers/yang_mills_bounds_2026/sections/schur.tex`

SHA-256: `a1907e99c6174dedd4ab85d00e9f74fc18b4ffec2eff9df0e30b1f0cc6a3f169`.

This review checks the new implications from those explicitly identified predecessor statements; it does not purport to be a new whole-paper audit of all earlier external source leaves.

The exact rational checker was read and rerun:

```text
python3 real_research/yang_mills_layer_2026_10_28/coarse/verify_exact.py
```

It exited successfully and reported `S_BC=1/4`, `K_BC=5/18`, and normalized eigenvalues `0,4/9,3`. Its implementation also reconstructs the weighted mass and energy matrices from the original four-state definition. The previously recorded computation manifest was inspected. This finite check supports only that single exact counterexample; the analytic estimates are supported by their derivations, not by that computation.

## Strongest safe statement and next obligation

The actual finite-volume Yang--Mills bounded-block conditional estimate survives every coordinate marginalization with unchanged constants. Combining those inherited bounds with a separately proved, exterior-uniform influence matrix norm `||R||<1` would produce a layer-cardinality-uniform conditional gap. The candidate does not prove that influence bound, and its inherited local constants retain their weak-coupling loss. Exact normalized Schur iteration additionally needs the specified analytic domain inputs and useful control of the accumulated metric; the displayed cost identity alone provides no depth-uniform result.

The cheapest meaningful next actual-model check is therefore an explicit estimate or counterestimate for the conditional score matrix of **successive marginals of the actual vacuum**, with the block geometry, exterior conditioning, coupling range, and norm all specified. Replacing that object by the bare plaquette interaction or by a Gaussian covariance without a comparison theorem would not discharge this obligation.

## Addendum: fixed-volume graph-domain extension

After the original review, the root investigator supplied a separate candidate, `../coarse/DOMAIN_EXTENSION.md`, SHA-256 `a821a8d084dd6d13dc2ccd43ca5d63a28aed54c9834ca9fb56ff509ca3ad8e5b`. Its written theorem and its restricted nested-coordinate corollary have now been independently audited and are **proved as written**. This addendum strengthens the earlier domain status for original product-diffusion splits; it does not change the missing uniform influence or accumulated-metric inputs.

The additional hypotheses are essential: compact **boundaryless** product geometry, a smooth strictly positive density, and the original weighted gradient form. With `sigma` and `S0,S1` defined in that artifact, differentiating `Pq=0` for `q` in `QH^1` gives `P grad_Y q=-P(q sigma)`. The cross form is therefore first order in the retained variable. Integrating that derivative onto `sigma conjugate(q) rho` gives precisely (D3), with the displayed sign and divergence term.

The resulting estimate is

`|b(u,q)| <= sqrt(t) (S0+S1/sqrt(lambda)) ||u|| sqrt(e[q])`.

There is no hidden factor from the marginal density: the full `L^2(mu)` norm of a function `u(Y)` is exactly its `L^2(nu)` norm. Riesz representation in the complete space `QH^1` equipped with the energy inner product then gives an extension `C:L^2(nu)->QH^1`, and conditional Poincare yields exactly

`||C|| <= S0/sqrt(lambda)+S1/lambda`.

For `u` in `H^1`, the extended functional agrees with the original mixed form, so this is the actual variational graph correction, not a different extension chosen for convenience. Constants have zero cross form, hence `C1=0`. Because both `P` and `C` preserve the required `H^1` domains at this fixed graph, the domain equality in (D2) follows in both directions. It matches the predecessor's closed-form Schur hypothesis exactly. The one-step normalized coarse form therefore exists as the closed transported form specified there, unconditionally for every fixed finite actual-vacuum coordinate split and fixed `x>0`.

For nested coordinates, the statement `j_i=E_i J_(i+1)` is also correct. If a finer competitor had the same `E_i` mean and lower energy than `J_(i+1)u`, the tower property would make it an admissible lower-energy competitor for the `E_(i+1)` constraint, contradicting its minimizing property. Thus `J_i j_i=J_(i+1)` on the form domain and then by the proved bounded extensions. Consequently `C_i=E_i C_tot,i+1`, and the fixed-graph `H^1` boundedness of `E_i` proves the claimed intermediate correction regularity. The unnormalized intermediate square completion has the stated domain.

No issue was found in this extension. Its constants need not be uniform in volume or coupling, and the author correctly does not claim to have checked all transported-subspace domain details for the repeated **normalized** iteration. The abstract trace counterexample remains valid: the new positive theorem uses structural hypotheses absent from that counterexample.
