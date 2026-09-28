# AS482 — Outskirts evacuation versus core retention constructive window

**Group:** A20 — Same-theory compatibility and closure synthesis  
**Priority:** P0 · **Kind:** construction · **Execution state:** proposed; not dispatched  
**Branch:** One supplied carrier transport action, current halo-model gates  
**Explicit prerequisites:** AS354, AS355

## Assignment and principle

Search for a radial carrier-retention profile that satisfies group-scale shear suppression and core-lensing retention under a single conservative transport mechanism.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [real_research/acceleration_trigger_2026/README.md](../../real_research/acceleration_trigger_2026/README.md) — pinned SHA-256 `dce2d221b59ae5fc0ee48fdcefb5d231f345c7992c90177ff2dfe28321b59264`.
- [real_research/breakthrough_review_2026_09_26/README.md](../../real_research/breakthrough_review_2026_09_26/README.md) — pinned SHA-256 `22cacef2b949f88c5539a81291f14232d01e8b1bbad266956018bcde6c6e32ab`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
f_ret(r,M) in[0,1]; constraints include integral Wshear rho f_ret<=Pmax, Mcore[f_ret]>=Mcore,min, and continuity dM/dt=-4pi r^2 J_r with one supplied J_r law.
```

## Inputs, domain and first bound

Use AT4's resolution-free halo-model response, core-retention bounds and an action-derived transport law if available; finite masses1e13 to1e14.5 Msun and20 radial shells. Freeze the supplied sample and units before estimating the target; missing covariance or calibration inputs permit only a labeled synthetic exercise, never an observed significance.

## First-principles obligation

Start from the declared One supplied carrier transport action, current halo-model gates equations and inspect the source premises for Outskirts evacuation versus core retention constructive window. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. Search for a radial carrier-retention profile that satisfies group-scale shear suppression and core-lensing retention under a single conservative transport mechanism. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Outskirts evacuation versus core retention constructive window to a single common-action closure witness. Deliver a realizable outskirts-clearing witness or a scoped unattainability result; an arbitrary retention curve is only a target, not a derived mechanism. This completes only the named implication; it does not establish full same-action gravity closure. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Form a constrained profile search first to determine whether any monotone or nonmonotone retention function satisfies the observational inequalities.
2. For a feasible profile, solve the transport inverse problem for admissible carrier fields and fluxes, enforcing charge and energy conservation.
3. Compare attainable transport profiles with unconstrained optimal profiles, recording the minimum extra physical mechanism needed if they differ.
4. Produce a table of the named estimand, numerical residuals, and uncertainty or rigorous enclosure on exactly the stated domain. Retain failed cells and distinguish a data limitation from a failure of the named implication.

## Controls that must be capable of failing

- Negative control: use a uniform high kick that hollows cores; the core-retention inequality must fail even if the shear integral improves.
- Repeat the decisive calculation with an independent implementation or analytic limiting case. State the tolerance before comparing results and retain both outputs if they disagree.

## Completion criterion

Deliver a realizable outskirts-clearing witness or a scoped unattainability result; an arbitrary retention curve is only a target, not a derived mechanism. This completes only the named implication; it does not establish full same-action gravity closure.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Outskirts evacuation versus core retention constructive window by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Outskirts evacuation versus core retention constructive window. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS482/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
