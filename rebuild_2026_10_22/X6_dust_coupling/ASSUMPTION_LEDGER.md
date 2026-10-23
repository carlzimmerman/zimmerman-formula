# X6_dust_coupling — ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any script or number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT.
This lane computes no new data product. It derives (sympy), reproduces record numbers, and grades candidates with the record's
machinery read-only. Paths are relative to the repository root unless marked "outside the repo".

## 1. The theory and its constants

| input | class | source |
|---|---|---|
| v3 action: BS khronon S = (c³/16πG)∫√−g[R − 2J(Y) + 2K(Q)], J = J_x (μ = x/(1+x) exactly), K = μ_K²(Q−1)², P + γ_L, matter on g | FRAMEWORK-NATIVE (J_x POSTULATED, outside BS's admissible class; C4) | `covariant_push_2026_10_22/C4_khronon_parent/README.md`, `THEORY_V3_DRAFT.md` |
| BS24 / BS25 equations (PN system eqs. 19, 25, 27, 29, 30; Eq. 7, 35, 39; BS25 DBI K) | LITERATURE-INPUT (WebFetch transcription, not on disk, PROVISIONAL; self-consistency checked in C4 K1/K7, Q6 D1–D7, Q7 S7/S8) | C4, Q6, Q7 READMEs; `real_research/bs_khronon_2026/BSK1_moving_source_gate.py` |
| κ = ½; a₀ = 9.3603e-11 / 1.1312e-10 m/s² | FRAMEWORK-NATIVE (κ FITTED) | doors BRIEF |
| μ_K and its cap μ_K⁻¹ ≥ 100 kpc (BS24 Eq. 39) | external premise (LITERATURE-INPUT); not in the v3 parameter table; not fitted here | F3 §7, S4 |
| cold abundance (khronon charge I₀; C1b's split f_d) | FITTED (initial condition; C2, C4 K7). f_d is graded over [0, 1], never chosen | C2, C4 |
| BS25 DBI sets P1 (μ⁻¹ 223 kpc, λ_D 30), P2 (22.3 Mpc, 1) | LITERATURE-INPUT (BS24 Fig. 1, via Q7); used only as K sub-rows | `rebuild_2026_10_22/Q7_bs25_cosmology/README.md` |
| mimetic constraint dust (Lagrange-multiplier field; Chamseddine–Mukhanov 2013) | LITERATURE-INPUT from memory, not looked up (PROVISIONAL). No verdict rests on the citation: the identities used (geodesic congruence, PN limit, linear mode and energy) are derived here in sympy (X-D2, X-D9) | — |
| AeST (SZ21 arXiv:2007.00082; VSZ 2304.05134), capped 𝒥, γ_L | LITERATURE-INPUT on disk outside the repo (`_external_data/aest_papers_2026_10_22/`), as used by H1/H2/C5; FRAMEWORK-NATIVE capped F (C1) | H1, H2, C5 |

## 2. Record results used as inputs (read-only; sha256 stored by the script)

| input | what is used | class of its own inputs | file |
|---|---|---|---|
| U1 T1, T3, B0/B1 branches per satellite | Delta_B0, Delta_B1_MS, Delta_B1_LIT, x_e per system; N5 medians and Coma B0 (⟨E⟩, se, σ_sys, z_sys) | data side: E3's kinematics (RAW, survey-reduced), Υ_V = 2 and binary corrections (SURVEY-CALIBRATION); host fields FRAMEWORK-NATIVE (law on bracketed host masses); speeds LVD 3-D (RAW) or PROXY; Coma β-model (RAW X-ray, hydrostatic) | `rebuild_2026_10_22/U1_v3_dust_content/u1_satellites_per_system.csv`, `u1_v3_dust_content_results.json` |
| S1 sample definition | through U1 (U1 N0 reproduced S1) | as U1 | `rebuild_2026_10_22/S1_v3_hosted_small/` |
| F1 cluster stack and dust rows | `dust` (gas-tracing dust sourcing AQUAL: f_needed, A_needed, A_cosmic_5364), `addendum_L187` NFW c* = 0.40 rows, `rows` PRIMARY | KiDS shear RAW; eRASS1 Mgas500 and R500 SURVEY-CALIBRATION / ΛCDM-PROCESSED (R500, distances); β = 2/3 outskirts extrapolation (soft, X0 A1); NFW c* = 0.40 ΛCDM-PROCESSED (L187: Dutton–Macciò c(M)) | `rebuild_2026_10_22/F1_cluster_cores/f1_cluster_cores_results.json` |
| S4 static μ_K solve | verdict_A1, knob_passes, single_cells_passing, galaxy guard (mu_K_gal) | F1's stack (above); F2 Track A (B21 lensing, SURVEY-CALIBRATION); VSZ zero-point convention (LITERATURE-INPUT) | `rebuild_2026_10_22/S4_v3_muK_clusters/s4_v3_muk_clusters_results.json` |
| F3 / M1 growth ODE and kernel | the ODE (copied), background A, R1b(iii) ratios 0.39080 / 0.12055 | background A: C2 c2b plik-lite refit (FRAMEWORK-NATIVE in the dust limit; plik-lite foreground compression SURVEY-CALIBRATION); CLASS 3.3.4 (tool); radiation Ω_r = 4.18e-5/h² | `rebuild_2026_10_22/F3_growth_audit/f3_growth_audit.py`, `M1_trilemma/m1_trilemma_results.json`, `covariant_push_2026_10_22/C2_aest_cosmology/c2b_native_cmb_results.json` |
| Q6 literal-K radiation era | μ_K,BBN = 1.836e8 h/Mpc; Boltzmann R_B 0.073 at the cap | CLASS khronon patch (FRAMEWORK-NATIVE), BBN line ΔN_eff ≤ 0.5 (EXTERNAL convention) | `rebuild_2026_10_22/Q6_v3_class/q6_native_results.json` |
| Q7 BS25 DBI | BBN passes; R_B 0.259–0.324 | as Q6; DBI sets LITERATURE-INPUT | `rebuild_2026_10_22/Q7_bs25_cosmology/q7_native_results.json` |
| C5 health | CONDITIONALLY HEALTHY (C4-literal), its conditions | FRAMEWORK-NATIVE (linear WKB analysis) | `covariant_push_2026_10_22/C5_health/c5_health_results.json` |
| M1 R1 health | R1(c) PASS with C5-edge flag | FRAMEWORK-NATIVE | `rebuild_2026_10_22/M1_trilemma/m1_trilemma_results.json` |
| H1 AeST family | verdict NONE IN THE FAMILY; theorem T1 (negative-energy mode = growth mode); growth column (ii) | SZ21 (LITERATURE-INPUT), SPARC (RAW) | `rebuild_2026_10_22/H1_aest_F/h1_aest_f_results.json` |
| H2 AeST clusters | verdict_A1 CANNOT | F1 stack (above) | `rebuild_2026_10_22/H2_aest_clusters/h2_aest_clusters_results.json` |
| CFG946 double-count estimator | NGC 3198 setup (Υ 0.61), D-F content, r_ta formula, BTFR at r_ta | SPARC NGC 3198 (RAW); r_ta uses Ω_b = 0.0493, H₀ = 67.4, Ω_c = 5.364 Ω_b and the EdS turnaround Δ_ta = 5.55 (ΛCDM-PROCESSED values and a spherical-collapse convention) | `campaign_fresh_gravity/CFG946_option2_phantom_not_cold/cfg946.py`, `cfg946_results.json` |
| P4 SPARC RAR recipe | per-galaxy Υ fit, CFG4 weights, iso_perUps rms and median Υ | SPARC rotmod + `SPARC_Lelli2016c.mrt` (RAW); V_bar² convention with 1.4 × bulge (SURVEY-CALIBRATION); spherical approximation (declared approximation, P4 D1) | `real_research/data/sparc_data/`, `rebuild_2026_10_22/P4_v3_galaxy_tiles/p4_v3_galaxy_tiles_results.json` |

## 3. This lane's own choices

| choice | class | note |
|---|---|---|
| C1b native content: dust traces baryons at the cosmic ratio 5.364 (satellites, UDGs) | ΛCDM-PROCESSED ratio (Ω_c/Ω_b from the record's fair-sample convention), zero-history convention | a convention for the native line; the branch range allows any content, so (a) can only reach UNDECIDED for C1b |
| C1b galaxy content: CFG946's D-F (f_d × 5.364 M_b, M ∝ r to r_ta) | record estimator (CFG946), ΛCDM-PROCESSED inputs in r_ta | an estimate of the clustered content, not a simulation |
| C1b cluster content: fair-sample amplitude in F1's two shapes | as F1 | monotonicity in amplitude is used; no new solve |
| growth start a_i = 1e-3 with δ_b = δ_τ = δ_d ∝ a | POSITED (F3's optimistic start; upper bound on R) | a_i = 1e-4 reported |
| ΔN_eff scaling (1 − f_d)²/μ_K² for C1b | DERIVED (X-D8) from the quadratic K background | uses Q6's μ_K,BBN at f_d = 0 |

No STANDARD-MOND-MACHINERY carries any grade: ν₁ is the exact spherical AQUAL solution of μ = x/(1+x), and AQUAL = QUMOND only
in spherical symmetry, which is where it is used. No downloads; no web lookups.
