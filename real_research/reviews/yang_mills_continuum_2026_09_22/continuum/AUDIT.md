# YM-C1-C self-review

Verdict for C1--C4 and the explicit counterexamples: **proved as written**
under the displayed hypotheses. Verdict for the requested Yang–Mills
construction: **conditional on a named input**, namely CT and the actual
weak-coupling estimates (12) and (8), plus the remaining QFT axioms.

This was a separate adversarial self-review by the author, not an independent
agent audit. It applies to `PROOF.md` in this directory only.

## Dependency graph

    CT + dense one-time contraction (4) -> C1
    CT + cutoff physical gap bounds -> C2 -> C1
    common asymptotic rate on total set -> C2b
    C1 + positive correlation/bounded norm (8) -> C3
    bounded Rayleigh quotient/positive norm (9a) -> witness (8)
    CT + diverging cutoff gaps -> C4 -> trivial cyclic limit
    I15 strong-coupling input + a->0 -> diverging physical gaps
    assumed beta expansion (14) -> integrated asymptotic (15)
    root block estimate (13), if proved + CT -> C2

Leaves: the spectral theorem, bounded-operator continuity, density, Jensen's
inequality, and elementary calculus are internal mathematical ingredients.
I15 is inherited input, JW is an authenticated target definition, and CT,
(12), (8), and applicability of (13) are unproved Yang–Mills obligations.
No numerical calculation is a proof dependency.

## Obligation matrix

| Obligation | Result | Check |
| --- | --- | --- |
| Correct energy scaling | Passed | K=(H_lat-E_lat)/a; time is t/a in lattice units |
| Actual vacuum centering | Passed | (2), orthogonality, and reduction by Omega stated |
| Full observable coverage | Passed | Dense vector subspace in C1; total set sufficient only for asymptotic C2b |
| Uniform constants | Passed | Common q,tau or decay rate; observable-dependent prefactors explicitly allowed where valid |
| Limit interchange | Passed | n limit at fixed t first; spectral theorem or strong continuity used afterward |
| Vacuum uniqueness | Passed | [0,m_0) excluded on Omega-perp, including zero |
| Finite mass/nonzero sector | Passed | (8) yields C3; C3b quantifies bounded-energy spectral weight |
| Coincident field divergences | Passed conditionally | Time-regularized contract stated; density of regularized vectors proved where underlying vectors exist |
| Strong-coupling collapse | Passed | Bounded regularized Gram norm times exp(-m_n t) tends to zero |
| Gapless limiting example | Passed | Multiplication spectrum [0,1], unique vacuum, operator-norm convergence |
| One-observable example | Passed | Gapless orthogonal summand excluded from chosen algebra |
| One-time basis example | Passed | Exact exponential inequalities; offending linear combination exhibited |
| Beta asymptotic signs | Passed conditionally | Reciprocal beta has -1/(beta_0 g^3)+beta_1/(beta_0^2 g); (15) has the resulting negative power |
| Magnetic coefficient normalization | Passed | beta_i distinguished from b_N; no universal numerical coefficients borrowed |
| Continuum Yang–Mills existence | Not addressed by transfer lemma | CT and full field construction are not established |
| Weak-coupling contraction | Not proved | I15 x>=X_d does not cover x(a)->0 |
| Root block route | Conditional | (13) quoted only as an input, not verified here |

## Adversarial checks

1. Dropping a common rate is refuted by energies 1/j.
2. Dropping dense coverage is refuted by a hidden multiplication-operator
   sector. Merely testing a basis at one time is separately refuted.
3. Dropping strong continuity allows the discontinuous n->infinity limit of
   diag(1,exp(-nt)); this explains why C4 must name that property.
4. Dropping a positive correlation witness allows a one-dimensional vacuum
   limit, satisfying gap exclusion vacuously.
5. Treating arbitrary trial vectors as continuum observable vectors would
   leave a gap in C3b's application; this is explicitly excluded.
6. Extending a polynomial lower gap to an asymptotically free continuum
   trajectory forces collapse, rather than proving the intended mass scale.

## Proofreading and validation

Applied the mathbox proof-audit and proofread-math workflows. The proofreading
skill's short `checklist.md` link resolved to `references/checklist.md` after
an initial missing-file read. Reviewed the changed mathematical prose,
equation references, hypotheses, and source links. A typographical adjacent
`>` and `>=` in C3b was separated; no mathematical claim was altered by that
correction. No other unresolved notation issue found.

Commands: source I15 compared to assigned base with `git diff` (empty diff);
input and artifact identities computed with `shasum -a 256`; all route files
read after creation. No test suite or floating-point script was run, because
the relevant counterexamples and inequalities are exact analytic proofs.

Next mathematical check: independently derive C1 and C3 from their raw
hypotheses, then decide whether the block-route construction actually produces
the convergent local-observable witnesses needed for (8), rather than only
abstract low-energy vectors.
