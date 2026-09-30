# NOEMA3D tables (Jolly+2026 papers 1 and 2), parsed from arXiv HTML

Sources (fetched 2026-09-29, sha256 in `manifest.json`): arXiv:2604.18503v2 (kinematics, radial flows) and arXiv:2604.18504v2 (resolved dust, CO, [CI]). `python3 build.py` regenerates everything and writes `checks.txt`. No downloads beyond the two HTML pages. No acceleration, a0 or verdict is computed.

Files: `noema3d_per_galaxy.csv` (10 rows, both papers merged), `noema3d_observations.csv` (paper 1 Table 2, two weightings per galaxy, 20 rows), `checks.txt`.

## What the tables give (10 galaxies, z = 1.1151-1.6335)
- Per galaxy: z, R_e,star (curve of growth), SED log M*, CO gas mass (paper 1 Table 1 and paper 2 Table 1), f_gas, SFR, inclination, PA, B/T, n_disk.
- DysmalPy (paper 1 Table 3): log M_bary, sigma_0, **V_c at R_e,disk**, V_c/sigma_0, f_DM(R_e,disk), R_e,disk and R_e,bulge (both fixed from photometry), Q_gas.
- Radial-flow velocities (paper 1 Table 4).
- Paper 2: R_e of the stars, CO, [CI], dust and 500 nm, S_CO, S_CI, S_dust, and disk/bulge fits.

## What the pages say, and what they don't
- **R_e definition:** Table 1 R_e,star is "effective radius of the galaxy stellar light, derived from the curve-of-growth method"; V_c and f_DM in Table 3 are at "one effective radius of the disk" (R_e,disk from photometric fitting, fixed in the model). They differ (G4_38065: 8.3 vs 11.0 kpc; G4_24078: 4.7 vs 3.08 kpc); seven of ten differ by more than 0.3 kpc.
- **Outermost radius:** the text gives only "up to a few R_e (2.74 on average, from weightings with the largest extent)". No per-galaxy outermost radius is stated; it needs Fig. 6 (figure only).
- **Pressure support:** the model is a turbulent disk with an isotropic sigma_0. The pages read do not use the words "pressure" or "asymmetric drift", so whether V_c is corrected for pressure support beyond DysmalPy's default is not stated here.
- **Conversion factors (paper 2):** CO alpha_CO = 4.36 ± 0.9 with R_14 = 2.4 (CO(4-3)) and R_13 = 1.8 (CO(3-2)) (Tacconi+2020); dust: T_d = 25 K, beta = 1.8, alpha_850 = 6.7 ± 1.7e12 W/Hz/Msun (Scoville+2016); [CI]: alpha_CI = 18.7 ± 0.6 (Dunne+2022). Paper 2 tabulates only the CO-based M_mol; the dust and [CI] gas masses are not in a table (S_CI and S_dust are, so they can be reconstructed by code with the stated factors, not done here).
- **Radial profiles** of CO, [CI] and dust are figure-only; the rotation curves themselves are figure-only (paper 1 Fig. 6).

## Findings to know before use
1. **Field assignment:** the paper 1 sample table read through a summariser gave "8 GOODS-N, 2 EGS"; the coordinates in Table 2 say **7 in the Extended Groth Strip (RA ~14h19-20m, Dec ~+53) and 3 in GOODS-N (RA ~12h36-37m, Dec ~+62)** (assigned by `build.py`, an inference from the coordinates). The earlier note and the message to the calc chat carried the wrong split; they are corrected.
2. **Overlap:** G4_38065 is PHIBSS 2013 EGS13035123 (0.01 arcsec, z_CO 1.115 vs 1.1151), the only positional match to any local table. Tacconi+2013 values for it: V_rot 193 km/s (its own formula), M_mol 9.0e10, M* 1.5e11, against NOEMA3D V_c(R_e,disk) 299 km/s, M_mol 10^10.82 = 6.6e10, M* 10^11.43 = 2.7e11. No positional overlap with PHIBSS2 (nearest 22 arcsec), the local KMOS3D catalogue (COSMOS, GOODS-S and UDS only), KURVS, ALPAKA I or CRISTAL; no shared ID numbers with Price+2021 RC41, PHIBSS 2013 or KMOS3D. The local tables do not include Tacconi+2018, Genzel+2020 or RC100 coordinates, so overlap with those is NOT checked.
3. **The two papers disagree on shared quantities** (22 differences listed in `checks.txt`): G4_38232 log M_mol 10.65 vs 10.54; GN4_32842 inclination 49 vs 20 deg and PA -20 vs -66 deg; B/T differs for five galaxies (e.g. GN4_24517 0.10 vs 0.23); n_disk for GN4_32842 1.5 vs 0.9. Not corrected; the paper-1 columns (the ones DysmalPy used) are the default in the merged CSV, with paper-2 values kept alongside as `*_P2`.
4. **Baryon masses:** log(M* + M_gas) minus the dynamical log M_bary is within 0.1 dex for 7 of 10, +0.41 dex for GN4_18574 and -0.32 for G4_20371 (M_bary is a model parameter, not a tabulated sum).

## Source PDFs (downloaded 2026-09-29 on the owner's go)
`~/new_physics/_external_data/noema3d/` (not committed): arXiv:2604.18503v2 (14,839,160 B) and arXiv:2604.18504v2 (5,663,104 B); sha256 in `manifest.json`. **The rotation curves are a single raster image** (paper 1 PDF Fig. 5, page 15, 3862 x 2376 px; the HTML numbers it Fig. 6), not vector, so extraction is raster digitisation, not the exact vector read used for KURVS and CRISTAL. No curve value has been extracted or read; extraction waits for the calc thread's frozen criteria, and a control against Table 3 V_c(R_e,disk) is planned.
