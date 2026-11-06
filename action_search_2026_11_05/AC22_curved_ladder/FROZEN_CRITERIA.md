# AC22 frozen criteria: settle the curved-interface numerics for AC21's iter_6 smoothing

Frozen before any AC22 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.
Lane rules: closure_2026_11_06/SWARM_BRIEF.md.

## Why

AC21 (63242d3e1e) proved analytically that a classical 3D theory across the stiffness switch needs a pure power
Pi^m near 0 with m > d + 2. Its iter_6 form meets this: Pi^6 near 0, C4 blend to (gamma/2) Pi^2 above b, with
b = rho_DE for v3s and b = X for AC2q. iter_7 tested it on a curved (circular) switch in an axisymmetric 2D
Lagrangian scheme.
- The b = 0.8 row passed.
- The b = 0.4 row's jump converged to zero (Delta_inf 4e-5, r 2.37), but its first-crossing ratio was 1.1045
  against a [0.9, 1.1] line.
- iter_7 stays **C1 FAIL as frozen**. Nothing here relabels it.

## Was iter_7's crossing line the right statistic?

No, and that is the reason for this new iteration. It is not a reason to move iter_7's line.

- The line's job was to tell v3s's immediate crossing (AC16 N3b: first crossing time falls as N^-1/2, ratio
  sqrt(2) = 1.414 per doubling) from a crossing at a finite continuum time (ratio near 1).
- It used one two-rung ratio of a discrete event: the first Lagrangian cell to reach zero area (J = 0). That
  event is non-monotone at fixed physics. iter_7's b = 0.4 times went 0.0917, 0.0956, 0.0896, 0.0812 on
  successive rungs, so a +-10% band on one ratio is a noise test, not a convergence test.
- AC22 replaces it with:
  - a fit over the ladder's last four rungs;
  - a better-posed event, J <= 1/2 (cell area halved), which converges smoothly when the solution is classical.
- Disclosure: this choice was made after seeing iter_7's numbers. iter_7's own statistic is also computed on
  AC22's ladder and reported as LEGACY, not used for the label.
- AC22 runs on fresh initial data that no earlier lane has seen.

## Scheme (as iter_7, extended)

- Axisymmetric Lagrangian charge-velocity scheme, switch on the circle r = 1, r in [0.25, 3.25]; code reused from
  AC21 iter_7 (iter_6 form evaluated by local Horner pieces, form.json).
- Stiffness force h(Pi) = F'(Pi)/gamma, and h = b f'(Pi/b) for the iter_6 form. Pi is carried by the labels.
- RK4 in time, dt = 0.1 da. Measurement at t_meas = 0.01. t_max = 2.0.
- Ladder: N = 800, 1600, 3200, 6400, 12800, 25600, 51200 (seven rungs; iter_7 stopped at 12800).
- Formal order: the C1 jump statistic is the difference of one-sided linear-fit slopes over 4 cells. For a
  classical (C2-across) solution its bias is O(dx), first order. Hence the order line p >= 0.8 below, set from the
  scheme, not from data.
