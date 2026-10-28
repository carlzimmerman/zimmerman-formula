# Self-audit of tensorization-route claims

Date: 2026-10-28. Scope: PROOF.md sections 2–6. This is self-review, not an
independent certificate. Primary target verdict: **conditional on a named
input** (actual influence summability and exact-coarse stability).

## Claim cards and dependency checks

| Claim | Quantified scope and conclusion | Verdict |
|---|---|---|
| T1 | Finite equal-size SU(N) blocks, actual conditional law at every exterior, actual Dobrushin spectral radius ≤q<1, one-block gradient gap λ0 ⇒ full discarded-layer form gap x(1−q)λ0/(2a) | Proved as a conditional implication; actual influence assumption unproved |
| T2 | Smooth positive measure on finite compact connected product, uniform conditional λ_i, mixed Hessian bounds h_ij, matrix ≥ρI ⇒ gradient Poincaré gap ≥ρ | Proved as written by block integration and discrete spectrum |
| T3 | All M, compact gauge-invariant mixture measures with fixed ε, local bounds uniform at each fixed block size, collective physical gap ≤12/(ε²M) | Proved as written; not a local-Wilson counterexample |
| T4 | Actual two-square SU(2) Wilson ground measure, sufficiently small nonzero real g, selected links on different plaquettes ⇒ conditional independence fails | Proved as written; no quantitative lower bound on the influence sum |
| T5 | Each fixed finite square-plaquette lattice and each perturbation order n, log-vacuum coefficient is sum over connected clusters of ≤n plaquettes | Proved as a formal coefficient/support statement; convergence radius not uniform |

Dependencies: T1 uses input vacuum.tex local bound plus Wu Theorem 2.1;
T2 uses conditional spectral calculus and a fully written mixed identity;
T3 uses the SU(2) fundamental-character Haar integral and Casimir eigenvalue;
T4 uses bounded analytic perturbation, expanded eigenfunction equation, and
a direct shared-link derivative; T5 uses the same recurrence and support
preservation of the product heat semigroup. None assumes the target gap.

## Adversarial checks

- **Normalization passed.** λ0 is a gradient gap. Multiplication by x/(2a)
  occurs once, in passing to physical quantum energy. g=2b/x² is obtained
  by division of H by x/2 and removal only of the constant magnetic term.
- **Metric passed.** Wu admits the measurable-space discrete metric;
  its Wasserstein convention equals sup_A|μ(A)−ν(A)|, without an extra 2.
  Compact Riemannian gradients enter separately through the local gap.
- **Boundary/domain passed.** Product groups are compact and boundaryless.
  Smooth positive density gives an elliptic weighted operator and compact
  resolvent in T2. Conditional projection/domain closure is inherited from
  the input proof on each finite graph; no uniform H¹ norm equivalence used.
- **Mixed identity passed.** For i≠j, differentiating L_i in j contributes
  +Hess_ji W to the positive operator convention. The cross Hessian norm of
  f is nonnegative. The ordered-pair sum gives exactly vᵀAv, with no missing 2.
- **Gauge passed.** All forms are treated before restriction. Conditional
  projection transforms each block separately; the mixture and its witness
  are Wilson-loop class functions. No quotient regularity is invoked.
- **Mixture constants passed.** ∫h²=1/4, four links give total Casimir 3,
  so mean-field witness energy is 3/(4M) and variance is at least ε²/16.
  Ratio gives 12/(ε²M). Exterior mixing weights may change but preserve
  the fixed-r block oscillation bounds.
- **Two-square coefficient passed.** First log coefficient is (Fp+Fq)/3.
  The second source contains 2Γ(Fp,Fq)/9. The shared-edge derivatives are
  −sin(t/2)/2 and +sin(s/2)/2; their product is the displayed negative quarter.
  Nonzero mixed rectangle difference proves the Haar double-centering does
  not vanish. J commutes with T; thus J ell₂ is nonzero. The analytic remainder
  then cannot cancel this leading term for all sufficiently small nonzero g.
- **Exceptional cases passed.** At b=0, the vacuum is product Haar and q=0;
  no nonindependence claim is made at g=0. A single block has no offdiagonal
  influence, and both criteria reduce to the existing local inequality.
- **Support recurrence passed.** Disjoint coordinate supports give zero Γ;
  mean-zero inverse T preserves dependence on a chosen link set. Constants
  are fixed by ∫logψ=0, and do not create mixed dependence.
- **Coarse-graining boundary passed.** Only ordinary marginal stability of
  an already proved Poincaré inequality is asserted. The metric-normalized
  quantum Schur transform is explicitly excluded from that inference.

## Remaining missing implication

No volume-uniform actual-vacuum influence sum is established in any new
interacting regime. The local ratio estimate gives only a bound growing with
the number of fast blocks. Formal perturbative locality alone provides no
summable bound on coefficients and no weak-coupling estimate.

## Proofreading self-review

Coverage: newly written PROOF.md, SOURCES.md, ROUTE.json, SELF_AUDIT.md.
Routine corrections: none after final reread. Mathematical-token corrections:
none. Validation: JSON parsed successfully; input/artifact SHA-256 recorded.
No LaTeX manuscript or publication file was edited. No numerical tests are
used as evidence for an infinite-volume assertion.
