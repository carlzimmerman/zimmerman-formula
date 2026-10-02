# ALFALFA-SDSS local sample: HI widths plus SDSS colours (data gathering only)

An HI-selected local galaxy sample with SDSS photometry, parsed into one CSV for later use as a same-pipeline local control for a z~0.2 HI width to circular velocity to baryon chain. **This directory contains data and documentation only.** No acceleration, a0, rotation velocity, baryonic mass or gravity test is computed here. The only recomputations are catalogue-internal identities run to verify what columns mean (check 3 and check 4 below).

## Files

| file | what it is |
|---|---|
| `alfalfa_sdss.csv` | 31,503 rows (one per AGC number), 49 columns, 8,092,685 bytes, sha256 `c790a7ec68c45b66a86be1bc6317b9b29da6b8736baa013e97af21fb40599ed2`. Missing = empty field. |
| `columns.md` | Data dictionary: every column, unit, source table and byte range, meaning (ReadMe wording paraphrased with line references), missing counts, and the list of columns the catalogue does not have. |
| `parse_alfalfa_sdss.py` | Self-contained parser (Python standard library only). `python3 parse_alfalfa_sdss.py` rebuilds the CSV; `--checks` prints every number quoted below; `--verify` rebuilds in memory and confirms byte-identity with the file on disk. |
| `README.md` | This file. |

## Provenance

Source: the ALFALFA-SDSS Galaxy Catalog, Durbala, Finn, Crone Odekon, Haynes, Koopmann and O'Donoghue 2020, AJ 160, 271 (arXiv:2011.02588; VizieR J/AJ/160/271, tables `table1` and `table2`), joined on AGC number to the ALFALFA alpha.100 HI source catalogue, Haynes et al. 2018, ApJ 861, 49 (VizieR J/ApJ/861/49, `table2`, the corrected version of August 2019).

**Why two catalogues.** The ALFALFA-SDSS tables hold only AGC, SDSS identification and photometry, distance, extinction, axis ratio, i-band magnitude, absolute magnitude, colour, stellar masses, star-formation rates and log M_HI. They contain **no W50, W20, S21, S/N or HI profile-quality code**. Those come from the alpha.100 table, so both are needed for "widths plus colours".

Cite Durbala et al. 2020 (AJ 160, 271) and Haynes et al. 2018 (ApJ 861, 49); the data are served by CDS (VizieR) and the Cornell ALFALFA archive.

All downloads used `data_assembly/fetch_logged.py` (HEAD first, hard size cap, sha256 logged); every file is far below the 100 MB per-file cap, and the total of 11,689,177 bytes (11.7 MB) is far below the 300 MB task limit. They sit in `<repo-parent>/_external_data/alfalfa_sdss/` (`<repo-parent>` is the directory that holds the repository checkout). The log rows are also in `data_assembly/FETCH_MANIFEST_2026-10-01.jsonl` and `FETCH_LOG_2026-10-01.md`. Fetched 2026-10-01 local time (UTC stamps below).

