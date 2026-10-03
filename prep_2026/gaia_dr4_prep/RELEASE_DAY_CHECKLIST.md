# Gaia DR4 release-day checklist (implements Amendment 15 exactly)

Written 2026-09-28. DR4 is scheduled for **2 December 2026**. This file is procedure only. It changes no
frozen text: `PREREGISTRATION_DR4.md`, every `AMENDMENT*_HASH.txt` and the drafts are untouched.
Sources for every statement: `PREREGISTRATION_DR4.md` §1.2 and Amendments 14–15, `catalog_builder/`
(`fetch_extract.py`, `build_catalog.py`, `README.md`) and `wide_binary_pipeline.py`, all read on 2026-09-28.

## 0. Read first: gaps between Amendment 15 and the code as it stands

These are properties of the repo today, not release-day surprises. Items A and B need the owner's decision
**before 2 December**, and any fix is an appended amendment, never an edit.

**A. Cut 9 (A_V): the filed text and the code disagree.** Amendment 15(a) says cut 9 reads the DR4 `ap_*`
extinction table. The frozen cut 9 (§1.2) names no map ("A_V < 0.5, Banik+24 §2.4.1"), and the code
implements it as **SFD98**, `A_V = 3.1 E(B−V)` from the dust maps in `real_research/data/dustmaps/sfd/`
(`build_catalog.py` `av_sfd98`; `catalog_builder/README.md` "A_V (SFD98)"). The `ap_*` clause was added at
filing from ESA's page and was not checked against the implemented route. Until resolved, running the code
as written does not follow Amendment 15(a) for cut 9, and switching the code to `ap_*` would change the
implemented cut. Options for the owner: (1) an Amendment 16 stating that cut 9 is SFD98 as implemented, with
`ap_*` extinction as a reported variant only; or (2) implement `ap_*` as primary and report SFD98 as the
variant. Either way, decide and record it before release. Do not decide on release day after seeing data.

**B. Cut 13 (triple search): the code searches the wrong catalogue for Amendment 15, and its criterion
differs in form from the frozen text.**
- Amendment 15(a): the search runs against the full `all_source_astrometry` (about 2.8 billion sources).
  `build_catalog.py` `third_star_flags` searches the gaia_source extract (`parallax > 3.5`, `parallax_over_error
  > 5`, `parallax_error < 2`, non-null G, |b| > 10). No all-source query, join or G < 20 lookup from
  `all_source_photometry` exists yet.
- Frozen §1.2 text: parallax within 3σ and proper motion "within 5 sigma of the pair". The code tests
  `dpar < 3` and `dmu < orb + 2·sdmu` (an orbit-aware bound, El-Badry style). I did not check whether an
  earlier amendment declares this form; if none does, that is a second mismatch to resolve the same way.
- The README already notes the extract floor can hide a faint third star near 250 pc; the full-catalogue
  search removes that limitation only once it is built.

**C. Variant (c) (the `all_source_*` base) is not implemented.** The builder has no base-table switch.
Variant (c) means the whole chain (crowding counts, pair search, chance-alignment KDE, Σ₁₈ map, cuts) on the
all-source base, not just a different column source. It needs its own extract, manifest and output CSV.

**D. No join code exists for the primary base either.** `fetch_extract.py` selects every column, including
`ruwe`, `ipd_frac_multi_peak`, `radial_velocity`, `radial_velocity_error` and `non_single_star`, from one
table (`gaia{release}.gaia_source`). If DR4 `gaia_source` lacks any of them, they must come from
`all_source_*` on `source_id`. No such code path has ever run.

**E. Cut 12 needs the `nss_*` tables; the code reads a single `non_single_star` integer.** ESA lists ten
`nss_*` tables (`nss_multiplicity` alone has 229,083,823 rows). Amendment 15(b) rejects a pair if either
component appears in any NSS table carrying an astrometric orbit, an acceleration solution or a spectroscopic
orbit. Whether a table such as `nss_multiplicity` counts is a judgement about its content; read the data
model, record the decision and the row counts, and do not tune it after seeing the sample size.

## 1. Ordered release-day list

Every step that touches data is logged in the manifest (section 2). Nothing below changes a cut value,
threshold, estimator setting or decision row.

