# PHIBSS2 z = 0.5–0.8: 61 near-main-sequence galaxies with CO(2-1) gas masses (Freundlich+2019, A&A 622, A105; arXiv:1812.08180)

Built 2026-09-29 by `build.py` on the owner's go ("yes, read the PHIBSS2 tables from the arXiv page"). Only the arXiv HTML page was fetched (`raw_small/`, sha256 in `manifest.json`); Tables 1–4 are parsed from the HTML cells by code. Data only: no velocity, baryonic mass or acceleration is computed.

## Files
`phibss2_z05_08.csv` (61 rows, one per galaxy, the four tables merged by number and ID; columns keep the paper's names and units), `build.py`, `checks.txt`, `manifest.json`.
Columns: sample (Table 1: `id`, `field`, `source`, `ra`, `dec`, `z_optical`, `morphology`, `Mstar_Msun`, `SFR_Msun_yr`, `sSFR_Gyr`); CO observation (Table 2: `config`, `t_int_hr`, beam, `dz_CO_minus_optical`, position offsets, `CO_peak_mJy`, `rms_30kms_mJy`, **`CO_FWHM_kms` and `CO_FWHM_err_kms`**); gas (Table 3: `F_CO_Jykms`, `dF_CO_Jykms`, `SN_CO`, `Lprime_CO21`, **`Mgas_Msun`**, `mu_gas`, `f_gas`, `t_depl_Gyr`); HST I-band structure (Table 4: `R_Sersic_kpc`, `n_Sersic`, `q_Sersic`, `R_d_halflight_kpc`, `R_b_halflight_kpc`, `BT`); `flag` (`detection`, `marginal` for the paper's ⋆, `nondetection` for †); and two check columns, `alpha_CO_effective_from_table` and `alpha_CO_eq4_5_predicted`.

## Contents (from the table)
61 galaxies at z_optical 0.501–0.788, log M* 10.04–11.64 (median 10.71), in COSMOS (25), AEGIS (17), GOODS-N (19). 55 detections, 5 marginal (XC53, XW53, XA55, XE55, L14GN022), 1 non-detection (XB55). Detected S/N 1.8–12; median μ_gas = 0.27 (0.03–1.79).

## Checks (all PASS, `checks.txt`)
The four tables agree row by row on number and ID; μ_gas = M_gas/M*, f_gas = μ/(1+μ) and t_depl = M_gas/SFR reproduce from the table columns (within table rounding); L′_CO recomputed from F(CO) with the paper's Eq. 2 (assumed Planck18) agrees within 10.1% for every row; the effective conversion α_CO,eff = M_gas·r₂₁/L′ (r₂₁ = 0.77) reproduces the paper's Eq. 4–5 metallicity-dependent α_CO within 15% for every row, mean 4.07 (the paper states 4.0 ± 0.3).

## What the paper says that bears on use (from its text and table notes)
- **The gas is CO(2-1) only** (molecular; no HI). **Conversion:** the M_gas values follow M_gas = α_CO(Z)·L′/0.77 with the metallicity-dependent α_CO of Eq. 4–5 (mean 4.0), which the paper says already includes helium; the **Table 3 footnote d** ("corrected by a factor 1.36 for helium, using α_CO = 4.36 and r₂₁ = 0.77") is **not** the recipe the numbers follow (applying it gives values 1.4–1.6 times higher than the table). The paper puts the systematic uncertainty at ±50%.
- **The width is the FWHM of a single-Gaussian fit to the spatially integrated CO spectrum, not a rotation curve, and no rotation-curve radius is given.** The text says eight galaxies show double-horned profiles (thin rotating discs). Seven detected galaxies have narrow or poorly constrained widths (L14CO012 39 ± 15, XH54 77 ± 21, L14EG006 75 ± 19, L14EG010 31 ± 8, L14EG014 79 ± 24, L14GN032 60 ± 61, L14GN033 100 ± 60 km/s), several at S/N below 4.
- **Sizes:** `R_d_halflight_kpc` is the **half-light radius of the n = 1 disc component** of a two-component I-band fit, not an exponential scale length; it is missing for 9 galaxies (XG53, XI53, XL53, XN53, L14EG010, L14EG015, XB55, L14GN007, L14GN032). Single-Sérsic fits are preferred over two-component ones in 39% of the sample (`sersic_single_better`).
- Stellar masses: SED fits, Chabrier IMF, ±0.2 dex systematic; SFRs from UV + IR, ±0.2 dex.
- A marginal detection or non-detection has an M_gas from a fitted or limit flux; use the `flag` column.

## Limits
This is a gas-mass and integrated-line-width table, so it can support a baryonic Tully–Fisher-level use at z ≈ 0.5–0.8 with measured H₂ but no HI, and no radial acceleration test. Whether a CO FWHM tracks the rotation velocity for these galaxies is not established in the abstract-level reading I did; the paper's Appendix A shows the spectra.
