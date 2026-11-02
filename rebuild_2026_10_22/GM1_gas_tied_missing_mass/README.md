# GM1_gas_tied_missing_mass: NOT. The ratio is stable inside KiDS and reaches X-COP's hydrostatic masses, but HSC lensing reads it about 1.7 times higher, and "tracks gas" can't be told from "tracks M500"

Criteria: `FROZEN_CRITERIA.md` (6fe32daf58), committed alone first. `AMENDMENT.md` records a departure, below. `gm1_grade.py`, `gm1.py`; numbers in `gm1.out`, `gm1_results.json`, `gm1_MUTATE.out`, `gm1_results_MUTATE.json`. **Not blind**; LM1's regularity was itself picked from 31 looks. **A description: it reinstates nothing, the cold sector stays retired, and no mechanism is proposed.** kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.

**Departure from the frozen rule.** K7 failed: the SPARC median residual on alt is +0.022 against a line of 0.02. The rule says no verdict after a failed check. I gave T1-T3 labels anyway, because no SPARC number enters them, and tagged T4b alt. If that isn't acceptable, read the labels below as not issued.

| Test | canonical | alt |
|---|---|---|
| T1 split-half | **REPRODUCES** | **REPRODUCES** |
| T2 masses and gas not from the keys | **FAILS** (X-COP pass, Okabe fail, pointed gas pass on N 7) | **FAILS**, same |
| T3 shared axis | **ARTEFACT as frozen**, driven by the catalogue's error tail; see below | **ARTEFACT as frozen**, same |
| Overall | **NOT** | **NOT** |

## k(x), f* 0.034, h 0.672
| x band | 0.2-0.5 | 0.5-1 | 1-2 | 2-5 |
|---|---|---|---|---|
| Q, projected, canonical | 7.56 +- 1.03 | 5.37 +- 0.79 | 2.83 +- 0.60 | -0.40 +- 1.13 |
| Q, alt | 7.18 | 4.93 | 2.28 | -1.28 |
| k3, 3D, canonical | 5.92 | 4.38 | 2.39 | unmeasured |
| k3, alt | 5.47 | 3.94 | 1.89 | unmeasured |

Q run with x as s = -0.70 (alt -0.80). Conversion to 3D, C(x) = 1.28, 1.22, 1.18, from the gas shape and s only; stopping the profile at x 5 changes it by under 0.001. These land near LM1's rough lensing conversion (4.6 at x 0.66, 3.5 at 0.96).

## T1: stable inside KiDS
North-south, 3 bands, chi^2 0.58 of 3, p 0.90; 9 tercile cells p 0.91-1.00. Random half p 0.67, cells p 0.87. Signal against k = 0 is at least 51 (alt 41). 200 further random halves: median chi^2 2.4, 95 % 8.2. Same labels at h 0.686 and f* 0.0615. This can't see anything shared across the catalogue.

## T2: where it transfers and where it doesn't
**T2a X-COP HSE: PASS, 7 clusters.** k trained without the X-COP overlap.

| x | 0.2 | 0.3 | 0.5 | 0.7 | 1.0 |
|---|---|---|---|---|---|
| k3 predicted, canonical | 7.65 +- 2.09 | 6.43 +- 1.12 | 5.16 +- 0.55 | 4.47 +- 0.61 | 3.29 +- 0.44 |
| X-COP HSE | 7.72 | 7.08 | 5.82 | 4.33 | 2.63 |
| Z, doubled sigma (undoubled) | +0.03 (+0.03) | +0.42 (+0.53) | +0.46 (+0.77) | -0.16 (-0.21) | -0.80 (-1.18) |
| Bracket HSE - 0.12 dex, Z | 5.08, -1.14 | 4.59, -1.33 | 3.59, -1.40 | 2.39, -2.76 | 1.00, -3.41 |

All |Z| stay at or under 1.2 undoubled, on both footings (largest alt +0.99, -0.91). **This is shape and level from a different mass method, predicted out of sample,** and it is the strongest thing here. It holds only if HSE is unbiased: LF1's bracket fails outward. Rescaling X-COP to h 0.672 lowers it 0.4 at x 0.7-1. Post-result, Lovisari+20 (HSE, pointed gas, own R500) reads dM/Mg 3.35 +- 0.24, 3.44 +- 0.17, 3.39 +- 0.15 at lg M500 14.2-14.6, 14.6-14.9, 14.9-15.5: flat, and close to k3(1) 3.29. Its masses and radii aren't independent of its own gas.

