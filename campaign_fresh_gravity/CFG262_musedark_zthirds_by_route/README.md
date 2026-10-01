# CFG262 — MUSE-DARK implied-a₀ levels in redshift thirds, by baryon route (z ≈ 0.52, 0.88, 1.20): the level depends on the route by up to a factor 13

> **κ = ½ FITTED. a₀(z) FLAT is the framework's distinctive law, a₀ ∝ H(z) the rival, ΛCDM has no a₀ (PROXY = CFG223's effective-a₀ curve). Every input is a model output of one GalPaK3D/DC14 analysis per galaxy plus an SED mass (CFG236 §7): these levels cannot tell a z-dependent a₀ from a z-dependent prior, pressure term, inclination or decomposition. No sentence says the data favour a law; a lean is not a detection.**
> Hashes: criteria **1c1e4fe44** · addendum 1 **5902b0c5e** (both before any script) · stage A pre-flight **3a15dad9e** · addendum 2 + measurement script + SELFTEST **1b495dd3c** (before any real level) · measurement, MUTATE and this README: the commit that carries this file. Data on disk only (the CFG236 chain, S = 109 galaxies, and the 126 external `true_Vrot.dat` files, 882 / 882 hashes verified); nothing fetched.

## Bottom line
1. **Reading bD** (projected velocity plus the asymmetric-drift term, the reading CFG236 found best supported; the headline row set). s\* is the implied a₀ scale relative to the canonical 9.3603e-11 (a₀ = s\* × 0.936e-10); thirds of S by z, N = 37 / 36 / 36:

