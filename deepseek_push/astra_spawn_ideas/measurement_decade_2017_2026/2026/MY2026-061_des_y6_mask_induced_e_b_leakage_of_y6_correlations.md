# MY2026-061 — DES Y6 — Mask-induced E/B leakage of Y6 correlations

**Year:** 2026 · **Source:** Y2026S03 · **Kind:** inference · **Priority:** P1

Status: authored work order, not an execution receipt or scientific result.

## Dated measurement anchor

[Dark Energy Survey Year 6 Results: Cosmological Constraints from Galaxy Clustering and Weak Lensing](https://arxiv.org/abs/2601.14559) — DES Collaboration. Identifier: `arXiv:2601.14559`.

Dated report/release anchor: **2026-01-21** (day precision). Date basis: First arXiv submission of this measurement report, verified in submission history. Version: v2, 2026-01-29. Observations: DES six observing years, 2013–2019; source/lens cuts release-dependent.

Reported measurement: Three two-point functions: source-shape correlations, lens-position clustering and galaxy-galaxy lensing.

Data availability: Collaboration page https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/ links https://des.ncsa.illinois.edu/releases/y6a2; latter returned no extractable page text, so file/schema availability remains unverified.

Verification scope: Opened the primary report/release page and read its measurement description and date/version metadata. This authenticates the report, not its conclusions. Full likelihood files, numerical tables and covariance contents were not audited; acquire and hash before inference. Locator: Abstract and submission history; collaboration key-paper/data-product links. Checked 2026-09-27. These metadata authenticate an anchor; the proposed calculations below are original work orders and are not claims made by its authors.

Source-record SHA-256: `1c29a473db62449cbbec2336644be497df1e78e8aa095d5dae32a389b40360b2` (metadata only; hash acquired payloads separately).

## Core framework and first-principles footing

Use the [core framework contract](../../FRAMEWORK_CONTRACT.md), current [standing](../../../../STANDING.md), and the [amended thirteen-gate specification](../../../../qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md). The amendment overrides historical targets. Pin the same action, physical metric, matter coupling, source/state domain, boundary conditions and parameter cell throughout. Read the pinned source list below before selecting a candidate; this card does not assert that any current candidate is closed.

The scale relation is `a0=(c/2)*sqrt(G_N*rho_Lambda)` with vacuum **mass density** in kg/m³; `kappa=1/2` is adopted unless independently derived. Evaluate dimensional examples separately at canonical `a0=9.3619e-11 m/s²` and alternative `1.1279e-10 m/s²`. Changing a0 with fixed kappa changes rho_Lambda. Keep measured `G_N`, action `G_E` and cosmological coupling distinct: `Lambda_eff=32*pi*(G_E/G_N)*a0²/c⁴`. If V0 denotes SI vacuum energy density, `a0²=G_N*V0/4` and `H_vac²=8*pi*G_E*V0/(3*c²)` under the stated vacuum-background assumptions.

The operative branch is **filtered MONO**, not an interchangeable scalar fit. Let `B=g_bar`, `y=B/a0`, `h_RAR=y*(nu_RAR-1)`, `nu_RAR=1/(1-exp(-sqrt(y)))`; use `h'_mono=max(h'_RAR,0.05*h_p/(y+y_p))`, with the specified continuous join. Rounded landmarks `y_star≈2.3374`, `y_p≈2.5396` are not exact roots. The filter is `S=exp(xi²*Delta/2)`; its adjoint depends on metric, measure and boundary domain. Derive the field/metric observation map before evaluating data. `r>>xi` can justify a controlled approximation, not exact equality with `xi=0`.

Comparison laws `Q: g²=B²+a0*B`, `RAR: g=B*nu_RAR(B/a0)`, and `MU2: [1-(1+g/(2*a0))^-2]*g=B` are distinct; historical EXP is separate. Never silently substitute them for filtered MONO or assume spherical identities hold for arbitrary sources. Use criterion **B** with a consistent preferred foliation and well-posed mixed problem, not an unproved blanket speed requirement. Count gravitational and permitted matter modes separately. No unannounced particle species, per-object force correction or quantum completion. A published GR/LambdaCDM posterior is a conditional derived product until translated.

The thirteen gates cover: static MONO; gravitational modes; both potentials/lensing; PPN; matter conservation; tensor sector; stability/criterion B; expanding cosmology; zero-field limits; Newton/GR and measured G; one physical metric; prescribed RAR/MONO segment; and the a0–vacuum relation. Successful observation-level evidence supplies only its stated edge in this common-action dependency graph.

## Principle and exact mathematical target

Derive the Y6 gravity-statistic leakage using the documented mask and pair weights.

Mathematical starting relation/estimand:

```text
A finite mask and angular binning mix shear modes unless the estimator accounts for boundaries.
```

Define every symbol, units, sign, domain and approximation before use. Treat schematic formulas as obligations to derive, not established framework theorems.

## Measurement inputs and unique new information

Released Y6 angular correlation vectors, redshift distributions, masks, response calibrations and covariance; verify actual data availability.

The Y6 joint measurement supplies a specific multivariate observation test beyond old abstract shear/galaxy likelihood tasks; account for shared Y1/Y3 sky and sources. Unique requested output: Mask-induced E/B leakage of Y6 correlations.

## Ordered execution

1. Authenticate the stated source/version and obtain the exact measured columns, units, selection and covariance needed here. Hash actual inputs. Mark missing products; do not invent measurements or treat a derived posterior as raw data.
2. Derive the Y6 gravity-statistic leakage using the documented mask and pair weights.
3. Derive the displayed statistic or response from the stated framework and measurement map, showing signs, units, parameter degeneracies and approximation bounds. Start with one hand-checkable fixture before evaluating the actual data.
4. Run the specified negative control plus an independent formulation or limiting case. Apply the estimator only where inputs and action-derived response exist; preserve failed controls and sensitivity to source/calibration choices.
5. Return the exact new measurement-conditioned claim and result contract, keeping finite evidence, synthetic checks and universal proofs separate. Propose a distinct evidence-triggered child using the parent branching protocol.

## Falsifiable controls

- Negative control: Treat every measured B component as an extra gravitational polarization.
- Repeat the decisive identity with an independent representation or controlled limit and hold the same measured sample fixed; variations sharing observations are not independent confirmation.

A negative control is deliberately wrong. Show why it should fail in the stated domain. If the actual data cannot distinguish it, report limited identifiability; do not fabricate rejection or declare the correct model false. Predeclare tolerances and preserve failed controls.

## First-principles obligation and closure bridge

Derive the Weyl-potential and matter correlations from one framework action, then the galaxy/shape observation map; no GR-derived S8 posterior is raw data. Exact implication to derive: Derive the Y6 gravity-statistic leakage using the documented mask and pair weights.

Connect mask-induced e/b leakage of y6 correlations to the framework’s common-action source/metric/background or observational gate. Any missing dynamical map stays an open prerequisite; the cited measurement does not derive it.

Separate primitive assumptions, measured calibrations, boundary/initial data, derived consequences and unresolved implications. Any worker may pursue a complete same-action witness through the [closure template](../../CLOSURE_WITNESS_TEMPLATE.md), but independent review of all gates is required. A fit or successful numerical example is not a derivation of the action, coefficient or vacuum scale.

## Required output and completion condition

A source-specific mask-induced e/b leakage of y6 correlations result: equation/estimator, valid domain, calibrated uncertainty or exact missing-data/theory prerequisite, and an explicit implication for the fixed framework. No numerical result is supplied by this work order.

Write the actual result and artifacts under `measurement_decade_2017_2026/results/MY2026-061/<unique-run-id>/`. Use [RESULT_CONTRACT.json](../RESULT_CONTRACT.json), including actual model identity, exact claim, execution/acceptance status, source/data/artifact hashes, equations, controls, tested range, overlap treatment, failed routes and next missing implication. A symbolic proof-only result needs its raw derivation and independent review. An unavailable dataset produces a precise blocked inference, not a synthetic substitute. A record is review-ready only when every field is supplied or explicitly marked not applicable with a reason.

## Reuse, overlap and prerequisites

Declared dependencies: No predeclared seed-ID dependency. Discover and register the exact theory/data dependencies before execution; this does not imply the observation map already exists.

Identify repeated objects, exposures, sky modes and calibration inputs within this source family and across years. Use conditional increments or joint covariance, not a product of overlapping likelihoods. Reuse any old AS result for the generic lemma; this task evaluates the explicitly named new release-specific output.

Before claiming work, search both seed manifests, child registries and live AS/MY/FGF claims/results. Reuse an existing generic theorem or active owner. New title/year alone is not novelty. Shared objects, pixels, events, calibrations or simulations need a joint covariance, conditional increment, or separate alternative analysis; do not multiply dependent evidence.

## Finding-driven continuation

1. **Promising result:** Construct a pure-mode statistic retaining a quantified fraction of gravity information.
2. **Independent bridge:** If that result survives, derive a measurable consequence of the mask-induced e/b leakage of y6 correlations bound in one independently observed channel of this source family. Name the new equation, required independent data and closest existing task before dispatch; reuse an existing owner if its target is already registered.
3. **Failure or obstruction:** If the mask is absent, restrict claims to the released validated estimator.

These are candidate branches, not preapproved scientific conclusions. A child must cite an actual parent result and evidence hashes, name its new equation/estimand, closest existing task, substantive difference, controls, prerequisites and finite resources. Use `MY2026-061.C01` etc. with a unique claim and write scope; descendants remain provisional until reviewed. At most two live children per parent and two levels before orchestrator reconciliation; later reviewed waves may continue. Follow [DISPATCH.md](../DISPATCH.md) and the [first-principles protocol](../../FIRST_PRINCIPLES_AND_BRANCHING.md). If no runner is available, return a ready child specification without claiming it ran.

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
