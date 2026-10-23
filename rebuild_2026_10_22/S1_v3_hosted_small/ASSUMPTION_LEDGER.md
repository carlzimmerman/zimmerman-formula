# S1_v3_hosted_small: assumption ledger (written before any script or number of this lane)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / MODEL ASSUMPTION.
Paths are repo-relative.

## A. Inputs of the old verdicts

### Tile 26 (E3, `doors_push_2026_10_22/E3_dwarf_excess/`)

| # | ingredient | class | source | note |
|---|---|---|---|---|
| A1 | σ_los (mostly single-epoch) | RAW | `real_research/data/dsph/lvd_dwarf_*.csv` | binaries inflate |
| A2 | binary corrections (Arroyo-Polonio free-f / f = 0.7) | SURVEY-CALIBRATION (population model) | `campaign_fresh_gravity/CFG257_ufd_kinematics_scoping/arroyo_polonio2026_tableA1.csv` | 12 UFDs; median ratio for the rest |
| A3 | multi-epoch σ (Geha 2026 II DEIMOS) | RAW | `CFG257_ufd_kinematics_scoping/geha_vs_lvd_match.csv` | worst-clean "lower σ" |
| A4 | R_e (circularised), distance modulus | RAW × SURVEY-CALIBRATION (RR Lyrae / HB / TRGB distances) | LVD | H₀-independent |
| A5 | M★ at Υ_V = 2 | SURVEY-CALIBRATION (SPS) | LVD `mass_stellar` | Υ 1–4 bracket |
| A6 | Wolf estimator g_obs = 3σ²/r₁₂, g_bar = G(M★/2)/r₁₂² | MODEL ASSUMPTION (equilibrium, sphericity) | A26 eq. 3 | data side kept here |
| A7 | screened prediction 1 + S(s)(ν₁(y) − 1), s = r₁₂/(L★²/2r_M), CFG691 table | FRAMEWORK-NATIVE in origin, but the **isolated** stiffness profile applied multiplicatively | CFG691/CFG820 | D10: in a field, screening is not multiplicative and its length is L★, not L★²/2r_M |
| A8 | no external field | MODEL ASSUMPTION (the old EFE-free class-A law) | E3 | v3 has an EFE everywhere (N0 cross-cutting 1) |
| A9 | EFE "+1.25 dex" diagnostic | STANDARD-MOND-MACHINERY (1-D QUMOND ν(y_i + y_e)) | D2 `efe_delta` | not used by E3's verdict; not used here |
| A10 | host masses MW 6e10, M31 1e11 | SURVEY-CALIBRATION / external label | CFG332, D2 | E3 used them for Jacobi radii only |

### Tile 29 (CFG933, CFG948)

| # | ingredient | class | source | note |
|---|---|---|---|---|
| B1 | σ_obs ± esig, R_e, L, M/L | RAW (spectroscopy, photometry) + SURVEY-CALIBRATION (SSP M/L) | `real_research/data/freundlich2022_coma_udgs.tsv` | transcribed from arXiv:2109.04487 |
| B2 | Coma distance (R_e and L in physical units) | SURVEY-CALIBRATION, H₀-dependent (redshift distance; the sources' H₀ is not on disk) | B1 | ±5 % systematic in CFG948 |
| B3 | isolated ν_e = 1/(1 − e^{−√y}) law, no EFE | FRAMEWORK-NATIVE kernel of the old chain; the no-EFE choice is the old class-A law | CFG921/928/933 | v3 kernel is ν₁; v3 has an EFE |
| B4 | P2 posit (CFG928), no-capture ceiling (CFG939/948 P-medium) | old-model rules (not in v3) | CFG928, CFG948 | dropped: v3 has no capture/supply |
| B5 | Coma β-model g(r) (kT 8.6 keV, r_c 276 kpc, β 0.71) and dmean/dproj | RAW (X-ray) + MODEL ASSUMPTION (isothermal hydrostatic equilibrium) + SURVEY-CALIBRATION (3-D distance from vdBurg+16 Einasto) | L23 §6, CFG948 | used by CFG948 only for capture speeds; not in the old prediction |

## B. Inputs of this rebuild

| # | ingredient | class | source | bracket / handling |
|---|---|---|---|---|
| R1 | field equation: stiffened AQUAL, μ = x/(1+x), γ_F = 0, L★ stiffness | FRAMEWORK-NATIVE (C4 literal, C5, D10 K1) | `doors_push_2026_10_22/D10_native_Lstar/d10_solver.py` (read-only) | L★ 0 / floor / 24 / 90 pc |
| R2 | host as a uniform total background field, response solved | FRAMEWORK-NATIVE (no recipe) | R1 | tidal (gradient) terms neglected: MODEL ASSUMPTION (E3: 14 % of satellites have r₁₂ beyond the baryon-only Jacobi radius) |
| R3 | L★ floor 21.68 / 22.85 pc; 24; 90 pc | FRAMEWORK-NATIVE fitted bound (D10, CFG820) and window edge | D10, C3 | not fitted here |
| R4 | Plummer, a = R_e, mass = light, M = M★ (no gas) | MODEL ASSUMPTION | as E3/CFG933 | Leo T's HI not in g_bar (as E3) |
| R5 | estimator E-W (primary), E-V (reported) | MODEL ASSUMPTION (equilibrium, isotropic Jeans on the monopole; E-V exact orientation average) | `d10_solver.jeans` | both reported |
| R6 | MW host: Hernquist M_b 6e10 (4e10, Mb_hi(a₀)), a_H 3 kpc, law field | SURVEY-CALIBRATION masses + FRAMEWORK-NATIVE law | D10 (A60 / CFG332 / D7b) | bracket E_lo/E_mid/E_hi |
| R7 | M31 host 1e11 M☉, a_H 3 kpc, same fractional bracket | external label (E3/D2), SURVEY-CALIBRATION | E3 | stated, not sourced on disk |
| R8 | LVD `distance_host` (3-D host distance); Leo T: LVD heliocentric distance | SURVEY-CALIBRATION (distances) | LVD | not varied in the MC (as E3) |
| R9 | Coma field = measured hydrostatic total acceleration (β-model) at dmean / dproj | RAW + MODEL ASSUMPTION (hydrostatic, isothermal) | L23 / CFG948 constants | ÷ 2 and isolated reported |
| R10 | the data side, sample rules, MC/bootstrap, se/σ_sys conventions | as A1–A6 / B1–B2 | E3, CFG933, CFG948 | reproduced first (K1, K7, K8) |
| R11 | μ_K² term (BS24 Eq. 35), μ_K ≤ 14.8 h/Mpc, h = 0.6856 | FRAMEWORK-NATIVE equation; μ_K an EXTERNAL premise (BS24 Eq. 39 cap); zero point not fixed by v3 | F3, L1 §1, H2 | bounded, not solved |
| R12 | native H₀ 67.2–68.6 (central 67.9) | FRAMEWORK-NATIVE (C2, A78) | THEORY_V3 / BRIEF | Coma distance × 70/67.9 ASSUMES the sources used H₀ = 70 |
| R13 | a₀ footings | FITTED (κ = ½) | BRIEF | never pooled |

No ΛCDM-PROCESSED input and no STANDARD-MOND-MACHINERY enters a verdict line of this lane. The ΛCDM-processed catchment
census (f_ret, 5.364) of E3's Part B is not used: v3 has no supply rule.
