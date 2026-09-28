# AS363 — Compute tidal stripping of a carrier packet during one encounter

**Group:** A15 — Clusters, mergers and the common source gate  
**Priority:** P1 · **Kind:** construction · **Execution state:** proposed; not dispatched  
**Branch:** filtered nu_mono common-observable bridge  
**Explicit prerequisites:** AS313, AS348, AS351

## Assignment and principle

Group outskirts may be depleted through gravitational tides instead of an arbitrary high-speed kick.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [real_research/acceleration_trigger_2026/AT4_halo_model_cosmic_shear.py](../../real_research/acceleration_trigger_2026/AT4_halo_model_cosmic_shear.py) — pinned SHA-256 `ba3b722826309e0f3cd05909752a8b31998dbf237f0088443efafaaba28cb503`.
- [real_research/common_action_2026_09_26/transport/CONVERSION.md](../../real_research/common_action_2026_09_26/transport/CONVERSION.md) — pinned SHA-256 `f72f861c486a44fec17d82175c9b5dc439f474d288ee79dbc9f0977286f972f2`.
- [real_research/common_action_2026_09_26/action/FINAL_ACTION.md](../../real_research/common_action_2026_09_26/action/FINAL_ACTION.md) — pinned SHA-256 `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
For a small packet in an encounter use delta a_i=-T_ij(tau)x_j with T_ij=partial_i partial_j Phi_ext; derive the energy increment from the action-consistent packet motion.
```

## Inputs, domain and first bound

One weak, finite-duration external tide and one bound narrow packet; impulse approximation only if encounter duration is short relative to internal time. Use one declared action or explicitly conditional operator throughout. Preserve the canonical and alternative acceleration footings as separate records, and do not transfer a historical gate pass across a changed force operator, kernel, carrier profile or retention epoch.

## First-principles obligation

Start from the declared filtered nu_mono common-observable bridge equations and inspect the source premises for Compute tidal stripping of a carrier packet during one encounter. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. Group outskirts may be depleted through gravitational tides instead of an arbitrary high-speed kick. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Compute tidal stripping of a carrier packet during one encounter to a single common-action closure witness. A conditional selective-stripping mechanism offers a concrete alternative to the failed uniform kick. Report scoped success, a concrete failed condition, or the exact missing input; none of these outcomes alone closes the thirteen requirements. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Derive the packet centroid and width response to the tidal tensor.
2. Compare the transferred energy with the escape condition while preserving the total encounter energy interpretation.
3. Determine whether an outskirts packet can escape while a core packet remains bound under the same encounter.
4. Write the requested relation or counterexample with every assumption used, then identify the single downstream calculation that it enables or blocks. Keep numerical evidence bounded by the stated domain.

## Controls that must be capable of failing

- A spatially uniform external acceleration must not create internal tidal heating.
- Negative control: use the impulse approximation for an adiabatically slow encounter and expose the neglected cancellation.

## Completion criterion

A conditional selective-stripping mechanism offers a concrete alternative to the failed uniform kick. Report scoped success, a concrete failed condition, or the exact missing input; none of these outcomes alone closes the thirteen requirements.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Compute tidal stripping of a carrier packet during one encounter by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Compute tidal stripping of a carrier packet during one encounter. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS363/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
