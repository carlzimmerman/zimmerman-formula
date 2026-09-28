# AS427 — ESD-to-acceleration conversion under non-power-law profiles

**Group:** A18 — Lensing, binaries and precision-gravity inference  
**Priority:** P1 · **Kind:** computation · **Execution state:** proposed; not dispatched  
**Branch:** Projection geometry, independent of action derivation  
**Explicit prerequisites:** No catalog result required to start the bounded task; inspect the stated sources and record any newly discovered dependencies.

## Assignment and principle

Quantify the error in a constant conversion from projected ESD to three-dimensional acceleration when the underlying profile bends across the measured window.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [deepseek_push/G073_lensing_completion.py](../../deepseek_push/G073_lensing_completion.py) — pinned SHA-256 `25ca8e0a4fc052ce032288f5f5e9bba6fe334c17c188710e9a44233cc7fd79bf`.
- [deepseek_push/G136_lensing_core_registry.py](../../deepseek_push/G136_lensing_core_registry.py) — pinned SHA-256 `5ffacef4bd29c3cafa226e71627bf54bb4438287495848cb7880b06f0e32dce8`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
Sigma(R)=2 integral_R^infinity rho(r)r/sqrt(r^2-R^2)dr; DeltaSigma=2R^-2 integral_0^R Sigma(s)s ds-Sigma(R); g=GM(<r)/r^2.
```

## Inputs, domain and first bound

Use finite Plummer, Hernquist and broken-power-law profiles with outer truncation declared; radial grid spans0.01 to100 scale radii. Freeze the supplied sample and units before estimating the target; missing covariance or calibration inputs permit only a labeled synthetic exercise, never an observed significance.

## First-principles obligation

Start from the declared Projection geometry, independent of action derivation equations and inspect the source premises for ESD-to-acceleration conversion under non-power-law profiles. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. Quantify the error in a constant conversion from projected ESD to three-dimensional acceleration when the underlying profile bends across the measured window. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by ESD-to-acceleration conversion under non-power-law profiles to a single common-action closure witness. Return a profile-dependent conversion envelope or identify the missing large-radius information; a universal constant factor is not presumed. This completes only the named implication; it does not establish full same-action gravity closure. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Derive projected ESD and true g from the same density and compute C(R)=g/(G DeltaSigma) instead of assuming2pi or4.
2. Evaluate how C varies with slope and radial boundaries, doubling quadrature resolution and truncation radius independently.
3. Apply the conversion uncertainty to the historical claimed lensing normalization offset without treating it as free adjustable mass.
4. Produce a table of the named estimand, numerical residuals, and uncertainty or rigorous enclosure on exactly the stated domain. Retain failed cells and distinguish a data limitation from a failure of the named implication.

## Controls that must be capable of failing

- Negative control: recover the analytic singular-isothermal conversion on an explicitly finite interior window where edge errors are controlled.
- Repeat the decisive calculation with an independent implementation or analytic limiting case. State the tolerance before comparing results and retain both outputs if they disagree.

## Completion criterion

Return a profile-dependent conversion envelope or identify the missing large-radius information; a universal constant factor is not presumed. This completes only the named implication; it does not establish full same-action gravity closure.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen ESD-to-acceleration conversion under non-power-law profiles by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in ESD-to-acceleration conversion under non-power-law profiles. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS427/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
