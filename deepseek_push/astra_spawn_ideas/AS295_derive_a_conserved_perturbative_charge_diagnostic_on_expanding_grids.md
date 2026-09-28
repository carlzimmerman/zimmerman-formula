# AS295 — Derive a conserved perturbative charge diagnostic on expanding grids

**Group:** A12 — Cosmological perturbations and early-universe predictions  
**Priority:** P0 · **Kind:** derivation · **Execution state:** proposed; not dispatched  
**Branch:** CA5-GNC-R cosmological perturbation candidate  
**Explicit prerequisites:** No catalog result required to start the bounded task; inspect the stated sources and record any newly discovered dependencies.

## Assignment and principle

Cosmological mode solvers should detect conversion bookkeeping errors independently of their field integrator.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [real_research/common_action_2026_09_26/transport/CONVERSION.md](../../real_research/common_action_2026_09_26/transport/CONVERSION.md) — pinned SHA-256 `f72f861c486a44fec17d82175c9b5dc439f474d288ee79dbc9f0977286f972f2`.
- [real_research/breakthrough_review_2026_09_26/transport/RESULT.md](../../real_research/breakthrough_review_2026_09_26/transport/RESULT.md) — pinned SHA-256 `3977dd5018bc06870059a1bb6fb336b52f4073cc2a7b9f44a9ad5bcbb59941ed`.
- [real_research/breakthrough_review_2026_09_26/occupied/RESULT.md](../../real_research/breakthrough_review_2026_09_26/occupied/RESULT.md) — pinned SHA-256 `6091291f05fca5f1f4fdcc216f305bd31a476a7ea3d16c09131faca1158975d5`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
Expand partial_tau(a³ j^0)+a² partial_i jhat^i=0 through first order, and through second order for a transverse seed with zero linear charge.
```

## Inputs, domain and first bound

One periodic Fourier pair on the homogeneous pump; diagonal U(1) current of the existing fields; prescribed background. Use the actual evolving background and its constraint reduction. Positive kinetic energy and a finite numerical trajectory alone do not establish cosmological viability; retain the physical perturbation norm and identify any approximation needed to connect the calculation to an observable.

## First-principles obligation

Start from the declared CA5-GNC-R cosmological perturbation candidate equations and inspect the source premises for Derive a conserved perturbative charge diagnostic on expanding grids. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. Cosmological mode solvers should detect conversion bookkeeping errors independently of their field integrator. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Derive a conserved perturbative charge diagnostic on expanding grids to a single common-action closure witness. A perturbative charge ledger prevents interpreting linear gain as new conserved matter. Report scoped success, a concrete failed condition, or the exact missing input; none of these outcomes alone closes the thirteen requirements. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Derive the linear mode identity including metric-volume perturbations.
2. For the transverse subsystem derive the quadratic light-field charge and the required pump depletion contribution.
3. Specify an independent residual monitor usable by a later perturbation solver.
4. Write the requested relation or counterexample with every assumption used, then identify the single downstream calculation that it enables or blocks. Keep numerical evidence bounded by the stated domain.

## Controls that must be capable of failing

- Zero mixing must not generate light-field charge from a neutral seed.
- Negative control: omit second-order pump depletion while reporting net charge creation and expose the conservation mismatch.

## Completion criterion

A perturbative charge ledger prevents interpreting linear gain as new conserved matter. Report scoped success, a concrete failed condition, or the exact missing input; none of these outcomes alone closes the thirteen requirements.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Derive a conserved perturbative charge diagnostic on expanding grids by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Derive a conserved perturbative charge diagnostic on expanding grids. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS295/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