| label | URL | bytes | sha256 | fetched (UTC) | stored as |
|---|---|---|---|---|---|
| ALFALFA-SDSS Durbala2020 VizieR ReadMe (J/AJ/160/271) | https://cdsarc.cds.unistra.fr/ftp/J/AJ/160/271/ReadMe | 9,565 | `ef44c9d8378a8db03f2fcb97596269f0eb6e478b5b7aa41ed57a218534c87273` | 2026-10-02T01:55:06Z | `ReadMe` |
| ALFALFA alpha.100 Haynes2018 VizieR ReadMe (J/ApJ/861/49) | https://cdsarc.cds.unistra.fr/ftp/J/ApJ/861/49/ReadMe | 13,857 | `9c3910a65100be7aceff9f949ffe6b568933b09860f5557c809cfd692b8498b0` | 2026-10-02T01:55:43Z | `ReadMe_Haynes2018_J_ApJ_861_49` |
| ALFALFA-SDSS Durbala2020 table1.dat.gz (J/AJ/160/271) | https://cdsarc.cds.unistra.fr/ftp/J/AJ/160/271/table1.dat.gz | 957,052 | `21e7e51ea9f75ceab6c039fe56e86ee6669f0323b173453b0b5da73173cfbcee` | 2026-10-02T01:56:50Z | `durbala2020_table1.dat.gz` |
| ALFALFA-SDSS Durbala2020 table2.dat.gz (J/AJ/160/271) | https://cdsarc.cds.unistra.fr/ftp/J/AJ/160/271/table2.dat.gz | 839,699 | `216e96b97fb12eda3dff7c937775be9d384697dd5eaab4b5fd839f71c926031e` | 2026-10-02T01:56:57Z | `durbala2020_table2.dat.gz` |
| ALFALFA alpha.100 Haynes2018 table2.dat.gz (J/ApJ/861/49, Aug-2019 corrected) | https://cdsarc.cds.unistra.fr/ftp/J/ApJ/861/49/table2.dat.gz | 1,221,575 | `85d4c299ea6cceea61f9b016a1b6c93cbbd9603a2f72aa1a11f12789f3abd31a` | 2026-10-02T01:57:05Z | `haynes2018_a100_table2.dat.gz` |
| ALFALFA-SDSS Durbala2020 table1 FITS (Cornell archive, 21-Sep-2020) | https://egg.astro.cornell.edu/alfalfa/data/a100files/durbala2020-table1.21-Sep-2020.fits.gz | 1,946,190 | `73cf97effac6fbf1676c330d7648ccb45cf1e2b11414a12b72036c758d7cf917` | 2026-10-02T01:59:34Z | `durbala2020-table1.21-Sep-2020.fits.gz` |
| ALFALFA-SDSS Durbala2020 table2 FITS (Cornell archive, 21-Sep-2020) | https://egg.astro.cornell.edu/alfalfa/data/a100files/durbala2020-table2.21-Sep-2020.fits.gz | 2,700,358 | `1423c29717aff27e58dad2b7f4fb6055878866f06188cb08a35055ee9438d32e` | 2026-10-02T01:59:40Z | `durbala2020-table2.21-Sep-2020.fits.gz` |
| ALFALFA alpha.100 table2 CSV (Cornell archive, a100.code12.table2.190808) | https://egg.astro.cornell.edu/alfalfa/data/a100files/a100.code12.table2.190808.csv | 4,000,881 | `a029d2786d0c41098777f1c2a17d2a4c993d1654a5144618b7998a537d6bdcd6` | 2026-10-02T01:59:46Z | `a100.code12.table2.190808.csv` |

The CSV is built from the three VizieR fixed-width tables (rows 3 to 5). The Cornell FITS and CSV (rows 6 to 8) are the authors' own releases of the same tables; they are used only to cross-check the VizieR text (section "Sanity checks", check 7) and are the place to go if more than the published rounding is wanted (every VizieR number is the 2-decimal rounding of the FITS value).

Documentation reading, outside the fetch log: the two papers (arXiv:2011.02588v1 and arXiv:1805.11499) were opened with the WebFetch tool, which cached their PDFs (2.1 MB and 3 MB) under the assistant's tool-results folder, outside this repository. They were read only for column definitions, caveats and published counts; no data were taken from them. The WebFetch tool could not list the CDS ftp directory (it received an anti-bot interstitial page); nothing was done to get around that, and the individual files were reachable through the logged helper. No page content contained instructions addressed to the fetcher.

## What the CSV contains

* One row per AGC number, ascending: **31,503 rows = 31,500 present in both sources + 1 Durbala-only (AGC 2023) + 2 alpha.100-only (AGC 116503, AGC 322050)**. Columns `in_durbala2020` and `in_a100_table2` say which. AGC 2023 has no HI widths or flux; AGC 116503 and 322050 have no SDSS information. The Durbala table post-dates the August-2019 alpha.100 correction yet lists the 31,501 sources of the earlier release (the count D20 quotes), which would explain this three-row difference; I did not investigate further.
* Column groups (details in `columns.md`): identity and flags; positions (Durbala optical position, alpha.100 HI centroid and optical counterpart, in decimal degrees); HI measurements (Vhel, distance and error, S21 and error, W50 and error, W20, S/N, rms, HI code, log M_HI and error); SDSS photometry and shape (Galactic extinction in g and i, r-band axis ratio b/a with error, i-band cmodel magnitude with error); derived optical properties (internal-extinction coefficients, absolute i magnitude, corrected g-i colour with errors); stellar masses by three methods and star-formation rates by three methods.
* **Magnitude type.** Observed magnitude: i-band **cmodel**, apparent, **not** extinction corrected (`imag_cmodel`; Galactic extinction is given separately in `gext_mag`, `iext_mag`). Corrected absolute i magnitude (`imag_abs_corr`): cmodel, Galactic plus internal extinction removed, no K-correction. Corrected colour (`gi_corr`): Galactic plus internal extinction removed; the paper says it is built from **model** magnitudes while the ReadMe's table-2 note says cmodel (unresolved, see ambiguities). **There are no u, g, r or z magnitudes and no g-r colour.**
* **Axis ratio:** `ba_r` is the SDSS r-band exponential-profile axis ratio, rounded to 0.01. No inclination angle exists.
* Other absent columns: optical size/R50, distance-method flag, cluster/group/Virgo flags (list in `columns.md`, section 7).

