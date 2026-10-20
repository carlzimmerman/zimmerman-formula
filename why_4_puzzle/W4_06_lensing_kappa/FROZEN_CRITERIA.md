# W4-06: is there a 4 in weak lensing? κ from KiDS isolated-galaxy lensing (frozen criteria, committed alone)

**Status: FROZEN 2026-10-20, before any W4-06 script exists or any fit is made.** Append-only after this commit. Rules:
`campaign_fresh_gravity/CFG894_kappa_campaign_ledger/KAPPA_CAMPAIGN_RULES.md`. This is an **observational lane (class
`obs`)**: a determination, not a derivation. **κ = ½ is FITTED.** Not theory closed.

## Why

"Why 4" presumes there is a 4. Every κ determination in the register comes from rotation curves or the BTFR. CFG493's
primary combines three M/L-insensitive gas routes and gives κ_Λ = 0.417 ± 0.095. The 10-20 audit of its error budget found
the per-galaxy scatter is set by rotation-curve reduction, plus an HI-flux tie, inclinations and distances. **No register row
measures κ from weak lensing**, which shares none of those systematics. Its own are stellar masses, photo-z and the
background distances.

CFG829 already found isolated blue (late-type) KiDS lenses on the law at the dwarfs' accelerations: A = 1.016 ± 0.086
relative to the canonical-footing law, so κ = ½ is assumed there. W4-06 frees κ and fits it.

## Data and code reused (read only)

- Brouwer et al. 2021 (B21) public KiDS-1000 RAR files on disk: `real_research/data/lensing_rar/brouwer2021_rar/`.
  - Colour-split isolated sample: `Fig-8_RAR-KiDS-isolated_Colorbin_1.txt` (blue, u−r < 2.5) with
    `Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt`.
- CFG829's loader (g_obs = 4G·ESD/bias, covariance block, the same unit constants) is copied unchanged into the W4-06 script.
- CFG840's stellar-mass and window variants and CFG885's native-background factor bracket T ∈ [0.968, 1.062] are read from
  their committed outputs.

## Model and estimator (fixed)

- Law: g_obs = g_bar ν(g_bar/a₀), with a₀ = κ s and s = c√(G ρ_DE).
- Kernels: **ν_simple** = ½(1 + √(1 + 4/y)) is primary (THEORY_CANONICAL 2026-10-14). ν_e = 1/(1 − e^{−√y}) is secondary,
  for report.
- Footings, never pooled:
  - ρ_DE = Ω_Λ ρ_crit (κ_Λ);
  - ρ_crit (κ_crit);
  - with ρ_crit = 8.533238720309458e-27 kg/m³ and Ω_Λ = 0.685 (GF1 registers). These are allowed only to convert a fitted a₀
    to κ.
- No footing a₀ value is an input; s is computed from G, c and ρ.
- Estimator: χ²(κ) = r^T C⁻¹ r with the full B21 covariance block, minimised on a fine log grid κ ∈ [0.05, 5] (4001 points).
  1σ is the Δχ² = 1 interval. This is a one-parameter fit, not a knob scan.

**Windows, all fixed by CFG829's frozen criteria, not chosen here:**
- **PRIMARY:** W = [10^−13.3, 10^−11.9] m/s² (CFG829's dwarf window, where A = 1.016).
- **SECONDARY:** WC = [10^−11.9, 10^−10.9] (CFG829's calibration window), and W ∪ WC.
- **REPORT:** every blue point.

## Declared systematics (each a separate refit; none is combined into a verdict by tuning)

- **S1 stellar mass:** g_bar × 10^{±0.2}, CFG840's lens M★ ± 0.2 dex.
- **S2 native background:** g_obs × T, with T = 0.968 and 1.062 (CFG885's full bracket).
- **S3 window:** the PRIMARY window shifted by ±0.3 dex (CFG840).
- The systematic envelope is the min and max of the S1–S3 best fits, reported beside the statistical 1σ.

## Hand expectation (disclosed before the fit)

- Deep regime: g_obs ∝ √(a₀ g_bar), so κ ≈ ½A² ≈ 0.52 with statistical σ ≈ 0.09 on the canonical footing, ν_simple.
- S1 spans roughly κ 0.41–0.86 (A from 0.90 to 1.31), so the stellar mass dominates.
- Expected class: **CONSISTENT with CFG493 and with ½, NOT DECISIVE.**

## Grading (frozen)

- **Agreement with CFG493:** z = (κ_lens − 0.417)/√(σ_lens² + 0.095²) on ρ_DE, and likewise with 0.345 ± 0.078 on ρ_crit.
  - |z| ≤ 2: CONSISTENT.
  - 2 < |z| ≤ 3: TENSION.
  - |z| > 3: DISAGREE.
  - Each is reported for the statistical σ alone and for σ including the S1 envelope half-width.
- **The ½ versus 0.461 question:** Δχ² = χ²(0.461) − χ²(0.5) on the PRIMARY.
  - |Δχ²| < 1: NOT SEPARATED.
  - |Δχ²| ≥ 9: SEPARATED.
- **Lane verdict:**
  - **DECISIVE:** total σ(κ) ≤ 2.8% of κ.
  - **CONSISTENT, NOT DECISIVE:** |z| ≤ 2, total σ above 2.8%.
  - **TENSION / DISAGREE:** by z.
  - **NOT DIAGNOSTIC:** fewer than 3 PRIMARY points, or a χ² minimum at a grid edge.

## Checks

- **K1:** reproduce CFG829's PRIMARY amplitude A = 1.016 ± 0.086 (canonical, ν_e, blue) with the copied loader, to 1e-3.
- **K2, mock recovery:** inject κ_true = 0.30 and 0.50 through the law, with Gaussian noise from the covariance (50 mocks
  each, seed 101). The median recovered κ must lie within 1σ_stat of the truth.
- **K3:** the χ² minimum is not at a grid edge, and Δχ² = 1 brackets exist.
- **K4:** in the deep limit, compare the fitted κ with ½A² from K1's amplitude; report the difference, it is not graded.
- **I1:** no footing a₀ value or measured κ upstream of the fit. CFG493's numbers appear only in grading.

## Mutation control (`W4_06_MUTATE=1`, separate `_MUTATE` outputs, exit 1 when it bites)

- **M1:** g_obs × 1.21. Expected: κ rises by about 1.21² ≈ 1.46 (deep regime). The check that κ is within 1% of the normal
  run's must FAIL, and the shift ratio is reported.
- **M2:** with κ_true = 0.30 injected, K2 must still pass (the estimator, not the data, is tested).

## Register

One `obs`-class row (family OB) with κ_Λ and κ_crit and their errors, then `kappa_campaign_lee.py` rerun. Nothing downloaded.
B21 files are read only.
