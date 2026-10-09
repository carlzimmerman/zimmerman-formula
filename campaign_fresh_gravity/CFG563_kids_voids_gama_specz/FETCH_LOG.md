# CFG563 fetch log (owner approved fetching GAMA spectroscopic data and a low-z large-scale-structure catalogue for this lane)

Endpoint for all rows: `https://datacentral.org.au/vo/tap/sync` (ADQL, FORMAT=csv, MAXREC=1000000), GAMA DR4 on Data Central.

| date (UTC) | query | file | rows | bytes | sha256 |
|---|---|---|---|---|---|
| 2026-10-09 10:48 | `SELECT CATAID, X, Y, Z FROM gama_dr4.VoidGalsv02` | data/VoidGalsv02.csv | 1,677 | 114,748 | d9b788fe208dd91c3e75a1266e816140f9a136d5ef19adb64909f2b6e31a88f8 |
| 2026-10-09 10:48 | `SELECT CATAID, X, Y, Z, TendrilID FROM gama_dr4.TendrilGalsv02` | data/TendrilGalsv02.csv | 14,544 | 1,121,503 | 77855fc6e98a88bdc99d4f7ea48c121e302093a048a753515edaeb51736331de |
| 2026-10-09 10:48 | `SELECT CATAID, X, Y, Z, d, GroupID, FilID FROM gama_dr4.FilGalsv02` | data/FilGalsv02.csv | 29,247 | 3,069,916 | c26715bb44f1b8988d40372c279d17b9cfb6e8a07b5627f882b31f32d5967635 |
| 2026-10-09 10:48 | `SELECT CATAID, RA, DEC, Z, NQ, GeoS4, GeoS10 FROM gama_dr4.GalaxiesClassifiedv01` | `_external_data/cfg563/GalaxiesClassifiedv01.csv` (git-ignored) | 117,556 | 8,387,128 | 95d9e2a17d788022f502191583f30582a22fe20e65b0247fe64492a6b8bea7b9 |

Reused read-only (not refetched): `_external_data/cfg471/G3CGalv10.csv`, sha256
051950e193e447ebf8bf7a9458c3ffe4ea368596b8042732ee933fc95f6ad9f8 (matches CFG471's FETCH_LOG; the script checks it).

Notes
- `VoidGals/TendrilGals/FilGals v02` = Alpaslan et al. 2014 (MNRAS 438, 177) filament finder DMU.
  `GalaxiesClassifiedv01` = Eardley et al. 2015 (MNRAS 448, 3665) geometric environments (GeoS4/GeoS10: 0 void, 1 sheet,
  2 filament, 3 knot; class codes from the table description and the paper's convention).
- Table list and column descriptions read from the same service's TAP_SCHEMA; no WebFetch summaries used.
- To refetch: rerun the queries above; the script refuses to run if any sha256 differs.
