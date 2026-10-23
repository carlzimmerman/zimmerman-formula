# X2_cluster_outskirts: assumption ledger (written before any number; committed with the frozen criteria)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / LCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT.
"Inherited" = taken unchanged from F1 (`F1_cluster_cores/ASSUMPTION_LEDGER.md`, rows A/B) and classed as there.

## A. The verdict under test (F1 PRIMARY and its "overshoot" sentence)

| # | ingredient | class | file | role here |
|---|---|---|---|---|
| A1 | KiDS-1000 SOM-gold e1, e2, w, RA, DEC, Z_B | RAW | F1 cache from `f1_extract.py` (session scratch; regenerable from `_external_data/kids_lensing_zsplit/`) | replayed (R1) |
| A2 | Σ_crit from point Z_B, Z_B > z_l + 0.2, ≤ 1.2; m = −0.01 | SURVEY-CALIBRATION | F1 `esd()` | inherited |
| A3 | random subtraction, 5–6 randoms 1–3° away (F1 rng seed 20261022) | RAW (estimator) | F1 `f1_cluster_cores.py` L100–116 | inherited; R−R from the same randoms (e) |
| A4 | data boost B < 1 applied (F1 frozen PRIMARY); F1 A1 says the sign is wrong | RAW (measured) / convention | F1 | graded as frozen; clipped convention reported |
| A5 | distances: DESI DR2 D_M/r_d × 101.54/h, h 0.672 / 0.686 | RAW × FRAMEWORK-NATIVE (C2) | F1 `DM()` | inherited |
| A6 | eRASS1 RA_XFIT/DEC_XFIT, BEST_Z, MGAS500 (ΛCDM(70, 0.3) distances, rescaled q^{5/2}), R500 (× q) | RAW / SURVEY-CALIBRATION; R500 LCDM-PROCESSED | `real_research/data/erass1cl_primary_v3.2.fits` | inherited; Mgas500 also sets the tercile split (b) and the PN scaling |
| A7 | catalogue miscentring (X-ray fit vs catalogue position) | RAW | F1 `predict(miscen=True)` | inherited |
| A8 | gas β = 2/3, r_c = 0.15 R500, cut at 3 Mpc; 78 % of the gas budget beyond R500 is this extrapolation (CFG949 A1) | LITERATURE-INPUT (assumed shape) | F1 `gas_mass()` | **changed in (a)** |
| A9 | stars f* = 0.20 × gas | LITERATURE-INPUT | F1 | inherited |
| A10 | spherical AQUAL μ = x/(1+x), lensing = dynamics (ϕ = ψ) | FRAMEWORK-NATIVE (E2, C4) | F1 `g_aqual_sph` | inherited |
| A11 | no external field (isolated law, phantom to 30 Mpc) | FRAMEWORK choice | F1 RG grid | **changed in (c)** |
| A12 | ESD estimator with g ≈ γ (no 1/(1 − κ)) | RAW estimator, approximation | F1 `esd()` | **changed in (d)** |
| A13 | jackknife errors only; cross shear MID 2.0σ (F1 MUTATE), R−R OUTER 2.2σ (CFG687 M2) not propagated | RAW (statistics) | F1, CFG687 | **changed in (e)** |
| A14 | the overshoot sentence rests on two shapes: dust tracing the gas sourcing AQUAL (F1, OUTER 0.58) and L187's NFW c* = 0.40 (LCDM-PROCESSED) | FITTED-needed amount / LCDM-PROCESSED | F1 README | re-posed as the PN bound (§2.1 of the criteria) |
| A15 | profile χ² line 11.07 (5 bins, p = 0.05), jackknife covariance + Hartlap | RAW (statistics) | H2 `chi2_prof` (A1) | inherited, named "F1's line" in the brief |
| A16 | a₀ footings 9.3603e-11 / 1.1312e-10, κ = ½ | FRAMEWORK-NATIVE (FITTED) | CFG4_common | inherited |

## B. This lane's inputs

