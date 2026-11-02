# LM1_law_missing_mass_map: the law's cluster deficit is a roughly fixed multiple of the gas at fixed r/R500, falling outward; no BCG link and no preferred acceleration or surface density scale found

Criteria: `FROZEN_CRITERIA.md` (3fc42aa028), committed alone first. `lm1_grade.py`, `lm1_map.py`; numbers in `lm1.out`, `lm1_results.json`, `lm1_MUTATE.out`, `lm1_results_MUTATE.json`. **Not blind**, and post-hoc in every look: 31 looks, 62 tests with both footings, TREND needs |t| >= 3.34. A measurement, not a mechanism: no rule, no cold sector reinstated, no pass or fail (LW1 owns that). kappa = 1/2 FITTED. Footings never pooled. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

**In one sentence:** inside about R500 the missing mass is a fixed multiple of the gas at the same r/R500, near 8 times at 0.2-0.5 R500 and 5 times at 0.5-1 R500, with no detected dependence on mass, and it falls outward to nothing measurable in all but the heaviest third by 1.7 Mpc.

"Fixed" means an exponent within about +-0.2 per dex over about 1 dex of gas, on catalogue gas. It isn't exact, and it doesn't reach above R500 with any force.

## The map, canonical, f* 0.034, h 0.672, gas +0.005. Alt in `lm1.out`
| R, Mpc | 0.18 | 0.26 | 0.38 | 0.56 | 0.81 | 1.18 | 1.71 | 2.49 |
|---|---|---|---|---|---|---|---|---|
| dDS, M_sun/pc^2 | 25 +- 33 | 47 +- 13 | 46 +- 10 | 37 +- 7 | 22 +- 5 | 9.9 +- 3.7 | 0.5 +- 2.4 | 1.9 +- 1.7 |
| alt | 23 | 44 | 43 | 34 | 20 | 8.0 | -1.2 | 0.6 |
| lensing / law | 1.91 | 2.61 | 2.57 | 2.36 | 1.91 | 1.47 | 1.03 | 1.14 |
| Q, dM/M_gas projected | 4.1 +- 5.2 | 7.5 +- 2.0 | 7.4 +- 1.6 | 6.7 +- 1.3 | 5.0 +- 1.1 | 2.9 +- 1.1 | 0.2 +- 1.0 | 1.2 +- 1.1 |
| M2D_min, 1e13 M_sun, sheet 0 | 1.6 | 3.3 | 5.3 | 7.3 | 8.0 | 6.4 +- 2.4 | 1.2 +- 3.2 | 3.7 +- 3.4 |
| M1, lg Mg 12.52 | 47 | 17 | 23 | 10 | 8 | -2 | -5 +- 4 | -3 +- 3 |
| M2, 13.07 | 85 | 54 | 33 | 42 | 30 | 16 | -2 | -1 |
| M3, 13.47 | -18 +- 57 | 82 | 95 | 74 | 37 | 23 | 14 +- 4 | 14 +- 4 |

M2D_min falls past 1 Mpc because the sheet is set to 0 and the integral runs only over bins; only its inner part means anything.

**X-COP, 3D, 7 clusters, hydrostatic.** Canonical; HSE - 0.12 dex (LF1) in brackets.

| x | 0.1 | 0.2 | 0.3 | 0.5 | 0.7 | 1.0 |
|---|---|---|---|---|---|---|
| M_HSE / M_law | 3.51 | 3.39 | 3.18 | 2.66 | 2.16 | 1.62 |
| dM, 1e14 M_sun | 0.19 | 0.67 | 1.38 | 2.34 | 2.94 | 2.74 |
| dM / M_gas | 8.5 (5.7) | 8.0 (5.2) | 6.7 (4.3) | 5.2 (3.1) | 3.9 (2.1) | 2.3 (0.7) |
| alt | 8.3 (5.4) | 7.7 (4.9) | 6.5 (4.0) | 4.9 (2.8) | | |

Lensing converted to 3D by a local power law (gamma 2.22, a conversion, not a fit): dM/M_gas 4.8, 4.6, 3.5, 2.1 at x about 0.45, 0.66, 0.96, 1.4. It sits near HSE at x 0.45-0.66 and above both HSE and the bracket near x 1, on an averaged stack with a rough conversion. Lensing's Q is projected and X-COP's is 3D, so only the falling shape is compared directly.

