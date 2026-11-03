# LAM1 amendments, dated, written before any count

`FROZEN_CRITERIA.md` (5ed7fac28a) is unedited. These amendments make stage-0 steps operational where the criteria could not be run as written. Each was written after looking at the downloaded files' column names and B21's text, and before computing any count, match or fraction. kappa = 1/2 FITTED. Not theory closed.

## 2026-11-03, A1: wave-1 files (owner approved)
- `_external_data/lam1_dynpop_2026_11_03/SDSSDR17_MaNGA_JAM_v2.fits`: 21,479,040 B, sha256 52b11451d8d7aa11eef6f2d133ce3d124bb393633fbbcb37c58a734a7f1cd66e, 10,296 rows.
- `_external_data/lam1_kids_bright_2026_11_03/KiDS_DR4_brightsample.fits`: 89,259,840 B, sha256 8baab69942bcb8f20cbff445107cd6e84b3efc3b6edd4ad64bdf3a349fa36fd6, 1,239,422 rows.
- `_external_data/lam1_kids_bright_2026_11_03/KiDS_DR4_brightsample_LePhare.fits`: 257,817,600 B, sha256 36e35e31a31f8a1c3c88de8a26dee824424adf74a09f7cc0db659848e89b4ca1, 1,239,422 rows.

## A2: B21's lens definitions, quoted from arXiv 2106.11677v1 (HTML), WebFetch, provisional
Isolated: no satellite with more than f = 0.1 of the lens's M* within a spherical r_sat = 3 Mpc/h70. Lens M* < 1e11 h70^-2 Msun. Lenses in 0.1 < z < 0.5, KiDS photo-z above 0.5 removed. Photo-z PDF Gaussian with sigma_z/(1+z) = 0.02. 259,383 isolated lenses. Red means m_u - m_r > 2.5, GAaP. Sersic n > 2 from 2DPHOT for S/N > 50 (Roy+2018). The colour and Sersic bins were equalised in M*. Per-bin counts are not stated.

## A3: reconstructions, labelled
- **Colour.** The downloaded files carry no GAaP u and r. Observed m_u - m_r is rebuilt as (MAG_ABS_u + K_COR_u) - (MAG_ABS_r + K_COR_r) from LePhare; the distance modulus cancels. Labelled RECONSTRUCTED COLOUR.
- **M\*.** MASS_BEST, masked == 0. The flux-scale correction needs GAaP r, which is absent. The correction is reported as not applied, and the M* systematic in F2 already carries CFG850's 0.123 dex.
- **Isolation.** B21's rule with zphot_ANNz2, applied as projected separation < 3 Mpc/h70 and |delta chi| < 3 Mpc/h70 in comoving distance. Distances come from CFG681 `Efun` (T2 fit) on each footing, with h70 units. Satellites are drawn from the full masked == 0 bright sample. Labelled RECONSTRUCTED ISOLATION.
- **K0, a reconstruction check:** the isolated count over 0.1 < z < 0.5, M* < 1e11 must fall within 15 % of 259,383. Otherwise F2 is NOT EVALUABLE and the lane stops at stage 0. The 15 % is set from the photo-z scatter's effect on |delta chi| and the absent flux-scale step, not from data.

## A4: F2 operational
- **N_red,B21** is not published. It is replaced by the reconstructed red isolated count. B21 equalised in M*, which can only reduce their red count, so this inflates the forecast error per class. That makes F2 harder to pass, not easier.
- **sigma_B21,red** is the red-bin amplitude error in W from CFG829's `amp` on `Fig-8_RAR-KiDS-isolated_Colorbin_2.txt` with its covariance, canonical and alt.
- **f_slow** cannot be measured on the application sample before stage 1 builds the estimator. For F2 it is the DynPop slow fraction (Qual >= 1, lambda_Re < 0.31 sqrt(Eps_MGE)) among red DynPop galaxies, where red is NSA rest-frame u - r >= 2.2. It is reweighted in 0.2 dex M* bins to the application sample's LePhare M* distribution, with NSA masses converted from h^-2 to h70^-2 (+0.310 dex). Labelled PROXY f_slow. Stage 1 re-measures it with the estimator.
- **Application sample:** reconstructed red isolated lenses with an SDSS DR17 SpecObj (class GALAXY, zWarning = 0) within 1 arcsec.
- **F1 match:** DynPop galaxies with Qual >= 1 and an SDSS DR17 SpecObj (class GALAXY, zWarning = 0) within 1 arcsec.

## A5: SDSS query
SkyServer SQL on SpecObj, columns specobjid, ra, dec, z only, class = 'GALAXY', zWarning = 0, chunked by RA. DynPop needs z < 0.2 over the full footprint. KiDS-N needs 0.05 < z < 0.6 inside the KiDS-bright bounding boxes. Matching is done locally. The total size of the query results is printed, against the approved scale of under 50 MB.

## A6: Sersic source for wave 2
Roy+2018 2DPHOT (S/N > 50), as B21 used. It is not fetched in wave 1.
