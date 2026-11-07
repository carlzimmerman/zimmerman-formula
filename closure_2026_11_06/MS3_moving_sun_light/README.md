# MS3: the moving-Sun door (v3s, AC2q): PASS (moving Sun, scoped), FINAL

Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

- **Criteria.** CRITERIA.md was committed alone and pushed first (local 3fda68e599, origin b7017db2bd),
  before any script, run or number.
- **Scripts.** The solver is hydro_ms3.py, whose diff from AC24's hydro_ac24.py is committed as
  hydro_ms3.diff. The grader is ms3_grade.py. Both were pushed in cf59388b97.
- **Outputs.** MS3.json and ms3.out hold every number below. ka5a_selftest.out holds KA5(a).
- **FINAL.** Per the owner's 11-07 direction, this is the FINAL label for the moving-Sun door. There is no MS4.

## Checks (all pass)

| Check | Result |
|---|---|
| KA1 | MS2 reproduced exactly: 298 values of MS2_interim.json, 0 mismatches at 1e-12. |
| KA2 | Plant recovery under the fixed-radius readout on all four rungs at both M: worst 0.615 % (line 1 %). |
| KA3 | Procedure checks pass, including the C3 synthetic additive plant. |
| KA4 | Both ultra runs reached t = 1000 with no NaN (M234 311 280 steps, 35 272 s; M490 310 701 steps, 35 187 s). |
| KA5 | (a) The chunked right-hand side equals the whole-grid one bit for bit, at both M, on the fine and ultra grids, for chunks 64 / 37 / 1000. (b) A coarse M234 rerun equals AC24's five snapshots bit for bit. |
| CONV | 0 failing series on (medium, fine, ultra). |
| MUTATE k = 2 | Under C3, reads FAIL everywhere: min L 1.937. |
| MUTATE k = 0.1 | Under C3, reads PASS: max U 0.324, 0 failures, 0 near-failures. |

**CONV classes.**
- q: all 168 series TINY_ABS.
- q_B at M234: 60 NOISE, 17 MONOTONE, 7 TINY_ABS.
- q_B at M490: 42 MONOTONE, 24 NOISE, 12 OSCILLATORY, 6 TINY.

**Information only.** MS2's direct R4 rule applied to the planted series also reads right: k = 2 min L 1.862,
k = 0.1 with 0 failures.

## Label and bracket

**PASS (moving Sun, scoped).** Every U < 1 in every cell, gate, bracket and reading. No cell fails.

[min L, max U] as a ratio to the line:

| Gate | Bracket | Worst-U location |
|---|---|---|
| G1 Earth | [0, 0.040] | |
| G1 Mars | [0, 0.617] | M490 REFLECT, q_B, alt footing, Lstar 24.6, V 220 |
| G1 Saturn | [5.2e-6, 0.221] | |
| G2 Earth | [0, 0.042] | |
| G2 Mars | [0, 0.173] | |
| G2 Saturn | [1.8e-6, 0.153] | |
| G3 Cassini | [1.6e-7, 0.063] | |

The margin is set by G1 Mars at 0.617 of the 1.4e-15 m/s^2 line.

## What carries the PASS (stated plainly)

**The fourth rung did not make q_B converge in the Richardson sense at M234.** M234 q_B is graded mostly as
NOISE. Its rung changes now lie within the five-snapshot time spread:

- the fine run's swing (G1 Mars 0.021-0.036) is about as large as the rung differences;
- ultra moved some series back up (G1 Earth 4.5e-3 to 7.4e-3).

At M490, G1 Mars and G2 Mars q_B read OSCILLATORY:

- fine to ultra rises from 0.050 to 0.078;
- the ultra time spread is 0.083.

Their brackets [min X - D - S, max X + D + S] are wide (U up to 0.19 on the ladder). Transferred to the
REFLECT medium bracket by R5's ratio, that gives the 0.617.

So the PASS rests on the frozen time-spread classes (NOISE, OSCILLATORY), not on a converged extrapolation.
Every rung mean on every series is at most 0.147 of its line (MS2) or 0.078 (ultra).

## Diagnostic D (reported)

The fine to ultra change in the q_B charge is still 99.8 % at r > 100 R_A, at both M.

## Deviation disclosed (operational, not arithmetic)

The first ultra launch hit the frozen RSS guard: peak 1508 MB (M234) and 1402 MB (M490) against 450 MB.
Both runs checkpointed cleanly at step 2000.

- tracemalloc showed live numpy memory of 157 MB (peak 185 MB).
- The excess was the macOS allocator keeping freed medium-size blocks.
- The runs resumed from their checkpoints with the environment variable MallocMediumZone=0. RSS was then
  about 225 MB each, under the guard throughout.
- This setting is not in CRITERIA.md. It changes allocation only, not any floating-point operation; KA5 is
  bitwise.
- The launch-1 logs are kept locally and are not committed.

Scope as AC15, AC24, MS1 and MS2: PN order, mu_K = 0, screening term dropped, axisymmetric, the Sun as a
point mass outside 2 R_A plus the Bernoulli core cap, and the Euler shock proxy. The R5 bracket transfer is
a scope assumption. No PPN alpha_1 or alpha_2 is claimed. AC2q differs by s^2/rho0 ~ 4e-6.
