# MS1 frozen criteria: the moving-Sun door (v3s and AC2q), the convergence item

Frozen before any MS1 script or number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.
No dark-matter particle, no LCDM input. Both footings graded, never pooled. AC15 and AC24 files are read
only: their code is exec'd and their parts are loaded, never edited.

## Why

AC24 (3f24c64253, criteria 81e48c2a3c) is NO VERDICT as frozen for one reason: its convergence line
(every graded ratio changes <= 30 % from medium to fine at t = 1000) fails, at 0.496 (M234) and 0.572
(M490). The failing numbers are all on the q_B reading. The q reading changes by 0.111 / 0.065. AC24's
grade.out also printed the coarse-to-medium maxima, 0.578 / 0.641. Those four maxima are the only ladder
numbers seen before this freeze; the per-gate rung values in AC24's GRADE.json have not been read for MS1.

## The two routes, decided on the equations before any number

Route 2 (q_B is the wrong reading, drop it) is rejected. From AC15 S1b, the khronon's P equation gives
global Bernoulli exactly, gamma q = c_gal^2 + Phi_N + (V^2 - w^2)/2, across kinks in sigma included. So
q_B is the khronon's own constraint evaluated on the simulated w. The Euler evolution's q is the one that
departs from the khronon at shocks (Rankine-Hugoniot does not conserve Bernoulli). Neither is gauge
invariant in a sense that would let one be discarded. What the equations do say is why q_B converges
slowly. In code units (rho0 = 1, V = 1), q_B = 1 + M_inf^2 [Phi_N + (1 - w^2)/2], so a truncation error
dw in the flow gives dq_B = -M_inf^2 w dw. That is an amplification by M_inf^2 = 5.5e4 to 2.4e5. Numerical
dissipation slows the flow (w^2 < 1 too far), which biases q_B upward. That is consistent with q_B falling
under refinement, but it is a reason, not a bound. Both readings stay graded and the worse one governs,
as in AC24.

Route 1 is taken, on the rungs that already exist. A fourth rung (dln r = 0.00625, 640 theta cells) costs
8 times the fine run: the fine run took 11 199 s of wall time to t = 1000 (done.json), so the fourth rung
would take about 25 h per M_inf. It is not run. MS1 uses the three rungs on disk (coarse, medium and fine
TRANSMIT UNIFORM at t = 1000, both M_inf, in AC24/parts and AC15/parts). It replaces AC24's two-rung
change line with a frozen three-rung Richardson / grid-convergence-index (GCI) bound.

## Series

For each M_inf in {234, 490}, each reading in {q, q_B}, each gate in {G1 Earth, G1 Mars, G1 Saturn, G2
Earth, G2 Mars, G2 Saturn, G3}, and each of the 12 cells (both footings, every Lstar and V): X_c, X_m and
X_f are the gate's ratio to its line at the final t = 1000 snapshot of the coarse, medium and fine runs.
The values come from AC15's field() / grade_snap(), exec'd verbatim as in AC24. The refinement ratio is 2
in both r and theta (and in dt through CFL).

With e1 = X_c - X_m, e2 = X_m - X_f and R = e2 / e1:

- TINY. |e2| <= 0.01 |X_f|. The bracket is [X_f - 3|e2|, X_f + 3|e2|].
- MONOTONE. 0 < R < 1. The observed order is p = log2(1/R) and p_u = min(p, 2), the formal order. Then
  X_R = X_f - e2 / (2^p_u - 1) and E = 1.25 |e2| / (2^p_u - 1), where 1.25 is the standard three-grid GCI
  safety factor. The bracket is [max(0, min(X_f, X_R) - E), max(X_f, X_R) + E].
- OSCILLATORY. R <= 0 (or e1 = 0 with e2 != 0). With D = max - min of the three rungs, the bracket is
  [max(0, min - D), max + D].
- DIVERGENT. R >= 1. The bracket is unbounded above.

## Convergence line (frozen)

CONV passes when every series (both M_inf, q and q_B, every gate and cell) meets both of these:

- C1. The series is TINY, MONOTONE or OSCILLATORY, never DIVERGENT.
- C2. Every MONOTONE series that is not TINY has p >= 0.5, the asymptotic-range line. The scheme is
  formally second order and first order at shocks and clipped extrema, and KA3 measured 1.08-1.40. A
  monotone series with p < 0.5 is called PRE-ASYMPTOTIC. Its bracket is still computed and reported, but
  CONV fails.

