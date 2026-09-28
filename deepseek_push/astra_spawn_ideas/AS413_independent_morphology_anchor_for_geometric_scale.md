# AS413 — Independent morphology anchor for geometric scale

**Group:** A17 — High-redshift spectra, evolution and identifiability  
**Priority:** P1 · **Kind:** computation · **Execution state:** proposed; not dispatched  
**Branch:** Q/RAR calibration orbit with external geometry  
**Explicit prerequisites:** AS410

## Assignment and principle

Test whether a separately measured inclination and distance can break the spectral calibration orbit to a useful precision.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [campaign_fresh_gravity_astra/stage_03/joint_identifiability/RESULT.md](../../campaign_fresh_gravity_astra/stage_03/joint_identifiability/RESULT.md) — pinned SHA-256 `a39952326ffe8793f0f2479c1c40e2af2ab21b2227a996d78f3c2b018680f335`.
- [deepseek_push/G071_sparc_fullcurve.py](../../deepseek_push/G071_sparc_fullcurve.py) — pinned SHA-256 `7ee75c8bc4bff2a9b501f575815a0888e357cb5fbc180c73d00b71bea442c89a`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
gamma proportional to D sin^2 i in the chosen angular map; dlog gamma=dlog D+2cot(i) di; a=AC/gamma.
```

## Inputs, domain and first bound

Require axis ratio, disk thickness prior, distance measurement and their covariance for one source; synthetic inclination20 to80 degrees and fractional distance error1 to20 percent. Freeze the supplied sample and units before estimating the target; missing covariance or calibration inputs permit only a labeled synthetic exercise, never an observed significance.

## First-principles obligation

Start from the declared Q/RAR calibration orbit with external geometry equations and inspect the source premises for Independent morphology anchor for geometric scale. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. Test whether a separately measured inclination and distance can break the spectral calibration orbit to a useful precision. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Independent morphology anchor for geometric scale to a single common-action closure witness. Produce a calibrated geometric-anchor posterior or show that morphology alone leaves an uncontrolled thickness degeneracy. This completes only the named implication; it does not establish full same-action gravity closure. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Derive the inclination likelihood from projected thickness rather than setting cos i equal to axis ratio for every disk.
2. Combine that likelihood with a frozen(A,C) spectral likelihood, propagating nonlinear low-inclination tails exactly.
3. Compare inferred a using numerical quadrature and Monte Carlo, checking sensitivity to physically supported thickness priors.
4. Produce a table of the named estimand, numerical residuals, and uncertainty or rigorous enclosure on exactly the stated domain. Retain failed cells and distinguish a data limitation from a failure of the named implication.

## Controls that must be capable of failing

- Negative control: remove the independent morphology/distance terms and require the absolute a posterior to regain its prior-dominated orbit direction.
- Repeat the decisive calculation with an independent implementation or analytic limiting case. State the tolerance before comparing results and retain both outputs if they disagree.

## Completion criterion

Produce a calibrated geometric-anchor posterior or show that morphology alone leaves an uncontrolled thickness degeneracy. This completes only the named implication; it does not establish full same-action gravity closure.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Independent morphology anchor for geometric scale by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Independent morphology anchor for geometric scale. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS413/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
