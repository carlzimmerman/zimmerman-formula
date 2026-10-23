# X5_mw_joint_baryons: assumption ledger (committed with FROZEN_CRITERIA.md, before any script or number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT.
LITERATURE-INPUT values from 2026-10-23 web look-ups are PROVISIONAL (search summaries, not the papers).

## Inherited by the verdicts being re-examined (P4 T4, U1 N6, S3 Part A)

| ingredient | class | file / source | used where |
|---|---|---|---|
| Bovy & Rix 2013 K_z,1.1(R)/2πG, 43 MAPs, R₀ = 8 kpc assumed, shifted by +0.122 kpc; σ ⊕ 5 % | SURVEY-CALIBRATION (outputs of Newtonian dynamical fits to SEGUE MAPs) | `real_research/data/mw_kz11_bovyrix2013_table3.tsv` | (i) χ²_Kz |
| Eilers+19 v_c(R), σ = stat ⊕ 2 % (P4) / ⊕ 3 % (CFG532 primary) / ⊕ 5 % (S2) | RAW + Jeans modelling (SURVEY-CALIBRATION) | `real_research/data/mw_rc_eilers2019_table1.tsv` | (i) v_c target 229.053 ± 4.645 at R₀; (ii) |
| R₀ = 8.122 kpc (GRAVITY 2018) | SURVEY-CALIBRATION | P4 `R0_MW`, S3 `s3_mw.R0` | (i), (ii) |
| McMillan17 baryons: disc vertical exponentials, thin/thick split, bulge shape, HI/H₂ | SURVEY-CALIBRATION; **partly ΛCDM-PROCESSED** (normalised in a joint fit with an NFW halo) | P4 `rho_mcm`; S3 `s3_mw.rho_mcm` | (i) shapes held; (ii) census baryons |
| McMillan17 stellar census 5.43 ± 0.57 × 10¹⁰ (s* scale in (ii) per-curve labels) | SURVEY-CALIBRATION, partly ΛCDM-PROCESSED | S3 `s3_mw.MSTAR_CENSUS` | (ii) reported labels only |
| Ou+24, Jiao+23, Wang+23, Zhou+23, Feng+26, SL23 DR3+ rotation curves and their error conventions | RAW + Jeans modelling (SURVEY-CALIBRATION) | `real_research/data/mw_rc_ou2024_table1.tsv`; `../_external_data/cfg532_work/src/<id>/` line ranges as S3 | (ii) |
| S2 error budget (5 % inner / 15 % beyond for Ou; 5 % Eilers; ⊕ 5 % stat-only curves; Jiao, SL23 as published) | SURVEY-CALIBRATION (top of the authors' stated systematic ranges) | CFG532 FROZEN_CRITERIA §5; CFG532b FROZEN_CRITERIA_v2 §1 | (ii) |
| One-curve-per-group combination, ρ = 0 / 0.5, labels | declared statistic (record) | CFG532b §2; S3 §2 | (ii) |
| MW external field e_N (hunt h81: LSS + M31 + LMC, Newtonian, from 2M++) along the disc axis (γ = 0) | ΛCDM-PROCESSED (2M++ reconstruction) | S3 `s3_mw.EN_H81` | (ii) v3 cell; e_N = 0 and 2 × h81 bracket it |
| Declared g_e = 0.03 a₀ along the axis (P4's round bracket) | declared value (no MW field on disk in P4's ledger) | P4 T4 | (i) robustness only |
| AQUAL ∇·[μ∇Φ] = 4πGρ_b with μ = x/(1+x) | FRAMEWORK-NATIVE (v3's static limit per E2/C4; the same function as standard MOND's "simple" μ) | `p4_solver.py`, `s3_aqual.py` | (i), (ii) |
| Screening: C4-literal stiffness, L★ = 24 pc scored (D10 floor 21.7 / 22.9), 90 pc bracket | FRAMEWORK-NATIVE (L★ FITTED, D10) | `p4_solver.py` | (i) |
| a₀ footings 9.3603e-11 / 1.1312e-10 m/s² (κ = ½ FITTED) | FRAMEWORK-NATIVE (fitted κ) | P4, S3 | (i), (ii) |
| χ² line χ²₀.₉₉(43) = 67.459; v_c line 2σ of the Eilers target | declared statistic | P4 FROZEN §T4; brief | (i) |
| QUMOND, the round rule (RM-v / RM-φ), ν_mono | STANDARD-MOND-MACHINERY / record rules not in v3 | CFG514, CFG516, CFG532 | **not used** here (record context only) |

## New in this lane (the prior box)

| ingredient | class | source | role |
|---|---|---|---|
| Σ_b(R₀) = 47.1 ± 3.4 M☉ pc⁻² (stars + gas, all z), grid ±2σ | LITERATURE-INPUT (star counts + gas census; no dynamics) | McKee, Parravano & Hollenbach 2015, ApJ 814, 13; in the record at `hunt_2026/g02_vertical_vs_planar_frequency_split.py`:53, 312 | (i) grid axis |
| M_bb = 1.88 ± 0.12 × 10¹⁰ M☉ (bar + bulge stellar mass), grid ±2σ | LITERATURE-INPUT, PROVISIONAL; **Newtonian-dynamics-derived** (made-to-measure models with a dark halo component in the fit: flagged ΛCDM-PROCESSED-adjacent) | Portail, Gerhard, Wegg & Ness 2017, MNRAS 465, 1621 (web look-up) | (i) grid axis |
| R_d = 2.6 ± 0.5 kpc (thin disc), grid ±2σ, applied to both discs | LITERATURE-INPUT (photometric/star-count review range) | Bland-Hawthorn & Gerhard 2016, ARA&A 54, 529; in the record at `hunt_2026/g02…py`:54 | (i) grid axis |
| Compact representation of the bar: McMillan17's bulge shape rescaled | modelling choice (declared) | this lane | (i) |
| One R_d for both stellar discs; thin share at R₀ and z_d held at McMillan17 | modelling choice (P4's B3 convention) | P4 `rho_b3` | (i) |
| Gas held at McMillan17 (its R₀ column is within 1σ of McKee+15's 13.7 ± 1.6) | SURVEY-CALIBRATION (held) | P4 `rho_mcm` | (i) |
| M★ tag: 6.08 ± 1.14 × 10¹⁰ M☉ (±2σ) | LITERATURE-INPUT, PROVISIONAL (meta-analysis assuming exponential discs) | Licquia & Newman 2015, ApJ 806, 96 (web look-up) | (i) tag only |
| R_d tag: 2.64 ± 0.13 kpc (±2σ) | LITERATURE-INPUT, PROVISIONAL | Licquia & Newman 2016 (arXiv:1607.05281; web look-up) | (i) tag only |
| S3 cached off-census solves (byte copies, keys by S3's rule) | record numerics (S3 A4 validated) | `rebuild_2026_10_22/S3_v3_mw_seals/_cache_final/` (read only) | (ii) C-table rows s ≠ 1 and s* only; census solved fresh |

Nothing is downloaded. No new constant enters any prediction: the grid values are published priors, and nothing is fitted.
