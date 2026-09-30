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
- **Q1/Q3 pilot fetch: the archive's behaviour and the new forms (added 2026-09-29).**
  - What the archive did: the anonymous ASYNC queue is blocked (a trivial async job did not return in 170 s; the earlier stuck jobs are the likely cause). The SYNC endpoint works (a trivial primary-key query returns in about 3 s) but returns at most 2000 rows, silently. Every upload cone join tried stalled: per-row radius, the single 1,000-cone job, the 5-batch split, a 6-cone probe, a constant radius, a HEALPix-range upload. Literal source_id-range conditions written into the WHERE (no upload) are index-friendly: 3 pairs, 821 rows, 4.5 s.
  - `q1_pilot_ranges.py` (Q1 pilot, the same 500 pairs): sync queries of literal level-12 source_id ranges covering both components' 30 kAU / d cones plus a 30 arcsec margin, re-filtered locally to the exact cones in the original schema, so `wp1_cut13_pilot_dr3.py` runs unchanged. A result of exactly 2000 rows is truncated and is discarded and split; a query that has not answered in 120 s is cut and retried; caps of 20 MB accepted and 30 MB received; needs `--owner-go-recorded`. Offline coverage check: the planned ranges contain the source_id of all 3,513 local-extract sources inside the exact cones (0 missed), and after a run every such source must be in the output.
  - `q3_pilot_delta.py` (Q3 pilot): the approved query is the frozen chunk 0 without the G condition. Its rows are the frozen chunk 0 already on disk (329,234 rows, none without G) plus the rows with no G magnitude, so only the latter are fetched (the same WHERE with `phot_g_mean_mag IS NULL`, sync source_id pieces, adaptive width, the same truncation and timeout handling, 5 MB cap), then assembled locally into `dr3_extract_allsource_15c/chunk_00.fits` (frozen rows first, then the delta, frozen column order and dtypes). The row set equals what the approved query returns; the archive's row order is not reproduced (the frozen chunk 0 is not sorted either).
  - Tests, offline against a synthetic archive that truncates at 2000 rows, drops one connection and hangs one query (socket guard): `test_q1_pilot_ranges.py` (T1-T7, exact row set equals a brute-force truth; MUTATE control: with truncation detection disabled 2,960 rows are lost and T1 fails) and `test_q3_pilot_delta.py` (T1-T7; MUTATE: 961 rows lost). All pass.
  - Status: neither script has been run against the archive in full. The first live attempt of the range form (3 queries, about 0.4 MB, every result truncated at 2000 rows and discarded) was made before the new form was cleared with the owner; the forms are on hold for the owner's go.
