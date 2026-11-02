# UX7_gas_term_shape: no form passes, and none reaches the frozen NEAR MISS. Local gas (F1) is the closest shape, IMPROVED on alt only, NO GAIN on canonical, with a worse joint chi^2 than the base term on both. M500 against gas: NOT SEPARABLE. No keyed k clears all 15 on any row

Criteria: `FROZEN_CRITERIA.md` (f96def22b5), committed alone first. Scripts `ux7_mass.py`, `ux7_fit.py`, `ux7_grade.py`, `ux7_read.py`, post-result `ux7_post.py`; order in `rerun.sh`. Numbers in `ux7_read.out`, `ux7_fit.out`, `ux7_mass.out`, `ux7_post.out`, their JSON. **Not blind, and the list was steered by the known miss.** Every form is FITTED, a description: no action, no field equation, nothing derived. **Discs are not graded and nothing here is a disc claim; they stay an open problem for every form.** The cold sector stays retired and nothing here reinstates it. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.

## Fitted forms, primary cell (gas +0.005, f* 0.034). k from X-COP train only
Margin = worst |Z| over both h, minus 2. Negative would clear every key. p is the smaller of the two h. X-COP lines: |mean| <= 0.05, rms <= 0.10.

**Canonical.** Frozen rank: F0 > F2 > F1 > F3 > R1 > F7 > F8 > F6 > F4 > F5 > R2.

| Form | k | keys | margin | over 2 | M3, h 0.672 | OUT-all | chi^2, h 0.672 | boot p | jack p | X-COP unseen | Label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F0 enclosed (UX3) | 13.29 | 14 | +0.77 | OUT-all | +0.58 | -2.71 | 16.1 | 0.20 | 0.20 | -0.044, 0.081 | reference |
| F1 local gas | 7.74 | 13 | **+0.56** | MID-T3, OUT-M3 | +2.56 | -1.86 | 21.7 | 0.067 | 0.02 | -0.040, 0.066 | NO GAIN |
| F2 saturating | 15.39 | 14 | +0.98 | OUT-all | +0.11 | -2.92 | 15.6 | 0.22 | 0.26 | -0.040, 0.076 | NO GAIN |
| F3 all baryons | 11.35 | 13 | +0.57 | MID-T3, OUT-all | +1.07 | -2.51 | 18.3 | 0.12 | 0.092 | -0.039, 0.075 | NO GAIN |
| F4 in a0 | 74.4 | 8 | +2.25 | 7 keys | -2.40 | -4.21 | 28.2 | 0.011 | 0.021 | -0.030, 0.077 | NO GAIN |
| F5 additive | 6.80 | 6 | +4.85 | 9 keys | -5.22 | -6.24 | 78.7 | 1e-10 | 3e-12 | -0.025, 0.090 | NO GAIN |
| F6 two-body | 82.3 | 11 | +1.69 | 4 keys | +3.69 | -1.35 | 37.1 | 7e-4 | 9e-6 | -0.060, 0.132 | X-COP FAIL |
| F7 additive local | 4.05 | 10 | +1.64 | 5 keys | -0.54 | -3.59 | 18.6 | 0.19 | 0.16 | -0.025, 0.057 | NO GAIN |
| F8 atmosphere | 18.18 | 13 | +1.47 | MID-T3, OUT-M3 | +3.47 | -1.46 | 28.5 | 0.013 | 9e-4 | -0.037, 0.079 | NO GAIN |
| R1 M500 boost | 1.79 | 12 | +1.01 | MID-b, OUT-M2, OUT-all | +0.79 | -2.90 | 18.4 | 0.14 | 0.13 | +0.001, 0.091 | NO GAIN |
| R2 M500 additive | 0.90 | 4 | +6.98 | 11 keys | -4.73 | -7.30 | 111.5 | 8e-18 | 8e-25 | +0.024, 0.105 | X-COP FAIL |

**Alt.** Frozen rank: F1 > F0 > F3 > F2 > F8 > F6 > R1 > F7 > F4 > F5 > R2.