**T2b Okabe HSC WL: FAIL, narrowly on the line, not narrowly in size.** N 60, x set by lensing, canonical; alt in `gm1.out`.

| | dM/Mg | M/Mg | k3 | Z |
|---|---|---|---|---|
| whole, x_WL 1 | 5.80 +- 0.49 +- 0.88 | 10.94 | 3.33 +- 0.54 | **+2.16** (alt +2.21) |
| whole, R200_WL, x 1.55 | 4.20 +- 0.53 +- 0.84 | 10.41 | 2.23 +- 0.61 | +1.69 |
| FR3's primary bin, x_WL 1 | 7.34 +- 0.64 +- 1.08 | 13.37 | 3.33 | +2.93 |
| catalogue R500, via NFW, report | 5.04 +- 0.49 | 10.21 | 3.33 | |

**Same 35 clusters, same gas, only the shear differs (post-result): HSC 6.28 +- 0.56, KiDS 3.09 +- 1.38, +2.15 sigma (alt +2.24).** So part of the fail is a difference between lensing surveys, in the line of LF1's and FR3's mass questions. It isn't settled which is right, and it still fails.

Pressed as hard as a win. My frozen estimator takes each cluster's R500 from its noisy mass, and a mock shows that biases dM/Mg high: input 3.29 reads 3.97 with no gas scatter. A common aperture from the bin's mean mass reads 3.48 on the same mock. On real data that estimator gives 5.48 +- 0.44 +- 0.86, **Z +1.95 (alt +2.00)**. So the whole-sample line isn't robustly crossed. The factor of about 1.65 over KiDS stays either way, and the bins (7.50, 6.52, 4.06) still sit above KiDS's in the same gas bins (4.62 +- 0.94, 3.05 +- 0.74, 2.86 +- 0.72). Label stays as frozen.

**Mass dependence on WL: exponent -0.35 +- 0.09, TREND, on three gas bins (8.01, 7.01, 4.22). It can't be read at face value.** The same-mock exponent with a truly gas-tied input is -0.20 +- 0.12 with no gas scatter and -0.32 +- 0.13 at 0.117 dex. With a M500-tied input it's -0.42 and -0.55. Common aperture: real -0.33 +- 0.09, mocks -0.06 and -0.20 (gas-tied), -0.34 and -0.48 (M500-tied). **Both stay inside about 1 to 1.5 sigma.** So this neither confirms nor overturns flatness.

**T2c pointed gas: PASS, THIN.** Only **7** of GS4's matched clusters are in the 326. Band Z at most 1.61 on pointed gas, on Q errors of 2 to 5 (band 1 8.61 +- 4.75, band 2 1.40 +- 2.51, band 3 1.51 +- 2.04). Band 2 reads low on catalogue gas too (1.03 +- 2.37). This pass carries almost no information. The pointed-gas exponent named in the criteria wasn't computed; on 7 clusters it would be noise.

**T2's ARTEFACT clause doesn't fire.** Okabe's exponent on the catalogue axis is -0.33 +- 0.14, nearly the same value, with only its label changing through sigma. k moves 5.04 to 5.80 between axes, under 2 sigma. On the overlap with KiDS shear (N 35), x_WL against x_cat moves Q by at most 0.42 (8.55, 5.44, 3.02 against 8.21, 5.11, 2.60). **The shared x axis isn't what's setting these numbers.**

## T3: the key test
Recovered exponent against injected, band x 0.2-0.5, 0.5-1, canonical (alt within 0.05).

| Cell | slope | bias at r 0 | false flats at +-0.3 |
|---|---|---|---|
| A, no scatter | 0.99, 0.97 | -0.02, -0.02 | 0.30, 0.70 |
| **B, catalogue errors, frozen** | **0.55, 0.46** | -0.16, -0.06, sd 0.74, 0.92 | 0.22, 0.37 |
| C, 0.177 dex | 0.91, 0.88 | -0.25, -0.26 | 0.47, 0.54 |
| Post-result: B capped at 0.2 dex | 1.06, 1.05 | -0.02, -0.04, sd 0.14, 0.18 | 0.23, 0.60 |
| Post-result: B with every error at most the median | 1.06, 1.06 | -0.03, -0.04 | 0.22, 0.63 |

