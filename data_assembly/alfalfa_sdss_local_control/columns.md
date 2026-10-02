# Data dictionary for `alfalfa_sdss.csv`

49 columns, 31,503 rows (one per AGC number). Missing value = empty field. Every value is the catalogue's own decimal text with padding stripped (no rounding added); the only computed values are the four sky-position pairs converted from sexagesimal.

How to read the references below:

* **D-RM** = the Durbala+2020 VizieR ReadMe, `<repo-parent>/_external_data/alfalfa_sdss/ReadMe` (J/AJ/160/271; sha256 in README.md). **H-RM** = the Haynes+2018 VizieR ReadMe, `.../ReadMe_Haynes2018_J_ApJ_861_49` (J/ApJ/861/49). The number after the colon is the line number in that file where the catalogue's own wording sits. The wording is paraphrased here (not copied); read the stored ReadMe for the verbatim text.
* **D20** = Durbala et al. 2020, AJ 160, 271 (arXiv:2011.02588v1). **H18** = Haynes et al. 2018, ApJ 861, 49 (arXiv:1805.11499). Section and column numbers are those papers'. Both PDFs were read for documentation only (see README.md, "Provenance").
* `n_missing` is out of 31,503 rows and comes from `python3 parse_alfalfa_sdss.py --checks`.

## 1. Identity and flags

| column | unit | source (table, label, bytes) | meaning | n_missing / notes |
|---|---|---|---|---|
| `agc` | - | all three tables, `AGC`, bytes 1-6 (D-RM:79, H-RM:120) | Entry number in the Arecibo General Catalog (a private database kept by the ALFALFA team). Numbers below 100,000 are UGC numbers (H-RM:161). If no optical counterpart was found the AGC number refers to the HI detection only (H18 Sect. 3.1 col. 1). Join key; unique in each table. | 0 |
| `in_durbala2020` | 0/1 | derived by the parser | 1 if the AGC number is in Durbala tables 1 and 2 (31,501 rows). | 0. Value 0 for AGC 116503 and 322050. |
| `in_a100_table2` | 0/1 | derived by the parser | 1 if the AGC number is in the Aug-2019 corrected alpha.100 table 2 (31,502 rows). | 0. Value 0 only for AGC 2023. |
| `name_oc` | - | alpha.100 `Name`, bytes 8-15 (H-RM:121) | Common name of the optical counterpart, free text from the AGC (for example `456-021`, `N 598`, `VCC  26`, `Eder Dw`). Padding stripped, interior spaces kept. Not standardised. | 21,115 (blank for 21,114 alpha.100 sources; AGC 2023 has no alpha.100 row). |
| `sdss_objid` | - | Durbala table 1 `ObjID`, bytes 10-29 (D-RM:81) | SDSS DR15 object identifier of the optical counterpart. The catalogue writes the int64 minimum (-9223372036854775808) where there is none; the CSV leaves those empty. | 1,865 = 1,296 outside the footprint + 567 no counterpart + 2 alpha.100-only rows. **Read as a string or nullable Int64; a float64 read destroys 19-digit IDs.** Four objIDs appear on two AGC rows each (AGC 204290/208436, 729793/729803, 5183/5186, 7085/220172) with positions up to degrees apart, so at least one ID of each pair is wrong. |
| `sdss_phot_flag` | 0-3 | Durbala table 1 `Flag`, byte 8 (D-RM:80, notes D-RM:97-104) | Photometry flag. 0 = outside the SDSS footprint (1,296 rows). 1 = SDSS photometry with g and i uncertainties below 0.05 mag, "good" (28,267). 2 = g and/or i uncertainty above 0.05, "bad" (1,371). 3 = inside the footprint but no SDSS counterpart identified (567). | 2 (the alpha.100-only rows). The derived optical columns of section 5 exist only for flag 1 (see below). |

## 2. Positions

