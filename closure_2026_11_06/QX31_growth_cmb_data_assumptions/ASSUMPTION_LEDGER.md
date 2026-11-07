# QX31 assumption ledger: LCDM-dependent steps in the data products behind the growth / CMB-lensing failures

Kappa = 1/2 FITTED; not theory closed.

**Sources.**
- "On disk" means the step is documented in the release files under `_external_data/` (dataset keys, file names).
- PROVISIONAL means a literature statement from memory. Section numbers and sizes were not re-read in this lane, so none of
  them sets a label.
- The sizes come from qx31.json unless a row says otherwise.

**Gaps.**
- **A**: shape chi^2 1308-1594 for the law alone, against a line of 20.09. WG6's screened runs read 126-261.
- **B**: mu_min/mu_max = 2.50 dex.
- **C**: Delta chi^2 92.6 against 4.
- **D**: Delta chi^2 230.9 against 4.
- **Direction**: "eases" moves a statistic toward a pass, "worsens" away from one.

## Planck PR4 lensing (Carron, Mirmelstein & Lewis 2022, PROVISIONAL citation)

How the record uses it: 9 raw PP bandpowers, L 8-400, with the CMB-marginalised covariance, run through the package rule
B = W X + M X - F (cfg917_lib.pr4_binned). This is used in WG2-WG6, QX3 iter1-3, QX27 G6 and QX10/QX15 J-checks. No derived
amplitude is graded except WG2-WG4's r, which WG6 withdrew in favour of the shape.

| # | LCDM-dependent step | Documented where | Direction | Size against the gap | Admissible? | Prior audit |
|---|---|---|---|---|---|---|
| L1 | Estimator normalisation (response) computed with FFP10's fiducial lensed TT/EE/TE | on disk: PS1.dataset `linear_correction_bin_window_in_order = TT EE TE PP` | V2 worsens | The CMB-spectrum part sum M^XY C^XY is 1.9-2.8x the data per bin, but at FFP10 it cancels against F_PS1 to 1.3e-4 (K2). Replacing the CMB-marged constant with the explicit PS1 correction (V2) raises S by 27-28 % of gap A for the QUMOND-on law-alone runs, 18 % for law off and <= 4 % for the screened runs, mostly through the tighter non-marginalised covariance. C +0.3, D +10.3, B 0 dex. | yes (V2) | CFG917 A1 (rule proven, unsized) |
| L2 | N1 bias, plus the normalisation's C^phiphi dependence, from FFP10's C^phiphi | on disk: `_CMBmarged_lens_delta_window`, `_lensing_fiducial_correction.dat` | the record applies it; dropping it (V1) eases | F/d is 0.016 at L 28 and 0.23 at L 377. For law-alone models the corrected bin 9 goes NEGATIVE (model/data -0.07, against +0.07 plain): the real N1 is smaller than the fiducial N1 that was subtracted. Dropping the correction moves A toward a pass by 8.8-9.5 % of the gap (WG6 at 100 Mpc: 17 %; at 33 Mpc: 2-4 %), C by 3.0 (3 %), D by 2.5 (1 %), B by 0 dex. | yes (V1 bounds it) | CFG917 (applied, unsized) |
| L3 | N0 from realisation-dependent RDN0, with simulations for the mean-field and noise model | file name `rdn0cov`; PROVISIONAL | second order in the fiducial | Not separable from the products. Covered by the V4 bound (5 % per bin): A 979-990 for the law alone, C 54, D 160. | no (bound) | none |
| L4 | Multiplicative Monte Carlo normalisation correction from FFP10 simulations | PROVISIONAL (few-percent size) | either | V4 bound, as L3 | no (bound) | CFG917 disclosure 2 (listed) |
| L5 | Foreground residuals (masked point sources, tSZ/CIB), checked on simulations | PROVISIONAL (~1 % at L < 400) | either | V4 bound, as L3 | no (bound) | none |
| L6 | Covariance from FFP10 simulations at the fiducial signal | on disk: `_CMBmarged_cov.dat` | V3 eases | The most generous model-dependent covariance (V3: cosmic-variance inflation wherever model > data, never shrinking) gives A 634-682 for the law alone, about 31-34x the line. B's Delta chi^2 at mu 79.4 is 352. C 50, D 185. V3 + V4 together (V5): A 370-399, C 31, D 131. Nothing flips. | no (likelihood choice; bound) | none |
| L7 | CMB-spectrum marginalisation (constant F at a package reference CMB, plus covariance inflation) | on disk: `_CMBmarged.dataset` | see L1 | V2 removes it | yes (V2) | CFG917 A1 |
| L8 | Bandpower binning weights from the fiducial | on disk: `_window/` | none | The windows are applied to the model, so there is no bias. Size 0. | n/a | none |

## ACT DR6 lensing

Not consumed by any failing lane, and not on disk. NOT CONSUMED: nothing to grade.

## Primary CMB (QX15: PR4 CamSpec NPIPE + ACT DR6 CMB-only)

How the record uses it: likelihood-level TT/TE/EE with nuisances profiled. The baryons-only + law control (MB) has
Delta chi^2 +172,848 (canonical) and +166,612 (alt), against a line of 25.

