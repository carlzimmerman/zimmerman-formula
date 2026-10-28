# HO2 — ASSUMPTION LEDGER (frozen with FROZEN_CRITERIA.md)

Tags: RAW (observed); FRAMEWORK-NATIVE (derived in the record); FITTED (one number calibrated on data, named);
EXTERNAL (one number not derived); SURVEY-CALIBRATION (a catalogue's own reduction); EXTRAPOLATED (used outside its
calibration range); PROVISIONAL (recalled, not checked against a file). No Planck number and no ΛCDM background enters;
the only backgrounds are EM1's CLASS backgrounds A (graded) and B (reported).

| # | input | tag | source | note |
|---|---|---|---|---|
| 1 | a₀ = κ c √(Gρ_Λ), κ = ½ | FITTED (κ) | record; 9.3603e-11 / 1.1312e-10 | never pooled |
| 2 | ν(y) = ½ + √(¼ + 1/y) | FRAMEWORK-NATIVE (CL2 harness `nu`, P4 `nu1`) | X62 / CL2 | not CFG528b's ν_mono; the law branch here uses this ν |
| 3 | switch T = 10^12.3 M☉ on M200 | FITTED (CF2 window, CL2 point) | CL2 b57ed8751f | strict `>` |
| 4 | M200(M_b) = 10^(a + b(log M_b − 10)) | FITTED (EM1 R1, SPARC) | EM1 | EXTRAPOLATED to SLUGGS (log M★ ≈ 11–12) |
| 5 | Σ_a₀ = a₀/(2πG) | FRAMEWORK-NATIVE | X38 | |
| 6 | Σ_coll(M), Lacey–Cole half-mass collapse | FRAMEWORK-NATIVE (EM1 CLASS P(k)) | X43 `sigma_coll` | |
| 7 | η = (4/(3B(1))) c_f^{5/4} | FRAMEWORK-NATIVE (self-similar infall) | X43 | |
| 8 | c_f level L = 4 | EXTERNAL (the record's one external c_f level) | X43 / CL2 | |
| 9 | c_f mass slope c_nat(M) (S9) | FRAMEWORK-NATIVE (zooms, not converged in level) | X48 ng48 A2 | clamped outside 10^12–10^14 |
| 10 | Burkert, ρ₀r₀ = Σ, compact root, M200 in R200 | FRAMEWORK-NATIVE choice | X38 A1 | |
| 11 | SLUGGS GC σ_LOS bins, bootstrap errors | RAW (statistical only) | CFG331 / CFG466 | |
| 12 | GC density profiles, anisotropy (row M) | RAW (published fits) | CFG528b | β = 0 for the two unmeasured galaxies |
| 13 | M_JAM, r₁₂, a_h = R_e/1.8153, distances | SURVEY-CALIBRATION (ATLAS3D, SBF) | CFG331 / CFG528 | M★ set by the route-E JAM analogue |
| 14 | SLUGGS classification (host centres / accreted) | record convention | CFG331 / CFG528 / GR1 | decides the branch |
| 15 | host R500 (Virgo 0.70, NGC 5846 group 0.38 Mpc) | PROVISIONAL | CFG528 template | used only for the branch of the two host centres |
| 16 | host halos of M87 / NGC 5846 | **omitted** | — | GR1's isolated reading, disclosed |
| 17 | MW baryon family and grid (175 cells), L&N tags | SURVEY-CALIBRATION / published priors | X5 (M_bb axis PROVISIONAL) | unchanged |
| 18 | McMillan 2017 baryons | SURVEY-CALIBRATION | P4 `rho_mcm` (GD1/S3) | |
| 19 | Eilers+19 v_c, Bovy & Rix K_z (43 MAPs and summary), Ou+24 curve | RAW / SURVEY-CALIBRATION | X5 / P4 / S3 | S3's Ou error model |
| 20 | algebraic law on the disc field (pointwise ν on |g_N|) | modelling choice (CL2 harness form) | this lane | not AQUAL/QUMOND; disclosed |
| 21 | Tian+2026 groups (Step 0 only) | RAW / SURVEY-CALIBRATION | `_external_data/vizier2026` | outside git, on disk |
