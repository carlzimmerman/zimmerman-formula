# CFG859 FROZEN CRITERIA: does CFG856's extra isothermal speed survive the ultra-faint dwarfs? (independent test; before any script)

**ID note:** last ID of the owner-chat block 850–859.

**Why.** CFG856's extra component (g = g_law + V_x²/r, V_x0 = 9.42 km/s calibrated on MW classical dSphs) passes SPARC out of sample.
The ultra-faint dwarfs (UFDs) were never used to calibrate it and probe r_1/2 ≈ 20–100 pc. An UNCORED component adds V_x²/3 to σ²
(Wolf estimator), i.e. σ ≥ 5.4 km/s for every dwarf.

## Prediction and data
- σ_pred² = σ_law² + V_x0²/3 with σ_law the law's Wolf dispersion from the stars (Υ_V = 2.20 for a 13.3-Gyr burst, CFG827's UFD value;
  r_1/2 = 4/3 r_h; canonical a0, ν_e; alt reported with its own V_x0 = 9.24 km/s).
- **Primary:** binary-corrected UFDs (Arroyo-Polonio+26 sig_f; the 7 with LVD M_V and r_h used in CFG826).
- **Secondary:** every LVD MW dwarf with M_V > −7.7, σ_obs and r_h, minus CFG821/824/826 members (literature σ).
- Statistic: mean E = ln(σ_obs/σ_pred) with standard error SD/√N; also the law alone (V_x = 0).

## Classes (primary)
- **SURVIVES UFDs** if |E| < 2 SE.
- **OVER-PREDICTS UFDs (needs a core)** if E ≤ −2 SE (UFDs are colder than the uncored component allows).
- **UNDER-PREDICTS** if E ≥ +2 SE.
- If OVER-PREDICTS: report, post-hoc and not a verdict, the core radius r_c for an extra component M_x(<r) = V_x0² r³/[G (r² + r_c²)]
  (cored isothermal) that brings E to 0 on the primary sample.

## Controls
- K1: V_x = 0 reproduces CFG826's binary-corrected UFD excess over the law (E ≈ +0.70 at Υ 2; here Υ 2.20). MUTATE (separate output):
  V_x0 × 0.3 → E must move toward the law-only value.

κ = ½ fitted; cold energy mass required; not theory closed.
