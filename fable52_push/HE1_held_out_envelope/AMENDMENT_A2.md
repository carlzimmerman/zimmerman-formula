# HE1 AMENDMENT A2 (committed alone, after the second run and before the third)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

**No criterion changes.** This file records a code bug that a known answer caught, and its fix.

## What happened

- The second run (after A1) was **NO VERDICT on both footings**. KA1-KA5, KA7 and KA8 passed. The new KA6 failed: a model
  window amplitude moved by 0.023 between the 0.01- and 0.005-dex lens grids (line 0.01). The outputs are kept unchanged as
  `he1_run2_noverdict.json`, `he1_run2_noverdict.out` and `run_main_run2.txt`. The MUTATE chain started after it was stopped
  before it finished; its partial log was discarded.
- **Cause: a root-bracketing bug in the closure-A solver.**
  - The solver brackets the share condition on a table of envelope masses and then refines with the exact function.
  - When the table's sign change fell one grid interval after the true root, the exact function had the same sign at both
    ends of the bracket. brentq raised an error, the error was silently skipped, and the solver kept the only other root:
    the inner equilibrium at x_w of about 0.07 r_M.
  - The bug hit isolated masses only. Example: X_share with R_out = 3 Mpc at log M 10.950, where the bin factors fell to
    about 0.01 in every bin at that one node.
  - Before reading the solver I suspected the quadrature. It was checked against adaptive integration across a wall
    crossing and agrees to 1e-4. The square-root behaviour of a bin's factor at a crossing is real.
- **Fix.**
  - When the exact function does not confirm a table bracket, the bracket is widened to the neighbouring intervals:
    (j-1, j+1), then (j, j+2), then (j-2, j+2).
  - Table rows whose first tabulated radius lies beyond R_out are now evaluated exactly.
  - Any sign change still unconfirmed is counted and printed (`root_bracket_misses`).
  - After the fix, the 0.005-dex scan of the case above has no outlier node. The largest remaining node-to-neighbour
    deviation is about 0.1, at wall crossings, as expected.
- **Possible reach of the bug.** Any envelope call could have taken the inner root: Part B, the GSMF grid (G1-G3, G2's
  walls) and the lens grid. G1 failures seen in runs 1 and 2 for X_cap may include spurious inner roots. The third run
  decides them.

## What the second run showed (seen before writing this file)

Gate outcomes as in run 1, apart from small moves in the G4 amplitudes. At the primary R_out G4 fails for every X on both
footings. G5 fails as frozen. FAILS at the primary for every X, before the fix.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
