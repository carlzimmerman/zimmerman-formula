# AMENDMENT 18 — DRAFT, NOT FILED (written 2026-09-30, revision 3; filing needs the owner's explicit go)

This is a draft. `PREREGISTRATION_DR4.md` and every `*_HASH.txt` are untouched. If the owner approves, the text below the line is appended verbatim (append-only) after Amendment 17, with a new `AMENDMENT18_HASH.txt`.

**Why now.** The DR3 dry run (`dr4_ready_1/WP2_GAMMA_SPREAD_FROZEN.md`, question frozen in 01bc48e32, results in 72f9a7ed4, code-path tests only, Amendment 7(e)) rebuilt the primary DR3 base ten times with different seeds for the frozen builder's random draws, at N_SHIFT = 30. Results:
- About 2.6% of the final pairs flip between builds.
- γ̂'s build-to-build SD is 0.30 σ_fit (canonical: 0.0164 against 0.0554) and 0.34 σ_fit (alt).
- The build-only part is 0.24 / 0.32 σ_fit.

The primary DR4 build is deterministic, because its seeds are frozen. But the seed choice carries a noise term that σ_tot = √(σ_fit² + 0.02²) does not include, and its size at DR4's N is not measured.

**Revision 3 (after the edge table and the label were built from the code, 676cbbec2 / 416530b57, controls L1–L7 7/7, re-run identical by the orchestrator from the committed state; and after the first code reading by an independent referee, CFG239, criteria 8f549fbd8). The corrections:**
- **(e) The chain ceiling is removed from the edge list.** Amendment 14's chain ceiling (1.0725 / 1.0900) is not a constant in the frozen pipeline, so a code-extracted table cannot contain it. The table lists it under "not in code", and the text now says the label does not see it. σ_sys = 0.02 is likewise read from the pre-registration text, not from a code constant.
- **(f) The understatement is corrected to about 2%.** The "roughly 5%" was the figure at DR3's N (σ_fit 0.0557 gives +4.4%). At DR4's expected σ_fit = 0.019 (§1.5), σ_tot = 0.02759 becomes 0.02817 when 0.3 σ_fit is added in quadrature: about +2%.
- **(f) The per-pair seeding sentence now says what it would and would not remove.** It would remove the sensitivity to changes of the pair array, but not the seed-to-seed noise itself.
- **"Flip" is defined:** a one-way count of pairs in the final sample of one build and not of the other.
- **"At least 10" means K_G ≥ 10 further G-only builds,** 11 γ̂ values including the primary.
- **The seed list** now carries the G-only stage-G seeds SEED + k for k = 1 … 100 (416530b57).
- **No extra network for the G-only sweep:** stages A–F are the primary's, so every G-only build has the primary's candidate pairs and correlation ids. Only the K_F full rebuilds need delta fetches.

**Revision 2 (after the DR3 rehearsal of the tooling: design be8a6405d + addenda 1a81a6622 / 6da28b334; tooling 7f1ab9542; stream and N-scaling a51d6f8f2; mechanism 2f2354b18; controls 12/12, including byte identity at k = 0 and σ_build = 0 exactly on identical seeds). The measurements change what the text must say.**
- **The mechanism.** The build-to-build noise comes from the stage-G velocity-error Monte Carlo, which draws one sequential stream over the pair array. ANY change to that array re-rolls every pair's σ(ṽ): even one pair added or removed, or a reordering. About 2.5% of the final pairs then move across the frozen ṽ-error cut.
  - Each seed stream alone reproduces about the whole spread: G-only 0.41 / 0.22 σ_fit, E/F-only 0.42 / 0.40, all streams 0.32 / 0.28.
  - The ratio SD/σ_fit shows no trend with N over a factor of 4 (1,550 to 6,200 pairs).
- **Consequence 1: σ_build is measured by a cheap G-only sweep.** At DR3 scale that costs about 3 s plus a 30 s fit per build, against about 880 s for an E–G rebuild. Full rebuilds are kept as confirmation.
- **Consequence 2: the primary is deterministic only for its exact pair array.** Upstream details the amendments treat as inert can move about 2.5% of the final pairs: a column mapping, one more cut-13 flag, an NSS table.
- **Consequence 3: the edges are defined by the frozen pipeline's own in-force decision constants, not by a hand list.** §1.5's targets include 1.137, which the code marks STALE (Amendment 4(i)).
- The per-build uncovered correlation ids were checked: 2–10 of about 20,450 per build, negligible.

