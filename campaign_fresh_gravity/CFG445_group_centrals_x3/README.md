# CFG445: group centrals x3. Do centrals of log M_h >= 12.5 groups sit above the RAR at g_bar < 10^-10.5, against luminosity-matched field controls?

## Verdict: NON-DISCRIMINATING on both footings, and UNDERPOWERED by design (stated before scoring). The 3x goal was NOT reached: 25 centrals (1.7x CFG393), 18 with a same-source field control.

One frozen load-bearing control (C-thin) FAILED, so the main run exits 1 (see Controls).

| statistic (frozen) | canonical a0 = 9.3603e-11 | alt a0 = 1.1312e-10 |
|---|---|---|
| N centrals GC (SPARC + WALLABY) / with a control within 0.2 dex / field F | 25 (15 + 10) / 18 / 123 | same |
| primary Delta_LM (central minus median of same-source field within 0.2 dex in log L) | +0.003 +- 0.064 (S +0.05) | +0.004 +- 0.064 (S +0.07) |
| per source: SPARC / WALLABY Delta_LM | -0.028 / +0.082 | -0.027 / +0.083 |
| secondary, unmatched pooled Delta (CFG393 style) | +0.031 | +0.032 |
| dBIC(linear - step), > 2 favours the step | -3.30 (slope preferred) | -3.52 |
| C5 within-source permutation p for abs(Delta_LM) | 0.94 | 0.92 |
| verdict | NON-DISCRIMINATING | NON-DISCRIMINATING |

Plain reading:
- Centrals of group-mass hosts do not sit measurably above luminosity-matched field galaxies of the same source: Delta_LM is
  zero to 0.004 dex with a 0.064 dex error. Not NOT SUPPORTED either: Delta + 2 sigma = 0.13 dex, above the 0.05 threshold.
- The step model loses to a smooth trend in host mass (dBIC about -3.3 to -3.5). This weakly disfavours a STEP at 12.5 in this
  sample. It is not a detection of a slope (slope +0.033 dex per dex of host mass, not tested for significance).
- WALLABY's centrals alone sit +0.08 above their matched field (S about 1). SPARC's sit -0.03 below. Both are within one sigma.
- Power, fixed before any real residual was computed (`cfg445_power_dryrun.out`, commit 852a66b3c): a real +0.10 dex step gives
  SUPPORTED in only 4.7% of mocks. The bottleneck is not the centrals, it is the few LUMINOUS FIELD galaxies that can serve as
  controls: only 10 of 15 SPARC centrals and 8 of 10 WALLABY centrals have any same-source field galaxy within 0.2 dex,
  and those controls are few, so each central's control median is noisy. Doubling only the centrals barely helps
  (power 0.10 at x2, 0.15 at x6). 80% power needs a 0.30 dex step at the current N.
- MUTATE shows the same thing on real residuals: +0.1 dex into every central moves Delta_LM by exactly +0.100 (to +0.103) and gives
  S 1.6 and dBIC +0.5 to +0.7, so it is NOT detected. The run exits 1 for that reason and because C3 fails by design.
  The within-source permutation p does drop to 0.01 under MUTATE, so the frozen bootstrap sigma is the conservative of the two.

Nothing here favours the framework over LCDM or the reverse. The cold-fluid mass is still required in groups and clusters
whatever this shows. kappa = 1/2 is fitted.

## What it would take (power; mock-only, no verdict weight)
`cfg445_power_posthoc.py` (a disclosed post-hoc extension, committed 750e341d9 before scoring) resamples centrals AND field
galaxies together: power at +0.10 dex = 0.06 (x1), 0.10 (x2), 0.24 (x3), 0.35 (x4), 0.61 (x6). Roughly 80% needs ~9-10x the
present sample, about 250 centrals with 1,200 field galaxies under the same matching. No public release does this today:
- BIG-SPARC (Haubner, Lelli, Di Teodoro et al.; ~4,000 galaxies with homogeneous HI curves + WISE mass models, >20x SPARC) is
  announced but not released. It is the release that would reach the power. At SPARC's rate (15 of 175) it would give roughly 300 centrals.
