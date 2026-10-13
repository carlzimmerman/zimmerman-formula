# CFG679D: inputs still to fetch before `cfg679_des.py` may measure (written 2026-10-13, before any DES lensing number)

`cfg679_des.py` refuses to measure (exit 3) until every item below is complete on disk under
`campaign_fresh_gravity/_external_data/cfg679_des/` (gitignored). All of it is queued in `run_after_mcal.sh`, which waits for
`mcal: COMPLETE` in `download_mcal.log`, so nothing here shares the DES server with the metacal download.

Server root: `https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/`.

| # | what | file / dataset | why (FROZEN_CRITERIA section) | bytes (estimate) | downloader mode |
|---|---|---|---|---|---|
| 1 | index group listing | `y3kp_cats/DESY3_indexcat.h5`, keys of `/` and `index/` (one level down), layout of every `select*` dataset | the probe never reached the index file; the names `select_bin1..4` (under `index/` or `index/metacal/`) are confirmed here before reading | < 5 MB metadata | `listcols --file index` |
| 2 | fiducial selection + tomographic bin | `index/select_bin1`, `select_bin2`, `select_bin3`, `select_bin4` (metacal row indices, or row masks: both handled) | sources and their bin (3) | ≤ 0.8 GB | `index` |
| 3 | stellar-mass coadd ids | `stellar_mass/DESY3_stellar_mass_catalog.hdf5`, `coadd_obj_id` (int64, contiguous) | key for the GOLD match (2) | 0.29 GB | `smid` |
| 4 | shear response | `y3kp_cats/DESY3_metacal_v03-004.h5`, `catalog/unsheared/R11`, `R22` on 20 seeded random 1M-row chunks (seed 6790, list in `resp_chunks.json`) | R_b (3) | 0.32 GB | `resp` |
| 5 | GOLD column listing + magnitude choice | `y3kp_cats/DESY3_GOLD_2_2.1.h5`, keys of `catalog/gold` | the choice rule of (2) is applied to the column list alone, before any lens is selected, and written to `gold_choice.json` | < 5 MB metadata | `listcols --file gold` |
| 6 | GOLD id + magnitudes | `catalog/gold/coadd_object_id`; `sof_cm_mag_corrected_g`, `_r`, `_i` (SOF corrected). If those names are absent: the GOLD 2.2 default model (BDF) magnitudes, first match of `bdf_mag_*corrected_<b>`, then `bdf_mag_dered_<b>`, then `bdf_mag_<b>` | r < 20 cut, isolation pool, g − i early/late split (2) | 4 columns × ~399 M rows: 6.4–12.8 GB (4- or 8-byte) | `gold` |
| 7 | selection response (optional) | `index/select_1p`, `_1m`, `_2p`, `_2m` (per-bin names `select_bin<b>_<sh>` / `select_<sh>_bin<b>` if they exist), only the rows inside the 20 response chunks, by a coarse sample every 500k elements + window reads | (3): "selection response ... if present, else neglected" | ~0.2–0.8 GB | `selresp` |

## Matching (2)
GOLD rows are matched to the stellar-mass catalogue by coadd id (`coadd_object_id` = `coadd_obj_id`), streamed in 1M-row slices
against the sorted ids of the 0.2 < z < 0.5 stellar-mass rows. Unmatched stellar-mass rows get no magnitude and fail r < 20; their
number is reported.

## Byte budget (owner approval: ≤ 30 GB)
Stellar-mass 1.14 + metacal 15.97 + smid 0.29 + resp 0.32 + index ≤ 0.8 + selresp ≤ 0.8 ≈ 19.3 GB before GOLD. GOLD needs 6.4 GB
(4-byte columns) to 12.8 GB (8-byte). `run_after_mcal.sh` passes the remaining budget as `--max-gb`; if the GOLD plan exceeds it,
the downloader logs `ABORT: plan exceeds --max-gb` and stops. If that happens, it is an owner decision (raise the budget by ≤ 2.5 GB, or
skip `selresp`); nothing is changed silently.

## Not needed
GOLD `ra`, `dec` (the match is by id), sompz, the sheared metacal catalogues (only their selection lists, item 7).
