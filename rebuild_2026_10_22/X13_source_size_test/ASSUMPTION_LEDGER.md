# X13_source_size_test: assumption ledger (written before any number; committed with the frozen criteria)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / LCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT.
"Inherited" = taken unchanged from X11 (`X11_cross_shear_diagnosis/ASSUMPTION_LEDGER.md`), itself inheriting X7, F1, X2,
and classed as there.

## A. The result under test (X11's E3 size dependence) and its inherited inputs

| # | ingredient | class | file | role here |
|---|---|---|---|---|
| A1 | KiDS-1000 SOM-gold e1, e2, weight, RAJ2000, DECJ2000, Z_B, PSF_e1/e2, THELI_NAME | RAW (shapes, weights are lensfit SURVEY-CALIBRATION products) | `../_external_data/kids_lensing_zsplit/KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits` (outside the repo) | re-extracted into session scratch (step 0) |
| A2 | bias_corrected_scalelength_pixels and X11's w-quantile edges 1.4136 / 1.9020 / 2.5378 px | SURVEY-CALIBRATION (lensfit fit); edges RAW (statistics) | KiDS FITS; X11 `x11_extract_extra.py` | the split under test; edges reused unchanged |
| A3 | Σ_crit from point Z_B, Z_B > z_l + 0.2, ≤ 1.2; m = −0.01 | SURVEY-CALIBRATION | F1 / X7 / X11 | inherited; (d) tests the point-Z_B assumption against the SOM n(z) |
| A4 | F1's 326 clusters, random positions (seed 20261022, acceptance), random subtraction | RAW (estimator) | F1, X7, X11 | inherited; (b) |
| A5 | per-class boost B (graded), clipped B = 1 (reported) | RAW (measured) / convention | X7, X11 | inherited |
| A6 | distances DESI DR2 D_M/r_d × 101.54/h, h 0.672 / 0.686 | RAW × FRAMEWORK-NATIVE (C2) | F1 `DM()` | inherited |
| A7 | eRASS1 positions, BEST_Z, MGAS500, R500 | RAW / SURVEY-CALIBRATION; R500 LCDM-PROCESSED | `real_research/data/erass1cl_primary_v3.2.fits` | inherited (cluster list) |
| A8 | X2's C\* model (spherical AQUAL μ = x/(1+x), native h, eRASS1 gas × q^{5/2}, β-model + CFG814 r⁻³ beyond 2.2 R500, f\* = 0.20, catalogue miscentring, Chae+21 noclu EFE via F2's solver, reduced shear) | FRAMEWORK-NATIVE (law) + LITERATURE-INPUT + LCDM-PROCESSED (r200m = 2.2 R500, PROVISIONAL) | X2, F2 `f2_aqual.py` | inherited; only the A-unit normalisation P (ratios within a cell hardly depend on it) |
| A9 | a₀ footings 9.3603e-11 / 1.1312e-10 m s⁻², κ = ½ | FRAMEWORK-NATIVE (FITTED) | CFG4_common, F1 `A0` | inherited, never pooled |
| A10 | paired cluster bootstrap (2000), X2's 30-patch jackknife, STAT = max | RAW (statistics) | X7, X11 | inherited; this lane's draws use new seeds (1300 + index) |
| A11 | 200 rotated-source realisations (splitmix64 of row index, r) | RAW (statistics) | X7 | (b) noise |

No STANDARD-MOND-MACHINERY enters (no ν_mono, no QUMOND, no additive EFE recipe).

## B. This lane's inputs

| # | ingredient | class | source | note |
|---|---|---|---|---|
| B1 | PSF_Q11, PSF_Q22, PSF_Q12 → psfD = Q11 Q22 − Q12², r_psf = psfD^¼ | SURVEY-CALIBRATION (PSF model) | KiDS FITS | (c) resolution; only ln r_psf enters, so the units do not matter |
| B2 | model_SNratio | SURVEY-CALIBRATION (lensfit) | KiDS FITS | (c) SNR |
| B3 | FLUX_RADIUS (SExtractor circular half-light radius, PSF-convolved) | RAW (photometry) | KiDS FITS | (f) reported only |
| B4 | circularised size r_ab = size √((1 − |e|)/(1 + |e|)) | SURVEY-CALIBRATION × convention | cache e1, e2, size | (f); assumes B11 |
| B5 | within-quartile halves (PSF size, SNR), circ/frad quantiles, ±0.05 ln bands | RAW (statistics, catalogue only) | criteria §2 | fixed before any shear number |
| B6 | KiDS-1000 SOM n(z) per tomographic bin, blind C, 0.05 steps | SURVEY-CALIBRATION (spectroscopic SOM calibration) / LITERATURE-INPUT | `../_external_data/kids_lensing_zsplit/KiDS1000_SOM_N_of_Z.tar.gz` (extracted to scratch) | (d) H_SOM; full-bin n(z), not per size class (none on disk) |
| B7 | H_SOM: within a tomographic bin, the true n(z) does not depend on size | hypothesis (the KiDS calibration's own granularity) | criteria §5d | (d) bounds the photo-z share; per-class n(z) not on disk |
| B8 | F2's lens catalogue (181,477 KiDS-bright galaxies, z 0.10–0.50, LePhare masses) and 50 patches | RAW positions / photo-z SURVEY-CALIBRATION | `real_research/data/lensing_rar/lr_lenses.npz`, `cfg96_stack.npz` | (e); masses unused |
| B9 | P2's native estimator and bins (flat Ω_m 0.3085, h 0.679; 0.03–3 Mpc, 15 bins) | FRAMEWORK-NATIVE background (C2) × RAW | P2 `p2_spec_isolated_lensing.py` | (e); a ratio of halves, so the background hardly matters |
| B10 | template T ∝ 1/R for the galaxy amplitude | statistical convention (shape only) | criteria §5e | cancels in the half ratio if the halves share a profile shape |
| B11 | lensfit scalelength = semi-major-axis exponential scalelength; lensfit e = (a − b)/(a + b) | LITERATURE-INPUT (recalled from the KiDS/lensfit papers; not verified, no download) | criteria §5f | (f)'s prediction; the circ2 gate and the alternative-convention numbers test it |
| B12 | first-order shear response of a size cut: δ ln a = g∥; ε' = (ε + g)/(1 + g* ε) | mathematics (standard lensing) | criteria §5f, K2 | checked by the exact-transform injection K2 |
| B13 | thresholds: 2σ (E classes, bands, gate), f ≥ 0.70 / < 0.30, σ_f ≤ 0.40 | statistical convention (declared; the 70 / 30 % lines are the brief's) | criteria §5–6 | |
| B14 | random points for galaxies: one per lens, F1's placement and acceptance, no retry | RAW (estimator) | criteria §4 | (e) |

Nothing is downloaded. Not on disk and not used (listed, not fetched): KiDS image simulations (m per size, SNR, resolution;
the selection response measured on sheared images), per-class SOM n(z), spectroscopic redshifts for the sources, a cluster
member catalogue.

## C. What each verdict would and would not establish

- SOURCE-SIDE SYSTEMATIC names a source property or measurement effect that reproduces the size dependence; it does not by
  itself say whether the all-source amplitude is biased. That is what the frozen correction (§7) answers, under the
  declared assumption of the correcting mechanism. A split-induced selection (f) biases the halves in opposite directions
  and leaves the all-source sample unbiased to first order.
- CLUSTER-SPECIFIC says the dependence is absent around galaxies and not explained by the declared source properties; it
  does not identify a cluster mechanism.
- UNDECIDED leaves X11's caveat ("unexplained source-size dependence") in place.
