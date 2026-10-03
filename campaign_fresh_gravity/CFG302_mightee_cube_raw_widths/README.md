# CFG302: raw HI widths and fluxes re-measured from the MIGHTEE-HI DR1 r1p0 cubes and compared with the catalogue's busy-function values

*This lane checks raw measurements; it does not measure a₀. Owner direction (2026-10-02): "keep going with the MIGHTEE cubes lane" and "we must use empirical evidence raw and unfiltered". No a₀ number is computed. At z ≤ 0.093 nothing here can separate FLAT from a₀ ∝ H(z). κ = ½ is FITTED. The only verdict words used are the frozen map entries.*

## Bottom line (the frozen map, from the first run)
1. **The widths agree.** We measured W50 on the raw r1p0 aperture spectra with the outside-in 50 %-of-peak rule, in the galaxy rest frame. Against the catalogue's busy-function W50, the median log ratio is **−0.022 dex** (ours are 5 % narrower) and the robust scatter is **0.039 dex**, over **n = 58** detections. Map entries: **WIDTH-SCALE AGREES** (tolerance 0.03 dex) and **WIDTH-SCATTER CONSISTENT WITH THE ERRORS** (4 of 58 pull outliers). Ten sources lie beyond 3 robust σ. Seven of them are wider than the catalogue, and six have a catalogued neighbour inside the 113″ aperture: this is confusion at a 75″ beam. Without the neighbour-flagged sources the median is −0.025 dex. If the catalogue quotes observed-frame widths, the median becomes +0.003 dex; this lane does not decide the catalogue's convention (± 0.025 dex).
2. **The fluxes do not agree.** The median S_win/S_cat over all **179** primary sources (non-detections included) is **0.22** (robust scatter 0.30). Over the 58 detections the median log ratio is **−0.30 dex** (a ratio of 0.50) with a scatter of 0.24 dex. Map entries: **FLUX-SCALE DIFFERS (lower)** and **FLUX-SCATTER NOT CONSISTENT** (46 of 58 pull outliers; median pull −5.6). Only **58 of 179** sources reach the frozen S/N_L ≥ 5. The catalogue's SNR_3D has a median of 15 for the detected sources and 6.9 for the rest.
3. **No resolved rotation curves at r1p0.** The restoring beam is circular, **74.2–77.3″** per channel (median 75.85″; 8″ pixels; BUNIT Jy/beam). The largest 3σ moment-0 extent is **3.10 beams** (MGTH_J095713.0+015456); T1 reaches 2.90. No source reaches 6 beams, so no PV extraction ran on the data.
4. **Controls:** the main run passes **12 of 13**. **C-OFF(b) FAILED** and is kept (details below). MUTATE=1 passes **8 of 8**. The cross-instrument check **C-T1 passes**: T1's r1p0 W50 is **384.6 ± 3.2 km s⁻¹**, against CFG300's r0p0 value of 380.1 (catalogue 392 ± 12).
5. **For CFG301:** `cfg302_per_galaxy.csv` gives independent raw widths. Use the column `W50_rest_kms` with the flag `W50_defined` (58 sources). The widths are already in the rest frame, so **do not divide them by (1 + z) again**. For a recipe that does divide, use `W50_obsframe_kms`. Do not use our fluxes as HI masses: the flux deficit is unexplained (see the post hoc section).

