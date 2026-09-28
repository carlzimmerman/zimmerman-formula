# AS1383 — Observer terms in large-scale lensing response

**Group:** A12 — Cosmological perturbations and early-universe predictions  
**Priority:** P1 · **Kind:** derivation · **Execution state:** proposed; not dispatched  
**Branch:** CA5-GNC-R where the supplied action reduction applies; CA4-PQ results transfer only with an explicit equation-level equality proof. Filtered nu_mono and criterion B retained.  
**Explicit prerequisites:** AS294

## Assignment and principle

Determine the following single implication: A complete large-scale scalar lensing observable with gauge artifacts canceled The output is the named mathematical object, with an explicit domain and failure condition, rather than a new interpretation of a preexisting numerical pass.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [real_research/breakthrough_review_2026_09_26/occupied/RESULT.md](../../real_research/breakthrough_review_2026_09_26/occupied/RESULT.md) — pinned SHA-256 `6091291f05fca5f1f4fdcc216f305bd31a476a7ea3d16c09131faca1158975d5`.
- [real_research/breakthrough_review_2026_09_26/transport/RESULT.md](../../real_research/breakthrough_review_2026_09_26/transport/RESULT.md) — pinned SHA-256 `3977dd5018bc06870059a1bb6fb336b52f4073cc2a7b9f44a9ad5bcbb59941ed`.
- [qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md](../../qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md) — pinned SHA-256 `98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
observable deflection includes source/observer frame terms; a uniform potential gradient cannot create local shear.
```

## Inputs, domain and first bound

Use constraint-reduced perturbations about one actual occupied expanding solution; q=k/A is physical wave number, the lapse denominator and time-dependent canonical mixing are retained. Begin with eight physical Fourier modes and a finite background interval, then16 modes or twice the temporal resolution. Require the missing action coefficients before running a prediction; no supplied coefficient may be replaced by its GR value.

## First-principles obligation

Test or derive a complete large-scale scalar lensing observable with gauge artifacts canceled from the complete occupied quadratic action, its constraints and background Ward identities; derive every effective coefficient in the displayed object before using it. Remaining independent data include initial/boundary conditions and the stated action couplings; kappa=1/2 is adopted, a0=(c/2)sqrt(G_N rhoLambda), and G_E/Gcosm are not silently identified with G_N.

## Contribution to common-theory closure

This result supplies a controlled transfer map that can feed observations without replacing the action by an assumed fluid. Its necessary bridge is concrete: a complete large-scale scalar lensing observable with gauge artifacts canceled must hold for the actual solution/parameters used by the other sectors, with no substitution of another action, source convention or carrier population.

## Execute in order

1. Derive the displayed object from the complete occupied quadratic action, its constraints and background Ward identities. Identify all background equations, constraints and boundary terms used in the reduction; isolate any extra assumption required specifically for a complete large-scale scalar lensing observable with gauge artifacts canceled
2. Derive line-of-sight and endpoint contributions for the supplied metric potentials and test uniform-gradient and constant-potential limits.
3. Construct an independent limiting case or exact small-system calculation for observer terms in large-scale lensing response. Compare it with the full restricted model at fixed physical normalization; refine the decisive residual rather than merely increasing the number of sampled points.
4. Return the formula, admissible set and one explicit witness or obstruction for a complete large-scale scalar lensing observable with gauge artifacts canceled Give solver-error bounds or analytic estimates and preserve any failure that changes the conclusion.

## Controls that must be capable of failing

- Negative control: Omitting observer terms must expose a spurious response to a pure gauge mode.
- Check dimensions, action identity and normalization on the displayed equation. A converged finite-domain answer must not be promoted to all wavelengths, all initial data or an empirical fit.

## Completion criterion

Complete when a complete large-scale scalar lensing observable with gauge artifacts canceled is established on the declared domain or its exact missing implication is isolated with a counterexample or blocker. Keep the same-action cosmological/observational implications conditional on the unevaluated sectors.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If promising, derive infrared-safe lensing transfer functions.
2. If promising, construct consistency with the action's equivalence principle.
3. If the implication fails, isolate the first term invalidating a complete large-scale scalar lensing observable with gauge artifacts canceled; construct a minimal same-field action or boundary-condition repair and recheck this object before transferring any earlier pass.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS1383/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
