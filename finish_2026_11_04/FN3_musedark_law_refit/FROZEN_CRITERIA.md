# FN3_musedark_law_refit: frozen criteria

Committed alone, before any script or number. Item 3 of the owner's five-item push (`finish_2026_11_04/README.md`). kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework. No cold component, no particle.

## 1. Question
PAPER67 names this test and says it was not run: "a per-galaxy MUSE-DARK refit with this law imposed and a stated baryon-mass error budget. If a0(z ~ 1) stays well above the band with mass systematics under control, the band fails."

So: with a0(z) fixed to the law's native band, do the MUSE-DARK [OII] cubes accept the law with stellar masses consistent with their SED masses plus stated gas, inside a stated error budget?

## 2. What this lane cannot decide, declared now
- **Flat against a0 proportional to H(z) is NOT DECIDABLE here by design.** AT1 and CFG689 need the non-cancelling common mode below 0.055 dex at z 1.0 for 3 sigma. The SED mass scale alone carries 0.20 dex (section 6). This lane grades the band at face value, not the tracking rival.
- A pass is not a measurement of a0(z). It says these data don't exclude the band at the stated budget.
- The record's prior lanes (CFG190, CFG198, CFG199, CFG236, CFG262, CFG356) used the survey's model outputs. Stage 0 here does too and is labelled FORECAST. Only Stage 1, on the cubes, is graded.

## 3. Data
**Stage 0, on disk, no download.**
- The released per-galaxy DC14 runs: 126 galaxies, 7 files each, in `../_external_data/muse_dark/numeric/` beside the repo. Their sha256 are in `data_assembly/musedark_catalogues/numeric_manifest_sha256.txt`. The script verifies every hash before use.
- `photometry_catalogue.txt` (SED log M*, its error, z, SFR) and `Fit_statistics_all_models.txt`, same folder's parent, hashes in `data_assembly/musedark_catalogues/manifest.json`.

**Stage 1, only after the owner's yes with name, source and size.**
- Byte-range cutouts from the three public MUSE HUDF DR2 cubes at `https://amused.univ-lyon1.fr/data/UDF/HUDF/download/`: `DATACUBE_UDF-10.fits` (3,062,799,360 bytes), `DATACUBE_MXDF.fits` (6,575,771,520 bytes), `DATACUBE_UDF-MOSAIC.fits` (26,353,494,720 bytes). HEAD requests on 2026-11-04 returned `Accept-Ranges: bytes`. The full cubes are never stored.
- `UDF_HUDF_Catalogs_FULL.tar.gz` (9,122,619 bytes) from the same folder, for positions and IDs.
- Per galaxy, keep data and variance in a box of 25 x 25 spaxels and 81 channels (plus or minus 50 Angstrom around the [OII] doublet). The fetcher's dry run reads only FITS headers and prints the exact transfer before the ask.

## 4. Sample
- **Primary:** galaxies without bulge parameters that pass every MUSE-DARK III cut present in the files: SED log M* > 8.8, 0.33 < z < 1.44, photometric inclination > 30 deg, released v22 / sigma_0 > 1, and released `log_Z_DC14` < 15000 (III, App. A, which says log Z was rescaled by -2). III's "regular" flag isn't in the files and isn't applied.
- **Secondary (flag only):** the same without the log Z cut.
- z-thirds: equal-count thirds of the primary sample by z, fixed once from the catalogue z before any fit.

## 5. The law, the band and the context laws
- g_obs = nu(g_N / a0) g_N with nu(y) = 1/2 + sqrt(1/4 + 1/y), the law's own interpolation, applied to the midplane baryonic acceleration as III's App. E does. No external field.
- **Band:** a0(z) = a0_foot x sqrt(w(z) / w(0)), where w(z) is linear in z between CFG689's primary (BAO + SN) posterior-mean nodes at z 0, 0.4, 0.7, 1.0, 1.5, 2.33, read from `campaign_fresh_gravity/CFG689_native_ruler_bao/cfg689.json`.
- **Footings, never pooled:** canonical a0_foot = 9.3603e-11 m/s^2, alt 1.1312e-10 m/s^2.
- **Context laws, graded the same way, with no label precedence:** III's linear law a0(z) = (1.00 + 1.59 z) x 1e-10 m/s^2 (III Eq. 4); the rival a0_foot x E(z) with CFG689's native E(z); and free a0 per galaxy, reported.
- **Distances:** CFG689's native background (posterior-mean nodes, omega_b, omega_c, omega_k, and the script's omega_r) gives kpc per arcsec and D_L. SED masses scale by (D_L,native / D_L,planck15)^2. The size of that change is reported.

## 6. Baryons, readings and the budget
**Mass model**, following III App. B and Paper I as written: v_c^2 = v_disk^2 + v_gas |v_gas| (+ v_H2^2), with the DM term removed and the law applied to the summed Newtonian acceleration.
- **Stars:** an MGE of the fitted Sersic [OII] profile, normalised by M*. M* is free per galaxy with no prior. The outcome per galaxy is Delta_i = log10(M*_fit,i / M*_SED,i).
- **Molecular gas:** M_H2 = mu_mol x M*_SED with Tacconi, Genzel and Sternberg (2020, ARA&A 58, 157) eq. 2, log10 throughout, as coded in CFG90: log mu_mol = 0.06 - 3.33 [log(1+z) - 0.65]^2 + 0.51 log(delta_MS) - 0.41 [log M* - 10.7]. delta_MS uses the catalogue SFR and the Speagle et al. (2014) main sequence at the native cosmic time. H2 is distributed like the stars. CFG236's natural-log reading is not used.
- **Atomic gas:** constant Sigma_HI as the survey's `sgas`, Sigma_HI free in [0, 15] Msun/pc^2 (the survey's prior).
- **Pressure support:** the survey's `DalcantonFull`, with the fitted dispersion profile.

