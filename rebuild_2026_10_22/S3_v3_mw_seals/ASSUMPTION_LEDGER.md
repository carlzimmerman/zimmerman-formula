# S3_v3_mw_seals ASSUMPTION LEDGER (committed with the frozen criteria, before any number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / FITTED / EXTERNAL MODEL.

## A. Ingredients of the ORIGINAL verdicts being rebuilt

| ingredient | used by | class | source | fate here |
|---|---|---|---|---|
| round enclosed-mass rule RM-v / RM-φ | CFG532/532b/533, CFG553 framework rows | OLD MODEL (not in v3) | CFG516 | dropped; quoted as step 0 |
| QUMOND phantom disc (PD) | CFG514/516, CFG553 rival, RM-φ | STANDARD-MOND-MACHINERY | CFG514 `build_PD` | replaced by AQUAL (E2/C4) |
| kernel ν_mono = 1/(1 − e^−√y) | CFG532/533/553/493/571 | old law | CFG2/CFG4_common | replaced by ν₁ (μ = x/(1+x)) |
| algebraic in-plane law g = ν(g_N)g_N on a disc | CFG532 ALG, CFG493 P1/P3, CFG571/AG4e | approximation of AQUAL (exact only for Kuzmin discs and spheres) | CFG532, CFG493, CFG571 | replaced by the AQUAL disc solve (correction C) |
| no EFE | CFG532/533/553, AG4e | omission (v3 has an EFE) | — | EFE added (MW: 3-D at γ = 57°; κ: γ = 0, reported) |
| P2 spherical V²/R width estimator | CFG493 P2 (CFG306/309) | approximation | CFG306 | bounded shift (no per-galaxy data) |
| P3 EFE as an error term (half of p43's shift, quadrature cubic) | CFG493 | STANDARD-MOND-MACHINERY (cubic EFE recipe) | p43 | kept as CFG493's error term in step A (unchanged budget); the v3 EFE is computed separately in step E |

## B. Inputs of this rebuild

| input | class | source | sensitivity / handling |
|---|---|---|---|
| AQUAL field equation, μ(x) = x/(1+x) | FRAMEWORK-NATIVE (J outside BS's class: POSTULATED, C4) | E2, C4, THEORY_V3 §1 | the solver |
| a₀ footings 9.3603e-11 / 1.1312e-10 | FITTED (κ = ½) | record | both, never pooled |
| screening L★ = 21.7 / 22.9 / 24 / 90 pc | FITTED lower bound (D10), upper ~90 pc | D10, C3 | l_g computed; no solve change expected |
| μ_K = 14.8 h/Mpc | EXTERNAL premise (BS24 Eq. 39 cap) | F3, L1 | reported bound only (R6 owns) |
| McMillan17 baryons (B1) | ΛCDM-PROCESSED in part: McMillan's disc normalisations come from a joint fit with an NFW halo; the record calls it the census | CFG514 Table 3 transcription | census band ±0.57e10 (stars); B2/B2b/B3 variants reported |
| B2 / B2b / B3 (L172 shapes 6.0 / 7.3e10; short disc R_d 2.15, recalled) | SURVEY-CALIBRATION (B3 recalled, unverified) | CFG516 `rho_b2`, `rho_b3` | envelope only |
| MW rotation curves (Ou, Eilers, Wang, Jiao, Zhou, Feng, SL23) | RAW + SURVEY-CALIBRATION (R₀, V⊙, distance scale, Jeans/asymmetric-drift terms) | `real_research/data/*.tsv`, `_external_data/cfg532_work/src/*.tex` | CFG532 error models; S-variants are the record's |
| CFG532 error model (stat ⊕ 3 %, 15 % beyond 22 kpc for Ou) | SURVEY-CALIBRATION (authors' systematics) | CFG532 | unchanged (same frozen rules) |
| MW external field e_N = 0.01273 / 0.01054, direction (268.5°, +33.0°) | ΛCDM-PROCESSED (2M++ linear reconstruction with ΛCDM bias b_K = 1.2 and f = Ω_m^0.55) | hunt h81 output | variants e_N = 0 and 2 × h81 (reported) |
| SPARC e_N (noclu / maxclu, units 1.2e-10) | SURVEY-CALIBRATION (2M++ + MCXC catalogue sum, M/L, ×8 missing-baryon bracket) | `../gext_vectors_2026/data/gext_vectors.csv` | step E only (reported) |
| WALLABY e_N (noclu / maxclu, per footing) | SURVEY-CALIBRATION (same estimator) | `prep_2026/wallaby_firing/gext_wallaby_237.csv` | step E only (reported) |
| SPARC rotmod V components, SB profiles, Υ 0.5 / 0.7 | RAW + SURVEY-CALIBRATION (SPS Υ) | `real_research/data/sparc_data/` | CFG493's levers unchanged |
| P1 ladder distances (TRGB / Cepheid) | SURVEY-CALIBRATION | CFG449 `sr_log` | CFG493's ladder term |
| WALLABY DR2 kinematics + Σ_HI, WISE M★ (M/L 0.6), Hubble-flow D at H₀ 67.4 | RAW + SURVEY-CALIBRATION (H₀ 67.4 lies in the native 67.2–68.6) | `../_external_data/wallaby_dr2/` | CFG493's terms |
| MIGHTEE P2 numbers | SURVEY-CALIBRATION (committed CFG306/304) | CFG306, CFG304 | not recomputed |
| shared priors S_gas 0.0473, S_star 0.068, S_HF 0.0174 dex | SURVEY-CALIBRATION | CFG493 | unchanged |
| gas inversion (NNLS on hats) / disc thicknesses (0.1 R_d stars, 0.1 kpc gas) | method choice (declared) | this lane | razor-thin variant → "AQUAL geometry" error term |
| ALMA: RC100 V_c 206 (pressure-corrected), KMOS3D log M★ 10.89 / 10.76, U4 V_c grid, R_e | RAW + SURVEY-CALIBRATION (SPS M★, pressure correction) | CFG571 / CFG809 | as sealed in AG4e |
| ALMA a₀(z) branch ratios (F-flat, F-DESI, E, E-CCBH, BH-k3, R-H, L-fb) | FRAMEWORK-NATIVE branches; F-DESI uses DESI CPL (EXTERNAL MODEL fit) | `SEALED_N1.json` "ratios" | read, never changed |
| ALMA D_A (flat ΛCDM H₀ 70, Ω_m 0.3; angular size only) | ΛCDM-PROCESSED (geometry only) | CFG571 | inherited unchanged (as AG4e) |
| NFW rival fitted to Ou+24 | EXTERNAL MODEL (ΛCDM halo shape, comparison only) | CFG553 | never in a v3 number |
