# ZT4_zstar_outer_lensing: assumption ledger (written before any script or number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / EXTERNALLY CALIBRATED / FITTED / POSITED.
"P2" = `rebuild_2026_10_22/P2_spec_isolated_lensing/`; "Z1" = `rebuild_2026_10_22/Z1_successor_design/`.
κ = ½ FITTED; footings never pooled; no dark-matter particle; not theory closed.

## A. Data side (all inherited from P2 unchanged; see P2's ledger for sources)

| # | ingredient | class | note |
|---|---|---|---|
| D1 | GAMA DR4 G3C spec-z, S3 isolated lenses (2,251), iso-randoms I3 | RAW | P2 §2–3, rebuilt from P2's code and seeds |
| D2 | KiDS-1000 shapes, weights, Z_B (F1 reader cache) | RAW + SURVEY-CALIBRATION | P2 D2 |
| D3 | Σ_crit from point Z_B, 1 + K = 0.9853 | SURVEY-CALIBRATION | P2 D3, D4 |
| D4 | Δ = L − I3 hole subtraction | RAW (data-only) | P2 E2 |
| D5 | 15 × 15 delete-one jackknife covariance, 36 patches | RAW (data-only) | P2 §4 |
| D6 | Hartlap factor (36 − p − 2)/(36 − 1) | standard statistics (choice, frozen) | new in this lane |
| D7 | native distances h 0.679, Ω_m 0.3085 for R and Σ_crit | FRAMEWORK-NATIVE / SURVEY-CALIBRATION | P2 H1 |

## B. Baryons and the law (inherited)

| # | ingredient | class | note |
|---|---|---|---|
| B1 | M★: KiDS-bright LePhare + 0.15 dex, rescaled to spec-z | SURVEY-CALIBRATION (SPS) | P2 M1 |
| B2 | cold gas log f = −0.69 lM70 + 6.63; hot CGM 0.5 M★ (100 kpc sphere / point) | SURVEY-CALIBRATION / POSITED inventory | P2, F2 B2–B3 |
| B3 | AQUAL μ = x/(1+x), lensing = dynamics, isolated (y_e = 0) | FRAMEWORK-NATIVE (v3s static owner limit, Z1 K4) | P2 F1 |
| B4 | a₀ footings 9.3603e-11 / 1.1312e-10 m/s² | FITTED (κ = ½); alt footing ΛCDM-PROCESSED (E1) | never pooled |
| B5 | screening L★ | FRAMEWORK-NATIVE (FITTED bound) | irrelevant at R ≥ 30 kpc |
| B6 | neighbour term: linear sum of each galaxy's profile | FRAMEWORK-NATIVE approximation | P2 F5 |

## C. Z★-specific ingredients

| # | ingredient | class | note |
|---|---|---|---|
| Z1 | owner frame, no EFE (R2) | POSITED (non-variational rule, DESIGN §2) | zero-field profile for every owner |
| Z2 | capacity cap M(r) = min(M_iso, (1+f) M_b), r_s = r_M √(f(f+1)) (R1, Z1 K5) | POSITED rule; closed form FRAMEWORK-NATIVE given R1 | exact for a point mass |
| Z3 | f_own bracket {5.364, 50}, the same f for every galaxy | 5.364 = Ω_c/Ω_b is ΛCDM-PROCESSED (record input); 50 is a frozen bracket end (TEST_PLAN) | not fitted; verdict only where both ends agree |
| Z4 | the cap uses the full inventory M_b = M★ + M_cold + M_hot | POSITED (owner = all its baryons) | — |
| Z5 | unowned medium = pressureless dust, linear growth = GR dust (Z1 K8, s(k) = 1) | FRAMEWORK-NATIVE (dust limit of Z★) | — |
| Z6 | linear P(k, z) from CLASS, backgrounds A (C2 c2b refit) and B (CFG886 background, A's A_s, n_s, ω_b) | ΛCDM-PROCESSED values (CMB / BAO fits run in the dust limit) on a FRAMEWORK-NATIVE form (C2: dust-limit background is GR) | F3 K2 parameters |
| Z7 | ρ̄ in the two-halo term = ρ̄_c of that background (dust only) | FRAMEWORK-NATIVE choice (the medium is the dust); value ΛCDM-PROCESSED via Z6 | baryons of neighbours sit in T_nbr |
| Z8 | **bias b = 1** (lens an unbiased linear tracer of the dust); random points b = 0 | **POSITED** | no native bias; no fitted constant; b_ST reported only |
| Z9 | Sheth–Tormen bias of (1+f) M_b on native σ(M) (a 0.707, p 0.3, δ_c 1.686) | EXTERNALLY CALIBRATED (ΛCDM N-body fit) | reported only (r5) |
| Z10 | two-halo ignores the isolation conditioning of S3 lenses (the linear ξ is the unconditioned mean) | POSITED approximation | stated; the I3 subtraction removes the environment only on the data side |
| Z11 | catalogued neighbours' owned mass is in both T_nbr and ξ_lin (double count) | approximation, stated | bracket (r4): two-halo without T_nbr |
| Z12 | P2's background (h 0.679, Ω_m 0.3085) for R vs A/B for P(k) | mixed, stated | ≤ 2 % in distances |

No ingredient is fitted in this lane. The only new constant-like choice is b = 1 (POSITED); the f bracket was frozen by
the test plan. No dark-matter particle enters: the dust is the cold-energy medium.
