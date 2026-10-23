# F2_outer_lensing: assumption ledger (written before any script or number of this lane)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY.
Paths are repo-relative. "Record" = the original verdict chain CFG801 → CFG804 → CFG902 (→ CFG903).

## A. Inputs of the original verdict (CFG804 / CFG902 / CFG903)

| # | ingredient | class | source | note |
|---|---|---|---|---|
| R1 | B21 Fig. 3 ESD profiles, 4 M★ bins × 15 R, released covariance, (1+K) | RAW (with SURVEY-CALIBRATION: shear m, lens/source photo-z) | `real_research/data/lensing_rar/brouwer2021_rar/Fig-3_*` | h70 units, B21 fiducial flat ΛCDM Ω_m 0.2793, h 0.70 for D_A and Σ_crit → ΛCDM-PROCESSED distances (CFG885) |
| R2 | B21 "isolated" selection (no neighbour > 0.1 M★ within 3 Mpc, photo-z) | SURVEY-CALIBRATION | B21; record reconstruction `lr_lenses.npz` (|Δχ| < 10 Mpc, count-calibrated) | CFG502: same-z veto probability only ~7 % ⇒ leaked satellites |
| R3 | the law B: spherical ν-law profile ρ ∝ 1/(2πs√(1+4s²)) of a point mass, no EFE | FRAMEWORK-NATIVE (= AQUAL in spherical symmetry) | `cfg804.py` | the isolated-sphere AQUAL = QUMOND identity makes it clean; no EFE term = an assumption g_ext = 0 |
| R4 | masses M_b profiled per bin (4 knobs), grid 9–12 dex | fit | `cfg804.py` | profiled masses sit 0.1–0.3 dex above the catalogue means (CFG801, CFG903) |
| R5 | catchment supply N = 1/f_ret(M_ta), f_ret census ramp (floor 0.10) | SURVEY-CALIBRATION + record census, provenance UNTRACEABLE (CFG886 T5) | CFG416 / CFG556 via `cfg804.py` | this is what makes the edge; a supply-limited phantom is the old "medium = phantom" bookkeeping |
| R6 | cosmic ratio 5.364 = Ω_c/Ω_b | ΛCDM-PROCESSED (Planck) | `cfg804.py` | E1: 5.272 (BAO+BBN) / 6.122 alternatives |
| R7 | Msun/h convention, h = 0.674 (CFG902 R1) | ΛCDM-PROCESSED convention | CFG902 | h from Planck ΛCDM, not native |
| R8 | a₀ footings 9.3603e-11 / 1.1312e-10 | FITTED (κ = ½); alt is ΛCDM-PROCESSED (E1) | doors BRIEF | never pooled |
| R9 | CFG903 neighbours: LePhare + 0.15 dex M★, f_cold, catchment cold energy 5.364 N M_b on the truncated law | SURVEY-CALIBRATION + R5 | CFG903 | framework-native in form, but supplied by R5 |
| R10 | CFG805 two-halo: T1x P_grav, free bias per bin | FRAMEWORK-NATIVE engine with inherited ΛCDM ICs + 4 free knobs | CFG805 | knobs ⇒ not usable in a verdict |
| R11 | CFG502 two-halo: NFW + Moster/inverse SHMR + b ξ_lin | ΛCDM-PROCESSED | CFG502 | excluded from any verdict (owner rule) |
| R12 | QUMOND vs AQUAL | — | — | for the isolated sphere they coincide; the record never needed the distinction until an EFE is added |

## B. Inputs of this rebuild

