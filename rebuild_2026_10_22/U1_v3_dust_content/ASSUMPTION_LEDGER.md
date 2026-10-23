# U1_v3_dust_content — ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / POSITED / EXTERNAL.

## A. What the audited verdicts (S1 tiles 26, 29; P4 tiles 19 and MW K_z; F1 clusters) rest on

| ingredient | class | where | used here as |
|---|---|---|---|
| static AQUAL with μ = x/(1+x), solved with the host field as a boundary condition | FRAMEWORK-NATIVE (BS24 Eq. 35 = v3's static limit, C4 K1) | S1, P4 | the LIT static branch; the question is whether free-falling systems realise it |
| dust = the AQUAL phantom (cold, at rest in the host frame) | **implicit premise** of every static tile | S1, P4, F1 | tested here (D2, D7, N1–N5) |
| host fields (MW/M31 spherical Hernquist law fields, Coma β-model, TDG/DF2/DF4 hosts from L_K or catalogue masses) | SURVEY-CALIBRATION / EXTERNAL labels (M31 1e11 M☉; L_K × 0.6) | S1, P4 | inputs for x_e (read from the CSVs / re-derived as P4) |
| E3 satellite data (LVD σ, r_h, Υ_V = 2, Arroyo free-f binaries) | RAW + SURVEY-CALIBRATION (SPS Υ, binary correction) | S1 `s1_per_system.csv` | central values (log_gobs_gbar) |
| Coma UDG σ, R_e, M★ (CFG933 admitted 9) | RAW + SURVEY-CALIBRATION (M★) | `s1_coma_per_galaxy.csv` | per-galaxy E |
| Lelli+15 TDGs (V_circ, M_bar, R_out, host L_K, D_p) | RAW + SURVEY-CALIBRATION (gas/stellar masses) | `real_research/data/tidal_dwarfs/lelli2015_tdg.csv` | as P4 |
| DF2/DF4 (M★, R_e, σ_obs, positions) | RAW + SURVEY-CALIBRATION | CFG657 constants, as P4 | as P4 |
| L★ screening (γ_L) | FRAMEWORK-NATIVE, FITTED floor | S1, P4 | not applied to B1 (B1 at L★ = 0 is an upper bound on held dust) |
| μ_K² term | FRAMEWORK-NATIVE, value not fixed by v3 (BS24 Eq. 39 cap 14.8 h/Mpc) | S4 (running) | N7 bound only; the static μ_K solve is S4's |

## B. This lane's own ingredients

| ingredient | class | source |
|---|---|---|
| PN system (Ξ, hold equation, Poisson, khronon continuity and Euler) | FRAMEWORK-NATIVE; BS24 equations EXTERNAL, transcribed in BSK1 (WebFetch, PROVISIONAL), self-consistency checked in BSK1 M2–M4, C4 K1 | `real_research/bs_khronon_2026/BSK1_moving_source_gate.py` L15–21; L1 §1 |
| LIT dust: single-stream, irrotational (v = −∇σ), σ single-valued and continuous, ρ_τ without sign requirement | FRAMEWORK-NATIVE (BS's khronon flow; C4 "no sign requirement") | BSK1 M2, M6; C4 no-go table |
| MS dust: collisionless particles, ρ_τ ≥ 0, any distribution function | **POSITED** beyond shell crossing (as L1) | L1 ledger |
| J_x (μ = x/(1+x) exactly) | FRAMEWORK-NATIVE choice, POSTULATED outside BS's admissible class | C4 K2 |
| κ = ½ | FITTED | brief |
| a₀ footings 9.3603e-11 / 1.1312e-10 | FRAMEWORK-NATIVE (fitted κ), never pooled | brief |
| isotropic Jeans / Wolf estimator at r12 = 4a/3 (E-W), g_bar = G(M/2)/r12² | STANDARD estimator (not MOND machinery), E3/S1 convention | S1 |
| distribution-function families (King, polytropes, L^{−2β} generalised polytropes) | test families for a counterexample search (no fit) | standard |
| shell-code initial conditions (λ multiples of the phantom; uniform cloud) | test ICs for a counterexample search (no fit) | this lane |
| record speeds: LVD proper motions + v_los, Galactocentric frame of G2 (R₀ 8.122 kpc, z☉ 20.8 pc, v☉ (12.9, 245.6, 7.78)) | RAW + SURVEY-CALIBRATION (solar motion) | `real_research/data/dsph/lvd_dwarf_*.csv`; G2 `galcen` |
| PROXY speeds (host law circular speed; Coma β-model circular speed) | record-derived PROXY, labelled | S1 host fields; CFG948/L23 β-model |
| DF2/DF4 speed V_coll/2 = 179 km/s [125, 225] | EXTERNAL (vD+22 via CFG657) | CFG657 FROZEN_CRITERIA L71 |
| McMillan17 MW baryons (B1) | SURVEY-CALIBRATION, partly halo-fitted (P4 caveat) | P4 `rho_mcm` (re-implemented) |
| Eilers+19 v_c, Bovy & Rix 13 K_z,1.1 | RAW (+ survey calibration of the tracers) | `real_research/data/mw_rc_eilers2019_table1.tsv`, `mw_kz11_bovyrix2013_table3.tsv` |
| μ_K values: 14.8 h/Mpc (h = 0.6856), 0.015637 Mpc⁻¹ | EXTERNAL (BS24 Eq. 39 edge; BS24's own scale via F3) | F3, S4 |
| Coma β-model (kT 8.6 keV, r_c 276 kpc, β 0.71) | SURVEY-CALIBRATION (X-ray hydrostatic), as S1 | S1 / CFG948 |

## C. Excluded on purpose

No ΛCDM halo machinery (no NFW, SHMR, concentrations). No QUMOND phantom, no EFE recipe, no ν-function shortcut except
where it is the exact spherical AQUAL solution (Gauss's law makes spherical AQUAL algebraic). No settling, catchment,
supply or capture rules from the record's earlier media: any capture law here must come from the PN system.