### Requested content against what exists

| requested | in the CSV | status |
|---|---|---|
| identifiers: AGC, SDSS objid | `agc`, `sdss_objid` (also `name_oc`) | present |
| RA, Dec | `ra_dur_deg`/`dec_dur_deg`, `ra_hi_deg`/`dec_hi_deg`, `ra_oc_deg`/`dec_oc_deg` | present |
| heliocentric velocity | `vhel_kms` | present |
| adopted distance, error, method/flow flag | `dist_mpc`, `e_dist_mpc` | distance present; **method flag absent** |
| S21 and error | `s21_jykms`, `e_s21_jykms` | present |
| W50, error, W20 | `w50_kms`, `e_w50_kms`, `w20_kms` | present |
| profile-quality code 1/2 | `hi_code` | present |
| log M_HI | `logmhi`, `e_logmhi` | present |
| SDSS ugriz magnitudes | `imag_cmodel` (i, cmodel, apparent, uncorrected) and `imag_abs_corr` | **only i; no u, g, r, z** |
| g-r and g-i colours | `gi_corr` | **g-i only (corrected); no g-r** |
| axis ratio or inclination | `ba_r`, `e_ba_r` | b/a present; **inclination absent** |
| stellar mass and method | `logms_taylor`, `logms_mcgaugh`, `logms_gswlc` | present (three methods) |
| SFR | `logsfr22`, `logsfr_nuvir`, `logsfr_gswlc` | present (three methods) |
| optical size or R50 | none | **absent** |
| cluster, group, Virgo flags | none | **absent** |

## Parsing decisions

1. Fields are read by the 1-based byte ranges of the two ReadMe byte-by-byte tables and kept as the catalogue's own text, stripped of padding (no reformatting, so no rounding). Missing = empty.
2. Outer join on AGC, so no row of any source is dropped. The overlapping columns (Vhel, Dist, e_Dist, log M_HI, e_log M_HI) are identical in the Durbala and alpha.100 tables on all 31,500 shared rows (check 7); the alpha.100 value is used, and the Durbala value fills AGC 2023 only.
3. The SDSS ObjID written as -9223372036854775808 (int64 minimum, 1,863 Durbala rows with no counterpart) is turned into an empty field.
4. alpha.100 sexagesimal positions are converted to decimal degrees with 6 decimals, taking the Dec sign from its own byte (needed for Dec between -1 and 0).
5. VizieR labels were renamed for clarity: `Ag`/`Ai` become `gamma_g`/`gamma_i` (they are coefficients, see `columns.md`), `logSFRN` becomes `logsfr_nuvir`, and units are in the CSV column names where useful.
6. **No value was changed, flagged out or removed**, including the clearly invalid ones listed under caveats.

## Row counts against the published numbers

| quantity | here | published |
|---|---|---|
| Durbala tables 1 and 2 rows | 31,501 | 31,501 (D-RM:53-56) |
| alpha.100 table 2 rows | 31,502 | 31,502 (H-RM:64) |
| `sdss_phot_flag` 0 / 1 / 2 / 3 | 1,296 / 28,267 / 1,371 / 567 | same in the ReadMe (D-RM:97-104). The arXiv v1 text of D20 gives 1,296 / 28,057 / 1,361 / 787, i.e. 220 fewer identifications (29,418 against 29,638 here); the published tables match the ReadMe, not the arXiv v1 text. |
| rows with an SDSS objID | 29,638 | 29,418 in arXiv v1 |
| `hi_code` 1 / 2 | 25,434 / 6,068 | 25,434 / 6,068 in H18 Sect. 3.1 (D20 quotes 25,433 / 6,068 for the earlier release) |

## Sanity checks

Every number is printed by `python3 parse_alfalfa_sdss.py --checks`; the full output is in the appendix.

