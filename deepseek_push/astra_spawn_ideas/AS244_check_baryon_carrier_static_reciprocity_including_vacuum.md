# AS244 — Check baryon-carrier static reciprocity including vacuum

**Group:** A10 — Derived lensing, PPN, tensors and measured G  
**Priority:** P1 · **Kind:** audit · **Execution state:** proposed; not dispatched  
**Branch:** CA5-GNC-R physical-metric branch; Q algebraic, RAR, historical EXP and mu2 laws are never interchangeable.  
**Explicit prerequisites:** AS126, AS127, AS142, AS226

## Assignment and principle

Obtain each observable from the physical metric and measured Newton constant of one action; keep candidate predictions separate from historical model passes.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [real_research/common_action_2026_09_26/action/FINAL_ACTION.md](../../real_research/common_action_2026_09_26/action/FINAL_ACTION.md) — pinned SHA-256 `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e`.
- [real_research/breakthrough_review_2026_09_26/vacuum/ACTION.md](../../real_research/breakthrough_review_2026_09_26/vacuum/ACTION.md) — pinned SHA-256 `290e5cbe83eca682fb68888375bb60f9230f677cbb3176ae6ec27557e777211d`.
- [real_research/common_action_2026_09_26/action/PERSPECTIVE_VARIANT.md](../../real_research/common_action_2026_09_26/action/PERSPECTIVE_VARIANT.md) — pinned SHA-256 `36efa45459468d22c1f2553cbcd5d2a2349bef56c6df1e03a5b9fefb9806d78b`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
Response matrix R_ab=delta Phi_a/delta rho_b should be symmetric after consistent source normalization when derived from one quadratic action.
```

## Inputs, domain and first bound

Homogeneous reciprocal vacuum plus weak cold excitations, finite k>0; identify whether rho or sigma is the independent source. Fix all unspecified coefficients before numerical work; use symbolic positive parameters when an exact identity is the deliverable.

## First-principles obligation

Start from the declared CA5-GNC-R physical-metric branch; Q algebraic, RAR, historical EXP and mu2 laws are never interchangeable. equations and inspect the source premises for Check baryon-carrier static reciprocity including vacuum. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. Obtain each observable from the physical metric and measured Newton constant of one action; keep candidate predictions separate from historical model passes. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Check baryon-carrier static reciprocity including vacuum to a single common-action closure witness. A finite-mode reciprocity check for the current candidate's source dictionary. Classify this target as derived, failed by an explicit residual/witness, or blocked by a named missing equation or hypothesis; do not promote it to complete gravity closure. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Pin the cited action and conventions, then write the one displayed mathematical target with independent fields and boundary or mode conditions. Retain the current candidate status.
2. Derive the two source couplings and eliminate the same auxiliary block with no one-sided force substitutions.
3. Compare the off-diagonal Green-function coefficients and state the source variables in which symmetry holds.
4. Run the stated falsifiable negative control and record its residual alongside the main result. For numerical work, refine once and specify the finite domain; for algebra, substitute back into the original equation.

## Controls that must be capable of failing

- Check dimensions, signs, averaging measure and the declared limiting case directly against the original action or operator; a successful solver exit is insufficient.
- Negative control: Use rho_R in one equation and sigma_R in the reciprocal equation and require a nonzero antisymmetric response.

## Completion criterion

A finite-mode reciprocity check for the current candidate's source dictionary. Classify this target as derived, failed by an explicit residual/witness, or blocked by a named missing equation or hypothesis; do not promote it to complete gravity closure.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Check baryon-carrier static reciprocity including vacuum by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Check baryon-carrier static reciprocity including vacuum. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS244/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
