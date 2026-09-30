# DR4-READY-1: plan for the work Amendment 16(c) requires before 2 December 2026 (NEW files only)

Written 2026-09-29, at the orchestrator's request. This is a plan; no code in it has run yet.

## What stays untouched

- `PREREGISTRATION_DR4.md`, every `*_HASH.txt`, every `AMENDMENT*` file, `catalog_builder/*.py` and `wide_binary_pipeline.py` are not edited.
- The frozen builder is imported read-only (bytecode writing disabled), as `catalog_builder_dr4/` already does.
- Every new file lives in this directory, `dr4_ready_1/`.
- No cut value, threshold, estimator setting or decision row is touched. Where a choice is needed, it is recorded here or in a run manifest before any data are opened.
- **DR3 numbers from these dry runs are code-path tests, not results.** DR3's γ̂ has already been seen, and Amendment 7(e) applies: no verdict word.

## The required work (Amendment 16(c); RELEASE_DAY_CHECKLIST section 0, items B–E)

| WP | what (new file) | reuses (read-only) | DR3 dry run | data |
|---|---|---|---|---|
| 1 | `cut13_allsource.py`: the cut-13 third-star search against the FULL catalogue. Server-side cone search around both components (radius 30,000 AU / d, d from the primary's parallax, as in `cut13.py`); the returned neighbours are tested client-side by `cut13.third_star_literal` (PRIMARY, Amendment 16(b)) and `third_star_orbit_aware` (reported VARIANT). The no-G, no-kinematics and environment-table counts go to the manifest. | `catalog_builder_dr4/cut13.py` | On the 6,210-pair DR3 final sample (and its pre-cut-13 parent). Compare: (i) the extract-based orbit-aware flags of the existing build against all-source orbit-aware, which measures what the ϖ > 3.5 mas extract floor misses; (ii) literal against orbit-aware on the same neighbours; (iii) the frozen γ̂ on each sample, reported as a dry-run systematic. | **archive query Q1** |
| 2 | `fetch_extract_variant.py` + `build_variant.py`: Amendment 15(c)'s sample-definition variant. The same chain (crowding, pair search, chance-alignment KDE, Σ₁₈, cuts) on a second base, written to its own extract directory, manifest and CSV. | `catalog_builder/build_catalog.py` stage functions (`stage_a(ext, …)` takes the extract path; `main()`'s orchestration is copied, not edited) | DR3 has no curated/all-source split, so the stand-in "all-source" base is the frozen extract query WITHOUT `phot_g_mean_mag IS NOT NULL`. This tests the variant chain end to end; its numbers are not physics. | **archive query Q3** |
| 3 | `join_columns.py`: join `ruwe`, `ipd_frac_multi_peak`, `radial_velocity` (+ error) and any other missing column by `source_id` from a second table. On release day the table and column names are read from the DR4 data model and recorded in the manifest before the data are opened. | — | Fully on disk. Drop those columns from the DR3 extract, write them to a separate table (shuffled order, with some ids missing on purpose), rejoin, and require the final CSV and γ̂ to be byte-identical to the reference build. Controls: a missing column must raise, not pass silently; a planted mismatched id must be caught. | on disk |
| 4 | `cut12_nss_union.py`: a loader for the `nss_*` source-id lists plus `cut12_stub.nss_union_flags`. Which tables count is a run-time list, written into the manifest before the data are opened, with row counts. | `catalog_builder_dr4/cut12_stub.py` | DR3's four NSS tables (`nss_two_body_orbit`, `nss_acceleration_astro`, `nss_non_linear_spectro`, `nss_vim_fl`), restricted to the 12,420 pair components. Compare the union with the extract's `non_single_star` integer; the mismatches, by solution type, are the dry-run output. | **archive query Q2** |
| 5 | `dry_run_dr3.py` + `README.md`: WP1–4 end to end on DR3. Outputs: the cut flow, pair counts and γ̂ for (a) the reference build, (b) + cut 13 all-source (literal, and orbit-aware), (c) + the cut-12 union, (d) the variant base, (e) the join path, which must equal (a). Runtime and query volumes are measured so the release-day jobs can be sized. MUTATE controls: a planted third star, a planted NSS id and a dropped join column must each be caught. | all of the above | — | Q1–Q3 plus on-disk data |

**Ready** means that each WP runs on DR3 without manual steps, WP3 reproduces the reference exactly, the planted controls are caught, and the manifest template lists every DR4 table and column name to be confirmed on release day. A cut that cannot be implemented is reported UNIMPLEMENTABLE (Amendment 15(d)).

## Data for the DR3 dry run

**On disk now (gitignored), no query needed:**
- The DR3 base extract, `real_research/data/widebinaries/dr3_extract/`:
  - 12 HEALPix chunks, 4,582,547 sources, about 400 MB;
  - the frozen query: ϖ > 3.5 mas, ϖ/σ > 5, σ_ϖ < 2, G not null, |b| > 10;
  - columns include `ruwe`, `ipd_frac_multi_peak`, `radial_velocity`, `non_single_star`.
