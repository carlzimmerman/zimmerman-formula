# FN4c_brouwer_lens_rebuild: REBUILD MATCHES (255,052 against 259,383, −1.7 %). On the rebuilt sample the law's lensing gap STANDS on both footings (A1 +0.085 / +0.046 dex)

Criteria: `FROZEN_CRITERIA.md` (d62a6b6b53), committed alone before any script or number. Stage 1 script and outputs: 7f4f3e98ce. Stage 2, the post-result scripts and this README: the commit after it. κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework. No download.

## Labels (frozen)
| Stage | canonical | alt |
|---|---|---|
| 1, the count | **REBUILD MATCHES**, N 255,052 (−1.7 %; line 5 %) | same |
| 2, the law's gap | **GAP STANDS**: G1 Z +8.92, G3 z +4.83 | **GAP STANDS**: G1 Z +6.32, G3 z +3.15 |

**One failed check:** the frozen stage-2 MUTATE (lens masses ×2) did not bite. Details below.

## What made the match
The record's rebuilds kept 55–72 % of candidates; B21 keeps about 34 %. The authors' public code (github.com/margotbrouwer/EG_project @ 4cc0a57826, read as web pages, not run) settles every convention the record had to guess:

| Convention | Authors' code | Record's rebuilds | Count if this one is changed back (`fn4c_rebuild.out`) |
|---|---|---|---|
| Distance for the 3 Mpc sphere | D_A = D_C/(1+z), Ωm 0.2793 | comoving D_C (NV2, LAM1) | +62.8 % |
| Neighbour pool | every row at 0 < z < 0.5, **masked rows included** | unmasked only | +14.2 % |
| Stellar mass | MASS_BEST + (MAG_GAAP_r − MAG_AUTO_CALIB)/2.5 | MASS_BEST + 0.15 | none: +22.3 %; +0.15: +6.8 % |
| 1e11 cut | on log M★ + 0.056 (`masslim` → `GL`) | same in NV2 | without +0.056: +5.4 % |
| Mass ratio | 0.006-dex bins, 0.1 × bin mean | 0.1 × M★ | unbinned: −1.7 % (no change) |

The lead's brief cites arXiv 2101.06010. That is the KiDS-bright catalogue paper (Bilicki+21). The isolation is in Brouwer+21, arXiv:2106.11677.

## Checks (stage 1)
| | Result |
|---|---|
| K1 catalogue sha256, rows, ID join | PASS |
| K2 D_A against an independent integral | PASS, 4.8e-14 |
| K3 planted isolation (distances 2.95 / 3.05 Mpc, ratios 0.095 / 0.105, a duplicate, an out-of-range mass) | PASS, 43 of 43 |
| K4 positional match quality to the shear catalogue | PASS, median 0.033 mag (line 0.10) |
| K5 NV2's recipe through this code | PASS, 486,584 exactly |
| MUTATE, redshifts shuffled in the pool | BITES: 319,202 (+23.1 %), exit 1 |
| Rerun from scratch | byte-identical JSON |

## The weak point, measured after the result (`fn4c_post.py`, POST-RESULT, no label change)
MAG_GAAP_r is not in the public bright files. The KiDS-1000 shear catalogue on disk has it for only 45,672 bright rows (3.7 %), all near the faint limit. So 93 % of isolated lenses carried the frozen stand-in, the matched median +0.182 dex. The count moves about 2.8 % per 0.01 dex of a constant flux scale:

| Flux scale for every row | N | vs 259,383 |
|---|---|---|
| +0.10 | 292,422 | +12.7 % |
| +0.15 | 276,916 | +6.8 % |
| +0.182 | 266,151 | +2.6 % |
| +0.20 | 260,096 | +0.3 % |
| +0.25 | 242,209 | −6.6 % |

LePhare's own output gives the r magnitude it was fed: MAG_ABS_r + DM(z) + K_COR_r. On the matched rows this sits 0.044 mag below MAG_GAAP_r, MAD 0.030 mag (0.012 dex in M★). With that offset, every row gets a flux scale. Bright galaxies need more: median +0.30 dex at r < 18, +0.17 at r ≥ 19.5. **V8, measured where matched and LePhare-rebuilt elsewhere: 259,166 lenses (−0.1 %).** The primary's −1.7 % is the stand-in's.

