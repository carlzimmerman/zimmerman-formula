# AS177 — Compute occupied adiabatic/entropy mixing

**Group:** A08 — Linear health and interaction control  
**Priority:** P0 · **Kind:** derivation · **Execution state:** proposed; not dispatched  
**Branch:** Filtered nu_mono CA5-GNC-R; frozen, fixed-filter and separate diagnostic scopes are explicitly restricted.  
**Explicit prerequisites:** AS176

## Assignment and principle

Positive kinetic energy, finite-wavelength restoring signs and interaction control are separate obligations; isolate one missing physical coefficient of the same action.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [real_research/breakthrough_review_2026_09_26/occupied/RESULT.md](../../real_research/breakthrough_review_2026_09_26/occupied/RESULT.md) — pinned SHA-256 `6091291f05fca5f1f4fdcc216f305bd31a476a7ea3d16c09131faca1158975d5`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
e_parallel=v/norm(v), chi=e_parallel chi_parallel+sum e_I chi_I; v nonzero.
```

## Inputs, domain and first bound

A smooth occupied homogeneous trajectory on a finite interval where norm(v)>=v_min>0. Fix all unspecified coefficients before numerical work; use symbolic positive parameters when an exact identity is the deliverable.

## First-principles obligation

Start from the declared Filtered nu_mono CA5-GNC-R; frozen, fixed-filter and separate diagnostic scopes are explicitly restricted. equations and inspect the source premises for Compute occupied adiabatic/entropy mixing. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. Positive kinetic energy, finite-wavelength restoring signs and interaction control are separate obligations; isolate one missing physical coefficient of the same action. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Compute occupied adiabatic/entropy mixing to a single common-action closure witness. An explicit rotated perturbation action with its nonzero-velocity limitation stated. Classify this target as derived, failed by an explicit residual/witness, or blocked by a named missing equation or hypothesis; do not promote it to complete gravity closure. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Pin the cited action and conventions, then write the one displayed mathematical target with independent fields and boundary or mode conditions. Retain the current candidate status.
2. Rotate the reduced six-variable action into the instantaneous adiabatic and four entropy directions.
3. Retain dot e_parallel and dot e_I and derive the off-diagonal kinetic and restoring couplings caused by basis rotation.
4. Run the stated falsifiable negative control and record its residual alongside the main result. For numerical work, refine once and specify the finite domain; for algebra, substitute back into the original equation.

## Controls that must be capable of failing

- Check dimensions, signs, averaging measure and the declared limiting case directly against the original action or operator; a successful solver exit is insufficient.
- Negative control: Treat a turning velocity direction as constant and require a nonzero omitted mixing term.

## Completion criterion

An explicit rotated perturbation action with its nonzero-velocity limitation stated. Classify this target as derived, failed by an explicit residual/witness, or blocked by a named missing equation or hypothesis; do not promote it to complete gravity closure.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Compute occupied adiabatic/entropy mixing by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Compute occupied adiabatic/entropy mixing. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS177/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
