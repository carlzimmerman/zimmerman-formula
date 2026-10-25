# NU1_cluster_gap_sources — assumption ledger (before any number; committed with the frozen criteria)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / EXTERNALLY-CALIBRATED /
PROVISIONAL (external fact quoted from memory of the literature, no download; to be checked before citing).

## A. Inherited (read-only) — the gap itself

| # | ingredient | class | source |
|---|---|---|---|
| A1 | KiDS-1000 shear stack on 326 eRASS1 clusters (D, E, Dx, DRR, den, den_r, source moments) | RAW | X2 `x2_replay_percluster.npz` (= F1's cache, X2 R1/R2) |
| A2 | eRASS1 Mgas500, R500, z, offsets; gas rescaled q^{5/2} from ΛCDM(70, 0.3) distances | SURVEY-CALIBRATION; R500 ΛCDM-PROCESSED (aperture only) | F1 B3/B6/B7 |
| A3 | distances: raw DESI D_M/r_d × r_d with native h 0.672 / 0.686 | RAW × FRAMEWORK-NATIVE | F1 B5 |
| A4 | field equation AQUAL μ = x/(1+x), spherical (= QUMOND identity in spherical symmetry) | FRAMEWORK-NATIVE | F1 B4/K5 |
| A5 | gas β-model (G0) / CFG814 r⁻³ beyond 2.2 R500 (C\*), f* 0.20 | EXTERNALLY-CALIBRATED | F1, X2 (a1) |
| A6 | EFE noclu (Chae+21 median environment), reduced shear (C\*) | RAW-derived / FRAMEWORK-NATIVE solver (F2) | X2 (c1), (d) |
| A7 | X7 CAL errors: PSF leakage regression, cross-shear excess over 200 rotations, R−R excess | RAW (statistics) | X7 JSON, commit b1a2ffcb6b |
| A8 | terciles in catalogue Mgas500 (carries eRASS1 selection) | SURVEY-CALIBRATION | X7 / X2 |
| A9 | κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10 | FRAMEWORK-NATIVE (fitted) | |

## B. New in this lane

| # | ingredient | class | note |
|---|---|---|---|
| B1 | oscillation splittings Δm²₂₁ ≈ 7.4e-5, |Δm²₃₁| ≈ 2.5e-3 eV² → Σ_min 0.0588 (NO) / 0.0995 (IO) | RAW (laboratory/oscillation), PROVISIONAL values | |
| B2 | record value Σ = 0.0613 eV (m₁ = ρ_Λ^{1/4}, NO) | FRAMEWORK-RECORD hypothesis (not a derivation; 3σ DESI tension) | real_research/neutrino_desi_2026_10_06 |
| B3 | KATRIN m_β < 0.45 eV (90 % CL) | RAW (laboratory, cosmology-agnostic), PROVISIONAL | three degenerate states → Σ ≤ 1.35 eV |
| B4 | Ω_ν h² = Σ / 93.14 eV (relic abundance from thermal decoupling, T_ν = (4/11)^{1/3} T_γ) | standard thermal history (not ΛCDM-fitted); T_CMB RAW | |
| B5 | Ω_b h² = 0.0222 (BBN deuterium) | RAW-derived (D/H + nuclear rates), PROVISIONAL | the record's covariant lane uses a BBN bound (A78) |
| B6 | fair-share infall cap M_ν(<3 Mpc) ≤ (Ω_ν/Ω_b) M_b(<3 Mpc) | FRAMEWORK-NEUTRAL physical bound | generous: ignores free-streaming suppression |
| B7 | Tremaine–Gunn fine-grained cap f ≤ ½ per helicity state; v_esc to R_ta = 5 Mpc (3, 10 reported) in the law's own potential | FRAMEWORK-NATIVE potential; R_ta is a declared bracket, not fitted | AQUAL potential is logarithmic, so R_ta must be stated |
| B8 | hot-gas calibration maxima: X-COP 1.236 (N 5), ACCEPT 1.034 (N 51), CFG922 1.081 (N 68, 16–84 % 0.73–1.50) | RAW X-ray / SURVEY-CALIBRATION | F1 C3d, CFG922 |
| B9 | stars incl. ICL: f* ≤ 0.30; X-COP measured M*/M_gas(<0.5 Mpc) ≤ 0.104 | EXTERNALLY-CALIBRATED / RAW (X-COP stellar profiles) | ICL not on disk |
| B10 | cold gas ≤ 2e11 M☉ per cluster | RAW (xGASS HI bracket, CFG922) + PROVISIONAL (BCG H₂ literature) | |
| B11 | clumping and hydrostatic bias add no baryon mass in this pipeline | logic (CFG922 2c/2d) | |
| B12 | sterile-neutrino constraints (BBN N_eff, laboratory sterile searches, small-scale structure) | PROVISIONAL, words only | reported, never adopted |

No ΛCDM halo, NFW, mass function, CMB-fitted Σm_ν or CMB-fitted Ω_c/Ω_b enters any graded number.
