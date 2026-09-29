# CFG89 — KMOS3D cubes: how far out can Hα rotation be measured, and how many z ≥ 1.9 discs reach g_bar < a₀ there? FROZEN CRITERIA

Written 2026-09-29, **before any CFG89 script existed and before any line fit, velocity, centroid, rotation curve, r_out or g_bar was computed for any real KMOS3D object.** This file is committed on its own. Any later departure goes in the README as a disclosed departure; anything added after the first run is a reported-only row.

**This is a feasibility count, not a test of B.** It asks whether the KMOS3D cubes contain z ≥ 1.9 discs whose Hα rotation is measured out to radii where the model baryonic acceleration g_bar is below a₀. It scores no law, compares no prediction with any velocity, and says nothing about which of flat a₀ (B), a₀ ∝ H(z) or ΛCDM the data favour. κ = ½ and Ω_c h² stay fitted.

## Known before freezing

**Read:**
- `data_assembly/kmos3d_phibss/`: README.md, TACCONI2013_VROT_RADIUS_NOTE.md, checks.txt, manifest.json, fetch_cubes.sh, and the `grep` hits in build.py.
- `data_assembly/HIGHZ_SOURCE_TABLE_2026-09-29.md`.
- `campaign_fresh_gravity/CFG52_a0z_feasibility/README.md` and `feas.py` (lines 1–250: the Freeman-disc and point-mass g_bar functions, the 0.20-dex mass floor, the two footings).
- `CFG54_README.md`; `CFG63_discrimination_forecast/README.md` (first 60 lines).
- `CFG57_sluggs_hot_gas.py` (structure, `Report` / `check` use, the MUTATE pattern).
- `CFG7_common.py` (`Report`, `jclean`, `A0_SI`).
- `CFG81_FROZEN_CRITERIA.md` and `CFG87_slacs_b_paired/CFG87_FROZEN.txt`, as format references.
- The Tacconi+2018 constants in `prep_2026/a0z_crossscale/highz_target_ledger_verified_2026.py` (lines 77–79) and `highz_deepmond_target_list_2026.py` (lines 198–206).

**Inspected in the cubes (no fit of any kind):**
- **All 739 cube headers.**
  - Each cube has 5 HDUs: flux, noise, exposure map, PSF image. The PSF header carries Moffat and Gauss fit keywords.
  - Spatial size is 16–21 × 16–21 spaxels at 0.2″ (CDELT = 5.5556e-5 deg in 739/739 cubes), with 2048 channels.
  - The wavelength axis is linear in µm: λ_k = CRVAL3 + (k + 1 − CRPIX3) CDELT3, CRPIX3 = 1.
    - YJ: CRVAL3 = 1.000, CDELT3 = 1.7529e-4.
    - H: 1.425, 2.1582e-4.
    - K: 1.925, 2.8076e-4.
  - BUNIT = `1e-17 W/m^2/um` for flux and noise alike, i.e. per spaxel (no per-arcsec² unit).
  - The primary header carries the spectral-resolution polynomial R(λ[µm]): `ESO K3D RES COEFF0–5`, `RES MIN`, `RES MAX`. At 1.2 µm it gives R ≈ 3500.
- **Data of 5 cubes** (COS4_00779_YJ, U4_11918_YJ, COS4_01966_K, GS4_18936_K, COS4_03784_H):
  - NaN in 0–7% of voxels.
  - Exact zeros in flux and noise in about 5–6% of voxels. These are runs of whole channels at the band edges (for example YJ channels 0–95 and 2022–2047; K channels 0–94 and 2015–2047).
  - In the brightest spaxels the per-spaxel spectral median reaches 0.08–1.1 times the per-channel noise, so **the cubes are NOT continuum-subtracted.**
  - In two cubes, the robust scatter of the flux over channels 300–700 divided by the noise extension is 1.06–1.09 per spaxel, so the noise extension is close to calibrated for a single spaxel. How it behaves for sums of spaxels, where resampling correlates the noise, was not examined; E2 below handles it.
- **The tarballs** contain only the 739 FITS files. No README or column description is on disk.
- **The catalogue** was cross-tabulated by flag, and the selected-sample counts below were computed from catalogue columns alone.

**Not done before freezing:** no Gaussian or moment fit to any real spectrum; no velocity, integrated flux, centroid or PA; no rotation curve, r_out or g_bar for any KMOS3D object. **C2 and C3 are therefore blind.**

## Flag and unit readings (INFERRED; the release's column descriptions are not on disk)