| Form | k | keys | margin | over 2 | M3, h 0.672 | OUT-all | chi^2, h 0.672 | boot p | jack p | X-COP unseen | Label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F0 | 14.25 | 10 | +1.29 | 5 keys | -0.06 | -3.23 | 18.5 | 0.12 | 0.14 | -0.042, 0.079 | reference |
| **F1** | 8.30 | 13 | **+0.48** | MID-T3, OUT-all | +1.86 | -2.40 | 20.0 | 0.099 | 0.047 | -0.038, 0.063 | **IMPROVED** |
| F2 | 16.13 | 10 | +1.45 | 5 keys | -0.44 | -3.40 | 18.9 | 0.11 | 0.15 | -0.039, 0.076 | NO GAIN |
| F3 | 12.17 | 10 | +1.10 | 5 keys | +0.41 | -3.03 | 19.6 | 0.086 | 0.087 | -0.037, 0.073 | NO GAIN |
| F4 | 72.9 | 8 | +2.59 | 7 keys | -2.71 | -4.55 | 33.7 | 0.002 | 0.003 | -0.029, 0.078 | NO GAIN |
| F5 | 6.52 | 6 | +5.38 | 9 keys | -5.60 | -6.59 | 89.7 | 1e-12 | 1e-14 | -0.024, 0.090 | NO GAIN |
| F6 | 105.8 | 12 | +1.14 | 3 keys | +2.96 | -1.90 | 31.9 | 0.003 | 2e-4 | -0.056, 0.125 | X-COP FAIL |
| F7 | 3.88 | 10 | +2.11 | 5 keys | -1.10 | -4.06 | 24.3 | 0.05 | 0.03 | -0.025, 0.058 | NO GAIN |
| **F8** | 19.46 | 12 | +0.75 | MID-T3, OUT-M3, OUT-all | +2.75 | -2.01 | 24.6 | 0.035 | 0.007 | -0.035, 0.074 | **IMPROVED** |
| R1 | 1.93 | 9 | +1.52 | 6 keys | +0.14 | -3.41 | 21.2 | 0.068 | 0.08 | +0.001, 0.090 | NO GAIN |
| R2 | 0.87 | 4 | +7.43 | 11 keys | -5.13 | -7.62 | 122.9 | 5e-20 | 1e-27 | +0.023, 0.104 | X-COP FAIL |

Other cells change little: f* 0.0615 drops canonical F1 to 12, F2 to 12, R1 to 9, and alt F6 to 11; alt F1 stays 13; gas 0 matches the primary counts on these rows.

## What the shape does
- **The miss moved; it didn't close.** F1, F6 and F8 bring OUT-all under or near 2 (canonical -1.86, -1.35, -1.46), and each one pushes G-OUT-M3 and MID-T3 up (+2.56, +3.69, +3.47). At k fixed by X-COP, falling faster outward takes mass off the heaviest clusters. That's the same tension as UX3's, in a different place.
- **F1 is the closest and it isn't a clean win.** Its worst key beats F0 by 0.21 canonical and 0.81 alt, but its chi^2 is **worse than F0's on both footings**: +5.6, +4.6 canonical, +1.5, +0.7 alt. Its jack p falls to 0.02, 0.047. What it does win is alt's 13 of 15 against 10, and footing stability: F0 reads 14 and 10, F1 13 and 13.
- **"Fixed multiple of the gas" fails as a rule.** F5, LM1's statement, passes X-COP and reads 6 of 15, M3 -5.2, chi^2 79. The boost's outward fall relative to the gas is doing real work. F4, moving a0, reads 8 of 15.

## Margins, including the near misses the labels don't show
**No row clears 15: 11 forms x 5 k x 2 footings, plus 80 control rows.** The k scan is a look at the keys, not a fit.

| Row, report only | keys | worst Z | X-COP unseen (line 0.05, 0.10) |
|---|---|---|---|
| canonical F6, k x 3 (MUTATE) | 14 | OUT-all -2.10, -2.14, margin +0.14 | -0.433, 0.456 **FAIL** |
| canonical F1, k x 1.3 | 14 | OUT-all -2.13, -2.19, margin +0.19 | -0.120, 0.133 **FAIL**, by 0.070, 0.033 |
| alt F1, k x 1.15 | 14 | margin +0.60 | -0.079, 0.094 **FAIL**, by 0.029; all 7 -0.051, by 0.001 |
| canonical F0, k x 0.85 | 13 | margin +0.52 | +0.003, 0.067 pass |
| canonical F1 fitted | 13 | margin +0.56 | -0.040, 0.066 pass |

- **The closest canonical key row needs k 30 % above what X-COP allows.** Keys and X-COP disagree on F1's level. LF1's HSE bracket makes this worse: taking 0.12 dex off M_HSE lowers X-COP's k, and the keys want it higher.
- **14 of 15 is cheap.** MUTATE F6 at k x 3 reads 14 of 15, worst 2.14 canonical, margin +0.14, joint p 0.49, 0.54; alt 14 of 15, worst 2.67, p 0.50, 0.55. That is the smallest margin in the lane, and X-COP unseen reads -0.433, -0.418, a huge fail. So the count and p say little without X-COP. Likely reason, not tested: x^2 is small in most key clusters, so the keys hardly constrain k there. Z's in `ux7_post.out`; those p from a separate inline read, not stored.

## M500 against gas: NOT SEPARABLE, frozen, both pairs
M_L: eRASS1 L500 through a hydrostatic fit on 82 clusters (S09 10, L15 7, L20 65), lg M = 13.114 + 0.610 lg L + 0.169 lg(1+z), scatter 0.100 dex. No shear enters. Independent of the keys' shear, **not of the gas data**: the same X-ray image.

| Pair | canonical Dchi^2, h 0.672, 0.686 | alt | Forecast F (needs 3) |
|---|---|---|---|
| R1 vs F0 | +2.3 +- 1.5, +1.5 +- 1.5 | +2.7 +- 1.4, +2.2 +- 1.5 | 0.36-0.38 |
| R2 vs F5 | +32.8 +- 5.7, +39.2 +- 6.2 | +33.2 +- 5.5, +39.9 +- 5.9 | 1.37-1.55 |

