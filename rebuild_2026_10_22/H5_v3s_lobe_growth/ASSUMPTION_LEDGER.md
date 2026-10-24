# H5_v3s_lobe_growth: ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / LCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT,
plus FITTED (κ = ½, L★), ILLUSTRATIVE, PROXY (record-derived stand-in for a missing measurement) and METHOD (numerics).

## A. What the open question rests on (X3 qualifier 3; V3_FULL_PICTURE §4.7, preliminary)

| ingredient | class | where | used here as |
|---|---|---|---|
| v3s switched stiffness −(γ_L/2)[max(D·P, 0)]²; soft side = H4's γ_L = 0 branch, bounded rate √(Kρ_τ(M − 1)) where ρ_τ < 0 | FRAMEWORK-NATIVE (adopted 10-23) | X3 README §1; H4 B1 | the rate (H4 `rates()`, copied verbatim) |
| D10 static maps with D·P < 0 external-field lobes (−8e-5 to −3.3e-3 M☉/pc³ at 180–1555 pc) | FRAMEWORK-NATIVE (D10 solver) on RAW + SURVEY-CALIBRATION cluster inputs | X3 json `D4_maps` | reproduced (B0b), then re-solved with full maps |
| lifetime T = min(T_H, ℓ/v) with v "≈ 100–200 km/s" | ILLUSTRATIVE (H4 convention) | H4 Part D; §4.7 | replaced by derived residence (path/V) and record speeds |
| co-moving alternative: T = T_H (15–86 e-folds deepest cell) | POSITED (not derived) | §4.7 | tested: is a co-moving lobe allowed / reachable? |
| M − 1 = (1 + x_e)² − 1 | FRAMEWORK-NATIVE (J_x M_L upper end) | §4.7 | kept; local x also used |

## B. This lane's ingredients

| ingredient | class | source |
|---|---|---|
| PN Lagrangian (H4 A1 form): Poisson, hold, continuity, Bernoulli; khronon kicked by −∇(φ − Ξ) | FRAMEWORK-NATIVE (BS24 PN transcription PROVISIONAL, via C4/BSK1) | L1 FROZEN_CRITERIA §1; H4 A1 |
| J_x masses M_T = 1 + x, M_L = (1 + x)²; μ = x/(1 + x) | FRAMEWORK-NATIVE | C4 K2, C5, H4 A5 |
| the khronon's rest frame is the reference (static host: the host's held frame) | FRAMEWORK-NATIVE (U1 part (b)) | U1 README |
| capture radius r_cap = 2GM_b/V² (LIT streaming criterion) | FRAMEWORK-NATIVE (U1 D6, BSK1 M6) | U1 README |
| positive khronon charge in the initial data (FRW cold-energy abundance Ω_K > 0, linear δ_τ ≪ 1) | FRAMEWORK-NATIVE (abundance is an initial condition: C2, C4; L1 engine ICs) | BRIEF; L1 §2 |
| Danby–Camm cold flow past a point mass (hyperbolic orbits, ψ = φ_N of the baryons) | METHOD (classical mechanics; formula re-derived and checked here, A5) | — |
| D10 axisymmetric solver `d10_solver.py` | METHOD (record code, imported read-only) | doors_push_2026_10_22/D10_native_Lstar |
| X3 `SW` switched operator, `g_mw`, `s_gal`, constants | METHOD / FRAMEWORK-NATIVE (record code, copied read-only) | X3 script |
| H4 `rates()` | METHOD (record code, copied verbatim) | H4 script Part D |
| a₀ footings; κ = ½; L★ ∈ {D10 central floor 21.68 / 22.85, 24, 90} pc | FITTED | doors BRIEF, D10 |
| globular L_V, r_h,l, R_GC (D10 json) | RAW + SURVEY-CALIBRATION | D10 / CFG332 (Baumgardt) |
| Υ_V = 1.6 for the globular maps | SURVEY-CALIBRATION (as X3 D4_maps) | X3 |
| MW Hernquist M_b = 6e10 M☉ (E_mid), a_H = 3 kpc, law field; host phantom at R_GC | SURVEY-CALIBRATION masses + FRAMEWORK-NATIVE law | D10 / X3 |
| satellite y, r_h, x_e_mid, d_host (S1 `s1_per_system.csv`; E3 data, Υ_V = 2) | RAW + SURVEY-CALIBRATION | S1 |
| satellite 3-D speeds (U1 `u1_satellites_per_system.csv`, `V_src = LVD-3D`) | RAW (LVD proper motions + v_los) + SURVEY-CALIBRATION (solar motion, U1's frame) | U1 |
| globular 3-D speeds | **MISSING on disk** → PROXY V_c = √(g_mw R) (D10 MW model) + speed-independent envelope | this lane |
| orbit bracket V_apo,10 = V_c √(2 ln 10/99) (flat rotation curve, r_a/r_p = 10) | ILLUSTRATIVE (round bracket) | this lane |
| T_H = 13.8 Gyr | ILLUSTRATIVE (H4's) | H4 |
| pile-up bound n_enc = 2 T_H/T_orb, T_orb = 2π d/V | METHOD (upper bound) | this lane |

## C. Not used

No ΛCDM-processed input, no QUMOND, no EFE recipe, no ν-function interpolation (every field is a solve of v3s's static
equation or a derived dynamical formula), no literature value in any check. No downloads.