**Engine conventions pinned by K1 before any graded number.** Three items aren't fully stated in the papers. Each is chosen from this list only, by K1 on the released curves: the sgas term (v^2 = pi G Sigma r, or 2 pi G Sigma r); the drift (v_AD^2 = -2 sigma^2 dlnSigma/dlnr, with or without the term -sigma^2 dln(sigma^2)/dlnr, sigma the total model dispersion; or the same with sigma_0 alone); the MGE intrinsic thickness (q 0.15, razor thin, or spherical). Every variant's K1 score is recorded.

**Readings (rows; the label carries a flag if any of them changes it):**
- R0 primary: survey drift, Sigma_HI free in [0, 15], mu_mol x 1, delta_MS from SFR.
- R1 half drift (v_AD^2 x 0.5). R2 no drift.
- R3 Sigma_HI = 0. R4 Sigma_HI = 15.
- R5 mu_mol x 0.5. R6 mu_mol x 2. R7 delta_MS = 1 (CFG90's form).

**Budget, frozen now:**
| term | size | kind | source |
|---|---|---|---|
| SED M* per galaxy | sqrt(0.15^2 + eMstar_i^2) dex | random | literature code-to-code scatter, e.g. Mobasher et al. 2015, Pacifici et al. 2023 (provisional, not re-derived) |
| SED M* scale | 0.20 dex | common mode | Conroy 2013 review range 0.2-0.3 dex (provisional) |
| SED M* drift with z | 0.10 dex per unit z | slope only | CFG262 used 0.25; 0.10 is the smaller, stricter choice, frozen here |
| mu_mol per galaxy | 0.25 dex | random | relation scatter (provisional) |
| mu_mol scale | 0.10 dex | common mode | relation normalisation error (provisional) |
| band | CFG689's 68 % half-width of log10 sqrt(X) at the nearest node | common mode | `cfg689.json` |
| fit error | profile likelihood, scaled by sqrt(chi2_red) | random | the fit |

Common mode per z-third: sigma_cm = sqrt(0.20^2 + (L_H2 x 0.10)^2 + (L_band x sigma_band)^2). The levers L_H2 = dDelta/dlog(mu_mol) and L_band = dDelta/dlog(a0) are computed on synthetic galaxies at each third's median z, M*, R_e and sigma_0. They go in `budget.json`, committed before Stage 1 runs.

## 7. Statistics and labels (Stage 1; Stage 0 uses the same with the prefix FORECAST)
Per footing, reading R0:
- Level: per z-third t, the median Delta_t with a bootstrap error (10,000 resamples, seed 20261104). sigma_tot,t = sqrt(sigma_cm,t^2 + sigma_boot,t^2). Z_t = median Delta_t / sigma_tot,t.
- Slope: Theil-Sen slope s of Delta_i against z, bootstrap error, with sigma_s = sqrt(sigma_s,boot^2 + 0.10^2 + (L_H2 x dlog mu_mol/dz error)^2), the last term from the relation's B and F errors.

Labels, first match wins:
1. **NOT DECIDABLE** if sigma_tot,t > 0.35 dex in any third, or fewer than 12 valid fits in any third.
2. **BAND EXCLUDED, TOO LITTLE GRAVITY** if Z_t > +3 in any third. **BAND EXCLUDED, TOO MUCH GRAVITY** if Z_t < -3 in any third.
3. **RISE REQUIRED** if s / sigma_s > +3.
4. **BAND CONSISTENT** if every |Z_t| < 2 and |s / sigma_s| < 2.
5. **TENSION** otherwise.

Flags: [DRIFT-DEPENDENT] if R1 or R2 gives another label; [GAS-DEPENDENT] if R3 to R7 do; [SAMPLE-DEPENDENT] if the secondary sample does. Each footing gets its own label; they are never pooled.

Reported, not graded: per-galaxy chi2 of the law against the survey's DC14 fit on the same voxels (Stage 1); the free-a0 distribution per third; the context laws' Z_t and s.

## 8. Checks
- **K0:** every input hash matches its manifest.
- **K1 (Stage 0):** with the survey's own components (DC14 halo from the released alpha, beta, gamma, concentration, V_vir, X; MGE disc; sgas; drift), the engine's v_perp reproduces `true_Vrot.dat` within 3 % rms over 0.5-2.5 R_e for at least 90 % of primary galaxies, and the released v22 within 3 % for at least 90 %. If no listed convention passes, K1 FAILS and the Stage 0 forecast reads NOT EVALUABLE.
- **K2 (Stage 0):** on 20 synthetic cubelets at survey-like noise with the law planted (canonical band), the 3D fitter recovers log M* within 0.05 dex (median) and a planted +0.30 dex offset within 0.05 dex.
- **K3 (Stage 1):** with the DC14 model on 10 real cutouts, the fitter recovers the survey's v22 within 5 % and inclination within 3 deg for at least 8 of 10.
- **K4:** the free-a0 results are identical on both footings to 1e-6, since they don't depend on the footing.
- **MUTATE:** a0 x 2. On synthetics it must shift the recovered Delta by -0.30 +- 0.07 dex. On real data it must move the median Delta by at least 0.15 dex in every third. If it doesn't bite, no label is issued.
- Rerun: every graded output byte-identical from an empty cache.

## 9. Compute and data hygiene
Single thread, under 1 GB RSS, checkpoint per galaxy, exit cleanly on SIGTERM. Downloaded cutouts live outside the repo in `../_external_data/fn3_musedark_cutouts/` with a sha256 manifest committed. No home paths in committed files.
