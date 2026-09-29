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
