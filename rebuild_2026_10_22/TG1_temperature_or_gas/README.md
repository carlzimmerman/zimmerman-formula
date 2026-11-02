# TG1_temperature_or_gas: NOT SEPARABLE on both footings. The deficit rises with X-ray depth, and these data can't say whether temperature or gas carries it; the split leans gas, the joint fit leans temperature, and neither reaches 3 sigma

Criteria: `FROZEN_CRITERIA.md` (2d7ab44aa0), committed alone first. Forecast committed before the split ran on data (5276062aa2). Scripts `tg1_common.py`, `tg1_forecast.py`, `tg1_split.py`; post-result `tg1_post.py`, `tg1_post2.py`. Numbers in their `.out`, `.json`, and `_MUTATE` twins. **Not blind:** X21's and UX7's readings were known. A measurement: no rule, no mechanism, and no law is passed or failed here. The cold sector stays retired and nothing here reinstates it. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.

## Verdict
| Footing | Forecast F, h 0.672, 0.686 (line 3) | Classifier accuracy (line 0.90) | Label |
|---|---|---|---|
| canonical | 0.52, 0.60 | 0.70-0.72 | **NOT SEPARABLE** |
| alt | 0.53, 0.55 | 0.65-0.72 | **NOT SEPARABLE** |

The label comes from the forecast, and the split doesn't overrule it. K4 also failed, and its rule gives the same label, tagged. **Neither "gas carries it" (UX3, LM1) nor "temperature carries it" (X21) is earned against the other.**

## Why the forecast is so low
- **KT is too noisy to split on.** On the 101 clusters with KT and MID shear, the rms catalogue error in lg KT is 0.325, more than the sample's own scatter of 0.233. Deconvolved, intrinsic t and g correlate at +0.99, so a KT split at fixed gas mostly sorts noise, and gas becomes a better temperature proxy than KT. Under a pure temperature truth, the mocks read Z_G (+0.45) above Z_T (+0.25).
- **Shared calibration isn't the limit.** Nuisances off, F is 0.56, 0.55. A mass-calibration tilt 10 times wider cuts F to 0.17, 0.13, so a large tilt would hurt.
- **Size needed, scaling only:** about 3300 clusters at this noise for F = 3.

Stress rows (F never reaches 3):

| Row, h 0.672 | F canonical | F alt |
|---|---|---|
| fixed alpha 1.5, beta 1 | 0.63 | 0.59 |
| q per patch | 0.51 | 0.49 |
| band IM | 0.55 | 0.55 |
| Post-result: KT errors x 0.25, re-deconvolved (rho +0.74) | 1.12 | 0.96 |
| Post-result: best linear axis, F_LD, catalogue errors | 1.11 | 0.91 |

## The split stacks, MID band, f* 0.034
b in M_sun/pc^2 per dex. Z = b / max(bootstrap, 30-patch jackknife, mock sd with all nuisances). Margin = |Z| - 3.

| Cell | b_T at fixed gas | Z_T (margin) | b_G at fixed T | Z_G (margin) | Joint Z_T, Z_G | Joint with z |
|---|---|---|---|---|---|---|
| canonical h 0.672 | +41.6 | +1.35 (-1.65) | +41.4 | +2.49 (-0.51) | +2.32, +1.04 | +2.39, +0.73 |
| canonical h 0.686 | +44.9 | +1.43 (-1.57) | +48.5 | +2.71 (-0.29) | +2.30, +1.42 | +2.29, +1.07 |
| alt h 0.672 | +41.0 | +1.29 (-1.71) | +39.7 | +2.34 (-0.66) | +2.37, +0.92 | +2.29, +0.62 |
| alt h 0.686 | +44.3 | +1.40 (-1.60) | +46.7 | +2.58 (-0.42) | +2.22, +1.30 | +2.29, +0.96 |

dDS high / low, canonical h 0.672:

| Split | bin 1 | bin 2 | bin 3 |
|---|---|---|---|
| KT, within gas bins | 6.1 / 2.7 | 21.2 / 9.2 | 59.2 / 30.8 |
| gas, within KT bins | 8.3 / -0.9 | 36.5 / 5.0 | 59.7 / 25.5 |

All six cells rise, on the ratio n/V too (`tg1_split.out`). Same reading at f* 0.0615, band IM: b_T Z +1.29 to +1.45, b_G Z +2.24 to +2.67, without the mock sd. L300kpc as gas (no R500 in it; V still inherits R500): b_T Z +1.19 to +1.27, b_L Z +1.65 to +2.10.

