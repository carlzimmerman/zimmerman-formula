# AC13: AC3's 8 slow roots, AC2q, to z = 1100 and beyond: NO VERDICT (no power), as frozen

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (12b71c9c08), frozen
before any code. Scripts: ac13.py (AC5's build() executed verbatim, AC5's streaming measurement with
checkpoints), grade.py. 80 jobs, 2 threads.

## Frozen label: NO VERDICT (no power)

The power gate fails. (a) M2, the flipped stiffness, never reaches R >= 1e3 on any witness. (b) The planted
2H tachyon reaches R >= 1e3 on 6 of the 8 witnesses, but the gate required every witness. KA1 also misses
its own 1e-6 line (below).

## What the numbers show

- **Main (AC2q, physical gamma s^2): no growth at all.** At N_obs = ln 1101 the largest R over all 8 witnesses
  is 2.526, the same value AC5 found at N = 5. Every witness converged (rtol 1e-9 vs 1e-11 to < 1e-3), and
  Omega drift is <= 8.7e-8. On the 6 witnesses run to N = 20 (about z = 4.9e8), R does not change past its
  N = 5 value: for example 1.4559 -> 1.4559 and 2.5232 -> 2.5232. The slow roots do not amplify over 15 more
  e-folds.
- **The measurement sees Hubble-rate growth where the clock is dark-energy-like.** The planted -(2H)^2 K q
  term gives R = 2,986 to 18,931 at N_obs on all 6 witnesses with eps_phi <= 0.5. On the 2 witnesses with
  eps_phi = 2 it gives only R 9.4-9.8. There the background decelerates (eps > 1), H falls as a^-2, and even
  a 2H tachyon cannot reach 1e3 in 7 e-folds. The frozen worst-case bound B1 is also below the line there:
  exp(0.948 N_obs) = 764.
- **The flipped stiffness breaks in another way.** M2 does not grow slowly. On all 8 witnesses its kinetic
  matrix changes sign: min det K / a^6 runs from -50 to -6e10, while the true AC2q stays positive (0.025 to
  5e3). On the 6 witnesses with eps_phi <= 0.5 the integration stops at that singularity, at N = 4.06-10.35.
  On the 2 witnesses with eps_phi = 2 it runs through it and reaches R 26. So the setup does tell a wrong
  stiffness from the right one, but through a ghost / singular kinetic matrix, not through the graded R.
  The frozen gate was written for R and does not count this.
- O1 ordering holds: main <= M2 on every witness at N = 5 (AC5's committed numbers, a re-read) and at N_obs.
- STRESS (pol_on 0.64, i.e. gamma s^2 = 0.1): R stays at 1.0-2.53. AC2q's physical pol_on differs from 1 by
  1.6e-16, so AC5's AC2 numbers are AC2q's.

POST-DATA reading (not the frozen label): on the 6 witnesses where the clock is dark-energy-like
(eps_phi <= 0.5), power by the planted term is met and main R <= 2.53 <= 10, so they would read HARMLESS
witness by witness. The 2 eps_phi = 2 witnesses are decelerating fixtures. No physical dark-energy clock sits
there, and no control has power there.

## Known answers and controls

- KA1 FAILS its frozen 1e-6 line. Main R at N = 5 matches AC5 to 0 to 4.4e-5 relative. That is inside AC4's
  measured sampling floor (about 2e-4) and the 1e-3 convergence line, but the line was set too tight and is
  reported as missed.
- MUTATE controls: M2 (flipped stiffness) and the planted tachyon, as above. The planted term bites on 6/8.

## Bug found and fixed during the run (on the record)

The first launch passed lambda = 1 instead of sqrt(2 eps_phi) into the matrix function, so the background
flow and the Bdot/Kdot terms disagreed except at eps_phi = 0.5. It showed up as Omega drift up to 1.7e-3 and
KA1 misses up to 1.1e-4. The fix passes lam. All eps_phi != 0.5 parts were deleted and rerun (run2.txt).
The eps_phi = 0.5 parts are exact (sqrt(2 * 0.5) = 1) and were kept. The first log is kept as
run_bugged_lambda.txt. Its early BrokenPipe tracebacks are from killed workers of a launch that was
stopped before any part was kept.

## What it does not show

These are linear modes on rolling-clock FRW fixtures (H Lstar = .001). There is no radiation era (outside
scope, FN1), nothing sourced and nothing nonlinear. On the decelerating fixtures no control has power. A
powered verdict there needs a gate stated on det K (ghost crossing) or on a background where a wrong term
can grow by 1e3. That gate would be a new lane with new criteria, not a re-read of this one.
