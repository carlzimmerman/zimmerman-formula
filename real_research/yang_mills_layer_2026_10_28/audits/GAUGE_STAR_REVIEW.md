# Independent audit of the gauge-star scope bound

Date: 2026-10-28. Reviewer: isolated proof-audit subagent
`/root/audit_layer_obstructions`. The candidate was not edited.

**Normalized claim.** For the actual finite-volume SU(N) vacuum with
N >= 2, x > 0, a > 0, the specified Casimir metric, and full independent
vertex gauge symmetry preserving the boundary conditions, let F include
every link incident to v and include an edge l with distinct endpoints,
one of which is v. For the conditional expectation P onto all links
outside F, the ground-form compression to ran(I-P) satisfies
`inf spec(D_F) <= t C_F`, where `t=x/(2a)`. Separately, the marginal
of a fully gauge-invariant probability measure on any forest of link
variables is product Haar, and its gauge-invariant cylinder functions
are constants.

**Primary verdict: proved as written.** This is a theorem about the full
kinematic discarded space and about coordinate marginals. The charged
trial function is excluded from the physical gauge-invariant subspace.
The candidate correctly refrains from transferring its upper bound to
that physical spectrum. No correction is required.

## Exact revision and dependency graph

Candidate:
`real_research/yang_mills_layer_2026_10_28/gauge_star/PROOF.md`.
Audited SHA-256:
`4386f33157d9eb717644b93ca3a3f3a0e9765dfee98d43cf4f21d8c9ff972316`.

The definitions imported from
`real_research/papers/yang_mills_bounds_2026/sections/vacuum.tex`
were read directly: finite product SU(N)^E, oriented edge representatives,
fundamental Casimir `C_F=(N^2-1)/(2N)`, actual positive gauge-invariant
vacuum, its weighted gradient form, and the form-compression definition
of D_F. That file's previously pinned hash is
`45b33bb7448c25ba0323b38478febd63ccc34958271cd1869e5facd09df872e0`.

Dependencies:

1. Actual vacuum gauge invariance plus full-star geometry -> invariance
   of each conditional F fiber under the action at v -> a fundamental
   matrix coefficient lies in ran(I-P).
2. Gauge invariance at either distinct endpoint -> Haar one-link
   marginal -> trial norm and derivative energy -> Rayleigh upper bound.
3. Full vertex action on forest assignments is transitive -> unique
   invariant probability -> product Haar marginal and constant invariant
   cylinder functions.

All new steps are internal representation and measure arguments. No
unproved influence estimate, coarse-operator identification, numerical
evidence, or continuum limit is used.

## Obligation matrix

| Obligation | Result | Reason |
|---|---|---|
| Gauge action fixes the conditioned exterior | Passed | Every link incident to v belongs to F, so a transformation only at v fixes all exterior link variables. |
| Conditional law invariance | Passed | The positive smooth density and product Haar measure are invariant under the fiber action; its normalizing integral is unchanged. |
| Q-admissibility of the trial | Passed | The average of a nontrivial fundamental matrix coefficient under left or right SU(N) multiplication is zero. |
| Nonzero trial norm | Passed | A distinct-endpoint link has Haar marginal and each matrix coefficient has squared norm 1/N. |
| Energy normalization | Passed | With the imported generator normalization, the fundamental Casimir is C_F and only derivatives on l contribute. |
| Form domain | Passed | The trial is smooth on the finite compact product and belongs to the conditional Q subspace; the variational principle needs only this form domain. |
| Full parameter range | Passed | The proof needs x,a positive and the stated gauge symmetry, but no small- or large-coupling approximation. |
| Forest marginal | Passed | Gauge transformations act transitively on forest assignments; product Haar is invariant, and the invariant probability on this compact homogeneous space is unique. |
| Forest physical observables | Passed | Transitivity forces any invariant function of the forest links alone to be constant, in the appropriate almost-everywhere sense. |
| Physical discarded gap | Out of scope | The trial is charged; the full-space upper bound does not bound the bottom of a smaller physical subspace from above. |
| General boundary conditions or self-loops | Out of scope | Full vertex symmetry and distinct endpoints are explicit hypotheses. |

## Independent reconstruction

Write the gauge action as `U_l -> g_s U_l g_t^{-1}`. With an exterior
configuration fixed and g nontrivial only at v, the integrand density is
unchanged because no exterior edge is incident to v. Averaging the
fundamental coefficient `(U_l)_{ij}` over this action gives zero. The
normalized conditional integral therefore vanishes at every exterior
configuration, not merely in its global mean. This is the necessary
admissibility step for the discarded operator.

For the one-link marginal, other edges also transform at the selected
endpoint, but they are integrated out. Invariance of the full measure
therefore implies invariance of the marginal under every left translation
of U_l, or every right translation if the selected vertex is its target.
Distinct endpoints allow the other endpoint transformation to be held
at the identity. Uniqueness of normalized Haar gives the marginal.
Haar invariance and row unitarity give `integral |U_ij|^2=1/N`.

The imported Casimir convention gives
`-sum_alpha X_alpha^2 U_ij=C_F U_ij`. Haar integration by parts then yields
`integral sum_alpha |X_alpha U_ij|^2=C_F/N`.
Since the function depends on no other edge, its quotient for the full
weighted gradient form is exactly `t C_F`. It lies in the actual Q
subspace, so the variational upper bound follows without substituting
a fiber form or dropping derivatives of a more complicated function.

For a forest, choose one root in each connected component and fix its
gauge group element. Recursively choose the group element at each next
vertex to map the corresponding edge assignment to any desired target
assignment. Absence of cycles ensures there is no conflicting equation.
The gauge transformations can also change edges outside the forest,
which does not affect marginal invariance because those variables are
integrated out. Product Haar is invariant under the induced forest
action; compact-group averaging proves uniqueness of its invariant
probability. This proves joint product Haar, not only one-link Haar
marginals.

If both `D_F >= c/a` and the audited upper bound held for all small x,
then `c <= x C_F/2`. A fixed positive c is incompatible with x tending
to zero, even if a also varies. This restriction applies only to the
full kinematic space with the stated star geometry. An order-x/a lower
bound is compatible, and no conclusion about a physical Yang--Mills
mass gap follows from this charged trial.

## Remaining gap and provenance

No missing implication was found in the stated result. No numerical
test is needed for this exact compact-group argument. The next relevant
research obligation is to formulate and prove the intended layer bound
with its physical sector and coarse observable algebra explicit; this
scope bound cannot replace such an estimate.

The audit was reconstructed from the candidate and its imported
definitions in a separate subagent. It is AI-assisted independent review
within the same session, not independent human peer review and not a
novelty determination.
