# DESI DR1 Milky Way Survey radial velocities for our wide-binary pairs: Phase A (data front, 2026-09-30)

Request (orchestrator, for my user): find the public DESI DR1 MWS stellar catalogue, its files, sizes, columns, RV precision, whether a subset or server-side cross-match avoids the full file, and how many of our 12,420 components could be in the footprint. Phase A is read-only: **no data file was downloaded.** What was read: directory index pages on data.desi.lbl.gov, HTTP HEAD, and small HTTP byte-range reads of FITS HEADERS and 41 sample rows of the big file (a few hundred kB in total, not kept), plus the published paper and data-model pages (summariser level, marked where unverified).

## 1. The catalogue and its files (DR1 = spectroscopic production `iron`)
Root: `https://data.desi.lbl.gov/public/dr1/vac/dr1/mws/iron/v1.0/` (README points to https://data.desi.lbl.gov/doc/releases/dr1/vac/mws/; data model https://desi-mws-dr1-datamodel.readthedocs.io; paper: DESI DR1 Stellar Catalogue, arXiv:2505.14787).
| file | size | content |
|---|---|---|
| `mwsall-pix-iron.fits` | **13,051,186,560 B (13.05 GB)**, sha256 eae3b31807c58ac340c257e06f66935d01bb81698a08108e6ca57a372cab76b5 | the merged catalogue: 6 HDUs, **6,372,607 rows** (one per coadded spectrum; the paper states 5,930,124 primary/unique objects, 4,378,110 of them stars by Redrock, 10,012,925 single-epoch spectra); the server sends `Accept-Ranges: bytes` |
| HDU RVTAB | 259 B/row, 37 columns, **1.65 GB** | VRAD, VRAD_ERR, VRAD_SKEW, VRAD_KURT, LOGG, TEFF, ALPHAFE, FEH (+ errors), VSINI, CHISQ_*, **RVS_WARN**, **REF_ID** (Gaia source id, REF_CAT 2 chars, 'G2' in the rows sampled), TARGET_RA, TARGET_DEC, TARGETID, SN_B/R/Z, SUCCESS, RR_Z, **RR_SPECTYPE**, **HEALPIX** (nside 64 nested), SURVEY, PROGRAM, **PRIMARY** |
| HDU SPTAB | 556 B/row, 22 columns, 3.54 GB | FERRE stellar parameters |
| HDU FIBERMAP | 421 B/row, 80 columns, 2.68 GB | TARGETID, TARGET_RA/DEC, MEAN_FIBER_RA/DEC, fibre status |
| HDU SCORES | 172 B/row, 42 columns, 1.10 GB | spectral scores |
| HDU GAIA | 640 B/row, 153 columns, 4.08 GB | **SOURCE_ID (Gaia DR3, int64 at byte 36)**, RA, DEC, PARALLAX, PMRA, PMDEC, PHOT_G/BP/RP_MEAN_MAG, RUWE, RADIAL_VELOCITY and its error |
| `rv_output/240520/rvpix-<survey>-<program>.fits` | main-bright 4.22 GB, main-backup 1.67 GB, main-dark 1.87 GB, sv1 (backup/bright/dark) 85/64/59 MB, special, cmx (kB-MB) | the same RV tables by program; `rv_output/240521/rvpix_exp-*` are the per-exposure tables (main-bright 5.65 GB, main-backup 3.40 GB, main-dark 2.87 GB) |
| **per-pixel files** `rv_output/240520/healpix/<survey>/<program>/<hpx//100>/<hpx>/rvtab_coadd-<survey>-<program>-<hpx>.fits` (+ `rvmod_coadd-*`) | rvtab **66 kB to ~0.65 GB-scale is NOT the case: 66-657 kB in the 50 files sampled** (rvmod spectra models are 1-25 MB and not needed) | one small RV table per sky pixel and program |
| `sp_output/230211/...` | (FERRE products) | not needed |
The table is **not sorted by pixel** (HEALPIX jumps in a sample of 41 rows), so a row range for our pixels cannot be found by bisection. A FITS row-major table also means a column subset still costs the whole HDU.

## 2. Columns that matter and the documented RV quality
- Match key: **Gaia DR3 SOURCE_ID is only in the GAIA HDU (4.08 GB)**; RVTAB carries REF_ID (the Legacy-Surveys reference Gaia id, 'G2' = DR2 in the sampled rows) plus TARGET_RA/DEC. For the pixel, **DESI HEALPIX = Gaia source_id >> 47 exactly** (verified on 8 DESI rows), so pixels of our components need no sky positions.
- Documented precision (paper, arXiv:2505.14787, summariser level): systematic floor **1.0 km/s (bright program), ~2 km/s (backup, non-Gaussian), 1.6 km/s (dark)**; median random error better than 1 km/s; recommended cuts `RR_SPECTYPE = STAR`, `RVS_WARN = 0`, `VSINI < 30 km/s` (plus `BESTGRID != 's_rdesi1'` for the FERRE side); stars span G ~12 to ~21, the bright program observes 16 < r < 19, the backup program reaches G = 19 from about G = 11 (`PRIMARY` marks the best observation of repeats).
- Scale of the signal we care about: the pairs in `wide_binaries_dr3.csv` have a median projected relative velocity **v_perp = 0.30 km/s (16th-84th: 0.14-0.56, max 1.5)** at median separation 3.6 kAU (2.4-7.3) and median distance 166 pc. **DESI's 1-2 km/s floors are several times larger than that, so a DESI radial velocity cannot measure the orbital velocity difference of one pair; it can reject contaminants (|delta RV| well above ~3 km/s: chance alignments, triples, unbound pairs) and supply a missing line-of-sight velocity.**

## 3. Ways to avoid the 13 GB (for Phase B)
1. **Per-pixel route (cheapest):** fetch `rvtab_coadd-main-bright-<hpx>.fits` and `...-main-backup-<hpx>.fits` only for the pixels that hold our window stars (section 4): **547 bright + 615 backup = 1,162 files, about 0.3 GB** (sampled mean 279 kB bright, 232 kB backup; an estimate from 25 files each). Whether these rvtab files carry REF_ID/TARGET_RA/DEC and the quality flags was not checked (needs one file).
2. **One HDU by byte range:** RVTAB alone is 1.65 GB (byte range 2,880 to 1,650,508,093 after the headers, offsets measured), holds REF_ID, TARGET_RA/DEC, VRAD, VRAD_ERR, RVS_WARN, SN, RR_SPECTYPE, PRIMARY, but REF_ID is a DR2-type reference id, so the Gaia DR3 id must be confirmed by position or by reading the 640-byte GAIA row of each match (one small range request per match).
3. **The whole file** (13.05 GB) or the GAIA HDU (4.08 GB) only for a direct DR3 source_id match: not needed.
4. **Server side:** NOIRLab Astro Data Lab hosts `desi_dr1` tables (`zpix`, cross-matched to Gaia DR3 within 1.5 arcsec, TAP at https://datalab.noirlab.edu/tap), but DESI's own documentation says the databases do **not** include most VACs, so **the MWS RVs (VRAD) are not there**; only Redrock redshifts, which are not MWS-grade stellar RVs. A TAP cross-match would tell which of our stars DESI observed at all, but it sends our Gaia ids to a third party and was not done.

## 4. How many of our components could be in the MWS (computed; `desi_mws/footprint_estimate.py`, results `footprint_estimate*.json`)
Method: my 12,420 components (6,210 pairs) carry Gaia ids; G, ra, dec and the Gaia RVS value come from the local Gaia chunks (all 12,806 ids of both pair files found); the list of nside-64 pixels that have DESI MWS per-pixel RV files was built from the directory indexes only (`crawl_index.py`, about 1,000 index pages; `desi_mws_pixels_by_survey_program.json`: main-bright 13,851 pixels, main-backup 4,726, main-dark 13,348, plus sv1/sv2/sv3/special/cmx). **A pixel with a file is necessary, not sufficient: DESI observed only part of each pixel's targets, and that completeness is not known here, so every count is an upper limit.**
| quantity (wide_binaries_dr3.csv) | components | pairs with both |
|---|---|---|
| our components / pairs | 12,420 | 6,210 (5,682 distinct pixels) |
| in a pixel with main-bright files | 5,075 | 2,535 |
| in a pixel with main-backup files | 1,409 | 703 |
| in any main-program pixel (bright, backup, dark) | 6,064 | 3,031 |
| in any DESI DR1 MWS pixel (all surveys) | 6,293 (51%) | 3,145 |
| G 16-19.2 in a main-bright pixel (the bright-program window) | 574 | 13 |
| G 11-19.2 in a main-backup pixel (the backup window) | 1,067 | 403 |
| in either window | 1,523 | 414 |
Our sample is **bright**: G median 13.45 (16th-84th: 10.3-15.7), none fainter than 19.2, 2,876 brighter than 11 (too bright for the MWS and Gaia already has RVs for 1,333 of those in DESI pixels).
What DESI could add: **9,769 components (79%) already have a Gaia DR3 RVS velocity**; 2,651 lack one, and **only 723 of those lie in a DESI window** (1,271 in any main-program pixel). Pairs with both RVs from Gaia alone: 3,746; if DESI supplied every window star, at most **4,425 pairs** would have both (a gain of up to ~680 pairs, plus independent repeats for up to ~1,500 components). The El-Badry-variant file `wide_binaries_dr3_elbadryR.csv` (6,230 pairs, 12,460 components) gives nearly identical numbers (1,518 components in the windows, 420 pairs; the full El-Badry+21 catalogue is not on disk).
Possible upside not counted: the MWS also targets nearby stars (I recall a ~100 pc class; unverified); 1,775 of our components have parallax > 10 mas and 887 of them sit in a main-program pixel.

## 5. What this means, and what needs my user's go
The DESI RVs add a line-of-sight velocity for at most a few hundred to ~700 components Gaia lacks, and their precision cannot test the orbital velocity difference, so the main use is **contaminant and triple rejection and filling ~680 pairs with RVs**. The cheapest download is the per-pixel route: **~1,162 small files, ~0.3 GB (estimated)**; the next is RVTAB (1.65 GB) by byte range; the full file is 13.05 GB. **Any download needs my user's go in this chat.**
