# F1_cluster_cores — assumption ledger (written before any number; committed with the frozen criteria)

Failure under rebuild: raw KiDS shear stacked on 318 eRASS1 clusters is 1.91 ± 0.12 (canonical) / 1.75 ± 0.11 (alt) times
the law's prediction from the clusters' gas in MID (0.5–1.2 Mpc) (CFG687, `campaign_fresh_gravity/CFG687_erass1_shear_stack/`).
Neighbours read: CFG686 (8 ACCEPT clusters, same code), CFG688 (richness re-binning), CFG922 (baryon census: EXCESS STANDS),
CFG949 / CFG959 (untethered native debris fixes MID, FRAGILE), CFG951 / CFG954 / CFG962 (LDT / SCT rules: core untouched),
doors E1 (h = 0.70 convention flag), E2 (AQUAL with μ = x/(1+x)), E4 (R500 ±0.1 dex in M500), covariant C2 (native H₀ 67.2–68.6,
D_M/r_d unchanged), C4 (static limit AQUAL, ϕ = ψ: lensing = dynamics; K(Q) dust; BS mass μ⁻¹ ≫ 100 kpc, free).

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / EXTERNALLY-CALIBRATED.

## A. The original verdict (CFG687, via CFG686 RUN3 code)

| # | ingredient | class | file | note |
|---|---|---|---|---|
| A1 | KiDS-1000 SOM-gold e1, e2, weight, RA, DEC | RAW | `_external_data/kids_lensing_zsplit/KiDS_DR4.1_..._SOM_gold_WL_cat.fits` | sha256 in FETCH_LOG |
| A2 | Z_B point photo-z, cut Z_B > z_l + 0.2, ≤ 1.2; Σ_crit from Z_B (no n(z)) | SURVEY-CALIBRATION | cfg686_shear.py `esd()` | no dilution / n(z) correction |
| A3 | m = −0.01 multiplicative bias | SURVEY-CALIBRATION | cfg686_shear.py `M_BIAS` | |
| A4 | no boost (cluster-member dilution) correction | SURVEY-CALIBRATION (omitted) | cfg686_shear.py | dilution lowers the observed ΔΣ |
| A5 | random subtraction (1–3° offsets) | RAW (estimator) | cfg687_stack.py | M2 shows +2 M☉/pc² additive at OUTER |
| A6 | distances = raw DESI DR2 D_M/r_d × r_d with h r_d = 101.54 Mpc and **h = 0.70** (r_d = 145.06 Mpc) | RAW (BAO ratios) × ΛCDM-PROCESSED (h convention) | cfg686_shear.py `DM()` | native h is 0.672–0.686 (C2) |
| A7 | cluster centres = eRASS1 X-ray RA, DEC | RAW (X-ray) | erass1_main.tsv | miscentring not modelled |
| A8 | z = eRASS1 BEST_Z | RAW / SURVEY-CALIBRATION | erass1_main.tsv | |
| A9 | Mgas500 (1e11 M☉) | SURVEY-CALIBRATION (X-ray imaging fit), computed by eRASS1 in flat ΛCDM H₀ = 70, Ω_m = 0.3 distances — **not rescaled** to CFG687's distances (D^{5/2}) | erass1_main.tsv col 5 | Eddington / low-count priors |
| A10 | R500 (kpc): from M500 via a count-rate–mass relation calibrated on weak lensing with NFW / ΛCDM | ΛCDM-PROCESSED | erass1_main.tsv col 8 | used as gas aperture and to set r_c = 0.15 R500 |
| A11 | gas shape β = 2/3, r_c = 0.15 R500, extended to 3 Mpc | EXTERNALLY-CALIBRATED (assumed shape); 78 % of the gas budget is beyond R500 (CFG949) | cfg687_stack.py `law()` | |
| A12 | stars f* = 0.20 of gas (bracket 0.10–0.30) | EXTERNALLY-CALIBRATED | cfg687_stack.py | CFG922: measured stars are below 0.20 |
| A13 | kernel ν_mono (monotone repair of the RAR ν), applied algebraically g = g_N ν(g_N/a₀) | STANDARD-MOND-MACHINERY (QUMOND-form algebra) with a non-action kernel | CFG4_common.nu_mono / FP1 | the action's μ = x/(1+x) is not ν_mono's inverse |
| A14 | spherical symmetry; lensing mass = dynamical mass | FRAMEWORK-NATIVE (C4: ϕ = ψ) | | |
| A15 | the law's phantom halo extended to 30 Mpc (grid) | FRAMEWORK-NATIVE (isolated law) | RGRID | |
| A16 | no cold-sector (dust) mass | FRAMEWORK choice at the time | | V3 has BS dust, abundance an IC |
| A17 | a₀ footings 9.3603e-11 / 1.1312e-10 m/s², κ = ½ FITTED | FRAMEWORK-NATIVE (fitted) | CFG4_common.A0 | |
| A18 | jackknife over 30 RA-ordered patches | RAW (statistics) | cfg687_stack.py | |

