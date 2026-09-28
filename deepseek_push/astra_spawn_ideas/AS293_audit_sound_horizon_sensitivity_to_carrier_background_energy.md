# AS293 — Audit sound-horizon sensitivity to carrier background energy

**Group:** A12 — Cosmological perturbations and early-universe predictions  
**Priority:** P1 · **Kind:** computation · **Execution state:** proposed; not dispatched  
**Branch:** CA5-GNC-R cosmological perturbation candidate  
**Explicit prerequisites:** AS251, AS272, AS275

## Assignment and principle

Early-universe distance effects can be estimated cheaply before a full anisotropy calculation.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [real_research/common_action_2026_09_26/transport/HOMOGENEOUS_FRW.md](../../real_research/common_action_2026_09_26/transport/HOMOGENEOUS_FRW.md) — pinned SHA-256 `ecc93b07a62d7ea531abcf4ca8ed8cbe7b9f73c8cb60f931dc8fcb6e9e685c1d`.
- [qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md](../../qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md) — pinned SHA-256 `98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
Linearize r_s=integral c_s(a) da/[a²H(a)] to obtain delta r_s=-integral c_s delta H da/[a²H²], holding the ordinary-fluid c_s prescription fixed.
```

## Inputs, domain and first bound

A supplied reference background and one small carrier-energy perturbation with |delta H/H|<=0.05; finite integration limits with explicit tail bound. Use the actual evolving background and its constraint reduction. Positive kinetic energy and a finite numerical trajectory alone do not establish cosmological viability; retain the physical perturbation norm and identify any approximation needed to connect the calculation to an observable.

## First-principles obligation

Start from the declared CA5-GNC-R cosmological perturbation candidate equations and inspect the source premises for Audit sound-horizon sensitivity to carrier background energy. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. Early-universe distance effects can be estimated cheaply before a full anisotropy calculation. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Audit sound-horizon sensitivity to carrier background energy to a single common-action closure witness. A bounded background response identifies whether a later full CMB calculation is warranted. Report scoped success, a concrete failed condition, or the exact missing input; none of these outcomes alone closes the thirteen requirements. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Derive the first-order response from the integral, distinguishing a changed expansion history from a changed sound speed.
2. Use the carrier dilution result to bound the weighted integral on the chosen epoch.
3. Compare the linear estimate to one direct quadrature using the perturbed H.
4. Write the requested relation or counterexample with every assumption used, then identify the single downstream calculation that it enables or blocks. Keep numerical evidence bounded by the stated domain.

## Controls that must be capable of failing

- Zero added carrier energy must give zero sound-horizon shift.
- Negative control: replace the weighted shift by its endpoint delta H/H and demonstrate the missed time weighting.

## Completion criterion

A bounded background response identifies whether a later full CMB calculation is warranted. Report scoped success, a concrete failed condition, or the exact missing input; none of these outcomes alone closes the thirteen requirements.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Audit sound-horizon sensitivity to carrier background energy by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Audit sound-horizon sensitivity to carrier background energy. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS293/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