| # | Step | Documented | Size against the gap | Label |
|---|---|---|---|---|
| P1 | CamSpec foreground and calibration nuisance model | on disk (CamSpec yaml, read as text by QX15) | All of the nuisance freedom is worth 732 in chi^2 (QX15 KA-P2, a computed record number). That is 0.42 % / 0.44 % of the gap, and every MB fit already profiles it. | ROBUST |
| P2 | CamSpec covariance at a fiducial spectrum | PROVISIONAL | Not regraded (it needs the MB spectra and CamSpec's covariance machinery). To flip, chi^2 would have to fall about 7,000x. A V3-type bound rescales chi^2 by at most (model/data power)^2 per mode, so it would need a power ratio of about 80 everywhere. Not computed. | ROBUST (sized, not regraded) |
| P3 | ACT DR6 CMB-only foreground marginalisation | PROVISIONAL (multi-frequency to CMB-only) | MB fails on CamSpec alone | ROBUST |

## KiDS-1000 lensing (Brouwer+2021 isolated lenses; QX7 iter_4/5 G6, QX10 G6, QX27 G2; QX21 T1)

| # | Step | Documented | Size against the gap | Label |
|---|---|---|---|---|
| K1 | Sigma_crit and ESD from flat LCDM (Om 0.2793, h 0.70) | CFG885 / E1 I28 | The graded statistic is a SHIFT in mean log(g_obs/g_pred) between two models on the same data, so a rescale T of g_obs cancels EXACTLY. CFG885's T 0.968-1.062 therefore has no effect. | ROBUST |
| K2 | Radius conversion R = theta D_A at fiducial distances | B21 | delta ln D_A between native (h 0.674, Om 0.3085) and fiducial is +0.031 to +0.035 at z_l 0.15-0.35. Bound: \|d shift\| <= 3 \|shift\| delta ln D_A = 0.016-0.028 dex, which is 13-16 % of the gap (shift 0.15-0.27 against 0.05). | ROBUST |
| K3 | Source n(z) (SOM spectroscopic calibration, validated on simulations) and shear m-bias (image simulations) | PROVISIONAL | Multiplicative on Sigma_crit^-1, so it cancels in the shift | ROBUST |
| K4 | Isolated-lens selection with LCDM distances | FN4c (+62.8 % sphere-distance change) | A selection, not a rescale. FN4c rebuilt it; outside the shift statistic | prior audit |
| K5 | QX21 T1 early/late split | CFG885: splits invariant (3.97 sigma / 4.95 sigma) | A ratio of two lens samples on the same Sigma_crit | prior audit |

## Lyman-alpha forest line (QX3 iter3 G4', QX27 G6c, QX7 G4': 0.42/h Mpc at z 3)

| # | Step | Documented | Size against the gap | Label |
|---|---|---|---|---|
| F1 | Line from X4's rule: L346 bands against an LCDM PM reference, and L319's WDM fitting formula (LCDM-hydro calibrated, including thermal history and emulator) | X22 ASSUMPTION_LEDGER (flagged) | The verdict line already sits at the loose edge. Across the published WDM-bound range (1.9-5.3 keV, PROVISIONAL), the half-mode length changes by x3.12, so the line loosens from 0.646 to 2.02 Mpc. QX27 needs 491.7-1024 Mpc. The move is 0.16-0.17 of the gap in log and 0.1-0.3 % linear. | ROBUST |
| F2 | Raw P1D (boera2019_p1d, desi_dr1_p1d_qmle are on disk) | on disk | A raw-P1D grade needs a framework-native hydro forest model, which is not small compute | NOT EVALUABLE (not needed at this gap) |

## Growth: fsigma8 / RSD / S8 / BAO

| # | Step | Status |
|---|---|---|
| G1 | fsigma8 (RSD templates, AP fiducial distances) | NOT CONSUMED. "Growth" in QX3 and QX27 is the PR4-lensing Delta chi^2 of the Jeans-suppressed spectrum (rows L1-L8). |
| G2 | S8 (an LCDM-derived amplitude) | NOT CONSUMED by the failures in scope. CT15 quotes S8 ~0.77 as context against 0.0007-0.0014 (about 1000x off). |
| G3 | BAO fiducial template / distances | Prior audit CFG680-685 (raw geometry). Not graded by these failures. |

## Seeds (EB1b)

| # | Step | Size | Label |
|---|---|---|---|
| S1 | QSO1 BH mass (virial calibration) and spectroscopic z | Enters only the timing gate. The failing step (no baryon clump collapses before z 0.48 at p05) uses CLASS baryons-only sigma_b and WG2's box field, with no external data product. | ROBUST |

## Framework-side inputs (not data products; listed so nothing is hidden)

- QX3 and QX27 brackets: omega_b {0.0215, 0.0230} from BBN D/H (survey calibration), H0 {65, 75}, n_s {0.95, 0.98},
  T_cmb from FIRAS.
- WG backgrounds B2/B2D: a measured-style expansion with a smooth matter term.
- None of these is a Planck LCDM value.
