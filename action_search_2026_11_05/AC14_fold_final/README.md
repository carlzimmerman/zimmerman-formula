# AC14: final label for AC2q's planar fold vs v3s: NO VERDICT (frozen)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (ad9d747016), committed alone
before any code. AC10's physics is imported unchanged (`../AC10_nonlinear_clock/ac10.py`). The full grid was run:
240 AC2q rows and 240 v3s twins, plus 4 stress rows, K1, and both MUTATEs.

Scripts:
- `ac14.py`: device E1 (stiffness taper inside the excluded edge cells), interior first-fold reading, and an extra
  rung at N = 16000 for rows that are not converged. Results are checkpointed per row in `parts/` and
  `parts_MUTATE/`.
- `grade.py`: the frozen lines. Output in `grade.out` and `GRADE.json`.

## Result

| item | outcome |
|---|---|
| K0 (E1 inert at gamma 0) | PASS, fold times identical to AC10's |
| K1 | PASS (coupled 1.2828263550 vs pair 1.2828263548; delay/v_cross 0.9994) |
| K2/K3 (own crossing speed) | **FAIL on the frozen J tolerance only** (see below) |
| MUTATE-A (repulsive sheet) | bites (REGULAR, J_min 1.0) |
| MUTATE-B (Mach 0.3 power gate) | **does not bite**: the solver stops (step underflow) at J_min 1.0, so the row is UNDECIDED, not REGULAR |
| physical pairs, stiffness off in both models (soft rows with Pi <= 0) | 24 of 240: AC2q FOLD = v3s FOLD; max \|t_AC2q/t_v3s - 1\| = 4.7e-6 |
| physical pairs, stiffness on | 216 AC2q rows UNDECIDED (solver stop, interior J_min 0.16-0.41). The same holds for 80 phantom v3s twins. Clock-only and soft v3s twins with Pi <= 0 FOLD |
| X > 0 | holds (min X/X_bg > 0.99) |

**K2/K3 detail.**
- The fold/no-fold outcome with each slab's own crossing speed matched the prediction and the exact per-label
  equation on all four rows:
  - A1: v_c = 1.14, omega v_c = 0.51 gives a fold; v_c = 1.31, omega v_c = 1.31 gives no fold.
  - A2: v_c = 1.09, Omega v_c = 0.69 gives a fold; Omega v_c = 1.55 gives no fold.
- The frozen J-agreement tolerance (<= 1e-3) holds on the two non-folding rows (3e-5 and 1e-4).
- It fails on the two folding rows (0.12 and 0.28). There J -> 0, and the relative difference floored at 1e-2 is
  not a meaningful measure. That is a defect in how the tolerance was written. It is reported and was not
  amended.

## What it means

The frozen label is NO VERDICT. The failure is in the method, not the physics: no row in the grid violates
"AC2q folds like v3s".
- Wherever the stiffness switch is off, AC2q and v3s fold at the same time to 5e-6.
- Wherever it is on, the explicit (DOP853) inviscid label code cannot get past the first edge fold. This happens in
  v3s too.
  - E1, the declared edge taper, did not remove the problem.
  - E1 made the stiff gate row (MUTATE-B) unrunnable, so the frozen power gate fails.
- AC10's subset reading is unchanged:
  - first fold = v3s to 0.3 %;
  - nothing AC2q-specific regularizes.
  It remains supporting evidence, not a label.

The honest closing answer to "does AC2q fix caustics?" is still the inference: no. AC2q's planar PN system is v3s's
with the charge shifted by s^2 (AC10 S1), and the clock's own pressure scale is Hubble-sized. The frozen
FAIL-SAME-AS-V3S label needs two things this code does not have:
- an implicit or shock-capturing integrator for the stiffness-on rows;
- a fixed K2/K3 tolerance.

Out of scope, as frozen: the post-fold stiffness-shock interior, 3D, the hold law, and the moving Sun.

Note: PAPER69 (97e742ddf3) cites "293 of 482 parts UNDECIDED" (a count not reproduced here, probably read
while the grid was running). The final count is 296 UNDECIDED physical rows (216 AC2q + 80 v3s). The verdict is the same.
