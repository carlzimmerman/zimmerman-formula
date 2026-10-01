# CFG262 stage 1 — the blind pre-flight: MUSE-DARK levels by baryon route in redshift thirds

> **κ = ½ FITTED. No g_perp, D, s\* or median a₀ of any third was formed from the real velocities (the run files were read only to count finite values). A forecast, not a measurement. No sentence says the data favour a law.**
> Criteria `FROZEN_CRITERIA.md` (**1c1e4fe44**) + `ADDENDUM_1.md` (before any script). Script `cfg262_musedark_zthirds.py` (`STAGE=A`); output `cfg262_stageA.out`, `cfg262_stageA_results.json`.

## Bottom line
1. **Estimator and plumbing validated: C1–C7 pass.** 882 / 882 run files and 9 / 9 catalogue files match their manifests; the chain is 126 / 124 / 14 / 110 / 109 with thirds 37 / 36 / 36; the route identity holds exactly (ρ ≡ 1); the imported estimator equals CFG223's bit for bit (200 random sets); the noiseless identity returns s_true to 1.7e-16 dex; the D1 reading is finite for all 109 galaxies; bootstrap coverage at N = 36 with 0.3 dex scatter on g_obs is **0.670 (68 %) and 0.943 (95 %)**.
2. **Baryon lever** d log₁₀ s\*/d(baryon dex), noiseless world, by third (z1 / z2 / z3): **route (i) −1.30 / −1.23 / −1.14** (y median 0.075 / 0.047 / 0.018); **route (ii) −1.65 / −1.90 / −2.45** (y median 0.29 / 0.49 / **1.00**); **route (iii) −1.42 / −1.50 / −1.73** (y median 0.14 / 0.19 / 0.35). Route (ii) in the highest third sits at y ≈ 1, where the lever grows and the Newtonian floor is near.
3. **No-root forecast (the impossibility proxy: route baryons within R_e above the model's mass):** route (i) 0.03 / 0.06 / 0.03; route (ii) 0.32 / 0.31 / **0.58**; route (iii) 0.19 / 0.14 / 0.28. By the frozen rule (≥ 0.50) only **route (ii), third 3, is NO ROOT LIKELY**; the other eight route-thirds are expected to have a root. (The earlier design-time print gave 0.33 for route (ii) z2 because it did not drop the one galaxy with a non-finite log M_dyn; the script's number is 0.31.)
4. **Precision forecast:** SD of log₁₀ s\* = **0.125 dex** for N = 36 at a 0.6 dex per-galaxy planning scatter.
5. **Calibration drifts on the thirds' relative level** d = log s\*(z3) − log s\*(z1), noiseless world at s = 1: **route (ii)** τ = +0.25 / −0.25 dex per unit z: **+0.23 / −0.26**; H₂ tilt t_H = +0.3 / −0.3: **−0.24 / +0.21**; **route (iii)** τ = ±0.25: **+0.21 / −0.23**. A z-dependent SED-mass bias at CFG236's declared plausibility ceiling moves the high-minus-low difference by about ±0.2–0.25 dex.
6. **FLAT versus H(z) from the thirds' levels: NOT POSSIBLE for all three routes.** The rival expects d = **+0.177** dex between the third medians (z 0.523 → 1.204); the thresholds 2√(2 SD² + drift²) are 0.354 (route (i), no SED drift), 0.621 (ii) and 0.577 (iii). Even with zero calibration drift the statistical forecast alone (2√2 × 0.125 = 0.354) exceeds the rival's shift.

## Decisions (the frozen map)
- **PF-D1 ESTIMATOR VALIDATED: True.** **PF-D2** root forecast as item 3. **PF-D3 DRAWABLE:** eight route-thirds; **(ii, z3) floor triangle** (its data may still produce a root; scored at stage B). **PF-D4: NOT POSSIBLE** for FLAT versus H(z) on every route.

## Hand estimates (frozen before any number; kept as they fall)
- **HE1 hit** (only route (ii) third 3 is NO ROOT LIKELY). **HE2 hit** (route (i) levers in [−1.6, −0.9]; routes (ii)/(iii) in [−4, −1]). **HE4 hit** (|τ-drift| of the difference 0.21–0.26 dex, in [0.2, 0.5]).
- **HE5 MISS:** I wrote POSSIBLE_SYS for route (i) "if its lever is near −1"; the arithmetic of the forecast alone (2√2 × 0.125 = 0.354 against +0.177) already says NOT POSSIBLE on every route, so the miss was foreseeable at the time of writing and is kept.
- HE3 (bootstrap SD 0.10–0.20 per third) and HE6–HE8 (levels, route contrast, M3) are scored at stage B.

## Disclosures
- The proxy fractions of §0.3 of the criteria were printed at design time; the script's A2 uses the same formula and drops the single galaxy with a non-finite log M_dyn.
- Stage A read the 109 run files (velocities in memory) only to count finite values; no velocity-derived quantity was formed.
- The planning scatter (0.6 dex per galaxy) is the record's (CFG199's lowest-third interval), not a blind number.
- C7 and the stage-A tables use the noiseless world on the velocity-free (R198-mode, thin-disc) baryon side for routes (ii) and (iii) and on the law-implied y for route (i); the stage-B baryon accelerations (R199 construction) differ by the velocity-dependent route-(i) factor and so the measured levers differ from these forecasts.