- WALLABY full-survey kinematic releases (beyond the pilot's 236 models) would add more, but WALLABY's pilot yield was low:
  10 usable centrals from 236 models (72 had no 2MASS XSC counterpart, 36 had no group-catalogue match).

## What was done
- Frozen criteria: `FROZEN_CRITERIA.md`, committed alone first (a1a2a05ac).
- Data (`FETCH_LOG.md`; fetched by `cfg445_fetch.py`): WALLABY pilot DR2 kinematic catalogue (contains all DR1 galaxies; 236 unique)
  and source catalogue from the CADC youcat TAP; 2MASS XSC cones (VizieR VII/233) around each WALLABY galaxy. The KT2017/T15 group
  catalogues and CFG393's SPARC match table were reused read-only.
- WALLABY baryons: thin-disc HI (1.33 x face-on SD, ring sum) + one exponential stellar disc from XSC K.ext and Kr.eff with
  Upsilon_K 0.6. Distances from the matched catalogue.
- Selection: `cfg445_selection.csv`. Residuals: `cfg445_residuals.csv` (canonical). Scoring: `cfg445_score.py` writes `.out` and
  `_results.json`; MUTATE writes `_MUTATE.out` / `_results_MUTATE.json`.
- WALLABY attrition (of 236): QFlag > 1: 5; inclination < 30: 17; no XSC: 72; unmatched in KT2017/T15: 36; ambiguous: 1; no
  distance: 13; fewer than 3 rings at g_bar < 10^-10.5: 25. That leaves 67 (10 GC, 25 SAT, 32 F).

## Controls (kept as they fell)
- **C-thin FAIL (load-bearing):** the ring-sum force with the frozen 0.1 kpc vertical softening is 2.3% low at 2 R_d on the
  declared test disc (R_d 3 kpc), against the 2% tolerance (within 1.7% from about 2.7 R_d out). With 0.01 kpc softening the error is
  0.3%. It does not matter for the result: the POSTHOC softening-0.01 sensitivity gives Delta_LM +0.0030 (identical) and dBIC -3.28.
  The run still exits 1, as frozen. (I saw this failure in a pre-run check of the code, before any residual existed. I kept the
  frozen softening rather than retune it.)
- C1 PASS (175 / 163). C-SPARC PASS (15 GC / 91 F, identical to CFG393). C-HI PASS: WALLABY SD profiles integrate to the source
  catalogue's HI masses within 0.021 dex (median), N 67. C3 PASS (identity, 0 difference); MUTATE breaks it by design.

## Departures after freezing (disclosed)
1. Distance fallback: the frozen text "KT2017 table3 Dist, else T15 table5 Dist" was implemented as: if the KT2017 galaxy row
   has no distance, use the T15 galaxy distance of an unambiguous T15 positional match. 19 galaxies recovered, 13 remain excluded.
2. Dry-run speed: 300 bootstraps per mock (the frozen primary uses 5,000). The scan used 200 mocks x 200 bootstraps.
3. POST-HOC power scaling (centrals and field together), described above. Mock only.
4. POST-HOC sensitivities: softening 0.01 kpc; KT2017 group distance (table2) instead of galaxy distance. No verdict weight.
5. The numpy/Accelerate matmul printed spurious floating-point warnings in the post-hoc run (as in CFG393). Results are unaffected.

## Sensitivities (reported, canonical; alt within 0.003 dex)
| variant | GC (used) / F | Delta_LM | dBIC |
|---|---|---|---|
| Upsilon_K 0.45 | 26 (19) / 125 | -0.016 +- 0.059 | -3.76 |
| Upsilon_K 0.80 | 24 (18) / 119 | +0.007 +- 0.063 | -2.96 |
| threshold 12.3 | 37 (22) / 109 | -0.020 +- 0.067 | -2.87 |
| threshold 12.7 | 20 (15) / 145 | -0.034 +- 0.061 | -0.67 |
| WALLABY only | 10 (8) / 32 | +0.082 +- 0.086 | -3.65 |
| SPARC only | 15 (10) / 91 | -0.028 +- 0.071 | -1.26 |
| matching window 0.3 dex | 25 (23) / 123 | +0.025 +- 0.058 | -3.30 |
| KT2017 dynamical logMd | 7 (7) / 60 | -0.031 +- 0.065 | +0.07 |
| POSTHOC softening 0.01 kpc | 25 (18) / 123 | +0.003 +- 0.065 | -3.28 |
| POSTHOC KT2017 group distance | 25 (18) / 123 | +0.023 +- 0.068 | -3.08 |

All verdicts are NON-DISCRIMINATING.

## Caveats
WALLABY pilot fields are centred on clusters and groups, so WALLABY's "field" is not a random field. The models are marginally
resolved (30 arcsec beam) and their outer rings are correlated. The stellar model is cruder than SPARC's, but centrals are compared
only with controls from the same source and luminosity. Group masses depend on the catalogue recipe. Sources declared and not used:
Di Teodoro+ massive discs (no per-radius baryons), MIGHTEE-HI resolved curves (not public), THINGS/HALOGAS (overlap SPARC),
Ponomareva+2016 (no machine-readable curves and mass models located), BIG-SPARC (not released), WALLABY high-res models (homogeneity).