Positive leans gas. Predictions are held fixed, an approximation.
- **R1 vs F0 can't be decided by these keys,** so GM1's open question stays open. It leans gas by under 2 sigma.
- **R2 vs F5 reads about 6 sigma for gas in Dchi^2, and the frozen label still says NOT SEPARABLE** since F < 3. Both rows fail badly, so that is a comparison of two wrong rules. I don't overrule the label.
- **The keys do see mass ordering:** M_L shuffled among clusters takes R1 from 12 to 4 keys (alt 9 to 5). A term tied to the right ordering works, whether gas or mass; gas and L500 correlate at 0.88.
- Catalogue M500, not independent: R1c 10 of 15, worst 3.90 (alt 9, 4.38); R2c 3 of 15. Worse than M_L, about what a higher level does.
- **K6's failure doesn't rescue the rival.** M_L sits 0.185 dex under X-COP's HSE on the 5 X-COP clusters in eRASS1. Raising it to match acts like k x 1.5; R1 is already worse at k x 1.3 (10 of 15, 3.59). The best scanned R1 is k x 0.7: 12 of 15, 2.67.
- **R1's X-COP mean of +0.001 is partly circular:** its amplitude is X-COP's own HSE M500.
- Post-result pairs in `ux7_read.out`: R1 vs F1 NOT SEPARABLE; R2 vs F7 reads GAS BETTER, no label protection.

## Look-elsewhere
- **8 forms and 2 rivals on a family picked from about 2e9 tries,** found after LM1 and GM1 had shown the ratio, with F0's keys already read and F1, F6, F7, F8 built knowing the direction. **No p here is a discovery p.** A high joint p is a failure to reject, conditional on all that. A plain 10-trial correction applied to F1's alt gain doesn't touch the earlier selection, which can't be corrected for.
- **Control, 40 random shapes x^p u^q S^t:** 1 of 40 passes X-COP and matches the best listed form on canonical, 0 of 40 on alt. So the frozen "not earned" line (0.10) **doesn't fire**. **I don't read that as earned.** 40 draws bound the fraction only under 0.113 and 0.072, and X-COP mostly sets it: only 1 draw in 40 passes X-COP at all.
- **That one draw beats every listed form on canonical's worst key:** p 0.94, q -0.22, t 0.09, 13 keys, |Z| 2.33, joint 0.10. On alt, 13 keys, 2.79, joint 0.11. It is F0 with a slight inward tilt and no meaningful local-gas part, so it does not support F1's physical reading. It's the best of 40, picked after the fact.
- Honest reading: a modest change in radial slope moves keys between OUT-all and M3, and no particular form is earned. "Local gas" is a statement of what was tried, not a finding.

## Checks: 10 of 12. K5 and K6 fail
K1 F0 vs UX3 keys 3e-15. K2 PASS. K3 every form at k 0 equals the law, 0. K4 2e-15. K7 N 82. MUT-X: k x 3 fails X-COP on every form. **MUT k x 3 on keys:** most fall (F0 5, F1 8, R1 3), but **F6 stays 14 and F8 13 on both footings**, as above. MUT-S: shuffled M_L moves keys up to 2.24 (R1), 6.93 (R2).
- **K5 FAILS, 0.305 against 0.02:** my tolerance was wrong. It came from the frozen qd difference, M500 x qd against gas x qd^2.5, and I underestimated it. Scaled as gas, post-result: 0.0008, so the plumbing is right. **The R1 and R2 rows carry that frozen scaling, which moves Z by up to 0.3 at k c = 10, h 0.672. It changes no label's reach:** no R1 row in the scan gets within 0.67 of the line.
- **K6 FAILS,** -0.185 dex, on 5 clusters; see above.

Rerun byte-identical, full chain, all 9 compared files: masses, fits, keys, read. `ux7_grade.py` gained the POST_k5 run between the two passes; default rows unchanged.

## Errors, disclosed
K5's row first had k 1 where 10 was meant; fixed before any row ran. `ux7_post.py`, the k5 diagnosis and the F6 p are post-result. The scan's k x 1.3 X-COP numbers are also post-result. No label was moved.

## Expectation against result
Any PASS 7 %: no. NEAR MISS on canonical 35 %: no. F1, F6 or F8 best 60 %: alt yes, canonical's rank says F0. F5, F7 hurt 60 %: F5 badly, F7 on OUT-all. Alt still worse on all 65 %: **wrong**, F1, F6, F8 read better on alt. NOT SEPARABLE 65 %: yes. Control at or above 0.10, 50 %: no, weakly.

## Limits, unfinished
No field equation. Bullet not tested here. X-COP hydrostatic. Keys are KiDS; HSC's disagreement unresolved. Stars are a constant share in the grader, so F3 differs from F0 only through k. M_L carries HSE bias and no Malmquist correction. Temperature mass not run: KT on 106 of 326, median error 0.75. **Needed, not on disk:** an independent mass on all 326 not from the X-ray image, or pointed gas with lensing at Mg near 1e15, to separate gas from M500.

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.
