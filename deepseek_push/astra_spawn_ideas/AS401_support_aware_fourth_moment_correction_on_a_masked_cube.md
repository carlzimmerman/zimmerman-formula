# AS401 — Support-aware fourth-moment correction on a masked cube

**Group:** A17 — High-redshift spectra, evolution and identifiability  
**Priority:** P0 · **Kind:** computation · **Execution state:** proposed; not dispatched  
**Branch:** Q moment estimator with support-qualified nuisance space  
**Explicit prerequisites:** No catalog result required to start the bounded task; inspect the stated sources and record any newly discovered dependencies.

## Assignment and principle

Construct a broadening correction that is exact on emitting cells without imposing fictitious constraints on zero-flux or zero-projection cells.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [campaign_fresh_gravity_astra/stage_03/SUPPORT_CORRECTION.md](../../campaign_fresh_gravity_astra/stage_03/SUPPORT_CORRECTION.md) — pinned SHA-256 `e98353c122e382bca53646ef933778fbe6cb7eef781ffafadc7e695fc2c4e6ea`.
- [campaign_fresh_gravity_astra/stage_02/DERIVATIONS.md](../../campaign_fresh_gravity_astra/stage_02/DERIVATIONS.md) — pinned SHA-256 `4d806bc45c1cbc31d8203fcd7b477e220e954560601ddae20538f72935957967`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
alpha=P^T l4; beta=P^T l2; error=6 sum I_i(s_i^2 alpha_i-beta_i)u_i^2; admissible condition is diag(I)(s^2 alpha-beta)=0 on the actual velocity support.
```

## Inputs, domain and first bound

Use rational PSF matrices with8 source cells and4 pixels, including two I=0 cells and one q=0 cell; real use requires masks and calibrated widths. Freeze the supplied sample and units before estimating the target; missing covariance or calibration inputs permit only a labeled synthetic exercise, never an observed significance.

## First-principles obligation

Start from the declared Q moment estimator with support-qualified nuisance space equations and inspect the source premises for Support-aware fourth-moment correction on a masked cube. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. Construct a broadening correction that is exact on emitting cells without imposing fictitious constraints on zero-flux or zero-projection cells. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Support-aware fourth-moment correction on a masked cube to a single common-action closure witness. Deliver the exact support-qualified estimator and its numerical conditioning; correctness on a mask does not imply immunity to mask uncertainty. This completes only the named implication; it does not establish full same-action gravity closure. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Derive the allowed latent subspace from the emission and projection masks, then solve the correction equations on its basis.
2. Compare active-support and full-column feasibility, constructing one example where the former succeeds and the latter incorrectly rejects an estimator.
3. Test exact correction for100 nonnegative velocity-square vectors on the admitted subspace and verify the denominator sum alpha I q^2 B is positive.
4. Produce a table of the named estimand, numerical residuals, and uncertainty or rigorous enclosure on exactly the stated domain. Retain failed cells and distinguish a data limitation from a failure of the named implication.

## Controls that must be capable of failing

- Negative control: add one positive-flux unconstrained velocity to a deleted cell and require the previously valid correction to fail unless recomputed.
- Repeat the decisive calculation with an independent implementation or analytic limiting case. State the tolerance before comparing results and retain both outputs if they disagree.

## Completion criterion

Deliver the exact support-qualified estimator and its numerical conditioning; correctness on a mask does not imply immunity to mask uncertainty. This completes only the named implication; it does not establish full same-action gravity closure.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Support-aware fourth-moment correction on a masked cube by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Support-aware fourth-moment correction on a masked cube. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS401/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
