# AS1239 — Strong-field ordinary-matter conservation cross-check

**Group:** A10 — Derived lensing, PPN, tensors and measured G  
**Priority:** P1 · **Kind:** derivation · **Execution state:** proposed; not dispatched  
**Branch:** CA5-GNC-R; filtered nu_mono target; criterion B — Derived relativistic observables and strong-field limits  
**Explicit prerequisites:** AS1213, AS1214, AS137

## Assignment and principle

Resolve the specific implication represented by strong-field ordinary-matter conservation cross-check. Preserve all action terms needed for the stated test; a favorable subblock does not certify the whole theory.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [real_research/common_action_2026_09_26/action/FINAL_ACTION.md](../../real_research/common_action_2026_09_26/action/FINAL_ACTION.md) — pinned SHA-256 `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e`.
- [real_research/breakthrough_review_2026_09_26/vacuum/ACTION.md](../../real_research/breakthrough_review_2026_09_26/vacuum/ACTION.md) — pinned SHA-256 `290e5cbe83eca682fb68888375bb60f9230f677cbb3176ae6ec27557e777211d`.
- [qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md](../../qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md) — pinned SHA-256 `98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
Evaluate nabla_mu T_b^{mu nu} on a solved compact or horizon-adjacent ordinary-fluid configuration.
```

## Inputs, domain and first bound

Use a numerical or symbolic stationary solution with nontrivial pressure. One weak-field or strong-field regime explicitly specified by the obligation; accept no empirical bound as an exact equation. The observed acceleration normalization remains independent input.

## First-principles obligation

Use one physical metric with minimally coupled ordinary probes and action-derived carrier stress. Measured G_N, Einstein G_E and any critical-density coupling stay distinct until matched.

## Contribution to common-theory closure

This establishes or blocks verify that the matter equations and the candidate metric equations imply the same force balance independently. It is one necessary link toward the same-action closure requirements.

## Execute in order

1. Read the pinned equations and import only the listed dependency results, recording their domains before choosing the test variables.
2. Verify that the matter equations and the candidate metric equations imply the same force balance independently.
3. Carry out the calculation on the stated fixture and isolate the residual, bound or rank condition that could invalidate the proposed implication.
4. Check an independently simplified limit, then apply the explicit negative control. Give the smallest hypothesis needed for extension beyond the tested domain.

## Controls that must be capable of failing

- The action-consistent simplified limit and an independent algebraic or numerical evaluation must agree within a declared error.
- Negative control: include auxiliary stress in T_b to conceal nonmetric ordinary forces.

## Completion criterion

Deliver the requested relation with its domain, or a concrete obstruction and the failed estimate. Keep finite verification separate from a general proof.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If promising: Can this residual certify compact-solution consistency?
2. If promising: Does it expose a missing surface stress at the fluid boundary?
3. If failed: Repair the metric or fluid equation rather than altering the conservation requirement.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS1239/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
