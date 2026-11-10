# SHP1 RESULT: the shape of the cold component, from raw data (2026-11-10)

Criteria db5f7da07b (committed alone, before any script or number). TEST lane, quarantined: adopts nothing, relabels
nothing, registers nothing. Footings never pooled. Origin ids: see the last section.

## Label

**THE LAW'S SHAPE ON ROTATION CURVES, LENSING ABOVE; NOT ONE SHAPE (R3b)** / the same (canonical / alt). Every known
answer passes, every MUTATE arm bites, `SHP1.lean` compiles (9 theorems, standard axioms) and its false twin does not.

Here "cold component" means all gravitating mass that is not baryons. Its enclosed mass is
X = M_C(<r) / M_b(<r) = g_obs / g_bar - 1, plotted against x = r / r_M = sqrt(a0 / g_bar).

**The shape, in one line.** X(x) = (sqrt(1 + 4x^2) - 1) / 2: about x^2 inside the law's radius r_M (density ~ 1/r), about
x outside it (density ~ 1/r^2). That is the counted-once law, certified in Lean.

- **Rotation curves follow it in every bin.** SPARC has 2700 points in 149 galaxies. The worst bin median is within
  0.057 dex canonical (0.021 alt) for x from 0.18 to 10, against a line of 0.10. The measured local slope d ln X / d ln x
  is 2.2-2.5 near x ~ 0.6 and 0.9-1.3 from x ~ 1 to 6.
- **Lensing has the law's shape but sits above it.** KiDS isolated lenses (B21 as published) sit 1.40 +- 0.03 /
  1.28 +- 0.03 times the law, roughly flat from x ~ 15 to ~ 200 (p 1e-33 / 1e-21). With B21's hot gas counted as baryons
  they sit below instead: 0.91 / 0.83 on average, falling to 0.19 / 0.18 at the last point.
- **Not one shape across mass, on lensing only.** KiDS's lowest stellar-mass bin (log M* 8.5-10.3) sits 0.21 / 0.19 below
  the other three (p 0.002). On rotation curves there is no trend with M_b (+0.028 / +0.027 dex per dex; line 0.05).
- **How much separate cold mass the data allow on top of the law** (R4, reported). R4 uses the record's own share
  profile (rho ~ 1/r^2 inside SWT1's R_h).
  - The record's full cosmic share, PD1's 59.5 M_b, is excluded on every reading: Delta chi^2 +565 to +6500 against no
    halo at all.
  - The record's own share (5.56 M_b) is allowed; the published points even prefer it to nothing (Delta chi^2 -43 to
    -84).
  - The best separate halo is 4.6-18 M_b on the published points and 1.9-5.3 M_b with hot gas.
  - A post-hoc check fits the excess better as B21's baryons being 1.9 / 1.6 times heavier (chi^2 57 vs 82 on 15
    points). So the data do not require any separate halo.

## R1: shape on rotation curves (SPARC, Upsilon_disk 0.5, Upsilon_bulge 0.7, Lelli+2017's cuts)

| log10 x bin | n (canonical) | median X measured | X_L at mid-bin | median delta (dex) canonical | alt |
|---|---|---|---|---|---|
| -1.00 to -0.75 | 12 (not graded) | 0.143 | 0.017 | +0.046 | +0.002 |
| -0.75 to -0.50 | 78 | 0.015 | 0.053 | -0.018 | -0.020 |
| -0.50 to -0.25 | 239 | 0.150 | 0.154 | -0.007 | -0.021 |
| -0.25 to 0.00 | 389 | 0.541 | 0.401 | +0.032 | +0.014 |
| 0.00 to 0.25 | 555 | 1.04 | 0.924 | +0.031 | +0.006 |
| 0.25 to 0.50 | 633 | 2.21 | 1.92 | +0.042 | +0.008 |
| 0.50 to 0.75 | 658 | 3.82 | 3.75 | +0.019 | -0.006 |
| 0.75 to 1.00 | 134 | 7.24 | 7.02 | +0.057 | -0.011 |
| 1.00 to 1.25 | 2 (not graded) | 10.1 | 12.8 | -0.015 | +0.058 |
| **R1** | | | | **PASS** | **PASS** |

The pass holds at the standard mass-to-light ratios only. At Upsilon_disk 0.3 or 0.8 (bulge 0.5 / 1.0) R1 fails: the
worst bin reaches 0.15-0.18 dex. The criteria named "0.3 / 0.8" brackets without a bulge value, so the bulge moved
with the disc; this is disclosed here.

