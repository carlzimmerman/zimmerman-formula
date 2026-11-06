# AC21 iter_7 frozen criteria: curved-interface C1 test with corrected statistic on fresh data (after iter_2)

Frozen after iter_2 ran and before any iter_7 number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## Why

iter_2 is NO VERDICT as frozen, and that label stands. Two of its frozen lines were the wrong statistic:

- **The smoothed rows converged too fast for the band.** Their jump falls as N^-3 (r = 8.0 in both rows), with
  Delta_inf = 0 to 1e-5. The band r in [1.6, 2.4] was written for first-order convergence, which AC20 saw for
  m = 4. A row that converges at higher order is smoother, not kinked, so the upper cap was never a C1 criterion.
- **The v3s control was measured after it had already crossed.** Its first crossing time fell by about
  sqrt(2) per doubling (0.075, 0.053, 0.037, 0.026, 0.018), which is AC16's "immediate crossing" signature N3b.
  For N >= 6400 that time was below t_meas = 0.03, so its slopes were read after crossing (the jump flips sign at
  12800), and the frozen "r < 0.9" line misfired.

This iteration fixes both lines and reruns on fresh initial data.

## Data and rows

- Same radial scheme as iter_2.
- Pi_0 = tanh(3 (r - 1)), v_0 = 0.1 cos(r - 1). These are new data that no earlier run has seen.
- t_meas = 0.01; N = 800, 1600, 3200, 6400, 12800.
- Rows: the iter_6 winner at b = 0.4 and b = 0.8.

## Lines

- **C1 PASS for a row.** All three of:
  - |Delta_inf| <= 0.1 |Delta_n3(12800)|;
  - r >= 1.6 (at least first-order convergence of the jump to zero);
  - first crossing time converged (last-two ratio in [0.9, 1.1]), or no crossing before t_max.
- **Controls.** All must hold, else NO VERDICT:
  - n = 3 pure power: r in [0.9, 1.1] and |Delta_inf| >= 0.5 |Delta(12800)| (a finite kink);
  - v3s max form: AC16 N3b signature, last-two first-crossing ratio in [1.2, 1.7], or r < 0.9;
  - compatible data under v3s's form (Pi_0 = tanh^3(3 (r - 1))): |Delta(12800)| <= 0.1 |Delta_n3(12800)|.
- **MUTATE** (AC21_MUTATE=1): v3s's max form through the row C1 statistic must FAIL.

## Labels

- **C1 PASS on a curved interface** if both rows pass and the controls discriminate. Together with iter_1's
  T1-T3 (the classical H^s theorem and its hypotheses), iter_6's T4'' (the form exists), T5, T6 and T7, this
  gives 3D PASS for v3s and AC2q with the iter_6 form.
- The numerics cannot see T3's dimension count. They check that curvature does not spoil C1.
