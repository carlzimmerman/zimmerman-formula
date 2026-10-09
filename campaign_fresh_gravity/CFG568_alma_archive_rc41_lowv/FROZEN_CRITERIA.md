# CFG568: ALMA archive metadata query (read-only, no data download) for the five low-velocity RC41 discs. FROZEN before any query is run

Owner chat 10-09 ("swing the ALMA archive query"). κ = ½ fitted. No DM particle. Metadata only: no product download, no flux, no gas mass, no a₀.

**Why.** CFG567: no z 1.5–3 disc qualifies for self-calibrated a₀(z), because gas-mapped discs are too massive to reach low g_bar. Its cheapest path names the KURVS rotators plus five low-velocity RC41 discs (Genzel+2020), which need an inner anchor and a resolved gas map.
- **KURVS is already done:** `data_assembly/alma_archive_footprint/` (09-29). Best chances there: KURVS-15 (Molina 2019.1.01238.S, CO(2-1) at 0.11″) and KURVS-13. It is cited, not re-queried.

**Targets** (positions from `data_assembly/kmos3d_phibss/kmos3d_catalog.csv`, matched on ID_TARGETED):

| target | RA | Dec | z |
|---|---|---|---|
| GS4_13143 | 53.0881 | −27.8506 | 0.760 |
| GS4_03228 | 53.1232 | −27.9013 | 0.822 |
| COS3_22796 | 150.0794 | +2.4055 | 0.907 |
| U3_05138 | 34.2495 | −5.2521 | 0.810 |

zC_405501 (z 2.154) has no position on disk, so it is queried by target name (`target_name LIKE '%405501%'`), declared. Note that four of the five are at z ≈ 0.8–0.9, not z ≈ 2–2.5.

**Method.** The ALMA Science Archive TAP (`ivoa.obscore`, CONTAINS(POINT, s_region)), with the column list and line-coverage parser copied from `data_assembly/alma_archive_footprint/query.py` and `lines.py`. Lines tested: CO(1-0) 115.271, CO(2-1), CO(3-2), CO(4-3), [CI](1-0), [CI](2-1), redshifted to each disc's z.

**Output.** Per target: proposals covering the position, bands, the best resolution, and which lines fall in a spectral window, with the archive's sensitivity estimate.

**Verdict.**
- **GAS-MAP CANDIDATE** for a target with a CO or [CI] window at resolution ≤ 0.5″.
- **COVERAGE ONLY** if only coarser or continuum coverage exists.
- **NONE** if nothing covers it.

**Controls** (copied).
- Positive: the GOODS-ALMA field centre returns 2015.1.00543.S and 2017.1.00755.S.
- Negative: (RA 150, Dec +60) returns no GOODS-ALMA proposal.

**MUTATE.** Query each target shifted by +1 degree in Dec. Coverage must change for at least one target (exit 1 when detected).
