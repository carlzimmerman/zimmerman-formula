# K1_braneworld_weyl — assumption ledger (before any number; committed with the frozen criteria)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / EXTERNAL-THEORY /
POSTULATE (this lane's, counted).

| # | ingredient | class | source | note |
|---|---|---|---|---|
| L1 | per-cluster KiDS ΔΣ, weights, boost, 326 clusters | RAW (F1's own estimator) | F1 scratch `f1_meas.pkl` (sha256 961ea4fc…e720), copied read-only | same object F1, H2 and J1 used |
| L2 | gas β-model (β = 2/3, r_c = 0.15 R500, to 3 Mpc), Mgas500 rescaled q^{5/2}, f* = 0.20 | SURVEY-CALIBRATION; R500 ΛCDM-PROCESSED | F1 `gas_mass()`, F1 ledger | inherited unchanged; F1 brackets them |
| L3 | distances: DESI DR2 D_M/r_d × 101.54/h, native h 0.672 / 0.686 | RAW × FRAMEWORK-NATIVE (C2) | F1 `DM()` | |
| L4 | data boost, catalogue miscentring (F1 PRIMARY) | as F1 (A1: boost < 1 is a deficit) | F1 | clipped-boost CAL reported |
| L5 | law: AQUAL μ = x/(1+x), spherical root | FRAMEWORK-NATIVE (E2, C4) | F1 `g_aqual_sph` | κ = ½ FITTED; footings never pooled |
| L6 | SMS effective equations; E_μν decomposition (U, P, Q) | EXTERNAL-THEORY, not verified on disk | arXiv:gr-qc/9910012; gr-qc/0312059; 1004.3962 | static consequences re-derived (sympy) |
| L7 | brane tension λ_b ≥ (1 TeV)⁴; RS2 AdS length ℓ ≤ 0.1 mm | EXTERNAL (table-top / review values), not verified on disk | arXiv:1004.3962 | used only for bounds |
| L8 | RS2 linear potential −GM/r(1 + 2ℓ²/3r²) | EXTERNAL-THEORY (bulk solution), not verified on disk | arXiv:hep-th/9911055 | B1 |
| L9 | DMPR tidal-charge metric | EXTERNAL-THEORY, exact vacuum solution re-verified with sympy | arXiv:hep-th/0003061 | C2 |
| L10 | linear EOS P = wU; HC flat-rotation closure | EXTERNAL-THEORY, not verified on disk (HC arXiv id recalled) | gr-qc/0404104; ApJ 636, 8 | C1; w = 1 ⇔ U ∝ r⁻² derived here |
| L11 | DGP decoupling-limit equation, β, r_c = c/H₀ | EXTERNAL-THEORY, not verified on disk | hep-th/0404159; hep-th/0702169 | B2, order of magnitude and sign only |
| L12 | closure P = 0 / w = 1 / P = −2U per element | POSTULATE (one per closure) | this lane | the brane equations leave this function free |
| L13 | LINK: static Weyl asymptote = cosmological dark radiation today | POSTULATE | this lane | only C0; enables R4 |
| L14 | zero point / truncation r_ref = 3 Mpc | RULE (POSTULATE) | this lane, F1's outer edge | r_ref = 10 Mpc reported |
| L15 | normalisations v_W² = ξ₁√(GM_b a₀) (C1), Q = −2G dm ℓ_Q/c² (C2) | POSTULATE + 1 constant each | this lane | |
| L16 | A-ADD: Weyl acceleration added to the law's (not fed through AQUAL) | POSTULATE | this lane | E_μν is geometry and traceless |
| L17 | BBN: |ΔN_eff| ≤ 0.30, N_eff = 3.046, x = (7/8)(4/11)^{4/3} | EXTERNAL (Planck 2018 + BBN) as used by the record | A78 `a78_checks.py` L46–47, read-only | |
| L18 | Ω_γ h² = 2.469e-5 | EXTERNAL constant as used by the record | C2 `c2_aest_cosmology.py` L135 | |
| L19 | isolated lens masses log M_b 10.36 / 10.83 / 11.01 / 11.18; R1 tolerance 0.14 | SURVEY-CALIBRATION (LePhare M★) via F2 | F2 results `trackA.canonical.L1_no_edge_B` | Plummer b = 5 kpc is this lane's choice (irrelevant beyond 0.4 Mpc) |
| L20 | dwarf satellites: σ, R_h, M★, binary ratio, B_scr at L★ = 24 pc | RAW / SURVEY-CALIBRATION / FRAMEWORK-NATIVE as E3 | E3 `e3_per_system.csv`, LVD `real_research/data/dsph/` distances | central values (E3 used MC) |
| L21 | MW 6.0e10 M☉, M31 1.0e11 M☉ Hernquist a = 3 kpc; R₀ = 8.122 kpc | SURVEY-CALIBRATION (record values) | J1 frozen criteria (CFG332, E3, D10/A60) | |
| L22 | planet bounds 8.7e-15 / 1.4e-15 / 7.0e-15 m/s²; Cassini γ − 1 = (2.1 ± 2.3)e-5 | RAW-derived ephemeris bounds as used by the record | C6 L35; `openai_push/final_closure/gate_lensing_weakfield_derivation.py` L140 | |
| L23 | spherical symmetry; weak field, leading order in Φ/c² | FRAMEWORK choice | | |Φ|/c² ≤ 1e-4 everywhere used |

No ΛCDM machinery and no standard-MOND machinery enters any Weyl prediction. L2/L4 are inherited exactly as F1 classified them.
