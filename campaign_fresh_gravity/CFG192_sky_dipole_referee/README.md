# CFG192 — independent referee re-derivation of CFG182 (is SPARC's acceleration scale different in different directions on the sky?)

Frozen criteria: `CFG192_FROZEN_CRITERIA.md` (sha256 d3a9f7cf..., committed before any script as "CFG192: frozen criteria"). Phase 2 order kept: my own profile curves, main run and the seven MUTATE runs were saved first; only then were CFG182's `.out`, `.json` and the relevant parts of its `.py` opened, and `CFG192_compare.py` written. Nothing in the repo was edited; every output is in this directory. kappa = 1/2 stays FITTED and a0 is fitted here, so kappa enters nothing. Nothing below says the data favour or disfavour the framework's directional flow.

## Bottom line

**The CFG182 headline reproduces with independent code, to the third digit.** 149 galaxies and 3150 points; best dipole A = 0.237 toward (l, b) = (239.1, -45.7) (CFG182: 0.238 toward (237.2, -44.2), 2.0 deg apart); permutation p = 0.771 simple / 0.756 block (0.772 / 0.774); S1, S2 and S3 all fail; my Neyman limit is A95 = 0.40 (0.425). The verdict is **NULL**. The frozen class printed by `CFG192_main.py` is **PARTIAL**, for exactly one row (section 1): my first-read definition of "sigma_A" (the standard deviation of the bootstrap amplitude, 0.161) misses CFG182's 0.201 by more than the frozen 0.03; CFG182's own definition (the bootstrap spread along the fitted direction) gives **0.2008** in my code. I keep the coded class and label the row a definition difference.

**Agreement measures the implementation, not the design.** The design (priors, Birge scaling, grid, kernel, permutation scheme, pass lines) is shared with CFG182 by construction, so a near-identical answer is expected from any correct code. The attacks are where the design is tested, and they find three things CFG182's README does not say (sections 3-6): (1) the NULL does not survive every nuisance treatment at the 0.05 level, (2) the recovery of an injected dipole is about 0.9-1.0 in my pipeline and direction-dependent (0.71-1.09), not a systematic 0.77 caused by the multiplicative form, and (3) the bootstrap error does not shrink when the nuisances are fixed, so the README's "5x larger errors because distance and inclination are marginalised" is not reproduced.

## Where independence stops (shared elements)

Own code (no repo import): loader, Equatorial-to-Galactic conversion, the baryonic model, the per-galaxy profile engine, Birge scaling, the dipole fit (analytic gradient, five starts), permutations, bootstrap, Neyman construction, hemisphere scan, splits, injections, all attacks. The repo enters only as data files.

Shared, not tested by me: (1) the data files (rotmod curves, `SPARC_Lelli2016c.mrt`, the VizieR position table); (2) the frozen design: LML-2018 priors (0.1 dex Y_d and Y_b, Gaussian D and Inc), the Birge factor max(1, chi2_min/(N-1)), the grid -11.3 to -9.0 step 0.01, |D| <= 0.95, the permutation schemes, the pass lines; (3) the kernel definition nu_mono (FP1): my implementation from the definition agrees with the repo's to a maximum relative difference of 0.0 over y = 1e-8 to 1e4 (`CFG192_compare.out`); (4) the published papers, known only through CFG182's abstract-level numbers. Cross-checks that could be made from inside the repo all pass: my (l, b) agree with `sparc_cosmicweb_match.csv` to 0.028 deg at most (165 galaxies); the rotmod-header distances equal the master-table distances (0 mismatches); the Galactic centre and the north Galactic pole convert to (0, 0) and b = 90.

Declared choices I made where the frozen text was silent (all before seeing results): Birge chi2 includes the prior terms; inclination bounds 5-90 deg; block permutation over 124 units; a 3072-point Fibonacci sphere instead of HEALPix for the hemisphere scan; cubic-spline curves with linear edge extrapolation. One definition I chose before running but did not record in the frozen file: "bootstrap sigma_A" = std of the bootstrapped amplitude (this is the row that misses; see above).

