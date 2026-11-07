# FS1: shock-capturing label for AC14's open door (AC2q planar fold vs v3s): NO VERDICT (frozen; K-visc fails)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Both footings are graded and never pooled. Criteria:
CRITERIA.md (f716e2f98f), committed alone before any script or graded number. The prototype probes are
disclosed there.

## What was built

AC10's planar label system is imported unchanged, and so are AC14's grid of 240 AC2q rows plus their 240 v3s
twins. Only the integrator is new (scheme S). It has four parts:
- Pressure is written in conservative Lagrangian form, p = gamma Pic/(2J^2). That is AC10's
  -gamma d_x(Pic/J) in flux form, so shocks get Rankine-Hugoniot speeds.
- A Christensen-limited quadratic + linear shock viscosity acts on pressure cells only. Dust rows are therefore
  exactly AC10's system.
- Time stepping is SSP-RK3 with a CFL step, and a cubic-Hermite event finds the interior J_thr crossing.
- The core is C (`fs1_core.c`), checked against a numpy reference (`fs1_ref.py`, K0, agreement 1e-11).

**It runs past the first edge fold on every row** (480 of 480; AC14 stalled on 296). All 480 rows converged on
N = 2000/4000/8000 at the frozen lines, so no 16000 rung was needed. `fs1.py` runs the ladder, the extra rung and
the checks; `grade.py` grades (output in `grade.out`, `GRADE.json`).

## Checks

| check | outcome |
|---|---|
| K0 core = reference | PASS (max 1.3e-11) |
| K1 zero-charge vs two-label | PASS (1.2828263548 vs 1.2828263548; delay/v_cross 0.99942) |
| KA1 AC14's 24 soft FOLD pairs | PASS: max \|r-1\| 4.07e-6 (<= 5e-6); fold times = AC14's to 1.97e-6 |
| KA2 AC10's first fold over all cells (23 converged rows) + AC10 K1 | PASS: max 3.7e-4 (<= 2.5e-3); K1 1.6e-10 |
| K2/K3 (stress rows; J tolerance posed in time-at-level) | PASS: outcomes match prediction and per-label equation on all 4. Time-at-level worst 1.3e-3 (A1) / 3.0e-3 (A2), line 5e-3. No-fold J 3.1e-5 / 1.1e-4 where J >= J_reg |
| MUTATE-A repulsive sheet | bites (REGULAR, J_min 1.0) |
| MUTATE-B Mach 0.3 power gate | **bites** (REGULAR, J_min 0.911, converged). AC14 could not run it |
| MUTATE-P1 planted Sigma_b +3 %, dust | bites: equals the two-label prediction to 2.5e-12; DIFF-TIME r 0.977 |
| MUTATE-P2 planted, stiffness on (canonical 11 kpc phantom) | bites: DIFF-TIME r 0.972 |
| MUTATE-P3 planted, clock-pressure shock | bites: DIFF-TIME r 0.976 |
| K-dt (cfl 0.2, sheet step halved; 40-row sample) | PASS (max 8.0e-4) |
| **K-visc ((c_Q, c_L) doubled; 40-row sample)** | **FAIL**: phantom fold times move by up to 8.0 % (18 of 32 FOLD rows exceed 2.5e-3); 2 HELD rows' J_min move by 10.2 % (line 10 %) |
| X > 0 | holds (min X/X_bg 0.999999) |

## Pairs (graded with the frozen pair logic; the label is NO VERDICT because K-visc fails)

| footing | kind | outcome | n |
|---|---|---|---|
| both | soft (stiffness off in the interior) | SAME-FOLD | 40 + 40 |
| canonical / alt | phantom | SAME-FOLD | 29 / 28 |
| canonical / alt | phantom | SAME-HELD (shock-held in both, J_min 1.3e-3 to 3.8e-3) | 11 / 12 |
| canonical / alt | clock-only | **DIFF-TIME, EARLIER** (r 0.9468-0.9471) | 40 / 40 |

The r range over all FOLD pairs is 0.9468 to 1.0033.

**Clock-only pairs.** AC2q's uniform clock charge s^2 gives the whole stream a tiny pressure,
c0 = 2e-5 to 1.1e-4. The stream's leading cells then shock at the sheet instead of crossing through it as v3s's
dust does. The first interior cell reaches J_thr when that shock arrives (shock_at_fold on all 80), 5.3 % before
v3s's free fold.
- This is not a regularization. AC2q reaches the compression threshold earlier, not later.
- K4 (reported, not gating): with pressureless edge cells (E-b) the difference goes away. 70 pairs become SAME-FOLD
  and 10 (alt) UNRESOLVED. So it is carried by the stream's own leading part, the physical front of a uniformly
  charged clock stream.

## Post-result reading (`post_visc.py`, `POST_VISC.json`; information only, not a label)

1. On the frozen K-visc sample, doubling the viscosity shifts each phantom pair's AC2q and v3s fold times together.
   The ratio moves by at most 5.6e-4, and no class changes. The absolute time is set inside the captured shock
   layer: the J_thr cell sits in the shocked layer, whose minimum J is viscosity-set at fixed cell count, a
   wall-heating-type error. That is why the ladder converges while K-visc fails.
2. The frozen sample (every 8th stiffness-on row) happened to hold phantom rows only. On 20 clock-only rows the
   viscosity was rerun at x2 and x0.5: r moves by at most 1.0e-4 and stays 0.9470-0.9472. So the clock-only
   EARLIER result is not viscosity-set.

## What it means

- The frozen label is NO VERDICT. The criteria demanded absolute fold times free of viscosity, and the phantom
  rows' shocked-layer reading does not give that.
- Bracket: 137 SAME-FOLD, 23 SAME-HELD and 80 DIFF-TIME (clock-only, EARLIER, edge-carried); no OPEN or
  UNRESOLVED pair; r in [0.9468, 1.0033].
- No pair anywhere shows AC2q regularizing a v3s fold (no REGULARIZES row):
  - wherever the stiffness is off, or both models carry it (phantom), AC2q = v3s;
  - where only AC2q carries pressure (clock-only), its stream reaches the threshold about 5 % earlier, through a
    shock.
- AC14's open door is narrowed, not closed by label. Two numerical defects are gone:
  - the stall at the first edge fold;
  - the dead power gate.
  What remains is a measurement-definition problem: J_thr read inside a captured shock is viscosity-dependent in
  absolute time.
- A successor lane would need a reading that is not set inside the shock, for example pair-ratio lines or a
  shock-front position. It would have to be frozen before use.

Out of scope, as frozen: evolution after the interior fold, 3D, the hold law, and the moving Sun.