## Process (everything kept)
1. **Criteria** were committed as `7d317dd4f` before any spectrum was extracted. Disclosed there: the headers, the beam tables, one nine-plane peek at the centre of sub-cube 0001-1055, and the catalogue counts.
2. **Dry run** of the script on a fabricated cube before the first real run: real headers, WCS and beams, with fake noise and fake galaxies at the catalogue positions; no real voxel was read. Width and flux ratios came back near 1, as built. The harness lived in a scratch folder and is not part of the lane.
3. **Main run, once** (`*_run1*`), then **MUTATE=1, once** (`*_MUTATE_run1*`).
4. **One output-only fix:** the per-galaxy CSV had been written with `%.6g`, which rounded input columns too (freq_MHz 1383.623 → 1383.62). It is now written with `%.10g`, and both runs were repeated. The main and MUTATE JSONs are **identical** before and after, the `.out` files differ only in their timing and memory lines, and the CSVs differ by ≤ 5 × 10⁻⁶ relative (the old rounding). The un-suffixed outputs are the repeats.
5. **Post hoc diagnostics** (`cfg302_posthoc_diagnostics.py`) have their reading rules in the docstring, fixed before the first post hoc run. There were three runs: `_run1`, `_run2`, and the final un-suffixed output (see Errors and corrections).
6. Runtime is about 17 s for each frozen run, including sha256 of the 24 GB of cubes. Peak resident memory is about 0.76 GB, and no cube-sized file was written.

## The frozen measurement (main run)
| quantity | value |
|---|---|
| sample (golden, 0.02 ≤ z ≤ 0.093) | 188; plus controls T1 and T3 (not golden) = 190 measured |
| flags in the sample | BEAMFLAG 7 (line window in the placeholder-beam channels, ν ≤ 1300.13 MHz), NAN 2, EDGE 0, TRUNC 0 → **primary set 179**; STITCH 26 (2 detected); NBFLAG 38 (included) |
| aperture and noise | R_ap = 1.5 θ ≈ 113″; aperture noise median 0.354 mJy per channel; f_corr median 0.81 |
| detected (S/N_L ≥ 5) | 58 of 179 (by z tercile: 27/59, 22/47, 9/73); median S/N_L of all 179 is 2.0 |
| W50 ratio (n 58) | median −0.0224 dex, robust scatter 0.0391, mean +0.023, std 0.194; our median error 12.4 km s⁻¹ (catalogue 7.0); W20/W50 median 1.45 (45 with W20 defined) |
| W50 outliers > 3 robust σ | J100222.5+030247 (135 vs 39), J095713.6+020705 (554 vs 89), J095641.0+021014 (679 vs 390), J100349.3+021616 (77 vs 107), J100058.6+022522 (205 vs 132), J100137.0+020623 (302 vs 67), J100236.5+014618 (437 vs 97), J100143.6+021953 (67 vs 129), J100320.1+015351 (66 vs 93), J095919.3+025959 (470 vs 250) |
| flux ratio | all 179: median 0.222; detections: −0.3035 dex (0.497), scatter 0.243; without NBFLAG 0.41; outliers > 3σ (all high, all with a neighbour): J100222.5+030247 (×39), J095713.0+015456 (×3.7), J100058.6+022522 (×4.2) |
| Spearman correlations | R_W against z −0.06, against S/N_L −0.05; R_S against z −0.33, against S/N_L +0.54 |

**CFG300's targets at r1p0.** T1: W50 384.6 ± 3.2, W20 406.5, flux ratio **0.96** (CFG300: 0.57 masked and 0.76 unmasked at r0p0, 0.85 at r0p5). The r1p0 aperture includes the catalogued neighbour MGTH_J100352.4+022534. T2 (in the sample): W50 148.9 ± 77.5 (CFG300 140.5 masked; 145.9 and 157.0 unmasked; catalogue 167 ± 7), flux ratio **0.38**, matching CFG300's unmasked 0.36 at a different weighting, so T2's deficit is in the cubes. T3: W50 77.4 ± 6.7 (CFG300 74.6, 86.3 and 81.9; catalogue 101 ± 7), flux ratio 0.62 (CFG300 0.59 and 0.71).