## B. This rebuild (own pipeline, `f1_cluster_cores.py`)

| # | ingredient | class | handling |
|---|---|---|---|
| B1 | KiDS columns re-extracted from the FITS by my own reader (`f1_extract.py`) | RAW | cache in session scratch, not committed |
| B2 | same estimator conventions as A2–A5 (reproduction), then each correction one at a time | as A | |
| B3 | eRASS1 clusters read from the FITS `real_research/data/erass1cl_primary_v3.2.fits`, cross-checked against the TSV | RAW / SURVEY-CALIBRATION | |
| B4 | field equation: AQUAL ∇·[μ(|∇Φ|/a₀)∇Φ] = 4πGρ, μ = x/(1+x), spherical (exact Gauss-law solve) | FRAMEWORK-NATIVE (E2, C4) | AQUAL ≡ QUMOND-with-ν_simple in spherical symmetry (identity check); asphericity bounded, not solved |
| B5 | native background: r_d = 101.54/h, h ∈ {0.672, 0.686} (distances × 0.70/h) | FRAMEWORK-NATIVE (C2) on RAW BAO ratios | |
| B6 | eRASS1 gas rescaled from its ΛCDM(70, 0.3) distances to the pipeline's distances: Mgas × q^{5/2}, R500 × q (same angular aperture) | SURVEY-CALIBRATION (convention fix) | the ΛCDM(70, 0.3) convention of eRASS1 is an external fact (Bulbul+2024), labelled PROVISIONAL |
| B7 | R500 only as an aperture; bracket ±0.033 dex (±0.1 dex in M500) with the gas mass at fixed physical radius held | ΛCDM-PROCESSED, bounded | |
| B8 | gas-mass calibration against deep X-ray: ACCEPT Chandra n_e profiles (on disk) and X-COP M_gas(r) (on disk) for matched clusters | RAW (X-ray) / SURVEY-CALIBRATION | reported, used as a bracket |
| B9 | gas shape alternatives: G0 β-model to 3 Mpc (record); G1 X-COP median measured M_gas(<x)/M_gas(<1) shape; G2 measured aperture only (no gas beyond R500) | EXTERNALLY-CALIBRATED (G0), RAW X-ray (G1, but high-mass clusters), RAW-bound (G2) | |
| B10 | stars f* = 0.20 primary, 0.30 most favourable to the law | EXTERNALLY-CALIBRATED | no new census (CFG922 did it) |
| B11 | miscentring: per-cluster offset = |(RA,DEC) − (RA_XFIT,DEC_XFIT)| from the catalogue, applied to the prediction | RAW (catalogue positions) | sign: can only lower the predicted MID |
| B12 | boost (member dilution) from the data: source weight density around clusters / around randoms per bin | RAW | |
| B13 | Σ_crit with the SOM n(z) of each tomographic bin instead of Z_B (bin-only bound) | SURVEY-CALIBRATION (KiDS SOM n(z), on disk) | bound, not a calibration |
| B14 | two-halo / correlated structure at MID: bounded self-consistently by the OUTER residual over the law (clipped ≥ 0) | FRAMEWORK-NATIVE bound | the framework's own two-halo term is not computed (CFG967) |
| B15 | BS dust: the theory gives no cluster-core dust amount (abundance = IC, C2/C4; nonlinear profile not computed; BS mass μ free). Reported only: the dust needed under AQUAL (dust sources the field), and the cosmic-ratio-tracing-gas bracket Ω_c/Ω_b = 5.364 (CFG949) | FITTED (IC) / NOT DERIVED | never used to pass |
| B16 | no ΛCDM halo, no NFW, no HMcode, no mass function anywhere | — | |
