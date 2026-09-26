# dark matter particle crispy ideas

10 proposed calculations, 2026-09-26. **No calculations or simulations in this list have been executed.**

**Review status:** Explicit particle-model extensions, added under the user's time/credit constraint. Particle dark matter already has substantial prior work in this repository; these cards connect particle calculations to the current reciprocal carrier construction and must not be presented as first-ever ideas.

**Goal:** Develop and test a declared particle interpretation of dark matter using the existing carrier interaction, rather than assigning arbitrary kicks.

**Framework:** filtered `nu_mono` and preferred-time causality criterion B remain the canonical target. Exact exponential RAR and AQUAL are separate comparisons. CA5 retains its actual gate and known exact-target mismatch. Freeze one action, metric, source prescription and parameter set per result; do not combine another model's successful tests into a common-action claim.

**Particle assumptions:** these are explicitly new particle/quasiparticle branches, as requested. State the quantization, particle content, initial abundance, thermal history and validity of a dilute kinetic approximation. The existing five real classical fields do not by themselves establish those assumptions. Start with the existing diagonal U(1) and positive-square interaction; any new species or portal is a separately named extension.

**Agent handoff:** claim one ID and write under `real_research/fresh_crispy_astra/<ID>/`. Preserve assumptions, source hashes, code/derivation, run commands and a bounded `RESULT.md`. A scoped failure or nonidentifiability result is useful closure. Numerical agreement is not a universal theorem. These files are a work order, not authorization to launch every expensive run.

**Sources:** [snapshot and novelty record](docs/superpowers/plans/2026-09-26-fresh-crispy-ideas.novelty.json); [machine-readable queue](docs/superpowers/plans/2026-09-26-fresh-crispy-ideas.tasks.json). Some required derivations are local-only. Resolve the pinned source bytes before execution; the snapshot records which sources are absent or different on the publication base.

**Related lists:** [first 40](ASTRA_CRISPY_IDEAS.md) · [fresh 20](FRESH_AND_CRISPY_ASTRA_IDEAS.md) · [inverse 10](BOLD_INVERSE_CRISPY_ASTRA_IDEAS.md) · [particle 10](DARK_MATTER_PARTICLE_CRISPY_IDEAS.md).

## D01 — Derive the particle Hamiltonian from the reciprocal field action

**Calculate:** Explicitly adopt a particle/quasiparticle branch. On a slowly varying positive-t background, derive the massive poles, WKB worldline Hamiltonian, physical energy, conserved charge and auxiliary source from the carrier action.

**Prediction / decisive test:** Predict the environment-dependent dispersion and force, and identify the adiabatic/coherence regime where a particle ensemble is valid. Do not import ordinary geodesic dark matter automatically.

**Start from:** `perspective`, `ca5`.

## D02 — Replace a fitted kick by the action's two-body decay

**Calculate:** At t=1 first, quantize the positive-square interaction and derive H->L+s matrix element, decay width, exact two-daughter momenta and charge/energy balance. Require the actual threshold m_H>m_L+mu.

**Prediction / decisive test:** Predict both daughter velocity distributions from masses and coupling. If the channel is forbidden, the phenomenological kick cannot represent this vacuum decay.

**Start from:** `conversion`, `twomode`.

## D03 — Infer masses from an escape-fraction curve

**Calculate:** Use D02's daughter spectrum to predict retention versus independently specified halo escape speed. Invert that curve jointly for mass ratios and decay timescale, allowing assembly uncertainty.

**Prediction / decisive test:** Predict retention in an unused mass bin and the neutral-daughter energy fraction. Report degeneracies rather than fitting each halo its own kick.

**Start from:** `retention`, `inner`, `conversion`. **Needs:** D02.

## D04 — Calculate inverse decays and the failure of one-way clearing

**Calculate:** Derive H<->L+s collision terms from the same amplitude, including Bose factors when occupations require them. Solve one homogeneous expanding cell and one declared halo phase-space distribution.

**Prediction / decisive test:** Predict the density/temperature regime where reverse conversion stalls clearing and the equilibrium fractions. Detailed balance cannot be replaced by a permanent one-way label.

**Start from:** `conversion`, `pm`. **Needs:** D02.

## D05 — Use escaping daughters as a dark-radiation calorimeter

