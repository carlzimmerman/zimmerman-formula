# X11_cross_shear_diagnosis: assumption ledger (written before any number; committed with the frozen criteria)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / LCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT.
"Inherited" = taken unchanged from X7 (`X7_cluster_core_significance/ASSUMPTION_LEDGER.md`), itself inheriting F1 and X2,
and classed as there.

## A. The verdict under test (X7's V1 and its CAL rule)

| # | ingredient | class | file | role here |
|---|---|---|---|---|
| A1 | KiDS-1000 SOM-gold e1, e2, weight, RAJ2000, DECJ2000, Z_B, PSF_e1, PSF_e2, THELI_NAME | RAW (shapes, positions, weights are lensfit SURVEY-CALIBRATION products) | `../_external_data/kids_lensing_zsplit/KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits` (outside the repo) | re-extracted by X7's extractor into session scratch (step 0) |
| A2 | Σ_crit from point Z_B, Z_B > z_l + 0.2, ≤ 1.2; m = −0.01 | SURVEY-CALIBRATION | F1 `esd()` via X7 `x7_measure.py` | inherited; m and n(z) not re-derived |
| A3 | F1's random positions (5–6 per cluster, 1–3°, seed 20261022, count acceptance) and random subtraction | RAW (estimator) | F1, X7 `x7_measure.py` | inherited; also null N1 |
| A4 | data boost B < 1 (graded), clipped B = 1 (reported) | RAW (measured) / convention | F1 A1, X2, X7 | inherited; E4 asks which applies |
| A5 | distances DESI DR2 D_M/r_d × 101.54/h, h 0.672 / 0.686 | RAW × FRAMEWORK-NATIVE (C2) | F1 `DM()` | inherited |
| A6 | eRASS1 RA_XFIT/DEC_XFIT, BEST_Z, MGAS500, R500, off_deg | RAW / SURVEY-CALIBRATION; R500 LCDM-PROCESSED | `real_research/data/erass1cl_primary_v3.2.fits` | inherited; z, MGAS500, off_deg define cluster splits |
| A7 | X2's C\* model (spherical AQUAL μ = x/(1+x), native h, eRASS1 gas × q^{5/2}, β-model + CFG814 r⁻³ beyond 2.2 R500, f\* = 0.20, catalogue miscentring, Chae+21 noclu EFE via F2's solver, reduced shear) | FRAMEWORK-NATIVE (law) + LITERATURE-INPUT (gas shape, f\*, field) + LCDM-PROCESSED (r200m = 2.2 R500, PROVISIONAL) | X2 `x2_cluster_outskirts.py`, F2 `f2_aqual.py` | inherited; here only the A-unit normalisation P (cross channel) and the model Σ (E2) |
| A8 | a₀ footings 9.3603e-11 / 1.1312e-10 m s⁻², κ = ½ | FRAMEWORK-NATIVE (FITTED) | CFG4_common, F1 `A0` | inherited, never pooled |
| A9 | LK-P PSF leakage (α, c per patch × tomographic bin), measured by X7 from the catalogue | SURVEY-CALIBRATION (coefficients measured here from RAW columns) | X7 `x7_psf_regression.py` | inherited (cross leakage +0.003 common to all classes) |
| A10 | 200 rotated-source realisations, splitmix64 hash of (row index, r) | RAW (statistics) | X7 `x7_measure.py` | reused unchanged; the per-class rotations draw the same angles |
| A11 | CAL rule: s_×² = max(0, offset² − σ_n²), tangential variance = cross variance (isotropic systematic) | statistical convention (declared by X7) | X7 criteria §3 | the assumption under test |
| A12 | cluster bootstrap (2000 draws) and X2's 30-patch jackknife; STAT = max | RAW (statistics) | X7 | inherited |

No STANDARD-MOND-MACHINERY enters (no ν_mono, no QUMOND, no additive EFE recipe; AQUAL = QUMOND only as F1's spherical
identity).

## B. This lane's inputs

| # | ingredient | class | source | note |
|---|---|---|---|---|
| B1 | MAG_AUTO (r-band detection-image magnitude) | RAW (photometry; zero points SURVEY-CALIBRATION) | KiDS FITS column `MAG_AUTO` | mag2 / mag4 splits; count slope for E2 |
| B2 | bias_corrected_scalelength_pixels | SURVEY-CALIBRATION (lensfit model fit) | KiDS FITS | size2 / size4 splits |
| B3 | PSF_Q11 + PSF_Q22 (PSF second-moment trace) | SURVEY-CALIBRATION (PSF model) | KiDS FITS | psfT4, tile-seeing groups |
| B4 | PSF ellipticity modulus and its tangential / cross projection about the call centre | SURVEY-CALIBRATION (PSF model) | KiDS FITS `PSF_e1`, `PSF_e2` | psfE4, psfx2, psft2 |
| B5 | neighbour_distance | SURVEY-CALIBRATION (lensfit deblending metadata) | KiDS FITS | blending proxy nbr2 |
| B6 | KiDS-1000 tomographic Z_B edges 0.1/0.3/0.5/0.7/0.9/1.2 | SURVEY-CALIBRATION (KiDS-1000 convention) | X7's LK-P groups | tomo split |
| B7 | Δz_ls edge from the catalogue's Z_B histogram and the clusters' z | RAW × FRAMEWORK-NATIVE (distances) | criteria §2 | dzls2 split ("source-plane separation" read as the line-of-sight separation behind the lens: an interpretation, declared) |
| B8 | class edges = lensfit-weight quantiles of the catalogue | RAW (statistics) | criteria §2 | fixed before any shear number |
| B9 | per-cluster tile-straddle fraction and m = 2 azimuthal coverage moment | RAW (geometry) | criteria §3 | cluster splits |
| B10 | extended random points: 20 per cluster, seed 20261025, F1's placement and acceptance rule | RAW (estimator) | criteria §3 | null N1 |
| B11 | thresholds Δχ² ≥ 9, p < 0.0027, |Z| < 3, |a/σ| < 2 (clean subset), Hartlap factor | statistical convention (declared) | criteria §5, §7 | 19 graded variables: look-elsewhere rate measured on the rotations, reported |
| B12 | weak-lensing magnification of counts, n ∝ μ^{α−1}, μ ≈ 1 + 2κ | LITERATURE-INPUT (standard lensing; no external number) | criteria §6 | E2 only |
| B13 | count slope α = 2.5 d log10(dN/dm)/dm from the catalogue's own MAG_AUTO counts, with brackets | RAW (with the assumption that the lensing selection acts on magnitude; soft selection makes it approximate) | criteria §2 | E2 only |
| B14 | κ for counts = X2's C\* Σ × the bin's mean Σ_crit⁻¹, scaled by the measured A_MID (bracket: unscaled law) | FRAMEWORK-NATIVE × RAW | criteria §6 | E2 only |
| B15 | the 90° position rotation is an algebraic identity (both channels flip sign) | mathematics | criteria §3 | recorded as a check, not as evidence |

Nothing is downloaded. Not on disk and not used (listed, not fetched): KiDS-1000 image simulations (m per class), star
catalogues for ρ-statistics, per-exposure PSF residual maps, a member catalogue for the clusters, n(z) per class.

## C. What a SYSTEMATIC verdict would and would not establish

- A split that names a variable establishes that the cross offset depends on it, not the mechanism. The clean-subset Z is
  the re-derived Z under the declared assumption that the clean classes carry no systematic.
- A FLUCTUATION verdict cannot exclude a systematic that is uniform across every declared split (a uniform systematic and a
  fluctuation give the same split pattern); it only removes the declared instrumental and cluster-property causes.