- The stage caches A–G, `wide_binaries_dr3.csv` (6,210 pairs), and the `scaled_clean` and El-Badry-R variants.
- The Σ₁₈ HEALPix-7 map and the SFD98 dust maps (`real_research/data/dustmaps/sfd/`).
- El-Badry+2021's catalogue (`all_columns_catalog.fits.gz`, 1.3 GB) for validation.
- **What this covers:** WP3 completely, and the unit and synthetic tests of WP1 and WP4 (which already exist).
- **What it cannot cover:**
  - an all-source search, because the extract's ϖ > 3.5 mas floor hides faint thirds;
  - the NSS tables;
  - a second base.

**Needs a Gaia archive query.** ESA Gaia TAP, `gaiadr3` tables, read-only, async jobs, pilot first. Each needs the owner's explicit go in the calculation chat.

| query | what | pilot | full |
|---|---|---|---|
| Q1 (WP1) | `gaiadr3.gaia_source` cone neighbours of the pair components (an uploaded table of source_id, ra, dec, radius; radius 30,000 AU/d ≈ 30ϖ″, 105–300″); astrometry, errors, G, with no quality cut server-side | 500 pairs: about 50–100 k rows, 10–20 MB | 6,210 pairs: about 1–2 M rows, 200–400 MB (batched; row counts go to the manifest) |
| Q2 (WP4) | the four DR3 `nss_*` tables joined to the 12,420 uploaded component source_ids (source_id, solution type) | — | ≲ a few thousand rows, < 1 MB |
| Q3 (WP2) | the frozen extract query without `phot_g_mean_mag IS NOT NULL` (the DR3 stand-in all-source base) | 1 of 12 chunks: about 35 MB | 12 chunks: about 4.6–5 M rows, 400–450 MB |

Row and size figures are estimates from the stellar density at |b| > 10° to G = 20 and from the existing extract's chunk sizes. The pilots measure them.

## Order and timing

1. WP3 (on disk).
2. Q2 and WP4 (tiny).
3. The Q1 pilot and WP1; then Q1 full.
4. The Q3 pilot and WP2.
5. WP5, the full dry run.

- All of it is well before 2 December.
- Each step commits its script, manifest and outputs with a MUTATE control, following the repo's usual rules.
- The DR3 dry-run numbers carry no verdict (Amendment 7(e)).

## Not in this plan

- Any DR4 table or column name. Those are read on release day, and names only (Amendment 15(d)).
- Whether `crowded_field_source` and `gaia_source_environment` are also searched for cut 13. Amendment 16(b) records their counts and decides on release day, before the data are opened.
- The `ap_*` extinction variant of cut 9. It is reported only, and its table is not yet known.

## Appended 2026-09-29 (after WP3; the plan above is unchanged)

- **WP3: READY on DR3, offline** (`wp3_join_dryrun_dr3.py`, `join_columns.py`).
  - R0: stage G re-run from the cached stages is byte-identical to the on-disk `wide_binaries_dr3.csv` (6,210 pairs, sha256 6fff64d9…).
  - J1: stripping `ruwe`, `ipd_frac_multi_peak`, `radial_velocity` and `radial_velocity_error` and rejoining them by source_id from a shuffled second table gives a byte-identical CSV, with 0 unmatched ids.
  - Controls: K1 (a missing column) and K2 (duplicated ids) raise. K3 (1% of ids dropped) counts all 45,784 and changes the CSV (6,107 pairs).
- **Incident, disclosed.**
  - The first WP3 attempt called the frozen builder's `fetch_correlations`.
  - Its cache did not cover 14 ids of today's primary selection, so it tried a Gaia archive query, without the owner's go. The process sat idle (6.6 s CPU in over 10 minutes) and was killed.
  - The cache file is unchanged (mtime 2026-09-23), so no query completed.
  - The dry run now blocks every outgoing connection by construction (socket guard) and reads correlations offline from the union of the two on-disk caches. Their values are identical on their 20,496 shared ids.
  - 4 ids are in neither cache and get zero correlation, identically in every run. R0 is still byte-identical to the on-disk CSV.
- **Release-day hazard found (not a frozen-file edit).** The frozen builder overwrites `stage_G_corr.npz` with only its latest query's ids; it does not merge them. So running a variant after the primary (or the reverse) forces a new archive query on the next run.
  - WP5's driver must give each variant its own correlation cache file.
  - A new driver can do that without editing `build_catalog.py`, because `fetch_correlations` takes the cache path.
