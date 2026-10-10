# CFG590 FROZEN CRITERIA: the framework's matter power against cosmic shear, with the same baryonic feedback applied to both models

Date frozen: 2026-10-10. Committed alone, before any number of this lane is computed.

Settings: κ = ½ FITTED; footings canonical a0 = 9.3603e-11 and alt a0 = 1.1312e-10 m/s², never pooled; flat a0 = κ c √(G ρ_DE); kernel ν_mono; candidate B. The cold energy's MASS is still required; no particle species. Not "theory closed". Nothing is downloaded. Other lanes are read only.

## Question

The growth gate so far compared the framework with featureless (dark-matter-only) ΛCDM at ±10%. Real cosmic-shear data prefer small-scale power BELOW dark-matter-only ΛCDM (A_mod < 1). Judge the framework's predicted matter power directly against the KiDS-1000 and DES Y3 small-scale amplitude, with the SAME baryonic-feedback suppression applied to ΛCDM and to the framework, and judge ΛCDM-dark-matter-only by the same rule.

## Inputs (read only)

- **Framework ratio R(k)** = P_framework / P_ΛCDM from the halo model, z = 0, k = 1e-3 to 10 h/Mpc (260-point grid), per footing:
  - **PRIMARY:** CFG559 `halo_model/<foot>/PRIMARY_kin/R` (kinetic profile, α-free finite-age supply).
  - **Mainline variants (class reported; can set VARIANT-SENSITIVE):** CFG559 `VARIANT_full_kin`; CFG557 `TESTED`; CFG556 `census|cen` (sharp, full supply); CFG556 `census|emg` (emergent edge).
  - **Reported only:** CFG556 `census|s25`, `census|s55`, `fret1|cen`, `census|cen|r200scope`.
  - R(k < 1e-3) = 1; R(k > 10) = R(10). R is taken as z-independent (z = 0 values at all z). This is an assumption, disclosed in the README; the scaled family R_s = 1 + s (R − 1) is reported (not a verdict input) and the s at which the primary verdict class changes is quoted.
- **ΛCDM base:** CAMB (installed, version recorded) with HMcode-2020 dark-matter-only (`mead2020`) as P_NL(k, z) and CAMB linear P_L(k, z). Cosmology as CFG556: h = 0.6736, ω_b = 0.02237, ω_c = 0.1200, n_s = 0.965, σ8 = 0.811, massless neutrinos, flat.
- **Data (recalled, PROVISIONAL, as in CFG526):** Amon & Efstathiou 2022 KiDS-1000 A_mod = 0.858 ± 0.052; Preston, Amon & Efstathiou 2023 DES Y3 A_mod = 0.82 ± 0.04. S8 (reported only): KiDS-1000 0.759 (+0.024 / −0.021), DES Y3 0.759 (+0.025 / −0.023).

## Feedback (identical for both models; no tuning to data)

- S_fb(k, z; T) = P_HMcode2020-feedback(k, z; log T_AGN = T) / P_HMcode2020-DMO(k, z), computed by CAMB (`mead2020_feedback`). This is the BAHAMAS-calibrated hydro family, executed, not recalled.
- **Fiducial range:** T ∈ [7.6, 8.0] (the BAHAMAS suite). **Full declared range:** T ∈ [7.3, 8.3] (the HMcode-2020 calibration range). Grid step 0.1.
- **Feedback off:** S_fb ≡ 1 (the featureless comparison).
- Model power: P_X(k, z) = R_X(k) · S_fb(k, z; T) · P_NL(k, z), with R_ΛCDM ≡ 1.
- The recalled van Daalen+20 / OWLS / FLAMINGO forms are not used; the executed BAHAMAS-calibrated family replaces them (one family only: disclosed as a limitation).

## Effective A_mod (the data's own parametrisation P = P_L + A (P_NL − P_L))

