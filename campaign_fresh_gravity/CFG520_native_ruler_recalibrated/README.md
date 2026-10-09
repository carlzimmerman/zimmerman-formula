# CFG520: the native ruler could not be recalibrated. CALIBRATION FAILED under both declared occupation forms, so there is no validation and no re-score of CFG506. Part B: with the measured leaked fraction 0.223, CFG503's LCDM passes its G1 gate (chi2 34.3 -> 26.1, p 0.037); CFG502's LCDM gets worse (45.9 -> 59.2)

Criteria: `FROZEN_CRITERIA.md`, committed alone before any script (6d184c37d). No new PM simulation and no particle load were run: the calibration uses CFG506's stored S0 halo catalogues only. nice 10, 2 threads.
- kappa = 1/2 is FITTED. Footings 9.3603e-11 and 1.1312e-10 are scored separately and never pooled.
- "Cold energy" = the cold clumping component. Its mass is still required, and no particle species is added.
- Nothing here says the data favour the framework. Not "theory closed".

## Part A: recalibrating the box galaxy-halo rule (numbers from `cfg520_calib_results.json`)

**Target.** CFG519's parent (all candidates) satellite fraction S_IC, computed with CFG519's own cell code.
- C_T PASS: it reproduces f_ALL_parent 0.3133864615 and ISO f_IC 0.2234274645 exactly.
- Calibration bins and targets (z 0.1-0.4):
  - log M* 10.50-10.75: T = 0.325 +- 0.004
  - log M* 10.75-11.00: T = 0.309 +- 0.005
- The measured fraction is flat in mass. The full (log M*, z) table is in `cfg520_calib.out`.

**Fits.** The fits used the S0 catalogues only (blindness check PASS: no TA box and no shear file was opened).

| rule | B | alpha | f_box (10.5-10.75 / 10.75-11.0) | weighted mean (box / data) | CAL-OK (each bin within 0.05, mean within 0.02) |
|---|---|---|---|---|---|
| CFG506 | 17 | 1 | 0.594 / 0.373 | | (reference) |
| primary (alpha = 1) | 64.9 | 1 | 0.463 / 0.169 | 0.309 / 0.317 | **FAIL** (off by +0.14 / -0.14) |
| declared fallback (B, alpha) | 175.8 | 0.30 (edge of the declared range) | 0.389 / 0.247 | 0.315 / 0.317 | **FAIL** (off by +0.064 / -0.062) |

- **By the frozen rule this is CALIBRATION FAILED.** The lane stops here: no validation, no DeltaSigma stage, no KiDS re-score.
- C_A PASS at the fallback rule on both S0 boxes. The drawn catalogue agrees with the expectation to within 0.007 per bin.
- **The fail is not a bug.** The same code with B = 17 reproduces CFG506's box (f_box 0.594 / 0.373, and per-0.1-dex fractions equal to CFG506's `fsat_par`, e.g. 0.657 at 10.5). The doubled-target MUTATE calibration converges (see below).

**Why it fails (post-hoc, `cfg520_posthoc.*`; not a verdict).**
- **PH1: box resolution.** To get fewer satellites, the abundance match has to put more galaxies in centrals.
  - That pushes log M* 10.5 centrals down to log M_ta 11.73-11.76, below the 512^3 completeness mass (log 150 m_p = 11.89).
  - So m_lim,box rises from 10.42 to 10.58-10.62. The lower calibration bin then lacks some of its centrals, and its satellite fraction is inflated.
- **Shape.** Above completeness, the box fraction still falls steeply with mass under both forms: primary 0.45 at 10.6 -> 0.08 at 11.0; fallback 0.39 -> 0.20. The data are flat at about 0.31.
- **PH2.** Fitting the primary form to the upper bin alone gives B = 24.5. The lower bin then sits at 0.571 against 0.325.
- **PH3.** The fallback optimum sits on the declared edge (alpha = 0.30). Outside the frozen range, alpha 0.15-0.20 would scrape through CAL-OK (0.363-0.373 / 0.260-0.265).
  - That is an almost host-mass-independent occupation.
  - Adopting it would need a new frozen lane. It is not done here.
- **So the CFG502 occupation form (power law in M - M_min on the box M_ta, SMF abundance match) cannot reproduce the measured flat ~0.32 parent fraction on the 512^3 boxes within the frozen tolerance.** Two limits act together: the box's halo completeness at KiDS lens masses, and the form's mass trend.
- Not modelled, and may matter for a follow-up:
  - photometric-mass scatter in KiDS (it flattens an observed trend);
  - the M* definition (+0.15 dex flux scale);
  - G3C's group-finding definition, where CFG519's definitional spread is 0.13-0.22 for ISO.

**What survives from CFG506.** Its ruler stays INVALID. The record's statement is unchanged: the zero-knob gravity changes the environment term by <= 0.2-0.8 sigma_data per bin relative to S0 (CFG506). The native ruler cannot yet give a KiDS model verdict.