- **AC2q configuration.** AC10's planar PN system for AC2q has per-label charge Pi = D.P + s^2 with Pi J conserved
  (AC10 criteria line 28, J'' = ... + K(M-1)(Pi_0 - s^2 J), and ac10.py's Pi = Pic/J). The stiffness is the same
  functional of the carried Pi as in v3s, so in this stiffness-only harness AC2q differs from v3s only through:
  - b = X = s^2/2, with N = 1 at PN order;
  - its background charge, which sits at the FRW value Pi = 2X = 2b.

  AC2q rows therefore use charge data that tend to 2b on the stiff side. The soft-side gravity term
  K(M-1)(Pi_0 - s^2 J) is lower order and absent here, as in AC16, AC20 and AC21.

## Data (fresh)

- v3s rows: Pi_0 = tanh(2.5 (r-1)) + 0.1 sin(2 (r-1)); v_0 = 0.1 cos(1.3 (r-1)) + 0.05.
- AC2q rows: Pi_0 = 2b tanh(2.5 (r-1)) + 0.1 b sin(2 (r-1)); same v_0.
- Each crosses zero transversally at r = 1 with slope > 0.
- Compatible-data control: Pi_0 = [tanh(2.5 (r-1))]^3 under v3s's max form.

## Rows

- Form rows (iter_6 form): v3s at b = 0.2, 0.4, 0.8; AC2q at b = 0.2 and b = 0.4.
- Controls:
  - n3: h = Pi^2 (F ~ Pi^3), the finite kink;
  - m4: h = Pi^3 (F ~ Pi^4);
  - v3s: h = Pi (the max form);
  - compatible: v3s max form on the compatible data.

## Statistics per row

- D(N): jump in dV/dr across the interface at t_meas (one-sided linear fits, 4 cells each side).
  - D_inf = 2 D(Nmax) - D(Nmax/2).
  - r = |D(Nmax/2)| / |D(Nmax)|.
  - Observed order p = log2(|D3 - D2| / |D2 - D1|) over the last three rungs.
- D2(N): jump in d^2V/dr^2 across the interface (one-sided quadratic fits, 8 cells each side); D2_inf likewise.
- T_half(N): first time any cell with |r-1| < 0.5 reaches J = area/area_0 <= 1/2. sigma_half = log-log slope of
  T_half vs N, least squares over the last four rungs (6400 to 51200).
- T0(N): the same for J <= 0 (iter_7's event); sigma_0 likewise.
- LEGACY: iter_7's line, T0 ratio at the last two rungs in [0.9, 1.1]. Reported only.

## Lines

- **C1 PASS (row):**
  - |D_inf| <= 0.1 |D_n3(Nmax)|;
  - p >= 0.8, or |D(Nmax)| <= 1e-6;
  - sigma_half >= -0.15 (or no J <= 1/2 event before t_max on the last four rungs);
  - sigma_0 > -0.35 (or no J <= 0 event).
- **C2 PASS (row):** |D2_inf| <= 0.1 |D2_inf(m4)|.
- **Controls** (all must hold, else NO VERDICT):
  - n3 kink: r in [0.9, 1.1] and |D_inf| >= 0.5 |D(Nmax)|.
  - v3s collapse: sigma_half <= -0.35 or sigma_0 <= -0.35 or r < 0.9.
  - compatible: |D(Nmax)| <= 0.1 |D_n3(Nmax)|.
  - m4 separates C2 from C1: m4 passes C1, and its D2 has a finite non-zero limit,
    |D2(Nmax/2)| / |D2(Nmax)| in [0.8, 1.25] and |D2_inf(m4)| >= 0.5 |D2(m4, Nmax)|.
- **MUTATE** (AC22_MUTATE=1, separate outputs): v3s's max form through the row C1 statistic must FAIL (exit 1).

Why m4 is the C2 control. Its velocity jump is C1 with a finite second-derivative jump, because h''' = 6 Pi'^3 is
non-zero at the interface. For m >= 5, h''' vanishes at the interface. So the C2 statistic separates m <= 4 from
m >= 5, which is the d = 2 count m > d + 2 = 4. This checks the count in the dimension the run lives in
(axisymmetric 2D). It is not a proof. The 3D count (m > 5) stays analytic: AC21 iter_1 T3 and Lean.

## Labels

- **PASS (curved 2D, C1 and C2):** every form row passes C1 and C2, and all controls hold. Together with AC21's
  analytic results this makes the iter_6 form the switch repair, scoped as AC21 states: PN charge-velocity
  system, local well-posedness, transverse data, shocks and soft-side folds untouched.
- **FAIL as frozen:** a form row misses a line while the controls hold. The failing rows are named.
- **NO VERDICT:** a control fails.

## Optional, report only (not graded)

If cheap: AC10-style first-fold rows with max(Pi, 0) replaced by the iter_6 form. AC10's first folds sit on soft
labels (Pi <= 0), where every candidate stiffness is zero, so they are expected unchanged. A run that shows a change
is reported, not graded.
