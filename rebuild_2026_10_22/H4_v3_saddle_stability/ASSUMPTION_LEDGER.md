# H4_v3_saddle_stability — ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / EXTERNAL / ILLUSTRATIVE.

## A. What the record's statement rests on (P3's flag "G < 0 at saddles")

| ingredient | class | where | used here as |
|---|---|---|---|
| decoupling-limit pair action, Z = k²/(Q̄²(K M_L + γ_L k²)) + μ_K²/K, G = D·P(1 + γ_L D·P) + μ_K²(Q̄−1)/(K Q̄) | FRAMEWORK-NATIVE (P3 E1, E2, A2) | P3 script L922–1020 | reproduced (A3, B3) and extended by the self-gravity term (A4) |
| "only tensor modes propagate" (frozen-coefficient matrix) | FRAMEWORK-NATIVE, corrected by P3 | C5 H4, C8 K6 | superseded at first order in background gradients |
| BS phantom-fluid WKB dispersion ω² = Kρ_τ(k²f_θ − μ²)/(k²(1−f_θ) + μ²) | FRAMEWORK-NATIVE (BS24 PN system, transcribed) | BSK1 M4 | γ_L = 0 limit that A4 must reproduce |
| AQUAL saddle depth C(0.2d) = −0.2413 / −0.2404; EFE sweep | FRAMEWORK-NATIVE (record solves) | A38 §2.3, A23 §3–4 | solver validation (C1) only |
| v3 phantom = D·P = ∇·((1−μ)∇Φ)/4πG (AQUAL) | FRAMEWORK-NATIVE | A38 §3.2, C4 K1, A33 | the region maps |

## B. This lane's own ingredients

| ingredient | class | source |
|---|---|---|
| v3 action (β = η = γ_F = 0, ξ = 1, capped W, γ_L = K L★²/2, K(Q) = μ_K²(Q−1)²) | FRAMEWORK-NATIVE | C4, C5, C8, THEORY_V3_DRAFT §1 |
| BS24 PN system (Ξ = φ − σ̇ + ∣∇σ∣²/2, khronon continuity) | EXTERNAL (BS24, WebFetch transcription in C4/BSK1, PROVISIONAL); re-derived here from the PN Lagrangian (A1) | BSK1 L15–21, C4 |
| J_x (μ = x/(1+x) exactly) ⇒ M_T = 1 + x, M_L = (1+x)² | FRAMEWORK-NATIVE, POSTULATED outside BS's class | C4 K2, C5 |
| AQUAL static field (not QUMOND) | FRAMEWORK-NATIVE (the theory's own static limit) | C4 K1, A38 §3.2 |
| a₀ footings 9.36e-11 / 1.13e-10 m/s² | FITTED (κ = ½) | doors BRIEF |
| L★ ∈ {21.7 / 22.9 (floors), 24, 90} pc | FITTED | D10 via THEORY_V3_DRAFT §2; P3 grid |
| μ_K → 0 in the region maps | FRAMEWORK choice; S4: μ_K ≥ 0.1 Mpc⁻¹ fails the galaxy guard | S4 README |
| Ω_K = 0.26 dust offset, H₀ = 68.6 | EXTERNAL (BS25 via C4, illustrative) / FRAMEWORK-NATIVE (C2, A78) | C4 K7, BRIEF |
| masses, separations, Plummer and disc scales, relative speeds, lifetimes | ILLUSTRATIVE (round literature-scale values, not data) | FROZEN_CRITERIA §3 |
| external field g_e = 0.01 a₀ along the axis | ILLUSTRATIVE (record's cosmic-mean scale, A23) | A23 report §1 |
| Galactic u at the Sun: x_e = 1.15–2.6 | FRAMEWORK-NATIVE / SURVEY-CALIBRATION (MW field model) | C5 inputs (D7d `R2_scan`) |
| Plummer softening, grid, Picard solver | numerical method (own code) | this lane |
| WKB / frozen-background linearisation, first order in background gradients | ADOPTED method (as P3, BSK1); B2 checks one case without WKB | — |

No ΛCDM-processed input and no standard-MOND machinery carries a verdict: AQUAL is v3's own static limit, QUMOND is not used,
no NFW/halo model enters. No RAW survey data are used: this is a theory-consistency lane; the systems are illustrative
backgrounds and the verdict rules are set so that factor-2 changes in them cannot flip a verdict.

## C. Excluded on purpose

- Strong-field (NS, BH) backgrounds: P3's domain; reproduced only as sign-convention checks (B3).
- Moving and rotating backgrounds beyond a uniform boost (A6).
- Nonlinear evolution of the instability (reported as a reading, not computed).
- The hydrostatic μ_K² dust inside the AQUAL solve (S4's domain); size estimate only.
