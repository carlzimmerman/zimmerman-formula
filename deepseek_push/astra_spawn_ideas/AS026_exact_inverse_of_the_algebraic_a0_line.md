# AS026 — Exact inverse of the algebraic a0 line

**Group:** A02 — Constitutive kernels and branch fidelity  
**Priority:** P0 · **Kind:** audit · **Execution state:** proposed; not dispatched  
**Branch:** Separate Q, RAR, MU2, historical EXP and operative MONO  
**Explicit prerequisites:** No catalog result required to start the bounded task; inspect the stated sources and record any newly discovered dependencies.

## Assignment and principle

A constitutive response, its inverse, and its filtered field equation must agree on their declared branch; matching one asymptote does not make two kernels equivalent.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [README.md](../../README.md) — pinned SHA-256 `91a5fac44ffe30db5f8e95247e5f04e913eccd149f2ff8b683c1f05510a6b6ed`.
- [qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md](../../qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md) — pinned SHA-256 `98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f`.
- [real_research/peer_review_2026_09_26/README.md](../../real_research/peer_review_2026_09_26/README.md) — pinned SHA-256 `521d9ac36a93a27dcd6c995f78743ae9b1de4304095911871d81e6a70f9ecaac`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
Q: g^2=B^2+a0*B; B=2*g^2/(sqrt(a0^2+4*g^2)+a0).
```

## Inputs, domain and first bound

Work primarily in y=B/a0>0 and x=g/a0. Use symbolic limits and a diagnostic grid y=10^k for k from -10 to 8 in steps of 0.1; explicitly bracket any roots instead of treating the grid as a proof.

## First-principles obligation

Start from the declared Separate Q, RAR, MU2, historical EXP and operative MONO equations and inspect the source premises for Exact inverse of the algebraic a0 line. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. A constitutive response, its inverse, and its filtered field equation must agree on their declared branch; matching one asymptote does not make two kernels equivalent. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Exact inverse of the algebraic a0 line to a single common-action closure witness. Deliver a self-contained derivation or explicit counterexample to the named claim, with reproducible checks. A conditional theorem must list every condition; missing dynamics or data is an explicit open dependency, never a pass. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Read the cited equations and write the precise claim, symbol dictionary, boundary conditions and assumptions needed for this task. Distinguish framework inputs from conclusions to be established.
2. Derive the stable inverse by rationalization and prove its monotonicity for positive g. Compare with the subtractive quadratic root near g=0.
3. Show the intermediate algebra or integration, including all scale factors, signs and units. If the calculation uses a limiting regime, derive the leading neglected term and state its domain.
4. Perform an independent check using a different representation: substitution into the original equation, direct differentiation, or a bounded high-precision calculation. Save the actual residual, not only a Boolean.
5. Apply the specified negative control, then write the strongest surviving statement and the first additional implication needed to transfer it to the full theory. Do not import a different branch to repair a failed result.

## Controls that must be capable of failing

- Perturb the inverse sign and require the forward law to reject it.
- Check the deep and Newtonian limiting regimes wherever they exist; otherwise check normalization and a boundary case. Distinguish an exact identity from a finite numerical consistency check.

## Completion criterion

Deliver a self-contained derivation or explicit counterexample to the named claim, with reproducible checks. A conditional theorem must list every condition; missing dynamics or data is an explicit open dependency, never a pass.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Exact inverse of the algebraic a0 line by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Exact inverse of the algebraic a0 line. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS026/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