| column | unit | source | meaning | n_missing / notes |
|---|---|---|---|---|
| `ra_dur_deg`, `dec_dur_deg` | deg | Durbala table 1 `RAdeg` bytes 31-40 (F10.6), `DEdeg` bytes 42-49 (F8.5) (D-RM:82-83, note D-RM:105-106) | J2000 position of the optical counterpart, or of the HI centroid when no optical counterpart was identified. | 2 each. As published (6 and 5 decimals). |
| `ra_hi_deg`, `dec_hi_deg` | deg | alpha.100 `RAh RAm RAs`, `DE- DEd DEm DEs`, bytes 17-31 (H-RM:122-128) | J2000 centroid of the HI line source, after the survey's systematic pointing correction (about 20 arcsec, H18 Sect. 3.1 col. 3). Converted: RA = 15 (h + min/60 + s/3600) with s to 0.1 s; Dec = sign (deg + arcmin/60 + arcsec/3600) with the sign taken from its own byte so that Dec between -1 and 0 is correct. Written with 6 decimals. | 1 each (AGC 2023). Agrees with the Cornell decimal-degree file to 4.3e-5 deg in RA and 8e-6 deg in Dec (that file is rounded). |
| `ra_oc_deg`, `dec_oc_deg` | deg | alpha.100 `RAOh ... DEOs`, bytes 33-47 (H-RM:129-135) | J2000 position of the most probable optical counterpart as recorded in the ALFALFA database (median offset from the HI centroid about 18 arcsec, H18 Sect. 3.1 col. 4). Converted as above. | 345 = 344 alpha.100 sources with no optical counterpart (all have `sdss_phot_flag` 3) + AGC 2023. |

## 3. HI measurements (alpha.100, Haynes+2018 table 2, Aug-2019 corrected version)

