# CFG240 -- the baryon-calibration wall: Lean theorems (ChainCert/CalibrationWall.lean) and a numeric Fisher companion

> **kappa = 1/2 is FITTED. No data, no empirical fact, no "the data favour" statement is in this lane.** Frozen criteria: `../CFG240_FROZEN_CRITERIA.md` (commit 56b99e337, written before any proof or script). The phase-1 statement file `CFG240_statements_phase1.lean.txt` is kept as is; the module `fable_independent_2026/lean_2026/ChainCert/CalibrationWall.lean` proves every one of its 36 statements AS FROZEN (verified mechanically: each frozen signature occurs verbatim in the module).

## 1. What Lean certifies and what it does not
**Certified (implication from declared premises).** For the declared law `g_obs = (f g) nu((f g)/a0)` (`gObs`; f > 0 is ONE multiplicative calibration of g_bar, the same f and a0 at every point):
- T1: the deep-regime law `g_obs = sqrt(f a0 g)`; dependence on (f, a0) only through f*a0 (an iff); a drift in log f or log a0 moves log g_obs by half the drift; for P2 the exact identity `g_obs^2 = f^2 g^2 + (f a0) g` and, for equal products, the exact ratio `g_obs'^2/g_obs^2 = (1 + rho^2 y)/(1 + y)` (rho = f'/f, y = f g/a0 of the first pair), the bound `|g_obs'^2 - g_obs^2|(f a0) <= |f'^2 - f^2| g g_obs^2` and `g_obs'/g_obs -> 1` as g -> 0+; and, for ANY kernel with C2's deep premise (nu y sqrt y -> 1), the same asymptotic wall.
- T2: exact two-point injectivity of (f, a0) for P2 (any two distinct positive g_bar); failure at one point (witness f' = f/2, a0' = 1.5 f g + 2 a0); failure for the deep kernel; a kernel-general two-point injectivity from strict convexity of `log(e^u nu(e^u))`, instantiated for P2 and for nu_mono; the closed-form Jacobian (rows `(1 - b, b)`, determinant `b(y2) - b(y1)`).
- T3: for any kernel with nu -> 1 at large y, `g_obs/g -> f` and the a0 dependence disappears.
- T4: for rows `(1 - b_i, b_i)` with every `b_i` in `[0, 1/2]`, `var(log a0) = (F^-1)_22 >= 9 sigma^2/N`, i.e. `sigma(log a0) >= 3 sigma/sqrt(N)` with f free (`T4_design_bound`, `T4_sigma_floor`; the Fisher entries are the definitions `fisher11/12/22`).
**NOT certified.** That a calibration factor exists in any survey, its size or redshift dependence; that a0 is common to the points; that nature follows P2 or nu_mono; any statistics beyond the algebra of the Fisher matrix as defined (the numbers in section 4 are numeric, not Lean); any other systematic (selection, M/L, gas, non-circular motion); non-multiplicative calibrations (offsets, g-dependent f); and that b(y) lies in [0, 1/2] for nu_mono: `T4_*` take `0 <= b_i <= 1/2` as a HYPOTHESIS, the Lean module proves the b-formula for P2 only (`T2c_dlogf`, `T2c_dloga`); for nu_mono b = sqrt(y)/(2(e^sqrt(y) - 1)) is checked symbolically and numerically here (PL2, PL8), not in Lean. T4's equality design (2/3 of the points deep, 1/3 Newtonian) is verified numerically (PL5), not in Lean.

## 2. Theorem list (module `ChainCert/CalibrationWall.lean`, namespace `CalibrationWall`; 50 theorems; library 281 -> 331)
Proved AS FROZEN (36): `nuP2_eq_nuBeta`, `T1_deep_law`, `T1_deep_equal_products`, `T1_deep_iff`, `T1_deep_drift`, `P2_sq`, `P2_sq_y`, `T1_P2_ratio`, `T1_P2_bound`, `T1_P2_limit`, `T2a_inversion`, `T2a_P2_injective`, `T2a_one_point_fails`, `T2b_deep_not_injective`, `T2c_dlogf`, `T2c_dloga`, `T2c_rows`, `T2c_det`, `T2c_det_ne_zero_iff`, `T2c_det_bounds`, `T2c_yratio`, `T2c_fisher_det`, `T2c_fisher_singular_iff`, `T3_newton_limit`, `T3_newton_limit_a0`, `nuP2_tendsto_one`, `nuMono_tendsto_one`, `T1_general_limit`, `T1_general_equal_products_limit`, `T2c_det_general`, `T4_design_bound`, `T2e_injective_of_strictConvex`, `nuMono_pos`, `nuMono_logslope_strictConvex`, `T2e_nuMono_injective`, `nuP2_logslope_strictConvex`.
Added (14; not in the frozen list): `T4_var_a0_closed_form`, `T4_sigma_floor` (the owner's request: T4 on the covariance, with `fisher11/12/22` as the Fisher matrix and `0 < det F` as the invertibility premise), and 12 helpers `gObs_nuP2_pos`, `nuP2_deep`, `log_gObs_nuP2`, `fisher_sum_id`, `sum_one_sub_sq`, `convex_increment`, `two_point_core`, `log_gObs_general`, `Lmono_eq`, `LmonoF_hasDeriv`, `LP2_eq`, `LP2F_hasDeriv`.
**nu_mono (T2e, the frozen "not formalisable cleanly" test).** PASSED: `nuMono_logslope_strictConvex` closes in about 60 lines (L(u) = u + w - log(e^w - 1), w = e^(u/2); L'(u) = 1 - (w/2)/(e^w - 1); strict monotonicity of w/(e^w - 1) from the strict secant slope of exp at 0), standard axioms only, no `native_decide`, no `sorry`. So the frozen fallback was NOT used: `T2e_nuMono_injective` is proved. Its content: any two distinct positive g_bar determine (f, a0) for nu_mono exactly as for P2.
**Mutate file.** `ChainCert/CalibrationWallMutate.lean.txt` (41 false variants, one per theorem or per spelling); `CalibrationWallMutate.out`: 41 errors, one per variant, 41/41 rejected (three of them, the variants that DROP a hypothesis, are rejected as unknown identifiers by construction; the others are type mismatches).

## 3. Numeric companion: definitions
`CFG240_fisher.py` (python3, numpy, sympy, mpmath). Parameters (log10 f, log10 a0); data log10 g_obs_i, independent Gaussian errors of sigma dex. **y = f g/a0 at the TRUE (f, a0)**, the argument fed to nu, because the Fisher matrix depends on the sample only through it; y_nom = g_bar/a0 = y/f differs by the unknown f. Design: N points, `y_i = y_min (y_max/y_min)^((i-1)/(N-1))` (log-uniform, endpoints included). Rows `(1 - b, b)`; P2 `b = 1/(2(1+y))`; nu_mono `b = s/(2(e^s - 1))`, s = sqrt(y). `sigma(log a0)` is the MARGINAL sigma, f free (with the Gaussian prior of tau dex on log10 f when stated). rho = -F12/sqrt(F11 F22): **NEGATIVE in every cell, -> -1** (both parameters raise g_obs; the degenerate direction keeps f*a0 fixed). cond = ratio of the eigenvalues of F. `y_max*` = the smallest y_max on the grid `y_min 10^(k/50)` such that sigma(log a0) < 0.1 dex for ALL larger grid y_max up to the cap **y_max <= 1e4** (the "stable" break-even the paper quotes); "none" = not within the cap. `y_max_first` (first crossing) is in the JSON; sigma(log a0) is NOT monotone in y_max (past the optimum extra Newtonian points hurt), and for some cells a first crossing exists with no stable one. Closed forms (hand and sympy, PL2): with A = 1 - b, B = b and D = (1/2) sum_ij (b_i - b_j)^2: `F = sigma^-2 [[sum A^2, sum AB],[sum AB, sum B^2]]`, `det F = D/sigma^4`, `var(log a0) = sigma^2 sum A^2/D`, `var(log f) = sigma^2 sum B^2/D`, `cov = -sigma^2 sum AB/D`, conditional `sigma(log a0|f) = sigma/sqrt(sum B^2)`, prior `var'(log a0) = sigma^2 (sum A^2 + sigma^2/tau^2)/(D + (sigma^2/tau^2) sum B^2)`. Two-point Jacobian det `= b(y2) - b(y1)` (P2: `(y1 - y2)/(2(1+y1)(1+y2))`, magnitude < 1/2).

## 4. The break-even table (the paper line: "a sample must reach y >~ y_max* to break the degeneracy at 0.1 dex")
Machine-readable: `CFG240_break_even_table.json` (header record with the definitions, then one record per case: kernel, y_min, N, sigma_dex, prior_log_f_dex, y_max_break_even (= y_max*, null if never within the cap), y_max_first, rho/sigma(log a0)/cond at the break-even, sigma_min and its y_max). The table below is generated from that JSON and the script CHECKS (PL10) that this block equals it.
**T4 floor:** sigma(log a0) >= 3 sigma/sqrt(N) for ANY sample (f free): at sigma = 0.1 dex the target 0.1 needs N > 9, at 0.2 dex N > 36, at 0.05 dex N > 2.25. No y range helps below the floor (hence "none" for N = 5, sigma = 0.1 and for N = 20, sigma = 0.2 in every row).
Reading the headline: for P2, y_min = 0.01, N = 20, sigma = 0.1 dex, no prior, the sample must reach **y >~ 8**; with y_min = 1e-3, y >~ 5.5; with y_min = 0.1 (no deep points) it never reaches 0.1 dex (best 0.117 at y_max ~ 48). For nu_mono, y_min = 0.01, N = 20, sigma = 0.1: first crossing at y_max = 42 but no stable break-even (minimum 0.0958); y_min = 1e-3: y >~ 17. A prior of 0.15 dex on log f lowers the P2 headline from 7.9 to 5.5; 0.3 dex to 7.2. Even at break-even rho ~ -0.8 and cond(F) ~ 13: the degeneracy is broken in sigma, not removed in correlation.

<!-- TABLE-BEGIN -->
| kernel | y_min | N | sigma (dex) | y_max* (no prior) | rho | sigma(log a0) | cond(F) | y_max* (tau=0.15) | y_max* (tau=0.3) |
|---|---|---|---|---|---|---|---|---|---|
| P2 | 0.001 | 5 | 0.05 | 2.75 | -0.844 | 0.0998 | 14.2 | 1.91 | 2.51 |
| P2 | 0.001 | 5 | 0.1 | none | - | - | - | none | none |
| P2 | 0.001 | 5 | 0.2 | none | - | - | - | none | none |
| P2 | 0.001 | 10 | 0.05 | 1.32 | -0.932 | 0.0989 | 30.7 | 0.955 | 1.2 |
| P2 | 0.001 | 10 | 0.1 | none | - | - | - | none | none |
| P2 | 0.001 | 10 | 0.2 | none | - | - | - | none | none |
| P2 | 0.001 | 20 | 0.05 | 0.759 | -0.969 | 0.0984 | 65.2 | 0.55 | 0.692 |
| P2 | 0.001 | 20 | 0.1 | 5.5 | -0.839 | 0.0999 | 14 | 3.63 | 5.01 |
| P2 | 0.001 | 20 | 0.2 | none | - | - | - | none | none |
| P2 | 0.001 | 50 | 0.05 | 0.398 | -0.988 | 0.0988 | 175 | 0.288 | 0.38 |
| P2 | 0.001 | 50 | 0.1 | 1.32 | -0.948 | 0.0994 | 39.7 | 0.955 | 1.26 |
| P2 | 0.001 | 50 | 0.2 | none | - | - | - | none | none |
| P2 | 0.001 | 100 | 0.05 | 0.263 | -0.994 | 0.0967 | 345 | 0.191 | 0.24 |
| P2 | 0.001 | 100 | 0.1 | 0.692 | -0.976 | 0.0997 | 85.2 | 0.525 | 0.661 |
| P2 | 0.001 | 100 | 0.2 | 3.8 | -0.880 | 0.0998 | 18.1 | 2.63 | 3.47 |
| P2 | 0.01 | 5 | 0.05 | 3.98 | -0.809 | 0.0996 | 13.5 | 2.88 | 3.63 |
| P2 | 0.01 | 5 | 0.1 | none | - | - | - | none | none |
| P2 | 0.01 | 5 | 0.2 | none | - | - | - | none | none |
| P2 | 0.01 | 10 | 0.05 | 1.45 | -0.923 | 0.0990 | 29 | 1.1 | 1.38 |
| P2 | 0.01 | 10 | 0.1 | none | - | - | - | none | none |
| P2 | 0.01 | 10 | 0.2 | none | - | - | - | none | none |
| P2 | 0.01 | 20 | 0.05 | 0.759 | -0.967 | 0.0996 | 63.2 | 0.603 | 0.724 |
| P2 | 0.01 | 20 | 0.1 | 7.94 | -0.791 | 0.0995 | 13.3 | 5.5 | 7.24 |
| P2 | 0.01 | 20 | 0.2 | none | - | - | - | none | none |
| P2 | 0.01 | 50 | 0.05 | 0.398 | -0.987 | 0.0980 | 164 | 0.302 | 0.38 |
| P2 | 0.01 | 50 | 0.1 | 1.32 | -0.942 | 0.0999 | 37.8 | 1.05 | 1.26 |
| P2 | 0.01 | 50 | 0.2 | none | - | - | - | none | none |
| P2 | 0.01 | 100 | 0.05 | 0.251 | -0.994 | 0.0994 | 349 | 0.2 | 0.24 |
| P2 | 0.01 | 100 | 0.1 | 0.692 | -0.973 | 0.0986 | 78.7 | 0.525 | 0.661 |
| P2 | 0.01 | 100 | 0.2 | 4.37 | -0.854 | 0.0998 | 17.2 | 3.16 | 4.17 |
| P2 | 0.1 | 5 | 0.05 | none | - | - | - | none | none |
| P2 | 0.1 | 5 | 0.1 | none | - | - | - | none | none |
| P2 | 0.1 | 5 | 0.2 | none | - | - | - | none | none |
| P2 | 0.1 | 10 | 0.05 | 3.02 | -0.875 | 0.0998 | 27 | 2.63 | 2.88 |
| P2 | 0.1 | 10 | 0.1 | none | - | - | - | none | none |
| P2 | 0.1 | 10 | 0.2 | none | - | - | - | none | none |
| P2 | 0.1 | 20 | 0.05 | 1.26 | -0.951 | 0.0995 | 55.5 | 1.1 | 1.26 |
| P2 | 0.1 | 20 | 0.1 | none | - | - | - | none | none |
| P2 | 0.1 | 20 | 0.2 | none | - | - | - | none | none |
| P2 | 0.1 | 50 | 0.05 | 0.631 | -0.983 | 0.0979 | 141 | 0.55 | 0.603 |
| P2 | 0.1 | 50 | 0.1 | 2.51 | -0.905 | 0.0997 | 33.9 | 2.19 | 2.4 |
| P2 | 0.1 | 50 | 0.2 | none | - | - | - | none | none |
| P2 | 0.1 | 100 | 0.05 | 0.417 | -0.992 | 0.0991 | 301 | 0.38 | 0.417 |
| P2 | 0.1 | 100 | 0.1 | 1.1 | -0.962 | 0.0989 | 69.2 | 0.955 | 1.05 |
| P2 | 0.1 | 100 | 0.2 | none | - | - | - | none | none |
| nu_mono | 0.001 | 5 | 0.05 | 7.59 | -0.815 | 0.0993 | 13.4 | 5.5 | 6.92 |
| nu_mono | 0.001 | 5 | 0.1 | none | - | - | - | none | none |
| nu_mono | 0.001 | 5 | 0.2 | none | - | - | - | none | none |
| nu_mono | 0.001 | 10 | 0.05 | 2.75 | -0.925 | 0.1000 | 29.6 | 2 | 2.63 |
| nu_mono | 0.001 | 10 | 0.1 | none | - | - | - | none | none |
| nu_mono | 0.001 | 10 | 0.2 | none | - | - | - | none | none |
| nu_mono | 0.001 | 20 | 0.05 | 1.2 | -0.966 | 0.0998 | 62.9 | 0.832 | 1.15 |
| nu_mono | 0.001 | 20 | 0.1 | 17.4 | -0.808 | 0.0999 | 13.5 | 12 | 15.8 |
| nu_mono | 0.001 | 20 | 0.2 | none | - | - | - | none | none |
| nu_mono | 0.001 | 50 | 0.05 | 0.437 | -0.987 | 0.0987 | 164 | 0.288 | 0.398 |
| nu_mono | 0.001 | 50 | 0.1 | 2.75 | -0.940 | 0.0989 | 36.8 | 1.91 | 2.51 |
| nu_mono | 0.001 | 50 | 0.2 | none | - | - | - | none | none |
| nu_mono | 0.001 | 100 | 0.05 | 0.209 | -0.994 | 0.0982 | 336 | 0.132 | 0.191 |
| nu_mono | 0.001 | 100 | 0.1 | 1.05 | -0.973 | 0.0993 | 79 | 0.692 | 0.955 |
| nu_mono | 0.001 | 100 | 0.2 | 11 | -0.858 | 0.0997 | 17.2 | 7.94 | 10 |
| nu_mono | 0.01 | 5 | 0.05 | 14.5 | -0.760 | 0.0995 | 13.3 | 11 | 13.2 |
| nu_mono | 0.01 | 5 | 0.1 | none | - | - | - | none | none |
| nu_mono | 0.01 | 5 | 0.2 | none | - | - | - | none | none |
| nu_mono | 0.01 | 10 | 0.05 | 3.8 | -0.908 | 0.0999 | 27.9 | 3.02 | 3.63 |
| nu_mono | 0.01 | 10 | 0.1 | none | - | - | - | none | none |
| nu_mono | 0.01 | 10 | 0.2 | none | - | - | - | none | none |
| nu_mono | 0.01 | 20 | 0.05 | 1.58 | -0.960 | 0.0994 | 58.4 | 1.2 | 1.51 |
| nu_mono | 0.01 | 20 | 0.1 | none | - | - | - | 28.8 | 38 |
| nu_mono | 0.01 | 20 | 0.2 | none | - | - | - | none | none |
| nu_mono | 0.01 | 50 | 0.05 | 0.575 | -0.986 | 0.0994 | 155 | 0.437 | 0.55 |
| nu_mono | 0.01 | 50 | 0.1 | 3.47 | -0.929 | 0.0997 | 35.2 | 2.75 | 3.31 |
| nu_mono | 0.01 | 50 | 0.2 | none | - | - | - | none | none |
| nu_mono | 0.01 | 100 | 0.05 | 0.288 | -0.993 | 0.0999 | 326 | 0.219 | 0.275 |
| nu_mono | 0.01 | 100 | 0.1 | 1.32 | -0.969 | 0.0998 | 74.6 | 1 | 1.26 |
| nu_mono | 0.01 | 100 | 0.2 | 17.4 | -0.811 | 0.0996 | 16.7 | 13.2 | 15.8 |
| nu_mono | 0.1 | 5 | 0.05 | none | - | - | - | none | none |
| nu_mono | 0.1 | 5 | 0.1 | none | - | - | - | none | none |
| nu_mono | 0.1 | 5 | 0.2 | none | - | - | - | none | none |
| nu_mono | 0.1 | 10 | 0.05 | 9.55 | -0.846 | 0.0999 | 27.2 | 8.71 | 9.55 |
| nu_mono | 0.1 | 10 | 0.1 | none | - | - | - | none | none |
| nu_mono | 0.1 | 10 | 0.2 | none | - | - | - | none | none |
| nu_mono | 0.1 | 20 | 0.05 | 3.31 | -0.941 | 0.0997 | 54.5 | 2.88 | 3.31 |
| nu_mono | 0.1 | 20 | 0.1 | none | - | - | - | none | none |
| nu_mono | 0.1 | 20 | 0.2 | none | - | - | - | none | none |
| nu_mono | 0.1 | 50 | 0.05 | 1.26 | -0.981 | 0.0998 | 141 | 1.1 | 1.26 |
| nu_mono | 0.1 | 50 | 0.1 | 7.94 | -0.882 | 0.0996 | 33.7 | 6.92 | 7.59 |
| nu_mono | 0.1 | 50 | 0.2 | none | - | - | - | none | none |
| nu_mono | 0.1 | 100 | 0.05 | 0.724 | -0.991 | 0.0989 | 283 | 0.631 | 0.692 |
| nu_mono | 0.1 | 100 | 0.1 | 2.75 | -0.954 | 0.0994 | 68.1 | 2.4 | 2.63 |
| nu_mono | 0.1 | 100 | 0.2 | none | - | - | - | none | none |
<!-- TABLE-END -->

## 5. Pass lines, MUTATE outcomes
PL1 analytic Fisher == 4-point finite-difference Fisher of the DEFINITION gObs (worst 4.8e-13 against 1e-8; f0 in {0.5, 1, 1.7}); PL2 closed forms == sympy (derivatives 5.6e-15; covariance, prior, det identities symbolic 0); PL3 T1 numerics (deep kernel equal to 0 for equal products; P2 relative difference `(rho^2 - 1) y/(1 + y)` to 2e-16 with mpmath at 50 digits, slope 0.9999; nu_mono ratio 1.0e-2); PL4 rho < 0 in every cell; single-y rho = -1; deep corner; PL5 T4 floor: 0 violations in 19505 seeded random designs (minimum ratio 1.135), equality at the 2/3-deep two-cluster design to 2e-16; PL6 det = b(y2) - b(y1) to 1.1e-16, max |det| 0.4995; PL7 scalings; PL8 eta strictly increasing on a grid (NOT a proof; the proof is `nuMono_logslope_strictConvex`), T3 numerics; PL9 break-even logic; PL10 JSON == README.
MUTATE controls (`MUTATE=k`, exit 1 iff it bites): M1 wrong kernel in the analytic rows (the deep value b = 1/2 for P2): PL1 and PL2 fail (also PL6, PL7, PL8) -- bites. M2 F built without 1/sigma^2: PL1 and PL7 fail -- bites. M3 y_nom = g/a0 used as the true y at f0 = 0.5 and 1.7: PL1 fails -- bites. M4 sign of the F12 term in rho flipped: PL4 fails -- bites. M5 break-even from sigma(log a0 | f) instead of the marginal sigma: PL9 fails (N = 5, sigma = 0.1 and N = 20, sigma = 0.2 then 'reach' 0.1 dex below the T4 floor) -- bites. M6 T4 constant 3 -> 3.1: PL5 fails (equality design) -- bites. All six exit 1; outputs `CFG240_fisher_MUTATE<k>.out` / `_results.json`. A control 'bites' iff the pass lines it was designed to break all fail (`EXPECT` in the script); other lines may fail too and are listed in each .out.

## 6. Failed checks and wrong estimates kept
Hand estimates of the frozen criteria (section 7 there) against the run -- hits and misses together:
- E1 (P2, y_min = 0.01, N = 20, sigma = 0.1, no prior): predicted first break-even ~17 (80% interval 8 to 40); run: **7.94** -- a marginal MISS below the interval. The estimate of sigma(log a0) at y_max = 10 was 0.105; run: 0.0972 (the continuum approximation to the endpoint-inclusive log-uniform sample overstated sigma by about 8%). The y_max = 30 estimate 0.097 against run 0.0913.
- E2 (y_min = 1e-3): predicted ~10 (5 to 25); run 5.5 (inside; lower than the y_min = 0.01 value, as predicted).
- E3 (y_min = 0.1): predicted NONE (P = 0.75): hit (none for both kernels, all priors). Predicted minimum 0.12 to 0.13 near y_max ~ 20; run 0.117 at y_max ~ 48: the minimum is slightly lower and about 2.4x further out (partial miss).
- E4 floors: hits (N = 5 and N = 10 at sigma = 0.1 and N = 20 at sigma = 0.2 return none; N = 100, sigma = 0.1: 0.69 against ~1 (0.3 to 3); N = 20, sigma = 0.05: 0.76 against ~1 (0.5 to 3)).
- E5 rho: predicted ~ -0.8 at y_max = 10 and ~ -0.7 at 30: run -0.77 and -0.69 (hits); deep corner -1.000 (hit).
- E6 cond(F) at the break-even: predicted ~15 (10 to 25); run 13.3 (hit).
- E7 prior: deep-only sample with tau = 0.15 gives sigma(log a0) ~ 0.156 predicted, run 0.160 (hit); tau = 0.15 lowers the first break-even by a factor 1.44 (predicted <= 1.5, hit) and tau = 0.3 by 1.10 (predicted < 1.15, hit).
- E8 nu_mono: predicted a first break-even within a factor 2 of P2's (P = 0.65). **MISS**: at y_min = 0.01, N = 20, sigma = 0.1 nu_mono needs y_max = 41.7 against P2's 7.9 (a factor 5.3), and it has no stable break-even (sigma(log a0) bottoms out at 0.0958 and is back above 0.1 for larger y_max). Reason, in hindsight: b falls from 1/2 more slowly for nu_mono at y ~ 1 to 30 (b(10) = 0.070 against 0.045), so a log-uniform sample carries less b-spread per decade.
- E9 Lean: the core 33 proved and nu_mono closed cleanly (hits); `T2c_dlogf` needed the sum rewrite (hit).
Other kept items:
- PL3b first failed at float64: the relative difference of g_obs^2 is ~ y, so double precision loses ~ 1e-16/y and the max relative error was 1.1e-10 against the frozen 1e-12. The formula was right; the check was moved to mpmath (50 digits), where the error is 2e-16. The frozen tolerance is unchanged.
- First implementation of MUTATE 2 (omit 1/sigma^2) only entered the finite-difference line, so it did not bite PL7 as frozen; the mutation was moved into the closed-form statistics so PL7 fails as intended. The first run had PL10 failing (README block not yet present): expected, the table is generated first and then pasted in.
- A first crossing without a stable one exists (for example nu_mono, y_min = 0.01, N = 20, sigma = 0.1: first 41.7, minimum sigma 0.0958 at y_max = 275, 'none' in the stable column). Those rows are marginal: the target is met only in a window of y_max.
- `T4_*` rest on `0 <= b_i <= 1/2` as a hypothesis; for nu_mono that range is numerical (PL2, PL8), not Lean. The equality design is numeric.
- Not run: the rest of the grid (sigma 0.05 and 0.2, other N, y_min = 0.1) is in the JSON but not individually hand-checked beyond PL1-PL10 and the floor.

## 7. Files and exact re-run commands
Lean (in `fable_independent_2026/lean_2026/`): `ChainCert/CalibrationWall.lean`, `ChainCert/CalibrationWallMutate.lean.txt`, `ChainCert/CalibrationWallMutate.out`; edited: `ChainCert.lean` (one import), `ChainCert/Axioms.lean` (import + 50 `#print axioms`), `ChainCert/README.md` (append). Numeric (this dir): `CFG240_fisher.py`, `CFG240_fisher.out`, `CFG240_fisher_results.json`, `CFG240_break_even_table.json`, `CFG240_break_even_table.md`, `CFG240_fisher_MUTATE1..6.out` and `_results.json`, this README. (The frozen plan named the script `cfg240_fisher.py`; the coordinator's phase-2 message asked for `CFG240_*` names; the latter is used.) Commands:
```
cd fable_independent_2026/lean_2026 && lake build ChainCert && ChainCert/verify_chain.sh        # PASS, 331 theorems
MUTATE=1 ChainCert/verify_chain.sh                                                                # must FAIL (exit 1)
cp ChainCert/CalibrationWallMutate.lean.txt ChainCert/CalibrationWallMutate.lean && lake env lean ChainCert/CalibrationWallMutate.lean > /tmp/m.out 2>&1; rm ChainCert/CalibrationWallMutate.lean; diff /tmp/m.out ChainCert/CalibrationWallMutate.out
cd campaign_fresh_gravity/CFG240_calibration_wall && python3 CFG240_fisher.py                    # exit 0, all PL pass
for k in 1 2 3 4 5 6; do MUTATE=$k python3 CFG240_fisher.py; done                              # each exits 1 (control bites)
```

## Orchestrator verification

Before this commit the orchestrator re-ran, in place: `lake build ChainCert` (8783 jobs, success), `ChainCert/verify_chain.sh` (331 theorems checked, 0 non-standard axioms, 0 sorry mentions, VERIFY: PASS), `MUTATE=1 ChainCert/verify_chain.sh` (VERIFY: FAIL, as required), the Mutate file compiled (41 errors, output identical to `CalibrationWallMutate.out`), a `sorry`/`axiom`/`native_decide` scan of `CalibrationWall.lean` (0 hits, 50 theorems), and the numeric companion (`CFG240_fisher.py` exit 0 with all six MUTATE runs exiting 1; every `.out`, `_results.json` and the break-even table identical to the author's apart from timing). `ChainCert/Axioms.out`, `verify_chain.out` and `verify_chain_MUTATE.out` were regenerated from the scripts (they showed 281 theorems before; now 331). Lean certifies the implications from the stated premises, not any empirical fact.
