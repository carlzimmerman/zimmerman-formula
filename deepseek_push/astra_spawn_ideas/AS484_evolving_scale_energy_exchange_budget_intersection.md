# AS484 — Evolving scale energy-exchange budget intersection

**Group:** A20 — Same-theory compatibility and closure synthesis  
**Priority:** P0 · **Kind:** construction · **Execution state:** proposed; not dispatched  
**Branch:** DP1 preferred-frame reservoir, covariant completion separately required; constant a is separate  
**Explicit prerequisites:** AS414

## Assignment and principle

Determine whether a proposed redshift evolution of a can be supplied by the same scale sector without violating its background energy budget.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [campaign_fresh_gravity_astra/stage_03/dynamics_precision/DERIVATION.md](../../campaign_fresh_gravity_astra/stage_03/dynamics_precision/DERIVATION.md) — pinned SHA-256 `41ad39d1521e7d5b5d974e320478faecd944df8d4608b4869a566624244af3ae`.
- [real_research/breakthrough_review_2026_09_26/README.md](../../real_research/breakthrough_review_2026_09_26/README.md) — pinned SHA-256 `22cacef2b949f88c5539a81291f14232d01e8b1bbad266956018bcde6c6e32ab`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
For the DP1 preferred-frame toy action using the declared normalization G=G_N, W=integral_0^g F^-1(s;a)ds and partial_t e_total+div S_total=Q_a=W_a adot/(4piG_N), with e in J/m^3, S in W/m^2 and Q_a in W/m^3. A reservoir balance must supply -Q_a; an FLRW equation dot epsilon_scale+3H(epsilon_scale+p_scale)=Q_scale requires a separately derived stress tensor and exchange Q_scale, not automatic identification with the toy average.
```

## Inputs, domain and first bound

Require the explicit DP1 normalization and boundary fluxes, or an action-derived covariant replacement with energy density epsilon_scale and pressure p_scale in common SI units; finite z interval0 to3 and supplied a(z). Freeze the supplied sample and units before estimating the target; missing covariance or calibration inputs permit only a labeled synthetic exercise, never an observed significance.

## First-principles obligation

Start from the declared DP1 preferred-frame reservoir, covariant completion separately required; constant a is separate equations and inspect the source premises for Evolving scale energy-exchange budget intersection. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. Determine whether a proposed redshift evolution of a can be supplied by the same scale sector without violating its background energy budget. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Evolving scale energy-exchange budget intersection to a single common-action closure witness. Deliver a consistent exchange-history witness or a missing-sector blocker; static fits cannot select an unprovided kinetic or energy-transfer law. This completes only the named implication; it does not establish full same-action gravity closure. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Re-derive the sign and coefficient Q_a from the chosen action at fixed g and compare with DP1 Eq.(10); only after a covariant extension is supplied derive its separate scale-sector exchange and averaging law.
2. For a supplied covariant extension, solve its actual scale-sector background equations and compare H(z), positivity and a(z); otherwise finish with the bounded preferred-frame reservoir requirement and mark cosmological closure blocked.
3. Test the deep-limit W=g^3/(3a) against the full primitive to bound errors from applying the asymptotic formula to transition fields.
4. Produce a table of the named estimand, numerical residuals, and uncertainty or rigorous enclosure on exactly the stated domain. Retain failed cells and distinguish a data limitation from a failure of the named implication.

## Controls that must be capable of failing

- Negative control: prescribe evolving a in the DP1 toy action with g nonzero and omit its reservoir; the local energy-balance residual must detect Q_a. Do not interpret that test alone as an FLRW Ward identity.
- Repeat the decisive calculation with an independent implementation or analytic limiting case. State the tolerance before comparing results and retain both outputs if they disagree.

## Completion criterion

Deliver a consistent exchange-history witness or a missing-sector blocker; static fits cannot select an unprovided kinetic or energy-transfer law. This completes only the named implication; it does not establish full same-action gravity closure.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Evolving scale energy-exchange budget intersection by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Evolving scale energy-exchange budget intersection. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS484/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