| check | result |
|---|---|
| 1. Row counts | 31,503 = 31,500 + 1 + 2; flags and codes as in the table above. |
| 2. Fraction with HI code 1 | **0.8074** (25,434 of 31,502; code 2 is 6,068). |
| 2. Median W50 | **174 km/s** over 31,502 rows (16-84 percent: 82-302; range 9-885). Code 1: 174; code 2: 175. |
| 2. Other HI medians | S21 1.26 Jy km/s (31,500 rows, excluding the two invalid fluxes); S/N 8.8; log M_HI 9.64; Vhel 7,946 km/s; D 114.8 Mpc. |
| 3. log M_HI = log10(2.356e5 D^2 S21) against `logmhi` | Over all 31,502 rows (using \|S21\| for AGC 715637): **max deviation 0.146 dex at AGC 5470** (Leo I, D = 0.3 Mpc, where rounding D to 0.1 Mpc allows 0.169 dex); median 0.0025, 99th percentile 0.0052. For D at least 10 Mpc and S21 at least 0.5 Jy km/s (29,886 rows) the maximum is **0.0077 dex**. **No row lies outside the envelope set by the published rounding** (D to 0.1 Mpc, S21 to 0.01, log M_HI to 0.01). H18's error formula (eq. 5) reproduces `e_logmhi` to a median 0.002 dex. |
| 4. (g-i) colour medians (flag-1 rows, 28,267) | **median 0.62 mag** (16-84 percent: 0.39-0.94); HI code 1: 0.62, code 2: 0.62. |
| 4. Other optical medians (flag 1) | iMAG -19.83; i_cmodel 15.77; b/a 0.57; log M*(Taylor) 9.50; log M*(McGaugh) 9.75 (29,298 rows); log M*(GSWLC-2) 9.76 (14,725 rows). |
| 4. Definition checks | `imag_abs_corr` is reproduced from the table's own columns as `imag_cmodel - iext_mag - gamma_i log10(1/ba_r) - 5 log10(dist_mpc) - 25` with median deviation 0.004 mag, max 0.021 (28,267 rows; rounding-limited). `gamma_i` is exactly 0 for all 2,517 rows fainter than M_i = -17 and positive for all 23,046 rows brighter than -18. |
| 4. Stellar-mass columns | median(GSWLC - Taylor) = +0.130 dex; median(GSWLC - McGaugh) = -0.140 dex: the three columns are raw method outputs that differ systematically. |
| 7. Cross-version | Durbala and alpha.100 agree on Vhel, Dist, e_Dist, logMHI, e_logMHI for all 31,500 shared rows. Against the Cornell FITS (float64) every Durbala column equals the FITS value rounded to 2 decimals, with identical missing patterns (largest deviation 1.000 in units of the rounding half-step). The Cornell alpha.100 CSV equals the VizieR table in every numeric column (31,502 rows); decimal-degree positions agree to 4.3e-5 deg in RA and 8e-6 deg in Dec (the Cornell file is rounded). |

Control that can fail (ad hoc, in scratch, not part of the script): corrupting 5 `gi_corr` and 3 `w50_kms` values in a copy of the CSV raised the FITS ratio for `gi_corr` from 1.00 to 6.9 and made the Cornell-CSV check report 3 differing W50 values; shifting byte ranges in a copy of the parser made the checks print an absurd W50 median (49 km/s, maximum 99) and then crash.

### Rows with each key column missing (of 31,503)

* 0 missing: `vhel_kms`, `dist_mpc`, `e_dist_mpc`, `logmhi`, `e_logmhi`.
* 1 missing (AGC 2023, which has no alpha.100 row): `w50_kms`, `e_w50_kms`, `w20_kms`, `s21_jykms`, `e_s21_jykms`, `snr`, `rms_mjy`, `hi_code`.
* 1,865 missing (no SDSS photometry: 1,296 outside the footprint + 567 no counterpart + 2 alpha.100-only rows): `sdss_objid`, `gext_mag`, `iext_mag`, `ba_r`, `e_ba_r`, `imag_cmodel`, `e_imag_cmodel`.
* 3,236 missing (as above plus the 1,371 flag-2 rows): `gamma_g`, `gamma_i`, `imag_abs_corr`, `gi_corr` (and its error), `logms_taylor`.
* 2,205 missing: `logms_mcgaugh`. 16,778 missing: `logms_gswlc`, `logsfr_gswlc`. 7,608 missing: `logsfr22`. 15,389 missing: `logsfr_nuvir`.
* 345 missing: `ra_oc_deg`, `dec_oc_deg`. 21,115 missing: `name_oc`. 2 missing: `sdss_phot_flag`, `ra_dur_deg`, `dec_dur_deg`. 1 missing: `ra_hi_deg`, `dec_hi_deg`.
* **Rows with W50, S21, HI code, D, log M_HI, b/a, g-i, iMAG and Taylor mass all present: 28,267** (code 1: 22,311; code 2: 5,956), exactly the `sdss_phot_flag` 1 rows.

All 49 columns with their counts are listed in the appendix and in `columns.md`.

## Caveats the analyst should know