- **HAFIT_FLAG:**
  - −3: no fit. Flux −99.9, Z = −9999 (79 rows).
  - −2: flux with error 0 and σ fixed near 115 km/s, Z = −9999 (79 rows). Read as an upper limit.
  - −1: the same with Z > 0 (10 rows). Read as an upper limit.
  - 0 (364 rows) and 2 (207 rows): a flux with a positive error, and Z = HAFIT_Z. **Only 0 and 2 are used.**
- **FLAG_ZQUALITY:** 0 on 679 rows, 1 on 106 rows (these include all 46 serendipitous detections). For primary targets, the median |Z − Z_TARGETED|/(1+Z) is 0.0024 for flag 1 against 0.0010 for flag 0. **Read as 0 = the higher-quality redshift class.**
- **FLAG_ADDGALDET = 1** (55 primary rows): another galaxy is detected in the same cube (data-assembly README). The one example seen, U4_11918, has two extra galaxies at |Δz| ≤ 0.0024.
- **RHALF:** read as the H-band semi-major-axis half-light radius in **arcsec**. Its median is 0.37″, about 3 kpc at z ≈ 1–2, which is the size of main-sequence discs; CFG52 used the same arcsec reading. **Q:** read as the axis ratio b/a. **LMSTAR:** log₁₀ M* [M☉]. **SFR:** M☉/yr.
- **HAFIT_FLUX_HA:** read as the Hα flux in 1e-17 erg s⁻¹ cm⁻² inside an aperture of radius HAFIT_AP_RADIUS = 1.5″ (the same on all rows). HAFIT_FLUX_AP_CORR (median 1.03) is read as an aperture correction.
- **Wavelengths** are taken as vacuum. This is the near-IR convention and was not verified on disk. An air/vacuum mismatch would show in C3 as a common offset of about 83 km/s.
- **If any of these readings is wrong, C2 or C3 is where it shows; nothing is re-read after the run.**

## Sample (declared once)

**Selection rules:**
- S1: FLAG_PRIMARYTARG = 1.
- S2: FLAG_ZQUALITY = 0 for the headline. The FLAG_ZQUALITY = 1 rows run through the same pipeline as the reported row R7.
- S3: Z > 0, and HAFIT_FLAG ∈ {0, 2}.
- S4: LMSTAR > 0 and SFR > 0; RHALF > 0 with RHALFERR > 0; 0 < Q ≤ 1 with QERR > 0.
- S5, redshift windows:
  - **HIGH:** Z ≥ 1.9 (all in band K).
  - **LOW:** 0.6 ≤ Z ≤ 1.1 (all YJ).
  - **MID:** 1.1 < Z < 1.9 (all H), reported row R8 only.
- S6: the cube file (catalogue FILE) exists in `../_external_data/kmos3d/cubes/` (relative to the repo root).
- S7: the fit window (E1) lies entirely inside the cube's valid wavelength range. Objects that fail are counted as "window-out".

**Counts from catalogue columns (before S6/S7):**
- FLAG_ZQUALITY = 0: HIGH 168 (Z 1.996–2.675), LOW 215 (Z 0.602–1.039), MID 145.
- FLAG_ZQUALITY = 1: 8, 21 and 12.
- FLAG_ADDGALDET = 1 among them: 15 HIGH and 9 LOW.

**Headline exclusions** (declared rules, applied after extraction, every excluded count reported):
- **K3** (companion or merger proxy): FLAG_ADDGALDET = 1.
- **K1** (no coherent rotation): see E10.
- **K2** (dispersion-dominated): see E10.

**Runtime fallback, declared now:** the main run uses 14 worker processes. If the projected wall time of the full selection, measured on the first 28 objects, exceeds 3 h, the run instead uses a random subsample of 120 objects per window (numpy `default_rng(8902)`, drawn without replacement), and says so in its output.

## Extraction (declared once)

**Constants:**
- c = 299792.458 km/s.
- Rest vacuum wavelengths (Å): Hα 6564.61; [NII] 6549.86 and 6585.27; [SII] 6718.29 and 6732.67; [OI] 6302.05 and 6365.54; HeI 6679.99.
- λ_line(v) = λ_rest (1 + Z)(1 + v/c). Velocities v are relative to the catalogue Z.

