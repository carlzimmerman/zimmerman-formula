# AS709 — Sum rule for a positive response spectral measure

**Group:** A03 — Coefficient mechanisms and their missing premises  
**Priority:** P1 · **Kind:** derivation · **Execution state:** proposed; not dispatched  
**Branch:** Explicit coefficient-mechanism diagnostic. Historical saturated kernels in k01/k02/k04 and probabilistic MU2 constructions remain distinct from filtered MONO and CA5-GNC-R.  
**Explicit prerequisites:** AS053

## Assignment and principle

A coefficient mechanism must remove an independent coupling or datum through a derived equation. Symmetry, dimensional analysis, normalization and an adopted boundary ensemble do not by themselves choose one half.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [deepseek_push/PD08_particle_free_derivation.py](../../deepseek_push/PD08_particle_free_derivation.py) — pinned SHA-256 `83f6054cdfb1b45834af1ce702b1a040f00ad1625ffc34799ae367bd367f0cfb`.
- [deepseek_push/G228_lomax_maxent.py](../../deepseek_push/G228_lomax_maxent.py) — pinned SHA-256 `cb82a65c2825e1633941ad286053876f2315ed60c16cdf3f6a24d9377265551d`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
p(Y)=int Y/(lambda+Y)dmu(lambda), int dmu=1.
```

## Inputs, domain and first bound

Positive measure supported on a finite positive lambda interval. Keep unspecified positive coefficients symbolic. Numerical witnesses require one declared finite fixture and one refinement; do not fit missing physical inputs.

## First-principles obligation

Vary the proposed action or derive the stated symmetry/response condition before fixing any normalization. The observed vacuum magnitude and kappa=1/2 remain inputs unless this particular obligation supplies an independent selecting equation. No new particle species is assumed.

## Contribution to common-theory closure

Needed implication: an explicit necessary condition for a scale-selection mechanism compatible with measured G_N and the current gravity action. Transfer requires the same action, source convention and healthy counted degrees of freedom.

## Execute in order

1. Fix the source equation, independent variables, boundary conditions and measure from the cited branch. State any additional assumption needed for the displayed target.
2. Derive p'(0) as an inverse moment and identify why saturation does not fix that moment.
3. Keep every integration constant, multiplier, dimensionless coupling and boundary datum independent until its equation fixes it. Separate a constructed candidate from a result inherited by the present common action.
4. Test the altered premise: Replace the inverse moment by one from normalization. Exhibit the residual, violated inequality or lost hypothesis using the original equation.
5. Verify the resulting equation by substitution or an independent representation. Report its exact scope and the first missing implication for the stated closure bridge.

## Controls that must be capable of failing

- Check units, signs, normalization and one admissible boundary or limiting case in the same measure.
- Negative control: Replace the inverse moment by one from normalization.

## Completion criterion

Return one derived equation or bound, admissible construction, falsifying witness, or precisely named missing input for this target. State the domain; no single result certifies gravity closure.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. Promising result: Test moment bounds from support. Keep the same source and action conventions.
2. Promising extension: seek a vacuum principle fixing the measure.. State the new required hypothesis.
3. Failure repair: Add an independently derived moment constraint. Name the changed equation or new datum; label a changed model separately.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS709/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
