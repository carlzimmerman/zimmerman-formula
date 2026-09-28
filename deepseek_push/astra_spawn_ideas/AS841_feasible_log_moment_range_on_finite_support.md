# AS841 — Feasible log-moment range on finite support

**Group:** A05 — Statistical mechanics and the gravity-response bridge  
**Priority:** P1 · **Kind:** derivation · **Execution state:** proposed; not dispatched  
**Branch:** Lomax/MU2 statistical-response diagnostics; no identification with MONO or metric gravity without an action-derived bridge. New stochastic dynamics are explicitly proposed models.  
**Explicit prerequisites:** AS840

## Assignment and principle

A stationary measure does not determine its generator, response, absolute energy or gravitational coupling. Derive one identifiable statistical or dynamical obligation with the sampling and reference measures explicit.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [deepseek_push/G228_lomax_maxent.py](../../deepseek_push/G228_lomax_maxent.py) — pinned SHA-256 `cb82a65c2825e1633941ad286053876f2315ed60c16cdf3f6a24d9377265551d`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
0<=c_log<=ln(1+U).
```

## Inputs, domain and first bound

Probability densities on [0,U]. Keep unspecified positive coefficients symbolic. Numerical witnesses require one declared finite fixture and one refinement; do not fit missing physical inputs.

## First-principles obligation

Derive the selected invariant-measure, response or information identity from a specified probability law or generator. The physical drive coupling, clock-time rate and vacuum normalization remain independent data unless separately derived from the existing fields.

## Contribution to common-theory closure

Needed implication: a statistically and dynamically defined response that could be coupled variationally to the physical metric and baryonic source. Transfer requires the same action, source convention and healthy counted degrees of freedom.

## Execute in order

1. Fix the source equation, independent variables, boundary conditions and measure from the cited branch. State any additional assumption needed for the displayed target.
2. Derive interior versus boundary feasibility and identify when no finite smooth entropy maximizer exists.
3. Specify the forward/backward generator or probability measure, normalization, support and boundary current. Distinguish distributional identities from dynamical assumptions and preserve the source coupling when translating to gravitational variables.
4. Test the altered premise: Request a mean outside the support range. Exhibit the residual, violated inequality or lost hypothesis using the original equation.
5. Verify the resulting equation by substitution or an independent representation. Report its exact scope and the first missing implication for the stated closure bridge.

## Controls that must be capable of failing

- Check units, signs, normalization and one admissible boundary or limiting case in the same measure.
- Negative control: Request a mean outside the support range.

## Completion criterion

Return one derived equation or bound, admissible construction, falsifying witness, or precisely named missing input for this target. State the domain; no single result certifies gravity closure.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. Promising result: Analyze boundary-concentrating sequences. Keep the same source and action conventions.
2. Promising extension: design consistent finite-grid constraints.. State the new required hypothesis.
3. Failure repair: Check feasibility before optimization. Name the changed equation or new datum; label a changed model separately.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS841/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
