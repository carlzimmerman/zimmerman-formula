# M3A1_outer_key_audit: PARTLY as frozen, and the wall stands. One measured effect, per-tile PSF leakage, reaches a third of the need in one cell of four. All measured effects together leave G-OUT-M3 at +3.55 to +3.99

Criteria: `FROZEN_CRITERIA.md` (78a75e92c9, committed alone first; Amendment A1 before any verdict and before the extended randoms were read). `m3a1_prep.py`, `m3a1_randoms.py`, `m3a1_grade.py`, `m3a1_audit.py`; numbers in `m3a1.out`, `m3a1_results.json`, `m3a1_prep.out`, `m3a1_jobs.out`. kappa = 1/2 FITTED; cold dark energy, no particle; not theory closed. Nothing here says the data favour the framework. Not blind. A data-side audit, no new mechanism, no new data. No rule passes here.

Baseline reproduced exactly: ZN4's 15 keys at gas +0.005, |d Z| 0, G-OUT-M3 +4.41, +4.07, +4.13, +3.81 (f* 0.034 h 0.672, 0.686; f* 0.0615 h 0.672, 0.686; this order below). Reach = (Z_base - Z)/(Z_base - 2).

## Measured effects, which enter the net
| id | effect | size | G-OUT-M3 | reach |
|---|---|---|---|---|
| C1a | Eddington: bin cut on the same noisy MGAS500 the prediction uses | M3 mean -0.018 dex (median error 0.069 dex) | +4.64 +4.29 +4.37 +4.04 | **-0.13 to -0.10, worse** |
| C2a | pointed gas in M3's window, cut on eRASS1 gas | +0.016 +- 0.007 (N 89), not +0.005 | +4.14 +3.82 +3.85 +3.54 | +0.11 to +0.15 |
| C4a | M3's own boost | B 0.946-0.950 against 0.950-0.955 | +4.36 +4.04 +4.08 +3.77 | +0.02 |
| C4c | SOM bin n(z) in Sigma_crit, F 1.09-1.15 at M3's z (F1 calls it a bound) | data up 11 % | +5.19 +4.83 +4.94 +4.59 | **-0.43 to -0.33, worse** |
| C4d | 6,499 extended randoms in place of F1's 5-6 per cluster | level -0.027 against F1's -0.080 (h 0.672) | +3.96 +3.80 +3.68 +3.54 | +0.13 to +0.21 |
| C4e | X7's per-tile PSF leakage on this template | +0.079, +0.083 in A | +3.73 +3.39 +3.46 +3.12 | **+0.28 to +0.38** |

Net, all as frozen: **+3.99 +3.80 +3.73 +3.55**. Without C2a, which overlaps C1a: +4.26 +4.06 +4.01 +3.82. Without C4c: +3.20 +3.04 +2.92 +2.78. Lowering effects only, not graded: +2.97 +2.82 +2.68 +2.55. **Even that doesn't reach 2.**

The PARTLY rests on C4e alone, at 0.38 in the easiest cell and 0.28 in the headline cell. X7 labelled that regression a bracket, and it overlaps C4d: per-cluster correlation of about +0.2 with the F1 random term. PSF columns aren't in the cache used here, so the overlap isn't removed, and the lowering sum double counts somewhat. My expectation had C4d at 25-40 % and leakage below a third; both were wrong.

## Reported, not counted
- **Miscentring doesn't matter at 1.42-3 Mpc:** offsets x 0 and x 2 give +4.40 and +4.44. It moves G-MID-T3 more (+2.12, +2.32).
- **B = 1:** +4.83, worse. No subtraction at all: +3.73.
- **m:** no table read here; a provisional 2 % ceiling is 0.26 in Z, reach 0.11.
- **Null levels:** A_x +0.087, A_RR -0.001 at h 0.672; +0.042, -0.009 at h 0.686. Not large against s 0.12.

## Is +4.41 stat-only? Yes
s is X7's s_CAL, equal to s_STAT: the leakage, cross and R-R terms round to 0. No model, gas or calibration error is in it. In quadrature with gas 0.021, slope 0.007, seed 0.009, m 0.031, n(z) 0.011, leakage 0.079, s goes 0.118 to 0.148: **Z_tot +3.51 +3.24 +3.29 +3.03.** It stays significant with no shift applied.

