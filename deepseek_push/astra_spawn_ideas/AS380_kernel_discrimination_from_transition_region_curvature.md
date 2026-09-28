# AS380 — Kernel discrimination from transition-region curvature

**Group:** A16 — Galaxy data, BTFR and dwarf inference  
**Priority:** P1 · **Kind:** computation · **Execution state:** proposed; not dispatched  
**Branch:** Q versus RAR, never identified with mu2 or filtered nu_mono  
**Explicit prerequisites:** No catalog result required to start the bounded task; inspect the stated sources and record any newly discovered dependencies.

## Assignment and principle

Ask whether a rotation-curve shape statistic distinguishes Q from RAR after nuisance normalization directions are removed. This avoids mistaking equal deep limits for equal full laws.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [deepseek_push/G071_sparc_fullcurve.py](../../deepseek_push/G071_sparc_fullcurve.py) — pinned SHA-256 `7ee75c8bc4bff2a9b501f575815a0888e357cb5fbc180c73d00b71bea442c89a`.
- [campaign_fresh_gravity_astra/DERIVATIONS.md](../../campaign_fresh_gravity_astra/DERIVATIONS.md) — pinned SHA-256 `8da8176e3daeaeeaf9e42edb1585f271c92a50c0d9fdd842aa10caee462fb889`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
F_Q=sqrt(B^2+aB); F_R=B/(1-exp(-sqrt(B/a))); t=P_perp[log F_Q-log F_R], P_perp=I-J(J^T C^-1 J)^-1 J^T C^-1.
```

## Inputs, domain and first bound

Use rings with0.1<B/a<30, measured geometry covariance and at least ten rings per retained galaxy; maximum100 galaxies. Freeze the supplied sample and units before estimating the target; missing covariance or calibration inputs permit only a labeled synthetic exercise, never an observed significance.

## First-principles obligation

Start from the declared Q versus RAR, never identified with mu2 or filtered nu_mono equations and inspect the source premises for Kernel discrimination from transition-region curvature. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. Ask whether a rotation-curve shape statistic distinguishes Q from RAR after nuisance normalization directions are removed. This avoids mistaking equal deep limits for equal full laws. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Kernel discrimination from transition-region curvature to a single common-action closure witness. Report an identified transition statistic and its calibration dependence, not a universal preference inferred from noiseless curves alone. This completes only the named implication; it does not establish full same-action gravity closure. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Form the nuisance tangent J for distance, inclination and two stellar mass-to-light components under each forward observation map.
2. Compute the projected contrast and t^T C^-1 t with stable QR solves, then inject each kernel into50 simulated galaxies before fitting its competitor.
3. Evaluate nonlinear nuisance refits at selected high-contrast galaxies to test whether tangent projection exaggerates distinguishability.
4. Produce a table of the named estimand, numerical residuals, and uncertainty or rigorous enclosure on exactly the stated domain. Retain failed cells and distinguish a data limitation from a failure of the named implication.

## Controls that must be capable of failing

- Negative control: restrict all radii to B/a<1e-4; the discriminator must lose information as both branches approach sqrt(aB).
- Repeat the decisive calculation with an independent implementation or analytic limiting case. State the tolerance before comparing results and retain both outputs if they disagree.

## Completion criterion

Report an identified transition statistic and its calibration dependence, not a universal preference inferred from noiseless curves alone. This completes only the named implication; it does not establish full same-action gravity closure.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Kernel discrimination from transition-region curvature by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Kernel discrimination from transition-region curvature. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS380/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