| column | unit | source | meaning | n_missing / notes |
|---|---|---|---|---|
| `vhel_kms` | km/s | alpha.100 `Vhel`, bytes 49-53 (H-RM:136-137); Durbala table 1 `RVel` bytes 51-55 (D-RM:84) | Heliocentric velocity of the midpoint of the HI profile (the mean of the two 50% crossing points of the profile horns), in the optical convention, observed frame (H18 Sect. 3.1 col. 5). Statistical uncertainty is half of `e_w50_kms`. The two tables agree on all 31,500 shared rows; the alpha.100 value is used, and the Durbala value fills AGC 2023. | 0 |
| `dist_mpc` | Mpc | alpha.100 `Dist`, bytes 91-95 (H-RM:148-149); Durbala `Dist` bytes 57-61 (D-RM:86) | Adopted distance, a Hubble-type distance, not a luminosity or comoving distance (H18 Sect. 3.1 col. 11). Recipe per H18: for heliocentric velocity above 6000 km/s, D = cz_cmb / 70 km/s/Mpc; below that, the Masters (2005) local flow model, replaced by published primary distances (secondary distances mainly from Tully+2013) where available, by the group systemic velocity for known group members, and by Virgo-substructure distances for objects in the Virgo region. **No column records which method was used.** See README.md for what can be inferred. | 0 |
| `e_dist_mpc` | Mpc | alpha.100 `e_Dist`, bytes 97-100 (H-RM:150) | Distance uncertainty from 1000 Monte Carlo draws of the peculiar velocity (H18 col. 11); the authors say it is likely an underestimate near major attractors such as Virgo. | 0. Value 0.0 on AGC 2023, 5470 (Leo I) and 198305 (Leo T). |
| `s21_jykms` | Jy km/s | alpha.100 `HIflux`, bytes 67-72 (H-RM:143) | Integrated HI line flux density S21: the source image integrated over the area inside the half-peak isophote, with a beam-pattern correction (H18 Sect. 2.5). No HI self-absorption correction. May underestimate very extended or asymmetric sources (H18 Sect. 2.5 and the Sect. 4 caveats). | 1 (AGC 2023). **Two invalid values kept as published:** AGC 715637 has -7.61 (its logMHI of 10.94 corresponds to +7.61); AGC 1117 (`N 598`) has the placeholder 999.90, and its logMHI of 8.20 follows from that placeholder. |
| `e_s21_jykms` | Jy km/s | alpha.100 `e_HIflux`, bytes 74-77 (H-RM:144) | Uncertainty in S21 (same procedure as for W50). | 1 |
| `w50_kms` | km/s | alpha.100 `W50`, bytes 55-57 (H-RM:138-139) | Full width of the HI profile at 50% of the peak, measured between polynomial fits to the two horns (fit range 15-85% of the peak, H18 Sect. 2.5). **Corrected for instrumental broadening only (Springob+2005 eq. 1); no correction for turbulence, disk inclination or cosmological stretch (H18 Sect. 3.1 col. 6 and the Sect. 4 caveats).** It is therefore the projected, uncorrected width. The ReadMe labels it "observed". | 1 (AGC 2023). Range 9 to 885. |
| `e_w50_kms` | km/s | alpha.100 `e_W50`, bytes 59-61 (H-RM:140) | Uncertainty in W50: statistical (S/N dependent) and a systematic part added in quadrature (H18 col. 6). | 1 |
| `w20_kms` | km/s | alpha.100 `W20`, bytes 63-65 (H-RM:141-142) | Same as W50 but at the 20% level; the fit is tuned for W50, so W20 is less robust (H18 col. 7). | 1. **Value 0 in 11 rows looks like a missing code** (the ReadMe range starts at 0); 20 rows have W20 below W50. Kept as published. |
| `snr` | - | alpha.100 `SNR`, bytes 79-83 (H-RM:145) | Signal-to-noise of the detection. The ReadMe calls it peak flux over rms; H18 eq. 4 defines it as (1000 S21 / W50) sqrt(w_smo) / rms with a smoothing width w_smo in 10 km/s bins, i.e. a profile-integrated S/N. Use the paper's definition. | 1 |
| `rms_mjy` | mJy | alpha.100 `rms`, bytes 85-89 (H-RM:146-147) | Noise of the extracted spectrum after Hanning smoothing to 10 km/s resolution, measured away from the signal and from interference. | 1 |
| `hi_code` | 1/2 | alpha.100 `HI`, byte 113 (H-RM:154, notes H-RM:162-165) | Detection category. 1 = 25,434 high-quality sources (matching signal in both polarisations, clean profile, S/N above about 6.5, with some softer cases admitted). 2 = 6,068 "priors": lower S/N (about 6.5 or less; 15 have S/N below 3) accepted because they coincide in position and velocity with a galaxy of known redshift. H18 says priors are not for statistical work that needs a defined completeness limit. | 1 (AGC 2023) |
| `logmhi` | log Msun | alpha.100 `logMHI`, bytes 102-106 (H-RM:151-152); Durbala table 2 `logMHI` bytes 113-117 (D-RM:145) | Log HI mass, M_HI = 2.356e5 D^2 S21 with D = `dist_mpc` (H18 Sect. 3.1 col. 12), optically thin, no self-absorption correction. The two tables agree on all shared rows; alpha.100 value used, Durbala fills AGC 2023. Re-computation reproduces it to the rounding of its inputs (README.md, check 3). | 0 |
| `e_logmhi` | dex | alpha.100 `e_logMHI`, bytes 108-111 (H-RM:153); Durbala `e_logMHI` bytes 119-122 (D-RM:147) | Uncertainty in log M_HI: flux error, 2 sigma_D / D and a 0.1 floor (10% flux-calibration allowance) added in quadrature, divided by ln 10 (H18 eq. 5; reproduced here to a median 0.002 dex). | 0 |

## 4. SDSS photometry and shape (Durbala table 1)

The SDSS object identifier is a DR15 one (D-RM:81); the ReadMe does not name the release for the magnitudes themselves. The catalogue provides **only the i-band cmodel apparent magnitude** among the observed magnitudes; there are no individual u, g, r or z magnitudes.