**E1 — reading and validity.**
- Flux is HDU 1 and noise is HDU 2. A voxel is **valid** if its flux and noise are finite and the noise is > 0.
- **Fit window:** Hα ± 2500 km/s at the object's Z.
- The window must lie inside [first, last] channel that is valid in at least one spaxel of the cube (S7).
- A spaxel is **usable** if ≥ 90% of the window's channels are valid in it. Only usable spaxels enter any sum.
- In a summed spectrum, a channel is valid only if it is valid in every contributing spaxel with non-zero weight.
- A spectrum is fitted only if ≥ 70% of the window's channels are valid.

**E2 — noise of a summed spectrum.**
- N_sum = √(Σ w_j² N_j²) × f.
- f is computed per summed spectrum: f = max(1, 1.4826 × MAD(r)), with r = (F_sum − med41(F_sum)) / √(Σ w_j² N_j²).
  - med41 is a 41-channel running median over the valid channels of the full band.
  - r is taken over valid channels outside ±3000 km/s of the object's Hα (and, in C1, of the injected Hα), and outside ±1000 km/s of [SII], [OI] and HeI at the object's Z.
- f absorbs the spatial correlation of resampled noise and is never allowed to shrink the noise. The same rule applies to single spaxels, 3×3 boxes, pseudo-slit apertures and the 1.5″ aperture.

**E3 — line model and fit.**
- **The model**, on the valid window channels:
  - F(λ) = c0 + c1 (λ − λ_c) + A_Hα P(λ; μ_Hα, s) + A_N [P(λ; μ_6585, s) + P(λ; μ_6550, s)/3].
  - P is a unit-area Gaussian integrated over each channel (an erf difference divided by the channel width). μ_line = λ_line(v). s = μ σ_obs / c.
  - σ_obs² = σ_int² + σ_instr², with σ_instr = c / (2.3548 R(λ_Hα,obs)). R comes from the primary-header polynomial, clipped to [RES MIN, RES MAX].
  - The fit is weighted by 1/N_sum².
- **Step 1, grid:**
  - v runs over {−600, −590, …, +600} km/s and σ_int over {0, 25, 50, 75, 100, 150, 200, 300} km/s.
  - At each node, (c0, c1, A_Hα, A_N) are solved by weighted linear least squares. If A_N < 0, the node is re-solved with A_N ≡ 0.
  - The node with the lowest χ² is kept, and its S/N (A_Hα over its linear error) is the "grid S/N".
- **Step 2, refine:** `scipy.optimize.least_squares` (method trf) fits all six parameters, starting from that node, with bounds v ∈ [−700, 700], σ_int ∈ [0, 600] and A_N ≥ 0.
- **Errors** come from (JᵀJ)⁻¹ of the normalised residuals. Any parameter sitting on a bound is dropped (held fixed). S/N = A_Hα / σ(A_Hα).
- **A fit is RELIABLE iff all of these hold:**
  - status ≥ 1 and finite errors;
  - **S/N ≥ 5**;
  - |v| ≤ 600 km/s;
  - σ_int ≤ 500 km/s.
- **Flux conversion:** the Hα flux in 1e-17 erg s⁻¹ cm⁻² is A_Hα [cube unit × µm] × 1e3, since 1e-17 W m⁻² = 1e-14 erg s⁻¹ cm⁻².

**E4 — smoothed velocity field (spatial bins).**
- At every spaxel position with ≥ 7 usable spaxels in its 3×3 box, the box-summed spectrum (weights 1) is fitted as in E3.
- Positions whose grid S/N is < 3 skip Step 2 and are unreliable. This is a speed shortcut.
- Reliable positions form a map. Its 8-connected components are labelled, and the component with the largest summed Hα flux is kept: the **galaxy map**.
- **EXTRACTABLE (E0)** iff the galaxy map has ≥ 10 positions.
- **Centre (x0, y0):** the Hα-flux-weighted centroid of the galaxy map.

**E5 — inclination from Q:** cos² i = (Q² − q0²)/(1 − q0²), with intrinsic thickness q0 = 0.2. For Q ≤ q0, i = 90°.

**E6 — kinematic PA from the velocity field.**
- **The model**, on the galaxy map:
  - v(x, y) = v_sys + V_a (2/π) arctan(R / r_t) cos φ sin i.
  - x′ = Δx cos θ + Δy sin θ and y′ = −Δx sin θ + Δy cos θ.
  - R = √(x′² + (y′ / max(cos i, 0.15))²), and cos φ = x′/R (0 at R = 0).
  - Coordinates are in the cube's pixel frame, at 0.2″ per spaxel.
- **The fit:** weighted least squares with weights 1/max(σ_v, 5 km/s)².
  - At each node of a grid θ ∈ {0°, 2°, …, 178°} × r_t ∈ {12 log-spaced values from 0.05″ to 2.0″}, v_sys and V_a are solved linearly. The lowest-χ² node is kept.