## Transfer to the medium-only brackets

AC24's other graded brackets have no fine rung: ABSORB M234 and M490, REFLECT M234 and M490, the HEDGEHOG
start M234, and the TRANSMIT medium runs at t_end = 3000. Each graded value G (per cell, gate and reading,
AC24's rule: the final value if steady, the envelope inflated by its change if NOT STEADY) gets a bound
from the TRANSMIT ladder at the same M_inf (HEDGEHOG uses M234). For the same gate, reading and cell, the
bracket is [G * L / X_m, G * U / X_m], where [L, U] is the ladder bracket. If X_m = 0, the bracket is
[0, G + U]. This assumes the medium-grid error fraction at t = 1000 TRANSMIT holds for the other brackets
and at t = 3000. That is a scope assumption, stated with the label. TRANSMIT t = 1000 is itself graded as
a bracket with its ladder bounds directly.

## Known answers (separate outputs; each must pass)

- KA1 (reproduce AC24). The X_c, X_m and X_f worst-over-cells values must equal AC24 GRADE.json
  `convergence.<M>.rungs` for every reading and gate, and each medium bracket's graded worst-over-cells
  value must equal AC24 GRADE.json `brackets.<b>.<reading>.graded`. Both to 1e-12 relative. AC24's
  medium-to-fine maxima 0.496 / 0.572 must be reproduced.
- KA2 (Richardson on known sequences). X_h = 0.3 + 0.2 h^p with h = 1, 1/2, 1/4, for p = 0.6, 1 and 2,
  must give p back to 1e-10, give X_R = 0.3 to 1e-10 (for p = 2; for p = 0.6 and 1 also, since p_u = p),
  and give a bracket containing 0.3. The sequences (1, 0.5, 0.8) and (1, 1.2, 1.5) must classify as
  OSCILLATORY and DIVERGENT.
- KA3 (Richardson on AC24's KA3 errors). The gravity-off errors (true value 0) for coarse, medium and fine
  must classify MONOTONE with p >= 0.5, and the bracket must contain 0. These three values are AC24's
  published numbers (1.20e-2, 4.55e-3, 2.16e-3), which were seen before this freeze, so KA3 is a check
  of the procedure, not a blind test.

## MUTATE (planted control through the extrapolation)

AC24's analytic plants (MONO for G1_p, QUAD for G2_p, QUAD3 for G3) are added through the same patched
field() as AC24, on each of the three TRANSMIT rungs at t = 1000, both M_inf, q and q_B. The planted
series is then extrapolated by the same rules.

- k = 2. The planted gate's lower bound L must be > 1 in every cell: it must read FAIL.
- k = 0.1. The planted gate's upper bound U must be < 1 in every cell where the unplanted U + 0.1 < 1: it
  must read PASS. Cells where unplanted U + 0.1 >= 1 are reported as near-failures, not counted.

If either fails, the extrapolated reading has no shown power and the label is NO VERDICT. AC24's P1-P3 on
the medium brackets are carried, not rerun.

## Labels

- **PASS (moving Sun, scoped).** CONV, KA1-KA3 and MUTATE all pass, and every upper bound U < 1 in every
  cell, gate, bracket and reading, on both footings.
- **FAIL.** CONV, KA1-KA3 and MUTATE pass, and some cell has L > 1 for some gate in every bracket. The
  line is named (planet G1/G2 bound or the Cassini Q_eff line).
- **UNDECIDED.** CONV, KAs and MUTATE pass, some U >= 1 and no FAIL. The splitting bracket is named.
- **NO VERDICT.** CONV, a KA or MUTATE fails. The bracket [min L, max U] over cells and brackets, per gate
  and reading, is reported with it.

Scope is AC15's and AC24's: PN order, mu_K = 0, screening term dropped, axisymmetric, the Sun as a point
mass outside r_in = 2 R_A plus the Bernoulli core cap, the Euler shock proxy checked by q_B, and the ladder
transfer above. No PPN alpha_1 or alpha_2 is claimed. AC2q differs from v3s by s^2/rho0 ~ 4e-6 in the
charge, as in AC15, and is reported with v3s, not run separately.

## Compute

No new hydro run; grading of snapshots already on disk only. One process, one thread, nice 15. Per-snapshot
gate rows are cached to a JSON file in this directory so that a killed run resumes. RSS is reported.
Outputs: ms1_grade.py, MS1.json, ms1.out.