| # | ingredient | class | source | error / bracket |
|---|---|---|---|---|
| D1 | B21 Fig. 3 ESD + covariance (Track A) | RAW + SURVEY-CALIBRATION | as R1 | released covariance; (1+K) applied |
| D2 | record per-lens re-measurement in B21's 15 g_bar bins, 50 patches (Track B) | RAW (record's own stack of the KiDS-1000 SOM-gold shear catalogue) | `cfg110_perlens.npz`, `cfg96_stack.npz`, `cfg96_isoflags.npz`, `lr_lenses.npz` (stage scripts `campaign_fresh_gravity/CFG110_stage_perlens.py`, `CFG96_stage_stack.py`) | jackknife; fid Ω_m 0.3, h 0.70 distances (ΛCDM-PROCESSED, rescaled below) |
| D3 | neighbour pool for S_strict | RAW photometry + SURVEY-CALIBRATION (ANNz2 photo-z, LePhare M★) | `KiDS_DR4_brightsample*.fits` (record's pool definition) | photo-z pair σ ≈ 115 Mpc (CFG502, measured) |
| B1 | M★ (LePhare MASS_MED + 0.15 dex fluxscale) | SURVEY-CALIBRATION (SPS) | `lr_lenses.npz` | ±0.2 dex systematic (E1) |
| B2 | cold gas log f_cold = −0.69 log M★ + 6.63 | SURVEY-CALIBRATION (scaling relation, B21) | `real_research/reviews/lensing_rar/lr_esd_remeasure.py` L89 | ±0.2 dex bracket (stated, not measured here) |
| B3 | hot CGM f_hot M★, uniform 100 kpc sphere, central 0.5, bracket [0, 1.0] | SURVEY-CALIBRATION, derived: f = 0.8 √(L_X,obs / L_pred(0.8 M★)) with CFG580's recorded APEC luminosities for 0.8 M★ (Z 0.3: 0.98–2.9e40; Z 1: 3.2–9.5e40 erg/s) and the recorded eRASS:4 stack L_X = 1.1e40 (Zhang et al. 2025 T3, as recorded in `campaign_fresh_gravity/closure_map/KIDS_HOT_GAS_ESCAPE_NOTE_2026-09-29.md`) ⇒ 0.27–0.85; 1.0 ≈ the metal-poor escape edge (CFG580) | quiescent log M★ 10.5–11 stack applied to all lenses (stated extrapolation); not verified from the paper on disk |
| F1 | AQUAL, μ = x/(1+x), lensing potential = dynamical potential | FRAMEWORK-NATIVE | C4 K1/K2, E2, THEORY_V3 §1 | — |
| F2 | screening L★ ≥ 21.7 pc | FRAMEWORK-NATIVE (fitted bound) | D10 | irrelevant at R ≥ 35 kpc (not computed) |
| F3 | BS K(Q) dust: abundance = initial condition; no galaxy-bound profile predicted | FRAMEWORK-NATIVE (OPEN) | C2, C4, THEORY_V3 §2 | T has no dust term; required dust reported as output |
| F4 | no catchment edge (phantom is a field response) | FRAMEWORK-NATIVE | C4 (Khronon escapes the D-T "medium = phantom" identity) | this removes R5–R7 from the one-halo |
| E1 | external field y_e (Newtonian, uniform): 0 / Chae+21 noclu median / maxclu median | SURVEY-CALIBRATION (SPARC-local environments, not KiDS) | `real_research/reviews/directional_efe_2026/laneB_data/chae21_env.csv` | bracket; the EFE equation itself is AQUAL (F1), not an algebraic EFE recipe |
| H1 | native h 0.679 (0.672–0.686) | FRAMEWORK-NATIVE (BBN-bounded) | C2 K5 | ends reported |
| H2 | Ω_m 0.3085; T_Ωm 1.0128 (B21) / 1.0037 (record stack) | SURVEY-CALIBRATION / record-computed | CFG682, CFG885 `cfg885_results.json` | Ω_m enters at ≤ 1.5 % |
| C1 | source photo-z / Σ_crit ± 3 % | SURVEY-CALIBRATION | KiDS-1000 SOM δz (order of magnitude; stated) | bracket |
| C2 | shear m: (1+K) = 0.9853 | SURVEY-CALIBRATION | B21 bias column | — |
| C3 | boost (lens-source clustering) | not corrected (B21 releases none) | — | affects inner radii only; stated |
| G1 | the stacked lens-mass distribution per bin | SURVEY-CALIBRATION | `lr_lenses.npz` + `cfg110_perlens.npz` weights | record's 181,477 vs B21's 259,383 lenses |

No ΛCDM-PROCESSED or STANDARD-MOND-MACHINERY ingredient enters a verdict line of this lane; the native-distance
rescaling replaces the ΛCDM distances (residual: Ω_m from CFG682 ≤ 1.5 %).