- **PA_kin**, the receding direction, is θ if V_a ≥ 0, else θ + 180°.
- **R²_vf** = 1 − χ²_model / χ²_const, where χ²_const uses the weighted mean alone.

**E7 — pseudo-slit.**
- Circular apertures of diameter D = max(PSF_FWHM, 0.4″) (catalogue PSF_FWHM), centred at (x0, y0) + k × 0.2″ × (cos PA_kin, sin PA_kin), for k = 0, ±1, ±2, …. Positive k is the receding side.
- Spaxel weights are the fractional overlap of each spaxel with the circle (5 × 5 sub-sampling).
- An aperture is **COVERED** iff its usable-spaxel weight is ≥ 80% of the circle's area (π D²/4 / 0.04 spaxels).
- Every covered aperture's spectrum is fitted as in E3.

**E8 — r_out.**
- On each side, walk k = 1, 2, …. An aperture **fails** if it is not covered or its fit is not reliable. The walk stops at the first two consecutive failures.
- The side's **run** is the set of reliable apertures before the stop.
- **r_out** is the largest k × 0.2″ such that both +k and −k are in their sides' runs (both sides must meet the threshold). It is 0 if there is none.
- "Either side" (reported row R6): the largest reliable k in either run.
- **FOV-LIMITED** iff the stop on the limiting side involves a not-covered aperture.
- r_out is converted to kpc with D_A of flat ΛCDM, H0 = 70 and Ωm = 0.3 (astropy `FlatLambdaCDM`).

**E9 — velocity at r_out.**
- ΔV = v(+r_out) − v(−r_out), with σ(ΔV) = √(σ_v+² + σ_v−²).
- V_rot = ΔV / (2 sin i). **σ_V/V ≡ σ(ΔV)/ΔV**, which does not depend on i.
- σ_0 = the median σ_int over the reliable apertures of both runs with r_out/2 ≤ |k| × 0.2″ ≤ r_out.

