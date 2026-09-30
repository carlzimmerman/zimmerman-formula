# AMENDMENT 18 — DRAFT, NOT FILED (written 2026-09-30, revision 1; filing needs the owner's explicit go)

This is a draft. `PREREGISTRATION_DR4.md` and every `*_HASH.txt` are untouched. If the owner approves, the text below the line is appended verbatim (append-only) after Amendment 17, with a new `AMENDMENT18_HASH.txt`.

**Why now.** The DR3 dry run (`dr4_ready_1/WP2_GAMMA_SPREAD_FROZEN.md`, question frozen in 01bc48e32, results in 72f9a7ed4, code-path tests only, Amendment 7(e)) rebuilt the primary DR3 base ten times with different seeds for the frozen builder's random draws, at N_SHIFT = 30. Results:
- About 2.6% of the final pairs flip between builds.
- γ̂'s build-to-build SD is 0.30 σ_fit (canonical: 0.0164 against 0.0554) and 0.34 σ_fit (alt).
- The build-only part is 0.24 / 0.32 σ_fit.

The primary DR4 build is deterministic, because its seeds are frozen. But the seed choice carries a noise term that σ_tot = √(σ_fit² + 0.02²) does not include, and its size at DR4's N is not measured.

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

The measured DR3 correlation-cache coverage per build (the uncovered ids) is being checked separately before the 0.30 σ_fit is relied on. The text below fixes all of these.

---

> ### 🚨 AMENDMENT 18 — 2026-09-30, ADDED IN THE OPEN BEFORE DR4. READ BEFORE SCORING.
>
> **THIS AMENDMENT ADDS A REPORTED BUILD-SEED SENSITIVITY TO THE DR4 WIDE-BINARY RESULT. IT CHANGES NO CUT VALUE, THRESHOLD, ESTIMATOR SETTING, σ_tot DEFINITION OR DECISION ROW, AND NOT THE PRIMARY BUILD'S FROZEN SEEDS.**
> **κ = ½ FITTED, NOT DERIVED.**
>
> **What was found.** On DR3 (a code-path test; Amendment 7(e)), rebuilding the primary base with ten seed sets for the builder's random draws (N_SHIFT = 30) gave the following:
> - about 2.6% of the final pairs flip between builds;
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
> **(c) The extra builds.** K = 10 further builds, k = 1 … K (the primary is k = 0), are run on release day. In build k:
> - stage E's shift realisations use r + 1 + 100k in place of r + 1;
> - the stage-E half-mask, the stage-F fold and stage G use SEED + k, with G's seed passed explicitly;
> - the fit uses the primary's registered fit path and seed, so the spread across builds is build-only.
>
> Each build re-runs stages E, F and G on the same stage-A–D inputs. The seeds are changed IN MEMORY: the frozen builder file's hash is checked before and after every build and never edited, as the release-day checklist requires. Each build has its own correlation cache.
>
> A fit-only control is run and reported alongside: the primary catalogue refitted with fit seeds 20261216 + k.
>
> The full seed list, the K actually run, and each build's γ̂, σ_fit, κ and ladder-variant shifts are written into the fetch manifest before the data are opened (the list) and after the runs (the values).
>
> **(d) σ_build, reported only.** σ_build is defined as the SD of γ̂ across the K + 1 builds, on each footing. It is REPORTED ONLY: it does not enter σ_tot and moves no decision edge.
>
> **(e) A seed-sensitivity label.**
> - **The edges:** the decision edges are the operative z-rule edges (each registered target γ ± 2σ_tot and ± 3σ_tot at the primary's realised σ_tot, §1.5) and the hard edges of Amendments 10 (Arm A rows and the 1.23 no-verdict edge), 11(d) as corrected by 12(d) (Arm B kill-from-above 1.084), 13(d) (Arm C rows) and 14(d). All are evaluated at the PRIMARY's σ_tot.
> - **The label:** if the primary γ̂ lies within max(σ_build, 0.3 σ_fit) of any such edge, the verdict is reported with the label **"seed-sensitive"**, stating how many of the K + 1 builds fall on each side.
> - **Stability conditions:** the frozen stability conditions (every ladder variant within 1 σ_fit, κ in [0.95, 1.05], the NSS-off direction) are also evaluated for each build. Any condition that changes its pass/fail status across builds is labelled "seed-sensitive" in the same way.
> - The primary's verdict is the one recorded; labels are added, never substituted.
>
> **(f) Against interest.**
> - The label can caveat a verdict favourable to the framework as well as an unfavourable one.
> - Keeping σ_tot unchanged keeps the frozen thresholds. If σ_build is comparable to σ_fit at DR4's N, the frozen σ_tot understates the total error, and the label is the only protection. That is stated here before the data exist.
> - The extra builds are costly: each re-runs stages E–G (about 880 s per build at DR3 scale, several times that at DR4) and needs its own correlation fetch. If time does not allow K = 10, the number run is recorded, and at least K = 3 are required for the label.
>
> **Untouched:** the estimator; the cut table; the error model and σ_tot; the strictness ladder; the frozen N = 30,000; both a₀ footings; Arms A, B and C; Amendments 10–17's decision rows and cut choices; the primary build's frozen seeds and the pipeline's registered RNG seed. κ = ½ remains fitted.
>
> **Provenance.**
> - `prep_2026/gaia_dr4_prep/AMENDMENT18_DRAFT_NOT_FILED.md`: the draft, revised once after a read-through against the frozen builder and the driver.
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
