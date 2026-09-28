# AS398 — Tidal-dwarf equilibrium applicability window

**Group:** A16 — Galaxy data, BTFR and dwarf inference  
**Priority:** P1 · **Kind:** computation · **Execution state:** proposed; not dispatched  
**Branch:** Q/RAR tracer assumptions, time-dependent control  
**Explicit prerequisites:** No catalog result required to start the bounded task; inspect the stated sources and record any newly discovered dependencies.

## Assignment and principle

Determine whether a young tidal dwarf supplies an equilibrium test of the acceleration law or only a time-dependent kinematic constraint.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [deepseek_push/G230_dmdg_measure.py](../../deepseek_push/G230_dmdg_measure.py) — pinned SHA-256 `a80516a57ee0dcd0e0ecbcb09d4a3d2238d10e0f9ec430b08c00374e037460bc`.
- [campaign_fresh_gravity_astra/stage_03/cluster_precision/DERIVATION.md](../../campaign_fresh_gravity_astra/stage_03/cluster_precision/DERIVATION.md) — pinned SHA-256 `4fcd05ab4781e790e51bd883e6fc67edcc9c339a359a85b9bebb6e921481f325`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
t_dyn=R/Vc; epsilon_adv=|partial_t u+u partial_r u|/F(B;a); circular inference requires epsilon_adv below a declared tolerance, not merely a smooth velocity gradient.
```

## Inputs, domain and first bound

Require resolved gas morphology, velocity and dispersion maps plus an independent age or interaction model for one tidal dwarf; synthetic snapshots span0.2 to5 dynamical times. Freeze the supplied sample and units before estimating the target; missing covariance or calibration inputs permit only a labeled synthetic exercise, never an observed significance.

## First-principles obligation

Start from the declared Q/RAR tracer assumptions, time-dependent control equations and inspect the source premises for Tidal-dwarf equilibrium applicability window. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. Determine whether a young tidal dwarf supplies an equilibrium test of the acceleration law or only a time-dependent kinematic constraint. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Tidal-dwarf equilibrium applicability window to a single common-action closure witness. Deliver a bounded equilibrium subdomain or a time-dependence blocker; selecting a visually regular gradient cannot establish stationarity. This completes only the named implication; it does not establish full same-action gravity closure. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Construct a time-dependent gas forward model constrained by the observed geometry and boundary flow, retaining the same baryonic mass map used for gravity.
2. Estimate or bound the advective and temporal acceleration terms on resolved scales, and compare their sum with the kernel separation in the accessible B range.
3. Fit a fixed equilibrium model only on regions where the dynamical remainder is independently bounded below ten percent, reporting excluded area and information loss.
4. Produce a table of the named estimand, numerical residuals, and uncertainty or rigorous enclosure on exactly the stated domain. Retain failed cells and distinguish a data limitation from a failure of the named implication.

## Controls that must be capable of failing

- Negative control: inject an expanding gas cloud with an ordered velocity gradient but no circular equilibrium; the applicability criterion must reject it as an equilibrium BTFR datum.
- Repeat the decisive calculation with an independent implementation or analytic limiting case. State the tolerance before comparing results and retain both outputs if they disagree.

## Completion criterion

Deliver a bounded equilibrium subdomain or a time-dependence blocker; selecting a visually regular gradient cannot establish stationarity. This completes only the named implication; it does not establish full same-action gravity closure.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Tidal-dwarf equilibrium applicability window by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Tidal-dwarf equilibrium applicability window. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS398/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