| # | ingredient | class | source | note |
|---|---|---|---|---|
| B1 | replay of F1's measurement with cross shear, per-random ESDs and Σ_crit⁻ᵏ moments (k = 2…5) | RAW | `x2_replay.py` → `x2_replay_percluster.npz` | must equal F1's caches (R1, R2) |
| B2 | (a1) gas ρ ∝ r⁻³ beyond r200m | LITERATURE-INPUT, PROVISIONAL | CFG814 (`campaign_fresh_gravity/CFG814_erosita_outskirt_catchment/`), from arXiv:2509.25317 (abstract/summary value) | not on disk; transcription |
| B3 | r200m = 2.2 R500 | LCDM-PROCESSED (concentration / Ω_m conversion), PROVISIONAL | CFG814 criteria | used as the steepening radius |
| B4 | (a2) filament flattening r⁻² beyond 2 r200m | LITERATURE-INPUT (simulations cited by eROSITA; LCDM-PROCESSED) | CFG814 bracket F | bracket |
| B5 | (a3) r⁻³ from R500 | assumption (bracket) | — | steepest reading; X-COP's on-disk median M_gas(<x) log-slope is 1.03 at x ≤ 1.64 (F1), i.e. NOT r⁻³ there |
| B6 | (c1/c2) Chae+21 e_N noclu / maxclu medians (SPARC-local environments) | LITERATURE-INPUT (SURVEY-CALIBRATION in F2's ledger) | `real_research/reviews/directional_efe_2026/laneB_data/chae21_env.csv` | not measured at clusters |
| B7 | (c3) P2 catalogue field median (GAMA galaxies' baryons only) | FRAMEWORK-NATIVE computation on RAW (lower bound) | T1 AMENDMENT_A1 / P2 README | not measured at clusters |
| B8 | EFE solver: exact axisymmetric AQUAL, point mass in a uniform field | FRAMEWORK-NATIVE | `rebuild_2026_10_22/F2_outer_lensing/f2_aqual.py` (read-only import, bytecode writing disabled) | |
| B9 | EFE transplant to an extended cluster: C(r/r_M,tot) (F2's), bracket C(r/r_M(<r)) | approximation | — | bracketed |
| B10 | (d) reduced shear g = γ/(1 − κ) forward-modelled with source moments, model's own Σ | RAW (estimator physics) | B1 | 4th-order series, checked against the exact source average (R3) |
| B11 | (e) cross-shear and R−R null stacks as rank-1 covariance templates and band offsets in quadrature | RAW (statistics), conservative | B1 | |
| B12 | PN diagnostic: point mass ∝ rescaled Mgas500 per cluster, Newtonian, "needed" λ | declared test shape (no physics claim) | criteria §2.1 | lower bound on outer signal for any monotone added component (proof in the criteria) |
| B13 | CFG949 debris: native EPS collapse (CFG654 tables), CFG930's C = 3000 rule, r_ta boundary, S-cen census f_ret, Ω_c/Ω_b = 5.364 | FRAMEWORK-NATIVE (record conventions) with the NFW form a LITERATURE-INPUT (generic collapse convention, NFW97; CFG949 "not derived") | `campaign_fresh_gravity/CFG949_clusters_untethered/cfg949.py` R930 block (exec'd read-only) + `CFG654_independent_inputs/` | K6 reproduces CFG949 |
| B14 | FPS Eq. 17, η = 10^0.93, r_c = 0.43 Mpc (16 CLASH clusters, gas 0.8–5.3e14 M☉, QUMOND ν simple, no EFE, no hydrostatic bias in the lensing fits) | LITERATURE-INPUT, PROVISIONAL (web lookup of the arXiv HTML; not on disk) | arXiv:2410.02612 | applied far below its mass range; no rescaling |
| B15 | Milgrom 2008 CBDM | LITERATURE-INPUT (abstract lookup, PROVISIONAL) | arXiv:0712.4203 | no fixed form → not tested |
| B16 | no ΛCDM halo, no NFW for the law, no HMcode, no mass function in any law prediction | — | — | B3/B4/B13 are the only LCDM-touched inputs and are labelled |

Nothing is downloaded. Missing on disk (listed, not fetched): arXiv:2509.25317 (eROSITA outskirt stack), arXiv:2410.02612
(FPS full text), arXiv:0712.4203, any per-cluster external-field estimate for eRASS1 clusters.