## The leans disagree, read as hard as a win
- **Split leans gas, joint leans temperature.** Likelihood ratio T/G on the split clouds is 0.09-0.16. On the joint fit, b_T is about 60 and b_G 12-17. I don't pick one; either way the leans are under 3.
- **The split's T row isn't clean:** residual gas imbalance is 0.475 of the KT contrast (K3 passes, line 0.5). Solving it out, a rough post-result linear reading with no errors, gives b_T about +24, b_G +36 to +45.
- **The joint fit is exposed to KT's noise and to nonlinearity,** since the excess is strongly convex in both variables and the fit is linear.
- **The joint data sit outside both clouds.** Post-result, on the mock sd alone z_T is about +3.6, with p 0.002-0.004 under gas and 0.000-0.002 under temperature. The mock sd of 16.5 is well under the data's 26, so the mock misses real scatter or leverage in KT. So part of the mock is wrong here. Catalogue KT errors may be too large, which the x 0.25 row tries, and F still stays under 3.
- **What holds:** a flat deficit fits poorly on the split, Mahalanobis 10.4-13.8 on 2 axes against 2.9-3.4 for gas and 6.6-8.3 for temperature. That approximates p about 0.001-0.005, not trial-corrected. A depth trend is there. This is what X21 and LM1 already showed, not a new detection.
- **Pure temperature is pressed on the split:** p(|Z_G| at least observed, given HT) is 0.011-0.029 against the frozen 0.01. The other way, p(|Z_T|, given HG) is 0.100-0.123. On the joint this flips. No weight.

## Shared mass calibration, how it's handled
- Physical apertures only: no R500 sets a bin.
- Each mock draws a mass-tilt (sd 0.10 per dex of M500), a gas level (0.05), a KT tilt (0.15), a shear level (0.02) and correlated X-ray error (rho -0.5 to 0.5). Widths are my own, PROVISIONAL, none looked up. F is measured over mocks, so it sees them.
- Gas error reaches the excess through V with its true sign, gamma about 0.55. That biases H0's Z_G by about -0.3.
- L300kpc row above.
- **Not handled:** V inherits catalogue R500 and Mg500 on every row; M500 is calibrated on shear including KiDS, so that isn't independent at the global level; no independent temperature for this sample is on disk, so the KT tilt can't be measured.

## Checks: failures under frozen labels
| Check | Result |
|---|---|
| K0, K1, K2 | PASS: 0, 0, 1e-16; noiseless split b_T 1.300 for plant 1.3, leak b_G +0.189 |
| K3 balance | PASS, 0.475, 0.149, line 0.5; the first is close |
| **K4** | **FAIL.** T errors x 3 raises F (0.68 against 0.52). Plants off 0.01 pass; tilt x 10 reacts, pass |
| **K5** | **FAIL.** H0 median Z_G -0.274 against 0.25, from gas error in V. sd 1.00 pass |
| **Plant MUTATE** | **FAIL.** Plants x 3 lowers F, 0.52 to 0.26. Post-result, F_LD rises 1.11 to 2.05 |
| K6 | PASS |
| K7 rerun | PASS, byte-identical, 7 files compared |
| KT-shuffle MUTATE | Fails K0, exits 1, as required. b_T -3.6 to +6.7, b_G +10 to +12 |

**K4 and the plant MUTATE show my frozen statistic is flawed.** Delta = Z_T - Z_G isn't monotone: a stronger plant lifts both Z, so the difference needn't grow. The classifier and F_LD behave properly, and at catalogue errors they also fall short: accuracy 0.65-0.72, F_LD 0.91-1.11. So the label doesn't rest on the flaw, but F's values are low partly because of it. Without amending: on the plant size the data imply, the honest number is F_LD about 1.

`tg1_split.py` implements only the NOT SEPARABLE branch of the verdict table, since the forecast never reached the rest.

## Expectation against result
NOT SEPARABLE 70 %: yes, on both. Lean temperature 60 %, gas 15 %, neither 25 %: split says gas, joint says temperature, so **no clean hit.**

## Limits, unfinished
- KT on 106 of 326, flux-selected; 101 with MID weight. Only KT against Mg500 is asked; KT can't be told from M500 or potential depth, and both come from one X-ray image.
- Keys are KiDS; HSC's disagreement is outside this lane.
- Plant exponents are marginal fits on noisy variables.
- **Needed, not on disk:** pointed temperatures and more clusters with lensing. Pointed KT alone, roughly the x 0.25 row, reaches F about 1 on this N, so a sample in the many hundreds is needed too; that's from sqrt(N) scaling, not a computed forecast.

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.
