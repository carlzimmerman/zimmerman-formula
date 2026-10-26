# IJ1 — ASSUMPTION LEDGER (frozen with FROZEN_CRITERIA.md)

Tags: RAW (observed); FRAMEWORK-NATIVE (derived in the record from the framework); FITTED (named number calibrated on data);
SURVEY-CALIBRATION (a catalogue's own reduction); DUST-N-BODY (collisionless N-body calibration, simulations not run here);
ΛCDM-LEAK (an input on the owner's 10-25 list; OPEN gap, never a framework result); EXTRAPOLATED; POSITED (the hypothesis).

| # | input | tag | source | note |
|---|---|---|---|---|
| L1 | a₀ = κ c √(Gρ_Λ), κ = ½; Σ_a0 = a₀/(2πG) | FITTED (κ) / FRAMEWORK-NATIVE | record, X38 | footings never pooled |
| L2 | isothermal core inside r₁, collisionless outside, Γ t = 1 at r₁ | POSITED (hypothesis IJ) | standard self-interacting-halo construction | v = (4/√π) σ₀, t = 13.8 Gyr |
| L3 | s(v) = K (√π/4)^(1−n) v^(−n), n = 2 q_f − 1, K at the SC1 anchor | FITTED (q_f, once on SPARC, OS1) / FRAMEWORK-NATIVE (anchor) | BU1, LN2, OS1 | zero free parameters in PRIMARY |
| L4 | variant amplitude A | FITTED (once, SPARC only) | this lane | reported only |
| L5 | NFW outer profile | DUST-N-BODY; ΛCDM-LEAK | EM1 (A7) | OPEN gap |
| L6 | Bullock+01 c(M, z), K = 4, F = 0.01, on backgrounds A / B CLASS P(k) | DUST-N-BODY; ΛCDM-LEAK | EM1 (A8) | applied to M200c (EM1's disclosed mismatch) |
| L7 | M200 = 10^(a + b(log M_b − 10)) | FITTED (EM1 R1, SPARC, NFW halos); ΛCDM-LEAK (owner 10-25) | EM1 | EXTRAPOLATED to clusters, groups, SLUGGS, dwarfs |
| L8 | backgrounds A / B (h, ω's) | FRAMEWORK-NATIVE refit backgrounds | F3 K2 | |
| L9 | branch rule (lowest-ρ₀ no-baryon root, continued in λ) | convention, frozen | this lane | multiplicity reported |
| L10 | SPARC rotmod, Lelli 2016c, P4 mask / weights / Υ grid | RAW (survey-reduced) | EM1 | baryon profile interpolation rules in criteria §1 |
| L11 | eRASS1 × KiDS bands, X30 cluster gas model, gas × 1.2 for stars, r_ta | RAW / record convention | X30 (read-only) | X30's `DA_lcdm` rescaling is a ΛCDM-LEAK, inherited |
| L12 | CFG922 BCG masses, tercile fill, Hernquist a = 10 kpc | RAW-derived / record convention | X39 / X40b | |
| L13 | cluster fair share 5.364 M_b | ΛCDM-LEAK | X30 `prep` | reported-only comparator row; not in any grade |
| L14 | Tian+2026 groups (σ_LOS, M_b, R_e); P4 T3 estimator | RAW / SURVEY-CALIBRATION / record convention | GR1 | on disk outside git |
| L15 | SLUGGS GC bins, profiles, anisotropy, M_JAM, a_h, distances | RAW / SURVEY-CALIBRATION | CFG528b via GR1 | host halos for M87 / NGC 5846 omitted (isolated) |
| L16 | X1 dwarfs: Δ[Newton], sd, M★, r_h | RAW-derived (binary-corrected) | X1 | isolated reading, no host stripping |
| L17 | Plummer stars for dwarfs (a = r_h) | approximation | this lane | dwarfs are halo-dominated at r₁₂ |
| L18 | t = 13.8 Gyr for every system | POSITED (hypothesis) | brief | clusters at z ≈ 0.1–0.6 not age-corrected |
