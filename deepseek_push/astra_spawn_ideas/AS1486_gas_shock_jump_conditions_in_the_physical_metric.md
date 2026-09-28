# AS1486 — Gas shock jump conditions in the physical metric

**Group:** A14 — Galaxy formation, relaxation and environments  
**Priority:** P1 · **Kind:** derivation · **Execution state:** proposed; not dispatched  
**Branch:** CA5-GNC-R where the supplied action reduction applies; CA4-PQ results transfer only with an explicit equation-level equality proof. Filtered nu_mono and criterion B retained.  
**Explicit prerequisites:** AS326

## Assignment and principle

Determine the following single implication: The correct baryonic shock conditions and gravity-source change at a gas compression front The output is the named mathematical object, with an explicit domain and failure condition, rather than a new interpretation of a preexisting numerical pass.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [real_research/common_action_2026_09_26/action/FINAL_ACTION.md](../../real_research/common_action_2026_09_26/action/FINAL_ACTION.md) — pinned SHA-256 `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e`.
- [real_research/acceleration_trigger_2026/README.md](../../real_research/acceleration_trigger_2026/README.md) — pinned SHA-256 `dce2d221b59ae5fc0ee48fdcefb5d231f345c7992c90177ff2dfe28321b59264`.
- [qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md](../../qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md) — pinned SHA-256 `98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
[rho u_n]=0,[rho u_n²+P]=0 with metric/body-force variation negligible across a resolved thin shock only under a scale hierarchy.
```

## Inputs, domain and first bound

Use one supplied action-specific field solver, baryonic assembly history and carrier initial state; retain the filtered nu_mono operator with S=exp(xi² Delta_h/2) and its actual source coupling. Use one smooth source geometry and three successively refined spatial grids, with a finite mass/radius interval stated before solving. A prescribed assembly history remains an external datum, not a first-principles galaxy-formation claim.

## First-principles obligation

Test or derive the correct baryonic shock conditions and gravity-source change at a gas compression front from the common gravity/carrier action, measured G_N and the imposed baryonic source history; derive every effective coefficient in the displayed object before using it. Remaining independent data include initial/boundary conditions and the stated action couplings; kappa=1/2 is adopted, a0=(c/2)sqrt(G_N rhoLambda), and G_E/Gcosm are not silently identified with G_N.

## Contribution to common-theory closure

This result supplies a formation prediction whose environmental and internal force laws come from the same equations. Its necessary bridge is concrete: the correct baryonic shock conditions and gravity-source change at a gas compression front must hold for the actual solution/parameters used by the other sectors, with no substitution of another action, source convention or carrier population.

## Execute in order

1. Derive the displayed object from the common gravity/carrier action, measured G_N and the imposed baryonic source history. Identify all background equations, constraints and boundary terms used in the reduction; isolate any extra assumption required specifically for the correct baryonic shock conditions and gravity-source change at a gas compression front
2. Derive integrated conservation equations and bound the nonlocal force variation across the shock width.
3. Construct an independent limiting case or exact small-system calculation for gas shock jump conditions in the physical metric. Compare it with the full restricted model at fixed physical normalization; refine the decisive residual rather than merely increasing the number of sampled points.
4. Return the formula, admissible set and one explicit witness or obstruction for the correct baryonic shock conditions and gravity-source change at a gas compression front Give solver-error bounds or analytic estimates and preserve any failure that changes the conclusion.

## Controls that must be capable of failing

- Negative control: Applying a discontinuous force jump by algebraic MOND rescaling must fail the action-derived field response.
- Check dimensions, action identity and normalization on the displayed equation. A converged finite-domain answer must not be promoted to all wavelengths, all initial data or an empirical fit.

## Completion criterion

Complete when the correct baryonic shock conditions and gravity-source change at a gas compression front is established on the declared domain or its exact missing implication is isolated with a counterexample or blocker. Keep the same-action cosmological/observational implications conditional on the unevaluated sectors.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If promising, derive baryonic shock-triggered carrier conversion.
2. If promising, construct consistent gas-plus-field assembly calculations.
3. If the implication fails, isolate the first term invalidating the correct baryonic shock conditions and gravity-source change at a gas compression front; construct a minimal same-field action or boundary-condition repair and recheck this object before transferring any earlier pass.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS1486/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