## Verdict per frozen pass line (section 4 of the criteria)

| pass line | mine | CFG182 | verdict |
|---|---|---|---|
| sample count exact (149; 3150 points; 81/37/3/2/26) | 149; 3150; 81/37/3/2/26 | same | REPRODUCES |
| A-hat within 0.03 | 0.237 | 0.238 | REPRODUCES |
| direction within 15 deg | (239.1, -45.7), 2.0 deg apart | (237.2, -44.2) | REPRODUCES |
| p (larger of simple/block) within 0.05 | 0.771 (simple 0.771, block 0.756) | 0.774 | REPRODUCES |
| verdict NULL with S1, S2, S3 each FAIL | S1 p = 0.771; S2 p = 0.067, z = -0.97 / +1.57; S3 axis 50.9 deg vs cone 115 deg | p = 0.108, -0.76 / +1.41; 52.9 vs 115.4 | REPRODUCES (each fails for the same reason) |
| a-bar0 within 5% | 1.129e-10 | 1.132e-10 | REPRODUCES |
| bootstrap sigma_A within 0.03 | 0.161 (std of amplitude) / **0.2008 along the fitted direction** / 0.198 rms component | 0.2013 | **MISS as coded; REPRODUCES under CFG182's definition** |
| null median / 95% within 0.03 / 0.05 | 0.348 / 0.647 | 0.339 / 0.615 | REPRODUCES (my null tail is 2.4 sigma(MC) higher at the median, 5% at 95%; p unaffected) |
| A95 within 0.06 | 0.400 (simple mean of 3 seeds), 0.408 (block); worst of 6 runs 0.425; finer grid 0.3875 | 0.425 / 0.375 | REPRODUCES |
| **class of `CFG192_main.py`** | **PARTIAL** (one row, a definition) | | see above |

## 1. Row-by-row comparison with CFG182 (`CFG192_compare.out`; 65 rows, 62 within tolerance)

Class of a difference: **definition** (different but legitimate reading), **numerical** (interpolation/optimiser/Monte Carlo), **typo** (README misstates its own output), **framing** (the number agrees; the reading does not).