1. **Before opening the archive.** Record UTC time. Confirm the working tree equals the freeze:
   `git status --short prep_2026/gaia_dr4_prep` clean, and run the diff check in section 3.
2. **Read the published DR4 data model.** Save the page or export used (URL, retrieval time, sha256).
   Write down, for cuts 1–15, the table and column that carries each quantity (section 1.3 below). Names only.
3. **Pull the primary base.** `gaiadr4.gaia_source` with the frozen extract WHERE clause (floors and
   latitude unchanged). Where a needed quantity is not in `gaia_source`, join `source_id` to the
   `all_source_*` table that carries it. Record row counts before and after every join. A join that
   drops rows is a finding, not something to repair.
4. **Cut 9.** Follow the owner's decision on item A. Record which route ran.
5. **Cut 12.** Union of `source_id`s across the NSS tables selected under Amendment 15(b), matched to both
   components of each pair. Record each table, its solution type and its row count. The strictness-ladder
   run with the NSS screen off is unchanged.
6. **Cut 13.** Follow the owner's decision on item B: search the full `all_source_astrometry` with G from
   `all_source_photometry`, at the frozen radius (30 kAU projected). Record the criterion actually run.
7. **Cut 11.** RV columns from `all_source_rvs` (312,247,580 rows per ESA) unless `gaia_source` carries them.
8. **Run the frozen chain** (`build_catalog.py --release dr4`, then the `scaled_clean` variant, then
   `wide_binary_pipeline.py --catalog …`), unchanged apart from names.
9. **Variant (c).** Only if item C was resolved before release; otherwise state that it was not run and why.
10. **Report.** The `[7(e)]` lines only. No verdict word (Amendment 7(e)). Report σ_fit, both footings, the
    κ window check, the distance to the chain ceilings 1.0725 / 1.0900 (Amendment 14), and the primary-vs-
    variant difference against σ_fit if variant (c) ran (Amendment 15(e)).

### 1.3 Which table each frozen cut reads (Amendment 15 mapping)

| cut | quantity | Amendment 15 source | what the code reads today | status |
|---|---|---|---|---|
| 1 | \|b\| > 15 | position from `gaia_source` (b computed from ra, dec) | `ra`, `dec` | ok if columns exist |
| 2 | G < 17 both | `gaia_source`, else `all_source_photometry` | `phot_g_mean_mag` | name check |
| 3 | d < 250 pc (ϖ > 4 mas) | `gaia_source`, else `all_source_astrometry` | `parallax` | name check |
| 4 | ϖ/σ_ϖ ≥ 40 | same | `parallax`, `parallax_error` | name check |
| 5 | parallax consistency | same | same | name check |
| 6 | 2 < s < 30 kAU | same | ra, dec, parallax | name check |
| 7 | RUWE < 1.4 | `gaia_source`, else `all_source_astrometry` or `all_source_flags` | `ruwe` | join may be needed (D) |
| 8 | ipd_frac_multi_peak ≤ 2 | `gaia_source`, else `all_source_flags` | `ipd_frac_multi_peak` | join may be needed (D) |
| 9 | A_V < 0.5 | `ap_*` per the filed text; **SFD98 in the code** | SFD98 dust map | **conflict (A)** |
| 10 | total mass window | from G and parallax (Banik+24 eq. 6) | `phot_g_mean_mag`, `parallax` | name check |
| 11 | RV consistency | `gaia_source`, else `all_source_rvs` | `radial_velocity(_error)` | join may be needed (D) |
| 12 | NSS screen | `nss_*` tables | `non_single_star` int | **not implemented (E)** |
| 13 | resolved-triple search | full `all_source_astrometry` (+ G < 20 from photometry) | gaia_source extract | **not implemented (B)** |
| 14 | R_chance < 0.01 | computed from the base sample | stages E–F on the extract | follows the base |
| 15 | σ(ṽ) error cut | astrometry and covariance columns | `pmra/pmdec` errors, `pmra_pmdec_corr` | name check |
| 16 | no catalogue-level ṽ cap | none | none | ok |

## 2. Manifest fields to record

One JSON record per fetch, appended to `catalog_builder/manifest_dr4.json` (the file `fetch_extract.py`
already writes; do not overwrite an earlier record). For every fetch and every join:
- `utc_start`, `utc_end`, `host`, `git_commit` of the working tree, and the sha256 of
  `wide_binary_pipeline.py`, `build_catalog.py` and `fetch_extract.py` at run time (compare with section 3).
