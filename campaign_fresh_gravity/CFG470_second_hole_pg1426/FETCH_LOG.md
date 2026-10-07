# CFG470 FETCH LOG (2026-10-07; data fetches approved by the owner for this lane)

Every fetch came after the frozen criteria commit (0b70d2b38). All are real tables or the paper's own LaTeX; no number comes from a WebFetch/WebSearch summary (none was used).

## Catalogue tables (curl, committed copies in data/)

VizieR URL form: `https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-out.max=unlimited&-out.all&-out.add=_RA,_DE&-source=<table>`. The VizieR headers carry the query date, so a re-fetch changes the sha256; the committed copies are the ones used.

| table | file | bytes | sha256 |
|---|---|---|---|
| J/ApJS/261/5/table5 (Mejia-Restrepo+22, broad Halpha) | mr22_t5_halpha.tsv | 230449 | 027a374700b50b72c234724554c26e0edf7a9c6c90d59a246f7e5f37680cbd9c |
| J/ApJS/261/5/table6 (Mejia-Restrepo+22, broad Hbeta) | mr22_t6_hbeta.tsv | 170028 | 8ed5fcdb91c76ed0f6454eca1b19aac26aa32ee8136c1377eb148ca6e41fd13d |
| J/ApJS/261/2/table9 (Koss+22 DR2 general properties) | koss22_t9_general.tsv | 202593 | 6e15ffebf3b059da90d1715a77aaf6105ccaa0a8c996fa0d54aaaf11febd9e08 |
| J/ApJS/235/4/table3 (Oh+18 BAT 105-month) | oh18_bat105.tsv | 450337 | 0ba36ba286824f8cdb2f8b588dd5ffa1b99d26c3de21f70f5ab1786f64d65fb3 |
| AGN Black Hole Mass Database index, https://www.astro.gsu.edu/AGNmass/ (HTML table, page default f) | agnmass_db_index.html | 43127 | 9a96ae17dd5ad1297efa8653ed8db7eb7cdad0378ef5cfba97d28da5aa426bb4 |

J/ApJS/261/1 returned no VizieR tables; the DR2 catalogue quantities come from J/ApJS/261/2 table9. All tables join on the BAT 105-month sequence number (MR22 `ID` = Koss22 `ID` = Oh18 `Seq`; checked on NGC 6240 = 841 and VV 697 = 1632).

## Informational lookups (fetch_aux.py; 21 responses)

2MASS PSC (VizieR II/246, 5 arcsec), HEASARC TAP `numaster` (3') and `xmmmaster` (10') for PG 1426+015 and the six part-A candidates. URL, bytes, sha256 and date of each response: `data/aux_manifest.csv`; responses in `data/aux/`.

## Paper source (not committed)

| arXiv id | paper | bytes | sha256 | used for |
|---|---|---|---|---|
| 2509.13411 | Walton et al. 2025, PG 1426+015 (W25) | 1819108 | 012431cbdf7f23d0fe2c831eff5c9b31cd88a5b5210a4a1b839a9988ad013fdb (identical to CFG394's copy) | Table tab_obs good exposures (NuSTAR 105 ks; pn/MOS/RGS 71/99/101 ks); Sec. hard band (spin ~ full prograde range); Sec. Black Hole Spin (a* = 0.95 +/- 0.01 xillver, 0.77 +0.06/-0.08 reflionx; hard band a* >~ -0.15; systematic Delta a* ~ 0.1; Mallick+25 warm-corona 0.3-0.93) |

Kept under `campaign_fresh_gravity/_external_data/cfg470/` (git-ignored). GRAVITY mass precisions are read from CFG444's committed `data/gravity_masses.csv` (each row names its source position in the paper), not re-fetched.
