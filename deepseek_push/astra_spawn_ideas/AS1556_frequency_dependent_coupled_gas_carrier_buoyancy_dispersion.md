# AS1556 — Frequency-dependent coupled gas-carrier buoyancy dispersion

**Group:** A15 — Clusters, mergers and the common source gate  
**Priority:** P0 · **Kind:** derivation · **Execution state:** proposed; not dispatched  
**Branch:** CA5-GNC-R where the supplied action reduction applies; CA4-PQ results transfer only with an explicit equation-level equality proof. Filtered nu_mono and criterion B retained.  
**Explicit prerequisites:** AS351, AS782

## Assignment and principle

Derive the buoyancy-branch dispersion relation when the cluster gas perturbs the same dynamical carrier and constrained gravitational fields that support it. The new object is the frequency-dependent coupled response, beyond the frozen-force entropy criterion in AS782.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [real_research/common_action_2026_09_26/action/FINAL_ACTION.md](../../real_research/common_action_2026_09_26/action/FINAL_ACTION.md) — pinned SHA-256 `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e`.
- [campaign_fresh_gravity_astra/stage_03/cluster_precision/DERIVATION.md](../../campaign_fresh_gravity_astra/stage_03/cluster_precision/DERIVATION.md) — pinned SHA-256 `4fcd05ab4781e790e51bd883e6fc67edcc9c339a359a85b9bebb6e921481f325`.
- [real_research/breakthrough_review_2026_09_26/README.md](../../real_research/breakthrough_review_2026_09_26/README.md) — pinned SHA-256 `22cacef2b949f88c5539a81291f14232d01e8b1bbad266956018bcde6c6e32ab`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
For perturbations proportional to exp(i k.x-i omega t), derive the constraint-reduced block symbol D=[[Dgg,Dgc],[Dcg,Dcc]]; physical modes satisfy det D=0. Where Dcc is invertible the gas response is Dgg-Dgc Dcc^-1 Dcg. In the adiabatic local frozen-force limit recover omega²=N_BV² k_perp²/|k|², N_BV²=g[(1/gamma_ad)dlnP/dr-dlnrho/dr]; Im omega>0 means growth in this convention. Dcc poles must be checked in the full block determinant, never discarded.
```

## Inputs, domain and first bound

Use one smooth hydrostatic baryonic gas profile P(r),rho(r), its adiabatic index, and a stationary occupied solution of the same CA5 action with stated radial boundaries. If only a slowly varying solution exists, state the frozen-background error and admit wavelengths/times satisfying that approximation. Begin with eight local wavevectors within the gas continuum and background-gradient validity bounds, then sixteen. Supply action-derived carrier/source response coefficients; a guessed relaxation time or prescribed decay fluid does not qualify. Missing a compatible occupied cluster background is a named blocker.

## First-principles obligation

Derive the reciprocal gas/carrier blocks and their retarded frequency dependence from the same action, gas conservation and constraint variation, rather than assuming a relaxation law. Gas equation of state, background occupation, boundary data and action couplings remain supplied inputs. Keep a0=(c/2)sqrt(G_N rhoLambda), adopted kappa=1/2, filtered MONO and criterion B; G_E/Gcosm are separate couplings.

## Contribution to common-theory closure

A cluster mass-support solution used for lensing or hydrostatic inference must also survive coupled gas/carrier perturbations at the same parameters. The derived dispersion supplies that necessary local dynamical condition without claiming global nonlinear stability or observed cluster agreement.

## Execute in order

1. Vary ordinary gas conservation and the common carrier/metric action about the supplied cluster solution. Eliminate lapse and auxiliary constraints with boundary and projector variations retained; identify physical gas and carrier variables and their units. Do not transplant the homogeneous FRW perturbation matrix into this inhomogeneous background.
2. Construct Dgg,Dgc,Dcg,Dcc and the retarded Schur response on its valid domain. Identify the branch continuously connected to the AS782 buoyancy mode as reciprocal coupling is turned off, and keep the complete determinant near carrier resonances.
3. Locate complex roots for the declared wavevectors and derive either a bounded stability condition or an explicit overstable root with positive real frequency and positive imaginary part. Verify it against the unreduced constrained initial-value system and double spectral/time resolution at the same physical wavevector.
4. Recover the frozen-force buoyancy limit and report the action term responsible for any new growth or damping. Bound finite-domain, local-gradient and frozen-background errors; return the dispersion relation and scoped admissible parameter region or the exact missing response/background obstruction.

## Controls that must be capable of failing

- Negative control: replace the carrier response by its zero-frequency value near a resolved carrier resonance; require this shortcut to fail the full determinant or the direct time evolution before using it as evidence for a buoyancy verdict.
- With reciprocal perturbative coupling removed, recover AS782 and distinguish k_perp=0 from transverse buoyancy. Check conjugate-root symmetry for real coefficients and verify that a canceled Schur denominator does not delete a physical carrier mode.

## Completion criterion

Deliver the frequency-dependent buoyancy dispersion and one certified stable region, unstable witness, or explicit missing-background/response blocker. This is a finite wavevector and stated-background result; a positive frozen-force N_BV² alone does not complete it.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If a stable frequency-dependent branch exists, derive its radial wave-action flux and turning-point conversion in a slowly stratified cluster using the computed mode eigenvectors.
2. If a resolved weakly damped resonance exists, derive the transfer from that eigenmode to jointly projected X-ray pressure and thermal-SZ fluctuations, including the ordinary gas emissivity inputs.
3. If an overstable mode survives both checks, isolate its reciprocal coupling and derive the minimum background occupation or boundary-flux change that removes it without changing the action; if none exists on the admitted domain, state that scoped obstruction.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS1556/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
