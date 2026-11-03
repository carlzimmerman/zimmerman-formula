# LAM2 amendments, dated, written before any count

`FROZEN_CRITERIA.md` (fa14da563a) is unedited. kappa = 1/2 FITTED. Not theory closed.

## 2026-11-03, A1: stage-0 query, EW sign, repeat observations (owner approved the query)
- **Query:** `lam2_fetch.py`, SkyServer DR17 SqlSearch, 23 chunks of up to 250 specobjid, 746,943 bytes in `_external_data/lam2_sdss_lines_2026_11_03/`. 5811 matched DynPop rows map to 5730 distinct specobjid; all 5730 returned, 5681 with a galSpecLine row.
- **EW sign, checked before any cut:** the three highest-S/N H-alpha emitters (plate-mjd-fiber 2636-54082-321, 349-51699-402, 630-52050-245; flux S/N 168-186) have h_alpha_eqw of -21.8, -29.8 and -93.0 A. Negative means emission. The gas-poor cut is therefore **-h_alpha_eqw < 3 A**. Small negative values at zero flux (about -0.1 to -0.3 A) fall inside it.
- **Repeat observations:** 157 DynPop rows share a specobjid with another row. They are the same galaxy (same mangaid) observed twice by MaNGA. One row per mangaid is kept: highest Qual, then the first row in file order. The slow label comes from that row. Duplicates are counted and reported.
- **Galaxies without a galSpecLine row** are excluded from both samples and counted, as frozen.
- **F2 counts:** Hanley-McNeil uses the gas-poor quality sample's slow and fast counts, and all of them, because all scores are out of fold.

## 2026-11-03, A2: wave 1 and the fit's operational details, before the full fit (owner approved wave 1)
- **pPXF 9.5.2** (pip, with capfit 2.7.1). **Templates:** `spectra_emiles_9.0.npz` from github micappe/ppxf_data, 13,370,634 B, sha256 6a1b1a70db4d95f67afe0adbe254f111eb2b50412b9f311714c54ffba18c6f0e, in `_external_data/lam2_templates_2026_11_03/`. 25 ages x 6 metallicities, FWHM 2.51 A over 3900-7400 A, finer than SDSS (about 2.65 A rest frame), so templates are broadened to each galaxy's `wdisp`.
- **Spectra:** `lam2_get_spectra.py`, DR17 spec-lite for the 3324 rows of `lam2_sample.csv` (written by `lam2_stage0.py`, whose printed output is unchanged). run2d from SpecObj: 3138 at 26 (sdss/spectro/redux/26), 186 at v5_13_2 (eboss/spectro/redux/v5_13_2).
- **Fit details** (`lam2_fit.py`), not in the criteria: rest frame from the file's SPECOBJ Z; flux divided by its median; pixels with ivar = 0 or and_mask != 0 are masked; sky lines masked +-5 A observed; templates built over 3500-7300 A, normalised over 5070-5950 A; start [0, max(VDISP, 80)] km/s; errors are pPXF formal errors x sqrt(chi2). Fit failures are written as error rows and counted, never refit.
- **Seen before this amendment:** a 20-spectrum test (first 20 rows of the sample) to check speed and memory. All 20 converged; sigma 101-304 km/s, h4 errors 0.02-0.06, chi2 0.72-0.96. No lambda label was compared with any fit output. Restricting the templates to 3500-7300 A changed no test value. Memory is measured as macOS peak physical footprint (672 MB), as in NP2's A3, because RSS counts freed pages (4.1 GB).
- **ATLAS3D:** VizieR timed out twice. The external test runs only once the positions table arrives; until then it is reported as NOT RUN.

## 2026-11-03, A3: grading details, before any real grade (`lam2_grade.py`, `lam2_k2.py`)
- **K1** "rms <= 0.06 dex" is read as rms of log10(sigma_pPXF / velDisp) about zero (the stricter reading); the median is reported too.
- **Features:** log M* = log10(nsa_sersic_mass) + 0.310; u-r = NSA Sersic absmag u - r; R_e in kpc = Re_arcsec_MGE x DynPop `DA` (Mpc, median 168 at z 0.04). DA and the NSA masses come from Omega_m = 0.3 catalogues; at z near 0.04 they enter only as classifier features, never as a science input, as in LAM1's STAGE0. MPA-JHU values of -999 or below and non-finite values count as missing. A galaxy missing any B, P or S input is dropped from all four models, so every model sees the same galaxies; drops are counted.
- **Bootstrap:** 1000 paired draws over galaxies of the out-of-fold scores; a draw with no slow or no fast galaxy is skipped.
- **M1:** 27 cells from terciles of log M*, log velDisp and Eps_MGE over the gas-poor graded sample; (h4, h6, sigma ratio) permuted together within each cell; S refit with the same folds and seed. Output `lam2_grade_MUTATE.*`.
- **Permutation importance:** one S input shuffled over the gas-poor sample, S refit out of fold, AUC drop reported.
- **Label order:** K1 or M1 fail gives NO VERDICT, then K2 fail gives h4 NOT MEASURABLE, then E3, then E4, then E1 or E2 (either failing gives KINEMATIC AXIS, TOO NOISY TO LABEL). A label printed while K2 or M1 has not run is marked PROVISIONAL.
- **K2:** the synthetic LOSVD is built by pPXF itself (the galaxy's best-fit template mix, fixed V = 0, sigma, h4, degree -1), normalised to median 1, plus Gaussian noise from the galaxy's noise vector. A one-spectrum smoke test recovered h4 = -0.08, 0, +0.08 exactly without noise and as -0.081, -0.011, +0.058 with noise. That run used no lambda label.
- **DRYRUN mode**, a code test only: lambda_Re, Eps_MGE and the slow flag are permuted across galaxies, outputs go outside the repo. It was run once on the first 69 fits. Because K1 does not use labels, it printed real K1 values for 56 gas-poor galaxies: median +0.006 dex, rms 0.021. No real-label AUC has been computed. DRYRUN is rerun on the full fits before the real grade.
- The `matmul` RuntimeWarnings printed by numpy 1.26 on macOS Accelerate are spurious; fits are unchanged and the warnings are filtered from logs only.