**Revision 1 (after the calculation chat's read-through against the frozen builder, sha256 46452daf…, and dry_run_driver.py; the first draft 3037b034f is in git history).** The first draft's quoted DR3 numbers all matched. Its seed text did not:
- **Stage-E overlap:** "integers 1–10 added to each base seed" would reuse most stage-E per-block shift realisations across builds (116,000 of 132,000 per-block seeds duplicated), understating σ_build.
- **Seed uses:** there are four, not three.
- **G's seed:** the stage-G seed is a default argument bound at import, so it must be passed explicitly.
- **Driver scope:** the driver alone can re-seed only stage G.
- **Outputs:** γ̂ and κ are not driver outputs.
- **Edges:** the list omitted Amendments 10 and 11(d)/12(d).
- **Build count:** K was ambiguous.
- **Manifest:** there was no slot for the seed sets.
- **Patching:** the release-day checklist forbids a diff touching the builder's seeds, so extra builds must patch in memory.

The measured DR3 correlation-cache coverage per build (the uncovered ids) was checked afterwards; see revision 2. The text below fixes all of these.

---

> ### 🚨 AMENDMENT 18 — 2026-09-30, ADDED IN THE OPEN BEFORE DR4. READ BEFORE SCORING.
>
> **THIS AMENDMENT ADDS A REPORTED BUILD-SEED SENSITIVITY TO THE DR4 WIDE-BINARY RESULT. IT CHANGES NO CUT VALUE, THRESHOLD, ESTIMATOR SETTING, σ_tot DEFINITION OR DECISION ROW, AND NOT THE PRIMARY BUILD'S FROZEN SEEDS.**
> **κ = ½ FITTED, NOT DERIVED.**
>
> **What was found.** On DR3 (a code-path test; Amendment 7(e)), rebuilding the primary base with ten seed sets for the builder's random draws (N_SHIFT = 30) gave the following:
> - about 2.6% of the final pairs flip between builds (a flip is a one-way count: a pair in the final sample of one build and not of the other);
> - γ̂'s build-to-build SD is 0.30 σ_fit (canonical) and 0.34 σ_fit (alt);
> - the build-only part is 0.24 / 0.32 σ_fit.
>
> Sources: `prep_2026/gaia_dr4_prep/dr4_ready_1/WP2_GAMMA_SPREAD_FROZEN.md` and `wp2_gamma_spread_full_dr3.*`, 72f9a7ed4.
>
> **(a) The primary is unchanged.** The DR4 primary is build k = 0, the frozen builder with its frozen seeds, fitted by the frozen pipeline exactly as registered.
>
> **(b) The seed uses, stated in full.** The frozen builder (`catalog_builder/build_catalog.py`) draws random numbers in four places, with SEED = 20261202:
> 1. the stage-E shifted realisations, with per-block seeds (r+1)·1000 + block for r = 0 … N_SHIFT−1;
> 2. the stage-E half-mask, default_rng(SEED);
> 3. the stage-F leave-10%-out fold, default_rng(SEED);
> 4. the stage-G velocity-error Monte Carlo, vt_error_mc(seed = SEED).
>
> The pipeline's fit uses its registered RNG seed, 20261216.
>
> **(c) The extra builds.**
> - **σ_build is measured by a G-ONLY sweep of K_G ≥ 50 builds**, k = 1 … K_G, with the primary as k = 0. In build k, stage G's velocity-error Monte Carlo uses SEED + k, passed explicitly. Stages A–F are the primary's. Every build is fitted by the frozen pipeline's own run on its catalogue with the registered fit seed, 20261216, so the spread is build-only.
> - **A confirmation sweep of K_F = 3 to 10 full E–G rebuilds** is also run, with stage-E per-block seeds r + 1 + 100k and SEED + k for the stage-E half-mask, the stage-F fold and stage G. Its SD is reported beside σ_build.
> - **A fit-only control** is also run: the primary catalogue refitted with fit seeds 20261216 + j.
> - **Implementation rules:** the builder's seeds are changed IN MEMORY only, with the frozen builder file's hash checked before and after every build; each build has its own correlation cache.
> - **The seed list:** `dr4_ready_1/seed_sets_dr4.json`, a pure function of this rule (the full-rebuild sets for k = 0 … 10 and the G-only stage-G seeds SEED + k for k = 1 … 100), is committed before DR4 is released.
> - **Recorded per build:** γ̂, σ_fit, κ and the implemented ladder-rung shifts (R_chance < 0.001; separation 3–20 kAU; RUWE < 1.2 on both components), written to a sweep manifest. Ladder rungs that cannot be implemented on release day are listed as NOT IMPLEMENTED; nothing is substituted.
>
> **(d) σ_build, reported only.** σ_build is the SD (ddof = 1) of γ̂ across the K_G + 1 G-only builds, on each footing. It is REPORTED ONLY: it does not enter σ_tot and moves no decision edge.
>
> **(e) A seed-sensitivity label.**
> - **The decision edges are the in-force decision constants of the frozen `wide_binary_pipeline.py` at release.** That means the named γ̂ edges and anchors, excluding any the code marks STALE: Arm A's band, Arm B's value, A falsified below, B killed at or above, the no-verdict edge and the MOND benchmark. Add the κ window and the §1.5 z-rule's ±2σ_tot and ±3σ_tot around each in-force target at the primary's σ_tot. Quantities that are not constants in the frozen code (Amendment 14's chain ceiling; σ_sys = 0.02, which is read from this document) are listed in the table as "not in code", and the label does not test them.
> - **The edge table:** these are extracted by code into a machine-readable edge table, committed before DR4. That table, not this text, is the operative list.
> - **The label:** if the primary γ̂ lies within max(σ_build, 0.3 σ_fit) of any edge, the verdict is reported with the label **"seed-sensitive"**, stating how many builds fall on each side of that edge.
> - **Stability conditions:** the frozen stability conditions (every implemented ladder rung within 1 σ_fit, κ in its window) are evaluated for each build. Any condition that changes its pass/fail status across builds is labelled the same way.
> - The primary's verdict is the one recorded; labels are added, never substituted.
>
> **(f) Against interest.**
> - The label can caveat a verdict favourable to the framework as well as an unfavourable one.
> - Keeping σ_tot unchanged keeps the frozen thresholds. If σ_build ≈ 0.3 σ_fit at DR4's N, as the DR3 N-scaling suggests (a constant ratio, with no extrapolation claimed), σ_tot understates the total error by about 2% at DR4's expected σ_fit = 0.019 (about 4% at DR3's N). The label is the only protection. That is stated here before the data exist.
> - The primary is sensitive to any change of stage G's pair array, including ones the other amendments treat as inert. This amendment measures that sensitivity; it does not remove it.
> - Per-pair seeding of the Monte Carlo would remove the sensitivity to changes of the pair array, but not the seed-to-seed noise itself. It would also change the frozen builder, so it is not adopted.
> - If time does not allow K_G ≥ 50 G-only builds, the number run is recorded. The label requires K_G ≥ 10 further builds (11 γ̂ including the primary); below that it reads "NOT APPLICABLE (K < 10)".
>
> **Untouched:** the estimator; the cut table; the error model and σ_tot; the strictness ladder; the frozen N = 30,000; both a₀ footings; Arms A, B and C; Amendments 10–17's decision rows and cut choices; the primary build's frozen seeds and the pipeline's registered RNG seed. κ = ½ remains fitted.
>
> **Provenance.**
> - `prep_2026/gaia_dr4_prep/AMENDMENT18_DRAFT_NOT_FILED.md`: the draft, revised three times: after a read-through against the frozen builder and the driver; after the DR3 rehearsal of the tooling (a51d6f8f2, 2f2354b18); and after the code-extracted edge table (676cbbec2).
> - `dr4_ready_1/seed_sets_dr4.json` (416530b57), and the edge table `dr4_ready_1/edge_table_dr4.json` with `seed_label.py` (676cbbec2).
> - `dr4_ready_1/WP2_GAMMA_SPREAD_FROZEN.md` and `wp2_gamma_spread_full_dr3.*` (72f9a7ed4).

---

**Implementation note (not part of the amendment text).** The implementation is being built as new code only:
- a per-k E/F rebuild that patches the builder in memory, with its hash asserted before and after;
- the driver's stage G on each per-k directory, with an explicit G seed;
- per-build γ̂ and κ through the real pipeline's fit path;
- a sweep manifest;
- a MUTATE in which identical seeds must give σ_build = 0 exactly;
- a check that k = 0 reproduces the current driver outputs byte for byte.

Also pending: the per-build uncovered-correlation count for the DR3 sweep, and a frozen σ_build-versus-N question on subsamples of the ten DR3 builds.
