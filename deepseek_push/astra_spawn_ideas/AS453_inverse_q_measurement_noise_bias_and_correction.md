# AS453 — Inverse-Q measurement-noise bias and correction

**Group:** A19 — Mathematical and statistical evidence certificates  
**Priority:** P1 · **Kind:** derivation · **Execution state:** proposed; not dispatched  
**Branch:** Q scalar force inversion  
**Explicit prerequisites:** AS026

## Assignment and principle

Quantify the nonlinear inversion bias induced by noisy force measurements; this differs from the algebraic inverse and its conditioning.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [campaign_fresh_gravity_astra/DERIVATIONS.md](../../campaign_fresh_gravity_astra/DERIVATIONS.md) — pinned SHA-256 `8da8176e3daeaeeaf9e42edb1585f271c92a50c0d9fdd842aa10caee462fb889`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
B(g)=(sqrt(a^2+4g^2)-a)/2; B''(g)=2*a^2/(a^2+4*g^2)^(3/2). For centered bounded noise epsilon, E[B(g+epsilon)]-B(g)=B''(g)*Var(epsilon)/2 plus a controlled Taylor remainder.
```

## Inputs, domain and first bound

Positive fixed a and g with bounded symmetric force noise |epsilon|<g; begin with a two-point noise law, then a finite bounded distribution. Scale both framework footings separately. Unknown measured noise permits synthetic evidence only.

## First-principles obligation

Start from the declared Q scalar force inversion equations and inspect the source premises for Inverse-Q measurement-noise bias and correction. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. Quantify the nonlinear inversion bias induced by noisy force measurements; this differs from the algebraic inverse and its conditioning. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Inverse-Q measurement-noise bias and correction to a single common-action closure witness. Deliver a scoped noise-bias certificate and correction with assumptions and remainder, distinct from stable evaluation of the noiseless inverse. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Use the AS026 physical inverse and derive its second through fourth derivatives; do not repeat its algebraic construction as the claimed new result.
2. Prove the sign of Jensen bias and bound the remainder on the entire noise-support interval.
3. Construct a leading bias correction and test its residual across noise amplitudes; then retain correlation if a itself is measured with uncertainty.
4. Return exact bounded-noise inequalities and a reproducible synthetic expectation comparison; identify the calibration information needed for a real measurement.

## Controls that must be capable of failing

- A linearized inverse must miss the positive second-order bias on the same symmetric-noise fixture.
- Compare exact two-point expectations with the analytic Taylor enclosure and require contraction as noise amplitude decreases.

## Completion criterion

Deliver a scoped noise-bias certificate and correction with assumptions and remainder, distinct from stable evaluation of the noiseless inverse.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Inverse-Q measurement-noise bias and correction by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Inverse-Q measurement-noise bias and correction. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS453/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