## Labels: canonical / alt, f* 0.034, h 0.672
| Look | canonical | alt | Label |
|---|---|---|---|
| L01 slope dDS, INNER | +0.24, raw s 0.77 | +0.25 | NOISE-LIMITED / [hint] |
| L02 MID | -1.66, s 0.45 | -1.82 | NOISE-LIMITED |
| L03 OUTER | +3.00, grid edge | -3.00, grid edge | NOISE-LIMITED, deficit near 0, not a slope |
| L04 one power law | chi^2 18.7/6, p 0.005 | 20.2/6, p 0.003 | NOISE-LIMITED, TREND at h 0.686 |
| L05 slope, M1 - M3 | M1's outer is negative | | NOISE-LIMITED, not meaningful |
| L06, L07 X-COP dM slope, x 0.1-0.3, 0.3-1 | +1.69, +0.63 | +1.69, +0.54 | TREND [N=7]: a bend |
| L08 dDS on Mgas, x 0.2-0.5 | +0.39 +- 0.11 | +0.39 +- 0.11 | TREND (alt [hint] at h 0.686) |
| L09 x 0.5-1 | +0.49 +- 0.17 | +0.50 +- 0.17 | NOISE-LIMITED [hint]; TREND under net, lowering |
| L10 x 1-2 | +0.61 +- 0.30 | +0.70 +- 0.44 | NOISE-LIMITED |
| L11 x 2-5 | +1.87 +- 1.12 | +2.09 +- 1.37 | NOISE-LIMITED; flips sign under rows, unmeasured |
| **L12 row 10, OUTER, data against law** | **0.92 +- 0.25 against 0.49**, t +1.72 | 0.92 against 0.49, t +1.73 | **NOISE-LIMITED** |
| L13 MID | 0.68 +- 0.13 against 0.43, t +1.95 | t +1.97 | CONSTANT (with law's slope), [hint] at h 0.686 |
| **L14 Q on Mgas, x 0.2-0.5** | **-0.14 +- 0.12**, Q(1e13) 8.5 | -0.14 +- 0.12, 8.1 | **CONSTANT**, [hint] -0.18 +- 0.09 under net |
| **L15 x 0.5-1** | **-0.02 +- 0.18**, Q 5.4 | -0.00 +- 0.20, 4.9 | **CONSTANT**, NOISE-LIMITED at h 0.686 |
| L16 x 1-2 | +0.05 +- 0.27, Q 2.8 | +0.13 +- 0.37, 2.1 | NOISE-LIMITED |
| L17 x 2-5 | +1.07 +- 1.21 | +1.29 +- 2.47 | NOISE-LIMITED, unmeasured |
| **L18 Q on x** | **-0.70 +- 0.11** | -0.80 +- 0.12 | **TREND** |
| **L19 X-COP dM/Mgas on x** | **-0.50 +- 0.10** | -0.55 +- 0.11 | **TREND [N=7]** |
| L20 X-COP dM/Mgas on Mgas | -0.30 +- 1.30, 0.31 dex span | | NOISE-LIMITED [N=7] |
| L21, L22 (1+z), MID, OUTER | +2.2 +- 2.1; +3.00 at grid edge | +2.5; +3.00 at edge | NOISE-LIMITED; L22 [hint], TREND at canonical h 0.686, but pinned at the grid's edge: not a measurement |
| L23, L24 BCG, gas removed, INNER, MID | +0.10 +- 0.20, +0.02 +- 0.15 | +0.11 +- 0.24, +0.02 +- 0.23 | CONSTANT canonical, NOISE-LIMITED alt |
| L25-L28 collapse: g_N/a0, V_N/W, r/R500, R | p 0.14, 0.46, 0.50, 0.22 | same to 0.01-0.05 | all NOISE-LIMITED |
| L29 curvature on g_N | -0.19 +- 0.75 | -0.34 +- 0.93 | NOISE-LIMITED |
| L30 X-COP against groups at same g_N | no overlap | no overlap | NOT COMPUTABLE |
| L31 groups' d on g_N | +0.25 +- 0.07 | +0.25 +- 0.07 | TREND |

Other cells: exponents move at most 0.1 at h 0.686 and 0.02 at f* 0.0615, in bands inside R500. Labels that change are listed in `lm1.out`, mostly near-threshold.

## Reading
- **Radial shape.** dDS rises or is flat inside 0.4 Mpc, then falls steeply, -1.7 +- 0.45 at 0.5-1.2 Mpc. X-COP bends the same way: dM runs as r^1.7 inside 0.3 R500 and r^0.6 beyond. **So there's a roll-over near 0.3-0.5 Mpc, about 0.3-0.5 R500, labelled TREND only on X-COP and only as a hint on shear. I give no concentration:** with eight bins and no profile that would be a fit.
- **Gas scaling.** dDS rises with gas at fixed x, but the ratio Q doesn't. So the deficit follows the gas, not the law's sqrt. This also matches row 10's sign, but **row 10 itself doesn't clear look-elsewhere:** 0.92 +- 0.25 against 0.49 here, 2.05 sigma on CFG687. At fixed physical R, the OUTER deficit's own exponent is steep (+1.32 +- 0.23, +1.48 +- 0.43), reported without a label. At fixed x above R500 the exponent is too noisy to say that this slope is only the R500 scaling (L16).
- **Above about 1.2 Mpc the deficit is M3 alone.** M1 and M2 sit at or below the law there, M1's Q negative at -6 +- 5, and x 2-5 is unmeasured.
- **BCG.** No dependence once gas is out, 190 clusters, Spearman with gas 0.52. Canonical is tight enough for CONSTANT, alt isn't.
- **Scales: no preferred scale found.** The frozen rule isn't met: no collapse is labelled CONSTANT, and L30 has no overlap. r/R500 has the smallest chi^2 (9.4/10), but all four orderings fit. Cluster bins overlap across terciles over only 0.3 dex of g_N, so this is weak. **g_N and mean baryon surface density are one variable,** as frozen.
- **Post-hoc, no label.** lg(obs/law) on g_N: lensing -0.02 +- 0.07 at lg g_N/a0 -2.2 to -1.8, +0.21 and +0.32 above; groups at -2.6 to -2.2 read +0.29 +- 0.07 where lensing reads -0.18 +- 0.48. Near zero under g_N/a0 of about 0.01 is the same statement as "outskirts", and it can't be separated from radius here. Groups' mass-estimator caveats apply.

## Against M3A1's rows, canonical. Alt in `lm1.out`
| row | MID M2 | MID M3 | OUTER M1 | OUTER M2 | OUTER M3 | OUTER T2 slope |
|---|---|---|---|---|---|---|
| base | 23.4 | 34.6 | -3.5 | -1.5 | 14.1 | 0.92 |
| C1a M3 | 23.4 | 35.1 | -3.5 | -1.5 | 14.4 | 0.93 |
| C1a all, capped (mine) | 23.3 | 35.0 | -3.7 | -1.6 | 14.4 | 0.98 |
| C2a | 23.4 | 34.1 | -3.5 | -1.5 | 13.8 | 0.91 |
| C4a | 20.7 | 36.2 | -3.5 | -1.6 | 13.9 | 0.91 |
| C4c, a bound | 27.2 | 41.5 | -3.1 | -0.2 | 18.0 | 0.93 |
| C4d | 23.4 | 31.6 | -4.8 | -0.7 | 12.8 | 1.04 |
| C4e | 22.4 | 34.2 | -4.1 | -2.5 | 12.1 | 0.95 |
| net, all | 23.2 | 39.3 | -5.0 | -0.6 | 14.1 | 1.09 |
| lowering only | 19.7 | 32.2 | -5.4 | -1.8 | 10.2 | 1.08 |

**What survives:** MID M2, M3 keep 84 %, 93 % under lowering-only (alt 82 %, 92 %). OUTER M3 keeps 73 % (alt 67 %), 14.1 +- 2.9 stat +- 2.2 sys in quadrature. M1, M2 outer stay at or below zero under every row. Q's flatness inside R500 stays within +-0.2 (-0.19 +- 0.09 at x 0.2-0.5 is a [hint]); L09 rises to TREND. Row 10's t stays 1.7. INNER M3 rises, not falls: 61 to 87, mostly the tercile's own boost and extended randoms. The rows don't include the inner bins' miscentring, so that band is the least secure. The Eddington rows move little, which rests on catalogue errors as M3A1 uses them. C4d and C4e overlap.

## Expectation against result
Wrong: MID slope (I said -0.7, it's -1.7), L30 (I said TREND, there's no overlap). Right: Q falls outward, no acceleration scale, BCG nothing useful, most of MID survives, M1 outer at or below zero. I didn't expect L14 and L15 to reach CONSTANT.

## Limits
1. Mgas is on both axes of L14-L17 in a sense: V_N scales with catalogue gas, whose noise and selection are shared. R500 comes from the same catalogue. Eddington is tested (C1a) and small, intrinsic scatter isn't.
2. Q's denominator includes GS1's tail, measured on X-COP only.
3. All catalogue gas is X-ray-selected, with M1 lying at z 0.15-ish against M3's 0.3, so mass and z aren't fully separated.
4. Collapse chi^2 ignores correlations between bins, as frozen. Fits at x > 1 hit grid edges in some resamples (counts in `lm1.out`).
5. Hydrostatic X-COP and lensing differ by 0.12 dex in the record, and that changes X-COP's ratio by about a third to two-thirds, more outward.
6. F(z) for h 0.686 isn't printed in M3A1, so C4c uses h 0.672's. Systematics are at h 0.672, f* 0.034 only. M3A1's terms were derived on canonical; on alt they're carried.

## Checks: 8 of 8, MUTATE bites
K1 same-process keys against LW1's JSON, both f*, h, footings: |d| 0; G-OUT-M3 +4.759 (DR1's row). K1b dump sums 8e-16. K2 n sums 7e-16. K3 CFG687 T2 0.896 +- 0.209, law 0.466. K4 X-COP against LW1's builder 6e-7. K5 synthetic p 0.7 recovers 0.58 +- 0.63, p 0 NOISE-LIMITED (so, on one band's noise, no false trend). K6 M3A1's rows on its own V: +4.363, +3.959, +3.734. K7 groups 0. **MUTATE a0 x 1.5** (`lm1_MUTATE.out`): every band and X-COP moves, min 0.071; dDS 19, 41, 40, 31, 17, 5.6, -3.2, -1.0. Q's labels on the two inner bands hold or go NOISE-LIMITED: the proportionality isn't tuned to a0. No flip is a result.

Run: `PYTHONHASHSEED=0 python3 lm1_grade.py; python3 lm1_map.py; python3 lm1_map.py --mutate`, one thread, nice 15, about 6 min for the grader, 8 min for the map.

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.
