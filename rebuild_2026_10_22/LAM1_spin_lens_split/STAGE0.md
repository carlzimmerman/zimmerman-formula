# LAM1 stage 0: feasibility record, 2026-11-03

Criteria: `FROZEN_CRITERIA.md` (5ed7fac28a), unedited. Nothing has been downloaded and no statistic has been computed. kappa = 1/2 FITTED. Not theory closed.

## Label catalogue, by the frozen rule
MaNGA DynPop JAM catalogue v2 (Zhu+2023; Zenodo record 17518315). The data model (read from `SDSSDR17_MaNGA_JAM_v2_datamodel.pdf`, 131,067 B) lists `Lambda_Re` ("within elliptical half-light isophote, beam corrected"), `Eps_MGE`, `Sigma_Re`, `Re_arcsec_MGE`, `obj_ra`, `obj_dec`, `Qual` (-1 to 3) and `drp3qual`, for over 10,000 galaxies. Graham+2018 covers about 2300 galaxies of the same survey and has no machine-readable table located. SAMI DR3 `samiDR3Stelkin` covers about 1800-3000 galaxies. DynPop is chosen provisionally. The rule's post-match count is confirmed at F1: DynPop stays only if more than 3000 of its galaxies match an SDSS DR17 fibre spectrum. If fewer match, SAMI is counted too.

The NSA masses and magnitudes in DynPop are h-scaled and K-corrected under Omega_m = 0.3, Omega_L = 0.7. They enter only the E3 photometric baseline as features, never as a science input.

## Distances
The record's framework-native expansion history is `campaign_fresh_gravity/CFG681_bao_raw_geometry/cfg681_bao.py` `Efun(om, xn, z)`. Its X(z) = rho_DE(z)/rho_DE(0) is piecewise-linear with no Lambda-CDM model. The parameters are taken from `cfg681_results.json`, the T2 BAO + SN-shape fit, on each footing. This file is named before any stack, as the criteria require.

## Files, HEAD-checked (byte sizes from Content-Length), none fetched

**Wave 1** (needed for F1 and F2):

| file | source | bytes |
|---|---|---|
| SDSSDR17_MaNGA_JAM_v2.fits | zenodo.org/records/17518315 | 21,479,040 |
| KiDS_DR4_brightsample.fits | kids.strw.leidenuniv.nl/DR4/data_files/ | 89,259,840 |
| KiDS_DR4_brightsample_LePhare.fits | same | 257,817,600 |
| SDSS DR17 SkyServer cross-match query results, specObj within 1 arcsec of the DynPop and KiDS-bright positions | skyserver.sdss.org | well under 50 MB, size printed by the query |

Wave 1 totals about 369 MB. The B21 isolation criterion is computed from KiDS-bright plus LePhare, because B21's release (`real_research/data/lensing_rar/brouwer2021_rar/`) has stacked ESD bins only, with no per-lens catalogue or isolation flags.

**Wave 2** (only if F1 and F2 pass):

| file | bytes |
|---|---|
| SDSS DR17 spec-lite FITS for the matched training and application galaxies | about 0.2-0.3 MB each, total printed after F1 |
| KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits | 17,712,469,440 (21,262,011 sources) |
| KiDS1000_SOM_N_of_Z.tar.gz | 4,360 |

## Blockers found
1. **Disk.** The data volume is 100 % full with 15 GiB free. The 17.7 GB shear catalogue does not fit. Wave 2 needs space freed or an external volume first. Wave 1 fits.
2. **pPXF is not installed.** Stage 1's line-of-sight velocity distribution fit needs `pip install ppxf`, which needs the owner's yes. torch 2.6.0 is present.
3. **Compute.** 18 processes are above 50 % CPU, with 22.3 GB RSS of 68.7 GB, mostly AN2 rows. Stage 0 work is small: catalogue reads and SQL. The shear re-stack in stage 2 is heavy and waits until the heavy runs are done, preemptible as frozen.
4. **The Sersic index for lenses has no named source.** The frozen MUTATE shuffles within (M*, u-r, n) terciles. KiDS-bright and LePhare carry no Sersic index. The source has to be named in a dated amendment before wave 2 (candidates: KiDS structural catalogues, or NSA for the z < 0.15 SDSS-matched lenses), or the shuffle runs within (M*, u-r) and is labelled as such. This is open, not decided.

## Not yet computed
F1 (training count, slow count), f_slow in the application sample, and the F2 power forecast all need wave 1.