## R2: shape on lensing (B21 isolated lenses, full covariance)

| | chi^2 / N | p | inverse-variance mean of g_obs / g_law - 1 | reading |
|---|---|---|---|---|
| published (no hot gas), canonical | 194.1 / 15 | 3e-33 | +0.403 +- 0.034 | **ABOVE** |
| published, alt | 133.0 / 15 | 6e-21 | +0.280 +- 0.031 | **ABOVE** |
| hot-gas bracket, canonical | 346.0 / 15 | 1e-64 | -0.092 +- 0.024 | BELOW (not graded) |
| hot-gas bracket, alt | 395.4 / 15 | 6e-75 | -0.173 +- 0.022 | BELOW (not graded) |

Per-point ratio g_obs / g_law, canonical, from x = 5 out to x = 260:

- Published: 0.90, 1.20, 1.26, 1.27, 1.51, 1.43, 1.69, 1.52, 1.75, 1.46, 1.50, 1.73, 1.56, 1.49, 1.18 (errors 0.11-0.15).
- Hot gas: 0.97, 1.14, 1.20, 1.31, 1.34, 1.38, 1.36, 1.46, 1.24, 1.19, 1.14, 0.83, 0.62, 0.34, 0.19.

**What the ratio says about the shape.**
- On the published points the ratio is flat from x ~ 15 to ~ 200. That means the law's shape at a higher amplitude.
- With hot gas the ratio turns over past x ~ 100: the dark mass stops growing like x. If B21's hot gas is real, the
  cold component has an edge near x ~ 100-150.

## R3: one shape?

| | canonical | alt |
|---|---|---|
| R3a SPARC: count-weighted slope of delta against log10 M_b (per-bin slopes -0.03 to +0.14) | +0.028 dex/dex, **PASS** | +0.027, **PASS** |
| R3b KiDS: four stellar-mass bins about one profile, cross-bin covariance | chi^2 77.3 / 45, p 0.0020, **FAIL** | the same, **FAIL** |
| R3b offsets of bins 1-4 from the common profile | -0.209, +0.041, +0.031, +0.032 | -0.190, +0.038, +0.029, +0.029 |

The failure comes from the lowest-mass lenses alone; the other three bins agree within 0.01. This lane does not
separate the cause (stellar masses, host leakage, or the component itself).

## R4: room for a separate cold halo on top of the law (reported, not graded)

Profile: X_s M_b with rho ~ 1/r^2 inside R_h = Rms("NC", M_b, 0, a_n). Fitted with X_s >= 0 to the four mass bins
jointly, with full covariance.

| z_n (R_h, kpc, for the four bins) | X_s fit, canonical | 2 sigma UL | Delta chi^2 vs no halo: 5.56 / 59.5 | X_s fit, alt | UL | Delta chi^2: 5.56 / 59.5 |
|---|---|---|---|---|---|---|
| 6 (46 / 103 / 125 / 146) | 6.2 +- 0.7 | 7.6 | -82.6 / +6041 | 4.6 +- 0.7 | 5.9 | -42.8 / +6466 |
| 3 (80 / 180 / 218 / 254) | 11.4 +- 1.1 | 13.5 | -83.7 / +1909 | 8.6 +- 1.1 | 10.8 | -56.9 / +2196 |
| 1.5 (125 / 281 / 340 / 396) | 18.1 +- 1.6 | 21.2 | -69.2 / +565 | 13.9 +- 1.6 | 17.0 | -50.2 / +768 |
| Nobins, hot gas, log M_b 10.45, z_n 3 | 5.3 +- 1.0 | 7.2 | -28.3 / +2999 | 1.9 +- 1.0 | 3.9 | +10.1 / +3409 |

**Post-hoc check** (`shp1_posthoc.py`, written after `shp1.out` was read; not in the criteria; grades nothing). It
scales every lens's baryons by k and refits.

| data | law alone | best k | chi^2 with k | separate halo instead (z_n 3) |
|---|---|---|---|---|
| published, canonical | chi^2 194.1 / 15 | k = 1.89 [1.80, 1.97] | 57.1 | X_s 12.0, chi^2 81.5 |
| published, alt | 133.0 / 15 | k = 1.59 [1.52, 1.67] | 53.4 | X_s 9.1, chi^2 69.1 |
| four mass bins, canonical | 269.0 / 60 | 1.88 | 133.3 | X_s 11.4, chi^2 155.6 |
| four mass bins, alt | 208.2 / 60 | 1.59 | 129.6 | X_s 8.6, chi^2 143.1 |
| hot gas, canonical | 346.0 / 15 | 0.84 | 332.6 | X_s 5.3, chi^2 317.6 |
| hot gas, alt | 395.4 / 15 | 0.69 | 335.0 | X_s 1.9, chi^2 391.7 |

