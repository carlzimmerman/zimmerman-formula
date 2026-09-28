# AS1418 — Detailed balance for classical resonant wave populations

**Group:** A13 — Nonlinear carrier transport and phase conversion  
**Priority:** P1 · **Kind:** derivation · **Execution state:** proposed; not dispatched  
**Branch:** CA5-GNC-R where the supplied action reduction applies; CA4-PQ results transfer only with an explicit equation-level equality proof. Filtered nu_mono and criterion B retained.  
**Explicit prerequisites:** AS1417, AS301

## Assignment and principle

Determine the following single implication: The stationary population family and its domain of positivity The output is the named mathematical object, with an explicit domain and failure condition, rather than a new interpretation of a preexisting numerical pass.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [real_research/common_action_2026_09_26/transport/CONVERSION.md](../../real_research/common_action_2026_09_26/transport/CONVERSION.md) — pinned SHA-256 `f72f861c486a44fec17d82175c9b5dc439f474d288ee79dbc9f0977286f972f2`.
- [real_research/breakthrough_review_2026_09_26/transport/RESULT.md](../../real_research/breakthrough_review_2026_09_26/transport/RESULT.md) — pinned SHA-256 `3977dd5018bc06870059a1bb6fb336b52f4073cc2a7b9f44a9ad5bcbb59941ed`.
- [real_research/breakthrough_review_2026_09_26/README.md](../../real_research/breakthrough_review_2026_09_26/README.md) — pinned SHA-256 `22cacef2b949f88c5539a81291f14232d01e8b1bbad266956018bcde6c6e32ab`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
C[n_eq]=0 with inverse occupations linear in conserved frequencies and charges when the derived statistics permit it.
```

## Inputs, domain and first bound

Use the existing two complex carriers Psi,Chi and real pump s with V=M²|Psi|²+m²|Chi+gamma s Psi|²+mu²s²/2, including its quartic term; no extra particle species or imposed decay rate. Use a periodic or stated open finite domain,32 to128 resolved spatial modes and a finite energy budget. Start on a fixed background only when stated, and record what changes when the reciprocal auxiliary evolves.

## First-principles obligation

Test or derive the stationary population family and its domain of positivity from the classical positive-square action and its diagonal U(1) current; derive every effective coefficient in the displayed object before using it. Remaining independent data include initial/boundary conditions and the stated action couplings; kappa=1/2 is adopted, a0=(c/2)sqrt(G_N rhoLambda), and G_E/Gcosm are not silently identified with G_N.

## Contribution to common-theory closure

This result supplies a transport or relaxation law derived from existing fields that could replace prescribed carrier clearing. Its necessary bridge is concrete: the stationary population family and its domain of positivity must hold for the actual solution/parameters used by the other sectors, with no substitution of another action, source convention or carrier population.

## Execute in order

1. Derive the displayed object from the classical positive-square action and its diagonal U(1) current. Identify all background equations, constraints and boundary terms used in the reduction; isolate any extra assumption required specifically for the stationary population family and its domain of positivity
2. Solve channel-by-channel balance conditions and check whether finite ultraviolet cutoffs or condensation are required.
3. Construct an independent limiting case or exact small-system calculation for detailed balance for classical resonant wave populations. Compare it with the full restricted model at fixed physical normalization; refine the decisive residual rather than merely increasing the number of sampled points.
4. Return the formula, admissible set and one explicit witness or obstruction for the stationary population family and its domain of positivity Give solver-error bounds or analytic estimates and preserve any failure that changes the conclusion.

## Controls that must be capable of failing

- Negative control: A negative occupation generated by an inadmissible chemical-potential parameter must be rejected.
- Check dimensions, action identity and normalization on the displayed equation. A converged finite-domain answer must not be promoted to all wavelengths, all initial data or an empirical fit.

## Completion criterion

Complete when the stationary population family and its domain of positivity is established on the declared domain or its exact missing implication is isolated with a counterexample or blocker. Keep the same-action cosmological/observational implications conditional on the unevaluated sectors.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If promising, derive a finite-band equilibrium closure.
2. If promising, construct continuum ultraviolet limitations of classical thermalization.
3. If the implication fails, isolate the first term invalidating the stationary population family and its domain of positivity; construct a minimal same-field action or boundary-condition repair and recheck this object before transferring any earlier pass.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS1418/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