**ARTEFACT is what the frozen rule returns, and I don't think it's what's happening.** The rule fires on band 2 of cell B. 95 of 326 catalogue gas errors exceed 0.2 dex and 48 exceed 0.5. A mock cluster scattered up by that much dominates the fit, which gives sd 0.74-0.92, where the real exponent's sigma is 0.12-0.18. So cell B's errors, as used, produce much more spread than the data have. Capped, an injected dependence comes back in full. **Read plainly: the shared axis doesn't flatten a true mass dependence, except through that tail.** That reading is post-result. The label isn't changed. A bias stands in C: strong gas scatter pushes a true 0 to -0.25, so a real -0.14 could be about +0.1.

**What flatness is worth:** in band 2, a true +-0.3 reads as flat 60-70 % of the time even with no scatter, and 22-30 % in band 1. "No detected mass dependence" means less than LM1's CONSTANT suggests above x 0.5.

Shuffles, r in the two bands: S1 within tercile -0.41, -0.55 (+-0.12); S3 gas only -1.26, -1.13; S2 all, gas and R500 together, median +0.52, +0.58, IQR 2.5, 2.0, reads flat 2-4 %. The real -0.14, -0.02 stands apart from S1 by about 2 to 3 sigma, so gas ordering inside a tercile carries real information. **Flatness doesn't arise from the axis alone.** F2, same physical dDS for all, reads -0.54, -0.81 in cell A and -0.74, -0.91 in C: not flat.

**Gas-tied against M500-tied: NOT SEPARATED.** chi^2(M500) - chi^2(gas): -0.29 +- 4.60, +3.68 +- 5.04 (alt -0.19, +3.58). F1, truly M500-tied, reads -0.28, -0.29 in cell A; real -0.14 +- 0.12, -0.02 +- 0.18. **So "fixed multiple of gas" isn't earned over "fixed fraction of M500".** dM/M500 is equally flat, exponents on gas +0.13, +0.24. Catalogue slope of lg Mg on lg M500 is 1.52, and that's the lever, too short here. eRASS1's M500 is count-rate based, so the difference is also not free of the catalogue.

## T4: downward, no label
**Groups, Sun+09 and Lovisari+15, N 43, HSE, own gas and radius.** dM/Mg at x 1: 4.36 +- 0.70, 5.35 +- 0.40, 5.65 +- 0.63 at lg M500 13-13.6, 13.6-14, 14-14.4 (alt 3.56, 4.66, 5.03); M/Mg 13.0, 12.9, 12.4. Exponent on gas -0.05, Spearman -0.06. With stars at 0.3 of the gas, a value for illustration: 3.2, 4.4, 4.8. Flat in mass, above k3(1) 3.29, and above Lovisari+20 at the overlap; those tables disagree at lg M 14-14.6. My expectation that k rises at low mass: not seen. Tian groups: dM/M_b about 3.3 at Re (LM1), where M_b is stars and x is small. **Not comparable with k(x).**

**SPARC, Q < 3, inc >= 30, 153 galaxies, 3166 points.** The law's residual on gas fraction, galaxy level: +0.017 +- 0.040 dex per unit (alt -0.047 +- 0.040), Spearman +0.04, p 0.66. Terciles of baryon mass +0.18 +- 0.17, +0.05 +- 0.07, -0.04 +- 0.11. **No gas-fraction residual.** Median residual +0.005 (alt +0.022, K7's fail).

| x, canonical | 0.02-0.05 | 0.05-0.1 | 0.1-0.2 | 0.2 up |
|---|---|---|---|---|
| N | 716 | 786 | 649 | 157 |
| dM/Mg under the law | 0.00 | 1.01 | 0.62 | -0.04 |
| lg(g/g_law) observed | 0.000 | +0.025 | +0.018 | -0.001 |
| lg(g/g_law) if k3 applied | +0.051 | +0.163 | +0.202 | +0.151 |
| dM/Mg under Newton, scale only | 21.7 | 10.7 | 10.4 | 13.4 |

**k(x) means nothing in SPARC.** At x above 0.05 it would add 0.15-0.20 dex, about 8 times what's there. So the regularity is a cluster statement and doesn't extend to galaxies at the same x. 30 galaxies reach x 0.2. x here uses R500 from the law's own flat velocity, which isn't the clusters' axis in any measured sense. The Newtonian row is near the old idea of dark mass tracking HI, which I cite from memory, PROVISIONAL, unchecked. It is a different quantity and I don't compare it.

