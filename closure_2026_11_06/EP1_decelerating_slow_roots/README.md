# EP1: AC2q's slow frozen roots on decelerating (eps_phi = 2) backgrounds: HARMLESS (scoped); reachability NOT DECIDED as frozen

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: CRITERIA.md (d8fc918584), frozen before any
script or number. Scripts: scan.py (witnesses, KA3), run.py (AC13's run() from its committed file plus one asserted
added kind; 67 jobs, 3 workers, nice 15), grade.py, reach.py. Every number below is in GRADE.json, GRADE_MUTATE_*.json,
REACH.json, witnesses.json and diag_KinvS.json.

## Witness label: HARMLESS (scoped)

- **Fresh witnesses.** eps_phi = 2 grid A (27 cells, every value new) gives 7 cells with a negative frozen root. Grid B
  was not needed. The 6 most negative were taken (w^2/H^2 -0.820 to -0.646; AC3's eps_phi = 2 pair: AC13's fixtures).
- **All 6 are powered, by both frozen controls.** PW-R (stiffness replaced by -(2H)^2 K) reaches R = 1105 to 1228 at
  N_obs at both tolerances, against the 1e3 line. **The margin is thin (1.10x to 1.23x).** PW-D (flipped stiffness
  m2) turns det K / a^6 negative on all 6 (-5.1e8 to -7.3e10).
- **AC2q does not amplify.** Main R at N_obs = ln 1101 is 1.32 to 2.53 (line 10). Convergence is within 1.5e-4
  between rtol 1e-9 and 1e-11 (line 1e-3). Omega drift is at most 1.4e-7 (line 1e-6). Main det K / a^6 is at least
  13.5 and positive throughout.
- **MUTATE bites.** Grading m2 in place of main gives UNSTABLE on all 6 (det K), and so does grading plantR (R >= 1e3).
  m2's R is only 21-22, so on these backgrounds a wrong stiffness is caught by det K, not by R (as AC13 found).
- Known answers. KA1: AC13's 2 eps_phi = 2 fixtures (main, gr, plant, m2) rerun through EP1's runner match AC13's
  committed parts exactly (8/8, relative difference 0). KA2: AC23's committed grade.py on its committed parts gives
  PASS (HARMLESS, scoped), 16 powered, max R 2.700138003169356 and min det K 0.050019119025378346, identical to
  AC23's GRADE.json. AC23's witness (0.25, 0.6, 0.0003, 3) rerun matches its part exactly. KA3: the scanner
  reproduces AC3's 27 eps_phi = 2 roots to 5.0e-30, and its witness set is exactly AC13's 2 fixtures.
- Reported: PW-R on AC13's own 2 fixtures gives R 2152 / 2081, where AC13's additive plant gave 9.75 / 9.43. AC13's
  additive plant on the fresh witnesses gives R 3.9-4.4.

## Post-data correction to the stated analysis (not a label change)

The criteria said gradient pressure swamps AC13's additive plant. diag_KinvS.json shows that is not the mechanism.
The smallest eigenvalue of K^-1 S / H^2 along main's background tends to +2.0 by N = 4 to 6, so the slow mode's
stiffness is Hubble-scale, not k^2/a^2. The additive -(2H)^2 K q then leaves a net -2H^2, and that it still does not
grow comes from the damping (Kdot + A) terms. PW-R also grew more slowly than the stated e^(1.56 N) estimate (about
e^(1.0 N)), for the same reason. The estimate was not a line, and both controls were graded exactly as frozen.

## Reachability (separate label): NOT DECIDED by the record data, as frozen

- The fixture family itself is excluded outright. With lambda = 2, eps >= 2 always, so q >= 1 and the universe never
  accelerates. A physical dark-energy clock does not sit there.
- On CFG689's measured rho_DE(z), z <= 2.33: the best-fit bound is 0.54 (0.22 with the full E^2), far below 2. The
  frozen 2-sd worst case reaches **2.163 at z = 0.4** (margin -0.163). That is above the line only because the
  frozen bound dropped rho_DE from rho_tot.
- Post-data, reported: keeping rho_DE in rho_tot gives 1.18. **EP2** (successor lane) freezes the corrected exact
  bound and grades it.

## What it does not show

Linear modes on rolling-clock FRW fixtures at eps_phi = 2, over 7.0 e-folds (N = 20 is infeasible there: k/(aH)
grows as e^N). It is not the radiation era, not nonlinear, not sourced and not adoption. Both footings: gamma s^2
enters only through pol_on, which equals 1 to within 1.6e-16 on both, so one run grades both (AC13).
