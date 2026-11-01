# AC1 FROZEN CRITERIA: pre-data predictions for the ALMA release of 2026-11-06 (2024.1.00100.L, MOUS uid://A001/X3788/Xbfd2)

Committed alone, before any script of this lane and before any byte of this MOUS is public. Owner request 2026-11-01. κ = ½ FITTED. Footings never
pooled. Cold dark energy is a gravitating field component, never a particle. One disc excludes no model. Not theory closed. Nothing here says the data
favour the framework. CFG571, CFG806 and its addenda, AG4d, AG4e and S3's seal are read only and stay the governing record for U4_27928.

**Not blind, disclosed.** Before writing this file I read the archive metadata of the MOUS, KMOS3D's catalogue row and this repo's Hα fits of both
galaxies, and Tadaki+2017 and Tadaki+2023 (arXiv:2309.02703) Table 1 for U4-28473. No pixel of the MOUS exists on disk.

## 1. Finding that opens this lane (archive and catalogue, 2026-11-01)
The MOUS's science target is **UDS28473 = KMOS3D U4_28473**, at the phase centre, z 2.52455, log M★ 11.35. It is not U4_27928. CFG570's box match found
U4_27928 because it lies inside s_fov/2. U4_27928 (z 1.41933) lies 7.36″ off the phase centre, and its CO(2-1) at 95.29 GHz falls in the 94.79–96.67 GHz
window. So the sealed test is a serendipitous off-axis reading, and the targeted galaxy has no seal. The 97.60–98.62 GHz window is centred on CO(3-2) at z 2.52.

