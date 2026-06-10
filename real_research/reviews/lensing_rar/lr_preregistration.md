# Lensing-RAR hostile audit — PRE-REGISTRATION (LR-0, locked before any data)

**Committed BEFORE fetching any data — the pre-commitment is the discipline.** *C. Zimmerman, 2026-06-10. This audit
attacks the framework's **strongest standing exposure**, not a favorable target: the weak-lensing RAR's early/late-type
split (Brouwer et al. 2021, A&A 650 A113, KiDS-1000+GAMA+BOSS), reported at ~6σ — a split that property-independent
modified gravity (MOND / this framework, where the force law is universal and type-blind) **cannot produce**, while cold
dark matter can. The same pre-registration + retraction-guard + both-ways discipline that just closed the wide binaries
applies here, with ONE inversion (below). Inline execution, no swarms. C1/C2 only (says nothing about a₀(z); C3 fence).*

## Target claims (what we are auditing — stated as the published authors state them)
- **(a)** The galaxy-galaxy weak-lensing RAR extends the McGaugh/SPARC relation **~2 decades below** SPARC accelerations
  (down to g_bar ~ 10⁻¹⁵ m/s²), via the Excess Surface Density (ESD) profile of ~10⁶ isolated lenses.
- **(b)** **Early-type and late-type galaxies follow DIFFERENT RARs at fixed g_bar, at ~6σ.** This is the exposure: a
  universal force law predicts ONE RAR independent of morphology; a ~6σ type-split, if robust, is **⛔ framework-impossible**.

## Pre-registered outcomes (decided now, before the data)
- **(A) — the split replicates robustly AND survives the systematics battery → the standing falsifier HARDENS.** The ledger
  records it with magnitude (σ, dex offset between the two RARs); the manuscript's exposure section is rewritten to LEAD with
  it. *This is the framework-unfavorable outcome and it is on the table at full weight.* **LOCKED WORDING (enrichment):** A must
  read "hardens the exposure **AGAINST property-independent modified gravity**" and may **NOT** read "ΛCDM confirmed" — Brouwer's
  own simulations (MICE vs BAHAMAS) **disagree with each other** about the split, so no single dark-matter model is validated by it;
  the split is an exposure to the *framework's* type-blind force law, not a vindication of a specific DM model.
- **(B) — the split's significance is ABSORBED by one or more systematics → exposure downgraded to systematics-limited, with
  the dominant term named and quantified.** The candidate systematics (each tested as its own axis, §Battery):
  1. **Stellar M/L by morphology** — early types host older populations → higher M/L; a type-dependent M/L offset moves g_bar.
  2. **Hot-gas / missing-baryon budget in early types** — *this is the PUBLISHED MOND-side response.* Our job is to **QUANTIFY
     whether a plausible hot-gas/CGM baryon budget closes 6σ — NOT to assert it.** Early-type X-ray/CGM baryons not in the
     stellar+cold-gas g_bar would shift early types rightward onto the late-type relation. **Enrichment (protective):** Brouwer
     themselves call the missing-baryon uncertainty "the single most severe limitation of our analysis" — so if outcome B obtains,
     it is documented as **the paper's own named limitation**, not our invention. (And it is now testable against post-2021 eROSITA.)
  3. **Satellite-fraction contamination** — the isolated-lens selection admits a type-dependent satellite fraction; satellites'
     ESD carries the host halo → biases g_obs differently for the two populations.
  4. **ESD → g_obs conversion** — the deprojection assumes sphericity / a specific density-profile form; quantify the
     systematic from ellipticity and profile freedom, do not hand-wave it.
- **(C) — partial survival → record the quantified residual σ** after the dominant systematic is applied (e.g. "6σ → 2.4σ,
  hot-gas-budget-limited").

## Hostility requirement (THE INVERSION — read twice)
The wide binaries were a *favorable* target, so there the adversarial pass tried to KILL framework-favorable findings. **Here
the exposure (outcome A) is framework-UNFAVORABLE, so the adversarial mandate INVERTS:** the verifier's named job is to try to
**CONFIRM the split as robustly as possible** and to **attack every systematic we propose as absorbing it** (is the hot-gas
budget physically plausible at the mass scale? does the M/L offset have the right sign and size? is the satellite fraction
really type-dependent enough?). **A framework-favorable downgrade (outcome B or C) SHIPS ONLY IF it survives that hostile
pass.** Equivalently: we make ourselves argue the falsifier's case first, and only concede the escape if the escape is
forced by the data. If we cannot honestly break the split, outcome A stands and we lead with it.

## Data plan (provenance-pinned; replication fidelity FIRST)
- **Primary:** Brouwer et al. 2021 released data products + **KiDS-1000** public weak-lensing catalogs (DOI-pinned on fetch) +
  **GAMA** spectroscopy for lens properties (stellar mass, Sérsic/morphology, environment). Their lens selection, their stellar-mass
  pipeline, their early/late classifier, their ESD stacking, their ESD→g_obs conversion — **transcribed first into
  `lr_published_pipeline.md` with TRANSCRIPTION-GAPs logged**, deviations logged thereafter.
- **Cross-check only (if primary gates):** DES Y3. Not used unless the KiDS-1000 replication passes the gate.
- **Replication gate:** our reproduced split significance must land **within a factor ~1.5 of the published ~6σ** before any
  stress-testing; else waterfall-diff the divergence (as in WB-R1) until the divergent step is identified.

## Pre-registered stop-and-report triggers
- Replication gate fails after **two waterfall cycles** → halt, report the divergence (catalog-version or pipeline difference).
- **Any single systematic moves the split by >3σ** → halt and relay BEFORE proceeding — that is a field-level finding either
  direction (it would mean the published 6σ is one-systematic-fragile, which cuts against everyone, or that the split is rock-solid).
- A required cut/quantity is not reproducible from the public products → log as a catalog/data-availability gap, do not fudge.

## Footing & fences
- **a₀ enters only as the RAR's low-acceleration scale; rerun the split test at a₀=1.2×10⁻¹⁰ as well as 9.36×10⁻¹¹ and state the
  insensitivity** (as in the WB methodology note §8). The split is about *type-dependence at fixed g_bar*, which is a₀-independent.
- Both-ways summary mandatory on every stage. Retraction guard on every commit. C1/C2 only; **no a₀(z) claim** (C3 fence).
- **Nothing is fetched before this file is committed.** LR-1 (execution) is bound by this document.