- **M1 (PRIMARY mapping):** Limber convergence power C_ℓ for one source distribution per survey, n(z) ∝ z² exp[−(z/z0)^1.5] with mean z 0.67 (KiDS-1000) and 0.63 (DES Y3) (recalled, PROVISIONAL), ℓ = 100–2000 in 24 log bins. Weights: diagonal Gaussian variance with shape noise (KiDS: 1006 deg², n_eff 6.17 arcmin⁻², σ_e 0.265; DES: 4143 deg², n_eff 5.59 arcmin⁻², σ_e 0.261; recalled, PROVISIONAL), evaluated on the DMO model. A_eff is the weighted linear least-squares fit of C_model to C_L + A (C_NL − C_L). Each survey's A_eff uses its own n(z) and weights.
- **M2 (continuity with CFG526):** A_eq(k) = (P_model − P_L)/(P_NL − P_L) at z = 0.5, averaged over k = 1, 2, 4 h/Mpc.
- Z_d = (A_eff − A_mod,d) / σ_d for d = KiDS, DES; signed (positive = too much small-scale power).

## Verdict per footing (framework PRIMARY R) and for ΛCDM-dark-matter-only, mapping M1, full feedback range [7.3, 8.3]

Let Zmax(T) = max_d |Z_d(T)| (one feedback setting must serve both datasets).
- **EXCLUDED** by cosmic shear: Zmax(T) ≥ 3 for every T in [7.3, 8.3].
- **TENSION:** not EXCLUDED, and Zmax(T) ≥ 2 for every T in [7.3, 8.3].
- **CONSISTENT:** Zmax(T) < 2 for some T in [7.3, 8.3]; the README states whether such a T lies inside the fiducial [7.6, 8.0].
- **NOT DIAGNOSTIC:** the class changes under any declared mapping systematic: M2 in place of M1; ℓ_max = 1000 or 3000; n(z) mean ± 0.1 (both surveys shifted together).
- **VARIANT-SENSITIVE** (flag, framework only): a mainline variant gives a different class under M1.
- Also reported: the same classes with feedback off; per dataset, the T at which A_eff = A_mod (Z = 0) and the T range with |Z| < 2, searched over [7.0, 9.0] (outside [7.3, 8.3] flagged as outside calibration); S_fb(k = 1, z = 0.5) at those T; the framework's excess over ΛCDM in A_eff (ΔA = A_F − A_ΛCDM at the same T).
- **S8-equivalent (reported, not a verdict input):** S8 of a DMO ΛCDM with σ8 rescaled whose M1-weighted C_ℓ amplitude matches the model (feedback off and T = 7.8).

## Controls

- **C1:** CAMB σ8(z = 0) = 0.811 within 1e-3.
- **C2:** M1 fit of C_NL returns A = 1 and of C_L returns A = 0 (to 1e-9).
- **C3:** for ΛCDM, A_eff decreases monotonically with T over [7.3, 8.3].
- **C4:** R(k = 1e-3) = 1 within 1e-3 for every input R.

## MUTATE (`CFG590_MUTATE=1`, separate `_MUTATE` outputs; exit 1 = all bite)

- **MU1:** framework R ≡ 1 must reproduce ΛCDM's A_eff, Z and verdict exactly (|ΔA| = 0).
- **MU2:** feedback off must give ΛCDM A_eff = 1 (to 1e-9) and the framework's featureless value (equal to the feedback-off row of the main run).
- **MU3 (tooth):** R = 0.5 for k ≥ 1 (R = 1 below) must give A_eff below every dataset by Z ≤ −3 at T = 7.3 (sign handling).

## Outputs

`cfg590_shear.py` → `cfg590_shear.out`, `cfg590_results.json`; MUTATE → `cfg590_shear_MUTATE.out`, `cfg590_results_MUTATE.json`; `README.md`. Compute light: `nice -n 10`, ≤ 2 threads. All numbers quoted come from the JSON.

## Decisive data products (listed for the owner's go; not downloaded)

KiDS-1000 COSEBIs / ξ± data vector, covariance and n(z); DES Y3 cosmic-shear 2pt FITS with covariance and n(z); a likelihood code (CCL or CosmoSIS). Sizes are stated in the README.
