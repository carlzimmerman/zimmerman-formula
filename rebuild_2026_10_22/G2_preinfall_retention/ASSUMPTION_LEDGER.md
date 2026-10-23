# G2_preinfall_retention ASSUMPTION LEDGER (written with the frozen criteria, before any number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / MODEL ASSUMPTION / POSITED RULE.

## A. What the original rule (PAPER36, CFG35–CFG39) rests on

| ingredient | PAPER36 / CFG35 | class | file |
|---|---|---|---|
| cold fluid Ω_c h² = 0.12, CDM-like before turnaround (T4) | "fitted as in ΛCDM" | ΛCDM-PROCESSED (abundance) | PAPER36 §1; CFG35 L56 |
| "pressureless and conserved ⇒ feedback cannot remove it ⇒ keeps collapse mass" | derivation by assertion | POSITED RULE for bound-system retention (total-mass conservation ≠ enclosed-mass conservation under tides) | PAPER36 §3 |
| T5: the fluid first *is* the phantom; leftover keeps collapse profile, unused by the law | identity + posit | POSITED RULE (CFG939: S4 free population NOT DERIVABLE from S2+S3; CFG888: no coupling in the record) | PAPER36 eq. 1 |
| M_coll | Moster+13 SHMR (CFG35), Mandelbaum+16 lensing halo masses (CFG36) | ΛCDM-PROCESSED (abundance matching on ΛCDM halo mass function; lensing halo-model NFW fits) | `hunt_2026/h48_h69b_relative_isolation.py` L83-88 |
| collapse profile | NFW, Dutton & Macciò 2014 c(M) | ΛCDM-PROCESSED (ΛCDM N-body calibration) | h48 L90-96 |
| edge x_e = 0.40 r_ta | B's edge | POSITED RULE (record) | CFG35 L71-75 |
| f_b = Ω_b/Ω_m | Planck | ΛCDM-PROCESSED | CFG35 L56 |
| calibration domain | massive ellipticals, log M* 10.3–11.5 | — (never tested below log M* ≈ 10) | PAPER36 §4 |

## B. What the dwarf baseline (E3) rests on (inherited, unchanged)

| ingredient | class | file |
|---|---|---|
| σ_los, R_e, M_V/M*, distance modulus, PMs, v_sys, [Fe/H] | RAW (LVD) / SURVEY-CALIBRATION (distances, SPS Υ_V = 2) | `real_research/data/dsph/lvd_dwarf_*.csv` |
| binary correction (Arroyo-Polonio free-f) | SURVEY-CALIBRATION | `campaign_fresh_gravity/CFG257_ufd_kinematics_scoping/arroyo_polonio2026_tableA1.csv` |
| Wolf mass 3σ² r12 / G | MODEL ASSUMPTION (equilibrium) | E3 |
| screened law B_scr = 1 + S(r12/ℓ)(ν − 1), L★ = 24 pc, CFG691 S table | FRAMEWORK-NATIVE (L★ fitted bound; κ = ½ FITTED); spherical AQUAL = QUMOND for the system's own field | E3 L42-66 |
| host baryons MW 6e10, M31 1e11 | SURVEY-CALIBRATION / external | E3 L24 |

## C. What this lane adds

| ingredient | class | sensitivity handled by |
|---|---|---|
| M_coll FREE (f_ret = 1) | FRAMEWORK-NATIVE floor (present baryons only) | cell |
| M_coll CHEM (E6 L_min) | SURVEY-CALIBRATION + MODEL (leaky box, ζ = 1 winds, no pre-enrichment) | two corners |
| M_coll CENSUS / SHMR | ΛCDM-PROCESSED | reported separately |
| top-hat (18π²) and B85 r^{3/4} profiles | FRAMEWORK-NATIVE in the sense of E6 D1 (outside the law ball, shells move as GR dust + Λ); idealised spherical collapse | two profiles |
| NFW DM14 | ΛCDM-PROCESSED | reported separately |
| z_coll ∈ {6, 10, 15} | MODEL BRACKET | three values |
| native background h = 0.674, Ω_m = 0.313 (E6 / CFG654 native column; inside the native H0 67.2–68.6) | FRAMEWORK-NATIVE background with CMB-fit parameters | — (enters r_vir ∝ ρ̄^{-1/3}) |
| Galactocentric frame R0 8.122 kpc, z⊙ 20.8 pc, v⊙ (12.9, 245.6, 7.78) km/s | SURVEY-CALIBRATION (astropy defaults v4.0) | — |
| host turnaround R_ta(t) ∝ t^{8/9}, R_ta0 ∈ {0.83, 1.10} Mpc | MODEL (self-similar infall, GR dust) + record (CFG548 K4) | bracket; only sets ζ |
| tidal radius at pericentre in the host law field (no EFE) | FRAMEWORK-NATIVE | — |
| TDG / DF2 / DF4 data | RAW + SURVEY (Lelli+15; CFG655/657 table) | — |
| NGC 1052 host baryons 1e11, D = 20 Mpc | external / SURVEY | bracket ×0.5–3 reported |

No STANDARD-MOND-MACHINERY is used: no EFE, no QUMOND phantom-as-gravity beyond the spherical identity, no deep-MOND shortcuts.