* **W50 is instrument-corrected only.** The alpha.100 W50 is the full width at 50% of the peak between polynomial fits to the two profile horns, corrected for instrumental broadening; **it is not corrected for turbulence, inclination or cosmological stretch** (H18 Sect. 3.1 col. 6 and Sect. 4). It is the projected width. Its error is a statistical S/N-dependent term plus a systematic term in quadrature.
* **Distance has no method flag.** Per H18: D = cz_cmb / 70 km/s/Mpc above 6,000 km/s heliocentric velocity; the Masters (2005) flow model below, overridden by primary or secondary distances, group systemic velocities, or Virgo-substructure distances where available. The authors warn that this is an inhomogeneous mixture, that the flow model can be double or triple valued near dense structure, and that errors near attractors are underestimated. What the table itself shows: of the 22,355 rows above 6,000 km/s, 98.8% have D within 5.5 Mpc of Vhel/70 (as D = cz_cmb/70 predicts), against 89.1% of the 9,147 rows at or below 6,000 km/s, so the low-velocity half is a mixture. Distances are Hubble distances; H18 estimates the resulting M_HI offset at most about 3% at z = 0.06.
* **Virgo and cluster membership are not flagged.** Partial proxies: 145 rows have D = 16.7 Mpc exactly (the most common value), 79 have 16.6 and 48 have 16.4, with errors of 1.2 to 4.3 Mpc, which is what Virgo-substructure assignments would look like; 472 rows lie at 15-18 Mpc; 151 `name_oc` begin `VCC` (Virgo Cluster Catalogue). Further repeated values (24.2 Mpc in 62 rows; 97.7 to 105.3 Mpc in 48 to 58 rows each) probably come from group assignments, but that is an inference. Absence from these lists does not mean field membership.
* **Code-2 detections.** 6,068 rows (19%) are "priors": low S/N accepted because of a coincident optical redshift; 15 have S/N below 3. The authors say they should not be used where a defined completeness limit matters. Code 2 and code 1 have indistinguishable medians in W50 (175 and 174 km/s) and g-i (0.62 for both) in this sample.
* **Selection and completeness.** ALFALFA is flux-limited in a width-dependent way and biased to gas-rich, blue, low-surface-brightness galaxies (H18 Sect. 4); statistical use needs completeness corrections. Interference makes the survey incomplete above cz_cmb about 15,000 km/s (1,235 rows have Vhel above 15,000).
* **Flux and confusion.** S21 comes from the half-peak isophote region with a beam-pattern correction and may underestimate very extended or asymmetric sources; there is no HI self-absorption correction. The beam is about 3.8 by 3.3 arcmin, one optical counterpart is assigned per HI source, and the authors consider confusion minor overall but note that individual confused sources are easy to find. HI centroids are accurate to about 20 arcsec on average and can be off by over an arcmin at low S/N; use the optical-counterpart positions for cross-matching.
* **Invalid values kept as published.** S21 is -7.61 for AGC 715637 (its log M_HI of 10.94 matches +7.61, a sign error) and 999.90 for AGC 1117 (`N 598`, presumably too extended for the pipeline; the placeholder flux makes its log M_HI of 8.20 wrong). W20 is 0 in 11 rows and below W50 in 9 more. `e_ba_r` exceeds 1 in 46 rows and `e_imag_cmodel` in 48 (SDSS pipeline values, up to 865 and 42,134), `e_gi_corr` reaches 220 mag. Three rows have e_Dist = 0.0 (AGC 2023, Leo I, Leo T).
* **SDSS matching.** 344 alpha.100 sources have no optical counterpart (all `sdss_phot_flag` 3). Four SDSS objIDs are attached to two AGC rows each, with the rows degrees apart (AGC 204290/208436, 729793/729803, 5183/5186, 7085/220172), so at least one ID of each pair is wrong. Flag-2 rows (g or i error above 0.05, often shredded or contaminated images) have no corrected magnitude, colour or optical stellar mass by design.
* **Internal extinction.** The correction (A = gamma log10(a/b), gamma rising linearly with luminosity above M = -17) was designed for blue, star-forming small and intermediate-mass galaxies and is not recommended for red-sequence or very massive galaxies (D20 Sect. 2.2). The paper adopts an uncertainty of 0.3 in gamma.
* **Stellar masses** differ by method by up to about 0.14 dex (median); the table does not apply the paper's linear translations to the GSWLC-2 scale, and the initial mass function is not stated in the ReadMe. The `logsfr_nuvir` column is the 22-micron-corrected NUV rate, not raw NUV as the ReadMe wording suggests.

## Ambiguities the analyst must resolve