Means against B21 Appendix A (no line): isolated log⟨M★⟩ 10.624 (B21 10.61); isolated log⟨M_gal⟩ 10.698 (10.69); all candidates without the 1e11 cut 10.773 (10.77). The r < 17.5 numbers do not match cleanly: isolated fraction 27.4 % of candidates (B21 32.0 %), 4,669 bright isolated lenses (about 3,800), log⟨M★⟩ 10.958 without the cut (10.78). B21 does not state these denominators.

## Stage 2: the law through LE1's graders (`fn4c_grade.py`)
LE1's G1 and G3 run unchanged on a mirror of CRG1's inputs. Only `lens_inventory.npz` differs. Per-lens lensing weights are modelled from the June inventory (cells in z and M_gal), as frozen.

| Inventory | Footing | G1 Z (A30) | G1 Z, R ≤ 0.31 | A1 mean (dex) | G3 z |
|---|---|---|---|---|---|
| June, true weights (LE1) | canonical | +9.27 | +5.55 | +0.089 | +5.01 |
| June, true weights (LE1) | alt | +6.52 | +3.59 | +0.050 | +3.32 |
| **Rebuilt, 255,052** | canonical | **+8.92** | +5.32 | **+0.085** | **+4.83** |
| **Rebuilt, 255,052** | alt | **+6.32** | +3.53 | **+0.046** | **+3.15** |
| V8, 259,166 (post-result) | canonical | +8.93 | | +0.085 | +4.84 |
| V8, 259,166 (post-result) | alt | +6.33 | | +0.046 | +3.16 |

- **K6** (the copied graders reproduce LE1 on the June inventory): PASS, difference 0.0 on all four values.
- **K7** (modelled weights on the June inventory): PASS, |ΔZ| at most 0.015 (line 0.20).
- **Frozen MUTATE, lens masses ×2: DOES NOT BITE** (ΔZ −0.19 canonical, −0.03 alt; line 1.0). The graders bin lenses by mass, so doubling every mass mostly moves lenses between bins. The test was badly chosen. It stays failed.
- **Post-result twin, LE1's own law ×2 candidate on the rebuilt inventory** (`fn4c_post_grade.py`): G1 χ² 150 → 1010 canonical, 123 → 1456 alt; G3 z to −8.2 / −9.9. The graders do respond to the model.

**Reading.** The rebuilt sample changes the law's gap by 0.004 dex. The gap is the data against the law, not an artefact of the June lens rebuild. The inventory enters the graders only through masses within fixed bins and their redshifts, so a closer rebuild could not have moved it much.

## What this does not settle
- Isolation still rests on photo-z. B21's MICE test puts satellite signal about 30 % high beyond 0.3 Mpc; the gap is present inside 0.31 Mpc too (S1 column).
- The lens weights are modelled, not recomputed from the 17.7 GB shear catalogue.
- The rebuild now makes per-lens inputs possible (NV2's lens E1, CY6's gas lenses). It does not by itself change any row.
- The exact flux scale needs MAG_GAAP_r for all 1.24 M rows: ESO TAP table `KiDS_DR4_1_ugriZYJHKs_cat_fits`, a few columns, a few tens of MB (estimate from CFG722's 110 MB for 13 columns of 1.545 M rows). Owner's yes needed; V8 suggests it would change little.

## Departures, all disclosed
1. **First run peaked at 25 GB RSS.** Reading the shear catalogue's dtype through astropy's `.data` pulled the whole 17.7 GB table into memory. Fixed to header-only reads; the rerun from scratch gave identical match arrays and a byte-identical JSON at a 0.52 GB peak footprint (2.09 GB max RSS, mostly reclaimable pages).
2. The first launch failed on a missing log folder and the second on a native-endian dtype (NaN positions, crash before any number). Neither produced a count.
3. Stage 2's MUTATE was a poor choice (above). `fn4c_grade.py` exits 1 because of it.

## Files
`fn4c_rebuild.py` (stage 1; `FN4C_MUTATE=1` for the twin), `fn4c_grade.py` (stage 2), `fn4c_post.py` and `fn4c_post_grade.py` (post-result), each with `.out` and `.json`. `cache/` (gitignored) holds the shear-catalogue match, the lens inventories and the input mirrors; all are rebuilt by the scripts. Run: `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 10 python3 -I <script>`; stage 1 about 45 s, stage 2 about 30 s.

κ = ½ FITTED. Not theory closed.
