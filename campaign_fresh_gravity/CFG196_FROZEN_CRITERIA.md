# CFG196 — a₀ at z ≈ 2.2 from SINS/zC-SINF adaptive-optics Hα kinematics with PHIBSS CO gas: flat a₀ against a₀ ∝ H(z). FROZEN CRITERIA (phase 1)

Written 2026-09-29, at the orchestrator's go, before any kinematic extraction and before the pre-flight script existed.
- **What has been read from the cubes:** FITS headers only (dimensions, the 0.05″ pixel scale, the wavelength axis, the reference pixel). No spectrum, channel, line map, velocity or dispersion has been read.
- **What the pre-flight will read:** the PSF images (a star; no velocity information) for their FWHM, and the cut-cube headers for the field of view.
- **Change rule:** nothing below may change after a kinematic number is seen. Any later deviation goes in the README as a disclosed departure, and pre-extraction corrections are appended here, dated, with the text above them unchanged.
- **Commit rule:** the orchestrator reviews and commits this file before any phase-2 extraction.

## 0. What the analysts knew before freezing: this test is NOT blind

**Published conclusions for these galaxies, as known to the analyst:**
- **Genzel et al. 2017** (Nature 543, 397): six z ≈ 0.9–2.4 star-forming discs with outer Hα rotation curves that fall beyond the peak, read as strongly baryon-dominated within about R_e. zC406690 is one of the six. This is recalled from the literature and not verified on disk.
- **Lang et al. 2017** (ApJ 840, 92; arXiv:1703.05491): the stacked KMOS3D + SINS outer curve falls. This is on disk only as the abstract-level row 12 of `data_assembly/HIGHZ_SOURCE_TABLE_2026-09-29.md`.
- **Genzel et al. 2020** (ApJ 902, 98): mass decompositions of 41 curves, with high baryon fractions at z ≈ 2. Which of our galaxies it contains is recalled, not verified.
- **Milgrom 2017** (arXiv:1703.06110): the reply that these galaxies sit at high accelerations, where MOND predicts near-Newtonian curves. Recalled, not verified.
- **Tacconi et al. 2013** (on disk, `~/new_physics/_external_data/papers/t13.txt`):
  - BX610's Hα and J-band light come from "an inclined ring … within which a red bulge is embedded", and its stellar half-mass radius is smaller than its Hα and CO radii;
  - R(Hα)/R(stars) ≈ 1.3 (Nelson et al. 2012, as quoted);
  - R1/2(CO) = 1.02 ± 0.06 R1/2(rest B) for the sample with both radii;
  - **BX482's CO "comes from the fainter source BX482se, rather than from the main galaxy BX482"** (Fig. 5 caption, around line 2640).
- **Förster Schreiber et al. 2009** (FS2009, on disk: CDS J/ApJ/706/1364, `data_assembly/high_z_tf_tables/sins2009_dynamics.csv`). Seeing-limited kinematic classes:
  - BX610, BX482 and BX389: "Kinematic modeling / Disk";
  - BX599: "Velocity width / Merger" (v_obs/2σ_int = 0.32);
  - BX513: "Velocity width", class blank (0.26). Below 0.4 FS2009 treats a galaxy as dispersion-dominated.
- **Published velocities seen during name matching** (the CSV rows were printed):
  - PHIBSS vrot: zC406690 224, BX599 284, BX513 98, BX610 216, BX482se 202, BX389 330 km/s;
  - FS2009 V_c: BX610 324 ± 71, BX482 237 ± 40, BX389 259 ± 14, BX599 264 and BX513 174 (the last two are dispersion-based equivalents);
  - FS2009 M_dyn for BX610: 1.9 × 10¹¹ M☉.
  - The pre-flight script does not read any velocity column.
