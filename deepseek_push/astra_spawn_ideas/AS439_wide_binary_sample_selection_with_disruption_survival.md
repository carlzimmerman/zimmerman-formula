# AS439 — Wide-binary sample selection with disruption survival

**Group:** A18 — Lensing, binaries and precision-gravity inference  
**Priority:** P1 · **Kind:** computation · **Execution state:** proposed; not dispatched  
**Branch:** Supplied binary dynamics and environmental survival model  
**Explicit prerequisites:** AS437

## Assignment and principle

Test whether separation-dependent catalog selection and dynamical survival reshape normalized velocities enough to affect a gravity comparison.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [deepseek_push/DE07_wide_binary_angular.py](../../deepseek_push/DE07_wide_binary_angular.py) — pinned SHA-256 `54aa0c1f18a7ea5df993253cf06a9086464293746e8f9f2bb2a24a3b7faa6ba3`.
- [deepseek_push/G100_wallaby_efe.py](../../deepseek_push/G100_wallaby_efe.py) — pinned SHA-256 `56b262ca3f97217fd6125cfb8dd0e28f6cc1b37855f612e25a7f6418b63abfaf`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
pobs(s,v)=S(s,v,sky) psurvive(age,environment|orbit) ptheory(s,v)/Z; Z integrates the same selection over latent orbits.
```

## Inputs, domain and first bound

Require pair-selection criteria, chance-alignment probabilities and a declared finite-age disruption model; use2000 synthetic systems over1e3 to5e4 AU. Freeze the supplied sample and units before estimating the target; missing covariance or calibration inputs permit only a labeled synthetic exercise, never an observed significance.

## First-principles obligation

Start from the declared Supplied binary dynamics and environmental survival model equations and inspect the source premises for Wide-binary sample selection with disruption survival. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. Test whether separation-dependent catalog selection and dynamical survival reshape normalized velocities enough to affect a gravity comparison. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Wide-binary sample selection with disruption survival to a single common-action closure witness. Deliver a selection-aware comparison or a blocked survival model; no unsupported age distribution may be tuned to secure agreement. This completes only the named implication; it does not establish full same-action gravity closure. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Construct selection from the actual proper-motion and distance-consistency cuts, keeping it distinct from physical survival probabilities.
2. Forward-select orbit libraries for each theory and normalize the likelihood after both factors are applied.
3. Compare gravity inference with and without high-contamination separation bins, reporting information loss rather than only a preferred cut.
4. Produce a table of the named estimand, numerical residuals, and uncertainty or rigorous enclosure on exactly the stated domain. Retain failed cells and distinguish a data limitation from a failure of the named implication.

## Controls that must be capable of failing

- Negative control: apply the selection to a Newtonian injection and verify that its induced velocity edge is not interpreted as a MOND transition.
- Repeat the decisive calculation with an independent implementation or analytic limiting case. State the tolerance before comparing results and retain both outputs if they disagree.

## Completion criterion

Deliver a selection-aware comparison or a blocked survival model; no unsupported age distribution may be tuned to secure agreement. This completes only the named implication; it does not establish full same-action gravity closure.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Wide-binary sample selection with disruption survival by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Wide-binary sample selection with disruption survival. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS439/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
