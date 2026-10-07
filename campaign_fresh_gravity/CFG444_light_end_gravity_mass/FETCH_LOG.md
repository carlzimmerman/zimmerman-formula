# CFG444 FETCH LOG (2026-10-06; data fetches approved by the owner for this lane)

Large raw files are kept under `campaign_fresh_gravity/_external_data/cfg444/` (git-ignored). Tables were read from the LaTeX source / PDF text and transcribed by row position into `data/gravity_masses.csv` and `data/spins_window.csv` (each row names its source position). WebSearch results were used only to locate papers; no number comes from a search summary.

## Paper sources (arXiv e-print, curl)

| arXiv id | paper | bytes | sha256 | used for |
|---|---|---|---|---|
| 1811.11195 | GRAVITY Collab. 2018, 3C 273 BLR (PDF) | 9016455 | 94191730279522d307d92d1c8c59c1155bab26aeeac3c5b9153fe3eff7c492dc | M = 2.6 +/- 1.1e8 (text) |
| 2009.08463 / 2102.00068 | GRAVITY 2020 IRAS 09149-6206 / 2021 NGC 3783 (arXiv API abstracts, file api_gravity_early.xml) | 15713 | 3a06d596cf6af0a128627387b2271f635deb70d7e15e78a4a6042d78c4fbe70d | IRAS 09149 ~1e8 (abstract); NGC 3783 mass taken from SARM II |
| 2401.07676 | GRAVITY Collab. 2024, Mrk 509 / PDS 456 / Mrk 1239 / IC 4329A | 11272210 | b174d858ce53deaecb59a993b8fcf555f430769a3471da95572305b0dbbe7589 | tab:pancoast, tab:circular log M_BH rows |
| 2401.14567 | Abuter et al. 2024, J0920+0657 z=2.3 (PDF) | 3709954 | 99dcf78d3ca9c6ccd724af9ecf2afc50a514737982e2aae2f67a144d4607c5e6 | log M 8.51, final 0.27/0.28 dex (Methods) |
| 2509.13911 | GRAVITY+ Collab. 2025, J0529-4351 z=4 | 2271071 | 1a4e80da98965dbc0c82a1ac5a72de8f491688bbe8451b488a132909b9420883 | tab:model log M_BH 8.90 (-0.13,+0.11) |
| 2609.00278 | disc sizes of J0920 and J0529 | 5398935 | f548ebf663273122ef9c2aa94e75c6fc11c01a681b91e26d11b18d832ee444fc | checked for spin: none |
| 2201.04470 | Li et al. 2022, SARM 3C 273 | 4094086 | d6e534d790cca06a3f009305b6855a868ed2baef60900c5d0fe70c97b3b16428 | log M 9.06 (+0.21,-0.27) model M4; other models 7.96-8.79 |
| 2502.18856 | Li et al. 2025, SARM II four quasars | 2554819 | 0ae48c7cdb23a72ecb3b8fba396040e0034aecc3c6f25eb6fd9e232c38775560 | 3C 273 8.55 (+0.21,-0.15); NGC 3783 7.17 |
| 2502.12645 | Gaur et al. 2025, 3C 273 reflection | 2702598 | c7f480afb0f03c2e401928d6be3acae7726b992e66975ff41e82db0a09e308cb | spin FIXED 0.998 in every fit (not a measurement) |
| 2605.13949 | Sisk-Reynes et al. 2026 (SR26) spin compilation | 2000326 | 0e753cb2268d642254020122b49bcd84897d6c7957db2005757bbb79e05c6235 | cross-match (no precise-dynamical-mass object in window); Table 2 redshifts for route B |

## Catalogues

| source | file (data/ copy) | bytes | sha256 |
|---|---|---|---|
| VizieR J/ApJ/831/134 table2 (van den Bosch 2016), asu-tsv, all rows | vdb16_t2.tsv | 49299 | see below |
| VizieR J/ApJ/831/134 table3 | vdb16_t3.tsv | 10245 | see below |
| VizieR J/A+A/682/A34 erass1-m cone 0.5' on J0529-4351 | erass1_J0529.tsv | 2429 | d87561df1a5c1e2fdf2ff7ff46772ed394f9c23cc3ad5e80e377729df4121295 |
| VizieR J/A+A/682/A34 erass1-m cone 0.5' on J0920+0657 (no source) | erass1_J0920.tsv | 2267 | d54e89c33bd3f9c5f8b7b78d08b521ef6eed89c897b982c366e6b6882c8738ff |
| CDS Sesame, HEASARC TAP (numaster, xmmmaster, xmmssc), VizieR J/ApJS/235/4 table3 (Swift/BAT 105-month): 280 responses by `fetch_xray.py` | `data/xray_fetch_manifest.csv` lists URL, bytes, sha256, date for each | | |

The VizieR TSV headers carry the query date, so re-fetching changes their sha256; the committed copies are the ones used.
- vdb16_t2.tsv: sha256 ccda598cd92a9f8abb02b7f4e3dfb32723b71da45f1d4062088beccf2bfa1f26
- vdb16_t3.tsv: sha256 ea1bda57392db9bbda2964cfe84927bc8108a50996e41f75e7cbfe8569bbe5c0
