# BUDHIES power pre-flight inputs: Abell 963 and Abell 2192 (data front, 2026-09-29)

Request (calculation thread): for each cluster, centre, redshift, mass (M500/M200 with errors, R500/R200), velocity dispersion, the survey's projected extent, per-galaxy cluster-centric distances, and the form of the HI detection limit. No W50 was opened. **No file was downloaded.**
Method: arXiv HTML/abstract pages read on 2026-09-29 through a page summariser (wording is the summariser's, not checked against the pages verbatim; **every value is UNVERIFIED until read in the PDF**). Nothing is from memory. Two PDF reads failed (Okabe & Smith 2016, arXiv:1507.04493, and Haines+2018 PDF; the binary was too large or unparsed), so items marked NOT OBTAINED are open.

## 1. Cluster properties as quoted by the BUDHIES papers
| quantity | Abell 963 | Abell 2192 | source |
|---|---|---|---|
| redshift | 0.206 | 0.188 | BUDHIES IV (arXiv:2302.12197) Table 1; pilot arXiv:0708.3853 |
| sigma (km/s) | 993 (BUDHIES IV, citing Jaffé+2016) | 653 (BUDHIES IV, citing Jaffé+2012); 530 ± 56 for the main substructure A2192_1a (Jaffé+2013 Table 1) | 2302.12197 Table 1; arXiv:1207.2767 Table 1 |
| sigma, pilot paper | **1350** | 650 | arXiv:0708.3853 (older value; **conflicts with 993**) |
| total mass (as quoted) | 1.4e15 Msun (Jaffé+2016) | 2.3e14 h^-1 Msun (Jaffé+2012) | 2302.12197 Table 1; **not M200/M500**, definition not stated on the page read |
| M200 (A2192_1a substructure) | | 2.27e14 Msun; R200 = 1.16 Mpc | arXiv:1207.2767 Table 1 and Sec. III.2 |
| R200 | 3 Mpc (pilot paper) | 1.5 Mpc (pilot paper) | arXiv:0708.3853; **conflicts with 1.16 Mpc for A2192_1a** (a different object: the main substructure, not the whole cluster) |
| L_X (erg/s) | 3.4e44 (Haines+2018) | 7e43 (Voges+1999, RASS) | 2302.12197 Table 1. Haines+2018 Table 1 itself lists 6.390e44 (ROSAT 0.1-2.4 keV): **two different L_X values for A963** (band/aperture not stated) |
| M200 X-ray | 8.92 ± 2.01 e14 Msun | | Haines+2018 (arXiv:1709.04945) Table 1, citing Martino+2014 |
| M200 weak lensing | 9.90 ± 1.79 e14 Msun | | same table, citing Okabe+2016 |
| M500, R500 | **NOT OBTAINED** (Okabe & Smith 2016, arXiv:1507.04493, is the likely table; PDF unparsed) | not in any page read; A2192 is only weakly detected in X-rays | |

Points for the power line: A963's dispersion is quoted as 993 or 1350 depending on paper, and its X-ray mass is 8.9e14 (M200), against 1.4e15 "total" in BUDHIES IV: an M200 for the external-field estimate spans roughly a factor 1.6 by source. A2192 has no X-ray mass on any page read, and only a dynamical/substructure mass.

## 2. Centres
| cluster | RA, Dec (J2000) | what it is | source |
|---|---|---|---|
| A963 | 10h17m14.22s, +39d01m22.1s | BUDHIES IV Table 1; the definition (BCG / X-ray peak / centroid) is **not stated on the page read**. The pilot paper describes the X-ray contours as centred on a central cD | 2302.12197 Table 1; 0708.3853 |
| A2192 | 16h26m36.99s, +42d40m10.1s | "centred on the cluster proper" (BUDHIES IV); the substructure paper gives 246.64774, +42.727723 deg = 16h26m35.5s, +42d43m39.8s, **"luminosity-weighted geometric centre"** (Table 1 footnote) | 2302.12197 Table 1; arXiv:1207.2767 Table 1 |
| WSRT pointing | A963 pointing is on 4C +39.29, 2.4 arcmin south-east of the cluster core | | 2302.12197 Sec. 3 |

The two A2192 centres differ by about 3.5 arcmin (my arithmetic from the two quoted positions; not a paper value).

## 3. Survey extent and HI limit
- Primary beam FWQM 61 arcmin at 1190 MHz; "7.09 < FWQM < 9.55 Mpc" across the redshift range (BUDHIES IV Sec. 3). The pilot paper says observations cover "4 Mpc from the cluster centers in the plane of the sky"; Jaffé+2013 says "~12x12 Mpc" per cluster. **Three different extents** quoted (4 Mpc, 7-10 Mpc FWQM, 12x12 Mpc); the FWQM statement is the newest.
- Spectral range 0.16427 < z < 0.22449 (Sec. 3); total volume 73,400 Mpc^3 (abstract).
- Detection limit is stated as an **HI mass**: "minimum detectable HI mass of 2e9 Msun at the field centres at their respective cluster redshifts over ~150 km/s, S/N 4 in each of three adjacent spectral resolution elements" (Sec. 3). The pilot abstract quotes 8e8 Msun for the final survey and detections 5e9-4e10 Msun (arXiv:0708.3853; older, differs). A column-density limit is also stated: 0.91e19 cm^-2 (A963), 1.1e19 cm^-2 (A2192) at 5 sigma (Sec. 3.7.2). The mass limit rises away from the field centre with the primary beam; that profile is not on the page read.
- **No per-galaxy cluster-centric distance or membership column** in the catalogues (BUDHIES IV Tables A1-A4, as read): only RA, Dec, so distances have to be computed from the centres in Sec. 2. Membership flags are in the earlier Gogate+2020 tables held in `high_z_tf_tables/` (not re-checked here).

## 4. Open items, all for the calc thread's decision
1. A963 M500/R500 not obtained; would need reading Okabe & Smith 2016 or Martino+2014 tables from the PDF.
2. The centre choice for A963 is undefined on the pages read; the two A2192 centres differ by ~3.5 arcmin.
3. sigma (1350 vs 993) and L_X (6.39e44 vs 3.4e44) conflicts for A963 are between papers; a choice is needed before any external-field estimate, made on input-side grounds only.
