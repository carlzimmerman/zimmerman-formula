# AS861 — Regulator dependence of thermal carrier charge susceptibility

**Group:** A05 — Statistical mechanics and the gravity-response bridge  
**Priority:** P2 · **Kind:** derivation · **Execution state:** proposed; not dispatched  
**Branch:** Lomax/MU2 statistical-response diagnostics; no identification with MONO or metric gravity without an action-derived bridge. New stochastic dynamics are explicitly proposed models.  
**Explicit prerequisites:** AS860

## Assignment and principle

A stationary measure does not determine its generator, response, absolute energy or gravitational coupling. Derive one identifiable statistical or dynamical obligation with the sampling and reference measures explicit.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [real_research/common_action_2026_09_26/action/FINAL_ACTION.md](../../real_research/common_action_2026_09_26/action/FINAL_ACTION.md) — pinned SHA-256 `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e`.
- [deepseek_push/G228_lomax_maxent.py](../../deepseek_push/G228_lomax_maxent.py) — pinned SHA-256 `cb82a65c2825e1633941ad286053876f2315ed60c16cdf3f6a24d9377265551d`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
For normalized classical charged normal-mode actions I_k^+,I_k^-: H=sum omega_k(I_k^++I_k^-), Q=sum(I_k^+-I_k^-), Z=integral exp[-beta(H-mu Q)]dGamma. chi_Q(K)=partial_mu<Q>|_0=beta Var(Q)|_0=2T sum_|k|<=K omega_k^-2 in this normalization, beta=1/T.
```

## Inputs, domain and first bound

Existing carrier fields only, a fixed finite periodic three-dimensional volume, stable quadratic branch with omega_k>0 and ultraviolet omega_k~c_s|k|. Set c=k_B=1 explicitly. Count physical charged branches from the action; do not add particle species. Keep K finite before any limit, and |mu|<min omega_k. Use the canonical mode measure derived from the quadratic symplectic form.

## First-principles obligation

Derive the Gibbs charge response from the existing action and its canonical U(1) generator. Temperature, chemical-potential ensemble, finite volume and regulator remain declared assumptions; thermal accessibility is not inferred.

## Contribution to common-theory closure

A statistical carrier closure using charge compressibility must match a finite, physically normalized susceptibility to the common action; total-energy regularization alone does not establish that response.

## Execute in order

1. Fix the source equation, independent variables, boundary conditions and measure from the cited branch. State any additional assumption needed for the displayed target.
2. Derive the charge susceptibility from the actual diagonal U(1) charge, including mode degeneracies and normalization. Determine its leading K dependence and whether fixing mean charge permits a nonzero regulator-independent small-mu response at fixed temperature. Do not repeat the total-energy equipartition calculation in AS1423.
3. Specify the forward/backward generator or probability measure, normalization, support and boundary current. Distinguish distributional identities from dynamical assumptions and preserve the source coupling when translating to gravitational variables.
4. Test the altered premise: Infer a finite continuum charge susceptibility merely because the thermal mean charge vanishes at mu=0. Exhibit its violated equation or omitted term.
5. Verify the resulting equation by substitution or an independent representation. Report its exact scope and the first missing implication for the stated closure bridge.

## Controls that must be capable of failing

- Check units, signs, normalization and one admissible boundary or limiting case in the same measure.
- Negative control: Infer a finite continuum charge susceptibility merely because the thermal mean charge vanishes at mu=0.

## Completion criterion

Deliver the explicitly displayed response identity and its domain, or an exact obstruction from the stated equations; preserve the independent empirical and ensemble inputs.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If promising, derive the charge-response matching condition under a physical coarse-graining change.
2. If promising, determine the charge fluctuation correction to a long-wavelength auxiliary response using the same finite regulator.
3. If failed, replace equilibrium closure by an explicitly finite-energy occupation law and derive its charge response before claiming continuum thermodynamics.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS861/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
