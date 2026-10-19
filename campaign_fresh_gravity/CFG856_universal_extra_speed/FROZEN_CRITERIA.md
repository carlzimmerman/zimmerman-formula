# CFG856 FROZEN CRITERIA: a universal extra circular speed V_x on top of the law? (calibrate on MW dSphs, test on SPARC dwarfs; before any script)

**Origin (post-hoc, disclosed):** CFG854's simplest Pareto formula in both blind splits was M_extra(<r_1/2) ∝ r_1/2, i.e. a constant
extra circular speed V_x ≈ 10 km/s. CFG854 used MW and M31 dwarfs, so the dSph samples are NOT independent of the idea. **The genuine
out-of-sample test is SPARC (P3), which no dwarf-excess lane has used to motivate this form.**

## Model
g_obs = g_law(g_bar) + V_x²/r (an isothermal extra component of fixed amplitude; canonical a0, ν_e; alt reported).

## Calibration
V_x0 = geometric mean of V_x = √(g_law (10^Δ − 1) r_1/2) over the MW satellites with Δ > 0.05 (CFG828 rows, Υ_SFH); its 1σ from the
scatter of log V_x over √N.

## Tests
- **P3 (primary, out of sample): SPARC small dwarfs** (Q ≤ 2, Inc ≥ 30°, M_b ≤ 3e9 M_⊙ as CFG845, points with errV/V < 0.10):
  Δ_pred(r) = log10[(g_law + V_x0²/r)/g_law]; D = mean over galaxies of median(Δ_obs − Δ_pred); bootstrap σ (2000, seed 856).
  PASS if |D| < 0.05 dex AND |D| ≤ 2σ_D. (For comparison the law alone gives D0 = mean Δ_obs.)
- **P1: M31 satellites:** mean log V_x within 2σ of the MW calibration (σ from both samples' scatter/√N).
- **P2: universality:** slope of log V_x on log M★ over all dwarfs with an excess, |slope| < 0.15 per dex OR within 2σ of 0.
- **P4 (reported): field dwarfs** (Cetus, Tucana, Aquarius, Phoenix, Leo T) mean log V_x vs MW.
## Classes
- **UNIVERSAL V_x SUPPORTED** if P3 AND P1 AND P2 pass.
- **SPARC-COMPATIBLE ONLY** if P3 passes but P1 or P2 fails.
- **EXCLUDED BY SPARC** if P3 fails with D ≤ −0.05 dex at ≥ 3σ (over-predicts the rotating dwarfs). **OTHER** otherwise.

## Controls
- K1: V_x0 = 0 reproduces CFG845's law-only SPARC residual (+0.032). MUTATE (separate output): V_x0 × 3 → must EXCLUDE BY SPARC.

κ = ½ fitted; cold energy mass required; not theory closed. A SUPPORTED is an empirical law needing a mechanism.
