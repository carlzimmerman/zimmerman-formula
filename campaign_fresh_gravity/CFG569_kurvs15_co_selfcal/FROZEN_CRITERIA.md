# CFG569 FROZEN CRITERIA: KURVS-15 (cdfs_31127, z_Halpha = 1.613) archival ALMA CO -> measured gas shape -> CFG385 self-calibrated a0 fit. ONE GALAXY = A DEMONSTRATION, never a verdict on a0(z)

Written 2026-10-09, before any ALMA cube is downloaded or read, and committed alone first. kappa = 1/2 is FITTED; both a0 footings are carried (9.3603e-11 / 1.1312e-10 m s^-2); no dark-matter particle (the cold mass is still required); a pass here would not favour the framework over LCDM.

## 0. Inputs
- **ALMA (owner-approved download, the minimum set only; ~6.6 GB):** to `campaign_fresh_gravity/_external_data/cfg569/` (git-ignored); every fetch logged in `FETCH_LOG.md` (URL, date, bytes, sha256). From `data_assembly/alma_archive_footprint/kurvs15_product_file_list.csv`:
  - Molina 2019.1.01238.S, Band 3 spw23 repBW `...X1465_X137f.CDFS_31127_sci.spw23.repBW.I.pbcor.fits` + `.pb.fits.gz` (CO(2-1), 0.11" class; resolved structure);
  - Ibar 2018.1.00164.S Band 3 spw29 `...X133d_X7a8...spw29.cube.I.pbcor.fits` + `.pb.fits.gz` (CO(2-1), 2.48" beam; the PRIMARY total flux);
  - Ibar Band 6 spw29 `...X133d_X7ac...spw29.cube.I.pbcor.fits` + `.pb.fits.gz` (CO(5-4), reported only);
  - continuum tt0 (small): Ibar B3 `cont.I.tt0.pbcor` + `cont.I.pb.tt0`, Molina `cont.I.tt0.pbcor` (39 MB) — header/astrometry sanity only.
  - NOT fetched: the 28.8 GB full-resolution Molina cube, any raw/ASDM tar. Pre-download gate: free disk >= 30 GB, else abort; throughput measured on a small file first; if the projected total exceeds ~6 h, only the Molina repBW pair is fetched first and reported.
- **Record (read-only):** `data_assembly/arxiv_tables/kurvs2023_*.csv` (KURVS-15: z 1.613, logM* 10.07, R_e 3.8 kpc, i_SFR 38 deg, i_star 65 deg, sigma0 68 +- 4 km/s, R_Halpha,max 9.2 kpc, V(R_max) 112.2 km/s); `kurvs_rc_profiles/kurvs_rc_points.csv` (22 observed markers, both sides) and `kurvs_rc_model_curves.csv`; `kurvs_positions/kurvs_positions.csv` (RA 53.070583, Dec -27.834461); KURVS PSF FWHM 0.57" (CFG184). Kernels: `CFG44_fluid_target/Bcommon.py` `nu_mono` (primary, owner decision 09-26) and `nu_p2` (reported), imported read-only; the exp-RAR kernel g = g_bar / (1 - exp(-sqrt(y))) is also reported.
- **The record has NO disc position angle for KURVS-15.** Declared: the PA is measured from the Molina CO moment-0 flux-weighted second moments inside the detection aperture (only if CO is detected there); the inclination is i_SFR = 38 deg (the record's deprojection choice) primary, i_star = 65 deg reported.

## 1. Pre-data expectation (recorded now, from CFG163's power row)
CFG163 found that the archival CO cubes reach only mu_mol >~ 5.5 for a 4-sigma detection, and its 1.32-mm dust non-detection limits the dust-traced gas to < 1.90 M* (nominal). **The expected outcome is "CO not detected", hence no measured gas shape, hence NO a0 number.** The KURVS seeing (0.57" = 4.8 kpc FWHM) also makes the inner Halpha points beam-smeared, so the expected g_obs span outside the PSF half-width is ~2x, well short of CFG475's 6.4x and CFG385's y >~ 3 -> <~ 0.3. Both are expectations, not results.

## 2. Header / data sanity (controls H1-H4; failures kept)
- H1: each cube's spectral axis covers the line: CO(2-1) nu_obs = 230.538/2.613 = 88.228 GHz (Band 3), CO(5-4) = 576.268/2.613 = 220.540 GHz (Band 6); the window +-300 km/s lies wholly inside the spw.
- H2: beam keywords (BMAJ/BMIN/BPA) present (or a per-channel beam table); the record's beam class reproduced (Ibar B3 ~2.5", Ibar B6 ~1.0", Molina ~0.1-0.2").
- H3: the KURVS-15 position lies inside the map with pb >= 0.9.
- H4: units Jy/beam; channel width read from the header; velocity axis built in the radio convention relative to the line's nu_obs.

## 3. CO detection criterion (D)
- **Moment-0:** sum over channels within +-300 km/s of z = 1.613 (primary); +-200 km/s reported. Units Jy/beam km/s.
- **Ibar Band 3 (PRIMARY total flux):** S_CO = the mom0 value at the KURVS-15 pixel (the galaxy, R_Halpha,max 9.2 kpc = 1.1", is smaller than the 2.48" beam; flux = peak, an underestimate of <~10% for a source of ~1" size, disclosed). A 2.0"-radius aperture sum / beam-area-in-pixels is reported.
- **Molina Band 3:** a 1.2"-radius circular aperture sum / beam-area-in-pixels at the position.
- **Noise (both):** the SAME statistic (pixel value or aperture sum) measured at >= 50 off-source positions with pb >= 0.5, centres >= 3" (Ibar B3: >= 6") from the source and non-overlapping where possible; sigma = 1.4826 x MAD. Integrated S/N = statistic / sigma.
- **Detection: integrated S/N >= 5** (primary window). 3 <= S/N < 5 = "tentative" (no gas shape used). S/N < 5 = not detected; a 3-sigma upper limit on S_CO and on M_mol (below) is reported.
- **Line-free check (control N1):** mom0 maps of equal width built from line-free windows in the same spw (centres >= 600 km/s from the line, not overlapping the spw edges' 5% channels): the statistic at the source position in each, divided by sigma, must have |median| < 1.5 and a scatter of order 1 (0.5-2). Failure kept and disclosed.
- **Injection (MUTATE_B, always run):** a model line S = 0.5 Jy km/s (Gaussian in velocity, FWHM 300 km/s; spatially the beam) injected into the Ibar B3 cube at the source position must read "detected" with recovered flux within 30%; exit 1 if not.
- Band 6 CO(5-4): same Ibar statistic; reported only (excitation unknown), never used as gas mass.

## 4. Conversion
L'_CO(2-1) = 3.25e7 S_CO dv nu_obs^-2 D_L^2 (1+z)^-3 (K km/s pc^2; S in Jy km/s, nu in GHz, D_L in Mpc, astropy Planck18). L'_CO(1-0) = L'_CO(2-1) / r21, **r21 = 0.77** declared. **M_mol = alpha_CO L'_CO(1-0), alpha_CO = 4.36 (Milky-Way-like, includes helium) PRIMARY; alpha_CO = 1.0 (taken as including helium) reported.** mu_mol = M_mol / M*, M* = 10^10.07. HI is unmeasured (mu_mol is a lower bound on the gas).

## 5. Gas profile (only if Molina detects at S/N >= 5)
- Moment-0 from the Molina cube (primary window), smoothed in the image plane to 0.30" FWHM (declared) for annulus S/N.
- PA from the flux-weighted second moments inside the 1.2" aperture (declared; the record has none); i = 38 deg primary, 65 deg reported.
- Elliptical annuli 0.15" wide (deprojected) from 0 to 1.2"; Sigma_CO(R) = mean in annulus; error = annulus rms of off-source noise scaled by sqrt(beams per annulus). The profile is normalised to the Ibar Band 3 total (Molina can resolve out flux; its total is a lower bound), so only its SHAPE comes from Molina.
- Shape flag: "measured" if >= 3 annuli at >= 2 sigma; otherwise "poorly measured" (reported, still used, flagged).
- If Molina does not detect (S/N < 5) but Ibar B3 does: the gas TOTAL is measured, the SHAPE is not; per CFG400/CFG475 the self-calibrated a0 fit is NOT run (no measured shape). This is a result.

## 6. Stellar profile
The record holds only a total M* (logM* 10.07, MAGPHYS) and R_e = 3.8 kpc. **DECLARED and FLAGGED: an exponential thin disc with R_d = R_e / 1.68 = 2.26 kpc as the stellar shape.** Its normalisation is free in the fit (below), so only the shape enters.

## 7. Rotation curve and the self-calibrated fit (CFG385 estimator)
- Points: the 22 KURVS-15 markers, folded (|R|, |v_obs|), v_rot = |v_obs| / sin i (i = 38 deg primary), errors = plotted / sin i, inflated by sqrt(PSF FWHM / marker spacing) = sqrt(4.83/0.847) ~ 2.39 for the correlation of per-pixel markers (declared). kpc/arcsec from Planck18 at z = 1.613.
- Radii used: |R| >= PSF half-width (0.285" in kpc, ~2.4 kpc) PRIMARY (the inner points are beam-smeared); all |R| >= 0.5 kpc reported and flagged.
- Pressure: two branches, never pooled: P0 (none; comparable to CFG140's D_flat) and B10 (v_c^2 = v_rot^2 + 2 sigma0^2 R / R_d, sigma0 = 68 km/s, R_d = 2.26 kpc; Burkert+2010).
- g_obs = v_c^2 / R. g_bar(R) = f [g_*(R) + mu_mol g_gas(R)], with g_* and g_gas the in-plane radial accelerations of thin discs (numerical ring sum with complete elliptic integrals) for the stellar shape normalised to M* and the measured gas shape normalised to M_mol(alpha_CO). **f is free** (the self-calibration); the gas-to-star ratio is fixed by the measurement at each alpha_CO (4.36 primary, 1.0 reported).
- Model g = nu(g_bar / a0) g_bar, kernel nu_mono primary; nu_p2, exp-RAR reported. Grid fit over log f in [-1.5, 1.5] and log(a0 / a0_ref) in [-2, 2]; 68% interval on a0 from the profile Delta chi^2 = 1 over f; chi^2 / dof reported.
- Reporting: a0(z = 1.6) / a0(0) with its interval, relative to EACH footing, against: the framework's DE tracking ~0.95-1.0; flat 1.0; LCDM-feedback ~1.7-1.9 (CFG565, a full-RAR fit; CFG566 notes the estimator dependence); a0 ~ H(z) ~2.4. The pull to each is stated; no class is "favoured" by one galaxy.
- **Span criterion (CFG385 / CFG475):** PASS only if g_obs(max)/g_obs(min) over the used points >= 6.4 AND the best-fit y = g_bar/a0 reaches >= 3 inside and <= 0.3 outside. Otherwise the fit is reported as "SPAN-LIMITED" (interval expected wide; the f-a0 degeneracy may leave it open to the grid edge, which is then said).

## 8. Reproduction control (R1)
The record's KURVS-15 numbers: the authors' model curve at |R| = 9.2 kpc divided by sin 38 deg reproduces V(R_max) = 112.2 km/s within 2%; the table row (z, logM*, R_e, i_SFR, sigma0, R_max) is read unchanged. A miss is kept and disclosed.

## 9. MUTATE
- **MUTATE_A (only if a measured gas shape exists):** the measured gas profile is replaced by an exponential with the same total and R_d = 2.26 kpc; the implied a0 is refitted. Report the shift; **exit 1 if |Delta log a0| > 0.1 dex** (the gas shape matters; the CFG400 lesson made explicit). If no measured shape exists, MUTATE_A cannot run and that is disclosed.
- **MUTATE_B (always):** the injection test of section 3.
- Mutation runs write separate outputs (`*_MUTATE_*`).

## 10. Verdict ladder (one galaxy; never an a0(z) verdict)
1. **NOT POSSIBLE — CO NOT DETECTED** (Ibar B3 S/N < 5): report the S_CO and mu_mol 3-sigma limits; no a0 number.
2. **NOT POSSIBLE — GAS SHAPE UNMEASURED** (Ibar detects, Molina does not): total gas reported; no a0 number.
3. **DEMONSTRATION, SPAN-LIMITED:** shape measured, fit run, span criterion fails: the a0 ratio and interval reported as a demonstration of the estimator only.
4. **DEMONSTRATION, SPAN OK:** as 3 with the span criterion passed. Still one galaxy: it cannot decide a0(z).
Exit codes: 0 if all controls (H1-H4, N1, R1) pass and MUTATE behaves as required; failed controls are kept and reported, never hidden.
