# LAM2_gas_poor_lambda_estimator: FROZEN CRITERIA, committed alone before any script, download or number

Owner's yes, 2026-11-03, to an estimator-only lane after LAM1 stopped at stage 0 (53d1be5347), with the instruction to see in depth how the method plays out on gas-poor galaxies. kappa = 1/2 FITTED. Footings never pooled (no footing enters this lane: it grades a kinematic estimator, not a gravity law). Not theory closed. Nothing here says the data favour the framework. Reinstates nothing. No download or install happens until the owner approves each one by name and size.

## Question
Can a single SDSS fibre spectrum of a **gas-poor** galaxy tell a slow rotator from a fast rotator better than its photometry can?

arXiv 2610.40789 (Waldrop, Psaltis, Ozel, Guver) reads lambda_R from the integrated H-alpha profile. Gas-poor galaxies have little or no H-alpha, so that input does not exist for them, and they are where most slow rotators are and where the red lenses of CFG849 sit. The only kinematic carrier left is the stellar absorption-line profile. This lane tests whether that carrier works.

## Not blind
I know LAM1's stage-0 numbers: 6063 DynPop galaxies with Qual >= 1, 5811 with an SDSS fibre spectrum within 1 arcsec, 514 slow among them. DynPop median z 0.040, median R_e 5.27 arcsec, so a 1.5 arcsec fibre radius is 0.28 R_e at the median (5-95 % range 0.13-0.59). One DR17 spec-lite file is 172,800 bytes. I have not seen any spectrum, any line measurement or any H-alpha value for these galaxies.

## Why the physics may fail, stated now
A centred fibre on a symmetric rotator gives a symmetric LOSVD, so h3 averages to near zero; the rotation signal can only show as a flat-topped profile (h4 < 0) and as extra width. Inside 0.13-0.59 R_e the rotation is still rising, so that signal is weak. Slow rotators are also older and more massive, so any spectral feature that tracks age will separate them without measuring spin. The gates below are built to catch both.

