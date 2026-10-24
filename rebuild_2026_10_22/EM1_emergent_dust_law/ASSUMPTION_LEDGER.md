# EM1_emergent_dust_law — ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / DUST-N-BODY / EXTERNALLY CALIBRATED / FITTED / POSITED.

| # | ingredient | class | source |
|---|---|---|---|
| A1 | route E itself: cold sector = pressureless dust everywhere, no law force | POSITED (the road under test) | V3S verdict §6 |
| A2 | SPARC rotmod + Lelli 2016c table, P4 mask/weights/Υ grid | RAW (survey-reduced) | `real_research/data/sparc_data`, P4 |
| A3 | spherical g_bar = V_bar²/r | approximation, P4-declared | P4 |
| A4 | M_b,ref = 0.5 L36 + 1.33 M_HI (relation axis only) | convention | this lane |
| A5 | backgrounds A / B (ω_b, ω_c, h, A_s, n_s) | FRAMEWORK-NATIVE in the dust limit (plik-lite foregrounds SURVEY-CALIBRATION) | F3 K2 |
| A6 | CLASS linear P(k), D(z) | FRAMEWORK-NATIVE in the dust limit (route E's linear sector is ΛCDM's) | CLASS |
| A7 | NFW profile shape | DUST-N-BODY (dust's own nonlinear solution; simulations not run here) | NFW 1997 |
| A8 | Bullock+01 c(M, z), K = 4, F = 0.01, applied to M200c | DUST-N-BODY calibration; mass-definition mismatch disclosed | Bullock+01 |
| A9 | (a, b) global halo relation | FITTED to SPARC (in-sample, two globals) | this lane |
| A10 | DC14 profile + c boost | EXTERNALLY CALIBRATED (hydro feedback); secondary row only | Di Cintio+14, CFG477 code form |
| A11 | ν_e (μ = x/(1+x)) as the fitting form for g† | FRAMEWORK-NATIVE law form used as a ruler only | THEORY_V3_DRAFT |
| A12 | a₀(z) framework band 0.91–0.94 at z 2.33 | FRAMEWORK-NATIVE | CFG689 |
| A13 | no adiabatic contraction, no EFE, isolated | approximation | this lane |