| row | mine | CFG182 | class |
|---|---|---|---|
| N, points | 149, 3150 | 149, 3150 | identical |
| a-bar0 no dipole | 1.1289e-10 | 1.1317e-10 | numerical (0.2%) |
| Birge median | 1.718 | 1.72 | identical |
| median Delta chi2 = 1 half-width | 0.243 dex | 0.264 | **definition** (CFG182 averages the two sides of the first crossing, caps at 1 dex; mine is (right - left)/2) |
| footprint \|<n>\| | 0.5985 toward (142, 54), 117 at b > 0 | 0.599 toward (142.2, 54.5), 117 | identical |
| best dipole | 0.2371 toward (239.1, -45.7) | 0.2380 toward (237.2, -44.2) | numerical (2 deg) |
| Delta chi2 (3 par) | 10.49 | 10.27 | numerical (spline vs Catmull-Rom interpolation) |
| Fisher sigma_A; best / least-constrained | 0.081; 0.0455 / 0.1057 | 0.0822; 0.0456 / 0.1058 | identical; the least-constrained axis is 0.5 deg from theirs |
| bootstrap sigma of D_x, D_y, D_z | 0.227, 0.196, 0.169 | 0.225, 0.197, 0.166 | identical |
| README "sigma_A = 0.201" | 0.2008 as sqrt(d^T Sigma d) | 0.2013 | **typo-level**: the README calls it "A = 0.24 +/- 0.20"; the number is the spread of the bootstrap D along the fitted direction, not of the amplitude (0.161) |
| cones 68% / 95% | 58 / 115 deg | 59 / 115 | identical |
| permutation p simple / block | 0.771 / 0.756 | 0.772 / 0.774 | numerical / **definition** (CFG182 compares the block null with its own A_obs = 0.231, UMa members collapsed to their mean position) |
| null A-hat median / 95% / 99.7% | 0.348 / 0.647 / 0.925 | 0.339 / 0.615 / 0.849 | numerical (mine higher by 2-9%, unexplained at that level, no effect on p) |
| A_fix +/- sigma: CMB, bulk, Chang, Zhou, Virgo, UMa | -0.071 +/- 0.145, +0.014 +/- 0.180, +0.107 +/- 0.220, +0.058 +/- 0.237, -0.106 +/- 0.144, -0.146 +/- 0.163 | -0.068 +/- 0.155, +0.014 +/- 0.175, +0.110 +/- 0.226, +0.066 +/- 0.237, -0.102 +/- 0.151, -0.141 +/- 0.170 | identical within Monte Carlo (500 vs 1000 resamples) |
| hemisphere H_max, direction | 0.604 toward (303, 6), p = 0.25 | 0.595 toward (295, 5), p = 0.24 | **definition** (Fibonacci vs HEALPix axes) |
| H at the Zhou axis | +0.111 +/- 0.224 | +0.146 +/- 0.216 | **definition** (exact axis vs a pixel) |
| distance split: H, I | H: 0.474 toward (263, 48); I: 0.428 toward (183, -61); p = 0.067; z -0.97 / +1.57 | 0.468 (259, 46); 0.403 (183, -62); p = 0.108; -0.76 / +1.41 | numerical (bootstrap covariances); UMa: mine 0.950 (bound) vs 1.213, **definition** (CFG182's subsample fit is not bounded at 0.95) |
| inclination split | p = 0.379 | 0.423 | **definition** (mine puts Inc = 63 exactly in the low half, theirs in the high half) |
| footprint alignment | axis 50.9 deg, cone 115 | 52.9, 115.4 | identical |
| PV template | 238 km/s, Delta chi2 11.4, p = 0.61 | 209 km/s, 12.2, 0.58 | numerical |
| distance trend | beta = +0.062 | +0.047 | numerical |
| variants: no Birge; all 171 | 0.584, p = 0.153; 0.306, p = 0.603 | 0.605, 0.120; 0.308, 0.587 | numerical |
| kernel P2, simple variants | not run | 0.228 / 0.215 | not in my frozen attacks |
| A95 (simple / block) | 0.400 / 0.408 (3 seeds each, 1000 trials); finer grid 0.3875 | 0.425 / 0.375 (300 trials) | numerical (MC +/- 0.025) |
| recovered <A-hat> at A_inj = 0.1, 0.2, 0.3, 0.5 | 0.367, 0.411, 0.445, 0.580 | 0.372, 0.391, 0.454, 0.590 | identical |
| median direction error at 0.2, 0.3, 0.5 | 53, 42, 27 deg | 55, 41, 26 | identical |
| their MUTATE (A = 0.20 toward (114.6, -41.9), a0ref = 1.2e-10, point level) | change 0.152, 22.3 deg | 0.151, 22 deg | identical (same recipe, own code) |
| post hoc: Hubble-flow subsample toward the CMB dipole | dipole 0.474 toward (263, 48), **1.2 deg** from the CMB dipole; amplitude along it +0.473 | 4 deg; +0.47 +/- 0.23 | reproduced (still a post hoc direction) |

Not reproduced because outside my frozen scope: the point-level generative Gaussian null (their part C: reduced chi2 0.68 vs 4.20, p = 0.010), the secondary per-galaxy table (`cfg182_d`), the orientation-quadrupole reading, the kernel variants.

**Where the README's wording goes beyond the numbers (framing).** "Errors are about 5x theirs because it marginalises distance and inclination" (section 5 below): not reproduced. "The recovery falls short (about 0.77) because the multiplicative form is fitted to over-dispersed values" (section 4): not reproduced.

## 2. MUTATE controls (exit 1 when the control bites), failed controls kept

| control | result | bites |
|---|---|---|
| M1 point-level injection A = 0.50 toward (seed 19211 direction) | change vector 0.414 (recovery 0.83), 16.7 deg from the injection, permutation p (N = 2000) = **0.095** | **NO** (amplitude and angle legs pass; the p < 0.05 leg fails: I expected p about 0.2-0.5, it came out smaller at 0.095 but still above the line). Kept as failed |
| M2 injection A = 0.20, same direction | change 0.183 (recovery 0.92), 16.7 deg; p = 0.41 (reported) | yes |
| M3 injection A = 0.50, positions shuffled in the fit | component along the injection +0.046; A-hat within 0.09 of the null median | yes |
| M4 no nuisance profiling | median half-width 0.243 -> 0.041 dex (5.9x); Fisher sigma_A 0.078 -> 0.012 (6.6x) | yes |
| M5 antipodal sign in the fit | change vector 16.7 deg from the antipode of the injection | yes |
| M6 Newtonian kernel | median Birge factor 1.72 -> 13.2 (7.7x) | yes |
| M7 A = 0 injection | data unchanged (max \|dV\| = 0) | no (as designed) |

## 3. Attack A: the clean-sample definition and leave-out sensitivity

**153 versus 149, plain answer.** The cuts Q <= 2 and Inc >= 30 give **153** galaxies in the master table (my phase-1 awk count, before any script). The four that drop out are **D512-2, NGC6789, UGC00634, UGC07232**: each has **only 4 rows in its rotmod file**, so they fail the frozen "at least 5 usable points" requirement (2 Hubble-flow, 2 TRGB, exactly the 81/37/3/2/26 breakdown that 149 requires). The same four are the only usable-sample losses (175 -> 171). The cut was not tuned: I predicted this in the frozen criteria before running, and it holds. I did not run the alternative ">= 4 points" sample.

Sample ladder (Birge scaling, profiled LML curves, 1000 permutations, 500 bootstraps; `CFG192_attacks_AB.out`):

| sample | N | A-hat toward | p_perm |
|---|---|---|---|
| primary | 149 | 0.237 (239, -46) | 0.80 |
| Q = 1 only, Inc >= 30 | 93 | 0.347 (282, -46) | 0.50 |
| Inc >= 45 / Inc >= 60 | 126 / 87 | 0.291 / 0.360 | 0.68 / 0.67 |
| Q <= 2, no Inc cut | 159 | 0.244 | 0.75 |
| all usable | 171 | 0.306 (256, -43) | 0.60 |
| >= 10 points | 115 | 0.146 | 0.93 |
| drop UMa / drop Hubble-flow / drop TRGB-Cepheid-SNIa | 123 / 68 / 107 | 0.218 / 0.421 / 0.419 | 0.84 / 0.68 / 0.54 |
| drop bulge galaxies | 118 | 0.335 (250, +4) | 0.63 |
| \|b\| > 10 | 148 | 0.263 | 0.70 |

**No cell has p < 0.01 (smallest 0.50): the NULL is robust across the ladder.** The direction moves by more than 90 degrees across cells (expected for a 59-degree 68% cone). Jackknife: the largest single-galaxy shift of D-hat is **0.176 (NGC2915)**, then NGC6503 0.121, NGC7814 0.115, UGCA444 0.109, NGC0891 0.094; my hand estimate ("below 0.10") was wrong. Removing the 10 most influential galaxies gives A = 0.41, p = 0.25; removing the 10 largest-|pull| gives 0.23, p = 0.61 (24 galaxies have |pull| > 3 with curve widths only). Removing each of 12 equal-area sky sectors: A from 0.17 to 0.41, p from 0.40 to 0.96.

## 4. Attack C: footprint response and injected dipoles A = 0.1, 0.2, 0.3, 0.5 (`CFG192_attacks_CD.out`)

Footprint: |<n>| = 0.60 toward (142, 54); 117 of 149 galaxies at b > 0. The Fisher covariance has sigma = 0.046 / 0.071 / 0.106 along its axes (analytic, weighted-footprint: 0.045 / 0.086 / 0.099). The least-constrained direction is (192, -8) (axis (12, 8)), **75 deg from the footprint axis** — my hand estimate (within 30 deg) was wrong. The fit's monopole and the dipole along the footprint vector are correlated at rho = -0.81. Best/worst direction sigma ratio 2.2 (analytic), 2.3 (numerical).

Curve-level injection on position-permuted real curves (N = 1000 per A; zero-injection control N = 5000, whose A-hat has median 0.346 and 95% / 99.7% thresholds 0.653 / 0.937):

| A_inj | mean A-hat | recovery ratio | median angle | 68% angle | power, A-hat > 95% thr. | nested power p < 0.05 (200 mocks x 499 perms) | power at S1-like 99.7% thr. |
|---|---|---|---|---|---|---|---|
| 0.1 | 0.367 | 0.88 | 72 deg | 92 deg | 0.051 | **0.040** | 0.004 |
| 0.2 | 0.411 | 1.00 | 53 | 71 | 0.087 | **0.090** | 0.011 |
| 0.3 | 0.445 | 0.96 | 42 | 55 | 0.107 | **0.090** | 0.004 |
| 0.5 | 0.580 | 0.98 | 27 | 35 | 0.341 | **0.290** | 0.023 |

**Detection power, plain answer:** 4%, 9%, 9% and 29% at A = 0.1, 0.2, 0.3, 0.5 (p < 0.05, look-elsewhere included); at the frozen S1 line (p < 0.003) at most 2%. The README's "SPARC cannot see a sky dipole below about 40%" is **confirmed** (power 0.09 at 0.3 and 0.29 at 0.5; frozen rule: < 0.5 and > 0.2). Synthetic Gaussian mock skies (C6, real widths, tau = 0.34 dex) give the same picture (power 0.05 / 0.07 / 0.09 / 0.20).

**Recovery: the README's 0.77 is not a systematic.** On the real sky the change of the fitted vector recovers 0.95 of the injection (curve level, all A) and 0.91 at the point level (mean of four directions: 1.09, 0.89, 0.71, 0.94); position-permuted base 0.96. Matching injection and fit forms gives 0.98 (multiplicative) and 1.00 (log-linear): **no form attenuation**. With CFG182's own injection (direction (114.6, -41.9), a0ref = 1.2e-10) my code returns exactly their 0.152 and 22 deg, i.e. 0.76: a low draw within the direction-to-direction range 0.71-1.09, not a general attenuation. Wrong expectation kept: I predicted 0.75 +/- 0.10; the frozen window [0.6, 0.95] is exceeded by the mean 0.958.

**Footprint sensitivity** (fixed directions, N = 500): recovery 0.88-1.07 across eight directions; power at A = 0.5 ranges from 0.20 (footprint antipode, south pole) to 0.43 (footprint axis): power differs by 2.2x, so by the frozen rule the estimator **is footprint-sensitive** in power, not in recovery.

## 5. Attack B: the nuisance profiling (`CFG192_attacks_AB.out`; 1000 permutations, step 0.02 for rebuilds)

Does the NULL hold with fixed and with looser priors? **Fixed: yes, but the direction and size change.** **Looser: yes.**

| treatment | A-hat toward | p_perm | median half-width | Fisher / bootstrap sigma |
|---|---|---|---|---|
| primary (step 0.02) | 0.237 (239, -46) | 0.76 | 0.243 dex | 0.078 / 0.192 |
| **fixed nuisances** (Birge) | **0.480 (193, +2)** | 0.23 | 0.041 | 0.012 / 0.209 |
| fixed, Birge off | 0.717 (170, -6) | 0.091 | | 0.005 / 0.201 |
| **profile Y only** (D, Inc fixed) | **0.724 (184, -1)** | **0.022** | 0.085 | 0.023 / 0.182 |
| profile D and Inc only | 0.382 (250, -26) | 0.63 | 0.184 | |
| Y sigma 0.2 dex / 0.3 dex | 0.308 / 0.336 | 0.56 / 0.51 | 0.258 / 0.278 | |
| D, Inc sigma x2 | 0.243 (267, -55) | 0.86 | 0.302 | |
| all looser (Y 0.2, D/Inc x2) | 0.398 | 0.54 | 0.352 | |
| Y sigma 0.05 dex (tighter) | 0.277 | 0.77 | 0.210 | |
| e_V x sin(i)/sin(i') | 0.352 | 0.62 | 0.219 | |
| Birge off / velocity-only / dof N / cap 3 (primary curves) | 0.584 / 0.224 / 0.234 / 0.426 | 0.15 / 0.80 / 0.78 / 0.36 | | |
| simple per-galaxy fit + regression: weighted / unweighted | 0.268 (191, -10) / 0.418 (267, -26) | 0.58 / 0.11 | | 0.012 / 0.131 |
| random-effects likelihood (fitted tau = 0.33 dex) | 0.469 (263, -16), LR = 6.7 | 0.093 | | |

**Frozen rule: "NULL SURVIVES iff p > 0.05 in every cell" is FALSE**, because of one cell (profile Y only, p = 0.022, look-elsewhere over 21 cells not accounted for); no cell has p < 0.01, so "nuisance-dependent" is not triggered. Wrong expectations kept: the random-effects amplitude (0.469) is not within 0.10 of the Birge fit (0.237).

**The "5x larger errors than the published" claim: not reproduced.** The frozen literal rule reads CONFIRMED (fixed-nuisance Fisher 0.012 vs profiled bootstrap 0.192) but compares two different kinds of error. Like for like, the bootstrap sigma is 0.209 with fixed nuisances and 0.192 profiled (ratio 0.92): fixing the nuisances does not shrink the honest error. What separates a published +/-0.04 from 0.2 is the between-galaxy scatter of best-fit a0 (0.39 dex against 0.24-dex profile widths; my random-effects tau = 0.33 dex): a curvature error that ignores it is 16x too small (0.012). Whether the published errors are curvature errors cannot be tested from repo files.

Diagnostics (B8): best log a0 is uncorrelated with log D (Spearman 0.00) but correlates with Inc (+0.24, p = 0.003) and with the fitted nuisance pulls (Y_d -0.36, D -0.58, i -0.52); 31% of galaxies pull Y_d by more than 2 sigma; the a0-D' degeneracy is only partly expressed (median d ln D'/d log a0 = -0.61 against -1.15 for full degeneracy).

## 6. Attack D: the 95% upper limit

My Neyman construction (definition as frozen; 1000 trials per cell, 3 seeds, both schemes): **A95 = 0.400 simple, 0.408 block** (worst run 0.425; finer grid 0.3875); the observed A-hat = 0.237 is the p = 0.77 point of the A_inj = 0 cell. A hand check with a Maxwell null (sigma 0.225) gives 0.436. Alternative definitions: likelihood-ratio ordering 0.400; bootstrap one-sided A-hat + 1.645 sigma 0.51 (std) / 0.57 (rms); spread 0.04 across Neyman / LR / Maxwell and 0.11 including the bootstrap-percentile version (a different, looser kind of limit); below the frozen 0.15, so not definition-dependent.

**Does the Neyman limit cover?** Yes. Each mock's own A95 (from the reference table) is at least the true amplitude in **0.938, 0.971, 0.954, 0.961** of mocks at A_true = 0.1, 0.2, 0.3, 0.5 (random directions; the 0.938 cell sits just under 0.95 but above the frozen 0.93), and in 0.96-0.99 for the footprint axis, its antipode, the south Galactic pole and the CMB direction at A_true = 0.3 and 0.5. **Caveat for direction-specific intervals:** the interval A_fix +/- 1.96 sigma_obs covers only 0.968 (Virgo), 0.974 (CMB), 0.930 (Chang), 0.910 (bulk) and **0.884 (Zhou)** of injected 0.3 dipoles along those directions (sigma held at its observed bootstrap value), so the quoted 95% ends along named directions are slightly anti-conservative. The limit is also **conditional on the real 0.34-dex scatter being noise**: if part of it were a dipole-like systematic, the limit would be wrong in sign.

## 7. Is S3 independent of S1?

**No.** S3 passes only if the footprint axis lies outside the 95% bootstrap cone. A footprint axis is an axis, so its angle to any direction is at most 90 degrees; the observed cone radius is 115 degrees, so S3 fails for **every** possible fitted direction. The cone shrinks below 90 only when the dipole is strongly detected, which is S1's job. So S3 is not an independent check. The cone-free statistic I added asks instead whether the fitted axis is more aligned with the footprint axis than a permuted one: 28% of permuted fits are at least as aligned as the observed 50.9 degrees (median null angle 64.5 deg), so the fit is **not** unusually aligned with the footprint. (My frozen criteria flagged this in advance.)

## 8. The two published claims: what can and cannot be said (`CFG192_attacks_E.out`)

Only repo files exist here; the papers' selection, distance handling, estimator and error model are unknown to me and their numbers reach me through CFG182's abstract-level text. Nothing below tests the papers.

- **README verdict "neither confirmed nor excluded": reproduced.** Along Chang's direction A_fix = +0.107 +/- 0.242, so 0.25 lies well inside the 95% interval; H at Zhou's axis = +0.111 +/- 0.224, so 0.37 is inside; injecting 0.25 along Chang's direction is detected (free dipole above the 95% threshold) with power 0.15, and 0.37 along Zhou's axis with power 0.27 (fixed-direction detection at 1.645 sigma: 0.35 and 0.46), i.e. this pipeline could not confirm a published-size dipole even if it were real.
- **Reachability (frozen rule): no variant reaches both A_fix(Chang) in [0.20, 0.30] and a bootstrap sigma <= 0.06** (smallest bootstrap sigma 0.194). The Fisher error of the fixed-nuisance fits is 0.004-0.013, below the published 0.04, but their A_fix is not in the frozen window (0.32 and 0.62).
- **Post hoc, not frozen: a fixed-nuisance fit points where the published claims point.** With nuisances fixed and no Birge scaling, the free dipole is A = 0.72 toward (170, -6): **9.5 degrees from Chang's direction and 5.5 degrees from Zhou's axis**, with H = +0.65 +/- 0.16 at Zhou's axis (fixed-axis permutation p = 0.013-0.02) and A_fix(Chang) = +0.62 +/- 0.23 (p = 0.03). The free-direction permutation p is 0.094-0.118, so nothing is detected once the direction is free, and the amplitudes are 2-3x the published values. "Profile Y only" points to (184, -1), 19 degrees from Chang's direction. A fixed-nuisance estimator with curvature errors could therefore produce a claim of the published direction and a small error; whether the papers did that cannot be tested here. It is a hypothesis about their method, not a result.
- **What cannot be tested:** whether their +/-0.04 errors are correct, what sample they used, whether their direction came from fixed Y, and every statement about "fixed distances" in CFG182's text.

## 9. Expectation record (hand estimates in the frozen file; wrong ones kept)

Right: N = 149 and points 3150 (0.80 / 0.60); A-hat within 0.03; direction within 15 deg (0.35, achieved 2.0); p within 0.05; verdict NULL, S2 and S3 fail; a-bar0; null quantiles; A95 0.40-0.45; mean A-hat at each injected A (0.36, 0.39, 0.44, 0.60 predicted; 0.37, 0.41, 0.45, 0.58); median direction error (30 deg at 0.5, 75 deg at 0.1; 27 and 72); detection power (0.06 / 0.08 / 0.12 / 0.35 predicted, 0.04-0.05 / 0.09 / 0.09-0.11 / 0.29-0.34); no simple-estimator variant reaches the published numbers; the README's "neither" verdict; fixed and looser priors keep p > 0.05; sample and ladder cells all p > 0.05; A95 coverage >= 0.93.
Wrong: sigma_A definition (0.161 vs 0.201, a row miss); recovery ratio 0.75 (found 0.96 mean, direction-dependent 0.71-1.09); M1 did not bite (p 0.095); largest jackknife shift below 0.10 (0.176); random-effects amplitude within 0.10 of the Birge fit (0.469); least-constrained direction within 30 deg of the footprint axis (75-82 deg); "NULL survives every nuisance cell at 0.05" (profile-Y-only p = 0.022); a fixed-direction A95 coverage failure (none found; the A_fix +/- 1.96 sigma intervals do under-cover, 0.884 for Zhou).

## Files (all `CFG192_*` unless noted)

Scripts: `CFG192_common.py`, `CFG192_profiles.py`, `CFG192_main.py`, `CFG192_attacks_AB.py`, `CFG192_attacks_CD.py`, `CFG192_attacks_E.py`, `CFG192_compare.py` (phase 2 only), `run_all.sh`.
Outputs: `CFG192_profiles.{out,json,npz}` and `CFG192_profiles_MUTATE_{1,2,4,6}.{out,json,npz}`; `CFG192_main.{out,json}`; `CFG192_MUTATE_{1..7}.{out,json}`; `CFG192_attacks_{AB,CD,E}.{out,json}`; `CFG192_compare.{out,json}`; `CFG192_SHA256.txt` (sha256 of every `.out`); `CFG192_FROZEN_CRITERIA.md`; this `README.md`.

## Reproduce

From this directory (or wherever the files are placed): `ZF_REPO=<repo root> bash run_all.sh`. Runtimes on a heavily loaded machine with 12 worker processes: profiles 26 s (each MUTATE build similar), main about 35 s, attacks A+B about 2 min, C+D about 7 min, E about 15 s, compare about 1 min; each script is well under 15 minutes. Exit codes: main 0; MUTATE k exits 1 when the control bites (k = 1 and 7 exit 0: M1 failed to bite, M7 is a no-op by design); attacks 0. A second complete run of `run_all.sh` gave byte-identical `.out` files (timings go to stderr only; the one nondeterminism found, dict ordering in the compare summary line, was fixed and the compare output then checked under three hash seeds). No absolute path appears in any output (`grep` for the home and temp prefixes finds nothing); the repository prints as `<repo>`.

## In-place re-run (orchestrator)

`bash run_all.sh` was re-run in this directory with `ZF_REPO` set (`run_all.out`): profiles and main exit 0; main MUTATE 2-6 exit 1 (bite); MUTATE 1 (point-level A = 0.5) and 7 (A = 0 injection) exit 0 (M1 does not bite, kept as failed; M7 is a designed no-op); the three attack scripts and the compare script exit 0. Every `.out` and `.json` is byte-identical to the referee's and the regenerated `CFG192_SHA256.txt` (the hash of every `.out`) is byte-identical to the referee's; the `.npz` profile curves were regenerated (not byte-compared). The frozen criteria are `../CFG192_FROZEN_CRITERIA.md` (6b619e616). Independence stops at the data files: the priors, Birge scaling, grid, kernel and pass lines are shared with CFG182, so agreement to three digits measures the implementation, not the design.