| column | unit | source | meaning | n_missing / notes |
|---|---|---|---|---|
| `gext_mag` | mag | table 1 `gext`, bytes 68-71 (D-RM:88-89, note D-RM:107) | Foreground Galactic extinction in g. Obtained from the Schlegel+1998 E(B-V) map with the R_V = 3.1 curve of Schlafly and Finkbeiner (2011), without their extra 14% recalibration; these equal the SDSS DR15 values (D20 Sect. 2.2). The authors adopt a 20% uncertainty on it. | 1,865 (flags 0 and 3, plus the 2 alpha.100-only rows). Present for flags 1 and 2. |
| `iext_mag` | mag | table 1 `iext`, bytes 73-76 (D-RM:90) | Same, i band. | 1,865 |
| `ba_r` | - | table 1 `b/a`, bytes 78-81 (D-RM:92) | Axis ratio b/a from the SDSS r-band exponential-profile fit (`expAB_r`, D20 Table 1 col. 11). **This is the only shape/inclination information; no inclination angle is given.** Range 0.05 to 1. | 1,865. Rounded to 0.01. |
| `e_ba_r` | - | table 1 `e_b/a`, bytes 83-88 (D-RM:93, note D-RM:108-110) | SDSS pipeline error on b/a; a few are absurdly large (up to 865; 46 rows above 1). The ReadMe says these are the pipeline's own values. | 1,865 |
| `imag_cmodel` | mag | table 1 `imag`, bytes 90-94 (D-RM:94) | SDSS **i-band cmodel magnitude, apparent, NOT corrected for Galactic or internal extinction** (the corrections are given separately; the identity in README.md check 4 confirms this). Not K-corrected. | 1,865 |
| `e_imag_cmodel` | mag | table 1 `e_imag`, bytes 96-103 (D-RM:95) | SDSS pipeline error on the cmodel magnitude; up to 42,134 mag (48 rows above 1 mag), as the ReadMe warns. | 1,865 |

## 5. Derived optical properties (Durbala table 2)

These are blank for `sdss_phot_flag` 0, 2 and 3 (g or i error above 0.05, or no photometry); D20 Sect. 2.2 excludes such galaxies from colour-magnitude and optical stellar-mass work. All 28,267 flag-1 rows have every column of this section.

| column | unit | source | meaning | n_missing / notes |
|---|---|---|---|---|
| `gamma_g`, `gamma_i` | mag | table 2 `Ag`, `Ai`, bytes 8-11 and 13-16 (D-RM:118-121, note D-RM:149) | The ReadMe calls these the "internal extinction factor". In the paper (D20 Sect. 2.2 eq. 1, Table 2 cols 2-3) they are the **coefficients gamma_lambda in A_lambda,int = gamma_lambda log10(a/b)**, with gamma = 0 for absolute magnitudes fainter than -17 and rising linearly with luminosity above (gamma_i = -0.15 M_i - 2.55, gamma_g = -0.35 M_g - 5.95, uncertainty 0.3). They are not extinctions until multiplied by log10(1 / `ba_r`). The correction is meant for blue, star-forming small and intermediate-mass galaxies, not for red-sequence or very massive ones. | 3,236. Range 0 to 1.91 (g) and 0 to 0.99 (i). The FITS names are `gamma_g`, `gamma_i`. |
| `imag_abs_corr`, `e_imag_abs_corr` | mag | table 2 `iMAG`, `e_iMAG`, bytes 18-23, 25-29 (D-RM:122-124, note D-RM:150-151) | Corrected absolute i-band magnitude: cmodel i, corrected for Galactic and internal extinction, with the adopted distance modulus. Reproduced from the table's own columns as `imag_cmodel - iext_mag - gamma_i log10(1/ba_r) - 5 log10(dist_mpc) - 25` to a median 0.004 mag (max 0.021, rounding-limited), so no K-correction term is present. | 3,236 |
| `gi_corr`, `e_gi_corr` | mag | table 2 `g-i`, `e_g-i`, bytes 31-35, 37-42 (D-RM:125-126) | Corrected (g-i) colour, Galactic and internal extinction removed. **Magnitude type is documented inconsistently:** the ReadMe Description (D-RM:44-46) and D20 (Sect. 2.2 and Table 2 col. 6) say the colours come from SDSS **model** magnitudes while absolute magnitudes use **cmodel**; the ReadMe note on table 2 (D-RM:150-151) says cmodel for both. This dictionary follows the paper (model). Cannot be checked from the tables because the model g and i magnitudes are not provided. | 3,236. Rounded to 0.01. Extremely large errors exist (up to 220 mag). |

## 6. Stellar masses and star-formation rates (Durbala table 2)

The three stellar-mass columns are raw outputs of three different methods. Where two exist the median offsets are median(logM_GSWLC - logM_Taylor) = +0.13 dex and median(logM_GSWLC - logM_McGaugh) = -0.14 dex, so the choice of column matters at the 0.1-0.3 dex level. D20 gives linear translations to GSWLC-2 masses (its eqs. 3 and 5) that remove the offsets; the table does not apply them. The initial mass function is not stated in the ReadMe.

