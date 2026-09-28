# AS950 — Differential energy relation for horizon-free carrier equilibria

**Group:** A06 — Common-action construction and full variation  
**Priority:** P1 · **Kind:** derivation · **Execution state:** proposed; not dispatched  
**Branch:** CA5-GNC-R; filtered nu_mono target; criterion B — Same-action higher variations and boundary identities  
**Explicit prerequisites:** AS887, AS910, AS938, AS949

## Assignment and principle

Derive the constrained first variation for stationary charged carrier equilibria without a horizon or inner surface-charge term.

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
For a horizon-free stationary family with fixed outer data, test delta E=Omega delta J+omega delta Q plus explicitly derived ordinary-matter work; E,J,Q are the action boundary energy, angular momentum and diagonal carrier charge.
```

## Inputs, domain and first bound

A smooth rotating or stationary carrier equilibrium family on a compact leaf or a fixed outer-boundary ensemble; no inner boundary and no black-hole entropy interpretation. Smooth compact leaf unless the task explicitly introduces a boundary; keep t_c=1+P_h Z positive and retain the actual lapse and intrinsic volume measure.

## First-principles obligation

Vary the CA5 reciprocal action, its intrinsic means and localized heat constraint before reduction. All couplings and prescribed boundary data remain inputs; no observational normalization is inferred.

## Contribution to common-theory closure

A horizon-free constrained energy variation supplies the premise for carrier or stellar equilibrium stability tests, independently of any horizon charge integrability problem.

## Execute in order

1. Import the covariant symplectic current and the exact global phase and rotational generators.
2. Vary between neighboring on-shell equilibria while keeping topology and outer ensemble fixed.
3. Identify which global charges are constrained and derive every remaining boundary or material work term.
4. Check the relation against an independent constrained-energy variation and state which equilibrium families it can support.

## Controls that must be capable of failing

- The nonrotating fixed-charge limit must remove both Omega delta J and omega delta Q variations as appropriate.
- Negative control: change unrecorded outer data between equilibria and incorrectly attribute its boundary work to a failed energy relation.

## Completion criterion

Deliver the requested relation with its domain, or a concrete obstruction and the failed estimate. Keep finite verification separate from a general proof.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If promising: Can fixed-charge turning points be related to a neutral equilibrium mode?
2. If promising: Does the identity characterize which carrier boundary data remain free in a stationary family?
3. If failed: Identify the nonintegrable outer or material work term before claiming a variational stability principle.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS950/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
