# CFG287 open item: published journal PDFs vs the arXiv copies used (2026-10-02, data-release chat; owner's yes)
PDFs (now in ~/new_physics/_external_data/papers/, outside the repo; hashes in published_journal_pdfs_SHA256_2026-10-02.txt there; iopscience open-access PDFs, plain GET returned 200 application/pdf, no challenge): see SHA256.txt.
## RC100 (ApJ 944:78, doi 10.3847/1538-4357/aca9cf), Table B1 = the paper's Table 3, text layer parsed (-layout)
Compared logM_baryon, R_e, f_DM, V_c, sigma_0 for all 100 rows against rc100_nestorshachar2023_table3_CORRECTED.csv.
- All 12 value cells CFG287/the 09-29 provenance check corrected (rows 24, 36, 43, 44, 58, 62, 63, 65, 77, 90, 93, 95) match the PUBLISHED table. So the published table agrees with the corrected CSV there.
- NEW difference, published != CORRECTED csv (6 cells): row 87 J0901+1814 (lensed, z 2.26): published logMbar 10.72, Re 3.85, fDM 0.44, Vc 250, sigma0 37 (also dSFR -0.05, Mbulge 9.98, Mvir 11.89, SigmaSFR 0.63, SigmaDM 8.72) vs csv 11.09, 4.33, 0.06, 209, 55. The arXiv v1 raster image (p29) shows the csv values, so this is a genuine v1 -> published change for that one row (a refit). Effect on the csv's a0_Vc4/(G Mbar): 1.17e-10 -> 5.61e-10 (x4.8); g(Re)=Vc^2/Re 3.27e-10 -> 5.26e-10.
- Row 78 (BX610) sigma0: published 77 and the v1 image also 77; the csv (and the 09-29 paper-values file) have 75, a transcription error in both. (Not a v1->published change.)
- 4 rows (24, 47, 70, 93) have R_e/f_DM displaced in the text layer (they print as a trailing line); their values (4.93/0.02, 6.49/0.53, 7.61/0.74, 1.75/0.03) match the csv.
- Not compared: columns FWHM, T_int, dSFR, M*, Mbulge, Mvir, SigmaSFR, SigmaDM, names, z (z was compared only in the first parse of 91 rows). No erratum found on the IOP page.
## FS+18 (ApJS 238:21, doi 10.3847/1538-4365/aadd49), Table 6
sins_ao_table6_kinematics.csv: 38 rows x 10 central values (Re, sin i, PA, dPA, half-dv, Vrot, sigma0, Vrot/sigma0, Vc, Mdyn): every CSV value appears as a number in the published row text (membership test, not position-exact; errors not compared). 0 absent.
## Umehata+25 (ApJ 997:79, doi 10.3847/1538-4357/ae1a84; arXiv 2502.01868)
- Table 2 row ADF22.A7: position 22:17:32.20 00:17:35.68, S 2.03+-0.04: matches the repo.
- Table 4 (F444W) free-n row A7: n 3.21+-0.37, Re 2.24+-0.25, b/a 0.54+-0.06, PA 10.6+-1.2: matches the repo.
- Table 3 (ALMA 870 um, masked fits) row A7 DIFFERS from the repo's alma870_* values: published n 1.42+-0.36, Re 1.58+-0.15, b/a 0.435+-0.05, PA 17.9+-2.6 (unmasked 1.70, 1.45, 0.40, 18.4; Table C1 n=1: Re 1.30, b/a 0.42, PA 18.5). Repo (from arXiv v1, read via a WebFetch summary): n 1.01, Re 1.53+-0.15, b/a 0.58+-0.06, PA 17.4. Inclination arccos(b/a) 64.2 deg (published) vs 54.5 deg (repo). Circularized published Re = 1.58*sqrt(0.435) = 1.04 kpc, consistent with the ADF22-WEB III value 1.05+-0.12 noted in the repo. CFG284/285 used alma870_Re and axis ratio (used_in_cfg284 = yes).
