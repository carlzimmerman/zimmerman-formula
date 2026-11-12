# EUC10: commit ids and the lead's re-run (dated addition, 2026-11-12)

No number, word or gate changes. This file is separate so RESULT.md stays as the lane wrote it.

## Commit ids (local / origin)

| Commit | Local | Origin |
|---|---|---|
| FROZEN_CRITERIA (alone) | 21578af22b | 2d0623e130 |
| Scripts and outputs | fc728754de | b565076df7 |
| RESULT | a5a28a2872 | bd93374308 |
| RESULT trim 1 | a91d084479 | 8f3dab2c08 |
| RESULT trim 2 | 081e1b8479 | 3742d071d8 |

RESULT.md is 101 lines by `wc -l`, one over the house limit; left as written.

## Re-run by the lead

From a copy of the six scripts, one thread, with no network: the offline steps in order (`euc10_parse_samples.py`,
`euc10_scan_lit.py`, `euc10_build_matches.py`, `euc10.py`, then `EUC10_MUTATE=newton`), reading the fetched data the
lane left under `_external_data/euc10_published_source_z/`. All eleven regenerated files equal the committed ones byte
for byte (three JSON, six CSV, two `.out`). The main run exits 0; the mutation twin exits 1. The two fetch scripts
(`euc10_fetch_ned.py`, `euc10_fetch_lit.py`) were not re-run, so the archives were not queried a second time.

A reproduction of the arithmetic from the cached inputs. Not an independent re-grade, and not a second literature search.

## Checked by hand against the cached source files

Both lenses that fall in sample P:

- EUCL-DR1-L015871: the DESI Strong Lens Foundry IV table (arXiv 2509.18078 source, `main.tex` lines 573 to 575) lists
  DESI J065.6453-28.0646 with lens redshift 0.62107 and source redshift 1.17482, both quality 1. The catalogue position
  (65.64466, -28.06521) is about 3 arcsec from the tabulated lens position.
- EUCL-DR1-L016382: the AGEL DR2 table (arXiv 2503.08041 source, `tables/redshifts_part1.tex` line 65) lists
  AGEL053724-464702A with source redshift 2.344 (flag 2) at (84.35163, -46.78401); the catalogue position is
  (84.35164, -46.78400). The SIMBAD row for its source gives 2.3443.

One thing a reader should know: the gate uses the catalogue's photometric lens redshift, as EUC1-F specifies (0.54 and
0.38 for these two). The same tables give spectroscopic lens redshifts of 0.62107 and 0.354. With two lenses the gate
is NOT EVALUABLE either way, so this changes no word; it would matter for any later reading on these two lenses.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
