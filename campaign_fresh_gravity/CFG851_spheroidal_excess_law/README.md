# CFG851 — one excess law for spheroidal systems? (calibrate on red lenses, predict the dSphs blind)

Criteria: `FROZEN_CRITERIA.md` (a6a62743f, before the script). Run: `python3 cfg851.py` (MUTATE `CFG851_MUTATE=1`). Seconds.

## Result — CLASS (canonical, M★-corrected red calibration): **DSPHS ABOVE** (no single law; the dwarfs carry ~3× more)
| calibration | b (per dex) | log10 g† | χ² (15 pts) vs law alone | dSphs predicted | dSphs observed | z |
|---|---|---|---|---|---|---|
| **red, M★ +0.123 (primary)** | **0.060 (0.050–0.070)** | **−10.05** | **16.1 vs 157.9** | +0.147 ± 0.025 | +0.438 ± 0.061 | +4.4 |
| red, uncorrected | 0.058 (0.050–0.065) | −9.01 | 15.8 vs 233.2 | +0.204 ± 0.026 | +0.438 ± 0.061 | +3.5 |
| alt, M★ +0.123 | 0.059 | −10.67 | 15.9 vs 115.0 | +0.108 | +0.398 | +4.5 |

- **A clean empirical law for red (early-type) isolated lenses:** g_obs = g_law(g_bar) · (g†/g_bar)^b with b = 0.060 ± 0.010 —
  a slow, steady excess growing ~0.06 dex per decade below g†. It brings χ² from 158 to 16 on 15 points (two fitted parameters;
  a description, not a prediction). Blue lenses: b unconstrained, consistent with 0.
- **Onset near a0, canonical only (flagged, not claimed):** with the CFG667-corrected masses on the canonical footing,
  g† = 10^−10.05 = 0.89e-10 m/s² ≈ a0 (0.94e-10). On the alt footing g† = 2.1e-11 ≠ its a0, and uncorrected masses give 1e-9. So this
  is footing- and mass-dependent; a coincidence to test, not a result.
- **The miss:** extrapolated to the dSphs' g_bar the lens law gives +0.15 dex; the satellite dSphs show +0.44 (4.4σ above). Lenses
  and dwarfs do not share one excess curve; the dwarfs' excess is ~3× larger in dex than the spheroidal-lens trend implies.
- MUTATE (calibrate on blue): b unconstrained → classed NOT DIAGNOSTIC rather than the expected DSPHS ABOVE (disclosed); the disc
  calibration predicts 0 and misses the dwarfs at z +7.2, as intended.

κ = ½ fitted; cold energy mass required; not theory closed.
