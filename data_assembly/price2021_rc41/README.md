# RC41: Price+2021 per-galaxy tables (41 star-forming discs at z = 0.66–2.45), parsed from the arXiv HTML page

Parsed 2026-09-29 by `build.py` on the owner's go ("yes, parse the Price 2021 tables from the arXiv page"). Source: Price et al. 2021, "Rotation Curves in z~1-2 Star-Forming Disks: Comparison of Dark Matter Fractions and Disk Properties for Different Fitting Methods", arXiv:2109.02659; only the arXiv HTML page was fetched (`raw_small/`, sha256 in `manifest.json`); tables parsed from the HTML cells by code. Data only: no acceleration, no a₀, no verdict.

## Files
`price2021_rc41.csv` (41 rows, Tables 1 and 3 merged by ID), `price2021_2D_priors.csv` (Table 4, 14 galaxies), `build.py`, `checks.txt`, `manifest.json`.
Columns: Table 1 (`z`, `logMstar_SED`, `SFR_Msun_yr`, `logMgas`, `BT`, `Re_disk0_kpc`, `n_Sersic_disk`, `q0_disk`, `incl_deg`, `c_halo_fixed`); Table 3, the 1D MCMC fit with an NFW halo, no adiabatic contraction and an asymmetric-drift correction, as MAP values with shortest-68% intervals (`logMbar_1D`, `Re_1D_kpc`, `sigma0_1D_kms`, `fDM_Re_1D`, `logMvir_1D`, each with `_lo`/`_hi` errors; `logMvir` is inferred, not free).

## Checks (all PASS, `checks.txt`)
41 galaxies in each of Tables 1 and 3, the same IDs; z 0.658–2.451 (paper: 0.65–2.45); f_DM(R_e) in [0, 1]; M_bar, R_e and σ₀ parsed for all 41; Table 4 lists 14 galaxies (the paper's 2D subset), all present in Table 1 by exact ID.

## What the tables say (descriptive)
- f_DM(R_e): median 0.43, 0.05–0.76; 7 of 41 below 0.2. σ₀ (fitted): median 59 km/s, range 11–83. log(M_gas/M*_SED): median +0.01 (−0.75 to +0.65).
- The fitted log M_bar versus log(M*_SED + M_gas): median difference +0.05 dex (16–84%: −0.08 to +0.33), more than 0.3 dex for 7 of 41.

## What the paper says that bears on use (text of the same page)
- **M_bar is prior-anchored, not free:** "Gaussian priors for log₁₀(M_bar/M☉) with a standard deviation of 0.2 dex that are centered on the baryonic mass derived using log₁₀(M*/M☉) from SED fitting and either a direct measurement of log₁₀(M_gas/M☉) (from Tacconi et al. [2013, 2018] and Freundlich et al. [2019]) or an estimate using the scaling relations from Tacconi et al. [2018]", bounded to [9, 13] dex. R_e has a Gaussian prior (σ = 2 kpc) centred on the earlier least-squares fit; f_DM is flat in [0, 1], σ₀ flat in [5, 300] km/s (Table 4).
- **Which galaxies have a directly measured gas mass is not flagged per galaxy in Table 1** (its footnote says only "From direct measurements, or gas-mass scaling relations"), so the gas column mixes measured (PHIBSS and PHIBSS2 CO) and scaling-relation values without a marker here. (The PHIBSS2 sample is in `../phibss2_z05_08/`; cross-matching would need positions, which Table 1 does not give.)
- f_DM(R_e) is the model's dark-matter fraction within R_e for a Freeman/Sérsic disc plus bulge plus NFW halo with forward-modelled kinematics; the data are Hα and CO rotation curves. **The tables carry no velocities, radii of the outermost data, or per-radius accelerations**: the rotation curves themselves are in the paper's figures and in Genzel+2020 (arXiv:2006.03046).
- For a single radius the fit's f_DM(R_e) fixes the ratio of the total to the baryonic mass within R_e (total = M_bar,R_e / (1 − f_DM)), so each galaxy has one R_e point in mass terms; no acceleration was computed here.

## Limits
Model outputs of a specific halo family (NFW without adiabatic contraction) and an asymmetric-drift correction; M_bar tied to SED plus gas by prior; the gas source is not flagged per galaxy; 41 massive, large discs (log M* about 9.8–11.4) selected for size and quality.