1. **Which magnitude type the colour is.** The ReadMe Description and D20 say model magnitudes for colours and cmodel for absolute magnitude; the ReadMe note on table 2 says cmodel for both. The tables cannot settle it. This dictionary follows the paper (model).
2. **Inclination.** Only the SDSS r-band exponential-fit axis ratio `ba_r` (rounded to 0.01, floor 0.05) is given; any thickness correction, and the handling of rows with a huge `e_ba_r`, is the analyst's choice.
3. **Which width.** `w50_kms` is not corrected for inclination or turbulence, and not for (1+z) (negligible at z < 0.06).
4. **Which stellar mass column** (three methods, 0.13-0.14 dex apart, none translated to a common scale) and the IMF.
5. **Which rows are "clean".** Code 2, photometry flags 2 and 3, the three e_Dist = 0 rows, and the invalid S21 and W20 values above are all left in.
6. **The three AGC rows** that exist in only one of the two sources.

## Reproduce

```
cd <repo>/data_assembly/alfalfa_sdss_local_control
python3 parse_alfalfa_sdss.py --checks     # rebuild the CSV, print the checks
python3 parse_alfalfa_sdss.py --verify     # rebuild in memory, compare with the file on disk
shasum -a 256 alfalfa_sdss.csv             # c790a7ec68c45b66a86be1bc6317b9b29da6b8736baa013e97af21fb40599ed2
```

Re-running reproduced the CSV byte for byte (two independent builds, one from a different working directory and hash seed, both `cmp`-identical). The script refuses to run if an input file's sha256 differs from the logged value. The input folder defaults to `<repo-parent>/_external_data/alfalfa_sdss/`, found relative to the script (override with `--data-dir`).

## Appendix: full output of `python3 parse_alfalfa_sdss.py --checks`

