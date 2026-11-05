# DP5: DR4 stage-A fetch (spec'd columns) and NSS id-file fetcher: BUILT, 6/6 OFFLINE CHECKS PASS

Criteria `FROZEN_CRITERIA.md` (c4c56e708e), committed alone before the code. New code only; offline tests against a fake
archive (socket guard on); no frozen file edited. Every query either tool can send needs the owner's go on the day.
κ = ½ FITTED; not theory closed.

## Why
DP3's release-day dry run found two blockers:
- **O1.** The frozen `catalog_builder/fetch_extract.py` asks `gaia_source` for `non_single_star`, a column the DR4 draft
  data model has only in `all_source_flags`, and that DR4 does not read.
- **O2.** No tool fetched the NSS-group id files that cut 12 reads.

## Result
| check | result |
|---|---|
| F1 DR3 spec: all 13 query texts (12 chunks + Σ18) byte-identical to the frozen tool's, from `manifest_dr3.json` | PASS |
| F2 DR4 default: `gaiadr4.gaia_source`, no `non_single_star`, the other 16 columns and the WHERE unchanged | PASS |
| F3 `--sync-ranges` on a fake 63,000-row chunk with a 2,000-row silent cap: exact row set (102 queries; 19 truncated pieces discarded and split) | PASS |
| N1 `inlist` vs `upload` (frozen `adql_nss` text) vs brute force, one-source and two-source tables, own pairs counted once | PASS |
| N2 id files read through `cut12_nss_union.load_entries` / `load_ids` | PASS |
| N3 refuses with no counted tables; on the filed A17 template it fetches the 9 declared tables, never `nss_epoch_flags` | PASS |
| MUTATE=1 (truncation detection off) | F3 FAILED as designed |
| MUTATE=2 (two-source secondary-id query dropped) | N1 FAILED as designed |

The NSS `inlist` truncation path was not triggered in N1 (0 truncated). It uses the same split rule as F3, which was.

## Release day
- Stage A: `python3 -B dr4_push_2026_11_05/DP5_dr4_fetchers/fetch_extract_dr4.py --release dr4 --print-queries`
  shows the 13 texts. Then run with `--manifest <path> --owner-go-recorded "<go>"` and optionally `--sync-ranges`; use
  that if the anonymous async queue is blocked again, as it was in 2026-09.
  - A name correction goes in `--spec-json`, recorded with its sha256.
  - Outputs go to the same gitignored `real_research/data/widebinaries/dr4_extract/` as the frozen tool.
- NSS: `python3 -B dr4_push_2026_11_05/DP5_dr4_fetchers/fetch_nss_dr4.py --manifest <dr4 manifest> --ids <component ids>
  --out-dir <data_dir> --transport inlist --owner-go-recorded "<go>"`. It writes one `<table>_ids.fits` per table and
  `nss_fetch_report.json` with the `id_files` map for `cut12_nss.id_files`.

## Not covered
- How the archive behaves: async queue, upload joins, throttling, and the real DR4 table and column names.
- O3 (logging in to a registered account) is not addressed. astroquery's `Gaia.login()` would have to be called by the
  owner, interactively, before either tool runs; no credential is ever stored or handled by these tools.
- Departure from the criteria: none.