## Samples
- **Labels:** MaNGA DynPop JAM v2 (on disk, sha256 in LAM1 A1). lambda_Re, Eps_MGE, Qual >= 1. Slow: lambda_Re < 0.31 sqrt(Eps_MGE) (Emsellem+11). The table is not refit.
- **Spectra:** SDSS DR17 SpecObj, class GALAXY, zWarning = 0, within 1 arcsec (LAM1's match).
- **Quality cut, for every model:** snMedian >= 20, velDisp >= 100 km/s, velDispErr / velDisp < 0.10. Below 100 km/s SDSS's resolution (about 70 km/s) makes h4 unmeasurable.
- **Gas-poor (graded):** H-alpha emission equivalent width < 3 A, from MPA-JHU galSpecLine, the WHAN "retired or passive" line (Cid Fernandes+2011). The sign convention of the EW column is checked in stage 0 against three named galaxies before any cut, and recorded in an amendment. Galaxies without a galSpecLine row are excluded and counted.
- **Gas-bearing (reported, not graded):** EW >= 3 A, same quality cut. Every gate is run on it as a row, so the two populations can be compared.

## Stage 0: feasibility, small inputs only
Inputs: one SkyServer SQL result (SpecObj velDisp, velDispErr, snMedian, plate, mjd, fiberID; galSpecIndx d4000_n, lick_mgb, lick_fe5270, lick_hd_a; galSpecLine h_alpha_eqw, h_alpha_flux, h_alpha_flux_err, sigma_balmer), for the 5811 matched DynPop spectra. Size printed, under 10 MB.
- **F1, size:** gas-poor quality sample >= 1000 galaxies with >= 100 slow. Otherwise STOP: NOT FEASIBLE.
- **F2, power:** Hanley-McNeil sigma(AUC) at AUC 0.75 with the gas-poor slow and fast counts. Pass if sigma(AUC) <= 0.05 / 3. Otherwise STOP: NOT POWERED. (One model's sigma stands for the paired difference, which is conservative for two correlated models.)
- **F3, compute:** single thread, under 1 GB, preemptible (checkpoint per galaxy on SIGTERM, resume via compute_queue).

## Stage 1 wave 1 (only if F1-F3 pass; each item to the owner by name and size first)
- DR17 spec-lite files for the quality sample, gas-poor and gas-bearing (about 0.17 MB each).
- `pip install ppxf` and the template library it bundles; the library file is named in an amendment before any fit.
- ATLAS3D positions (Cappellari+2011 table 3, VizieR) and an SDSS SpecObj query at those positions, for the external test.

## Stage 1: measurements
- **LOSVD fit:** pPXF, moments 6 (V, sigma, h3-h6), additive degree 8, mdegree 0, rest frame 3900-6800 A, pPXF's standard emission-line mask plus 5577 and 6300 sky lines, instrumental dispersion from each file's `wdisp` column. One fit per spectrum, no refits after looking.
- **K1, fit check:** pPXF sigma against SDSS velDisp on the gas-poor sample: median log ratio within +-0.03 dex and rms <= 0.06 dex. Otherwise NO VERDICT (the fits are wrong).
- **K2, h4 recovery:** 200 synthetic spectra per S/N tercile, made from the best-fit template of a random gas-poor galaxy, convolved with a Gauss-Hermite LOSVD (sigma drawn from the sample, h4 uniform in -0.10 to +0.10, h3 = h5 = h6 = 0) and noised to that galaxy's S/N. Recovered h4 rms <= 0.03 over the sample. Otherwise STOP: **h4 NOT MEASURABLE AT SDSS S/N**, and stage 2 is not run.

## Stage 2: the estimator
Four models, one architecture: scikit-learn 1.5.2 MLPRegressor, hidden (128, 128), logistic activation, Adam, MSE on lambda_Re, early stopping on 10 % of each training fold, inputs standardised on the training fold, random_state fixed in the script before any fit. 5-fold cross-validation stratified by the slow label, fold seed fixed. All scores are out of fold.
- **B, photometry:** log M* (NSA Sersic, +0.310 dex to h70), rest-frame u-r (NSA Sersic), Sersic n, Eps_MGE, log R_e in kpc (R_e arcsec x DA), fibre radius / R_e, log velDisp.
- **P, populations:** B + d4000_n, lick_mgb, lick_fe5270, lick_hd_a.
- **S, shape:** B + pPXF h4 and h6, and log(pPXF sigma / velDisp).
- **SP:** P + S's shape inputs.
- **Slow score:** 0.31 sqrt(Eps_MGE) - predicted lambda_Re. AUC is the slow/fast ROC AUC of this score. Predicted slow means score > 0.

Gates, on the gas-poor sample:
- **E1:** S's out-of-fold rms on lambda_Re <= 0.10.
- **E2:** S's purity among predicted slow >= 0.70.
- **E3, beyond photometry:** AUC(S) - AUC(B) >= 0.05, with the 95 % lower bound of a paired bootstrap (1000 draws, seed fixed) > 0. Otherwise STOP: **NO KINEMATIC AXIS BEYOND PHOTOMETRY**.
- **E4, beyond age:** AUC(SP) - AUC(P) >= 0.03, with the paired bootstrap lower bound > 0. The 0.03 is about 2 sigma at F2's limit.
- **M1, MUTATE:** h4, h6 and the sigma ratio shuffled together within cells of M* tercile x velDisp tercile x Eps_MGE tercile, then S refit. AUC(S_mut) - AUC(B) must fall within +-0.02. Otherwise NO VERDICT. Outputs named by mode.

## Labels (gas-poor sample)
- **KINEMATIC ESTIMATOR:** K1, K2, E1-E4 and M1 pass.
- **SPECTRAL, AGE-DEGENERATE:** E3 passes and E4 fails. The spectrum separates slow from fast, but no better than stellar populations do, so it cannot be read as spin.
- **NO KINEMATIC AXIS BEYOND PHOTOMETRY:** E3 fails.
- **h4 NOT MEASURABLE:** K2 fails.
- **NO VERDICT:** K1 or M1 fails.
E1 and E2 failing with E3-E4 passing gives **KINEMATIC AXIS, TOO NOISY TO LABEL**.

## Reported, not graded (the in-depth part)
- Every gate and AUC on the gas-bearing sample, side by side with gas-poor.
- On gas-bearing only: model B + MPA-JHU sigma_balmer, the closest catalogue analogue to the paper's H-alpha input, against S. This compares the paper's carrier with the absorption carrier where both exist.
- Gas-poor AUC gains in terciles of M*, velDisp, Eps_MGE and fibre radius / R_e. The fibre radius tercile is the transfer row: lenses at z 0.1-0.5 put the fibre at 0.5-1 R_e or more, beyond most of this training range.
- Gas-poor AUC gain by EW(H-alpha) in 0-1, 1-2 and 2-3 A, to see whether residual gas helps or hurts.
- h4 against lambda_Re and against V/sigma-like proxies, slow and fast separately; the median h4 of each class with its error.
- Permutation importance of each S input.
- ATLAS3D: S and B trained on all of MaNGA, applied to the ATLAS3D galaxies with SDSS spectra inside the training range of fibre radius / R_e and the quality cut. AUC gain with its bootstrap interval. Reported as CONSISTENT if that interval contains the MaNGA gain, otherwise INCONSISTENT. Not graded, because the count is expected to be small.
- f_slow against M* in the gas-poor sample.

## What each outcome means for the framework
None of these labels is a gravity result. KINEMATIC ESTIMATOR would make a spin split of gas-poor lenses possible from fibre spectra. That would need a new lane with a larger spectroscopic lens sample than LAM1 found, for example DESI BGS over KiDS. NO KINEMATIC AXIS or AGE-DEGENERATE closes that route: a "spin" split of red lenses from fibre spectra would only re-split colour, structure or age, which CFG849 and CFG850 already did. Gas-poor galaxies matter for the law because their baryonic acceleration is stars alone, without a cold-gas estimate. This lane does not use that.

## Limits stated now
Training covers z of about 0.04 and fibre radii 0.13-0.59 R_e. DynPop lambda_Re is a JAM-era catalogue value, beam corrected, not remeasured. The WHAN 3 A line separates emission, not cold gas mass: a galaxy can have H I and no H-alpha. No H I catalogue is used.
