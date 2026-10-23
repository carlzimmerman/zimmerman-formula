# H2_aest_clusters — assumption ledger (before any number; committed with the frozen criteria)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / EXTERNAL-THEORY.

| # | ingredient | class | source | note |
|---|---|---|---|---|
| H1 | per-cluster KiDS ΔΣ, weights, boost, 326 clusters | RAW (F1's own estimator) | F1 scratch `f1_meas.pkl` (sha256 961ea4fc…e720), read-only | same object F1's verdict used |
| H2 | gas β-model (β = 2/3, r_c = 0.15 R500, to 3 Mpc), Mgas500 rescaled q^{5/2}, f* = 0.20 | SURVEY-CALIBRATION / EXTERNALLY-CALIBRATED; R500 ΛCDM-PROCESSED | F1 `gas_mass()`, ledger A9–A12 | inherited unchanged; F1 brackets them |
| H3 | distances: DESI DR2 D_M/r_d × 101.54/h, native h 0.672 / 0.686 | RAW × FRAMEWORK-NATIVE (C2) | F1 `DM()` | |
| H4 | data boost and catalogue miscentring (F1 PRIMARY) | as F1 (A1 caveat: boost < 1 is a deficit) | F1 | A1 clipped rows also reported |
| H5 | AeST quasi-static equations, μ definition, μ⁻¹ ≳ 1 Mpc | EXTERNAL-THEORY, verified on disk | `_external_data/aest_papers_2026_10_22/` (outside repo; C2 PROVENANCE sha256) | VSZ L294–L311, SZ21 L362–L382 |
| H6 | λ_s → ∞ with C1's capped 𝒥 ⇒ AQUAL μ = x/(1+x) | FRAMEWORK-NATIVE (C1 K2) | C1 README | health of the cap OPEN (C1, C2) |
| H7 | zero point of Φ (VSZ Δ; Mistele's chemical potential) | FREE INTEGRATION CONSTANT of AeST | VSZ §Boundary conditions | Δ = 0 is VSZ's fiducial; any other value is a knob |
| H8 | VSZ Δ prescription transplanted from a point mass to the extended baryon profile (M = M_b(<3 Mpc), imposed at 3 Mpc on the μ = 0 solution) | EXTERNAL-THEORY, approximate | VSZ eq_chioutmax | the envelope over Δ covers any error in this transplant |
| H9 | galaxy RAR guard: Hernquist 1e11 M☉, a_h = 3 kpc, ≤ 10 % to 200 kpc | EXTERNAL-THEORY criterion (VSZ L765) | | the strict lensing-RAR bound (Mistele+23) is a record transcription only |
| H10 | dust (b), CDM-like branch | ΛCDM-PROCESSED (NFW c* = 0.40, L187) | F1 addendum A2 | cited, not recomputed, never graded |
| H11 | a₀ footings, κ = ½ | FITTED | F1 | |
| H12 | spherical symmetry | FRAMEWORK choice | | AeST curl mode vanishes (VSZ footnote); asphericity not solved |

No ΛCDM or standard-MOND machinery enters the AeST prediction itself; H2/H4/H10 are inherited exactly as F1 classified them.