**What would unblock it (new frozen lane, owner's call).**
- A resolved host population at log M_ta ~11.5-11.9: a 1024^3 box or a zoom, which CFG506 also asked for its inner bins.
- An occupation form whose mass trend is fixed in advance from data. Examples: a conditional SMF fitted to G3C, or a near-flat occupation (PH3), frozen before use.

**MUTATE M2X (doubled targets 0.650 / 0.619).** The primary form fails, and the fallback calibrates: B 3.17, alpha 0.76, f_box 0.684 / 0.588, CAL-OK True.
- So the procedure can calibrate a satellite-rich box, but not the measured one.
- Its load-bearing role (validation must fail) never ran, because the main lane has no validation. No box was run for it.

## Part B: CFG502 / CFG503 with the measured leaked fraction (numbers from `cfg520_partB_results.json`)

**Method.** Each lane's f grid is scaled to f_obs = 0.2234 and E is rebuilt from that lane's own stored pieces.
- Checks, all PASS:
  - B0: E tables rebuilt exactly (<= 5e-14).
  - B1: CFG502's 14 chi2 reproduced (max |d| 0.0000).
  - B2: CFG503's 14 chi2 reproduced (max |d| 0.0000).
  - C1: the data match CFG377.
- Scale factors: CFG502 s = 1.3049; CFG503 s_M = 1.2374, s_B = 1.2358.
- E rises by 24-47% at 0.3-1.4 Mpc. Stack P at 0.44 Mpc: CFG502 2.25 -> 2.95, CFG503 2.24 -> 2.79 Msun/pc^2.

**Stack P, 15 bins: chi2 old -> new (Delta)**

| model | CFG502 canonical | CFG502 alt | CFG503 canonical | CFG503 alt |
|---|---|---|---|---|
| LCDM | 45.92 -> 59.15 (+13.2) | same | **34.34 -> 26.13 (-8.2), p 0.037** | same |
| law to r_ta | 53.92 -> 51.59 (-2.3) | 38.29 -> 49.91 (+11.6) | 81.38 -> 69.75 (-11.6) | 59.51 -> 55.00 (-4.5) |
| 5.85 r_M edge | 429.1 -> 306.4 (-122.7) | 431.5 -> 307.9 (-123.6) | 416.7 -> 320.7 (-96.0) | 417.7 -> 320.8 (-96.9) |
| V1 | 57.22 -> 41.50 (-15.7) | 34.33 -> 31.58 (-2.7) | 85.05 -> 66.33 (-18.7) | 57.74 -> 46.19 (-11.5) |
| F_dd | 23.28 -> 22.56 (-0.7) | 23.50 -> 24.99 (+1.5) | 24.68 -> 20.67 (-4.0) | 25.01 -> 21.50 (-3.5) |
| F_nodd (reported) | 51.42 -> 84.97 | 60.82 -> 99.05 | 26.81 -> 25.53 | 29.44 -> 28.96 |

**Inner 9 bins.**
- CFG503 LCDM: 7.60 -> 7.93.
- CFG503 F_dd: 5.24 -> 4.46 (can).
- CFG503 law to r_ta: 60.7 -> 50.3.
- CFG503 edge: 240.9 -> 206.0.
- CFG502 LCDM: 22.3 -> 36.8.

**Gates.**
- CFG502's gate still FAILS: LCDM 59.15, p 3.5e-7. In CFG502 (no stripping) the larger satellite term overshoots the inner bins; its outer 6 improve, 26.1 -> 19.4.
- **CFG503's G1 now PASSES**: LCDM 26.13 / 15, p 0.037. The E-only variant gives 26.06; a constant f = 0.2234 gives 27.16.
- What this does and does not mean:
  - With the measured leakage, CFG503's stripped, nonlinear LCDM-native template meets its own stack-P gate.
  - It is a re-score with a measured input, not a new frozen verdict.
  - CFG503's G3 (the ALL null) was not re-scored here, and its frozen "MODEL STILL INADEQUATE" label stands.
- On that template, every framework model except F_dd stays far above LCDM. The edge is +300.0 / +299.3 above F_dd. F_dd's low chi2 is the halo-mass degeneracy named in CFG495/502/503, not a drawdown detection.

**Disclosed point (dated 2026-10-09).** CFG502's 0.171 and CFG503's 0.181 are the same f grid under two weightings: per-lens summed weight vs CFG506's pair-weighted convention.
- The frozen rule scales each to 0.2234 in its own convention.
- So CFG502's scaled grid reads 0.236 in CFG506's convention.
- The constant-f row (reported in `cfg520_partB.out`) brackets this: CFG502 LCDM 69.6, CFG503 LCDM 27.2.

## Controls, MUTATE, departures
- **PASS:** C_T, C_A (both S0 boxes), blindness, B0 (three tables), B1, B2, C1. The M2X calibration converges.
- **Not run, because the calibration failed (prepared code kept):**
  - `cfg520_box.py`: R0a, the stage split and the memory guard. A test load measured 8.1 GB peak for particles plus the tree.
  - `cfg520_score.py`: R0b, R0c, V-A / V-B and the re-score.
  - MUTATE M2X validation and SHUF.
- **Implementation detail (disclosed).** The fallback alpha scan evaluates log B on a 0.05-dex grid, then 0.005 dex around the minimum, then a bounded refinement. This is for run time; the primary uses the full 0.005-dex grid as frozen. The best alpha is at the scan edge, which PH3 examines.
- PH1-PH3 are post-hoc, written after the fail was seen.

## Run
```
nice -n 10 python3 -u cfg520_calib.py ; CFG520_MUTATE=1 nice -n 10 python3 -u cfg520_calib.py   # ~2 h each (fallback scan)
nice -n 10 python3 cfg520_partB.py                                                             # seconds
nice -n 10 python3 cfg520_posthoc.py                                                           # post-hoc, ~10 min
```
Inputs: `../_external_data/cfg506_work/cfg506_box_S0512_*.npz`, `cfg519_work/cfg519_state.npz`, `cfg502_work/*`, `cfg503_work/*` (not committed).
