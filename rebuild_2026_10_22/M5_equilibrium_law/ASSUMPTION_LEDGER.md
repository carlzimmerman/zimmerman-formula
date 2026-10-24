# M5_equilibrium_law: assumption ledger (committed with the frozen criteria, before any script or number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / POSTULATED (this lane's
construction, tested not assumed).

| # | ingredient | where | class | note |
|---|---|---|---|---|
| A1 | AQUAL field equation, μ = x/(1+x) | doors E2, covariant C4 | FRAMEWORK-NATIVE | the law the equilibrium must reproduce |
| A2 | a₀ footings 9.3603e-11 / 1.1312e-10 | FP0 via `campaign_fresh_gravity/CFG4_common` | FRAMEWORK-NATIVE (κ = ½ FITTED) | never pooled |
| A3 | Newtonian Poisson for baryons + medium, unit weight | route premise | POSTULATED | "self-gravitates normally" |
| A4 | medium stress Π(ρ_c, ∇Φ), polarisation, bath, drift | candidates (a)–(f) | POSTULATED | each tested |
| A5 | SPARC rotmod V_obs, eV, V_gas, V_disk, V_bul | `real_research/data/sparc_data/` | RAW (+ SURVEY-CALIBRATION: distances, inclinations, 3.6 µm photometry) | |
| A6 | SPARC table (D, eD, Inc, eInc, Vflat) | `real_research/data/SPARC_Lelli2016c.mrt` | SURVEY-CALIBRATION | |
| A7 | per-galaxy Υ, bulge 1.4 Υ, grid 0.30–1.20 | P4 recipe | FITTED per galaxy (as P4) | |
| A8 | spherical enclosed mass from V_bar² r/G | P4 / CFG695 | STANDARD-MOND-MACHINERY (spherical approximation of a disc) | P4 showed EFE / geometry move rms < 0.001 dex |
| A9 | Z2 per-system CSV (ISO, MOND, V3S, V3D predictions; x_e, M_V, clean flags) | `rebuild_2026_10_22/Z2_satellite_systematics/z2_per_system.csv` | inherits Z2's ledger (static spherical MW, PM orbits, N_eff proxy) | read-only |
| A10 | F1 cluster A_MID (AQUAL on eRASS1 gas + KiDS) | `rebuild_2026_10_22/F1_cluster_cores/README.md` | inherits F1's ledger (eRASS1 gas SURVEY-CALIBRATION, native h) | read, not recomputed |
| A11 | P4 T5 TDG / DF2-DF4 rows; U1 dust-free TDG row | P4, U1 | inherits | read |
| A12 | EdS background for the top-hat (N1) | this lane | ΛCDM-form background in its dust limit (native at high z); Λ neglected | flag: Λ only delays both arms |
| A13 | WKB local stability (S4, R2) | this lane | approximation | R2 numbers are order-of-magnitude, labelled WKB |
| A14 | Ω_c/Ω_b = 5.36 | Planck-like | ΛCDM-PROCESSED | reported only, never a verdict |
| A15 | H₀ = 67.9 for 1/H₀ | native band 67.2–68.6 (C2) | FRAMEWORK-NATIVE | |
| A16 | Bohm-type stiffness D = L★^{3/2} a₀^{1/2}, L★ = 22 pc; compressional c² = g L★ | this lane (f) | POSTULATED (built only from allowed scales) | tested as an escape |
| A17 | BLT dipolar reading, CFG121/122 results | record | read | provisional where those lanes say so |

Original verdicts this lane revisits: the D-T dichotomy (U1 / TM1 / Y1 / PH1 / O1) and CFG660's open question
("whether a two-variable law Π(ρ_c, g) can keep the law as an exact equilibrium for every baryon profile").
