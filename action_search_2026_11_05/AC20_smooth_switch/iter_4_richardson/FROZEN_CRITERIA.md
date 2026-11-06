# AC20 iter_4 frozen criteria: fresh-data C1 test with a resolution-independent statistic

Frozen after iter_3's run (the iter_3 numbers are known) and before any iter_4 number. Kappa = 1/2 FITTED; not
theory closed. Adopts nothing.

Why: iter_2 and iter_3 missed the absolute line "|Delta v_x| at finest N <= 0.01005". In every smoothed row the
jump was falling as 1/N (ratios 1.89-1.98 per doubling), but the 4-cell stencil error is about delta x v_xx,
and v_xx is large where the force bends (over the width a or b). An absolute line at finite N therefore cannot
separate "C1, under-resolved" from "kinked". This iteration uses a statistic that can, on NEW initial data that
no earlier run has seen, so the numbers it grades are not ones already looked at.

## Data and rows

Pi_0 = tanh(2q) (c1 = 2), v_0 = 0.2 sin q, gamma = 1, t_meas = 0.03, N = 800 / 1600 / 3200 / 6400 / 12800,
4-cell one-sided slopes (harness, extended with v_0).
Rows: iter_3 spline m = 4 with b = 0.4 and b = 0.2; iter_2 contact form with a = 0.4 and a = 0.2.

## Statistic and lines

- Richardson limit Delta_inf = 2 Delta(12800) - Delta(6400) (signed), and ratio r = |Delta(6400)| / |Delta(12800)|.
- C1 PASS for a row: |Delta_inf| <= 0.1 |Delta_n3(12800)|, r in [1.6, 2.4], and t_inv converged (last-two
  ratio in [0.9, 1.1]).
- Controls (must hold, else NO VERDICT): n = 3 pure power: r in [0.9, 1.1] and |Delta_inf| >= 0.5 |Delta(12800)|
  (a finite kink); v3s (n = 2): r < 0.9 (growing).
- S-a' (sympy): contact order 6 with a C^2 knot (degree 8, q^6 (c0 + c1 q + c2 q^2)): exists, unique, F'' >= 0 on
  [0, 1]. (iter_3's C^3, degree-9 version failed convexity; that stands.)

## Labels

- v3s with the spline (b = rho_DE): REPAIR (1D) if both spline rows pass (S-a, S-b, S-d passed in iter_3).
- AC2q with the spline (b = X): REPAIR (1D) if both spline rows pass (S-e passed in iter_3).
- iter_2 contact rows: C-c regrade only. AC2q with the contact form stays NOT A REPAIR (C-e); v3s with the
  contact form is REPAIR (1D) if both contact rows pass.
- 3D is not graded. The m = 6, C^2 result is reported as existence plus convexity only.
- MUTATE (AC20_MUTATE=1): v3s's F through the C1 statistic must FAIL.
