# AS397 — Low-acceleration completeness and nondetections

**Group:** A16 — Galaxy data, BTFR and dwarf inference  
**Priority:** P1 · **Kind:** computation · **Execution state:** proposed; not dispatched  
**Branch:** Deep-limit observational selection  
**Explicit prerequisites:** No catalog result required to start the bounded task; inspect the stated sources and record any newly discovered dependencies.

## Assignment and principle

Test whether excluding galaxies without an outer velocity detection biases the apparent low-acceleration response toward stronger gravity.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [deepseek_push/G230_dmdg_measure.py](../../deepseek_push/G230_dmdg_measure.py) — pinned SHA-256 `a80516a57ee0dcd0e0ecbcb09d4a3d2238d10e0f9ec430b08c00374e037460bc`.
- [deepseek_push/G100_wallaby_efe.py](../../deepseek_push/G100_wallaby_efe.py) — pinned SHA-256 `56b262ca3f97217fd6125cfb8dd0e28f6cc1b37855f612e25a7f6418b63abfaf`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
L_nondet=integral_{Vlim}^infinity p(V|M,a)dV or its appropriate detection complement; selection direction must follow the actual instrument threshold.
```

## Inputs, domain and first bound

Require parent HI detections, velocity upper/lower limits and line-width selection for a fixed dwarf sample; synthetic sample size500 and detection fractions0.3,0.6,0.9. Freeze the supplied sample and units before estimating the target; missing covariance or calibration inputs permit only a labeled synthetic exercise, never an observed significance.

## First-principles obligation

Start from the declared Deep-limit observational selection equations and inspect the source premises for Low-acceleration completeness and nondetections. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. Test whether excluding galaxies without an outer velocity detection biases the apparent low-acceleration response toward stronger gravity. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Low-acceleration completeness and nondetections to a single common-action closure witness. Deliver a completeness-calibrated acceleration result or a parent-sample blocker; missing galaxies cannot be assigned velocities to improve the law. This completes only the named implication; it does not establish full same-action gravity closure. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Derive the line-width detection probability from channel noise and flux rather than assuming every missing curve has low velocity.
2. Fit detected and censored sources jointly while keeping flux selection and velocity selection distinct.
3. Compare recovered a and intrinsic scatter across the three completeness levels and a complete-data control.
4. Produce a table of the named estimand, numerical residuals, and uncertainty or rigorous enclosure on exactly the stated domain. Retain failed cells and distinguish a data limitation from a failure of the named implication.

## Controls that must be capable of failing

- Negative control: randomly censor galaxies independent of mass and velocity; the joint inference must recover the complete-data result.
- Repeat the decisive calculation with an independent implementation or analytic limiting case. State the tolerance before comparing results and retain both outputs if they disagree.

## Completion criterion

Deliver a completeness-calibrated acceleration result or a parent-sample blocker; missing galaxies cannot be assigned velocities to improve the law. This completes only the named implication; it does not establish full same-action gravity closure.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Low-acceleration completeness and nondetections by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Low-acceleration completeness and nondetections. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS397/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