- **A hand estimate made while planning, disclosed:** with PHIBSS's Galactic-α_CO gas (2.3 × 10¹¹ M☉ at R_CO,1/2 = 3.8 kpc), BX610's Newtonian baryonic peak is of order 450 km/s, above both published velocities. A "baryon overshoot" outcome is therefore anticipated for BX610, and its decision line is declared below (§5, D5) before any extraction.
- **A vague recollection, disclosed:** zC406690's published inclination is low, perhaps about 25°. It is not verified. No inclination cut is imposed (§3.4); the inclination error is propagated instead, so this recollection cannot select the sample.
- **The record:**
  - the KURVS a₀(z) lanes CFG140–CFG194, whose readings turn on the outer pressure support and the unmeasured gas;
  - CFG52's correlated mass-scale floor;
  - CFG54's PHIBSS N = 0 at an assumed velocity radius, with CFG90's knife-edge correction.

## 1. Question and laws

**Question:** do resolved AO Hα rotation curves at z ≈ 2.2, with directly measured CO molecular gas, prefer a flat a₀ or a₀ ∝ H(z)?

**The laws**, for a galaxy with Newtonian midplane field g_N(R) from its measured baryons:
- **the prediction:** g_pred = ν(g_N/a) g_N and V_c,pred = √(g_pred R);
- **flat** (the framework's distinctive law): a = a₀;
- **rival:** a = a₀ E(z), with E(z) = √(0.315 (1+z)³ + 0.685), CFG140's Ω_m. E(2.2) = 3.32 here, against 3.24 at Ω_m = 0.3;
- **Newton** (reference only): ν ≡ 1.

**Conventions:**
- **Kernels:** P2, ν = √(1 + 1/y), is primary. ν_mono (FP1's committed kernel, imported read-only through `CFG4_common`) is reported beside it.
- **Footings:** a₀ = κ c √(G ρ_Λ) with κ = ½ FITTED. The canonical footing, 9.3603 × 10⁻¹¹ m s⁻², is primary; the alt footing, 1.1312 × 10⁻¹⁰, is reported.
- **Algebraic application:** ν is applied to the midplane g_N of the thin-disc model. There is no external-field term (declared, untested).
- **Redshift:** z is PHIBSS z_CO; for BX389, which has no CO detection, FS2009's z_Hα.

## 2. Sample (from published classifications only; never from any fitted outcome)

### 2.1 Name match (verified by the analyst; the pre-flight re-verifies it in code)

SINS/zC-SINF AO release names (35) against PHIBSS 2013 names (73), case-insensitive ("ZC" = "zC"):

| SINS AO | PHIBSS row | comp | PHIBSS type | CO | FS2009 class (seeing-limited) |
|---|---|---|---|---|---|
| ZC406690 | zC406690 | — | Disk(A) | detected | not in FS2009 |
| Q2343-BX610 | Q2343-BX610 | — | Disk(A) | detected; CO resolved (R_CO = 3.8 kpc) | Kinematic modeling / Disk |
| Q1623-BX599 | Q1623-BX599 | — | Merger/Disk | detected | Velocity width / Merger |
| Q2343-BX513 | Q2343-BX513 | — | Disp.Dominated | detected | Velocity width / — |
| Q2346-BX482 | Q2346-BX482 | **se** | Disk(A) | detected, attributed by Tacconi et al. to BX482se, not the main disc | Kinematic modeling / Disk |
| Q2343-BX389 | Q2343-BX389 | — | Disk(A) | **3σ upper limit** | Kinematic modeling / Disk |

- **Six name matches, not five.** The brief's five omit BX389, whose CO is an upper limit.
- **Of the five with detected CO, one (BX482) is not the disc's own gas.**
- The other 29 AO galaxies have no PHIBSS row.

### 2.2 Rules

- **R1, measured gas that belongs to the disc:** PHIBSS `co_upper_limit` = 0, AND the PHIBSS row names the whole galaxy (`comp` blank), AND the paper does not attribute the CO to another source.
- **R2, a disc by PHIBSS:** Type = "Disk(A)", i.e. an HST disc morphology plus a resolved CO velocity gradient (Tacconi et al. §3.1).
- **R3, a disc by FS2018:** the AO kinematic classification of Förster Schreiber et al. 2018 (ApJS 238, 21) is a rotation-dominated disc.
  - FS2018's table is NOT on disk. In phase 2 it is transcribed, with page and table cited, before any cube spectrum is fitted. Fetching it needs the owner's go.
  - R3 can move a galaxy OUT of the primary set, never into it.
  - If FS2018 cannot be obtained, R3 is recorded as "not applied", and every phase-2 statement carries that label.
- **PRIMARY = R1 ∧ R2 ∧ R3 = {ZC406690, Q2343-BX610}**, with R3 pending.
- **REPORTED ONLY:** each of these is its own row, never pooled with the primary or with each other.
  - **Q1623-BX599:** R1 passes; R2 fails (Merger/Disk); FS2009 Merger.
  - **Q2343-BX513:** R1 passes; R2 fails (Disp.Dominated). Its V_c rests almost wholly on the pressure prescription.
  - **Q2346-BX482:** R1 fails, because the CO is BX482se's. The PHIBSS row's M* (6.0 × 10⁹) and radius (2.4 kpc) are not the main disc's; FS2009 gives the main galaxy 1.69 × 10¹⁰ M☉ and r1/2(Hα) = 4.2 kpc. It is reported with gas bracketed from 0 to the BX482se value: no measured gas.
  - **Q2343-BX389:** R1 fails (a 3σ upper limit). It is reported with gas from 0 to the limit, a one-sided row.
- **Scope, stated plainly:** the primary sample is two galaxies. CFG52's "2–4 discs give 3σ" was for the deep regime (g_bar < 0.3 a₀); these discs are not deep (see the pre-flight).

## 3. Extraction (phase 2; frozen now)

### 3.1 Data
- Per galaxy, `*_data_cut.fits` and `*_noise_cut.fits` (1001 channels around Hα; the area of FS2018's Fig. 16) and `*_psf.fits`.
- The full cubes are used only if the cut noise cube lacks isolated OH lines for §3.6.

### 3.2 Orientation and PA
- **Frame:** the pixel grid is in the SINFONI frame. Per the release README, rotating the data counter-clockwise by PASINF (from the file name) gives north up and east left.
- **The major axis in the cube frame:** PA_cube = PA_sky − PASINF, measured from the cube's +y axis toward −x.
- **PA_sky:** FS2018's published kinematic PA (transcribed). If FS2018 is unavailable, the fallback is the morphological PA of the Hα line-flux map from second moments (§3.4).
- **Reported only:** the kinematic PA fitted to the velocity map. A disagreement with PA_sky above 30° stops phase 2 for that galaxy for the orchestrator's review. It is never a silent exclusion.

### 3.3 Centre
- The cut cube's CRPIX1/CRPIX2. Per the README, this is FS2018's adopted centre, kinematic for most galaxies. It is fixed, not fitted.
- Variant: ±1 pixel on each axis.

### 3.4 Inclination
- **Primary:** FS2018's published i (transcribed). Its error is ±5° (the record's convention) or FS2018's quoted error, whichever is larger.
- **Fallback, if FS2018 is unavailable:** from the axis ratio q of the Hα line-flux map's second moments, with cos²i = (q² − q₀²)/(1 − q₀²) and q₀ = 0.2, and an error of ±10°.
- **No inclination cut.** The inclination error is propagated coherently (§4) and enters as three cells, i − δi, i and i + δi.

### 3.5 Per-spaxel line fits
- **Spectra:** the primary is a 3 × 3-spaxel box average (0.15″, below the PSF FWHM), with noise propagated in quadrature. Unbinned spaxels are a variant.
- **Model:** Hα plus [N II] λλ6549.86, 6585.27, all sharing one velocity and one width, with vacuum rest wavelengths (Hα 6564.61 Å).
  - [N II]6585/6549 is fixed at 3.0.
  - The Hα and [N II]6585 amplitudes are free.
  - The continuum is linear.
  - The fit window is ±3000 km s⁻¹ around the galaxy-integrated Hα centroid, weighted by 1/noise².
- **Acceptance:** Hα S/N ≥ 5; 0 < σ_fit < 500 km s⁻¹; |v − v_sys| < 600 km s⁻¹. The thresholds are fixed now.
- **The velocity zero point is the free v_sys of §3.8,** so the air/vacuum convention cancels.

### 3.6 Instrumental resolution
- σ_instr is the median Gaussian σ of at least five isolated OH lines in the spatially averaged noise spectrum, converted to km s⁻¹ at the galaxy's Hα wavelength.
- It is subtracted in quadrature from the model side (§3.8), not from the data.
- **Sanity window:** 25–60 km s⁻¹. Outside it, phase 2 stops for review.

### 3.7 Major-axis profiles
- **The pseudo-slit:** along PA_cube through the centre, one PSF FWHM wide (the FWHM is measured from the provided PSF image, as in the pre-flight).
- **Bins:** a half-FWHM along the slit. Each bin's value is the median of the accepted spaxels in it. Its error is 1.25 × the median per-spaxel fit error/√N_indep, where N_indep = (bin area)/(PSF beam area) and at least 1.
- **Scored points:** V and σ bins at projected |x| ≥ 1 FWHM, taking every second bin (one FWHM apart, so independent) from |x| = 1 FWHM. The two sides are kept separate.
- Variants: the offset bin set; bins folded over the two sides.
- **Data sufficiency:** a galaxy with fewer than two scored V points on either side contributes no χ² and is reported only. This is a reach rule, not an outcome rule.

### 3.8 Forward model (beam smearing)
- **The disc:** a thin disc at the fixed centre, PA and i.
- **The intrinsic rotation:** V_rot(R) = √max(V_c,L(R)² − α(R) σ₀², 0).
- **The dispersion:** a constant intrinsic σ₀.
- **The Hα surface brightness:** I ∝ exp(−R/R_d,Hα), with R_d,Hα = rh_opt/1.678. PHIBSS's rh_opt is the Hα half-light radius for the BX sample (Tacconi et al. note 2). For zC406690 the table does not say which band; this is flagged.
- **Beam smearing:** the observed model V and σ are the PSF-convolved, flux-weighted first and second moments. The convolution uses the provided per-galaxy PSF image, normalised, on a 0.05″ grid with 3 × 3 sub-pixel sampling, and the model maps pass through the same slit extraction as the data.
- **The moment approximation is checked** against a full model cube fitted with the §3.5 fitter (C4).
- **Free per law and per cell:** σ₀ ≥ 0 and v_sys. Everything else is fixed.

### 3.9 Pressure support (never pooled)
- **PS-B, primary:** Burkert et al. 2010, α = 2R/R_d,Hα. It is the orchestrator's stated form, and, as recalled, the correction the published analyses of these same galaxies used, so a like-for-like comparison is possible.
  - It is the record's CFG140 P1 and CFG141 P2 form, placed at s_eq = 3.00 in CFG162.
  - **Where this differs from the record:** CFG160 and CFG164 took Kretschmer et al. 2021 (s = 1) as primary. The record's indication that the self-gravitating form over-corrects at 4–7 R_d (the CFG161 KROSS differential; CFG162) is acknowledged. The radii here are about 1.7–5 R_d, where the gap between prescriptions is smaller but not negligible. The verdict rule (§5) requires PS-B and PS-K to agree.
- **PS-K, alternative 1:** Kretschmer et al. 2021 (CFG160's function, verbatim): α(x) = −0.146x² + 1.204x + 1.475, x = R/R_e − 1 clipped to [0, 4], R_e = rh_opt.
- **PS-0, alternative 2:** α = 0, the no-pressure scenario.
  - Pressure support only lowers the rotation below V_c. So a law whose PS-0 model rotation lies below the data is below it under every α ≥ 0.
  - PS-0 therefore carries the one-sided robust exclusion D4 and nothing else.

### 3.10 Baryons
- **Stars:** a Freeman exponential thin disc with M* from PHIBSS (SED, Chabrier) and R_d* = rh_opt/1.678.
- **Molecular gas:** a Freeman exponential thin disc with M_mol from PHIBSS (Galactic α_CO = 4.36 including helium; CO(1-0)/CO(3-2) = 2, as PHIBSS used).
  - R_d,gas = rh_co/1.678 where rh_co exists (BX610 only), otherwise rh_opt/1.678. That is supported by Tacconi et al.'s R1/2(CO) = 1.02 R1/2(opt).
- **g_N(R)** = Σ V_N,i²/R, from the exact Freeman Bessel form, per component.
- **The verdict grid (9 mass cells):** δ* ∈ {−0.2, 0, +0.2} dex on M*, times M_mol × {1/1.5, 1, 1.5} (Tacconi et al.'s stated 50% systematic).
- **Stress rows (reported, never in the verdict grid):**
  - α_CO ULIRG-like, M_mol × 0.8/4.36 (CFG164's bracket);
  - stellar R_e = rh_opt/1.3 (the quoted R(Hα)/R(stars));
  - HI with h = M_HI/M_mol = 0.5 at twice the gas scale (HI is unmeasured at z ≈ 2.2);
  - CFG140's spherical-shortcut geometry.
- **Untested, declared:** a bulge (BX610 has one, per Tacconi et al.); disc thickness; non-circular and radial motions; the external field; HI; dust-obscured stars.

## 4. Statistic

For galaxy g, law L and cell c, with c = (δ*, δ_CO, i, kernel, footing, prescription):

χ²_{g,L,c} = min over (σ₀, v_sys) of Σ over scored V and σ points of (d − m)²/e²,

where e² is the bin error² plus a floor of (10 km s⁻¹)² for V (non-circular motions and side asymmetry) and (10 km s⁻¹)² for σ.

- **Headline number:** Δχ²_c = Σ over primary g of (χ²_{g,rival,c} − χ²_{g,flat,c}). It is positive when flat is preferred.
- **The decision cell:** nominal masses (δ* = 0, Galactic α_CO), published i, P2, canonical footing, PS-B.
- **Fit quality is reported for every law, Newton included:** χ², the number of points and p.

## 5. Decision lines (declared)

- **D0, feasibility (H0).** Before any extraction, the pre-flight (§7), re-run with the published inclinations, must give Z_prof ≥ 2 for the primary sample. If H0 fails, the lane is **NON-DIAGNOSTIC for flat against the rival.** Phase 2 may still run for its reported rows, but no lean or verdict line fires.
- **D1, lean at the decision cell.**
  - Lean flat: Δχ² ≥ +4, and flat's fit has p ≥ 0.01.
  - Lean rival: Δχ² ≤ −4, and the rival's fit has p ≥ 0.01.
  - Anything else is non-diagnostic at the cell.
- **D2, robustness of a lean.** A lean is "robust" only if it holds with the same sign and |Δχ²| ≥ 4 under both PS-B and PS-K, both footings, all three inclination cells, and at least 7 of the 9 mass cells. Otherwise it is "conditional", and the failing conditions are named.
- **D3, disfavoured and killed (the record's language).**
  - Flat is disfavoured if Δχ² ≤ −4 in EVERY cell of the 54-cell grid (9 mass × 3 i × 2 footings) under BOTH PS-B and PS-K, with P2. It is killed at ≤ −9 in every such cell.
  - The same holds for the rival with the signs reversed.
  - ν_mono is reported beside P2.
- **D4, the one-sided robust exclusion (PS-0).** A law is below the data for every pressure support if, under PS-0, the error-weighted mean V residual (data − model) over the scored points exceeds +2σ in every mass cell and both footings.
- **D5, BARYON OVERSHOOT (anticipated for BX610).** Declared before extraction.
  - **Trigger:** at the decision cell, Newton's model rotation, after the PS-B pressure deduction, exceeds the data, with an error-weighted mean V residual below −2σ.
  - **Reading for that galaxy:** "the PHIBSS baryons at Galactic α_CO over-predict the rotation with no a₀ term". Every a₀ law over-predicts further, so the flat–rival comparison measures the allowed gas, not a₀. The galaxy is NON-DIAGNOSTIC for a₀.
  - **Reported alongside:** the gas scale factors f_N, f_flat and f_H at which each law's fit is best (root of dχ²/df = 0 over f ∈ [0.05, 3]). These are the analogue of CFG162/164's break-even gas.
- **D6, BOTH-FAIL.** If both laws have p < 0.01 at the decision cell, the model is inadequate and there is no a₀ reading.
- **Otherwise: NON-DIAGNOSTIC.** The cells favouring each law are listed.
- **Language rule:** "The data favour the framework" is never written. A lean is "a PS-B-conditional (or robust) lean at z ≈ 2.2, with the stated conditions".

## 6. Controls and MUTATE (phase 2)

**Controls:**
- **C1, kernel limits:** P2 at y = 10⁻¹² gives g_pred/√(g_N a) − 1 < 10⁻⁵, and at y = 10¹² gives g_pred/g_N − 1 < 10⁻⁵ (the CFG140-corrected form).
- **C2, the Freeman disc:** V² peaks at R = 2.15 ± 0.02 R_d with V²_peak R_d/(GM) = 0.387 ± 0.004, and V²R/(GM) = 1 ± 0.01 at R = 50 R_d.
- **C3, the spaxel fitter:** on 200 synthetic spectra per galaxy (the cube's own wavelength grid and noise spectrum; S/N 5–30; seed 196), the recovered bias at S/N ≥ 10 must be |⟨Δv⟩| < 3 km s⁻¹ and |⟨Δσ⟩| < 5 km s⁻¹.
- **C4, the forward model:**
  - a δ-function PSF returns the input curve (to 10⁻⁶);
  - i = 0 gives V_los ≡ 0;
  - the moment approximation agrees with the full cube-plus-fitter path to within 3 km s⁻¹ at the scored points (one cell per galaxy).
- **C5:** σ_instr lies inside 25–60 km s⁻¹.
- **C6:** the Hα wavelength at z_CO lies inside each cut cube's wavelength range (this check is also made in the pre-flight).

**MUTATE runs.** Each writes separate `*_MUTATE{n}*` outputs.
- **M1, a planted a₀ recovered from a mock cube.**
  - The mock is built from each primary galaxy's geometry, PSF, noise cube (Gaussian per voxel), σ_instr, σ₀ = 50 km s⁻¹ and nominal baryons.
  - M1a plants the rival and must give Δχ² ≤ −4 at the decision cell. M1b plants flat and must give Δχ² ≥ +4.
  - There are 20 noise realisations per plant (seeds 196–215). Recovery is required in at least 16 of 20.
  - **If recovery fails, the lane is NON-DIAGNOSTIC, whatever the real data give.** A pipeline that cannot see a planted a₀ cannot read a real one.
- **M2, shuffled gas.** A cyclic derangement of M_mol and the gas scale over the four gas-measured overlap galaxies (ZC406690 → BX610 → BX599 → BX513 → ZC406690, each galaxy's gas passing to the next), so ZC406690 receives BX513's gas and BX610 receives ZC406690's.
  - Pinned: the decision-cell Δχ² must move by at least 1, or some law's χ² by at least 4.
  - If neither happens, the README states that the result does not depend on the measured gas (the "gas is inert" flag).
- **M3, velocity scale:** every observed V × 10^0.15 (g_obs × 2). The decision-cell class (D1) must change. The run exits 0 when it does.
- **M4, E(z) → 1:** the rival equals flat, so Δχ² = 0 to 10⁻⁹ in every cell. This is also the pre-flight's MUTATE.

## 7. Pre-flight forecast (phase 1; this lane's `CFG196_preflight.py`)

**Inputs:**
- PHIBSS table values (M*, M_mol, rh_opt, rh_co, z_CO, comp, type, co_upper_limit);
- cut-cube headers (the field of view and the wavelength range);
- PSF images (FWHM).
- **Reported variants only:** FS2009's Hα r1/2 for BX599, BX513 and BX482 (where it differs from PHIBSS), and FS2009's M* for BX482's main disc.
- **Nothing kinematic is read.**

**Predictions:**
- V_c at 1, 2 and 3 R_e (R_e = rh_opt) for Newton, flat and the rival;
- P2 and ν_mono, both footings;
- nominal values plus band minimum and maximum over the 9 mass cells;
- g_N/a₀ at each radius.

**The declared per-point error budget on V_c** (deprojected):
- **(a) statistical, line of sight:** 10, 15 and 25 km s⁻¹ at 1, 2 and 3 R_e, for the two-side average. This is linear in R/R_e between those points and constant outside them, divided by sin i, and multiplied by √2 per side for the dense variant.
- **(b) inclination:** ±5°, i.e. V cot i δi, coherent across the radii of a galaxy.
- **(c) σ₀:** 50 ± 10 km s⁻¹, entering as α σ₀ δσ₀/V_c, coherent across radii (σ₀ is one fitted number). The prescription is PS-B, with PS-K reported. The value 50 is a declared round number of the order of published z ≈ 2 disc σ₀; it is not a measurement of these galaxies.
- **(d) residual beam smearing after forward modelling:** 5 km s⁻¹.
- **(e) floor for non-circular motions and side asymmetry:** 10 km s⁻¹.

The covariance is C = diag(a² + d² + e²) + u uᵀ + p pᵀ, with u the inclination vector and p the σ₀ vector. The inclination is i ∈ {30°, 45°, 60°}, with 45° central until the published values are transcribed.

**The prescription spread (a systematic, reported beside the budget):** V_c,PS-B − V_c,PS-K for the same observed rotation, with V_rot taken from flat-nominal under PS-B.

**Reach, from the header geometry and the PSF only:**
- **inside:** R ≤ the cut cube's half-width along its shorter axis;
- **corner-only:** up to the half-diagonal;
- **outside:** beyond that;
- **resolved:** R ≥ 1 PSF FWHM.
- **Reachable** means inside and resolved.
- The header geometry is an upper bound on the reach; the S/N reach is unknown until phase 2.

**Separations:**
- **per point:** ΔV = V_rival − V_flat at nominal baryons, in km s⁻¹ and in units of the per-point error;
- **Z_nom** = √(ΔVᵀ C⁻¹ ΔV);
- **Z_prof:** the smaller, over the two directions (truth = rival fitted by flat, and truth = flat fitted by the rival), of the minimum over (δ*, δ_CO) of √[ΔV(δ)ᵀ C⁻¹ ΔV(δ) + (δ*/0.2)² + (δ_CO/log₁₀1.5)²];
- **Z_band:** the same minimum with flat priors inside the bands (the worst case);
- **"bands overlap"** at a radius if the flat band's maximum is at least the rival band's minimum.

**Two radius sets:**
- **3-point:** 1, 2 and 3 R_e (the requested table);
- **dense:** every FWHM from 1 FWHM to the reach, both sides as separate points.

**Sample level:**
- Z_prof,sample = √(Σ_g Z²_prof,g) with independent per-galaxy nuisances (primary);
- a coherent variant with one shared (δ*, δ_CO) for the primary galaxies (CFG52's correlated floor).

**H0 (the feasibility gate; the forecast's answer).** On the dense set over reachable radii, with P2, the canonical footing, PS-B budget, i = 45° and independent nuisances:
- Z_prof,sample ≥ 3: "the test CAN be decisive (forecast)";
- 2 ≤ Z_prof,sample < 3: "CAN discriminate at 2σ (forecast)";
- < 2: "CANNOT discriminate (forecast)".
- It is also reported at i = 30° and 60°, for ν_mono and the alt footing, under the PS-K budget, and for the 3-point set.
- **H0 is REPORTED, not load-bearing, in the pre-flight.** It is the answer, not a code check. In phase 2 it is re-evaluated with the published inclinations as D0.

**Load-bearing checks in the pre-flight:**
- C0: the name match reproduces §2.1;
- C1 and C2 (above);
- C6: Hα inside every cut cube's wavelength range;
- **S1 [HEADLINE; MUTATE must change it]:** the rival and flat predictions differ, ΔV > 0 at every radius of every galaxy and Z_nom > 0.

**MUTATE=1** sets the rival's E(z) to 1. Then every ΔV = 0 and every Z = 0, so S1 fails and the run exits 1. Outputs go to `CFG196_preflight_MUTATE.out` and `CFG196_preflight_MUTATE_results.json`.

## 8. NON-DIAGNOSTIC (collected)

- D0/H0 fails (in the pre-flight at i = 45°, or in phase 2 with the published i).
- No primary galaxy meets the data-sufficiency rule (§3.7).
- M1 planted recovery fails.
- D5 (baryon overshoot) or D6 (both fail) at the decision cell, for every primary galaxy.
- The sign of Δχ² differs between PS-B and PS-K, or across the mass cells: the result is "conditional", with the conditions listed.
- |Δχ²| < 4 at the decision cell.
- FS2018 unobtainable: phase 2 may run on the fallback geometry, but every statement is labelled "fallback geometry, R3 not applied".

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## Pre-extraction notes (appended 2026-09-29 after the pre-flight ran; the text above is unchanged; no cube spectrum has been read)

- **§0, citation status.** For Lang et al. 2017, only the arXiv id (1703.05491) is on disk. The journal reference ApJ 840, 92 is recalled, like the other recalled items in §0.
- **§7, implementation of the profile.**
  - Z_prof and Z_band are minimised on a 0.02-dex grid, with δ* ∈ [−0.8, 0.8] and δ_CO ∈ [−0.7, 0.7], and the grid minimum is reported.
  - For rows with no gas (BX389 at gas = 0; BX482's main disc), δ_CO is pinned at 0.
  - The PSF FWHM is a circular Gaussian fitted to the central 25 × 25 pixels of each PSF image. The half-maximum-area equivalent is reported beside it.
- **§7, a post-hoc diagnostic added after the first run.** The first run is kept verbatim as `CFG196_preflight_firstrun.out`.
  - The diagnostic has three parts: a near-perfect-kinematics limit, the masses-exact Z_nom, and a one-term-at-a-time ablation of the error budget.
  - It is reported only. Every frozen-set number, and the H0 verdict, is identical between the first run and the final run.

## Orchestrator note at commit (2026-09-29; no rule changed)
The orchestrating session re-ran `CFG196_preflight.py` (exit 0) and `MUTATE=1` (exit 1) in a scratch copy, and both `.out` files are identical to the lane's. **The frozen D0 feasibility gate fails:** the profiled separation is 0.91σ against 2, and no declared variant reaches 2. Phase 2 is therefore NOT run as a flat-versus-rival test. The lane's standing answer is that with these data the a₀(z ≈ 2.2) question is NON-DIAGNOSTIC before extraction. Phase 2 may be run later only for its reported rows (D5 baryon overshoot, break-even gas scale, an M1-validated pipeline), on a fresh go. The request that opened the lane said E(2.2) ≈ 3.2; the lane uses 3.32 (Ω_m = 0.315, the record's value).