- **Correction to Q1's radius.** The cone radius is 30,000 AU/d = 30ϖ″. That is 120″ at 250 pc, but it grows past 300″ inside 100 pc (600″ at 50 pc; 3000″ at 10 pc), not "105–300″" as written above. The pilot's row counts will show whether the nearest pairs dominate the volume. (Noted by the orchestrator.)
- **WP1 and WP4, offline halves (added 2026-09-29).**
  - `cut13_allsource.py` builds the cone-search upload table and ADQL (DR3: `gaia_source`; DR4 form: `all_source_astrometry` joined to `all_source_photometry` for G). It evaluates the returned neighbours with `cut13.py`'s literal and orbit-aware criteria.
  - `cut12_nss_union.py` loads per-table id files named in the manifest and calls `cut12_stub`. Its table list is run-time data: DR4's NSS tables, per ESA's page, are not DR3's four (data chat, d9ac3a13f).
  - `manifest_template_dr4.json` holds every name and count to be confirmed before the data are opened. Its candidates come from the data chat's preview and are non-binding.
  - `test_wp1_wp4_offline.py` runs synthetic tests under a socket guard: 10/10 pass, and both removal controls bite.
  - The real DR3 dry runs of WP1 and WP4 still need queries Q1 and Q2.
- **WP5 driver skeleton (added 2026-09-29): `dry_run_driver.py`.**
  - Design:
    - a socket guard unless `--allow-network` is given;
    - a per-base correlation cache (`<extract>/stage_G_corr_<variant>.npz`);
    - the manifest-driven WP3 joins, and the UNIMPLEMENTABLE rule (disable and flag, never substitute);
    - cut 13 from the builder, or from `cut13.py`'s orbit-aware or literal criterion.
  - `--self-test` passes 7/7 offline (about 15 s):
    - the driver reproduces the DR3 reference CSV byte-identically (6,210 pairs, sha 6fff64d9…);
    - `cut13.py`'s orbit-aware criterion on the extract equals the builder's cut 13 byte for byte;
    - the literal PRIMARY criterion on the extract runs end to end (6,189 pairs; a code-path number only);
    - a planted unavailable column (RUWE) is flagged UNIMPLEMENTABLE and the run completes;
    - a second-table join inside the driver leaves the CSV byte-identical.
  - No cache file is written by the self-test.
- **Owner's go and Q2 (added 2026-09-29).**
  - The owner approved, in the calculation chat, Q2 plus the Q1 pilot (500 pairs) and the Q3 pilot (one chunk). Full-size Q1 and Q3 need a separate go.
  - `q_fetch_dr3.py` is the only DR4-READY-1 script that opens the network. It refuses a pilot larger than 500 pairs and records query text, row counts and sha256 in `manifest_q_dr3.json`. The data files stay gitignored.
  - **Q2 result: 0 rows** in each of DR3's four NSS tables for the sample's 12,420 components. This is expected by construction: the frozen build required `non_single_star = 0`. In the extract, 84,906 of 4,582,547 sources are nonzero, and none of them is a sample component.
  - `wp4_nss_dryrun_dr3.py` reads the real archive FITS through both loaders. Every reading flags 0 pairs, in agreement with the frozen proxy.
    - This is a mechanics check, not an independent test of the query. A positive control (a query on known NSS sources) was not in the approved scope.
    - Its readings were written after the zero row counts were printed. With zero rows, no reading can differ.
    - The first run crashed before writing output: the script passed a table as counted in one reading and excluded in another, which `run_a17` refuses. The fix is in the script.
- **Amendment 17 readings (the amendment is a DRAFT, NOT FILED; added 2026-09-29).**
  - New in `cut12_nss_union.py`:
    - `run_a17` runs every reading declared in the manifest.
    - A two-source row is own-pair when its ids match the pair's two components as an unordered pair; otherwise it is third-source. The exemption applies only to the declared, recorded `solution_type` strings.
    - A17 (c)'s diagnostic is reported, never used to reject.
    - `adql_nss` is the release-day query text, searching both id columns.
    - `run()` now refuses two-source tables, because it matches `source_id` only.
  - `test_wp4_a17.py`: 19/19 pass, and all three MUTATE controls are caught. The harness had two bugs of its own, kept and disclosed: the first run is in `test_wp4_a17_firstrun.out`.
  - `manifest_template_dr4.json` now carries the draft data model's names (every one "draft 2026-06-26, confirm on release day") and the A17 draft's readings as NOT-FILED candidates.
  - The template's `join_by_source_id` key is renamed to `join_file`, the key the driver actually reads. This was a latent mismatch in this template, found while editing it.
- **Amendment 17 FILED (added 2026-09-29).**
  - The owner filed it in the orchestrator's chat: ab9557d58, append-only, prereg sha256 97aa97c4 → 7fd0b36b, with `AMENDMENT17_HASH.txt`. Its text equals draft revision 2.
  - `cut12_nss_union.run_a17` with the reading `A17_primary` is now the binding cut-12 reading. V17a and V17b are the reported variants.
  - `manifest_template_dr4.json` now carries the filed reading in `cut12_nss` (`primary_reading`, `readings`, `two_source_tables`, `diagnostic`, `excluded`), with the block renamed `a17_filed_ab9557d58`.
  - `solution_types_recorded` stays null until release day (A17 (d)); `run_a17` refuses an exemption until it is filled.
  - Nothing in `run_a17` or `test_wp4_a17.py` changed.
