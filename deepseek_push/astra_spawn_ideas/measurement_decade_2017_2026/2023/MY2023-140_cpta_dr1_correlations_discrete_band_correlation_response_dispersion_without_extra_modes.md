# MY2023-140 — CPTA DR1 correlations: discrete-band correlation response: dispersion without extra modes

**Year:** 2023 · **Source:** Y2023S06 · **Kind:** inference · **Priority:** P1

Status: authored work order, not an execution receipt or scientific result.

## Dated measurement anchor

[Searching for the nano-Hertz stochastic gravitational wave background with the Chinese Pulsar Timing Array Data Release I](https://arxiv.org/abs/2306.16216) — Xu et al.; CPTA. Identifier: `arXiv:2306.16216`.

Dated report/release anchor: **2023-06-28** (day precision). Date basis: Initial arXiv measurement-report submission shown by the primary page; later journal publication/revisions do not change the assigned year. Observation dates are separate.. Version: v1 dated 2023-06-28. Observations: unknown.

Reported measurement: Correlated signal and angular correlation search using FAST pulsar timing.

Data availability: Primary report accessible; machine-readable data, masks, covariance and likelihood archive contents not inspected. Availability of required ancillary products remains unverified.

Verification scope: Opened primary arXiv abstract page and read initial submission date, title, and reported observable. Full-text equations, tables, archive payloads and likelihood implementation were not audited; tasks require their extraction before numerical claims. Locator: Abstract; initial submission line and Submission history; Comments where archive availability is stated. Checked 2026-09-27. These metadata authenticate an anchor; the proposed calculations below are original work orders and are not claims made by its authors.

Source-record SHA-256: `b319f241ece2fcd900b090cc790bc8946d334a50f53d8106118c26a7baf91a7a` (metadata only; hash acquired payloads separately).

## Core framework and first-principles footing

Use the [core framework contract](../../FRAMEWORK_CONTRACT.md), current [standing](../../../../STANDING.md), and the [amended thirteen-gate specification](../../../../qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md). The amendment overrides historical targets. Pin the same action, physical metric, matter coupling, source/state domain, boundary conditions and parameter cell throughout. Read the pinned source list below before selecting a candidate; this card does not assert that any current candidate is closed.

The scale relation is `a0=(c/2)*sqrt(G_N*rho_Lambda)` with vacuum **mass density** in kg/m³; `kappa=1/2` is adopted unless independently derived. Evaluate dimensional examples separately at canonical `a0=9.3619e-11 m/s²` and alternative `1.1279e-10 m/s²`. Changing a0 with fixed kappa changes rho_Lambda. Keep measured `G_N`, action `G_E` and cosmological coupling distinct: `Lambda_eff=32*pi*(G_E/G_N)*a0²/c⁴`. If V0 denotes SI vacuum energy density, `a0²=G_N*V0/4` and `H_vac²=8*pi*G_E*V0/(3*c²)` under the stated vacuum-background assumptions.

The operative branch is **filtered MONO**, not an interchangeable scalar fit. Let `B=g_bar`, `y=B/a0`, `h_RAR=y*(nu_RAR-1)`, `nu_RAR=1/(1-exp(-sqrt(y)))`; use `h'_mono=max(h'_RAR,0.05*h_p/(y+y_p))`, with the specified continuous join. Rounded landmarks `y_star≈2.3374`, `y_p≈2.5396` are not exact roots. The filter is `S=exp(xi²*Delta/2)`; its adjoint depends on metric, measure and boundary domain. Derive the field/metric observation map before evaluating data. `r>>xi` can justify a controlled approximation, not exact equality with `xi=0`.

Comparison laws `Q: g²=B²+a0*B`, `RAR: g=B*nu_RAR(B/a0)`, and `MU2: [1-(1+g/(2*a0))^-2]*g=B` are distinct; historical EXP is separate. Never silently substitute them for filtered MONO or assume spherical identities hold for arbitrary sources. Use criterion **B** with a consistent preferred foliation and well-posed mixed problem, not an unproved blanket speed requirement. Count gravitational and permitted matter modes separately. No unannounced particle species, per-object force correction or quantum completion. A published GR/LambdaCDM posterior is a conditional derived product until translated.

The thirteen gates cover: static MONO; gravitational modes; both potentials/lensing; PPN; matter conservation; tensor sector; stability/criterion B; expanding cosmology; zero-field limits; Newton/GR and measured G; one physical metric; prescribed RAR/MONO segment; and the a0–vacuum relation. Successful observation-level evidence supplies only its stated edge in this common-action dependency graph.

## Principle and exact mathematical target

Discrete-band correlation response: dispersion without extra modes tests a distinct observable implication of a single gravity model. The CPTA discrete-frequency correlation measurement has a short-baseline window distinct from NANOGrav; derive its frequency-window-weighted response instead of importing a broadband amplitude. The proposed new result is discrete-frequency window and leakage contribution to two-mode dispersive overlap correction for CPTA DR1 correlations, using its actual measured selection/windows and source-specific covariance; the cited authors are not claimed to have performed this calculation.

Mathematical starting relation/estimand:

```text
Base physical quantity q: omega^2=c_T^2 k^2+Delta_action(k). Distinct measured estimand: q_k=O_q[W_k C_ab W_k^T]; leakage_k=sum_j_not_k O_q[W_k C_j W_k^T]. Define every symbol and domain in the derivation, derive this observation/estimand relation from the pinned action where physical, and audit its approximation order; a schematic relation here is a work obligation, not a completed theorem. Target: discrete-frequency window and leakage contribution to two-mode dispersive overlap correction for CPTA DR1 correlations, using its actual measured selection/windows and source-specific covariance.
```

Define every symbol, units, sign, domain and approximation before use. Treat schematic formulas as obligations to derive, not established framework theorems.

## Measurement inputs and unique new information

Anchor arXiv:2306.16216, first report 2023-06-28. Measured timing residuals or released correlation likelihood, pulsar sky positions/distances, cadence, noise and timing-fit operators; obtain covariance rather than using one strain-amplitude posterior. For discrete-band correlation response: dispersion without extra modes, extract the measured quantities entering Base physical quantity q: omega^2=c_T^2 k^2+Delta_action(k). Distinct measured estimand: q_k=O_q[W_k C_ab W_k^T]; leakage_k=sum_j_not_k O_q[W_k C_j W_k^T] and their correlated uncertainties. Primary report accessible; machine-readable data, masks, covariance and likelihood archive contents not inspected. Availability of required ancillary products remains unverified. If the necessary payload is unavailable, return an exact extraction dependency plus valid symbolic progress; never fabricate rows or covariance. Additional required extraction: Use the CPTA reported discrete-frequency estimator and FAST cadence. Resolve the measurement-band response separately from broadband spectral extrapolation and calibrate adjacent-band leakage.

New measured-result objective: discrete-frequency window and leakage contribution to two-mode dispersive overlap correction for CPTA DR1 correlations, using its actual measured selection/windows and source-specific covariance. The CPTA discrete-frequency correlation measurement has a short-baseline window distinct from NANOGrav; derive its frequency-window-weighted response instead of importing a broadband amplitude. This is an application seeking this release-specific quantitative response/constraint, beyond generic old-AS methodological seeds; it does not claim a new universal mathematical method. The 2000-task manifest and AS1736 calibration seed were consulted for scope. The exact equation/output pair and source-conditioned inference, not merely the report label, define this obligation. Distinct estimand, not a report-name substitution: q_k=O_q[W_k C_ab W_k^T]; leakage_k=sum_j_not_k O_q[W_k C_j W_k^T]. Use the CPTA reported discrete-frequency estimator and FAST cadence. Resolve the measurement-band response separately from broadband spectral extrapolation and calibrate adjacent-band leakage.

## Ordered execution

1. Pin arXiv:2306.16216, the report/revision distinction, the common action and both acceleration footings. Extract the release fields needed for discrete-band correlation response: dispersion without extra modes, independently checking units, prior content, selection and shared observations; list unavailable payloads before numerical inference.
2. Derive the two tensor propagating modes and their positive kinetic normalization, propagate them on the solved background, and integrate each pulsar photon path before timing-fit projection. Derive the task-specific relation Base physical quantity q: omega^2=c_T^2 k^2+Delta_action(k). Distinct measured estimand: q_k=O_q[W_k C_ab W_k^T]; leakage_k=sum_j_not_k O_q[W_k C_j W_k^T]; identify each boundary, source-population and regularity premise needed for discrete-frequency window and leakage contribution to two-mode dispersive overlap correction.
3. Construct discrete-frequency window and leakage contribution to two-mode dispersive overlap correction for CPTA DR1 correlations, using its actual measured selection/windows and source-specific covariance. The CPTA discrete-frequency correlation measurement has a short-baseline window distinct from NANOGrav; derive its frequency-window-weighted response instead of importing a broadband amplitude. Identify the observable and nuisance directions mathematically; derive the conditioning/projection or likelihood normalization needed for this particular estimand, retaining a finite-data uncertainty or explicit nonidentifiability witness. Use the CPTA reported discrete-frequency estimator and FAST cadence. Resolve the measurement-band response separately from broadband spectral extrapolation and calibrate adjacent-band leakage.
4. Implement the intentionally wrong control: Use a massive-particle formula absent from the action; additionally, treat the correlated contrast/conditional components as independent. Require a measurable rejection or explain why the available data cannot distinguish it. Independently check: Inject a known two-tensor correlated process and independent clock/dipole contaminant through the actual cadence; test recovery without changing the noise fit. Use a bounded analytic fixture or small reproducible prototype before any larger inference; a synthetic recovery is not observed evidence.
5. Write MY2023-140 results to its own run directory when executed, with the exact discrete-frequency window and leakage contribution to two-mode dispersive overlap correction, covariance treatment, tested range and surviving assumptions. Separate theory derivation, numerical fixture and measured inference. State the precise input this supplies to gates 2, 6, 7, 8, 11, 13 and leave every unproved closure implication open.

## Falsifiable controls

- Negative control (deliberately wrong; must fail): Use a massive-particle formula absent from the action; additionally, treat the correlated contrast/conditional components as independent.
- Inject a known two-tensor correlated process and independent clock/dipole contaminant through the actual cadence; test recovery without changing the noise fit.
- For discrete-band correlation response: dispersion without extra modes, compare the direct defining observable with the equation-based compressed result using identical input realizations; quantify disagreement and approximation error rather than reporting only a pass flag.
- Contrast control: hold the physical sky/events fixed and alter only the explicitly isolated response/selection; the inferred physical component must remain invariant while the bias/innovation term changes as derived.

A negative control is deliberately wrong. Show why it should fail in the stated domain. If the actual data cannot distinguish it, report limited identifiability; do not fabricate rejection or declare the correct model false. Predeclare tolerances and preserve failed controls.

## First-principles obligation and closure bridge

Derive the two tensor propagating modes and their positive kinetic normalization, propagate them on the solved background, and integrate each pulsar photon path before timing-fit projection. Specific obligation: establish Base physical quantity q: omega^2=c_T^2 k^2+Delta_action(k). Distinct measured estimand: q_k=O_q[W_k C_ab W_k^T]; leakage_k=sum_j_not_k O_q[W_k C_j W_k^T] in the measurement convention that yields discrete-frequency window and leakage contribution to two-mode dispersive overlap correction. Use a0=(c/2)sqrt(G_N rho_Lambda) with mass-density rho_Lambda; kappa=1/2, vacuum magnitude and filter are adopted inputs unless explicitly derived. Carry canonical 9.3619e-11 and alternative 1.1279e-10 m/s^2 separately. Keep G_N, G_E, G_bare and G_cosmo distinct until matching is derived; Lambda_eff=32pi(G_E/G_N)a0^2/c^4. Pin action revision, ordinary-matter coupling, S=exp[(xi^2/2)Delta], S* measure/domain/boundary, source gate and occupation. Filtered nu_mono is operative; Q/RAR/MU2 are comparisons only until a bridge is proved. No added particle species or per-object rescue parameters. Published GR/LambdaCDM posteriors are conditional summaries, not theory-independent raw observations.

This result can supply the observable implication discrete-frequency window and leakage contribution to two-mode dispersive overlap correction to amended thirteen-gate requirements 2, 6, 7, 8, 11, 13, only for the identical action/parameter cell used elsewhere. Derive the observation map before any empirical closure claim. Count exactly two gravitational propagating degrees of freedom and any healthy allowed matter separately where relevant; stability uses criterion B (global preferred time, no backward-time paths, well-posed mixed problem). Neither a good fit nor classical consistency supplies a quantum completion or earns closure.

Separate primitive assumptions, measured calibrations, boundary/initial data, derived consequences and unresolved implications. Any worker may pursue a complete same-action witness through the [closure template](../../CLOSURE_WITNESS_TEMPLATE.md), but independent review of all gates is required. A fit or successful numerical example is not a derivation of the action, coefficient or vacuum scale.

## Required output and completion condition

discrete-frequency window and leakage contribution to two-mode dispersive overlap correction for CPTA DR1 correlations, using its actual measured selection/windows and source-specific covariance. Deliver a derivation, a machine-readable estimand/response definition, a covariance-aware measured constraint or explicitly conditional bound, and the controlled failure witness for the specified mutation. Record units, conventions, data hashes, model premises and whether an inference was executable. A missing action-to-observable map is a named unresolved implication, not an empirical success.

Write the actual result and artifacts under `measurement_decade_2017_2026/results/MY2023-140/<unique-run-id>/`. Use [RESULT_CONTRACT.json](../RESULT_CONTRACT.json), including actual model identity, exact claim, execution/acceptance status, source/data/artifact hashes, equations, controls, tested range, overlap treatment, failed routes and next missing implication. A symbolic proof-only result needs its raw derivation and independent review. An unavailable dataset produces a precise blocked inference, not a synthetic substitute. A record is review-ready only when every field is supplied or explicitly marked not applicable with a reason.

## Reuse, overlap and prerequisites

Declared dependencies: No predeclared seed-ID dependency. Discover and register the exact theory/data dependencies before execution; this does not imply the observation map already exists.

Family CPTA-DR1. The CPTA discrete-frequency correlation measurement has a short-baseline window distinct from NANOGrav; derive its frequency-window-weighted response instead of importing a broadband amplitude. These 25 work orders reuse one report and are not 25 independent datasets. Build an object/event/pixel/epoch overlap map before combining any related release; retain cross-covariance or use a conditional innovation likelihood, and exclude duplicate observations. Different summaries of identical samples are representation or conditional-information tests, not independent confirmation. Audit external-anchor reuse separately. Known cross-source links: Check pulsar/event/object matches and shared calibrators against all external data before asserting independence.

Before claiming work, search both seed manifests, child registries and live AS/MY/FGF claims/results. Reuse an existing generic theorem or active owner. New title/year alone is not novelty. Shared objects, pixels, events, calibrations or simulations need a joint covariance, conditional increment, or separate alternative analysis; do not multiply dependent evidence.

## Finding-driven continuation

1. **Promising result:** Promising extension: combine the derived discrete-frequency window and leakage contribution to two-mode dispersive overlap correction with the distinct estimand low-frequency transfer after spin and astrometry fitting (C_post=P_a C_pre P_b^T) under a joint covariance, and determine which additional physical direction becomes identifiable. This is a new joint implication, not a second run of the same marginal fit.
2. **Independent bridge:** Independent bridge: test the surviving discrete-band correlation response: dispersion without extra modes implication using another pulsar array with shared arrival times/pulsars identified and common clocks modelled; derive the cross-observation map and common-data covariance before asserting agreement.
3. **Failure or obstruction:** Failed-route repair: if the control "Use a massive-particle formula absent from the action; additionally, treat the correlated contrast/conditional components as independent" cannot be rejected, construct the exact nuisance/physical null direction that hides discrete-frequency window and leakage contribution to two-mode dispersive overlap correction, then specify the minimal independent calibration or missing field equation required to break it; preserve the original failure and do not change branches silently.

These are candidate branches, not preapproved scientific conclusions. A child must cite an actual parent result and evidence hashes, name its new equation/estimand, closest existing task, substantive difference, controls, prerequisites and finite resources. Use `MY2023-140.C01` etc. with a unique claim and write scope; descendants remain provisional until reviewed. At most two live children per parent and two levels before orchestrator reconciliation; later reviewed waves may continue. Follow [DISPATCH.md](../DISPATCH.md) and the [first-principles protocol](../../FIRST_PRINCIPLES_AND_BRANCHING.md). If no runner is available, return a ready child specification without claiming it ran.

## Pinned local base

- [STANDING.md](../../../../STANDING.md): `660462ebe8f98844c418e173a1dada90b9df3800c4d445fd5a0556eb9476bf63`
- [qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md](../../../../qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md): `98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f`
- [real_research/breakthrough_review_2026_09_26/README.md](../../../../real_research/breakthrough_review_2026_09_26/README.md): `22cacef2b949f88c5539a81291f14232d01e8b1bbad266956018bcde6c6e32ab`
- [real_research/common_action_2026_09_26/README.md](../../../../real_research/common_action_2026_09_26/README.md): `4381ce719f9f203e7dba73508203bdf2b354e9fd32f9d9eac7d9911b4222ae20`
- [deepseek_push/astra_spawn_ideas/FRAMEWORK_CONTRACT.md](../../FRAMEWORK_CONTRACT.md): `ca696c7fe7cccbe21d754eff833a4c59df6dee962ea61f50f04b5d20d80dddf9`
- [deepseek_push/astra_spawn_ideas/FIRST_PRINCIPLES_AND_BRANCHING.md](../../FIRST_PRINCIPLES_AND_BRANCHING.md): `f633cdb4f487a16d6ad345092faabbeb1db88c6ca27a010732ba31f65f5c570f`
- [deepseek_push/astra_spawn_ideas/ORCHESTRATOR.md](../../ORCHESTRATOR.md): `2eb07b9d1995ff2223a15219bbf7fc813be56fb69337ed4dd14d170c1dcaf671`
- [deepseek_push/astra_spawn_ideas/measurement_decade_2017_2026/DISPATCH.md](../DISPATCH.md): `3ac3cbccf8d5f324cb46ec0650449df05b708b5e509a0f610adc24d87ff0421a`
- [deepseek_push/astra_spawn_ideas/measurement_decade_2017_2026/RESULT_CONTRACT.json](../RESULT_CONTRACT.json): `903cef0f1e798cad896ae9ea59da291621d586c7214b0a2e19b2d49a8284b405`
