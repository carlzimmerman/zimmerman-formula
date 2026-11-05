# DP5 FROZEN CRITERIA: DR4 stage-A extract fetch with a spec'd column list, and the NSS-table fetcher

Written 2026-11-05, committed alone before any code. NEW code only; OFFLINE tests (a fake archive; no connection is
opened); no frozen file edited (`catalog_builder/fetch_extract.py`, `cut12_nss_union.py`, `cut12_stub.py`, the driver,
the prereg and amendments, the owner decisions). Every query these tools can send needs the owner's go on the day.
κ = ½ FITTED; not theory closed.

## Why (DP3 open issues O1, O2)
- **O1.** The frozen `fetch_extract.py` selects `non_single_star` from `gaia{release}.gaia_source`. The DR4 draft data model
  (2026-06-26) has `non_single_star` only in `all_source_flags`, so the frozen DR4 stage-A query would fail. The frozen
  script has no `--spec-json`. For DR4 the column is not read (`manifest_template_dr4.json`: "not read for DR4: cut 12 is the
  nss_* union").
- **O2.** No tool fetches the NSS-group id files that `cut12_nss_union.run` / `run_a17` read. Only the query text exists
  (`adql_nss`, an upload join). Upload joins stalled on the anonymous archive in 2026-09 (PLAN.md).

## What is built
1. `fetch_extract_dr4.py`: the frozen stage-A query (same WHERE, same 12 level-0 source_id chunks, same Σ18 query, same
   output layout and manifest keys) with the column list and table taken from a spec (`--spec-json` overrides; recorded
   with its sha256). Default DR4 spec = the frozen columns minus `non_single_star`. Transport: the frozen async job with
   retries (default), or `--sync-ranges`: sync queries over finer source_id ranges with the 2000-row truncation rule
   (a result of exactly the cap is discarded and the range split), as the Q1/Q3 pilots used.
2. `fetch_nss_dr4.py`: for each table named in the manifest's `cut12_nss.counted_tables` (and only those), fetch the rows
   touching the sample's component ids, writing one id file per table in the form `cut12_nss_union.load_ids` reads
   (FITS with `source_id`, plus `source_id_secondary` for two-source tables and `solution_type`). Two transports:
   `upload` (the frozen `adql_nss` text, unchanged) and `inlist` (the same SELECT with `t.source_id IN (...)` batches, and
   for two-source tables also `t.source_id_secondary IN (...)`, sync, truncation rule). It refuses to run without declared
   counted tables (as `cut12_stub` does).

## Controls (offline; all reported)
- **F1 regression.** With the DR3 spec, every query text `fetch_extract_dr4.py` builds (12 chunks + Σ18) is
  byte-identical to the frozen `fetch_extract.py`'s text, read from the frozen `catalog_builder/manifest_dr3.json`.
- **F2 DR4 text.** The DR4 default query has no `non_single_star`, the table is `gaiadr4.gaia_source`, and the other 16
  columns and the WHERE are unchanged.
- **F3 sync-ranges completeness.** On a fake archive holding a synthetic table (≥ 50k rows; sync cap 2000), the
  sync-ranges fetch returns exactly the brute-force row set; truncated results are discarded and split.
- **N1 transport equivalence.** On a fake archive with synthetic one-source and two-source NSS tables, `inlist` and
  `upload` return the same row set per table (after the A17 union / own-pair de-duplication), equal to a brute-force truth.
- **N2 reader.** The written id files load through `cut12_nss_union.load_ids` (imported read only) and give the truth ids.
- **N3 refusal.** With no counted tables declared, the fetcher refuses before any query.
- **MUTATE=1** truncation detection disabled: F3 must FAIL. **MUTATE=2** the two-source secondary query dropped: N1 must FAIL.

## Limits
Offline only: archive behaviour (async queue, upload joins, throttling, real DR4 names) is not tested. The NSS table
list and two-source flags come from the manifest on the day (A17). Memory ≤ 2 GB.
