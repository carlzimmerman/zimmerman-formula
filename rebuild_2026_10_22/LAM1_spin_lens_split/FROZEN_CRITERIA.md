# LAM1_spin_lens_split: FROZEN CRITERIA, committed alone before any script, download or number

Owner's yes, 2026-11-03, to writing this lane after reading arXiv 2610.40789 (Waldrop, Psaltis, Ozel, Guver 2026: a network reads the spin parameter lambda_R from spatially integrated H-alpha profiles, trained on 1471 MaNGA galaxies, rms 0.08). kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Reinstates nothing. No download happens until the owner approves each file by name and size.

The id LR1 is taken (`LR1_j09_window_law`, Lean certificate), so this lane is LAM1.

**Not blind.** I have read CFG829, CFG849 and CFG850: red isolated KiDS lenses sit at A = 1.587 (1.451 after CFG850's +0.123 dex M* shift), blue at 1.016, in W = 10^-13.3 to 10^-11.9 m/s^2; Sersic and colour split equally and cannot be separated in B21's published bins. I have read VS1: slow rotators +0.182, fast +0.062 dex, n = 16, all slow ones central. I made a rough estimate that VS1's split would give about 0.08 dex for a red population that is 85 % fast, against about 0.2 dex in lensing, and said so to the owner. That estimate mixes radii and is not used here.

## Question
At the dwarfs' accelerations, does the isolated red-lens lensing excess follow rotation support (lambda_R), or does it sit equally in fast- and slow-rotating red lenses?

CFG849 asked for cross-classified lenses. Fast-rotating red ETGs and slow-rotating red ETGs are a cross-classification that B21 does not publish, and their kinematics exist only as unresolved fibre spectra.

## What is borrowed from 2610.40789, and what is not
Borrowed: the idea that a network trained on resolved IFU kinematics can read lambda_R from an integrated spectrum. Not borrowed: their network or weights (none released) or their H-alpha input. Red lenses have little H-alpha, so this lane builds its own estimator on stellar absorption lines. Any result here is this lane's estimator, not the paper's.

## Stage 0: feasibility, before any large download

Small inputs only: one public stellar lambda_Re catalogue, SDSS DR17 position cross-match query results, the B21 lens catalogue or the KiDS-bright catalogue if B21's isolated flags are not public, and HTTP HEAD requests for sizes. Each file is listed with source, name and byte size for the owner before it is fetched.

- **Label catalogue, chosen by rule:** the largest public catalogue of stellar lambda_Re with per-galaxy ellipticity, among MaNGA DynPop (Zhu+2023), Graham+2018 (MaNGA) and SAMI DR3 (van de Sande), counted after matching to an SDSS DR17 single-fibre spectrum within 1 arcsec. The ATLAS3D table on disk (`_external_data/atlas3d_emsellem11`, SAURON) is never trained on. It is the external test.
- **Application sample:** B21 isolated lenses with an SDSS DR17 fibre spectrum within 1 arcsec, spectroscopic z used in place of the photo-z. Training and application use the same instrument (SDSS fibre spectra). GAMA spectra are not used.
- **F1, training size:** at least 1000 labelled galaxies with SDSS fibre spectra, and at least 100 of them slow (lambda_Re < 0.31 sqrt(eps), the Emsellem+11 divider). Otherwise STOP: NOT FEASIBLE.
- **F2, power, from B21's own errors:** sigma(Delta A) forecast for Delta A = A_slow - A_fast in W, scaling B21's red-bin covariance by sqrt(N_red,B21 / N_class) per class. The shared shear-calibration term cancels in Delta A; the M* term does not, because slow rotators are more massive, so CFG850's 0.123 dex is applied to slow minus fast as a systematic, added in quadrature. Rotation hypothesis H-rot: all of the excess sits in slow rotators, Delta A_rot = (A_red - 1) / f_slow, where f_slow is measured in the application sample and A_red = 1.451 canonical, CFG850's alt value on alt. Population hypothesis H-pop: Delta A = 0. **Pass:** forecast sigma(Delta A) <= Delta A_rot / 3 on both footings. Otherwise STOP: NOT POWERED, and no shear catalogue is fetched.
- **F3, compute:** stages 1-2 run only as small jobs (under 1 GB RSS, 1 thread) while any heavy run is live, and are preemptible (checkpoint on SIGTERM, resume via compute_queue).

## Stage 1: the estimator (only if F1-F3 pass)

- **Inputs:** each SDSS fibre spectrum fitted for its line-of-sight velocity distribution (V, sigma, h3, h4) with the instrumental resolution from the spectrum's own file. Network: 2 x 128 sigmoid hidden layers as in 2610.40789, one output (lambda_Re), MSE, Adam. Inputs are sigma, h3, h4, the fibre radius over R_e, and photometric eps. Ellipticity is allowed because lambda_R's fast/slow divider uses it.
- **Split:** 80/20 random within the label catalogue, seed fixed and written in the script before training. ATLAS3D is held out.
- **E1:** held-out rms on lambda_Re <= 0.10 (the paper's 0.08 plus its stated 20 % aperture bias at a mean lambda near 0.1).
- **E2:** among galaxies predicted slow, purity >= 0.70 on the held-out set and on ATLAS3D.
- **E3, the confound gate:** a baseline with the same architecture and **no spectral shape** (inputs: M*, u-r, Sersic n, eps, R_e, fibre sigma) is trained on the same split. Slow/fast ROC AUC of the full estimator must exceed the baseline's by >= 0.05 on held-out and on ATLAS3D. Otherwise STOP: **NO KINEMATIC AXIS BEYOND PHOTOMETRY**. In that case a lambda split would only re-split colour and structure, which CFG849 already did.

## Stage 2: the lens split (only if E1-E3 pass)

- **Re-stack:** per-lens excess surface density from the KiDS-1000 gold shear catalogue with its SOM n(z), B21's isolation criterion, and B21's g_bar recipe (stars plus B21's cold-gas estimate; hot gas not used). Distances come from the record's framework-native expansion history on each footing, the same one used by the CFG680-685 raw-geometry lanes; the exact file is named in stage 0 before any stack. A Lambda-CDM background is never a science input.
- **Classes:** red isolated lenses (u-r >= 2.5, as B21) with SDSS spectra, split by predicted lambda_Re at the Emsellem+11 divider. A_class = the CFG829 amplitude over B21-matched bins in W.
- **K1, code check:** re-stacking all B21 red isolated lenses with B21's own cosmology reproduces B21's red-bin A within 1 sigma of B21's error. This uses B21's convention only to check the code. Failure means NO VERDICT.
- **MUTATE:** predicted lambda labels shuffled within (M*, u-r, n) terciles. Delta A must fall within 1 sigma of 0, or NO VERDICT. Outputs are named by mode.

## Labels, each footing; the same label on both, otherwise FOOTING-DEPENDENT
- **KINEMATIC:** Delta A >= +0.30 at > 3 sigma, and A_fast - 1 within 2 sigma of 0.
- **NOT KINEMATIC:** |Delta A| < 1 sigma and < 0.15, and A_fast - 1 >= +0.25 at > 3 sigma (fast red lenses carry the excess).
- **UNDECIDED:** anything else.
Every label is reported with and without the CFG850 +0.123 dex M* shift on both classes. The label is read on the shifted row.

## Reported, not graded
A_slow and A_fast on blue lenses, if any blue slow rotators exist. The Sersic n split within fast red lenses. The mass-matched Delta A (|dlog M*| < 0.2). f_slow as a function of M*.

## Limits stated now
A fibre covers the centre: at z of 0.1-0.2 a 3 arcsec SDSS fibre sees under one R_e, so this estimator infers lambda_Re from the inner profile. Lensing at W probes hundreds of kpc. A KINEMATIC label is a correlate of the excess, not a mechanism, and says nothing about cold dark energy halos or their failing keys. An isolation criterion is not a central/satellite label, so VS1's environment confound is reduced, not removed.
