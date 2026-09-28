# AS270 — Audit double counting of vacuum energy in the background action

**Group:** A11 — Homogeneous cosmology and global modes  
**Priority:** P0 · **Kind:** audit · **Execution state:** proposed; not dispatched  
**Branch:** CA5-GNC-R homogeneous candidate  
**Explicit prerequisites:** AS253

## Assignment and principle

The same dark-energy density must not enter both a bare cosmological constant and the carrier vacuum floor unnoticed.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [real_research/breakthrough_review_2026_09_26/vacuum/ACTION.md](../../real_research/breakthrough_review_2026_09_26/vacuum/ACTION.md) — pinned SHA-256 `290e5cbe83eca682fb68888375bb60f9230f677cbb3176ae6ec27557e777211d`.
- [real_research/common_action_2026_09_26/transport/HOMOGENEOUS_FRW.md](../../real_research/common_action_2026_09_26/transport/HOMOGENEOUS_FRW.md) — pinned SHA-256 `ecc93b07a62d7ea531abcf4ca8ed8cbe7b9f73c8cb60f931dc8fcb6e9e685c1d`.
- [qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md](../../qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md) — pinned SHA-256 `98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
At t_c=1 use rho_v=V0 F(1)=V0 and p_v=-V0; with bare Lambda the Einstein vacuum contribution is M_P² Lambda.
```

## Inputs, domain and first bound

Compare the documented bare-Lambda-zero CA5 branch to an explicitly labeled nonzero-Lambda extension; no parameter fitting. Keep the exactly homogeneous sector separate from every nonzero Fourier constraint. Carrier masses, initial charge, V0 and host coefficients remain inputs; this task must not promote an allowed cosmological branch into a prediction of abundance.

## First-principles obligation

Start from the declared CA5-GNC-R homogeneous candidate equations and inspect the source premises for Audit double counting of vacuum energy in the background action. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. The same dark-energy density must not enter both a bare cosmological constant and the carrier vacuum floor unnoticed. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Audit double counting of vacuum energy in the background action to a single common-action closure witness. A vacuum accounting identity prevents a false derivation of the observed floor. Report scoped success, a concrete failed condition, or the exact missing input; none of these outcomes alone closes the thirteen requirements. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Trace every constant term through lapse and spatial-metric variation.
2. Express the total homogeneous vacuum density and the scale-relation density in one unit system.
3. Determine which combination is observable in H_vac and which separate parameter remains unidentifiable at background order.
4. Write the requested relation or counterexample with every assumption used, then identify the single downstream calculation that it enables or blocks. Keep numerical evidence bounded by the stated domain.

## Controls that must be capable of failing

- Set bare Lambda=0 and recover the recorded candidate.
- Negative control: apply the Zimmerman relation independently to both constants and expose duplicated vacuum density.

## Completion criterion

A vacuum accounting identity prevents a false derivation of the observed floor. Report scoped success, a concrete failed condition, or the exact missing input; none of these outcomes alone closes the thirteen requirements.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Audit double counting of vacuum energy in the background action by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Audit double counting of vacuum energy in the background action. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS270/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
