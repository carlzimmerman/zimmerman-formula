# S2_v3_lowg_lensing: assumption ledger (written before any script or number of this lane)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / FITTED / POSIT.
Paths are repo-relative.

## A. Inputs of the verdicts being recomputed (tiles 17 and 30)

| # | ingredient | class | source | note |
|---|---|---|---|---|
| O1 | B21 RAR ESD in g_bar bins (Fig-8 colour bins, Fig-4-5-C1 all isolated), covariance, (1+K) | RAW + SURVEY-CALIBRATION (shear m, photo-z) | `real_research/data/lensing_rar/brouwer2021_rar/` | ESD in h70 with B21's flat ΛCDM distances (Ω_m 0.2793): ΛCDM-PROCESSED distances, rescaled by CFG885 |
| O2 | B21 g_bar = G M★(1+f_cold)/R², point mass | SURVEY-CALIBRATION (SPS M★, cold-gas scaling) | B21; CFG829 uses the labels as published | hot gas not included (B21's hot-gas variant unused) |
| O3 | the law g_bar ν_e(g_bar/a₀), algebraic, no EFE | FRAMEWORK-NATIVE kernel of the time (ν_e), but **EFE-free = an assumption g_ext = 0**; algebraic g compared to 4GΔΣ | `cfg829.py` | the isolated "class-A" law; v3 has an EFE everywhere (N0 finding 1) |
| O4 | g_obs = 4G·ESD (B21 Eq. 7) | SURVEY-CALIBRATION (estimator; exact for an SIS) | B21; CFG926 R6 measured the bias at 0.004 dex | applied to data only in CFG829 |
| O5 | "supply suffices ≤ 0.31 Mpc" | catchment supply rule (CFG804/902), census f_ret UNTRACEABLE (CFG886) | CFG804, CFG902 | not in v3 (F2: removing the edge = law B) |
| O6 | CFG667 +0.123 dex on red-lens M★ | SURVEY-CALIBRATION (Taylor+11 colour–M/L vs LePhare, OLD − YOUNG) | `campaign_fresh_gravity/CFG667_kids_age_anatomy/cfg667_results.json` | an estimator choice; which estimator is right is not decided (CFG667 §3) |
| O7 | IMF α–σ: log α_Salp = −0.0748 + 0.0986 log(σ/200), log σ = 2.1496 + 0.2792 (log M★ − 10.5), S/C = 1.778 | POSIT with SURVEY-CALIBRATION inputs (ATLAS3D JAM with Cappellari's NFW halos; SLACS S/C) | `CFG926_small_reframings_B/cfg926_results.json` (relation) | the JAM halos are ΛCDM-shaped (CFG926's R5-law variant with the framework's ν moves D_red 0.172 → 0.168 / 0.154); premise: discs stay Chabrier |
| O8 | a₀ footings | FITTED (κ = ½); alt is ΛCDM-PROCESSED (E1) | doors BRIEF | never pooled |

## B. Inputs of this recompute

| # | ingredient | class | source | bracket |
|---|---|---|---|---|
| D1 | B21 RAR files as O1 | RAW + SURVEY-CALIBRATION | as O1 | released covariance |
| D2 | record lens catalogue (181,477 lenses, B21-style isolation at \|Δχ\| < 10 Mpc), its M★, Mgal, z, typ | SURVEY-CALIBRATION (photo-z isolation, LePhare M★) | `lr_lenses.npz` (stage `campaign_fresh_gravity/CFG96_stage_stack.py`) | proxy for B21's 259k lenses (F2 ledger G1) |
| D3 | per-lens Σ_crit⁻²-weighted source weights per g_bar bin | RAW (record's own KiDS-1000 stack) | `cfg110_perlens.npz` | used as model weights only |
| D4 | lens colour: record typ (u−r > 2.0, LePhare MAG_ABS valley); variant u−r > 2.5 reconstructed | SURVEY-CALIBRATION | `lr_esd_remeasure.py` L87; `KiDS_DR4_brightsample_LePhare.fits` | B21's own split is 2.5 in its colour system; K5 reports calibration |
| B1 | M★ (LePhare + 0.15 dex) | SURVEY-CALIBRATION (SPS, Chabrier) | `lr_lenses.npz` | ±0.2 dex (E1) |
| B2 | cold gas log f_cold = −0.69 log M★ + 6.63 | SURVEY-CALIBRATION | B21 relation (F2 B2) | ±0.2 dex |
| B3 | hot CGM f_hot M★, uniform 100 kpc sphere, central 0.5 | SURVEY-CALIBRATION, derived in F2 (CFG580 emissivities + recorded eRASS:4 L_X of a quiescent stack) | F2 ledger B3 | [0, 1.0]; applying a quiescent stack to blue lenses is an extrapolation (stated) |
| F1 | AQUAL μ = x/(1+x); φ = ψ for lensing | FRAMEWORK-NATIVE | C4, E2, THEORY_V3 §1 | — |
| F2 | F2's AQUAL point-mass + uniform-field solver; extended baryons by the point-mass EFE ratio | FRAMEWORK-NATIVE (own solver, validated K1/K2 in F2) | `rebuild_2026_10_22/F2_outer_lensing/f2_aqual.py` | ratio exact where all baryons are enclosed (r ≥ 100 kpc) |
| F3 | screening L★ 24 / 90 pc | FRAMEWORK-NATIVE (FITTED bound, D10) | D10, M2 (l_g = L★²/2r_M) | irrelevant at R ≥ 30 kpc (computed) |
| F4 | no μ_K²ψ term | FRAMEWORK-NATIVE omission, deferred | N0 R6 | caveat on every verdict |
| F5 | no dust (cold-energy) profile around galaxies | FRAMEWORK-NATIVE (OPEN: v3 predicts none) | C2, C4, F2 | an excess would be what dust must supply |
| E1 | external field y_e: 0 / Chae+21 noclu / maxclu medians | SURVEY-CALIBRATION (SPARC-local environments, not KiDS lenses) | `real_research/reviews/directional_efe_2026/laneB_data/chae21_env.csv` via F2 | bracket; no KiDS-lens field measurement exists on disk |
| H1 | native h 0.679 (0.672–0.686), Ω_m 0.3085, T_Ωm per file | FRAMEWORK-NATIVE (BBN-bounded) / record-computed | C2 K5; CFG682; `CFG885_kids_rar_native_distances/cfg885_results.json` | ends reported |
| C1 | Σ_crit ± 3 % (source photo-z) | SURVEY-CALIBRATION | KiDS SOM δz (order of magnitude) | bracket |
| C2 | boost (lens–source clustering) | not corrected (none released) | — | inner radii; stated |
| P1 | red-lens posits R1 (O6) and R2 (O6 + O7) | SURVEY-CALIBRATION + POSIT | O6, O7 | reported per reading; blue kept at R0 by declared asymmetry |

No ΛCDM-PROCESSED or STANDARD-MOND-MACHINERY ingredient enters a verdict line. The EFE is v3's own AQUAL solve (F1/F2), not
an additive recipe. The one inherited soft ingredient that can move a verdict is the unmeasured y_e of KiDS isolated lenses;
it is bracketed, never fitted.
