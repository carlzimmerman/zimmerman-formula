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