## Controls
| control | result |
|---|---|
| S1 width rule on a noise-free synthetic profile | PASS (152.44 vs truth 151.85 km s⁻¹) |
| S2 aperture flux of a synthetic point source | PASS (0.998) |
| S3 PV code on a synthetic 8-beam disc | PASS (+4/−4 bins, ρ −0.95, receding side as built) |
| C-INT size and sha256 against the manifest | PASS (all four) |
| C-GRID frequency grid, BUNIT | PASS |
| C-OFF(a) false detections in the line-free offset windows | PASS (0 of 170; 9 with a neighbour inside O not counted) |
| **C-OFF(b)** robust std of S/N_win in the offset windows within [0.75, 1.33] | **FAIL: 0.489** (S/N_L 0.497) |
| C-OFF(c) median offset S/N within ± 0.5 | PASS (+0.058) |
| INJ(a) injected W50 recovered within ± 0.03 dex | PASS (−0.0040 dex, n 125) |
| INJ(b) injected flux recovered within ± 0.03 dex | PASS (+0.0018 dex, n 176) |
| INJ(c) width-pull robust std within [0.4, 1.5] | PASS (0.867); injection detections 127 of 179 against 58 in the main run |
| C-T1 T1 within max(25, 3σ) of CFG300's r0p0 W50 | PASS (384.6 vs 380.1) |
| C-BEAM median FWHM_eq/θ (20 brightest) within [0.85, 1.6] | PASS (0.952; range 0.87–1.47) |
| MUTATE M1 width-defined in the shifted window ≤ 5 % | PASS (0 of 179) |
| MUTATE M2 detected in the shifted window ≤ 5 % | PASS (0 of 179) |
| MUTATE M3 T1's width collapses | PASS (undefined, S/N_L 0.11) |

**Hand estimates (scored as they fell).** HE3 (width ratio 0.950), HE4 (no source at 6 beams), HE6 (C-T1) and HE7 (largest extent 3.10 ≤ 4) hit. **HE1 MISS** (58 detected, against 90–175). **HE2 MISS** (flux ratio 0.222, against 0.70–1.10). **HE5 MISS** (C-OFF(b); M1–M3 passed).

## Post hoc diagnostics (2026-10-02; NOT frozen; no map entry or check of the frozen runs is changed)
- **PH0** passes in the final run: the re-extraction reproduces the CSV's S_win and W50 to 1e-5 for all 179 sources.
- **PH1, noise at long spectral lags.** We pooled the variance of n-channel block sums over n σ_ch². It is **1.00 at n = 1, 0.84 at 8, 0.36 at 32 and 0.16 at 128**. The aperture spectra behave as if high-pass filtered on scales of roughly 10–30 channels (60–175 km s⁻¹). The frozen σ_S assumes no correlation beyond 8 channels, so it over-states window-sum errors by about 2×. Rescaling the C-OFF S/N with the measured F(n) gives a robust std of **1.05**, so PH1 explains the C-OFF(b) failure. One consequence: the frozen S/N_L values are about 2× too small, which makes S/N_L ≥ 5 an effective threshold of about 10σ.
- **PH2, recalibrated threshold.** k = 0.497, so a calibrated 5σ is S/N_L ≥ 2.48. At that threshold 83 of 179 sources are detected, with **0** false detections in both the offset and the MUTATE windows. The 79 sources with a finite W50 give a width ratio of **−0.015 dex** (scatter 0.082) and a flux ratio of **−0.385 dex** (scatter 0.26).
- **PH3, what the flux deficit depends on.**
  - Over all 179, the median S_win/S_cat by catalogue-SNR_3D tercile is **0.05, 0.23 and 0.36**.
  - Within the recalibrated detections, the ratio falls with W50_cat at fixed SNR_3D (ρ −0.30, p 0.007) and with z (ρ −0.41, p 2 × 10⁻⁴). That is consistent with spectral filtering of broad lines.
  - By the rule, the rise with SNR_3D is not significant within the detected set (ρ +0.20, p 0.08).
