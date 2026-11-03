# LAM2 amendments, dated, written before any count

`FROZEN_CRITERIA.md` (fa14da563a) is unedited. kappa = 1/2 FITTED. Not theory closed.

## 2026-11-03, A1: stage-0 query, EW sign, repeat observations (owner approved the query)
- **Query:** `lam2_fetch.py`, SkyServer DR17 SqlSearch, 23 chunks of up to 250 specobjid, 746,943 bytes in `_external_data/lam2_sdss_lines_2026_11_03/`. 5811 matched DynPop rows map to 5730 distinct specobjid; all 5730 returned, 5681 with a galSpecLine row.
- **EW sign, checked before any cut:** the three highest-S/N H-alpha emitters (plate-mjd-fiber 2636-54082-321, 349-51699-402, 630-52050-245; flux S/N 168-186) have h_alpha_eqw of -21.8, -29.8 and -93.0 A. Negative means emission. The gas-poor cut is therefore **-h_alpha_eqw < 3 A**. Small negative values at zero flux (about -0.1 to -0.3 A) fall inside it.
- **Repeat observations:** 157 DynPop rows share a specobjid with another row. They are the same galaxy (same mangaid) observed twice by MaNGA. One row per mangaid is kept: highest Qual, then the first row in file order. The slow label comes from that row. Duplicates are counted and reported.
- **Galaxies without a galSpecLine row** are excluded from both samples and counted, as frozen.
- **F2 counts:** Hanley-McNeil uses the gas-poor quality sample's slow and fast counts, and all of them, because all scores are out of fold.
