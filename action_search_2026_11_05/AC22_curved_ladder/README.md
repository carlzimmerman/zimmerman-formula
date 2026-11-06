# AC22: curved-interface ladder for AC21's iter_6 smoothing: PASS (curved 2D, C1 and C2)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (81636503ed), frozen and
committed alone before any number. Script ac22.py, which reuses AC21 iter_7's scheme and iter_6's form.json.
Runtime about 25 minutes, 4 workers, nice 15.

## Result

**PASS (curved 2D, C1 and C2, all five form rows); every control discriminates; the MUTATE bites.**

| row | D_inf | order p | D2_inf | sigma_half | sigma_0 | legacy T0 ratio |
|---|---|---|---|---|---|---|
| v3s b 0.2 | +5.4e-6 | 1.50 | +0.11 | -0.021 | -0.095 | 1.015 |
| v3s b 0.4 | +3.4e-7 | 1.04 | +7.1e-3 | -0.009 | -0.102 | 1.018 |
| v3s b 0.8 | +2.1e-8 | 1.00 | +4.5e-4 | -0.005 | -0.119 | **1.164** |
| AC2q b = X 0.2 | +4.6e-8 | 1.01 | +9.7e-4 | -0.006 | -0.088 | 1.074 |
| AC2q b = X 0.4 | +9.2e-8 | 1.01 | +1.9e-3 | -0.006 | -0.052 | 1.032 |
| control n3 (kink) | -0.1385 (finite) | 0.99 | - | 0.000 | -0.001 | 1.001 |
| control m4 | +8.9e-10 | 1.00 | **-1.175** (finite) | 0.000 | -0.005 | 1.000 |
| control v3s max | +266 (diverges) | - | -2.7e6 | **-0.50** | **-0.50** | 1.415 |
| control compatible | +1.3e-10 | 1.00 | -0.93 | 0.000 | -0.001 | 1.002 |

- **C1.** The velocity-gradient jump goes to zero at first order or better. Every D_inf is at most 5.4e-6,
  against the line 0.1 |D_n3| = 0.0139.
- **C2.** The second-derivative jump goes to zero at second order (r2 = 4.000 in every form row). The m = 4 control
  instead holds a finite -1.175. So the run sees the d = 2 count m > 4: the m4 control is C1 but not C2, and the
  form (m = 6) is both C1 and C2.
- **Crossing.** The J <= 1/2 event converges in every form row (|sigma_half| <= 0.021). In v3s's max form it
  collapses as N^-1/2 (sigma -0.50, AC16's N3b), so the max-form interface is crushed at once and the smoothed one
  is not.
- **MUTATE** (v3s max form through the row C1 statistic): FAIL, exit 1. It bites.

## What changed from AC21 iter_7, and why

AC21 iter_7 stays **C1 FAIL as frozen**; AC22 does not relabel it. iter_7's crossing line was a +-10% band on a
single two-rung ratio of the first J = 0 cell event. That event is non-monotone at fixed physics, so the line
tested noise. AC22 uses:
- a log-log slope over the last four rungs;
- a better-posed event (J <= 1/2);
- a ladder to N = 51200;
- fresh data.

The criteria disclose that this choice was made after iter_7's numbers. iter_7's own statistic is reported here as
LEGACY, and on AC22's ladder it would fail one row too: v3s b 0.8, ratio 1.164.

## Caveat on the record

The J = 0 events in the form rows drift slowly downward (sigma_0 -0.05 to -0.12, inside the frozen line -0.35).
The last steps of v3s b 0.8 steepen: 0.120 to 0.103. The J = 0 event comes after the J <= 1/2 event, in the window
where AC20 found ordinary gas shocks forming on the stiff side. The frozen statistic treats it as converged-or-slow.
A slow approach of the J = 0 event to zero after shock formation is not excluded by this ladder. It would be a
post-shock (weak-solution) matter, which is out of scope.

## Optional fold rerun (report only)

Not run. AC10/AC14's first folds sit on soft labels (Pi <= 0), where max(Pi, 0) and the iter_6 form are both
identically zero, so the first fold is unchanged by construction. This is an argument, not a run.

## Scope

- PN charge-velocity system with a transverse switch, axisymmetric 2D, local in time.
- The 3D count (m > 5) is analytic only (AC21 iter_1 T3 and Lean). This run checks the d = 2 count, not the proof.
- In this stiffness-only harness, AC2q enters as v3s with b = X and FRW-level background charge (Pi J conserved,
  AC10). The soft-side gravity term is absent, as in AC16, AC20 and AC21.
- Shocks and soft-side caustics are untouched. No data are graded. Nothing is adopted.
