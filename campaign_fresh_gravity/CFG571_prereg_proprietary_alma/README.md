# CFG571: pre-registered predictions for three unreleased ALMA data sets

Criteria 5f68a68c3 (committed alone, first). Run: `python3 cfg571_prereg.py` (and `--mutate`). **Committed before any of the data are public.** `PREDICTIONS_HASH.txt` holds the SHA-256 of the results JSON. Never edit these files after release; any change goes in a new, dated file.

The quantity predicted is how much baryonic mass, and so how much **gas**, each disc must have for its measured rotation to come out right under each model:
- the framework with a0 ∝ √ρ_DE (F-DESI; a0 ratio 0.94 / 0.92 / 0.87 at z 1.4 / 1.6 / 2.0);
- the framework with constant a0 (F-flat);
- a0 ∝ H(z) (R-H; 2.24 / 2.49 / 3.03);
- the ΛCDM+feedback RAR-equivalent scale (L-fb; 1.85 / 2.17 / 2.82; CFG565, with CFG566's caveat).

"FLOOR" means the stars alone already exceed what the model allows, so any detected gas counts against that model.

## The crispest prediction: GS4_24110 (z 1.997; [CI] + dust at 0.09″, public 2026-11-28)
| model | required log M_gas (total, R_g = R_d / 1.5R_d) |
|---|---|
| F-DESI | 9.8 / 10.1 (M* 10.89, canon), 10.4 / 10.7 (M* 10.76, canon); 9.1 / 9.4 at M* 10.89 on the alt footing |
| F-flat | 9.5 / 9.7 (canon, M* 10.89); **FLOOR** at alt footing + M* 10.89 |
| R-H | **FLOOR in every branch** |
| L-fb | **FLOOR in every branch** |

So the sign is clean:
- If the ALMA data find gas of ~10^10 M☉ or more inside R_e, both rivals' RAR-scales would need less baryons than the stars alone provide.
- If the gas is negligible, the framework's F-DESI branch is in trouble.

Caveats:
- It's one disc, so it's a demonstration and nothing is excluded (criteria).
- The stellar-mass branch moves the framework's number by 0.6 dex.
- ΛCDM itself has no gas prediction here (RC100's own halo fit puts baryons at 10^10.51 within R_e).

## U4_27928 (z 1.419; CO 0.07″, public 2026-11-06): conditional on the CO rotation speed at 2R_e = 8.3 kpc
- Below V_c ≈ 200 km/s, every model is FLOOR: the disc is star-dominated and tests nothing.
- At V_c 225, the framework needs log M_gas ≈ 9.2–9.8 and both rivals are FLOOR.
- At 250–300, all models need gas, and the framework needs 0.2–0.9 dex more than R-H.

## KURVS CO survey (2026.1.00363.S, ~1.6″, not yet observed): the sample test
- **The primary sample** is 7 discs with v/σ0 ≥ 1.5.
- **Forecast separation, F-DESI vs R-H:**
  - 0.19–0.21 dex (Burkert pressure branch);
  - 0.30–0.31 dex (no-pressure branch, where R-H is FLOOR in 6 of 7 discs).
- **Forecast significance:** about **1.0–1.6σ** with the 0.15 dex systematic floor. The KURVS gas masses alone can't decide it, but they would lean.
- F-DESI vs F-flat is ≤ 0.02 dex and can't be separated.
- **The pressure branch dominates.** The Burkert correction at R ≈ 3–5 R_d doubles some speeds (KURVS-15: 112 → 224 km/s). The two branches are never pooled; how to treat pressure support is the biggest open input.

## Controls
- C1 DESI ratio 0.874 at z 2: PASS.
- C2 KURVS-15 inputs: PASS.
- C3 Freeman peak 0.3870 at 2.150 R_d: PASS.
- C4 Newtonian round trip: PASS.
- MUTATE (ν ≡ 1): the separation collapses, so it is detected (exit 1).

κ = ½ fitted; the cold mass is still required. These are predictions, not results.