- `table` (full archive name), `columns` (exact names as published), `where` (verbatim), `query` (verbatim),
  `rows`, `sha256` of the output file, `seconds`, archive job id.
- For each join: left and right table, key, rows in, rows out, rows dropped.
- For cut 9: route (`SFD98` or `ap_*`), and for `ap_*` the table and column; for SFD98 the map file sha256.
- For cut 12: every NSS table used, its solution type, its row count, and the reason any `nss_*` table was
  excluded.
- For cut 13: catalogue searched, criterion applied verbatim, and the count of pairs it removed.
- The data-model page or export used (URL, retrieval time, sha256).

### UNIMPLEMENTABLE-cut procedure (Amendment 15(d))
If DR4 lacks a quantity a frozen cut needs, or the quantity cannot be joined:
1. Write `UNIMPLEMENTABLE: cut N (<name>): <quantity> absent from <tables searched>` in the manifest and in
   the report's first line.
2. Run the chain **without** that cut. Flag every downstream number as "cut N not applied".
3. Choose **no substitute quantity** and no proxy after the data exist. (The README's DR3 `non_single_star`
   "sparse proxy" is not a substitute for cut 12 on DR4.)
4. Report how many pairs the missing cut would have been expected to remove only if that is knowable from
   pre-release information; otherwise say it is unknown.

## 3. Check that the pipeline changes names only

Reference hashes on 2026-09-28 (working tree equals HEAD for these files):

| file | sha256 | last commit |
|---|---|---|
| `wide_binary_pipeline.py` | `7c884e0e0a4cb9cb5d6280d558cf64c829974ed14143a90261bd6a6fbf3007c9` | 2a18b570e8 |
| `catalog_builder/build_catalog.py` | `46452daf1f2e2521b6e5a892a7a234e6ad063f2fd4f1c7392664f63f99a507ad` | 4f3c1b385b |
| `catalog_builder/fetch_extract.py` | `d826f688e140ebf5f948f518bb2bc0efd754cfb2d0519feada4044861040b46f` | 4f3c1b385b |
| `catalog_builder/validate_dr3.py` | `69280396596de09251f4edea948af20b27ed4770461eebfcaa23020747ec2a16` | 4f3c1b385b |

Procedure:
1. `sha256sum` the four files. `wide_binary_pipeline.py` must match exactly (it holds `FROZEN_DR4_CUTS`, the
   estimator and the error model). A mismatch means stop and find out why.
2. For `build_catalog.py` and `fetch_extract.py`, run `git diff 4f3c1b385b -- <file>` after the release-day
   edits. Every changed line must be a table name, column name or a join. Reject any diff touching a numeric
   literal in `frozen_cuts` (1.4, 2, 40, 250, 17, 0.464, 4.31, 0.01, the 2000 and 30000 AU limits), `WHERE`'s
   floors (`parallax > 3.5`, `parallax_over_error > 5`, `parallax_error < 2`, `ABS(b) > 10`), the estimator
   grid, `boot`, the seed, or the cap.
3. Confirm the cut list in the run's output still has the same 15 named cuts, in the same order, and record
   the cut-flow counts.
4. Diff the numeric constants: extract every float and int literal from `frozen_cuts` before and after and
   compare as sets.

## 4. What to verify on DR3 first (and what has NOT been tested)

Already validated end to end on DR3 (`catalog_builder/README.md`, `validation_dr3*.json`): 4,582,547 sources
→ 6,210 pairs after every frozen cut; recovery of El-Badry's pairs 99.40%, purity 98.76%, R < 0.01 decision
agreement 98.93%. Every DR3 γ̂ there is contaminated, NON-SCORING, and evidence for nothing.

**Not tested, and not testable by simply re-running that chain:**
1. **Any join.** DR3 `gaia_source` carries every column the code reads, so the `source_id` join path (D) has
   never executed. A DR3 join test is possible in principle if DR3 exposes some of these quantities in
   separate tables (my recollection is that DR3 has a separate RUWE table and separate NSS tables; verify the
   archive schema before relying on it): build the extract through the join and require the sample to be
   identical to the single-table sample for every column both routes provide.
