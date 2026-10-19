# CFG826 FROZEN CRITERIA: does CFG824's age trend, carried to the oldest systems, predict the ultra-faint dwarfs? (before any script)

**Why.** CFG824 found a positive (not significant after the M/L control) trend of the excess over the law with quenching age
in 28 out-of-sample dwarfs. The ultra-faint MW dwarfs (UFDs) are uniformly ancient and carry the theory's open +0.33 dex
excess. If H-FOSSIL is one mechanism, the CFG824 line extrapolated to UFD ages should land on the UFDs. Free cross-check.

## Inputs
- **The trend:** weighted line E = a + b τ90 refit from `CFG824_dwarf_age_fossil/cfg824_results.json` out-of-sample rows,
  weights 1/[(e_σ/σ)² + 0.075²] (exactly CFG824's), primary (Υ = 2) and C-ML (Υ_V ∝ τ50^0.7). Residual RMS s_res of those rows
  about the line is the per-galaxy intrinsic scatter.
- **UFD ages:** τ90 = 12.5 Gyr, τ50 = 12.6 Gyr for every UFD (declared: UFDs formed ≥ 80% of their stars before z ≈ 6;
  no Weisz+14 value exists for the UFDs used below).
- **UFD sample, primary (binary-corrected):** the Arroyo-Polonio+2026 table (`real_research/data/arroyopolonio2026_ufd_binary_corrected.tsv`),
  σ = sig_f (flat binary-fraction prior), error = mean of its ±1σ; M_V and r_h from LVD `lvd_dwarf_mw.csv` by name.
  Dropped if no LVD row, and dropped if already used by CFG821/824 (Leo IV, Crater II are not independent).
- **UFD sample, secondary (literature σ):** every LVD MW dwarf with M_V > −7.7, σ_obs and r_h, minus CFG821/824 members.
- σ_law: CFG821's isolated law, canonical a0 (alt reported), Υ_V = 2 (primary) / C-ML Υ_V(τ50 = 12.6) = 2.35.

## Statistic and classes (primary sample, primary trend)
- Observed mean Ē_UFD with standard error SD/√N. Predicted Ē_pred = a + b × 12.5 with error √(var_fit + s_res²/N).
- z = (Ē_UFD − Ē_pred) / √(se_obs² + se_pred²).
- **CONSISTENT** if |z| < 2; **UFDs ABOVE TREND** if z ≥ 2; **UFDs BELOW TREND** if z ≤ −2. **NOT DIAGNOSTIC** if N < 4.
- Also report the flat (no-age) alternative E = weighted mean of the CFG824 out-of-sample rows, and z against it.
  A useful discrimination needs the trend CONSISTENT and the flat alternative at |z| ≥ 2.

## Controls
- K1: the refit slope equals CFG824's stored slope to 1e-6.
- MUTATE (separate output): set b = 0 (no trend) → the prediction must equal the flat alternative.

κ = ½ fitted; cold energy mass required; not theory closed. A CONSISTENT is a cross-check, not support (CFG824 was NO SIGNAL).
