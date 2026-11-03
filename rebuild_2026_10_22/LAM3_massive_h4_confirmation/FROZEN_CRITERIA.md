# LAM3_massive_h4_confirmation: FROZEN CRITERIA, committed alone before any script, download or number

Owner's yes, 2026-11-03, to a confirmation lane for LAM2's post-hoc lead. kappa = 1/2 FITTED. No footing enters (this grades a kinematic estimator, not a gravity law). Not theory closed. Nothing here says the data favour the framework. Reinstates nothing. No download happens until the owner approves each file by name and size.

## The lead, and why it needs this lane
LAM2 (1f83062261) graded NO KINEMATIC AXIS BEYOND PHOTOMETRY: in 2352 gas-poor MaNGA galaxies the SDSS fibre line shape added AUC +0.014 over photometry. After the grade, an ungraded row showed the gain concentrated in the most massive third, log M* > 11.17 (+0.061, 262 of 396 slow rotators), and the highest-velDisp third (+0.064). I looked at that row after the grade, and it is one of 15 subset rows, so it may be chance. It counts only if it repeats on galaxies LAM2 never saw.

## Not blind
I know every LAM2 number in its README. I have not seen any SAMI value. I have read only the SAMI DR3 Data Central TAP schema (table and column names, 3426 rows in `samiDR3Stelkin`).

## Question
On an independent sample, does the SDSS fibre absorption-line shape rank massive gas-poor slow rotators above fast ones better than photometry does?

## Frozen models, trained once, before any SAMI value is fetched
- Models **B** and **S** of LAM2, same inputs, same MLPRegressor settings and seed. Each is trained once on all 2352 LAM2 gas-poor graded galaxies (no folds), with its scaler. Both are saved with their sha256 and committed **before** stage 0's SAMI query runs. They are never retrained, refit or recalibrated on SAMI.
- B: log M*, u-r, Sersic n, eps, log R_e (kpc), fibre radius / R_e, log velDisp. S: B + h4, h6, log(sigma_pPXF / velDisp).
- Slow score: 0.31 sqrt(eps) - predicted lambda_Re, as in LAM2.

## Sample
- **Labels:** SAMI DR3 `samiDR3Stelkin` LAMBDAR_RE_MGE, with `MGEPhotomUnregDR3` epsMGE_Re as eps and ReMGE as R_e (SDSS photometry row where a galaxy has two). Slow: LAMBDAR_RE_MGE < 0.31 sqrt(epsMGE_Re). Galaxies without a finite lambda or eps are dropped and counted. SAMI's lambda is not seeing-corrected and DynPop's is. That shifts which galaxies are labelled slow, and it affects B and S alike.
- **Independence:** any SAMI galaxy within 3 arcsec of a DynPop galaxy is removed.
- **Spectra:** SDSS DR17 SpecObj within 1 arcsec, class GALAXY, zWarning = 0. GAMA and SAMI aperture spectra are not used (different instrument).
- **Photometric features:** NSA v1_0_1 from SkyServer `nsatlas`, matched within 3 arcsec (sersic_mass + 0.310 dex, sersic_absmag u - r, sersic_n). R_e kpc uses DA from flat Omega_m 0.3, h 0.7 at the SDSS redshift, as a classifier feature only. Stage 0 checks this DA against DynPop's on the DynPop galaxies (median ratio within 1 %), or uses DynPop's convention if found.
- **Cuts, as LAM2:** snMedian >= 20, velDisp >= 100 km/s, velDispErr / velDisp < 0.10; gas-poor = MPA-JHU -h_alpha_eqw < 3 A; MPA-JHU sentinels count as missing.
- **Primary cell:** log M* > 11.17, the edge of LAM2's top mass third. **Secondary cell:** velDisp above LAM2's top-third edge, 10^2.327 = 212 km/s. Both edges are from LAM2 and are not re-derived.
- **Line shapes:** `lam2_fit.py` settings unchanged (pPXF 9.5.2, E-MILES 9.0, moments 6, degree 8).

## Stage 0: feasibility (small queries only)
- SAMI TAP query: Stelkin (CATID, LAMBDAR_RE_MGE, its error, APER_CORR_FLAG_MGE), MGEPhotomUnregDR3 (CATID, photometry, ReMGE, epsMGE_Re, epsMGE_LW), InputCatGAMADR3 / InputCatClustersDR3 / InputCatFiller (CATID, RA_OBJ, DEC_OBJ). Size printed, under 2 MB.
- SDSS SQL: SpecObj, galSpecLine, galSpecIndx and nsatlas at the SAMI positions. Size printed, under 20 MB.
- **F1:** primary cell has >= 150 galaxies with >= 40 slow. Otherwise STOP: NOT FEASIBLE.
- **F2:** Hanley-McNeil sigma(AUC) at 0.75 with the primary cell's counts <= 0.020, so the lead's +0.06 would sit at 3 sigma. Otherwise STOP: NOT POWERED. No confirmation is claimed from an unpowered cell.
- **F3:** small single-thread jobs, preemptible.

## Stage 1: grade (only if F1-F3 pass)
- **K1:** sigma_pPXF vs velDisp, as LAM2 (median within +-0.03 dex, rms about zero <= 0.06). Otherwise NO VERDICT.
- **C1, the confirmation:** on the primary cell, AUC(S) - AUC(B) >= 0.03 (half the lead), with the 95 % paired-bootstrap lower bound (1000 draws, fixed seed) > 0.
- **C2:** the same on the secondary cell, reported with the same bar.
- **M1:** h4, h6 and the sigma ratio shuffled within M* x velDisp x eps tercile cells of the primary cell, scored with the frozen S. |AUC(S_mut) - AUC(B)| <= 0.02. Otherwise NO VERDICT.

## Labels
- **CONFIRMED IN MASSIVE GALAXIES:** K1, C1 and M1 pass.
- **NOT CONFIRMED:** C1's gain < 0.03, or its lower bound <= 0. LAM2's massive-third row is then read as chance and is not cited.
- **NO VERDICT:** K1 or M1 fails.
C2 never changes the label. It is reported beside it.

## Reported, not graded
The gain over all SAMI gas-poor quality galaxies (LAM2's E3, transferred). The gain with epsMGE_LW in place of epsMGE_Re. AUCs of B and S separately. Median h4 of slow and fast in the primary cell. Counts dropped at each cut.

## What it means
CONFIRMED would say the fibre line shape carries spin information beyond photometry in massive gas-poor galaxies, the regime of red lenses. It would still not reopen LAM1: the spectroscopic lens sample is too small. It would make a spin split of massive lenses worth a new lane, once a large spectroscopic sample exists. NOT CONFIRMED closes the fibre-spin route. No outcome is a gravity result.
