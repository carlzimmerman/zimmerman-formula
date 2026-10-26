# GR1 — ASSUMPTION LEDGER (frozen with FROZEN_CRITERIA.md)

Each input is tagged with one of:
- RAW: observed;
- FRAMEWORK-NATIVE: derived in the record from the framework;
- FITTED: one number calibrated on data, named;
- SURVEY-CALIBRATION: a catalogue's own reduction;
- EXTRAPOLATED: used outside its calibration range.

No ΛCDM-processed input enters. No Planck number enters. No background beyond EM1's own CLASS background A enters.

| # | input | tag | source | note |
|---|---|---|---|---|
| 1 | a₀ = κ c √(Gρ_Λ), κ = ½ | FITTED (κ) | record; footings 9.3603e-11 / 1.1312e-10 | never pooled |
| 2 | Σ_a0 = a₀/(2πG) | FRAMEWORK-NATIVE | X38 | |
| 3 | q_f = 0.892 / 0.748 | FITTED (once, SPARC only) | OS1 a8b817e19e | read from JSON, never moved |
| 4 | σ_ref = 70.50 km/s | RAW (median SPARC V_last/√2) | SC1 | |
| 5 | M200(M_b) = 10^(a + b(log M_b − 10)), h_A | FITTED (EM1 R1, SPARC) / FRAMEWORK-NATIVE background | EM1, F3 | EXTRAPOLATED to groups and SLUGGS |
| 6 | Burkert profile, compact root | FRAMEWORK-NATIVE choice of X38 | X38 A1 | |
| 7 | group σ_LOS, M_b, R_e | RAW / SURVEY-CALIBRATION | Tian+2026 (on disk, outside git) | M_b is the catalogue's baryonic mass |
| 8 | group estimator: Hernquist tracer, whole-system aperture, 10 % slope systematic | record convention | P4 T3 / CFG540 | executed read-only |
| 9 | SLUGGS GC σ_LOS bins and bootstrap errors | RAW (statistical only) | CFG331 / CFG466 | |
| 10 | GC density profiles and anisotropy (row M) | RAW (published fits) | CFG528b (FETCH_LOG, SHA-256 checked) | β = 0 for the two unmeasured galaxies |
| 11 | M_JAM, r12, Hernquist a_h = R_e/1.8153 | SURVEY-CALIBRATION (ATLAS3D JAM) | CFG331 / CFG528 | M★ is set by the route-E JAM analogue |
| 12 | distances | SURVEY-CALIBRATION (SBF) | CFG331 | |
| 13 | Salpeter M/L (reported only) | SURVEY-CALIBRATION | ATLAS3D via CFG528 `Mpop` | |
| 14 | hot gas (reported only, 'bar') | RAW-derived | CFG331 `gas_on_RG`, extrap | |
| 15 | host halos for M87 / NGC 5846 | **omitted** | — | isolated reading, disclosed |
| 16 | red KiDS lenses | **not graded** | — | no σ per lens under V2 (criteria §1c) |
