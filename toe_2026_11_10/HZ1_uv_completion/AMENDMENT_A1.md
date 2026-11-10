# HZ1 AMENDMENT A1 (POST HOC, 2026-11-10): a stronger twin for M5

Committed alone, after the first graded and MUTATE runs. Changes no graded line and no label.

**What happened.** Twin M5 (FROZEN_CRITERIA section 4) sets every (ii) matter bound to 1e-60 and expects the window to
be empty and (iii) to read FAIL. It does not. At C = 1e-3 and alpha_LV = 2 the top of the window is
Mbar_P sqrt(16 pi^2 1e-60/(2e-3)) = 0.68 eV, still above M_lo = 5.1e-3 eV. So (ii) and (iii) read OPEN (empty at C = 1e3,
non-empty at C = 1e-3), not FAIL. My pre-run choice of 1e-60 was too weak by my own formula. **M5 is recorded as NOT
BITING AS FROZEN.** The gate logic did move (PASS -> OPEN), but not to the frozen expectation.

**Added (post hoc) twin M5'.** Every (ii) bound set to 1e-70. The window is then empty for C >= 1e-3 on both footings
(the top falls below M_lo once a bound is under about 5.6e-65), so (ii) and (iii) must read FAIL. It is run in the
MUTATE pass and reported next to M5, marked post hoc. It only checks that the FAIL branch of the window logic can fire.

kappa = 1/2 FITTED; not theory closed.
