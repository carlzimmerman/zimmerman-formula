# S4_v3_muK_clusters — assumption ledger (before any number; committed with the frozen criteria)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / EXTERNAL-THEORY / FITTED.

## A. Inherited verdicts being recomputed

| # | ingredient | class | source | note |
|---|---|---|---|---|
| A1 | F1 per-cluster KiDS ΔΣ, weights, boost, 326 eRASS1 clusters | RAW (F1's own estimator) | F1 `f1_meas.pkl` (session scratch, sha256 961ea4fc…e720), read-only | same object F1, H2, J1, K1, M2 used |
| A2 | gas β-model (β 2/3, r_c 0.15 R500, to 3 Mpc), Mgas500 × q^{5/2}, R500 × q, f★ = 0.20 | SURVEY-CALIBRATION / EXTERNALLY-CALIBRATED; R500 ΛCDM-PROCESSED (aperture only) | F1 ledger A9–A12, B6–B10 | inherited unchanged; F1 brackets them (C3) |
| A3 | distances DESI DR2 D_M/r_d × 101.54/h, h 0.672 / 0.686 | RAW × FRAMEWORK-NATIVE (C2) | F1 `DM()` | |
| A4 | data boost and catalogue miscentring (F1 PRIMARY) | RAW (A1 caveat: boost < 1 is a deficit) | F1 | A1-clipped rows reported |
| A5 | F2 Track A: B21 Fig. 3 ESD + released covariance, (1+K) | RAW + SURVEY-CALIBRATION | F2 ledger R1/D1 | |
| A6 | F2 lens inventory: M★ LePhare + 0.15, cold-gas relation, hot CGM 0.5 M★ uniform to 100 kpc; lens weights | SURVEY-CALIBRATION | F2 ledger B1–B3, G1 | F2's central configuration only |
| A7 | F2 native conversion h 0.679, Ω_m 0.3085, T_Ωm 1.0128 | FRAMEWORK-NATIVE / SURVEY-CALIBRATION | F2 ledger H1/H2 | |
| A8 | F2 EFE ratio C(r; y_e) for a point mass in a uniform field (AQUAL, own solver) | FRAMEWORK-NATIVE (equation) × SURVEY-CALIBRATION (y_e from Chae+21) | F2 `f2_aqual.py`, read-only import | used only in the labelled y_e = noclu approximation |

## B. This lane's model

| # | ingredient | class | source | note |
|---|---|---|---|---|
| B1 | static equation ∇·[μ(|∇ψ|/a₀)∇ψ] + μ_K²ψ = 4πGρ_b, μ = x/(1+x); ϕ = ψ | FRAMEWORK-NATIVE (v3), J = J_x POSTULATED (outside BS's class, C4); BS24 equations EXTERNAL-THEORY read via WebFetch (PROVISIONAL), re-derived from the action in C4 K1 (residual 0) | C4 README §1–2; L1 §1 | the record's transcription; not verified on disk |
| B2 | the μ_K² term = hydrostatic K(Q) dust, 4πG δρ_K = −μ_K²ψ; no separate dust source (no double counting) | FRAMEWORK-NATIVE reading | L1 §1; F3 K1(ii) | static branch only; the dust's non-static (collapsed, CDM-like) branch needs a simulation (L1) |
| B3 | spherical symmetry | FRAMEWORK choice | | asphericity not solved (as F1) |
| B4 | zero point of ψ: VSZ λ_max + Δ on the μ_K = 0 solution at 3 Mpc (H2's convention), Δ = 0 primary, universal Δ envelope | EXTERNAL-THEORY convention for a FREE integration constant | VSZ eq_chioutmax via H2 (H7/H8) | Δ ≠ 0 counted as a knob; any regular solution decays at infinity, so no boundary condition fixes it |
| B5 | μ_K allowed range μ_K⁻¹ ≥ 100 kpc (BS24 Eq. 39) | EXTERNAL-THEORY premise (μ_K is not in v3's parameter table, F3 §7) | F3 K4/K5; C4 | not fitted; scanned on a fixed grid |
| B6 | growth-motivated μ_K = 243.78 / 277.82 / 1718 Mpc⁻¹ | FRAMEWORK-NATIVE (F3's linear ODE on CLASS dust-limit spectra) | F3 K5 `inv_mu_min_kpc_phys` | excluded by B5; reported only |
| B7 | ρ̄_K for the dust-sign diagnostic: Ω_K = Ω_m − Ω_b on model B | FITTED abundance (C2/C4); model B FRAMEWORK-NATIVE in the dust limit (CFG886 GR fit, BAO + BBN) | L1 ledger | diagnostic only |
| B8 | annulus averaging of predicted ΔΣ (P2/P3) | estimator convention (data are annulus averages) | | F1's centre value (P1) reported alongside |
| B9 | r_max = 30 Mpc (clusters and graded galaxy rows), M_L constant beyond | pipeline convention (F1's grid) | | 30 → 60 Mpc sensitivity reported |
| B10 | κ = ½, footings 9.3603e-11 / 1.1312e-10 | FITTED | | never pooled |
| B11 | R4: v3 kernel ν₁(y) = (1 + √(1 + 4/y))/2 (the spherical AQUAL root for μ = x/(1+x)) replacing ν_mono | FRAMEWORK-NATIVE | C4 K2, E2 | kernel only: each script's geometry, data, rules and verdict code unchanged |
| B12 | R4 tile 22 v3 reading: no host ownership (R-own → R-bar) | FRAMEWORK-NATIVE (v3 has no ownership, N0 tile 22) | | other R4 scripts: kernel swap only |

No ΛCDM halo, NFW, HMcode, mass function or QUMOND-phantom machinery enters any R6 prediction. R4 runs the record's
scripts unchanged apart from the kernel; whatever ΛCDM-PROCESSED inputs those scripts carry are theirs (each lane's
ledger), and the swap does not touch them.
