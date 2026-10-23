# T1_efe_strength — ASSUMPTION LEDGER (committed with the frozen criteria, before any script or number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / DIAGNOSTIC.
Every input is reused read-only from the lane named; this lane adds one diagnostic multiplier (ε) and nothing else.

## A. The diagnostic itself

| item | class | source / note |
|---|---|---|
| ε_EFE multiplies the total host-field magnitude x_e entering v3's static solve; direction unchanged; ε = 0 is the isolated solve | DIAGNOSTIC | this lane. It is not a theory parameter and no ε ≠ 1 is proposed as physics |
| v3 static equation: stiffened AQUAL, μ = x/(1+x), L★ stiffness (C4-literal, γ_F = 0) | FRAMEWORK-NATIVE | D10 `d10_solver.py`; E2 (the action gives AQUAL); C4/C5/C6 |
| κ = ½ (a₀ footings 9.3603e-11 / 1.1312e-10 m/s²) | FITTED | FP0; never pooled |
| L★ = D10 floor 21.68 / 22.85 pc (v3 reading); 24 / 50 / 90 pc reported | FITTED (lower bound from the globulars at ε = 1) | D10 |

## B. Dataset inputs

| dataset | input | class | source |
|---|---|---|---|
| SAT (tile 26) | LVD σ, r_h, M★ (or M_V), distances | RAW + SURVEY-CALIBRATION (SPS M★, distance moduli) | `real_research/data/dsph/lvd_*.csv` via S1 |
| SAT | Arroyo-Polonio free-f binary correction; Geha lower σ (W) | SURVEY-CALIBRATION | `campaign_fresh_gravity/CFG257_ufd_kinematics_scoping/` via S1 |
| SAT | Υ_V = 2 (primary), 4 (W) | SURVEY-CALIBRATION | E3 / S1 |
| SAT | Plummer, mass = light, isotropic Jeans, Wolf r₁₂ | model assumption | S1 |
| SAT | host field: law field of a Hernquist MW (6e10, E_lo 4e10, E_hi from E2's 8 kpc total) / M31 1e11 | FRAMEWORK-NATIVE law + SURVEY-CALIBRATION masses (M31 1e11 an external label) | S1 / D10 / D7b |
| COMA (tile 29) | Freundlich+22 σ, R_e, L, M/L, d_proj, d_mean | RAW + SURVEY-CALIBRATION (SSP M/L) | `real_research/data/freundlich2022_coma_udgs.tsv` via S1 |
| COMA | Coma total field: isothermal hydrostatic β-model (kT 8.6 keV, r_c 276 kpc, β 0.71) | RAW X-ray + hydrostatic-equilibrium assumption | L23 / CFG948 via S1 |
| COMA | σ_sys recipe (M★ ±0.2 dex, σ ±15 %, D ±5 %) | SURVEY-CALIBRATION | CFG948 via S1 |
| LENS (F2 Track A) | B21 Fig. 3 ESD profiles + released covariance (4 mass bins × 15 radii) | RAW (survey product) + SURVEY-CALIBRATION (B21 fiducial distances, converted to native h 0.679, Ω_m 0.3085 by F2) | `real_research/data/lensing_rar/brouwer2021_rar/` via F2 |
| LENS | lens M★ (LePhare + 0.15), cold gas (B21 relation), hot CGM 0.5 M★ inside 100 kpc | SURVEY-CALIBRATION (SPS soft, E1; hot CGM from one eROSITA stack, unverified) | F2 |
| LENS | external-field reference: Chae+21 SPARC environments, noclu y_e 7.8e-4 (primary), maxclu 6.4e-3 | SURVEY-CALIBRATION, **not measured for the KiDS lenses** | F2 |
| LENS | CFG885 T_Ωm | SURVEY-CALIBRATION | F2 |
| S2 window | the same KiDS lenses and shear | not independent of LENS; reported only | S2 |
| GC (D10) | Baumgardt σ_obs, N, RV-bin radii, L_V, r_h,l, R_GC | RAW + SURVEY-CALIBRATION (distances, structural fits) | D10 via CFG332 |
| GC | Υ_V prior P1 logN(1.6, 0.15 dex) | SURVEY-CALIBRATION (SPS) | D10 |
| GC | binary-aware likelihood tables (f_b 0.3, e_c calibrated) | SURVEY-CALIBRATION | D10 JSON `lik_tables` (read, not regenerated) |
| GC | MW field E_mid (bracket E_lo/E_hi reported from D10) | FRAMEWORK-NATIVE + SURVEY-CALIBRATION | D10 |
| SS (Cassini, planets) | Q₂ at E0–E3, hedgehog anomaly, Hees 2014 / Park 2026 bounds | FRAMEWORK-NATIVE (computed) + RAW ephemeris bounds | C6 JSON (read only) |
| WB | screened γ_v − 1 (C6 R3) | FRAMEWORK-NATIVE | C6 JSON |
| WB | DR3 R = 0.973 ± 0.178 (CFG825 official C4 run, UNDECIDED) | RAW (Gaia DR3 registered catalogue) | `campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/` |
| WB (unscreened contrast only) | E2's AQUAL binary γ_v 1.167 / 1.199 at g_ext 1.778e-10; point-mass AQUAL curve γ_pm(ε) from F2's solver | FRAMEWORK-NATIVE (unscreened law, not v3) | E2; `f2_aqual.py` |
| REC | Chae amplitude A = e_fit / e_env (CFG179 M5; CFG8) | **STANDARD-MOND-MACHINERY** (Chae's algebraic EFE fit function) + SURVEY-CALIBRATION (environment) | CFG8 / CFG179 |
| REC | directional asymmetry Â (n = 16 aligned firing; WALLABY n = 25) | RAW velocity fields + **STANDARD-MOND-MACHINERY** (QUMOND-class Legendre prediction as the unit) | `prep_2026/aligned_firing/`, `prep_2026/wallaby_firing/` |
| REC | CFG447 (DR3 dry run γ̂ 1.075 ± 0.055, non-scoring), CFG478 (QUMOND satellite lensing) | as recorded; quoted, not recomputed | LEDGER rows |

## C. Inherited assumptions that the ε reading depends on (stated, not removed)

1. **No extra bound mass in the hosted systems.** The satellites and Coma UDGs constrain ε only if the predicted σ is the
   whole dynamical mass. v3's open item (2) says ultra-faints need bound cold mass; if so, their ε information is the
   tracking statistic (§3 of the criteria), not the offset.
2. **Equilibrium in the present host field** (S1's caveat for Coma; tides not modelled for satellites).
3. **The lens stack measures isolated galaxies' own profiles** (F2's AMENDMENT A1 calls the outer range UNDECIDABLE)
   and Chae's SPARC fields stand for the KiDS lenses' fields (not measured).
4. **The globulars' ε information exists only at fixed L★**: D10's floor was derived at ε = 1, so at the floor the
   globulars penalise ε < 1 by construction; with L★ re-floored at each ε they carry none.
5. **Uniform host field, spherical (Plummer / point-mass) sources, monopole Jeans** (S1, D10, F2).
6. **ΛCDM-PROCESSED inputs: none** in any verdict line. STANDARD-MOND-MACHINERY appears only in the record rows (REC),
   which are reported separately and never enter the primary combination.
