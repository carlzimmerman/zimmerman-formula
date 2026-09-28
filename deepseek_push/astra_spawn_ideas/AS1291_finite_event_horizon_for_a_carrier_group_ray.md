# AS1291 — Finite event horizon for a carrier group ray

**Group:** A11 — Homogeneous cosmology and global modes  
**Priority:** P1 · **Kind:** derivation · **Execution state:** proposed; not dispatched  
**Branch:** CA5-GNC-R where the supplied action reduction applies; CA4-PQ results transfer only with an explicit equation-level equality proof. Filtered nu_mono and criterion B retained.  
**Explicit prerequisites:** No catalog result required to start the bounded task; inspect the stated sources and record any newly discovered dependencies.

## Assignment and principle

Determine the following single implication: A sharp source-time-dependent upper bound on the distance reached by a late massive carrier packet The output is the named mathematical object, with an explicit domain and failure condition, rather than a new interpretation of a preexisting numerical pass.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [real_research/common_action_2026_09_26/transport/HOMOGENEOUS_FRW.md](../../real_research/common_action_2026_09_26/transport/HOMOGENEOUS_FRW.md) — pinned SHA-256 `ecc93b07a62d7ea531abcf4ca8ed8cbe7b9f73c8cb60f931dc8fcb6e9e685c1d`.
- [real_research/breakthrough_review_2026_09_26/transport/RESULT.md](../../real_research/breakthrough_review_2026_09_26/transport/RESULT.md) — pinned SHA-256 `3977dd5018bc06870059a1bb6fb336b52f4073cc2a7b9f44a9ad5bcbb59941ed`.
- [real_research/breakthrough_review_2026_09_26/README.md](../../real_research/breakthrough_review_2026_09_26/README.md) — pinned SHA-256 `22cacef2b949f88c5539a81291f14232d01e8b1bbad266956018bcde6c6e32ab`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
Delta x=integral vgroup(t)dt/A(t); vgroup=p/sqrt(m²+p²), p=k/A only in the free adiabatic regime.
```

## Inputs, domain and first bound

Use the five canonical real fields u, velocities v, scale factor A>0 and expanding H, with Vmix=M²|phi|²/2+m²|chi+gamma s phi|²/2+mu²s²/2; begin with M,m,mu,V0>0 and distinguish any explicitly changed limit. Start with dimensionless M=1 and a finite declared initial-energy sublevel; use at most100 initial states and at most four dynamical timescales. Analytic conclusions must specify their full hypotheses, and numerical conclusions retain this finite range.

## First-principles obligation

Test or derive a sharp source-time-dependent upper bound on the distance reached by a late massive carrier packet from the varied homogeneous Friedmann constraint and polynomial carrier potential; derive every effective coefficient in the displayed object before using it. Remaining independent data include initial/boundary conditions and the stated action couplings; kappa=1/2 is adopted, a0=(c/2)sqrt(G_N rhoLambda), and G_E/Gcosm are not silently identified with G_N.

## Contribution to common-theory closure

This result supplies a cosmological branch with controlled initial and asymptotic data from the same carrier action. Its necessary bridge is concrete: a sharp source-time-dependent upper bound on the distance reached by a late massive carrier packet must hold for the actual solution/parameters used by the other sectors, with no substitution of another action, source convention or carrier population.

## Execute in order

1. Derive the displayed object from the varied homogeneous Friedmann constraint and polynomial carrier potential. Identify all background equations, constraints and boundary terms used in the reduction; isolate any extra assumption required specifically for a sharp source-time-dependent upper bound on the distance reached by a late massive carrier packet
2. Optimize the ray integral using the actual H(t) envelope and compare it with the metric event horizon, retaining the no-later-interaction premise.
3. Construct an independent limiting case or exact small-system calculation for finite event horizon for a carrier group ray. Compare it with the full restricted model at fixed physical normalization; refine the decisive residual rather than merely increasing the number of sampled points.
4. Return the formula, admissible set and one explicit witness or obstruction for a sharp source-time-dependent upper bound on the distance reached by a late massive carrier packet Give solver-error bounds or analytic estimates and preserve any failure that changes the conclusion.

## Controls that must be capable of failing

- Negative control: A later momentum-changing interaction must invalidate the fixed-k bound rather than be silently included.
- Check dimensions, action identity and normalization on the displayed equation. A converged finite-domain answer must not be promoted to all wavelengths, all initial data or an empirical fit.

## Completion criterion

Complete when a sharp source-time-dependent upper bound on the distance reached by a late massive carrier packet is established on the declared domain or its exact missing implication is isolated with a counterexample or blocker. Keep the same-action cosmological/observational implications conditional on the unevaluated sectors.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If promising, derive cosmological recapture criteria for exported charge.
2. If promising, construct a finite-horizon bound on interhalo transport.
3. If the implication fails, isolate the first term invalidating a sharp source-time-dependent upper bound on the distance reached by a late massive carrier packet; construct a minimal same-field action or boundary-condition repair and recheck this object before transferring any earlier pass.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS1291/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