## 2. Part A: U4_27928, sealed requirement at the Hα prior (information; no governing plan changes)
Inputs from `CFG99_kmos3d_outer_rc/cfg89_per_object.csv`: vrot 226.1, σ0 77.8, R_out 6.75 kpc, Rd 2.46 kpc. CFG99 records a median 28% slow bias at r_out.
V_c cases, at the sealed R = 2R_e: **a** P0 226.1; **b** P0 bias-corrected 226.1/0.72; **c** P-B on a; **d** P-B on b. Per kernel (ν_mono, n = 1, n = 2),
footing, a₀ model (CFG571's four) and R_g row, with CFG571's head executed read-only. Empirical gas line for comparison: CFG99's μ_gas 0.589.
Sealed-grid values must be reproduced (K2).

Detection forecast: archive line sensitivity at this window, primary-beam response at 7.36″, 12 m FWHM at 95.29 GHz, CFG806's aperture and ±500 km/s window,
exponential disc. Report S/N and the 3σ upper limit on log M_gas, against the requirement range.

## 3. Part B: U4_28473, new predictions, forward and inverse
### Inputs (never pooled, every branch printed)
- **Redshift:** 2.52455 (KMOS3D); Tadaki+23 z_CO 2.523 ± 0.004.
- **Gas flux:** CO(3-2) 0.79 ± 0.08 Jy km/s (Tadaki+23, ≈ 0.6″). L′(1-0) = R31 L′(3-2), R31 1.8 (their value). **α_CO 4.36 and 1.0.**
- **Stars:** log M★ 11.31 (Tadaki+17) and 11.35 (KMOS3D), each also −0.2 dex. **Shape S1:** exponential, R_e 1.37 kpc (Tadaki+23 4.4 μm). **Shape S2:** R_e 3.09 kpc
  (KMOS3D 0.383″, rest-optical).
- **Gas shape:** exponential, R_e 1.56 kpc (Tadaki+23). Interval from their ±0.30 printed.
- **Background:** flat, h 0.6856, Ω_m 0.2976 (`B_cfg886_bg`), w = −1 for distances; the DESI CPL distance is printed as a check. No ΛCDM input to a prediction. SED masses and the
  published flux keep the authors' reductions; this is disclosed, not corrected.

### a₀ readings (both footings)
F-flat, F-DESI (CFG571's CPL), CFG689 band ends 0.325 and 1.212 (at z 2.33, extrapolated, labelled); rivals R-H and L-fb exactly as CFG571 codes them (L-fb's table
ends at z 2.5, held there, labelled).

### Theory readings
1. **n = 1 algebraic (canonical law), primary.** 2. **ν_mono.** 3. **n = 2.** 4. **v3 AQUAL disc:** S3's solver `Disc.C_at`, unedited, on the F-flat, F-DESI and R-H cells.
5. **Route N:** Newtonian baryons + a cold core, S_cold = f_c η Σ_coll with X80's ρ10, ρ11 and CE1's A4 η, no a₀, conditional on lg M200 12.0, 12.5, 13.0. Σ_coll at z = 0 is held at fixed M200 (EM1 R4
reads the ratio at z 2.33 as 0.99–1.06); R200 uses the background above at z. **No z rule for N has been derived, so this reading is an extrapolation and is labelled so.** 6. **Newton**, baryons alone, as the floor every
reading with ν ≥ 1 must exceed.

### Forward prediction
V_c(R) at R = 1, 2, 3, 4, 6, 8 kpc, per reading and input branch.

### Inverse prediction, the primary statistic
At R = 2, 3, 4 kpc and V_c = 300, 350, 400, 450, 500, 550, 600 km/s: required log M_gas and implied **α_CO,req = M_gas,req/L′(1-0)**, per reading, M★ and shape. FLOOR as in CFG571.

### Detection forecast
From 439→434 μJy/beam per 10 km/s (archive, this window): S/N per beam per 50 km/s channel against R for the exponential disc at inclination from Tadaki's q; the largest R with S/N ≥ 3 per 100 km/s; sum-in-aperture S/N.

## 4. Scoring rules for U4_28473, frozen now
- **G1:** CO(3-2) at ≥ 5σ selection-aware (same procedure as CFG806 A-U13), centroid within 0.5″ of the phase centre, z within 0.004 of 2.52455. Else upper limit, stop.
- **G2:** the emission reaches R = 3 kpc. Else report the largest radius and score only there.
- **V_c:** CFG806 §3.1's forward model, inclination branches moment-0 q and Tadaki q4.4, pressure branches P-B and P0, never pooled.
- **Flux check:** total CO(3-2) against 0.79 ± 0.08 Jy km/s, within 30% or flagged: a resolved-out flux is reported, and the published flux governs L′.
- **Per reading:** α_CO,req at the measured V_c, with interval from V_c ± 1σ and M★ ± 0.2 dex. **Consistent** if the interval includes α_CO in [0.5, 6]; **in tension** if the whole interval lies outside; FLOOR when stars alone exceed the requirement at M★ − 0.2 dex.
- **Separation:** a pair of a₀ readings is called separated only if α_CO,req differs by more than the M★ interval on both. Otherwise "not separated". Expect this.
- **Forbidden:** pooling, choosing a branch after seeing V_c, exclusion statements, a law-form statement from one disc.
- **A scoring harness for this target must be committed before the cube is read; any measurement made without one is labelled a departure.**
- **Access:** the download needs the owner's yes with the file size stated, as CFG806 §1.

## 5. Checks (a failure is reported and kept)
- **K1** identity: separations 0.0 ± 0.1″ (U4_28473), 7.36 ± 0.05″ (U4_27928) from the archive's phase centre; both lines inside their windows.
- **K2** reproduction: Part A's machinery reproduces CFG571's U4 grid ≤ 1e-12 dex, AG4e and AG4d grid points likewise for F-DESI, F-flat, R-H, L-fb.
- **K3** seal hashes: PREDICTIONS_HASH be27457d…, AG4e 9802de0d…, AG4d d64727b5…, S3 b5d65a5e… unchanged.
- **K4** Newtonian round trip: ν ≡ 1 gives V_bar,req = V_c to < 1e-6, and all readings ≥ Newton at every R.
- **K5** route N reproduces S at lg M200 11 from the committed rule within 1%.
- **K6** S3 solver: a sealed U4 grid C value reproduced within 1e-3.
- **MUTATE:** set R31 ×10 in the L′ conversion; K7 (log M_gas from flux equals my hand value 11.3 ± 0.1 for α 4.36) must fail; exit 1. Outputs tagged `_MUTATE`.

## 6. Hand expectations, on record before running
- U4_27928: integrated S/N below 1 at its requirement; expected "G1 FAIL, upper limit", the limit above every framework requirement, so nothing scored.
- U4_28473: G1 passes. With α_CO 4.36 and M★ 11.31 the baryons alone give V well above Hα's 430 km/s, so α_CO,req falls near or below 1, or M★ must be lower.
- a₀(z) readings are not separated, because g/a₀ ≳ 5 where the CO reaches and M★ dominates the interval.

## 7. Files
`ac1_predict.py` (with `--mutate`), `ac1_predict.out`, `ac1_results.json`, `README.md`. One process, under 1 GB.
