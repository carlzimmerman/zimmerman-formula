# AC13 frozen criteria: a final label for AC3's 8 slow roots (AC2q)

Frozen before any AC13 script exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## Why

AC3 found 8/81 frozen finite-wavelength cases with one negative omega^2, -0.898 <= omega^2/H^2 <= -0.167
(all at H Lstar = .001, k/H = 10 or 100), i.e. frozen rates Gamma <= 0.948 H, below H where freezing is
not controlled. AC4 (constant V) and AC5 (rolling clock, 5 e-folds) evolved them: AC5 main R <= 2.68, but
its power gate failed (flipped stiffness only R 8.6 < 1e3), so NO VERDICT (no power). AC13 asks the
remaining question directly: over the expansion the record actually uses, can these roots amplify
beyond a fixed line, and can the measurement see such amplification at all?

## Candidate: AC2q, not only AC2

AC7 Q1 (exact): on FRW, AC2q's quadratic block is AC2's with the polarization coefficient
cY -> cY (1 - 2 gamma phidot^2)^2. AC5's integrator multiplies cY by `pol_on`, so AC2q is AC5's
equation with pol_on = (1 - 2 gamma s^2)^2. Physically gamma s^2 = 2.4e-17 / 4.0e-17 (AC9), so
pol_on differs from 1 by <= 1.6e-16: AC5's numbers are AC2q's to double precision. AC13 also runs a
stress value gamma s^2 = 0.1 (pol_on = 0.64), reported only.

## Background and e-fold range (framework-native)

AC5's rolling-clock flow (exponential V, lambda = sqrt(2 eps_phi0), canonical stiff matter), unchanged.
No LCDM input. Graded window: a = 1 to a = 1101, N_obs = ln(1101) = 7.004 e-folds. Why: z = 1100 is the
earliest epoch at which the record grades linear information (CMB lensing, WG1-WG6), and it is a measured
redshift (raw data), not a model background. The radiation era is outside AC2q's scope (FN1). A long
window to N = 20 (about z = 4.9e8) is run for the power control and reported for main; it is not graded
for main.

## Runs (witnesses only, 8 cases; two tolerances rtol 1e-9, 1e-11; AC5's measurement)

Running maxima of R = max_t ||q||_inf / max_t ||q_GR||_inf recorded at N = 5, 7.004, 10, 15, 20, plus the
absolute growth G = max_t ||q|| / ||q(0)|| for candidate and GR (reported).
- MAIN: AC2q at physical gamma s^2 (pol_on = 1 in double precision).
- M2: AC5's flipped polarization stiffness.
- MUTATE-P (planted): main plus a tachyonic term -(2 H)^2 K q added to the stiffness (a wrong term with
  frozen rate 2H, about twice AC3's largest slow rate), candidate only.
- STRESS: pol_on = 0.64, N_obs window, reported.

## Lines (stated before running)

- Known answer KA1: at N = 5, MAIN R must reproduce AC5's committed witness R (evidence/main/result.json)
  to 1e-6 relative on all 8 witnesses (same code path, same tolerances).
- Convergence: R agrees between the two tolerances to 1e-3 relative at each graded N; else NO VERDICT for
  that case. Omega drift <= 1e-6 on MAIN and M2.
- Ordering O1: MAIN R <= M2 R on every witness at N = 5 (AC5's committed numbers; already on record, so
  this is a re-read, reported in the grade but not a blind test) and at N_obs (new).
- POWER: at least one of (a) M2 reaches R >= 1e3 on some witness by N = 20, or (b) MUTATE-P reaches
  R >= 1e3 on every witness by N_obs. If neither bites, NO VERDICT (no power).
- HARMLESS (scoped) if power is met, every witness converged at N_obs, Omega line met, and MAIN R <= 10 at
  N_obs on every witness.
- FAIL if MAIN R >= 1e3 at N_obs on any converged witness.
- UNDECIDED otherwise.
- The 1e3 line is AC5's frozen FAIL line, kept. Reported alongside: the linearity line 1e5 (a 1e-5 seed
  reaching order one).

## Analytic bound (reported, not graded)

B1: if the frozen rate held at its worst value throughout, growth <= exp(0.948 N): reported at N_obs and
N = 20. It is uncontrolled (rates < H), which is why the direct runs decide.

## Scope stated now

HARMLESS says: on rolling-clock FRW backgrounds, AC2q's slow roots do not amplify beyond 10x the GR control
over the 7 e-folds since z = 1100, and the measurement detects a Hubble-rate wrong term. It is not
radiation-era health, nonlinear health, sourced backgrounds, a derivation of xi or kappa, or adoption.