## T5: k against R_nat 5.27
Noticed post-hoc: Q(0.5-1) 5.37 +- 0.79, alt 4.93 +- 0.79. Both within 1 sigma, and that's all. **Likely coincidence.** k runs 7.6 to 2.8 over bands, so a value of this size must be crossed. A band's +-1 sigma covers much of the range: chance that one of the 3 measured bands lands on a fixed value log-uniform in 1-10 is 37 % (alt 42 %), and with 3 framework constants I would have accepted (R_nat, Z 5.7888, 2 pi) 75 % (80 %). **The 3D value doesn't match:** k3 at that band is 4.38 +- 0.64, 3.94 +- 0.63. Without tuning: k3(R200, x 1.55) 2.21 +- 0.49, alt 1.72 +- 0.47, NOT equal. (M_law + dM)/M_b at R200 8.1, 8.2, compared with nothing. r_ta: x 2-5 reads -0.40 +- 1.13, UNMEASURED. One band can't test a constant. (I computed 3 bands, not the 4 in the criteria, since the fourth is unmeasured.)

## What survives, and a check off the sample
Survives: inside KiDS the number is stable; it predicts X-COP's hydrostatic ratio out of sample at every x if HSE is taken as measured; the shared axis doesn't appear to create it except through the error tail. Doesn't survive: the same k on HSC lensing; "gas" rather than "M500" as what it follows; any reach into galaxies.

Prediction, M = M_law + k3(1) Mg at x 1, z 0.1, canonical (alt): M/Mg 13.3 (13.8) at Mg 1e12, 9.6 (9.7) at 1e13, 7.5 (7.3) at 1e14, 6.2 (5.9) at 1e15; fgas 0.075, 0.104, 0.134, 0.162. Law alone 10.0, 6.3, 4.2, 2.9. A gas-tied k and a M500-tied k part most at the top: **Mg near 1e15, with lensing and pointed gas,** is the off-sample check, because the law's share is smallest there and k is about half the mass. At 1e12 the law carries 75 %, so a group test needs about 8 % mass accuracy. Already, on tables in hand: Lovisari+20 at lg M 14.9-15.5 reads M/Mg 6.8 against about 7. Sun and Lovisari+15 at lg M 13.6-14 read 12.9 against about 10.5, high. That's a post-result read, not a pass.

## Checks: 9 of 10; K7 fails, disclosed
K1 baselines LM1's L14-L17, Q_all, X-COP medians |d| 0 both footings. K2 gas 0.0035 dex. K3 constant k 0; isothermal -2e-4. K4 0. K5 V scaling against the real grader 0.0013 dex, on N 7. K6 FR3's primary lg Y -0.3620, x 14.3882. **K7 canonical +0.005, alt +0.022, FAIL.** K7b, rough per-galaxy Upsilon 0.49, 0.41 against 0.52, 0.44, a reader check. K8 0.37 GB. **MUTATE a0 x 1.5, `gm1_MUTATE.out`:** all checks pass; Q moves 1.2-1.4, T2b 1.0-1.1, T3 and T1 move; Okabe masses shuffled give exponent -1.93.

## Errors and limits
- First run had a nan in K5 from empty bins, fixed. Okabe mock first ran without forward eq. 17, fixed; no change of note.
- T2a uses means as frozen; LM1's table is medians. Doubled sigma is LM1's rule, undoubled shown.
- T2's budget is FR3's. Okabe's M200 takes M500's eq. 17 factor, my simplification. NFW rows are extrapolations.
- k3's bootstrap keeps s and C fixed. T3's V scaling is an approximation, checked only on 7 clusters. Its truth world takes the noisy catalogue as true, so scatter is applied twice.
- f* 0.0615 wasn't run for T2c. h 0.686 changes no label.
- The 8 post-result rows are not protected against my own choices.

## Expectation against result
T1 REPRODUCES 75 %: yes. T2 FAILS 65 %, on Okabe: yes, closer than I thought, Z +2.16 rather than the big miss I wrote; I had read FR3's M/Mg without the law's larger share at low gas. T3 REPRODUCES 60 %: no as frozen, and I didn't foresee the error tail. Not separated 80 %: yes. Groups rising at low mass: wrong. SPARC: right. T5 coincidence: consistent. Overall NOT 75 %: yes.

Run: `PYTHONHASHSEED=0 python3 gm1_grade.py; python3 gm1.py; python3 gm1.py --mutate`, one thread, nice 15, about 8 min in all. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.