2. **The `nss_*` union** (cut 12): DR3's single flag is a sparse proxy. A DR3 test of the union route would
   need DR3's NSS tables.
3. **The full-catalogue triple search** (cut 13) and **variant (c)**: neither exists in code.
4. **The curated-subset-plus-`all_source_*` sample as a whole.** The DR3 run is a single-table sample. No test
   has established that a curated `gaia_source` base joined to `all_source_*` yields the same pairs as the
   single-table logic, or how many it drops (that is exactly what variant (c) measures on DR4).
5. **`ap_*` extinction (A):** never read by any code.

Before release, run on DR3: the section 3 hash check, the full chain once to confirm the reference numbers
above are still reproduced byte for byte, and a dry run of any new join code on a small DR3 chunk with an
assertion that the joined sample equals the single-table sample.

## 5. Do not

- Edit `PREREGISTRATION_DR4.md`, an `AMENDMENT*_HASH.txt` or a draft. New amendments are append-only and need
  the owner's go.
- Change any cut value, floor, estimator setting or decision row; choose a substitute quantity; or pick the
  primary versus the variant after seeing the result.
- Emit a verdict word. Report raw γ̂, σ_fit, both footings and the distances to the registered numbers.
- Treat κ = ½ as derived. It is fitted.

## 6. STATUS MAP (appended 2026-10-01 at the orchestrator's request; sections 0 to 5 above stand unchanged and describe the repo as of 2026-09-28)

Sources: `git log`, `dr4_ready_1/PLAN.md`, the tests named below. Nothing here changes a frozen text, a cut, a threshold or the registered analysis. DR3 numbers are code-path tests, never results (Amendment 7(e)).

### 6.1 What changed since section 0 was written
- **Amendments 15 to 18 are FILED:** 15 (the cut list mapped onto DR4's tables; 9f60163d3, 09-28), 16 (cut 9 = SFD98 primary with `ap_*` a reported variant; cut 13 literal primary with the orbit-aware bound a reported variant, searched in the full `all_source_astrometry` with G from `all_source_photometry`; the optional crowded-field / environment tables a release-day decision; 304affce5, 09-29), 17 (cut 12 against the draft data model's `nss_*` tables, with variants V17a / V17b; ab9557d58, 09-29), 18 (a reported build-seed sensitivity sigma_build and a 'seed-sensitive' label; 1f7b9bcfb, 09-30).
- **The code that sections 0 and 4 said was missing now exists and has run on DR3** (new files only; the frozen builder `build_catalog.py` 46452daf… and `wide_binary_pipeline.py` 7c884e0e… are untouched): the cut-13 all-source search, the cut-12 union, the join code, variant (c), a driver that runs the frozen stage G with those pieces, the cones-based cut 13 on fetched neighbour cones, the seed sweep and the label.
- **Two DR3 neighbour-cone fetches were run under the owner's go** (all 6,210 final pairs, 3,122 queries, 135 MB; the 4,021 candidates that are not final pairs, 2,193 queries, 93 MB) and the all-source cut 13 was run on all 10,231 DR3 candidates through the driver (`cones_all_candidates_dr3.py`, 3a4ce6e2a).
- **Release-day tooling for DR4 was written offline on 2026-10-01** (design `dr4_ready_1/DR4_Q1_TOOLING_DESIGN_FROZEN.md`, 6742d206d): the DR4 variant of the cone fetch, the pre-brief estimator, the optional-table fetch, a sync fallback for stage G's correlation fetch and the `--neighbours-manifest` switch. All of it is tested against a MOCK archive only; **no DR4 query form has ever run**, and every one needs the owner's go on the day.