**E10 — classification.**
- **K1, coherent rotation:** E0, r_out > 0, **R²_vf ≥ 0.5**, and **ΔV ≥ 3 σ(ΔV)**.
- **K2, rotation-dominated:** V_rot / σ_0 ≥ 1.
- **K3:** FLAG_ADDGALDET = 1, which excludes the object.
- **Velocity gate** (CFG54's 25%): **σ_V/V ≤ 0.25** at r_out.
- A **CLEAN DISC** passes K1 and K2, is not excluded by K3, and passes the velocity gate.

## g_bar model (declared once)

- **Stars:** M* = 10^LMSTAR. R_e = RHALF [″] × D_A [kpc/″]. R_d = R_e / 1.678.
- **Gas:** μ_gas = M_gas/M* from Tacconi+2018 (ApJ 853, 179), with the repo's constants (A, B, F, C, D) = (0.12, −3.62, 0.66, 0.53, −0.35):
  - log μ_gas = A + B [log(1+z) − F]² + C log δMS + D (log M* − 10.7).
  - δMS = sSFR / sSFR_MS, with sSFR = SFR / M* (catalogue).
  - log sSFR_MS [Gyr⁻¹] = (−0.16 − 0.026 t_c)(log M* + 0.025) − (6.51 − 0.11 t_c) + 9. This is Speagle+2014 in Tacconi+2018's form.
  - t_c is the age of the universe in Gyr at z in the declared cosmology.
  - The gas sits in an exponential disc with the stars' R_d, so the baryons form one exponential disc of mass M_bar = M* (1 + μ_gas).
- **g_bar(r) at r_out:** the exact Freeman thin-disc radial acceleration, as in CFG52:
  - g = (2 G M_bar / R_d) y² [I0(y) K0(y) − I1(y) K1(y)] / r, with y = r / (2 R_d).
  - Constants: G = 6.6743e-11, M☉ = 1.98847e30 kg, kpc = 3.0856775814913673e19 m.
- **Lower-g bracket (row R4):** the enclosed-mass form G M_bar [1 − (1 + x) e^(−x)] / r², with x = r / R_d.
- **Gas bracket (row R3):** μ_gas × 0.5 and × 2.
- **0.2-dex robust counts (row R9):** g_bar × 10^0.2 below the threshold. This is CFG52's correlated mass-floor convention.
- **Footings:** a₀ = 9.3603e-11 (canonical) and 1.1312e-10 (alt) m s⁻², from `CFG7_common.A0_SI`.
- **No bulge is modelled.** No pressure-support or beam-smearing correction enters r_out or g_bar.

## Checks (load-bearing unless marked reported)

A failed load-bearing check makes the run exit 1. Nothing is tuned after a result is seen.

**C1 — injection-recovery on synthetic cubes.** Load-bearing; not affected by MUTATE.

- **Hosts:**
  - Drawn with `default_rng(8901)`: a permutation of the eligible S1–S7 objects with FLAG_ZQUALITY = 0 and FLAG_ADDGALDET = 0, taken separately for HIGH and LOW.
  - The first 30 per window that can host an injection are used. The first 20 get a rotating disc and the next 10 a non-rotating one.
- **Injection:**
  - The model is added to the host cube's real flux, with the host's noise extension unchanged, at a velocity offset of −6000 km/s from the host's Hα.
  - If that window (±2500 km/s) is not inside the valid range, the offset is +4000 km/s. If neither fits, the host is skipped.
  - Z_inj = λ_Hα,host (1 + v_off/c) / 6564.61 Å − 1.
- **The model disc:**
  - An infinitely thin exponential disc with R_d = RHALF/1.678 and inclination from the host's Q (E5). PA_true is uniform on [0°, 360°) and sets the receding direction.
  - It is centred at the host catalogue position's pixel (flux-HDU WCS) and built on a 5× oversampled grid (0.04″) with a 1″ margin.
  - It is convolved with a circular Moffat of FWHM = PSF_FWHM, with β from the host cube's `PSF MOFFAT BETA`, then rebinned to 0.2″.
  - Total Hα flux = HAFIT_FLUX_HA × 1e-3 cube units·µm. [NII]6585/Hα = 0.3, and [NII]6550 = [NII]6585/3.
  - Line width σ_obs = √(σ_0² + σ_instr²), with σ_0 = 45 km/s (HIGH hosts) or 30 km/s (LOW hosts).
  - Rotating: V(R) = V_max (2/π) arctan(R/r_t), with r_t = 0.4 R_d and V_max = (2 × 10^LMSTAR / 47)^¼ km/s.
  - Non-rotating: V ≡ 0 and σ_0 = 80 km/s.
- **The extraction** is run unchanged on the injected cube, with Z = Z_inj. A **reference** is then made: the noiseless model cube (host noise kept for the weights and for f) is fitted in the SAME apertures (same centre and PA), giving v_ref and F_ref.
- **The checks:**
  - **C1a (honest errors):** over all reliable pseudo-slit apertures of the rotating injections, the robust std (1.4826 MAD) of (v − v_ref)/σ_v lies in [0.7, 1.5], with ≥ 30 apertures (else FAIL).
  - **C1b (r_out not noise-inflated):** over the rotating injections that are E0-extractable, r_exp is found with the E8 walk using S/N_true = F_ref / σ_F ≥ 5 (coverage as in E8). PASS iff median(r_out − r_exp) ∈ [−0.2″, +0.2″] and |r_out − r_exp| ≤ 0.4″ in ≥ 80% of them.
  - **C1c (V at r_out):** over the rotating injections with r_out ≥ PSF_FWHM and i ≥ 30°, |V_rot / V_true(r_out) − 1| ≤ 0.25 in ≥ 70% of them. Here V_true(r_out) = V_max (2/π) arctan(r_out / r_t). At least 8 injections are required (else FAIL).
  - **C1d (rotation detection):**
    - (a) ≥ 80% of the rotating injections with r_out ≥ PSF_FWHM and i ≥ 30° pass K1 (at least 8 required, else FAIL); AND
    - (b) ≤ 2 of the 20 non-rotating injections pass K1.
- **Reported (R12):** PA recovery, the median |PA_kin − PA_true| for r_out ≥ PSF_FWHM, and C1c and C1d in the r_out < PSF_FWHM regime.

**C2 — integrated Hα flux.**
- For every selected HIGH and LOW object (FLAG_ZQUALITY = 0) with catalogue S/N (HAFIT_FLUX_HA / HAFIT_FLUX_HA_ERR) ≥ 5, the spectrum summed in a 1.5″-radius aperture is fitted as in E3. The aperture is centred at the catalogue position's pixel (flux-HDU WCS), or at the cube centre if that pixel falls outside the cube.
- PASS iff the median log₁₀(F_cube / HAFIT_FLUX_HA) is within ±0.10 dex AND its robust scatter (1.4826 MAD) is ≤ 0.15 dex.
- Reported (R16): the same with HAFIT_FLUX_HA / HAFIT_FLUX_AP_CORR.

**C3 — Hα centroid redshift.** For the same fits, Δv = c (z_cube − Z)/(1 + Z), which equals the fitted v. PASS iff |median Δv| ≤ 30 km/s AND its robust scatter is ≤ 60 km/s.

**D1 — rotation is detected in the real sample (the MUTATE target).** PASS iff ≥ 20% of all selected HIGH + LOW objects (FLAG_ZQUALITY = 0, after S7) pass K1.

**H1-can and H1-alt — HEADLINE (feasibility gate, CFG54's):**
- Count the HIGH clean discs with g_bar(r_out) < a₀, i.e. N(< a₀), and also N(< 0.3 a₀), on each footing.
- **FEASIBLE** on a footing iff N(< a₀) ≥ 5. Otherwise NOT FEASIBLE.
- Each footing is its own load-bearing check. As in CFG54, a NOT FEASIBLE verdict makes the main run exit 1, and that is a declared, valid result.
- The counts are printed whatever the verdict.

**Reported rows (not load-bearing):**
- R1: N(< 0.3 a₀) on both footings. This is headline information, but not a gate.
- R2: distributions (minimum, 16th, 50th and 84th percentiles, maximum) of r_out/R_e (both in arcsec) and of g_bar/a₀ at r_out.
  - Given for HIGH and for LOW.
  - Each for (a) every E0 object with r_out > 0 and (b) the clean discs.
- R3: the gas bracket counts (× 0.5, × 2) for HIGH, both footings.
- R4: counts with the enclosed-mass (lower-g) bracket.
- R5: beam smearing. The distribution of r_out / PSF_FWHM, and the headline counts restricted to r_out ≥ PSF_FWHM.
- R6: counts using the either-side r_out.
- R7: counts with the FLAG_ZQUALITY = 1 objects added.
- R8: the MID window (1.1 < z < 1.9).
- R9: counts robust to the 0.2-dex mass floor.
- R10: the stage table for each window: selected → window-in → E0 → r_out > 0 → K1 → K2 → not K3 → velocity gate.
- R11: the fraction of clean discs whose r_out is FOV-LIMITED.
- R12: C1 details (above).
- R13: K3-excluded objects that would otherwise count.
- R14: the list of HIGH clean discs with g_bar(r_out) < a₀ on either footing, giving:
  - ID, z, log M*, R_e in kpc;
  - r_out in ″, in kpc, over R_e and over the PSF;
  - g_bar/a₀ on both footings, and μ_gas;
  - V_rot, σ_V/V, V_rot/σ_0 and i.
- R15: the median ratio of the header-polynomial R(λ_Hα) to the catalogue SPEC_RES.
- R16: C2 with the aperture-corrected reading (above).

## MUTATE (declared)

- **What it does:** with `MUTATE=1`, every real cube used by the kinematic extraction (E1–E10, the HIGH, LOW, MID and FLAG_ZQUALITY = 1 objects) has its spaxels spatially scrambled before any extraction step. The spatial positions of all spaxels with ≥ 1 finite channel are randomly permuted, flux and noise spectra moving together, with `default_rng(8989 + catalogue row index)`.
- **What stays unscrambled:** C1 (synthetic), C2 and C3 (integrated aperture fits) run on unscrambled cubes, so they are identical in both runs.
- **What must happen:**
  - The scramble destroys coherent rotation, so **D1 must FAIL**, and the MUTATE must exit 1.
  - Its failing set must differ from the main run's. It will: the main run is expected to pass D1. If the main run is NOT FEASIBLE, both runs fail H1, and the difference is D1.
- **Informativeness:** the README says whether the control is informative. It is informative on rotation detection in any case, and informative on the headline only if the main run is FEASIBLE.

## Outputs (lane directory)

- The script `cfg89_kmos3d_outer_rc.py`. It resolves the cube directory as `os.path.join(REPO, "..", "_external_data", "kmos3d", "cubes")`, with REPO derived from `__file__`.
- `cfg89_kmos3d_outer_rc.out` and `_results.json`, with the `_MUTATE` pair.
- The per-object table `cfg89_per_object[_MUTATE].csv`.
- The per-aperture curves of the E0 objects, `cfg89_curves[_MUTATE].csv`.
- The per-injection table `cfg89_c1_injections[_MUTATE].csv`.
- No cube data are copied into the repo.

**κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed, and nothing here says the data favour B, the framework or ΛCDM.**