- **PH4, aperture completeness.** S(2.5θ)/S(1.5θ) = **1.002**, so the frozen aperture is complete and the missing flux is not outside it.
- **PH5, stacked spectra** (added after post hoc run 1). The stacked line holds **0.60 ± 0.05** of the catalogue's mean flux density. **No negative bowls** appear beside the lines (+1.0σ), so the stack does not confirm the filter hypothesis.
- **Reading.** The r1p0 cubes hold about half of the catalogue flux for the detected sources and far less for the faint ones. The aperture is complete (PH4) and the beam matches the source sizes (C-BEAM). Three causes remain open, and this lane cannot separate them:
  - spectral filtering in the released cubes (PH1's noise signature and PH3's W50 trend, but no bowl in PH5);
  - catalogue fluxes extracted differently, or boosted near the detection limit;
  - residual-flux (dirty-beam) scaling of uncleaned emission at r1p0.

  The deficit agrees with CFG300's r0p0 and r0p5 cutouts, which come from different imaging of the same visibilities.

## Errors and corrections
- **C-OFF(b) failure.** The frozen error model assumed the noise correlation stays within 8 channels. The data show strong anticorrelation out to more than 100 channels (PH1). The failure is kept. The frozen detection counts and pulls are therefore conservative: about 2× too few S/N units. M1 and M2 also pass at the calibrated threshold (PH2).
- **Post hoc PH0, run 1:** it demanded 1e-9 relative against a CSV written to 6 significant figures, a design flaw in the check, so it failed for all 179 sources. **Run 2:** it failed for 37 sources because that CSV had also rounded freq_MHz. The fix raised the frozen script's CSV precision only, with identical computations (Process, step 4). Both post hoc runs are kept (`_run1`, `_run2`). PH2 and PH3 read only the CSV and are unchanged. PH1 and PH4 moved slightly because of the rounded window centres (F(8) 0.837 → 0.843, PH1b 1.021 → 1.053, S(1θ)/S(1.5θ) 0.984 → 0.987). The final run is the reference. **PH5 was added after run 1**, with its rule written into the docstring before run 2. The final run also corrected the PH0 label, with numbers unchanged.
- In the frozen criteria, the data-assembly README's phrase "a 40″ taper" for r1p0 is quoted as found. The restoring beam in the headers is about 75″, and C-BEAM supports it.
- The beam table of sub-cube 0001-1055 says TUNIT arcmin, but its values are in arcsec. Its channels 0–383 carry placeholder beams (10.0, 5198.39). The sources concerned are flagged (BEAMFLAG) and excluded from the primary statistics.

## What this does not say
- It is not an a₀ measurement, and it cannot separate the laws.
- The widths are not inclination corrected (neither are the catalogue's).
- At a 75″ beam, the 113″ aperture holds any HI inside it. NBFLAG lists only the catalogued neighbours.
- The injection is added after imaging. It cannot test anything done to the cube before release, such as continuum subtraction or cleaning.
- The catalogue's velocity convention is not decided (± 0.025 dex).
- r0p0 and r1p0 share visibilities, so C-T1 compares two imaging weightings of the same data, not independent observations.
- The cause of the flux deficit is open (above).
- The catalogue has no optical position-angle column, so any PV cut would have used the HI axis. None was needed.

## Files
- **Frozen inputs and code:** `FROZEN_CRITERIA.md` (committed `7d317dd4f`) and `cfg302_raw_widths.py` (the main run, or `MUTATE=1`; the cube folder comes from `$MIGHTEE_R1P0_DIR`, default `../_external_data/mightee_hi_dr1` relative to the repository root).
- **Main run:** `cfg302_raw_widths.out` and `_results.json`, plus `cfg302_per_galaxy.csv` (190 rows: our widths, errors and fluxes with flags, catalogue values, offset-window and injection columns). First run: `*_run1*`.
- **MUTATE run:** `cfg302_raw_widths_MUTATE.out`, `_MUTATE_results.json` and `cfg302_per_galaxy_MUTATE.csv`. First run: `*_MUTATE_run1*`.
- **Post hoc:** `cfg302_posthoc_diagnostics.py`, with `.out` and `_results.json` (final) and the `_run1` and `_run2` outputs.
