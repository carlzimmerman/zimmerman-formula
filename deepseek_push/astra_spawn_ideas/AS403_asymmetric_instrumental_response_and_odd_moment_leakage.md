# AS403 — Asymmetric instrumental response and odd-moment leakage

**Group:** A17 — High-redshift spectra, evolution and identifiability  
**Priority:** P1 · **Kind:** computation · **Execution state:** proposed; not dispatched  
**Branch:** Q observational moment map  
**Explicit prerequisites:** No catalog result required to start the bounded task; inspect the stated sources and record any newly discovered dependencies.

## Assignment and principle

Establish which odd response moments must be calibrated before even spectral moments can be interpreted as gravitational invariants.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [campaign_fresh_gravity_astra/stage_02/DERIVATIONS.md](../../campaign_fresh_gravity_astra/stage_02/DERIVATIONS.md) — pinned SHA-256 `4d806bc45c1cbc31d8203fcd7b477e220e954560601ddae20538f72935957967`.
- [campaign_fresh_gravity_astra/stage_03/SUPPORT_CORRECTION.md](../../campaign_fresh_gravity_astra/stage_03/SUPPORT_CORRECTION.md) — pinned SHA-256 `e98353c122e382bca53646ef933778fbe6cb7eef781ffafadc7e695fc2c4e6ea`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
m4=U4+4 e1 U3+6 e2 U2+4 e3 U1+e4; m2=U2+2 e1 U1+e2, where ej=E[epsilon^j].
```

## Inputs, domain and first bound

Use asymmetric response mixtures with e1=0 but e3 nonzero, source mean velocities spanning positive and negative signs, and a401-channel synthetic cube. Freeze the supplied sample and units before estimating the target; missing covariance or calibration inputs permit only a labeled synthetic exercise, never an observed significance.

## First-principles obligation

Start from the declared Q observational moment map equations and inspect the source premises for Asymmetric instrumental response and odd-moment leakage. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. Establish which odd response moments must be calibrated before even spectral moments can be interpreted as gravitational invariants. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Asymmetric instrumental response and odd-moment leakage to a single common-action closure witness. Return a response-calibration sufficiency condition and a bounded recovery demonstration; asymmetry correction is conditional on independent convolution. This completes only the named implication; it does not establish full same-action gravity closure. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Derive the full triangular moment inversion through order4, preserving odd source moments instead of symmetrizing them away by assumption.
2. Fit or calibrate response moments from reference lines, then recover intrinsic moments under three deliberately asymmetric LSFs.
3. Compare a parity-averaged approaching/receding estimator with explicit odd-moment correction when brightness on the two sides differs.
4. Produce a table of the named estimand, numerical residuals, and uncertainty or rigorous enclosure on exactly the stated domain. Retain failed cells and distinguish a data limitation from a failure of the named implication.

## Controls that must be capable of failing

- Negative control: use unequal side brightness and omit the e3 U1 term; the recovered fourth moment must fail the injected truth check.
- Repeat the decisive calculation with an independent implementation or analytic limiting case. State the tolerance before comparing results and retain both outputs if they disagree.

## Completion criterion

Return a response-calibration sufficiency condition and a bounded recovery demonstration; asymmetry correction is conditional on independent convolution. This completes only the named implication; it does not establish full same-action gravity closure.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Asymmetric instrumental response and odd-moment leakage by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Asymmetric instrumental response and odd-moment leakage. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS403/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
