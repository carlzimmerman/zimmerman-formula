# QX8: the flagship SPARC grade on the action's exact field. EXACT FIELD PASSES on both footings (U refits upward)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Footings never pooled. Criteria: FROZEN_CRITERIA.md
(8ad4e65ea3), committed before any graded number. Script: qx8.py (solve, grade, grade --mutate). Outputs: qx8.out /
qx8.json and qx8_MUTATE.out / qx8_MUTATE.json, with per-galaxy parts in parts/{canonical,alt}/NNN.npz.

## Why

PAPER67's SPARC pass (FG1 row S, EM1/P4's grader) applies the algebraic law in the plane. QX4 found that the
action's exact static field, AQUAL with mu = x/(1+x), sits up to 0.097 dex below the law in low-surface-density
discs. So the action's own prediction had never been graded on SPARC. This lane grades it with the same sample,
mask, weights, U grid and line (rms <= 0.110 and median U 0.50-0.80). The exact field enters as a per-point
correction T = log10(g_exact/g_alg). Both terms come from the solver's own field, so baryon-inversion error is
second order.

## Result

| | Law (algebraic) | Exact field (the action) |
|---|---|---|
| canonical, rms @ median U | 0.0541 @ 0.52, PASS | **0.0560 @ 0.58, PASS** |
| alt, rms @ median U | 0.0537 @ 0.44, FAIL (U) | **0.0558 @ 0.52, PASS** |
| canonical, fixed U = 0.50 rms / mean residual | 0.1124 / +0.0504 | 0.1181 / +0.0594 |
| alt, fixed U = 0.50 rms / mean residual | 0.1029 / +0.0239 | 0.1070 / +0.0333 |
| without the 26 K4-tagged galaxies (149) | 0.0575 @ 0.53 / 0.0579 @ 0.44 | 0.0595 @ 0.61 / 0.0600 @ 0.53, PASS / PASS |

- **Label, both footings: EXACT FIELD PASSES (U refits upward).** The exact field lowers the predicted
  accelerations: median T is -0.012 dex overall and about -0.02 in the deep-MOND bin. U refits upward to
  compensate: median +0.020 per galaxy, mean +0.056. The cost in rms is +0.002 dex. At fixed U = 0.50 the exact
  field fits worse (canonical rms 0.112 -> 0.118).
- **The alt footing now meets the line.** The law alone failed it only on U (0.44); the exact field's upward U shift
  puts alt at 0.52. This changes the record's footing story: on the action's own field both footings pass PAPER67's
  line.
- **Where T is large.** T scales with low surface density and with the innermost data points:
  - Median per-galaxy minimum T: -0.20 (SBdisk(R_1) < 50 L/pc^2), -0.16 (50-200), -0.06 (200-1000), -0.025 (> 1000).
  - The ten most negative T values (-0.35 to -1.69) are all at each galaxy's first data point, in gas-dominated dwarfs
    (UGCA444, DDO064, NGC3109, ...). They are numerically converged: UGCA444's first three points at 160x48 / 240x72
    / 320x96 read -1.691 / 0.0 (g <= 0, T = 0) / -1.687, then -0.599 / -0.582 / -0.597. This is physical in AQUAL:
    at a disc's centre the radial Newtonian field goes to 0 while the vertical one stays finite, so mu is evaluated on
    |grad Phi| and the algebraic nu(g_R) overstates the boost. These points carry large velocity errors and little
    weight.
- **Surface-brightness trend at fixed Vflat (reported, 2 sigma line): no trend on either field.**
  - Canonical: law -0.030 +- 0.021 (1.5 sigma), exact -0.038 +- 0.021 (1.8 sigma).
  - Alt: -0.028 (1.4 sigma) and -0.034 (1.6 sigma).
  - The exact field moves the slope toward a trend but stays under 2 sigma.
  - The per-galaxy mean residual also has a slope of +0.21 to +0.26 against log Vflat, about the same for the law and
    the exact field. This is the existing grader's statistic and was not graded here; it is reported as found.

## Known answers and controls

- KA1: the algebraic mode reproduces P4/EM1 exactly, 0.054087 @ 0.52 and 0.053718 @ 0.44. PASS.
- KA2 Plummer: 6.2e-4 (line 1e-3), PASS. KA3 Kuzmin against BM95: 0.0047 (line 0.02), PASS. The fast deposit
  matches aqual.Grid.deposit exactly (0.0).
- K4 baryon reconstruction: median 3.35 % (line 5 %), PASS. 26 galaxies are above 10 % and are tagged; the grade
  without them still PASSES on both footings.
- K5 ladder (160x48 against 240x72, 12 galaxies): 0.0032 / 0.0033 dex (line 0.005), PASS.
- K6 U interpolation: 0.0004 dex (line 0.005), PASS.
- K7: 0 of 875 solves per footing above residual 1e-7. In 45 points per footing g <= 0, so T = 0 is used there.
- MUTATE M1 (mu = 1, Newton): rms 0.2528 @ U 1.20 on both footings, line FAIL. Bites.
- MUTATE M2 (planted T - 0.100): the fixed-U mean residual moves +0.1000; median U moves 0.58 -> 0.89
  (canonical) and 0.52 -> 0.79 (alt). Bites.
- Sensitivity (reported, U 0.60, 12 galaxies): z_g x 2 changes T by median 0.0006 (max 0.023); z_d x 2 by median
  0.0018 (max 0.050).

## Disclosed

- The first solve crashed: scipy's NNLS hit its iteration cap on the unscaled gas basis (run_solve_first_nnls_maxiter.txt).
  The fix is unit-norm column scaling, with bounded least squares as a fallback. That is a conditioning fix only.
  All parts were deleted and recomputed.
- The data are the rotmod files plus SPARC_Lelli2016c.mrt, as the flagship grader uses. The RC100 CSV is not
  involved.

## What it does not show

- Isolated discs only: no external field.
- Catalogue distances and inclinations.
- One vertical-thickness convention (SPARC's z_d = 0.196 R_d^0.633 for stars; z_g = 0.15 kpc for gas), plus the
  reported sensitivity.
- Bulges are spherical, from Vbul.
- AQUAL static sector only. v3s/AC2q's other static terms are <= 4e-4 (QX4 3a, AC8).

The pass leans on U refitting upward by about 0.02 (median). A stellar-mass prior that pinned U near 0.50 would
turn the exact field's extra 0.006-0.009 dex mean offset into a cost (see the fixed-U rows).
