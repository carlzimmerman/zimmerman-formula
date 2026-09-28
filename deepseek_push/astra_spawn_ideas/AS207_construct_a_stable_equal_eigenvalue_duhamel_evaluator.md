# AS207 — Construct a stable equal-eigenvalue Duhamel evaluator

**Group:** A09 — Filters, zero-field limits and well-posedness  
**Priority:** P0 · **Kind:** computation · **Execution state:** proposed; not dispatched  
**Branch:** Filtered nu_mono and criterion B; reciprocal fixed-data estimates are not assumed to prove coupled evolution.  
**Explicit prerequisites:** No catalog result required to start the bounded task; inspect the stated sources and record any newly discovered dependencies.

## Assignment and principle

Use the actual filtered nu_mono operator and preferred-time criterion B; distinguish spatial smoothing, source dependence and coupled evolution well-posedness.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [real_research/peer_review_2026_09_26/xc1/REVIEW.md](../../real_research/peer_review_2026_09_26/xc1/REVIEW.md) — pinned SHA-256 `26693935fcaf2870119a6f630b819b40ec33d94d0bdcf967beb51750e326f770`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
d_b(lambda,mu)=(exp(-bmu)-exp(-blambda))/(lambda-mu), d_b(lambda,lambda)=b exp(-blambda).
```

## Inputs, domain and first bound

Nonnegative Laplacian eigenvalues in [0,1e4], b=1/2, near-equal separations from 1e-2 to 1e-12. Fix all unspecified coefficients before numerical work; use symbolic positive parameters when an exact identity is the deliverable.

## First-principles obligation

Start from the declared Filtered nu_mono and criterion B; reciprocal fixed-data estimates are not assumed to prove coupled evolution. equations and inspect the source premises for Construct a stable equal-eigenvalue Duhamel evaluator. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. Use the actual filtered nu_mono operator and preferred-time criterion B; distinguish spatial smoothing, source dependence and coupled evolution well-posedness. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Construct a stable equal-eigenvalue Duhamel evaluator to a single common-action closure witness. A numerical operator building block with error bounds, not a physical stability result. Classify this target as derived, failed by an explicit residual/witness, or blocked by a named missing equation or hypothesis; do not promote it to complete gravity closure. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Pin the cited action and conventions, then write the one displayed mathematical target with independent fields and boundary or mode conditions. Retain the current candidate status.
2. Derive a cancellation-safe expm1 or series representation and a switching criterion based on dimensionless separation.
3. Compare the implementation against high-precision values on a deterministic finite grid.
4. Run the stated falsifiable negative control and record its residual alongside the main result. For numerical work, refine once and specify the finite domain; for algebra, substitute back into the original equation.

## Controls that must be capable of failing

- Check dimensions, signs, averaging measure and the declared limiting case directly against the original action or operator; a successful solver exit is insufficient.
- Negative control: Use direct subtraction near equality and require the loss of significant digits to be measured.

## Completion criterion

A numerical operator building block with error bounds, not a physical stability result. Classify this target as derived, failed by an explicit residual/witness, or blocked by a named missing equation or hypothesis; do not promote it to complete gravity closure.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Construct a stable equal-eigenvalue Duhamel evaluator by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Construct a stable equal-eigenvalue Duhamel evaluator. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS207/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