```
wrote alfalfa_sdss.csv: 31503 data rows, 49 columns, 8092685 bytes, sha256 c790a7ec68c45b66a86be1bc6317b9b29da6b8736baa013e97af21fb40599ed2
# sanity checks on alfalfa_sdss.csv  (sha256 c790a7ec68c45b66a86be1bc6317b9b29da6b8736baa013e97af21fb40599ed2)

## 1. row counts
rows (union of AGC numbers) = 31503; in both = 31500; Durbala only = 1 (AGC 2023); alpha.100 only = 2 (AGC 116503, 322050)
Durbala rows = 31501 (published 31501); alpha.100 rows = 31502 (published 31502)
sdss_phot_flag counts {'0': 1296, '1': 28267, '2': 1371, '3': 567}; VizieR ReadMe {'0': 1296, '1': 28267, '2': 1371, '3': 567}; arXiv v1 text {'0': 1296, '1': 28057, '2': 1361, '3': 787}
rows with an SDSS objID = 29638 (flags 1+2 = 29638); arXiv v1 text quoted 29,418
hi_code counts {'1': 25434, '2': 6068} (published {'1': 25434, '2': 6068}); fraction code 1 = 0.8074 of 31502

## 2. HI widths and fluxes (alpha.100 rows)
W50 [km/s]: n=31502 median=174 p16=82 p84=302 min=9 max=885
  code 1: W50 n=25434 median=174 p16=80 p84=304 min=10 max=885
  code 2: W50 n=6068 median=175 p16=90 p84=291 min=9 max=861
S21 [Jy km/s]: n=31500 median=1.26 p16=0.72 p84=2.75 min=0.11 max=461.1 (excluding S21 <= 0 and the 999.9 placeholder)
SNR: n=31502 median=8.8 p16=6 p84=18.3 min=1.2 max=964
logMHI: n=31502 median=9.64 p16=9.08 p84=10.03 min=3.76 max=10.94
Vhel [km/s]: n=31502 median=7946 p16=4374 p84=1.242e+04 min=-430 max=1.782e+04; dist [Mpc]: n=31502 median=114.8 p16=63 p84=178.1 min=0.3 max=259.6

## 3. log M_HI = log10(2.356e5 D^2 S21) against the catalogue logMHI
rows checked = 31502; max |deviation| = 0.1462 dex at AGC 5470 (its distance rounding envelope is 0.169 dex); median = 0.0025; p99 = 0.0052; rows outside the rounding envelope (0.005 + 2|log10(1-0.05/D)| + |log10(1-0.005/S21)|) = 0
top 5 deviations: AGC 5470 +0.1462 (envelope 0.169); AGC 198305 -0.0379 (envelope 0.121); AGC 110007 +0.0364 (envelope 0.062); AGC 668 -0.0284 (envelope 0.069); AGC 227869 +0.0276 (envelope 0.043)
rows with D >= 10 Mpc and S21 >= 0.5 Jy km/s: n = 29886, max |deviation| = 0.0077 dex, median = 0.0025 dex
  (the catalogue publishes D to 0.1 Mpc, S21 to 0.01 Jy km/s and logMHI to 0.01 dex, so the identity can only be verified to that rounding)
S21 <= 0 rows (agc, S21, logMHI, W20): [('715637', '-7.61', '10.94', '0')]
S21 >= 900 rows (agc, S21, logMHI, D, Vhel): [('1117', '999.90', '8.20', '0.8', '-182')]
Haynes+2018 Eq. 5 for e_logMHI: median |deviation| = 0.0023, max = 0.0566 dex

## 4. optical columns
(g-i)_corr [mag], flag 1 rows: n=28267 median=0.62 p16=0.39 p84=0.94 min=-1.97 max=3.8
  flag 1 & HI code 1: n=22311 median=0.62 p16=0.39 p84=0.94 min=-1.79 max=3.8
  flag 1 & HI code 2: n=5956 median=0.62 p16=0.42 p84=0.94 min=-1.97 max=1.83
iMAG [mag], flag 1: n=28267 median=-19.83 p16=-21.49 p84=-17.8 min=-23.95 max=-10.01
i_cmodel [mag], flag 1: n=28267 median=15.77 p16=14.23 p84=17.13 min=9.58 max=20.67
b/a (SDSS expAB_r), flag 1: n=28267 median=0.57 p16=0.32 p84=0.82 min=0.05 max=1
logM*_Taylor, flag 1: n=28267 median=9.5 p16=8.61 p84=10.37 min=4.49 max=12.45; logM*_McGaugh: n=29298 median=9.75 p16=8.76 p84=10.57 min=4.4 max=11.94; logM*_GSWLC: n=14725 median=9.76 p16=9.02 p84=10.58 min=7.37 max=11.69
stellar-mass offset, median(logM_GSWLC - logM_Taylor) = +0.130 dex over 14663 rows (p16 +0.050, p84 +0.220); the table holds the raw method values
stellar-mass offset, median(logM_GSWLC - logM_McGaugh) = -0.140 dex over 14591 rows (p16 -0.280, p84 +0.010); the table holds the raw method values
iMAG definition check, iMAG = i_cmodel - iext - gamma_i*log10(a/b) - 5log10(D/Mpc) - 25: n = 28267, median |dev| = 0.0037, max = 0.0214 mag (rounding-limited)
gamma_i behaviour: rows with iMAG > -17: 2517, of which gamma_i = 0: 2517; rows with iMAG < -18: 23046, of which gamma_i > 0: 23046 (D20 eq. 1: gamma = 0 fainter than -17, rising linearly above)
derived optical columns present by flag (flag, iMAG present, Taylor mass present): ('', False, False): 2; ('0', False, False): 1296; ('1', True, True): 28267; ('2', False, False): 1371; ('3', False, False): 567

## 5. missing values per column (empty fields), of 31503 rows
  agc                     0
  in_durbala2020          0
  in_a100_table2          0
  name_oc             21115
  sdss_objid           1865
  sdss_phot_flag          2
  ra_dur_deg              2
  dec_dur_deg             2
  ra_hi_deg               1
  dec_hi_deg              1
  ra_oc_deg             345
  dec_oc_deg            345
  vhel_kms                0
  dist_mpc                0
  e_dist_mpc              0
  s21_jykms               1
  e_s21_jykms             1
  w50_kms                 1
  e_w50_kms               1
  w20_kms                 1
  snr                     1
  rms_mjy                 1
  hi_code                 1
  logmhi                  0
  e_logmhi                0
  gext_mag             1865
  iext_mag             1865
  ba_r                 1865
  e_ba_r               1865
  imag_cmodel          1865
  e_imag_cmodel        1865
  gamma_g              3236
  gamma_i              3236
  imag_abs_corr        3236
  e_imag_abs_corr      3236
  gi_corr              3236
  e_gi_corr            3236
  logms_taylor         3236
  e_logms_taylor       3236
  logms_mcgaugh        2205
  e_logms_mcgaugh      2205
  logms_gswlc         16778
  e_logms_gswlc       16778
  logsfr22             7608
  e_logsfr22           7608
  logsfr_nuvir        15389
  e_logsfr_nuvir      15390
  logsfr_gswlc        16778
  e_logsfr_gswlc      16778
rows with ALL of w50_kms, s21_jykms, hi_code, dist_mpc, logmhi, ba_r, gi_corr, imag_abs_corr, logms_taylor present: 28267 (HI code 1: 22311, code 2: 5956); these are exactly the sdss_phot_flag = 1 rows: True

## 6. oddities kept as published
W20 = 0: 11 rows; W20 < W50: 20 rows (of which W20 = 0: 11); e_dist = 0.0: ['2023', '5470', '198305']
hi_code 2 with SNR < 3: 15; e_ba_r > 1: 46; e_imag_cmodel > 1: 48
Vhel < 2000 km/s: 2019; Vhel > 6000: 22355; Vhel > 15000: 1235
SDSS objIDs shared by two AGC rows: 4 objIDs (8 rows); AGC pairs: 204290/208436; 729793/729803; 5183/5186; 7085/220172
alpha.100 rows without an optical counterpart position (ra_oc_deg empty): 344, all with sdss_phot_flag ['3']; flag-3 rows overall: 567
name_oc beginning 'VCC' (Virgo Cluster Catalogue designation, a partial Virgo indicator only): 151
most common (dist, e_dist) pairs, i.e. group / Virgo-substructure assignments (no flag column exists): 16.7+-1.2 x96; 16.6+-4.3 x65; 16.7+-1.3 x32; 16.4+-1.2 x31; 97.7+-4.3 x29; 24.2+-1.8 x26; 105.3+-4.3 x25; 100.5+-2.3 x23; 102.6+-4.2 x22; 99.4+-4.3 x21
distance recipe visibility, Vhel > 6000: 22095 of 22355 rows (0.988) have D within 5.5 Mpc of Vhel/70 (Hubble-flow rows D = cz_cmb/70 differ from Vhel/70 by the CMB-frame term, at most ~5.3 Mpc)
distance recipe visibility, Vhel <= 6000: 8152 of 9147 rows (0.891) have D within 5.5 Mpc of Vhel/70 (Hubble-flow rows D = cz_cmb/70 differ from Vhel/70 by the CMB-frame term, at most ~5.3 Mpc)
most common dist values: 16.7 x145; 16.6 x79; 24.2 x62; 102.6 x58; 105.3 x52; 102.9 x51; 97.7 x49; 101.8 x48; 16.4 x48; 11.1 x47
rows with 15 <= D <= 18 Mpc: 472; rows with D == 16.7 exactly: 145

## 7. cross-version checks
Durbala vs alpha.100 overlapping columns over 31500 shared AGC: differing rows per column = none (Vhel, Dist, e_Dist, logMHI, e_logMHI identical)
VizieR (rounded text) vs Cornell FITS (float64): max |FITS - CSV| per column, in units of the rounding half-step, and missing-pattern mismatches
  durbala2020-table1.21-Sep-2020.fits.gz: sdss_phot_flag: 0.000/0; sdss_objid: 0.000/0; ra_dur_deg: 0.000/0; dec_dur_deg: 0.000/0; vhel_kms: 0.000/0; dist_mpc: 0.000/0; e_dist_mpc: 0.000/0; gext_mag: 1.000/0; iext_mag: 1.000/0; ba_r: 1.000/0; e_ba_r: 1.000/0; imag_cmodel: 1.000/0; e_imag_cmodel: 1.000/0
  durbala2020-table2.21-Sep-2020.fits.gz: gamma_g: 1.000/0; gamma_i: 1.000/0; imag_abs_corr: 1.000/0; e_imag_abs_corr: 1.000/0; gi_corr: 1.000/0; e_gi_corr: 1.000/0; logms_taylor: 1.000/0; e_logms_taylor: 1.000/0; logms_mcgaugh: 1.000/0; e_logms_mcgaugh: 1.000/0; logms_gswlc: 1.000/0; e_logms_gswlc: 1.000/0; logsfr22: 1.000/0; e_logsfr22: 1.000/0; logsfr_nuvir: 1.000/0; e_logsfr_nuvir: 1.000/0; logsfr_gswlc: 1.000/0; e_logsfr_gswlc: 1.000/0; logmhi: 0.000/0; e_logmhi: 0.000/0
  largest ratio over all columns = 1.0000 (1.0 = exactly at the rounding boundary; the CSV text is the 2-decimal rounding of the FITS values everywhere)
VizieR alpha.100 vs Cornell a100.code12.table2.190808.csv: 31502 rows; numeric columns differing = none; max position differences (deg) HI RA 4.30e-05 Dec 8.00e-06, OC RA 4.30e-05 Dec 8.00e-06 (the Cornell decimal degrees are rounded; the VizieR sexagesimal is the original)
```