### 6.2 Section 0, gaps A to E, now
| gap | state | where / evidence | still open on the day |
|---|---|---|---|
| A cut 9 conflict | RESOLVED by Amendment 16(a): SFD98 primary, `ap_*` a reported variant only | `AMENDMENT16_HASH.txt` | for the variant, name its table and column in the manifest (the draft: `ap_xp.ag_gspphot`, `ebpminrp_gspphot`, or the consolidated `gaia_source.ag` with `extinction_origin`); no code has ever read `ap_*` |
| B cut 13 | RESOLVED in text by Amendment 16(b); IMPLEMENTED (WP1) | `cut13_allsource.py` (77371136e), `cones_cut13.py` (43773f280), driver `--cut13 cones-literal / cones-orbit`; tests `test_cones_cut13.py` (6/6 + MUTATE), `test_wp1_wp4_offline.py`; DR3 end to end on all 10,231 candidates | the real DR4 query form, the DR4 names, the `source_id` to HEALPix-pixel assumption (checked offline at plan time against the base extract, optionally online by `--spot-check`), the optional tables |
| C variant (c) | IMPLEMENTED (WP2) as a DR3 dry run and the driver's `--variant allsource_15c` | `wp2_variant_full_dr3.py` (957b9d91e), `PLAN.md` | the DR3 version is a stand-in; the real test (curated base against all-source base) exists only on DR4 |
| D joins | IMPLEMENTED (WP3), manifest-driven, with the UNIMPLEMENTABLE rule | `join_columns.py` (920aac1cd), driver `apply_manifest_columns`, driver self-test S5 / S6 | the draft says `ruwe`, `ipd_frac_multi_peak`, `radial_velocity(_error)` stay in `gaia_source` and `non_single_star` is only in `all_source_flags`; confirm on the day |
| E cut 12 | IMPLEMENTED (WP4) for the Amendment 17 counted tables, manifest-driven | `cut12_nss_union.py` (77371136e), `test_wp4_a17.py` | DR3 has no DR4 `nss_*` tables, so the real union runs first on DR4; record each table, solution type and row count |

### 6.3 Section 1, the ordered list, with the tool for each step (N = needs the owner's go in the calculation chat: filename, source, size, caps, location)
| step | tool now | state |
|---|---|---|
| 1 freeze check | section 3's hash check | unchanged |
| 2 data model | the draft names are in `data_assembly/DR4_DRAFT_DATAMODEL_COLUMNS_2026-09-29.md` and `dr4_ready_1/manifest_template_dr4.json` (all 'draft, confirm on release day') | on the day: save the published model, correct names through `--spec-json` (recorded with its sha256), never in code |
| 3 primary base | frozen `fetch_extract.py` + WP3 joins (N) | unchanged |
| 4 cut 9 | SFD98 (Amendment 16(a)) | decided |
| 5 cut 12 | WP4 union (N for the table reads) | implemented, first real run on DR4 |
| 6 cut 13 | (a) candidates: `dry_run_driver.py --release dr4 --cut13 extract-builder --dump-candidates PATH`; (b) pre-brief: `dr4_q1_estimate.py --pairs-csv PATH`; (c) counts: `q1_cones_dr4.py --print-count-queries` (ADQL text only, to be run with a go); (d) offline plan check: `q1_cones_dr4.py --spec dr4_all_source ... --plan-only`; (e) the fetch (N): `q1_cones_dr4.py --spec dr4_all_source ...` with explicit caps; (f) evaluate: `dry_run_driver.py --cut13 cones-literal / cones-orbit --neighbours F --neighbour-pairs C` | (a), (b), (d), (f) offline and tested on DR3; (c), (e) tested against a mock archive only |
| 6b optional tables (Amendment 16(b)) | `q1_cones_dr4.py --spec dr4_gaia_source_environment / dr4_crowded_field_source` (N), then `dry_run_driver.py --neighbours-manifest M` with `include` true or false per table; the choice is recorded in the report | mock-tested; the decision itself is the owner's, recorded before the data are opened |
| 7 cut 11 | RV columns from `gaia_source` (draft) through the WP3 join if absent | unchanged |
| 8 frozen chain | the driver (`--release dr4`) runs the frozen stage G with the pieces above; if the async archive queue is down, `--corr-transport sync` runs the builder's own SELECT synchronously in chunks of at most 1,999 ids (N). **Using it for the primary run must be recorded in the release manifest** (the report carries `correlation_transport`) | `test_driver_corr_sync.py` 8/8 + MUTATE 1-4: byte-identical CSV and correlation arrays against the builder's async path and the on-disk cache, for identical server answers; real-server identity is not testable offline |
| 9 variant (c) | WP2 / `--variant allsource_15c` | see 6.2 C |
| 10 report | the `[7(e)]` lines only; Amendment 18's sigma_build and label from `seed_sweep.py` (G-only K_G >= 50, K_F = 3-10 full rebuilds that need delta fetches of correlation ids and cones, N) and `seed_label.py` | tooling tested on DR3 (`test_seed_sweep.py` 15/15, `_FULL` 17/17, `test_seed_label.py` 8/8); the ladder rungs 'RV-screened subsample' and 'NSS off' are NOT IMPLEMENTED by design (definitions need DR4's tables) and the label lists them as such |

