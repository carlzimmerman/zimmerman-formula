# AC23: AC2q's slow roots on fresh dark-energy-like witnesses: PASS (HARMLESS, scoped)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (6b3a77495e),
frozen before any script or number. Scripts: scan.py (witness selection with AC3's own algebra), run.py
(AC13's run() imported unchanged, output redirected), grade.py. 3 threads, nice 15.

## Label: PASS (HARMLESS, scoped)

- **Fresh witnesses.** The new 81-cell grid (eps_phi 0.1/0.25/0.4, eps_m 0.2/0.6/0.95, H Lstar
  3e-4/3e-3/3e-2, k/H 3/30/300; every value new) has 58 cells with a negative frozen root. Grid B was not
  needed. By the frozen rule the 16 most negative were taken: w^2/H^2 from -0.804 to -0.482, comparable to
  AC3's -0.898 to -0.167.
- **All 16 are powered.** The planted -(2H)^2 K q term reaches R = 2,577 to 18,882 at N_obs = ln 1101 on
  every witness, at both tolerances. The measurement sees a Hubble-rate wrong term on each one.
- **AC2q does not amplify.** Main R at N_obs is 1.00 to 2.70 (line 10). It is unchanged at N = 20
  (largest 2.70). Convergence is within 2.0e-4 between rtol 1e-9 and 1e-11 (line 1e-3), and Omega drift is
  at most 5.7e-8 (line 1e-6).
- **The kinetic matrix stays positive.** AC2q's min det K / a^6 is at least 0.050 on every witness. The
  frozen det K discriminator bites on all 16: the flipped stiffness (m2) reaches det K / a^6 of -4.4 to
  -4.5e4, or stops at the singularity, by N = 20.

## Known answers and controls

- KA1: AC13's witness (.05, .3, .001, 10), rerun through AC23's import, reproduces AC13's committed
  max_I, max_II and det K at N_obs exactly (relative difference 0).
- KA2: the scanner reproduces AC3's 81 committed roots to 5e-30 relative and its 8 witnesses exactly. The
  40- and 80-digit roots agree.
- MUTATE (`AC23_MUTATE=1`, grade_MUTATE.out / GRADE_MUTATE.json): grading m2 in place of main gives FAIL.
  The gates catch a wrong stiffness.

## How this relates to AC13

AC13 stays NO VERDICT as frozen. Its gate needed power on every witness, and its 2 eps_phi = 2 witnesses
are decelerating fixtures where nothing can grow 1e3 in 7 e-folds. AC23 put that scope choice into its
criteria before running, with reasons: the physical clock is the dark-energy scalar, so it is
dark-energy-like (eps < 1). It then graded power witness by witness on new parameters. AC13's post-data
reading is now a frozen result on fresh data.

## What it does not show

Linear modes on rolling-clock FRW fixtures from z = 1100 (and to N = 20, reported). Not the radiation era
(FN1), not decelerating fixtures (eps_phi = 2 stays NO VERDICT in AC13), nothing sourced and nothing
nonlinear. The cap took the 16 most negative witnesses, so 14 of them have eps_phi = 0.1 or 0.25, and none
has eps_phi = 0.4. All witnesses sit at a = H = 1 frozen-root selection, as in AC3.
