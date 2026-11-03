# LAM4_whole_galaxy_absorption: FROZEN CRITERIA, committed alone before any script, sample draw or number

Owner's yes, 2026-11-03, to building whole-galaxy integrated spectra from MaNGA cubes for 1000 gas-poor galaxies (about 100 GB streamed, each cube deleted after summing), all stages approved. kappa = 1/2 FITTED. No footing enters (this grades a kinematic estimator, not a gravity law). Not theory closed. Nothing here says the data favour the framework. Reinstates nothing.

## Why
LAM2 (1f83062261) found that a 3 arcsec SDSS fibre, which sees about 0.3 R_e, adds only AUC +0.014 over photometry in ranking gas-poor slow rotators above fast ones. arXiv 2610.40789 reads lambda_R from spectra summed over the whole galaxy, and names stellar absorption lines as future work. This lane does that: the same galaxies, the same absorption-line fit, with the aperture changed from the central fibre to the half-light ellipse.

## Not blind
I know every LAM2 and LAM3 number. I have opened one cube (8553-1902) to read its layout: FLUX, IVAR, MASK and LSFPOST per spaxel, 0.5 arcsec spaxels, 4563 log-lambda pixels (step 1e-4 dex, the same velocity scale as SDSS); LSF FWHM 2.54, 2.97 and 3.68 A at 4000, 5500 and 6800 A observed. I did not sum or fit it.

**Circularity, stated now:** lambda_Re and Sigma_Re in DynPop come from the same cubes. The question is the paper's own: does the kinematic information survive being summed into one spectrum? It does not test independent noise.

## Sample, drawn once by the script with a fixed seed
From LAM2's gas-poor graded set (2352 galaxies, 396 slow, the same finite-feature cut): all 396 slow, and 604 fast drawn at random (numpy default_rng(20261103)). The download order is random (same seed), so a partial run is a fair sample. AUC does not depend on the class ratio. Purity does, so it is reported reweighted to LAM2's slow fraction 0.168.

## Integrated spectrum, per galaxy
- Cube: DR17 v3_1_1 `manga-{plateifu}-LOGCUBE.fits.gz`, streamed. Each cube is deleted after its sum is written. At most one cube per worker is on disk.
- Aperture: the ellipse centred on OBJRA/OBJDEC, with DynPop Re_arcsec_MGE (circularised), Eps_MGE and PA_phot. Semi-major axis Re / sqrt(1 - eps). A spaxel counts if its centre is inside.
- A spaxel is used if MASK == 0 and IVAR > 0 on at least 80 % of pixels in the fit window. At each wavelength the sum takes the good used spaxels. A pixel is masked if the spaxels missing there carry more than 5 % of the aperture's median flux.
- Noise: summed variance x (1 + 1.62 log10 N)^2, the DAP covariance correction (Westfall+2019), with N = number of spaxels used, capped at 100.
- LSF: flux-weighted mean of LSFPOST sigma over the used spaxels, FWHM = 2.355 sigma, divided by (1 + z) for the rest frame. z is DynPop's.
- Velocities are not shifted before summing. The rotation broadening is the signal.

## Fit
LAM2's `lam2_fit.py` settings: pPXF 9.5.2, E-MILES 9.0, moments 6, degree 8, mdegree 0, emission mask, 5577 and 6300 A sky masks, errors x sqrt(chi2). One change, forced by the resolution: the rest-frame window starts at the first wavelength >= 3900 A where the galaxy's rest FWHM is >= 2.51 A (E-MILES), and ends at 6800 A. One fit per galaxy, failures counted, no refits.

## Checks
- **K1:** log10(sigma_pPXF,int / DynPop Sigma_Re): median within +-0.03 dex and rms about zero <= 0.06. Otherwise NO VERDICT (the sums or fits are wrong).
- **K2:** 200 synthetic integrated spectra (as LAM2's K2: random galaxy's best-fit template mix, sigma drawn from the sample, h4 uniform in -0.10 to +0.10, that galaxy's noise vector). Recovered h4 rms <= 0.03. Otherwise h4 NOT MEASURABLE.
- **M1, MUTATE:** h4 and h6 shuffled together within M* x sigma_int x eps tercile cells, S4 refit. |AUC(S4_mut) - AUC(B4)| <= 0.02. Otherwise NO VERDICT. Outputs named by mode.

## Models
LAM2's architecture and training: MLPRegressor (128, 128), logistic, Adam, early stopping, 5-fold stratified CV, fixed seeds, out-of-fold scores, slow score 0.31 sqrt(eps) - predicted lambda_Re. Paired bootstrap of 1000 draws for every gain.
- **B0, photometry only:** log M*, u-r, Sersic n, eps, log R_e (kpc).
- **B4, + width:** B0 + log sigma_int.
- **S4, + shape:** B4 + h4_int, h6_int.
- **SF, the fibre:** LAM2's S inputs on the same galaxies (B + fibre h4, h6, sigma ratio), refit on the same folds.

## Gates
- **G1, beyond photometry:** AUC(S4) - AUC(B0) >= 0.05, bootstrap lower bound > 0.
- **G2, shape beyond width:** AUC(S4) - AUC(B4) >= 0.03, bootstrap lower bound > 0.
- **G3, whole galaxy beats fibre:** AUC(S4) - AUC(SF) >= 0.03, bootstrap lower bound > 0.
- **E1, E2, qualifiers:** rms(S4) on lambda_Re <= 0.10; reweighted purity of predicted slow >= 0.70.

## Labels
- **NO VERDICT:** K1 or M1 fails. **h4 NOT MEASURABLE:** K2 fails.
- **NO GAIN FROM THE WHOLE GALAXY:** G1 fails.
- **WHOLE-GALAXY SPECTRUM READS SPIN:** G1 passes. The label carries each of these that passes: SHAPE BEYOND WIDTH (G2), BEATS THE FIBRE (G3), PRECISE (E1 and E2).

## Reported, not graded
AUCs of all four models. The gain in M* terciles. Median h4_int of slow and fast. Spearman(h4_int, lambda_Re). Fit window start per galaxy. Cubes failed, spaxel counts.

## What it means
G1 with G2 would show a stellar absorption-line version of the paper's method working on gas-poor galaxies, as long as the whole galaxy is in the spectrum. That would be worth showing to its authors as a result. For lenses at z 0.1-0.5, a 3 arcsec fibre already covers about 0.5-1 R_e, so G3 says how much of that gain a survey fibre at those redshifts could reach. No label is a gravity result.
