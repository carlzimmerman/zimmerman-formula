# AS259 — Classify the massless neutral homogeneous endpoint

**Group:** A11 — Homogeneous cosmology and global modes  
**Priority:** P1 · **Kind:** derivation · **Execution state:** proposed; not dispatched  
**Branch:** CA5-GNC-R homogeneous candidate  
**Explicit prerequisites:** No catalog result required to start the bounded task; inspect the stated sources and record any newly discovered dependencies.

## Assignment and principle

The massless slow-transport witness must not inherit the positive-mass attraction theorem.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [real_research/common_action_2026_09_26/transport/HOMOGENEOUS_FRW.md](../../real_research/common_action_2026_09_26/transport/HOMOGENEOUS_FRW.md) — pinned SHA-256 `ecc93b07a62d7ea531abcf4ca8ed8cbe7b9f73c8cb60f931dc8fcb6e9e685c1d`.
- [real_research/common_action_2026_09_26/transport/CONVERSION.md](../../real_research/common_action_2026_09_26/transport/CONVERSION.md) — pinned SHA-256 `f72f861c486a44fec17d82175c9b5dc439f474d288ee79dbc9f0977286f972f2`.
- [real_research/breakthrough_review_2026_09_26/transport/RESULT.md](../../real_research/breakthrough_review_2026_09_26/transport/RESULT.md) — pinned SHA-256 `3977dd5018bc06870059a1bb6fb336b52f4073cc2a7b9f44a9ad5bcbb59941ed`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
Set mu=0 in Vmix=M²|phi|²/2+m²|chi+gamma s phi|²/2; stationary points satisfy grad Vmix=0.
```

## Inputs, domain and first bound

Finite homogeneous energy and V0>0; expanding branch; no spatial modes. Keep the exactly homogeneous sector separate from every nonzero Fourier constraint. Carrier masses, initial charge, V0 and host coefficients remain inputs; this task must not promote an allowed cosmological branch into a prediction of abundance.

## First-principles obligation

Start from the declared CA5-GNC-R homogeneous candidate equations and inspect the source premises for Classify the massless neutral homogeneous endpoint. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. The massless slow-transport witness must not inherit the positive-mass attraction theorem. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Classify the massless neutral homogeneous endpoint to a single common-action closure witness. A correct massless scope statement decides whether the slow-wave branch has a usable homogeneous endpoint. Report scoped success, a concrete failed condition, or the exact missing input; none of these outcomes alone closes the thirteen requirements. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Find the entire equilibrium set using the exact field equations.
2. Linearize transverse to that set and identify which estimates remain uniform as the limiting value of s varies.
3. Formulate the strongest possible convergence statement supported by the energy identity, or isolate an unresolved drift along the flat direction.
4. Write the requested relation or counterexample with every assumption used, then identify the single downstream calculation that it enables or blocks. Keep numerical evidence bounded by the stated domain.

## Controls that must be capable of failing

- Positive mu must collapse the equilibrium set to the known unique origin.
- Negative control: initialize arbitrary constant s with all charged fields zero and reject a theorem claiming all fields approach zero.

## Completion criterion

A correct massless scope statement decides whether the slow-wave branch has a usable homogeneous endpoint. Report scoped success, a concrete failed condition, or the exact missing input; none of these outcomes alone closes the thirteen requirements.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Classify the massless neutral homogeneous endpoint by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Classify the massless neutral homogeneous endpoint. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS259/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