| route | z = 0.523 | z = 0.878 | z = 1.204 | third-3 minus third-1 (log₁₀) |
|---|---|---|---|---|
| **(i) fitted DC14 masses** (the model's own decomposition) | **1.22** (95 %: 0.86–1.94) | **3.05** (1.61–3.76) | **4.53** (3.79–5.47) | **+0.570 ± 0.094** |
| **(ii) SED M\* + H₂** | **0.46** (0.31–1.61) | **1.02** (0.75–1.36) | **0.36** (0.03–0.75; 12 of 36 galaxies have D < 1) | −0.115 ± 0.489 |
| **(iii) SED M\*, no H₂** | **1.58** (1.17–3.37) | **3.32** (1.95–4.91) | **1.71** (1.13–2.94) | +0.036 ± 0.138 |

   The H(z) rival expects +0.177 dex between the first and third thirds; FLAT expects 0. **The three routes disagree about the same galaxies by up to a factor 13 at z ≈ 1.2** (route (i) 4.53 against route (ii) 0.36).
2. **Route (i) rises with redshift, and the routes with an independent SED stellar mass do not.** This is CFG198/199/236's result in levels: the rise travels with the DC14-fitted masses (the baryon fraction of route (i) is an output of the same fit that produced the velocity), not with the measured SED mass. Nothing here shows which mass is right (CFG236). Route (i) at the highest third is outside the ±0.30 dex band for FLAT and PROXY (flags `nnn`) and inside it for H(z) (`nnY`); route (ii) at the highest third is outside every band for every law (`nnn`) because its level is low and its error large.
3. **No-pressure lower bound (reading b):** route (i) 0.68 / 1.63 / 2.60; route (ii) 0.33 / 0.59 / 0.16; route (iii) 1.05 / 1.97 / 0.72. The pressure term raises every level by 0.15–0.38 dex (route (i) by 0.24–0.27). The lowest-third route (i) values reproduce the record (control M3 below).
4. **The calibration budget is route-specific.** Baryon lever d log₁₀ s\*/d(baryon dex): route (i) −1.16…−1.30, route (ii) −1.49…−1.72, route (iii) −1.16…−1.34 (bD); ±0.15 dex baryons is therefore ±0.17…±0.26 dex in s\*. **The frozen recipe half-width of route (ii) is 0.74–0.93 dex, dominated by one knob — the natural-log reading of the μ_mol formula (−0.37…−0.71 dex);** without it 0.41–0.79. A z-dependent SED-mass bias τ = ±0.25 dex per unit z moves route (ii)'s highest-third level by +0.09 / −0.16 and route (iii)'s by +0.09 / −0.12.
5. **FLAT versus H(z) from the thirds' levels was NOT POSSIBLE before the measurement** (stage A: threshold 0.35–0.62 dex against +0.177) and no sentence here changes that: route (i)'s rise (+0.57 ± 0.09) is a statement about the route, and the other two routes do not rise.

## Row details (reading bD; reading b is in the CSV and the output)
| row | N | s\* | 68 % | ±0.15 dex M\* band | ±0.30 dex band | recipe ± dex (no natlog) | median D | D<1 | flags FLAT / H(z) / PROXY |
|---|---|---|---|---|---|---|---|---|---|
| z1 route i | 37 | 1.220 | 1.07–1.58 | 0.76–1.92 | 0.43–2.81 | 0.09 | 4.17 | 0 | YYY / YYY / YYY |
| z2 route i | 36 | 3.046 | 2.61–3.37 | 1.81–4.65 | 0.97–6.99 | 0.08 | 5.13 | 0 | nnY / YYY / nnY |
| z3 route i | 36 | 4.534 | 4.10–4.89 | 2.98–6.78 | 1.96–9.92 | 0.06 | 8.01 | 0 | nnn / nnY / nnn |
| z1 route ii | 37 | 0.464 | 0.40–1.38 | 0.26–1.11 | 0.12–1.81 | 0.93 (0.60) | 2.91 | 6 | YYY / YYY / YYY |
| z2 route ii | 36 | 1.017 | 0.93–1.10 | 0.56–1.69 | 0.23–2.58 | 0.74 (0.41) | 2.57 | 4 | YYY / nYY / YYY |
| z3 route ii | 36 | 0.356 | 0.14–0.46 | 0.14–0.58 | 0.001–0.97 | 0.87 (0.79) | 1.70 | 12 | nnn / nnn / nnn |
| z1 route iii | 37 | 1.579 | 1.40–2.04 | 1.01–2.41 | 0.61–3.60 | 0.11 | 5.92 | 3 | nnY / YYY / nYY |
| z2 route iii | 36 | 3.317 | 2.71–4.23 | 2.02–4.91 | 1.21–7.17 | 0.09 | 6.19 | 3 | nnn / nnY / nnn |
| z3 route iii | 36 | 1.715 | 1.43–1.92 | 1.07–2.67 | 0.58–3.88 | 0.19 | 3.97 | 3 | nnY / YYY / YYY |

- **The route contrast** (log₁₀ s\*(route) − log₁₀ s\*(i), reading bD): route (ii) **−0.42 / −0.48 / −1.11** (factors 2.6, 3.0, 12.8 below route (i)); route (iii) +0.11 / +0.04 / −0.42.
- **Sensitivity rows** (reading a, v_perp = v_f; never drawn): route (i) 0.44 / 0.98 / 1.68; route (ii) 0.22 / 0.31 / 0.10; route (iii) 0.66 / 1.26 / 0.53; with the drift (aD) route (i) 0.92 / 2.32 / 3.45; route (ii) 0.42 / 0.83 / 0.28; route (iii) 1.28 / 2.61 / 1.49.
- **Historical estimator** (the CFG199/236 level: median log₁₀ a₀,i over the rows with D > 1.05, kernel RAR) is in the output and the CSV beside the headline; it differs from s\* by up to +0.48 (route (ii), third 1) because it drops the censored rows.

## Controls and MUTATE (nothing hidden)
- **Stage A (3a15dad9e): C1–C7 pass** (882 / 882 run files, chain 109, route identity exact, estimator bit-equal to CFG223, noiseless identity 1.7e-16, coverage 0.670 / 0.943).
- **Stage B: M1 passes** (alt footing, same absolute a₀ to 1e-16); **M3 passes to 0.004 dex: the historical estimator on route (i) reproduces the record's lowest-third levels** (a −10.376 vs −10.38; b −10.143 vs −10.14; aD −10.054 vs −10.05; bD −9.932 vs −9.93); M4 (header) and M5 (the thirds partition the 109 galaxies) pass. **M2 MUTATE=1 passes: the planted law at s = 2 moves every row by +0.277 … +0.334 dex (planted +0.301; tolerance ±0.05).**
- **SELFTEST** (1b495dd3c): fabricated g_perp on route (iii) returned the truth inside the 95 % interval in all six route-(iii) rows.

## Hand estimates (frozen before any number; kept as they fall)
- **Stage A:** HE1 (the forecast rule), HE2, HE4 hit; **HE5 missed** (foreseeable arithmetic; PREFLIGHT_RESULTS.md).
- **Stage B:**
  - **HE1, the outcome clause, misses:** the forecast "route (ii) third 3 is NO ROOT LIKELY" (proxy 0.58) did not materialise; the row has a root (median D 1.70; 12 of 36 galaxies have D < 1, 33 % against the proxy's 58 %), at a low level with a wide interval (SD 0.43 dex, 2 % of resamples unbounded). The proxy over-forecast the Newtonian-floor failures.
  - **HE3 mostly misses:** the bootstrap SD of log₁₀ s\* ranges 0.044–0.48 dex (route (i) 0.04–0.09 in bD, route (ii) 0.08–0.43); 9 of 18 rows lie in the frozen 0.10–0.20.
  - **HE6:** route (i) reading bD third 1 **1.22 hits** (frozen ≈ 1.2); reading b third 1 is 0.68 against ≈ 0.77 (−0.05 dex; the 0.77 came from the historical level); route (i) third-3 minus third-1 **+0.57 / +0.58 misses high** (frozen 0.2–0.5); route (ii) in the range 0.3–2 with no clear rise **hits in bD** (0.46 / 1.02 / 0.36) and misses at z3 in reading b (0.16); **route (iii) between (i) and (ii) misses** (above route (i) at z1 and z2 in bD).
  - **HE7 hits:** s\*(i) exceeds s\*(ii) in every third and reading, and the contrast widens with z (−0.42, −0.48, −1.11 in bD). **HE8 hits** (coverage; M1–M5; M3 to 0.004).

## Disclosures
- The impossibility proxy and the CFG236/CFG199 numbers were read before the freeze (criteria §0); the levels of thirds 2 and 3 and of routes (ii)/(iii) in the R199 construction were not in the record.
- **Addendum 2 (before the measurement):** the frozen recipe half-width keeps the natural-log μ_mol knob (CFG236's sensitivity); a second half-width without it is reported beside it, and reading (a)/(aD) sensitivity rows are added. Neither changes a frozen decision.
- One run, no re-run to change a result. The historical estimator and the kernel P2 are knobs, not alternatives to the headline.
- **A level here is not a measurement of a₀ at z ≈ 0.5–1.2.** g_obs and g_bar of route (i) and the velocities are outputs of one model fit; the SED mass is the only measured baryon quantity and it is itself an SED-fit output; nothing in the repo shows which mass is right (CFG236). A low or no-root row is a statement about the baryon model against the dynamics, not about the law.

## Files
`FROZEN_CRITERIA.md`, `ADDENDUM_1.md`, `ADDENDUM_2.md`, `PREFLIGHT_RESULTS.md`, `cfg262_musedark_zthirds.py`; `cfg262_stageA.out` / `_results.json`, `cfg262_stageB.out` / `_results.json`, **`cfg262_points_stageB.csv`** (chart shape; 18 rows: 3 thirds × 3 routes × readings b and bD), `cfg262_stageB_MUTATE1.*`, `cfg262_stageB_SELFTEST*.*`, `cfg262_points_stageB_MUTATE1.csv`. Run: `STAGE=A python3 cfg262_musedark_zthirds.py`, then `STAGE=B` (and `STAGE=B MUTATE=1`); about 1 minute each; needs the external `_external_data/muse_dark/numeric/` beside the repo.