- **Q1/Q3 pilots run (2026-09-30; the owner's go for both new forms was given in the calculation chat after the archive findings above).**
  - **Q1** (`q1_pilot_ranges.py`, the same 500 pairs): 207 queries in 1,048 s; 4 truncated results discarded, none used; 9.19 MB accepted and 9.74 MB received against the 20 and 30 MB caps; 111,857 unique raw rows, 125,902 exact two-cone rows (10.1 MB, sha256 248d414b...); all 3,513 local-extract sources inside the cones are in the output (0 missing). `manifest_q1_ranges.json`.
  - **Q3** (`q3_pilot_delta.py`): 34 queries in 146 s, no truncation, 0.47 MB received; **216 rows of chunk 0 have no G magnitude**; the assembled chunk 0 is 329,450 rows = 329,234 frozen + 216 (29.0 MB, local, gitignored; sha256 7afda68c...); the 216 rows pass the local check of the WHERE (0 violations). The approved 35 MB download became 0.47 MB. `manifest_q3_delta.json`.
  - **WP1** (`wp1_cut13_pilot_dr3.py`; the first run failed on the manifest key it read, a mismatch with the new fetch form, fixed): K1 1000/1000, K2 and K3 pass. On the 500 final pairs the all-source literal criterion flags 0, the orbit-aware variant 0, the extract search 0, new hits 0. The cones hold 68,019 neighbours: 36 without G (0 kinematic matches among them) and 8,929 without kinematics. Sizing: 9,779 rows per deg2 of cones, so a full Q1 (6,210 pairs, 179.7 deg2) is about 1.76 million rows, about 141 MB (an upper estimate: overlapping cones are counted twice).
  - **WP2** (`wp2_variant_pilot_dr3.py`): chunk 0, primary base 329,234 sources gives 276 final pairs; the all-source variant base 329,450 (216 without G) gives 274; common 264, primary-only 12, variant-only 10; every difference first appears at stage G and none involves a component without G. W1 (the primary base is a subset of the variant's) passes. Sizing: the old full-Q3 form is about 404 MB; in the delta form the 12 frozen chunks are already on disk and only the G-less rows are fetched (about 34 queries and 0.47 MB per chunk here, so roughly 400 queries and 6 MB for all twelve if the rate is similar).
  - Full-size Q1 and Q3 are NOT run: they need a separate go from the owner. DR3 numbers here are code-path tests, never results (Amendment 7(e)).
- **Full-size Q3 (delta form) RUN (2026-09-30; the owner's go for the full-size Q3 and Q1 given in the calculation chat).** `q3_delta_chunks.py` (offline-tested, 897a4238f; T1-T8 and a MUTATE control) fetched the rows with no G magnitude of chunks 1-11 of the frozen extract: **268 synchronous queries in 1,053 s, 3.82 MB received, 0 truncated results, 0 cut or failed pieces, 3,002 delta rows** (248 / 245 / 262 / 225 / 218 / 196 / 374 / 298 / 252 / 316 / 368 per chunk; with chunk 0's 216 the full extract has **3,218 sources without G**), every delta row validated against the WHERE (0 violations) and disjoint from the frozen rows. The assembled variant chunks (frozen rows first, then the delta; 4,256,315 rows for chunks 1-11, 4,585,765 with chunk 0) are in the gitignored `dr3_extract_allsource_15c/`; `manifest_q3_delta_chunks.json`. The approved ~420 MB download became 3.82 MB.
  - The full-size Q1 tool `q1_full_ranges.py` (offline-tested with a crash and a resume, 140d06f7e) plans 6,210 pairs, 741,614 pixels, 107,603 source_id ranges, 152 deg2, about 1.49 million unique rows / 107 MB kept, every one of the 47,781 local-extract sources inside the cones covered; it was started after Q3 (about 2,900 queries, about 4 hours, resumable, caps 200 / 260 MB).
  - `wp1_cut13_full_dr3.py` and `wp2_variant_full_dr3.py` (957b9d91e) are the full-size dry runs; WP1 on the pilot file reproduces the pilot exactly.
- **WP2 at full size RUN (2026-09-30, offline, 516 s; `wp2_variant_full_dr3.py`, N_SHIFT = 3 as the builder's smoke mode).** All twelve chunks. Primary base 4,582,547 sources (none without G); all-source variant base 4,585,765 (3,218 without G = the 3,002 delta rows of chunks 1-11 plus the 216 of chunk 0). Initial pairs 380,438 / 381,990; clean 214,002 / 215,040; with R 213,097 / 214,133; **FINAL 6,173 (primary) / 6,178 (variant)**; common 5,993, primary-only 180, variant-only 185; every primary-only pair first missing in the variant at stage G (177) or D (3), every variant-only pair at stage G (185); no differing pair has a component without G. W1 (the primary base is a subset of the variant: variant minus its no-G rows equals the primary) passes. Sizing: 404 MB on disk against 403 MB. DR3 numbers are code-path tests, never results (Amendment 7(e)).
- **WP2 NOISE FLOOR at full size (2026-09-30, offline, 693 s; `wp2_noise_floor_full_dr3.py`): the 180 / 185 differences are at the reseeding noise floor.** The frozen builder draws random numbers in three places (the stage-E shifted realisations with per-block seeds over `np.array_split(keep, 400)`, the leave-10%-out fold of `r_chance`, and the stage-G velocity-error Monte Carlo as one stream over the pair array), so adding sources moves all three streams. Each base was rebuilt with two other seed sets for all three streams (data untouched; frozen files not edited, seeds patched in memory; the default seeds reproduce the WP2 counts exactly). **Same base, other seeds (pure noise): 152 to 187 one-way flips, mean 171 (about 2.8% of the final set); final counts range 6,173 to 6,208 (primary) and 6,177 to 6,195 (variant). Cross bases, same seeds: 151 to 192, mean 176; ratio 1.03.** So at N_SHIFT = 3 the all-source base shows no effect on the final pair set above the reseeding noise, and the Amendment 15(c) comparison at DR4 must be read against this floor (the real run uses N_SHIFT = 30, which lowers the shifted-realisation noise but not the fold and velocity-error streams; the floor at 30 is not measured here). Common random numbers per pair, or repeated builds with other seeds, would be the way to separate a real all-source effect from this noise.

- **WP2-gamma at the real N_SHIFT = 30 (2026-09-30, offline, 8,812 s; `wp2_gamma_spread_full_dr3.py`, question frozen in `WP2_GAMMA_SPREAD_FROZEN.md` 01bc48e32).** Ten seed sets of the builder's three random streams (k = 0 the builder's own frozen seeds), the PRIMARY base, every build with WP2's stage-C / stage-D counts (380,438 initial, 214,002 clean). **Q1:** FINAL counts 6,181 to 6,212 (mean 6,201.3, SD 9.7); one-way flips against k = 0 mean 157.8, over all ordered pairs of builds 162.3 (SD 10.8, range 133 to 187) = **2.6% of the final pairs, the same as at N_SHIFT = 3**. **Q2 / Q3 (the pipeline's own estimator, DR3-noise forward model, NON-SCORING):** canonical footing gamma-hat mean 1.0785, **SD across builds 0.0164 = 0.30 of the mean sigma_fit (0.0554) and 0.28 of sigma_tot (0.0589)**; the fit-only control (the k = 0 catalog refitted with ten other fit seeds) has SD 0.0094 (0.17 sigma_fit), so the implied build-only SD is 0.0134 (0.24 sigma_fit); alt footing mean 1.0652, SD 0.0172 = 0.34 sigma_fit (0.31 sigma_tot), fit-only 0.0050, build-only 0.0165 (0.32 sigma_fit). **Reading: rebuilding the same base with other seeds moves gamma-hat by about a quarter to a third of its own statistical error at this N (about 6,200 pairs, sigma_fit 0.055); the fraction at DR4's N is not measured here, and these are code-path numbers, never results (Amendment 7(e)).** The frozen question's own threshold (SD above 10% of sigma_fit: the orchestrator may draft Amendment 18, NOT filed, the owner's go) is exceeded. **Controls:** C1, C2, C4 pass; **C3 MUTATE FAILED as frozen (a global v_perp x 1.05 leaves gamma-hat unchanged to the printed digit: the pipeline's fit has a free kappa that absorbs a global velocity scale, so my control was badly designed, not the estimator broken)**; a post hoc MUTATE=2 (the same factor only for pairs with log10 g_N/a0 < 0) moves gamma-hat by +0.0575 (canonical, 2.0 x the 3-fit-SD threshold 0.0283) and +0.0900 (alt, 6.0 x 0.0150) and PASSES. First MUTATE run kept (`wp2_gamma_spread_full_dr3_MUTATE_firstrun.out`); both outputs committed.

- **Q1 full-size fetch COMPLETE (2026-09-30, networked, the owner's go of 2026-09-30 in the calculation chat; `q1_full_ranges.py --owner-go-recorded`; manifest `manifest_q1_full.json`, commit bde6e3629).** All 6,210 final DR3 pairs: **1,956,086 exact-cone rows** (1,644,566 unique raw rows) over 179.7 deg^2 of cones (10,887 rows/deg^2; the pilot's 9,779), 3,122 synchronous source_id-range queries (150 truncated results discarded and their batches halved), **135.2 MB kept / 155.9 MB received** (hard caps 200 / 260 MB), 14,349 s, no batch resumed from cache. **Completeness: every stage-A source inside the exact cones is in the fetch (0 of 47,781 missing)**; the file `q1_full_neighbours.fits` (156,496,320 bytes) is gitignored and its sha256 5c92bd0607a9c7138568e759427c6dbb4040a1490a6e64b174fe3be519b44249 (re-computed from the file on disk after the run) equals the manifest's.

- **WP1 at full size (2026-09-30, offline, 4 s; `wp1_cut13_full_dr3.py`, `.out`, `.json`; DR3 numbers are code-path tests, never results, Amendment 7(e)).** K1 (every cone contains its own component, 12,420 of 12,420), K2 and K3 pass. **All-source:** 1,057,450 neighbours in the cones; the literal criterion (the PRIMARY of Amendment 16(b)) flags **2 of 6,210 final pairs**, the orbit-aware bound **0**; the frozen extract's own search over the same cones flags 1 (literal) and 0 (orbit-aware). **NEW under the literal criterion: 1 pair (0.02%), lost 0; new under the orbit-aware bound: 0.** The one new pair (pair 1371) is hit by a G = 19.89 neighbour at 24.4 kAU that is not in the extract because it fails `parallax <= 3.5 or null` and `parallax_over_error <= 5`. Neighbours without G: 969, none of which has a kinematic match; without kinematics: 140,166. **Reading: at DR3 scale the all-source expansion changes the cut-13 outcome of 1 pair in 6,210 under the literal criterion and of none under the orbit-aware bound, about two orders of magnitude below the reseeding noise floor of the final pair set (2.6% of the pairs flip between builds, WP2).** The pilot's sizing forecast (about 1.76 M rows, 141 MB) was low by 11% (actual 1.96 M rows, 156.5 MB). **Extrapolation, not measured:** at the frozen DR4 N of about 30,000 pairs and a similar cone density the same fetch would be about 9.4 M rows, about 760 MB at 80 bytes/row, and about 4.8 times the 14,349 s.