### 6.4 The six release-day gaps of the 2026-10-01 list
1. **Q1 at DR4 scale and schema:** the DR4 tool exists (`dr4_archive_fetch.py`, `q1_cones_dr4.py`, mock test 20/20 + MUTATE 1-6). At the registration's N = 30,000 final pairs the candidate count is about 49,000; the estimator prints low / central / high: about 25,000 / 39,000 / 64,000 queries, 1.1 / 1.7 / 2.7 GB accepted, 31 / 47 / 77 h serial at the DR3 pace (the density factor for the larger catalogue is an ASSUMPTION; a slower release-day archive multiplies the hours). Q1 sits between stage F and stage G, so the first primary gamma-hat comes after it. NOT testable before release: the real archive's cap and speed, whether the LEFT JOIN is index-friendly, whether DR4 `source_id` still encodes the pixel.
2. **Async dependence of stage G's correlation fetch:** the sync fallback exists in the driver (6.3 step 8).
3. **This checklist was stale:** this section is the refresh.
4. **Optional neighbour tables:** fetch code and the switch exist (6.3 step 6b); the whole-table counts Amendment 16(b) wants recorded come from the printed ADQL text, run on the day.
5. **Ladder rungs RV-screened and NSS-off:** NOT IMPLEMENTED by design.
6. **Owner side:** a registered Gaia archive account (higher quotas for a multi-day fetch; only the owner can create it) and a pre-brief of expected size and time per step (`dr4_q1_estimate.py`); the orchestrator is taking both to the owner.

### 6.5 Section 3 (names-only diff check) and section 4 (not tested), updated
- The frozen builder and pipeline are unchanged, so section 3's hash and diff checks apply as written. The new files (the driver, `dr4_archive_fetch.py`, `q1_cones_dr4.py`, the tests) are NOT in that diff; record `git rev-parse HEAD` and the sha256 of the driver, `dr4_archive_fetch.py` and any `--spec-json` file at run time in the manifest.
- Section 4, now: (1) a join: tested on DR3 through a second table (driver self-test S6), never against DR4 tables; (2) the `nss_*` union: tested offline, first real run on DR4; (3) the full-catalogue triple search and variant (c): implemented and run on DR3 (all 10,231 candidates; the DR3 variant-(c) base is a stand-in); (4) curated base plus `all_source_*`: still NOT testable before release; (5) `ap_*` extinction: still never read by any code. New, NOT testable before release: every DR4 query form and name, the real sync cap and pace, the real count of no-G rows and of sources only in the optional tables, and that a sync and an async query give identical rows on the real server (same table, same SELECT; the first real use is recorded in the manifest).

## 7. ADDENDUM 2026-10-03 (dry run; sections 0 to 6 stand unchanged)
- Step 10 (report) gains one command after the pipeline fit: `python3 dr4_ready_1/amdt14_distances.py --log <the pipeline's --catalog output>`. It prints the Amendment 14 distances to the chain ceilings 1.0725 / 1.0900, which no frozen code prints, and flags any fit pinned on the frozen grid edge (0.90 or 1.50). Distances only, no verdict word.
- The readiness audit's F4 now checks the freeze against the LATEST filed amendment's hash (it had compared with Amendment 12's and failed after Amendments 13-19).
- Record: `dr4_ready_1/DRY_RUN_2026-10-03.md`.
- **OWNER DECISION 2026-10-03, recorded before any DR4 data:** the pipeline's `[aniso]` lines (the perpendicular-minus-parallel anisotropy split) are **NOT QUOTED** in the release-day report or anywhere else. Reason: in the dry run every proj-PARALLEL fit sat on the frozen grid floor 0.90, so the split is not a measurement. The frozen pipeline still prints the lines; they are left out of the report. `amdt14_distances.py` prints this decision with its output.
