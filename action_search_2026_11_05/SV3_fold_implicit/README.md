# SV3: AC14 successor, implicit integrator. Planar AC2q fold vs v3s on the declared subset: NO VERDICT (frozen)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing.
- Criteria: FROZEN_CRITERIA.md (2febd29269), committed alone before any graded number. It was written after
  AC14's NO VERDICT, and AC14's failure modes are listed there.
- Physics: AC10's, imported unchanged in the interior (`../AC10_nonlinear_clock/ac10.py`). No AC10 or AC14 file
  was edited.

## Scripts

- `sv3.py`: the method changes declared in the criteria:
  - I1, Radau IIA with an analytic sparse Jacobian;
  - E3, pressureless edge cells with a transmissive interface ghost;
  - E3b, the ghost variant used by the K4 check;
  - a per-run cap of 1500 s; per-rung checkpoints in `parts/` and `parts_MUTATE/`; SIGTERM-safe stops.

  One change was made after the freeze, for scheduling only. A `--reverse` flag let a third process take rows
  from the other end of the list once the MUTATE process was done. Numerics are unchanged.
- `grade.py`: the frozen lines. Output in `grade.out` and `GRADE.json`.
- Compute: nice 15, at most 3 processes. About 3.7 CPU-hours, 1h20 wall. 0 timeouts; the longest single run
  was 642 s.

## Result

| item | outcome |
|---|---|
| K0 (Radau vs AC10 DOP853, gamma 0) | PASS: 1.3e-10 and 2.1e-7 (line 1e-6) |
| K1 | PASS (coupled 1.2828263548 vs pair 1.2828263548; delay/v_cross 0.9994) |
| K2/K3 (i) fold/no-fold outcome | matches the prediction and the per-label equation on all 4 rows |
| K2/K3 (ii) fold-time agreement (line 5e-3) | A1_0.2: 1.3e-3; A2_0.4: 3.0e-3. PASS |
| K2/K3 (iii) J agreement where J >= J_reg (line 1e-3) | no-fold rows 3.1e-5 and 1.1e-4; **fold rows 4.0e-3 (A1_0.2) and 8.1e-3 (A2_0.4): FAIL** |
| MUTATE-A (repulsive sheet) | bites (REGULAR, J_min 1.0) |
| MUTATE-B (acoustic power gate, Mach 0.3) | **bites** (it did not in AC14). Pressure row REGULAR on every rung, J_min 0.652. Dust twin FOLD at 5.494502 vs analytic 5.4945 (4e-7) |
| MUTATE-C (K4 has power) | bites: E3a FOLD at 2.483; the vacuum ghost is UNDECIDED (solver stop) |
| X > 0 | holds (min X/X_bg 0.9999998) |

Physical subset: every 5th of the 160 stiffness-on AC2q rows, so 32 AC2q rows and their 32 v3s twins.
- **No subset row stalls.** I1 and E3 carry every stiffness-on row past the edge-cell folds that stopped AC14.
- **Every rung of all 64 rows reads FOLD.** No row, and no rung, is REGULAR.
- **8 pairs are fully decided.** These are clock-only rows (FOLD in both models, converged, K4-clean). Max
  |t_AC2q/t_v3s - 1| = 6.7e-4.
- **24 rows are UNDECIDED, on K4 only.** E3b moves the fold time by 1.2e-3 to 1.6e-3, against a 1e-3 line. The
  rows are:
  - 8 AC2q clock-only rows at Lstar 90 pc;
  - 10 phantom pairs (AC2q and v3s alike).
- **12 phantom rows (6 pairs) are NOT CONVERGED.** The ladder fold time still drifts by 1.6e-3 to 5.9e-3 between
  8000 and 16000, at 11 and 33 kpc, where gamma ~ 5e-4 to 8e-3. Pressure delays the front-cell fold by up to
  11 % there (1.42 vs dust 1.28), and the delay depends on resolution.
- Across all 32 pairs at the final rung, regardless of status, max |t_AC2q/t_v3s - 1| = 3.1e-3. That is inside
  the 1e-2 pair line, but it is not a label.

**Frozen verdict: NO VERDICT.** Three things block it:
1. K2/K3 (iii) fails on the fold rows.
2. 24 subset rows are UNDECIDED (K4 edge-sensitive).
3. 12 subset rows are NOT CONVERGED.

## What it means

- The integrator problem behind AC14 is fixed. The implicit method with pressureless edge cells runs every
  stiffness-on row to the interior first fold, and the power gate now bites. The method can see pressure
  regularization: the acoustic Mach 0.3 row stays regular while its dust twin folds on time.
- Even so, no subset row regularizes. AC2q and v3s fold at the same time within 3.1e-3 on every pair.
  - On the decided pairs the agreement is within 6.7e-4.
  - AC2q's extra s^2 pressure only delays clock-only folds by about 0.1-0.3 %.
  - So nothing in the subset contradicts "AC2q folds like v3s".
- The frozen label is still blocked by method, not by any row going the other way:
  - The graded cell is the front-most interior cell, which borders the edge treatment. Its fold time moves by
    about 1.5e-3 between ghost variants.
  - The strongest-stiffness phantom rows have grid-dependent pressure delays.
  - The fold-row J tolerance (iii) was set at 1e-3, and the measured mismatch at J >= J_reg is 4e-3 to 8e-3.
    These fold rows have gamma 0, so the mismatch reflects how the coupled code differs from the isolated
    per-label pair near the fold. It is not stiffness.
- None of these lines was amended after the result.

A successor would need three things:
- a reading cell away from the edge, for example the first fold beyond a sound-crossing distance from the
  interface;
- a K4 line derived from the measured ghost-variant spread, set before any run;
- a resolution study, or a shock-capturing scheme, for the gamma >~ 5e-4 phantom rows.

Out of scope, as frozen:
- the post-fold interior;
- 3D;
- the hold law;
- the moving Sun;
- the 128 stiffness-on AC2q rows outside the subset, for which no label is claimed.
