# LAM4: does one whole-galaxy absorption spectrum read spin?

Criteria `1023fbaae9` (frozen first), amendment A1 `90c548c6cf` (K2 noise scaled by sqrt(chi2), before results).
Sample, scripts and grader committed before any grade. kappa = 1/2 FITTED; not theory closed.

**LABEL: WHOLE-GALAXY SPECTRUM READS SPIN (SHAPE BEYOND WIDTH, BEATS THE FIBRE).** PRECISE not earned (E1 fails).

## What was done
1000 gas-poor MaNGA galaxies from LAM2's graded set (all 396 slow rotators + 604 random fast, seed 20261103).
Each DR17 LOGCUBE was streamed, summed inside the half-light ellipse (Re, Eps_MGE, PA_phot), and deleted
(`lam4_stream.py`). Each sum was fitted once with pPXF + E-MILES, moments 6 (`lam4_fit.py`; 1000/1000 ok,
median S/N 108, chi2 2.6). The lambda_R labels (DynPop) were joined only in `lam4_grade.py`.

## Checks
| check | result | bar |
|---|---|---|
| K1 sigma_int vs Sigma_Re | median -0.005 dex, rms 0.027 | |median| <= 0.03, rms <= 0.06: PASS |
| K2 h4 recovery, 200 synthetics | rms 0.021, bias -0.0002, slope 0.86 | <= 0.03: PASS |
| M1 h4/h6 shuffled in mass x sigma x eps cells | S4_mut - B4 +0.0075 | within +-0.02: PASS |
| DRYRUN labels permuted (code test, not kept) | every gate -0.005 to -0.008 | null as expected |

The DRYRUN printed the real K1, since sigma is not permuted; it is disclosed here as in LAM2 A3.

## Grade (5-fold CV AUC for slow vs fast, paired bootstrap 95 %)
| model | inputs | AUC |
|---|---|---|
| B0 | log M*, u-r, n, eps, log Re | 0.793 |
| B4 | B0 + log sigma_int | 0.784 |
| SF | LAM2 fibre shape model | 0.817 |
| S4 | B4 + h4_int, h6_int | **0.878** |

- G1 S4 - B0 **+0.085** [+0.065, +0.105], bar 0.05: PASS
- G2 S4 - B4 **+0.094** [+0.073, +0.115], bar 0.03: PASS
- G3 S4 - SF **+0.061** [+0.043, +0.078], bar 0.03: PASS
- E1 rms(S4) 0.157 vs 0.10: FAIL. E2 purity (reweighted to 0.168) 0.706 vs 0.70: PASS

Ungraded rows: the gain grows with mass (S4 - B0 +0.07, +0.14, +0.21 by log M* tercile). h4_int median is
+0.041 for slow and -0.018 for fast; Spearman(h4_int, lambda_Re) is -0.78, against -0.39 for the fibre h4 on the
same galaxies. The split holds in every S/N tercile (slow +0.040 to +0.043, fast -0.010 to -0.023). 63 % of fast
rotators have h4_int < 0, against 9 % of slow ones.

## Reading
Rotation inside the half-light ellipse smears the summed line profile into a flat top (negative h4); a pressure-
supported galaxy keeps a peaked one (positive h4). One integrated absorption spectrum therefore carries the spin
class, much better than its width or the 3" fibre does. This is an estimator result: the same MaNGA photons give
lambda_Re, summed instead of mapped. It says nothing about gravity or the a0 law; the direct spin-law test is KU2
(UNIVERSAL). The estimator is a classifier (E2 passes), not a precise lambda_R meter (E1 fails).

Files: `lam4_sample.csv`, `lam4_fit.jsonl`, `lam4_k2.*`, `lam4_grade.*`, `lam4_grade_MUTATE.*`.
Data (not in repo): `_external_data/lam4_integrated_2026_11_03/` (1000 integrated spectra, cubes deleted).