Neither reading fits well. On the published points the flat excess is better described as a baryon calibration
(B21's masses about 1.6-1.9 times low, matching KO1's "inner level 1.6 to 1.8 above the law" and ONE1's fitted
calibration) than as a separate cold halo. With hot gas, nothing of the law's shape fits, because the points turn over.

## Checks

| check | result |
|---|---|
| KA1: synthetic law data | every residual, slope, chi^2 and X_s exactly 0, both footings: PASS |
| KA2: conversion | SNP1's arrays reproduced exactly; B21's README v_circ formula agrees to 2.1e-4: PASS |
| KA3: SPARC | 175 files, 2700 points (Lelli+2017: 2693), 149 galaxies (153): PASS |
| KA4: closed form against u_in | 3e-16: PASS |
| KA5: truncated-isothermal ESD against direct quadrature | 8e-16, 2e-15: PASS |
| MUTATE M1: a0 x 2 | R1 FAILS (worst 0.114 / 0.152 dex): bites |
| MUTATE M2: injected separate halo of 59.5 | recovered 59.5 +- 1.1: bites |
| MUTATE M3: injected mass trend | slope +0.228 / +0.227, R3a FAILS: bites |
| Lean `SHP1.lean` | exit 0; 9 theorems (`closed`, `X_le_x`, `X_ge`, `X_le_sq`, `X_strictMono`, `hasDerivAt_X`, `D_strictAnti`, `D_inj`, `law_identity`); axioms propext, Classical.choice, Quot.sound only |
| Lean `SHP1_MUTATE.lean` | exit 1; 7 errors at lines 96-134, all inside the six false versions (from line 92) |

**Against the pre-freeze estimates.**
- R1: held.
- R2: held for the sign (above, with no hot gas).
- R3: the four KiDS bins do not agree. I expected them to.
- R4: held. The record's share is allowed, and the published points prefer more than it.

## What it means, in plain words

- **The cold component has one measured shape around galaxies, and it is the law's.** Inside r_M it rises like r^2
  (density 1/r). Outside it rises like r (density 1/r^2). Rotation curves show this to within 0.06 dex from 0.2 r_M to
  10 r_M. Lensing shows the same shape out to about 200 r_M. Its level there depends on how the lenses' baryons are
  counted: 1.3-1.4 times the law with B21's stars, below it with B21's hot gas.
- **On clearing: the data do not ask for the record's share to be removed. They forbid a cosmic-sized halo on top of the
  law.**
  - A galaxy cannot carry its full cosmic cold share, 59.5 M_b, as a separate halo beside the law. That is excluded by
    Delta chi^2 of hundreds to thousands on every reading.
  - Whatever the cold component is, near galaxies it either is the law's halo (counted once) or is absent. It cannot be
    both there and extra.
  - The record's own share (5.56 M_b) on top of the law is not excluded. A baryon calibration explains the lensing
    excess better than any separate halo does.
- **An edge, if the hot gas is real.** With B21's hot gas the shape stops growing past x ~ 100-150. For an L* lens that
  is about 1 Mpc. That is beyond PD1's cap (x ~ 60) and short of the radius where the halo's density meets rho_DE
  (x 230-570 for the four masses).
- **Not one shape across mass, on lensing only.** KiDS's lowest-mass lenses sit 0.2 dex low. Rotation curves show no
  mass trend.

## Files

- `FROZEN_CRITERIA.md`
- `shp1.py`, with `shp1.json` / `shp1.out` and `shp1_MUTATE.json` / `shp1_MUTATE.out`
- `shp1_posthoc.py`, with `shp1_posthoc.json` / `shp1_posthoc.out` (post hoc, labelled)
- `SHP1.lean`, `SHP1_MUTATE.lean`, `compile.txt`, `compile_MUTATE.txt`
- `THEORY.md`: the coherent statement this lane feeds, a note that grades nothing.

## Commit ids

Shared checkout: criteria db5f7da07b; result: see `git log -- fable52_push/SHP1_cold_component_shape`. Origin: filled
in after the push.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