**Calculate:** Combine the full recoil budget with an explicit cosmological decay history. Integrate daughter energy density, equation of state and anisotropic stress, keeping massive and relativistic stages distinct.

**Prediction / decisive test:** Predict the expansion/free-streaming contribution associated with a given amount of halo clearing. Compare with primary observational likelihoods only after deriving the transfer.

**Start from:** `conversion`, `frw`, `retention`. **Needs:** D02.

## D06 — Link a decay rate to compulsory self-scattering

**Calculate:** Using the same cubic and quartic couplings, calculate the leading charge-preserving elastic amplitudes and transport cross sections in a declared perturbative regime, including interference and exchange symmetry.

**Prediction / decisive test:** Predict velocity-dependent scattering once a decay rate is chosen. State where Born or dilute-gas assumptions fail instead of assigning an independent self-interaction cross section.

**Start from:** `conversion`, `perspective`. **Needs:** D02.

## D07 — Derive the kinetic-decoupling cutoff

**Calculate:** For an explicitly chosen thermal initial-state branch, solve momentum-exchange rates from D06 against expansion, retaining the reciprocal dispersion. Compute the resulting damping/free-streaming scale through decoupling.

**Prediction / decisive test:** Predict a smallest-structure scale correlated with conversion parameters. The initial temperature and abundance are inputs unless a production mechanism is separately derived.

**Start from:** `frw`, `conversion`. **Needs:** D06.

## D08 — Bound the residual charged relic after heavy-particle decay

**Calculate:** Use the exact diagonal U(1) charge to derive a lower-energy/number bound on the surviving charged daughter population, with particle-antiparticle asymmetry specified. Propagate it through expansion and halo escape.

**Prediction / decisive test:** Predict the minimum surviving charged component and its cold/hot split in the declared branch. Escaping a halo does not erase cosmic charge or establish the observed abundance.

**Start from:** `conversion`, `frw`.

## D09 — Map where a dilute particle description fails

**Calculate:** For allowed particle masses and halo phase-space densities, compute occupation, de Broglie scales and collision times using the derived local dispersion. Compare them with xi, halo gradients and observation times.

**Prediction / decisive test:** Predict where a dilute-particle calculation must be replaced by a coherent-field or degenerate kinetic treatment, and an associated resolvable scale. Bosons have no fermionic phase-space ceiling.

**Start from:** `perspective`, `conversion`, `zero`.

## D10 — Derive an environment-dependent decay clock

**Calculate:** Canonically normalize the interacting fields at locally constant t, derive the physical decay-width scaling, then restore slowly varying t from the actual constraint solution. Retain gradient/nonadiabatic corrections.

**Prediction / decisive test:** Predict a correlation between carrier lifetime and auxiliary/lensing environment instead of postulating a density threshold. Compare with D02 at t=1; do not promote t->1/t symmetry of F to a symmetry of the full action.

**Start from:** `ca5`, `perspective`, `conversion`. **Needs:** D01, D02.

## First assignments

Start with **D01 → D02 → D04/D06**. Establish the actual particle Hamiltonian and decay process before relic or halo forecasts. Existing phenomenological two-body decay, kick and flux-power calculations are controls, not evidence that the present field action already realizes their parameters. Vacuum normalization and the observed dark-matter abundance remain inputs until derived.

## Source map

- `ca5`: `real_research/breakthrough_review_2026_09_26/vacuum/ACTION.md`
- `conversion`: `real_research/common_action_2026_09_26/transport/CONVERSION.md`
- `frw`: `real_research/common_action_2026_09_26/transport/HOMOGENEOUS_FRW.md`
- `inner`: `real_research/dark_sector_2026/L376_triggered_carrier_inner_galaxies.py`
- `perspective`: `real_research/common_action_2026_09_26/action/PERSPECTIVE_VARIANT.md`
- `pm`: `real_research/dark_sector_2026/L377_full_construction_pm.py`
- `retention`: `real_research/dark_sector_2026/L375_triggered_carrier_galaxy_retention.py`
- `twomode`: `real_research/merger_infall_2026/L373_two_mode_carrier_pm.py`
- `zero`: `real_research/closure_push_2026_09_26/filtered_zero_field/RESULT.md`
