# MY2017-014 — GW170104: Vacuum-induced tensor refractive term

**Year:** 2017 · **Source:** Y2017S01 · **Kind:** inference · **Priority:** P1

Status: authored work order, not an execution receipt or scientific result.

## Dated measurement anchor

[GW170104: Observation of a 50-Solar-Mass Binary Black Hole Coalescence at Redshift 0.2](https://arxiv.org/abs/1706.01812) — LIGO Scientific Collaboration and Virgo Collaboration. Identifier: `arXiv:1706.01812`.

Dated report/release anchor: **2017-06-01** (day precision). Date basis: Collaboration detection page https://ligo.org/detections/gw170104/ dates public announcement to 2017-06-01; arXiv v1 followed on June 6.. Version: Historical arXiv v1 anchors the report; current arXiv v2 abstract and submission history inspected. Full-text changes between versions were not compared. First public-date exceptions are recorded in date_basis.. Observations: 2017-01-04.

Reported measurement: Detector strain, waveform phase and inferred compact-binary parameters; GR-dependent masses and propagation bounds.

Data availability: Primary abstract/report page and PDF link verified. Raw data, complete likelihood, numerical tables and covariance availability not inspected; obtain and authenticate before numerical inference.

Verification scope: Opened the primary arXiv report and read abstract plus submission metadata. Authentication covers reported observable and calendar assignment, not raw likelihood extraction or proof of the proposed gravity interpretation. Locator: Abstract and submission-history/header; proposal equations below are original work orders, not attributed source results.. Checked 2026-09-27. These metadata authenticate an anchor; the proposed calculations below are original work orders and are not claims made by its authors.

Source-record SHA-256: `4981fb698c45c4267badfcd419441da70adb0c52b6b5e140c600c496d71a12b1` (metadata only; hash acquired payloads separately).

## Core framework and first-principles footing

Use the [core framework contract](../../FRAMEWORK_CONTRACT.md), current [standing](../../../../STANDING.md), and the [amended thirteen-gate specification](../../../../qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md). The amendment overrides historical targets. Pin the same action, physical metric, matter coupling, source/state domain, boundary conditions and parameter cell throughout. Read the pinned source list below before selecting a candidate; this card does not assert that any current candidate is closed.

The scale relation is `a0=(c/2)*sqrt(G_N*rho_Lambda)` with vacuum **mass density** in kg/m³; `kappa=1/2` is adopted unless independently derived. Evaluate dimensional examples separately at canonical `a0=9.3619e-11 m/s²` and alternative `1.1279e-10 m/s²`. Changing a0 with fixed kappa changes rho_Lambda. Keep measured `G_N`, action `G_E` and cosmological coupling distinct: `Lambda_eff=32*pi*(G_E/G_N)*a0²/c⁴`. If V0 denotes SI vacuum energy density, `a0²=G_N*V0/4` and `H_vac²=8*pi*G_E*V0/(3*c²)` under the stated vacuum-background assumptions.

The operative branch is **filtered MONO**, not an interchangeable scalar fit. Let `B=g_bar`, `y=B/a0`, `h_RAR=y*(nu_RAR-1)`, `nu_RAR=1/(1-exp(-sqrt(y)))`; use `h'_mono=max(h'_RAR,0.05*h_p/(y+y_p))`, with the specified continuous join. Rounded landmarks `y_star≈2.3374`, `y_p≈2.5396` are not exact roots. The filter is `S=exp(xi²*Delta/2)`; its adjoint depends on metric, measure and boundary domain. Derive the field/metric observation map before evaluating data. `r>>xi` can justify a controlled approximation, not exact equality with `xi=0`.

Comparison laws `Q: g²=B²+a0*B`, `RAR: g=B*nu_RAR(B/a0)`, and `MU2: [1-(1+g/(2*a0))^-2]*g=B` are distinct; historical EXP is separate. Never silently substitute them for filtered MONO or assume spherical identities hold for arbitrary sources. Use criterion **B** with a consistent preferred foliation and well-posed mixed problem, not an unproved blanket speed requirement. Count gravitational and permitted matter modes separately. No unannounced particle species, per-object force correction or quantum completion. A published GR/LambdaCDM posterior is a conditional derived product until translated.

The thirteen gates cover: static MONO; gravitational modes; both potentials/lensing; PPN; matter conservation; tensor sector; stability/criterion B; expanding cosmology; zero-field limits; Newton/GR and measured G; one physical metric; prescribed RAR/MONO segment; and the a0–vacuum relation. Successful observation-level evidence supplies only its stated edge in this common-action dependency graph.

## Principle and exact mathematical target

Vacuum-induced tensor refractive term must be inferred from the measured observation functional and its nuisance directions. A source-reported GR/LambdaCDM posterior is conditional on its original observation map; this task seeks a new, explicitly scoped candidate-theory result.

Mathematical starting relation/estimand:

```text
delta n_T(f)=partial_k omega_T/c-1 from the quadratic tensor action, then integrate phase along the event ray. Symbols are task-local; define units, normalizations and domains before calculation. Approximate/GR reference expressions in this work order are diagnostic limits to derive, not an asserted candidate law.
```

Define every symbol, units, sign, domain and approximation before use. Treat schematic formulas as obligations to derive, not established framework theorems.

## Measurement inputs and unique new information

GW170104 propagation residual and candidate vacuum background. Anchor: https://arxiv.org/abs/1706.01812. Primary abstract/report page and PDF link verified. Raw data, complete likelihood, numerical tables and covariance availability not inspected; obtain and authenticate before numerical inference. Any additional measurement named here must receive its own primary-source authentication and version pin before use; otherwise give a symbolic/partially identified result.

New proposed application of the 2017-06-01 GW170104 report: obtain vacuum-induced tensor refractive term, specifically delta n_T(f)=partial_k omega_T/c-1 from the quadratic tensor action, then integrate phase along the event ray. This is an additional release-resolved estimand/conditional theorem beyond the old AS catalog's generic action, projection and evidence obligations; it does not claim that this historical measurement was unavailable in 2026, nor claim a literature novelty theorem. Other tasks on this source seek different mathematical outputs from the same data.

## Ordered execution

1. Authenticate the pinned arXiv:1706.01812 measurement version and extract only the inputs required for vacuum-induced tensor refractive term: GW170104 propagation residual and candidate vacuum background. Separate measured quantities from derived GR parameters, mark inaccessible data, and lock the source/selection/covariance provenance.
2. Vary the reduced tensor action, derive source energy balance and retarded propagation, then project geodesic deviation onto the two interferometers. Specialize that derivation to vacuum-induced tensor refractive term; identify the precise observable and all approximation conditions before using the displayed estimand.
3. Derive and evaluate the task equation: delta n_T(f)=partial_k omega_T/c-1 from the quadratic tensor action, then integrate phase along the event ray. Carry the actual release window, units and nuisance correlations; if information is missing, compute the admissible symbolic range or rank deficiency rather than inventing a central value.
4. Run the negative and independent controls below on this estimand, then propagate their residuals into the uncertainty/error budget for vacuum-induced tensor refractive term. State whether each check is analytic, finite numerical or data-limited.
5. Write the MY2017-014 result with an explicit allowed/excluded/unidentified parameter region or conditional lemma, the release-overlap ledger and the exact implication to 6 tensor propagation; 7 criterion-B evolution; 10 measured-G recovery. Separate new evidence from unproved dynamics and nominate the three continuations below.

## Falsifiable controls

- Negative control: Reverse the frequency-dependent propagation phase while holding the injected source waveform fixed; the signed propagation statistic must reverse, not remain spuriously unchanged. Evaluate its effect on the specific vacuum-induced tensor refractive term statistic, not only on a global fit score.
- Independent control: Inject a nondispersive coherent signal into independently selected off-source detector noise and recover zero excess phase within calibrated coverage. Archive the residual relevant to vacuum-induced tensor refractive term and its units; a Boolean success is insufficient.
- Inference control: repeat the actual vacuum-induced tensor refractive term estimand after an admissible nuisance/approximation change identified in the displayed equation; report whether any apparent gravity sensitivity is entirely prior or truncation driven.

A negative control is deliberately wrong. Show why it should fail in the stated domain. If the actual data cannot distinguish it, report limited identifiability; do not fabricate rejection or declare the correct model false. Predeclare tolerances and preserve failed controls.

## First-principles obligation and closure bridge

Vary the reduced tensor action, derive source energy balance and retarded propagation, then project geodesic deviation onto the two interferometers. The obligation is specifically delta n_T(f)=partial_k omega_T/c-1 from the quadratic tensor action, then integrate phase along the event ray. Use a0=(c/2)sqrt(G_N rho_Lambda), with rho_Lambda a mass density and 1/2 explicitly adopted unless independently derived. Keep canonical a0=9.3619e-11 and alternative a0=1.1279e-10 m/s² as distinct fixed models; G_N, G_E, G_bare, G_cosmo are not identified without proof. Pin action revision, matter coupling, heat-filter metric/measure/domain/boundaries, kernel, gate and initial data. Filtered MONO is operative; Q, RAR and MU2 are comparison branches unless an observation-map bridge is proved. No extra particles or per-object force fits may silently repair a mismatch. Criterion B uses a global preferred time; classical agreement is not quantum completion or thirteen-gate closure. 

The output for vacuum-induced tensor refractive term can constrain 6 tensor propagation; 7 criterion-B evolution; 10 measured-G recovery only after the action-to-observable derivation above is established. Transfer the actual allowed region and error/domain conditions to one shared action cell; a missing dynamical map is an OPEN dependency, and an empirical fit cannot certify the other thirteen-gate requirements. Use a0=(c/2)sqrt(G_N rho_Lambda), with rho_Lambda a mass density and 1/2 explicitly adopted unless independently derived. Keep canonical a0=9.3619e-11 and alternative a0=1.1279e-10 m/s² as distinct fixed models; G_N, G_E, G_bare, G_cosmo are not identified without proof. 

Separate primitive assumptions, measured calibrations, boundary/initial data, derived consequences and unresolved implications. Any worker may pursue a complete same-action witness through the [closure template](../../CLOSURE_WITNESS_TEMPLATE.md), but independent review of all gates is required. A fit or successful numerical example is not a derivation of the action, coefficient or vacuum scale.

## Required output and completion condition

MY2017-014: deliver vacuum-induced tensor refractive term as an explicit observation-map derivation and a reproducible equation/estimand evaluation, with its numerical region or non-identifiability witness, nuisance covariance and approximation-error envelope. Save the unique result as my2017-014_result.md plus its task-specific input/likelihood manifest; no catalog-authoring step executes this calculation.

Write the actual result and artifacts under `measurement_decade_2017_2026/results/MY2017-014/<unique-run-id>/`. Use [RESULT_CONTRACT.json](../RESULT_CONTRACT.json), including actual model identity, exact claim, execution/acceptance status, source/data/artifact hashes, equations, controls, tested range, overlap treatment, failed routes and next missing implication. A symbolic proof-only result needs its raw derivation and independent review. An unavailable dataset produces a precise blocked inference, not a synthetic substitute. A record is review-ready only when every field is supplied or explicitly marked not applicable with a reason.

## Reuse, overlap and prerequisites

Declared dependencies: No predeclared seed-ID dependency. Discover and register the exact theory/data dependencies before execution; this does not imply the observation map already exists.

GW170104 strain is reused in GWTC-1. Select one strain analysis or condition the update on the old data; calibration nuisance is shared with O2 events. The 25 work orders attached to Y2017S01 are correlated analyses, not 25 datasets. For vacuum-induced tensor refractive term, identify every reused row/epoch/mode and share the corresponding nuisance block before any combined significance or information-gain calculation.

Before claiming work, search both seed manifests, child registries and live AS/MY/FGF claims/results. Reuse an existing generic theorem or active owner. New title/year alone is not novelty. Shared objects, pixels, events, calibrations or simulations need a joint covariance, conditional increment, or separate alternative analysis; do not multiply dependent evidence.

## Finding-driven continuation

1. **Promising result:** Promising extension: carry the derived vacuum-induced tensor refractive term likelihood/domain into the neighboring, distinct question "Heat-filter tensor contamination". Derive its new target T_tensor(k, xi)=exp(-xi²k²/2) only if obtained from varied tensor equations; bound any induced attenuation, including cross-response/covariance with the present output; do not count the reused release as independent evidence.
2. **Independent bridge:** Independent bridge: use the explicit vacuum-induced tensor refractive term result to predict a matching observable in the lower-mass GW170608 inspiral, with one shared propagation coefficient. Derive the translation from the same action and authenticate that second observation before a joint inference.
3. **Failure or obstruction:** Failed-route repair: if vacuum-induced tensor refractive term fails its control or is not identifiable from GW170104 propagation residual and candidate vacuum background, preserve the failing residual/null direction. Determine the minimum additional calibrated observable or action-derived term that separates the degeneracy in delta n_T(f)=partial_k omega_T/c-1 from the quadratic tensor action, then integrate phase along the event ray; if none exists within the pinned model, deliver the scoped obstruction rather than retuning gravity per object.

These are candidate branches, not preapproved scientific conclusions. A child must cite an actual parent result and evidence hashes, name its new equation/estimand, closest existing task, substantive difference, controls, prerequisites and finite resources. Use `MY2017-014.C01` etc. with a unique claim and write scope; descendants remain provisional until reviewed. At most two live children per parent and two levels before orchestrator reconciliation; later reviewed waves may continue. Follow [DISPATCH.md](../DISPATCH.md) and the [first-principles protocol](../../FIRST_PRINCIPLES_AND_BRANCHING.md). If no runner is available, return a ready child specification without claiming it ran.

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
