# LAM3_massive_h4_confirmation: STOPPED AT STAGE 0, NOT FEASIBLE. SAMI DR3 has 63 independent massive (log M* > 11.17) gas-poor galaxies with a usable SDSS fibre spectrum, 31 of them slow; F1 needs 150 and 40, and F2's sigma(AUC) is 0.062 against 0.020. LAM2's massive-third lead can be neither confirmed nor killed on public data, and stays an unconfirmed row that is not cited

Criteria `FROZEN_CRITERIA.md` (d5c434a268), alone first. Frozen LAM2 models (`lam3_model_B.pkl`, `lam3_model_S.pkl`, sha256 in `lam3_models.json`, 881b1e9bd5) were committed before any SAMI value and were never used. Files: `lam3_fetch.py`, `lam3_stage0.py`, `.out`, `.json`, `lam3_sample.csv`. Not a gravity test. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.

| step | count |
|---|---|
| SAMI DR3 Stelkin rows | 3068 |
| with MGE photometry and a position | 3017 |
| finite LAMBDAR_RE_MGE, epsMGE_Re, ReMGE | 1752 |
| removed, within 3" of a DynPop galaxy (independence) | 84 |
| independent, SDSS spectrum <= 1", NSA <= 3", quality cut | 590 (107 slow) |
| with an MPA-JHU line row | 568 (101 slow) |
| gas-poor | 446 (93 slow) |
| **primary: log M* > 11.17** | **63 (31 slow)**: F1 FAIL (>= 150, >= 40) |
| F2 sigma(AUC) at 0.75 | **0.0619**: FAIL (<= 0.020) |
| secondary: velDisp > 212 km/s (row) | 74 (33 slow), sigma(AUC) 0.058 |

Inputs: SAMI DR3 TAP (Data Central), 587,655 B in `_external_data/lam3_sami_dr3_2026_11_03/`; SDSS DR17 SpecObj + galSpecLine + galSpecIndx and nsatlas in 55 one-degree RA strips, 3,321,483 B in `_external_data/lam3_sdss_2026_11_03/`. No spectra were downloaded; stage 1 did not run.

## Checks, reported
- NSA masses from SkyServer `nsatlas` equal DynPop's to 0.0000 dex on the 84 overlap galaxies, so the features would have matched training exactly.
- DA from flat Omega_m 0.3, h 0.7 is 0.968 of DynPop's DA, constant to 0.0003: DynPop uses another H0 (about 3 % larger D). The criteria say to use DynPop's convention when found; it would have shifted log R_e by 0.014 dex. Not needed, as the lane stopped.

## Reading
- The bottleneck is SDSS spectra, not SAMI kinematics: about 40 % of SAMI galaxies have an SDSS fibre spectrum, and the massive gas-poor cell keeps 63 after the quality cut. A +0.06 gain would sit at 1 sigma.
- No other public independent sample gets there. CALIFA and ATLAS3D are smaller still, and ATLAS3D's fibre covers about 0.05 R_e, outside LAM2's training range. Only MaNGA itself has enough massive gas-poor slow rotators, and it is the sample the lead came from.
- So LAM2's verdict stands as the result: NO KINEMATIC AXIS BEYOND PHOTOMETRY. The massive-third gain is a post-hoc row, unconfirmed, and is not cited.
