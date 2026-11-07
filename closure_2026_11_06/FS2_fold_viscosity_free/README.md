# FS2: viscosity-free fold reading for AC14's open door (AC2q planar fold vs v3s): DIFFERS (frozen)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Both footings graded, never pooled.

Criteria: CRITERIA.md (1a686ed9a2). It was committed alone, before any script or FS2 number. No probe was run.

## What changed from FS1

FS1 (f716e2f98f) was NO VERDICT only because K-visc failed. Its J_thr = 1e-3 reading in pressure-carrying rows sits inside the captured shock layer, and the viscosity sets it.

FS2 keeps FS1's physics, rows, scheme S, ladder and stopping rule. Only the graded reading changes. It is now **t_reg, the first time min interior J reaches J_reg = 0.05**:
- J_reg is AC10's own regularization line.
- Every row is hypersonic down to J_reg: c_E <= 0.063 against a stream speed of 1.
- So the crossing is either a smooth collapse or the arrival of a shock. Neither reads J inside the shock profile.

The reason was frozen in advance; see CRITERIA.md.

`fs2_core.c` is FS1's core with read-only level events added. `fs2_ref.py` is an independent numpy reference. `fs2.py` runs the ladder, the extra rung and the checks. `grade.py` writes `grade.out` and `GRADE.json`.

## Checks (all gating, all PASS)

| check | outcome |
|---|---|
| KA = FS1's numbers | all 1455 FS1 rungs reproduced bitwise (max rel 0, step counts equal); FS1 bracket 137/23/80 recomputed; FS1's 40 x2-viscosity files equal |
| K0 core = reference (incl. level times) | max 1.3e-11 |
| K1 two-label at J_reg / J_thr | 3.7e-11 / 3.8e-11 abs; delay/v_cross 0.99942 |
| K2/K3 stress rows | pass (time-at-level worst 1.3e-3 / 3.0e-3, line 5e-3) |
| **K-visc x2 / x0.5 (100 rows: phantom, clock-only, soft + twins)** | **PASS: t_reg moves <= 3.5e-5 / 2.3e-5; no class change** |
| K-dt | 1.8e-8 |
| MUTATE-A | REGULAR, J_min 1.0 |
| MUTATE-B Mach 0.3 | REGULAR, J_min 0.911, converged |
| MUTATE-P1/P2/P3 planted Sigma_b +3 % | all DIFF-TIME (r 0.977 / 0.975 / 0.976); P1 equals the two-label prediction to 3.8e-12 |
| X > 0 | min X/X_bg 0.999999 |

All 480 rows converged at 8000 vs 4000. No 16000 rung was needed.

## Result

| footing | kind | outcome | n |
|---|---|---|---|
| both | soft | SAME-REACH | 40 + 40 |
| both | phantom | SAME-REACH (r 0.99990-1.00004) | 40 + 40 |
| canonical | clock-only | **DIFF-TIME EARLIER**, r 0.98772-0.98794 | 40 |
| alt | clock-only | **DIFF-TIME EARLIER**, r 0.98767-0.98792 | 40 |

- The minimum DIFF margin over the 1e-2 line is 1.9e-3. The largest ladder error is E 2.1e-4, and the largest viscosity shift is 3.5e-5.
- The largest SAME |r - 1| + E is 2.1e-3.
- No row is REGULAR, and no pair shows AC2q regularizing.

**Reading:**
- AC2q's uniform clock pressure s^2 makes the leading stream cells shock instead of crossing the sheet. That shock reaches J_reg 1.2 % before v3s's dust collapse; at J_thr, FS1 saw 5.3 %.
- K4 E-b (edge cells pressureless) gives SAME-REACH on all 80 pairs (r 1.0004-1.0008). The difference is carried by the stream's own front: the clock charge runs uniformly to the stream ends.
- Where both models carry the stiffness (phantom), or neither does in the interior (soft), AC2q collapses exactly like v3s.

**Reported, not graded:**
- Shock flag at the J_reg crossing: all phantom (both models) and all clock-only AC2q rows; no soft or dust rows.
- FS1's J_thr reading is recomputed exactly as FS1 had it.
- Viscosity sensitivity by level:
  - at J >= 0.01, <= 1.7e-4;
  - at J = 0.005, 2.7-5.7 %;
  - at J = 0.002, 11-15 %;
  - at J_thr, 8-11 %.

  So the shock layer starts to set the reading below J ~ 0.01. J_reg sits clear of it.

## Not decided

- Whether a shock-held stream's post-shock J lies above or below J_thr. That is viscosity-set at this resolution.
- Evolution after the interior J_thr event.
- 3D, the hold law and the moving Sun.