## Stability
- Own bootstrap and jackknife of A - pred: +4.33, +4.53 (grader +4.41). Bootstrap P(A - pred <= 2 s) 0.008.
- Leave one out +4.21 to +4.67; leave one sky patch +4.17 to +4.70. Drop the top 1, 3, 5, 10 by contribution: +4.21, +3.89, +3.59, +2.85. So not [FEW-CLUSTER]. 10 % trimmed: +5.75.
- N +3.61, S +2.69; z low +3.30, z high +3.28: no one half carries it.
- Joint chi^2 for ZN4 on measured gas: **35.9-38.2 for 15 at f* 0.034, p 0.002-0.0009; 31.9-34.2 at f* 0.0615, p 0.007-0.003. JOINT FAIL on BA1's line, all 4 cells.** Jackknife R is harsher, p to 2e-6. Without G-OUT-M3: p 0.011-0.0016 at f* 0.034, 0.028-0.005 at f* 0.0615, so more than this key is off.

## Where it lives (post-result, h 0.672, f* 0.034, own bootstrap)
| split | A | pred | Z |
|---|---|---|---|
| bin 1.42-2.06 Mpc | 1.48 | 1.23 | +1.72 |
| **bin 2.06-3 Mpc** | **1.61** | **0.93** | **+4.41** |
| M3's heavier half | 1.50 | 1.22 | +1.81 |
| **M3's lighter half** | **1.63** | **0.85** | **+4.61** |

The miss sits in the outermost bin and the lighter half: the signal stays flat in A while the prediction falls. This wasn't frozen and proves nothing. It says the place to look is the model's shape near its outer edge at those radii, or real signal beyond it (DR6 says the two-halo term is too small), and not the sample as a whole. Cutting the bin wouldn't be a pass.

## Other keys
- **G-MID-T3 is close to the line and isn't a separate wall:** under C4d it goes +2.17 to +1.70, +2.54 to +2.03 at f* 0.034; C2a takes +2.17 to +2.06.
- **G-OUT-Mall:** +3.36 to +2.99, +3.64 to +3.42 under C4d.
- **G-OUT-M2 goes the other way:** +1.90 to +2.20, +1.99 to +2.26, so extended randoms push it over 2.

## Limits
1. C1a uses tabulated errors as Gaussian in dex. M1's tail makes its all-326 version nonsense (shifts to +4.26 dex, G-OUT-Mall -155), so Mall reads from C1a_M3. M3's Z depends only on M3. Tweedie is a mean correction; a forward noise simulation gives a much larger -0.14, unreliable because M1's huge errors flood the top tercile. Cap at 0.2 dex: +4.63.
2. C2a's window has median lg Mg 13.86, against M3's 13.47; below M3's median N is 10, +0.007 +- 0.031. Only 4 clusters are in M3 itself, -0.042 +- 0.023. Pointed samples are X-ray bright, and a shared pointed bias wouldn't show.
3. C4c is a bound, not a calibration, and it dominates the raising side.
4. Shifts add linearly. Additive ones use the grader's s; multiplicative ones keep its fractional s.
5. C4e is X7's stored stack on F1's randoms, not refit.
6. Intrinsic scatter in gas fraction at fixed gas would add to C1a in the same direction. It isn't measured here.

## Checks
K1 |d Z| 0, preds 0. K2 own sums 0. K3 Draw, Rmean on F1's seed 2e-13, 4e-14; Draw on all M3 3e-13. K4 X11's field levels |d| below 1e-5 on X11's scale, 6,499 accepted, same draws. K5 Tweedie synthetic ratio 0.93. K6 6e-15. MUTATE (a) C1a +0.23, flipped -0.28, BITES; (b) e2 flipped, K3 FAILS as required; (c) shuffled membership +1.64 against +4.33, BITES; (d) excess removed |Z| 0.000. GS4's +0.005 +- 0.017, N 45 reproduced in `m3a1_prep.out`. Audit rerun byte-identical.