| column | unit | source | meaning | n_missing / notes |
|---|---|---|---|---|
| `logms_taylor`, `e_logms_taylor` | log Msun, dex | table 2 `logMsT`, `e_logMsT`, bytes 44-48, 50-55 (D-RM:127-129, note D-RM:152) | Stellar mass from the optical colour method of Taylor+2011 (log M/L_i = -0.68 + 0.70 (g-i), D20 eq. 2), the "uncorrected" value (D20 Sect. 2.3). Available only for flag 1. | 3,236 |
| `logms_mcgaugh`, `e_logms_mcgaugh` | log Msun, dex | table 2 `logMsM`, `e_logMsM`, bytes 57-61, 63-66 (D-RM:130-132) | Stellar mass from unWISE W1 (3.4 micron) luminosity with M/L_W1 = 0.45, McGaugh and Schombert 2015 (D20 Sect. 3.1 eq. 4). Needs an unWISE match, not SDSS photometry quality. | 2,205 |
| `logms_gswlc`, `e_logms_gswlc` | log Msun, dex | table 2 `logMsG`, `e_logMsG`, bytes 68-72, 74-77 (D-RM:133-135) | Stellar mass from the GALEX-SDSS-WISE Legacy Catalog 2 SED fits (Salim+2016, 2018), where the galaxy is in that catalogue (about 47% of rows). | 16,778 |
| `logsfr22`, `e_logsfr22` | log Msun/yr, dex | table 2 `logSFR22`, `e_logSFR22`, bytes 79-83, 85-88 (D-RM:136-138, note D-RM:153) | Star-formation rate from the unWISE 22 micron (W4) flux with the Kennicutt and Evans 2012 conversion, using the adopted distance (D20 Sect. 3.2 eq. 7). The paper warns it underestimates SFR for low-SFR, low-mass galaxies. | 7,608 |
| `logsfr_nuvir`, `e_logsfr_nuvir` | log Msun/yr, dex | table 2 `logSFRN`, `e_logSFRN`, bytes 90-94, 96-100 (D-RM:139-141); FITS name `logSFRNUVIR` | The ReadMe describes this as an SFR from GALEX NUV photometry. The FITS name and D20 (Sect. 3.2 eq. 9, Table 2 col. 16) show it is the **NUV rate corrected with the 22 micron flux** (the paper judges it the most reliable of the three, and says uncorrected NUV is not included in the catalogue). | 15,389 for the value, 15,390 for its error (one row has a value without an error). |
| `logsfr_gswlc`, `e_logsfr_gswlc` | log Msun/yr, dex | table 2 `logSFRG`, `e_logSFRG`, bytes 102-106, 108-111 (D-RM:142-144) | SFR from GSWLC-2, where available. | 16,778 |

## 7. What the catalogue does NOT contain

Content one might expect for a local control sample, but absent from every table fetched:

* Individual SDSS u, g, r, z magnitudes (apparent or absolute), model or Petrosian magnitudes, or any g-r or other colour besides corrected g-i. Only i-band cmodel (apparent) and the corrected iMAG and g-i exist.
* Optical size or half-light radius (R50), surface brightness, morphology, or an inclination angle (only the r-band axis ratio exists).
* Any distance-method or flow-model flag, and any cluster, group or Virgo membership flag (a partial proxy: 151 rows have `name_oc` starting `VCC`, and a distance spike at 16.7 Mpc; see README.md).
* HI-profile shape measures (asymmetry, peak flux, W_mx or any inclination- or turbulence-corrected width), the CMB-frame velocity, and SDSS spectroscopic redshifts or flags.
* The HI spectra (the 1 GB ALFALFA spectra archive was not fetched).

## 8. Reading the CSV

```python
import pandas as pd
df = pd.read_csv("alfalfa_sdss.csv", dtype={"sdss_objid": "string", "name_oc": "string"})   # empty fields -> NaN / <NA>
```

`sdss_objid` must not be read as float64. The file is UTF-8 with LF line endings, 31,503 data rows after one header line.
