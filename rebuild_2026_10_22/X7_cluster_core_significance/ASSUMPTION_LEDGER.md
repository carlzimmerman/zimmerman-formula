# X7_cluster_core_significance: assumption ledger (written before any number; committed with the frozen criteria)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / LCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT.
"Inherited" = taken unchanged from F1 (`F1_cluster_cores/ASSUMPTION_LEDGER.md`) or X2 (`X2_cluster_outskirts/ASSUMPTION_LEDGER.md`)
and classed as there.

## A. The verdicts under test (F1 PRIMARY, X2's V3 and terciles)

| # | ingredient | class | file | role here |
|---|---|---|---|---|
| A1 | KiDS-1000 SOM-gold e1, e2, weight, RAJ2000, DECJ2000, Z_B | RAW | `../_external_data/kids_lensing_zsplit/KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits` (outside the repo; sha256 in its FETCH_LOG) | re-extracted by my own reader (E1 equals F1's cache) |
| A2 | Σ_crit from point Z_B, Z_B > z_l + 0.2, ≤ 1.2; m = −0.01 | SURVEY-CALIBRATION | F1 `esd()` | inherited; m not re-derived |
| A3 | random subtraction, 5–6 randoms 1–3° away, F1 seed 20261022 | RAW (estimator) | F1 `f1_cluster_cores.py` | inherited; also the random-point stack of (b) |
| A4 | data boost B < 1 applied (F1 frozen PRIMARY); F1 A1 says the sign is wrong | RAW (measured) / convention | F1, X2 | graded as frozen; clipped reported |
| A5 | distances DESI DR2 D_M/r_d × 101.54/h, h 0.672 / 0.686 | RAW × FRAMEWORK-NATIVE (C2) | F1 `DM()` | inherited |
| A6 | eRASS1 RA_XFIT/DEC_XFIT, BEST_Z, MGAS500 (ΛCDM(70, 0.3) distances, × q^{5/2} in the model), R500 (× q) | RAW / SURVEY-CALIBRATION; R500 LCDM-PROCESSED | `real_research/data/erass1cl_primary_v3.2.fits` | inherited; catalogue MGAS500 (unrescaled) is the mass proxy of §4 |
| A7 | catalogue miscentring | RAW | F1 `predict(miscen=True)` | inherited |
| A8 | gas β = 2/3, r_c = 0.15 R500, r⁻³ beyond 2.2 R500 (CFG814), cut at 3 Mpc | LITERATURE-INPUT; r200m = 2.2 R500 LCDM-PROCESSED (PROVISIONAL) | X2 `gas(shape="P")` | inherited (C\*) |
| A9 | stars f\* = 0.20 × gas | LITERATURE-INPUT | F1 | inherited |
| A10 | spherical AQUAL μ = x/(1+x); lensing = dynamics | FRAMEWORK-NATIVE (E2, C4) | F1 `g_aqual_sph` | inherited |
| A11 | external field: Chae+21 noclu median, F2's exact axisymmetric AQUAL solve, F2 transplant | LITERATURE-INPUT (field) / FRAMEWORK-NATIVE (solver) | X2 (c1), `F2_outer_lensing/f2_aqual.py` | inherited (C\*); not measured at clusters |
| A12 | reduced shear forward-modelled with source moments m3…m8 | RAW (estimator physics) | X2 `redfac()` | inherited (C\*) |
| A13 | jackknife over 30 equal-count RA patches | RAW (statistics) | F1, X2 | inherited; compared with the bootstrap |
| A14 | X2's (e): cross shear and R−R band offsets added in quadrature, unreduced by their noise | RAW (statistics), conservative | X2 `stats(sysx=True)` | reproduced as CONS; replaced by CAL |
| A15 | a₀ footings 9.3603e-11 / 1.1312e-10 m s⁻², κ = ½ | FRAMEWORK-NATIVE (FITTED) | CFG4_common, F1 `A0` | inherited, never pooled |
| A16 | mass proxy for terciles: catalogue MGAS500 | SURVEY-CALIBRATION (X-ray imaging fit, ΛCDM(70, 0.3) distances, Eddington/low-count priors) | X2, CFG687 | inherited as the graded proxy |

No STANDARD-MOND-MACHINERY enters: the record's ν_mono (F1's R0 recipe) is not used; AQUAL = QUMOND-with-ν_simple only as
F1's spherical identity.

## B. This lane's inputs

| # | ingredient | class | source | note |
|---|---|---|---|---|
| B1 | PSF_e1, PSF_e2 per source (lensfit PSF model ellipticity at the galaxy position) | SURVEY-CALIBRATION | KiDS FITS columns `PSF_e1`, `PSF_e2` | non-finite → no leakage field, excluded from the fit |
| B2 | KiDS tile id THELI_NAME (THELI_INT cross-checked) | RAW (survey metadata) | KiDS FITS | LK-T groups |
| B3 | patch split N/S by RA (100°–260° = N) | RAW (footprint geometry) | — | LK-P groups |
| B4 | KiDS-1000 tomographic Z_B edges 0.1/0.3/0.5/0.7/0.9/1.2 | SURVEY-CALIBRATION (KiDS-1000 convention) | F1's C5d `TB` list | LK-P groups |
| B5 | linear additive model e = c + α e_PSF per group | LITERATURE-INPUT (standard KiDS / CFHTLenS form; no external coefficient used) | — | coefficients measured here from the data |
| B6 | rotated-source realisations, R = 200, splitmix64 hash of (row index, r) | RAW (statistics) | — | shape-noise expectation of every null stack |
| B7 | cluster bootstrap, 2000 draws, seed 20261024 | RAW (statistics) | — | compared with the jackknife; σ_STAT = max |
| B8 | excess-variance rule s² = max(0, offset² − σ_n²); isotropic systematic (tangential variance = cross variance) | statistical convention (declared) | criteria §3 | CAL |
| B9 | coherent additive ΔΣ offset across mass bins (κ_b scaling) | assumption (declared) | criteria §4 | CAL covariance for the trend |
| B10 | shape models S0/S1/S2, pivot = median MGAS500, step at X2's T1/T2 boundary | declared test shapes (no physics) | criteria §4 | no physics constant |
| B11 | eRASS1 M500 binning | LCDM-PROCESSED (count-rate–mass relation calibrated on weak lensing with NFW/ΛCDM) | eRASS1 FITS `M500` | reported only |
| B12 | X2's code (statistics, gas, model, reduced shear, EFE tables) and F1's functions, exec'd read-only from their source text | as A | `X2_cluster_outskirts/x2_cluster_outskirts.py`, `F1_cluster_cores/f1_cluster_cores.py` | sha256 recorded |
| B13 | no ΛCDM halo, no NFW, no mass function, no dark-matter particle in any prediction | — | — | |

Nothing is downloaded. Not on disk and not used (listed, not fetched): KiDS-1000's published per-bin α and c-term tables,
star catalogues for ρ-statistics, image simulations for the multiplicative bias, per-exposure PSF residual maps (the per-exposure
PSF_e columns exist but are not used).
