# MS2 frozen criteria: the moving-Sun door (v3s and AC2q), fixed-radius readout and a fourth rung

Frozen before any MS2 script, run or number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.
No dark-matter particle, no LCDM input. Both footings graded, never pooled. AC15, AC24 and MS1 files are
read only.

## Why, and what was seen before this freeze

MS1 (af5d153290 / 5a818344be) is NO VERDICT for two reasons. All of MS1's printed numbers were seen
before this freeze. They are listed here because the choices below were made knowing them.

1. MUTATE k = 0.1 failed. The planted anomaly is exact and grid-independent, yet it read 0.1015, 0.1015
   and 0.0989 on the three rungs.
   - Cause, from the code: AC15's field() reads at the nearest radial edge, rp = re[argmin|re - rp0|],
     not at the planet's radius rp0.
   - The edge is up to dln/2 from rp0 in ln r. For a monopole read at r^-2, that is up to dln, which is
     5 % coarse, 2.5 % medium and 1.25 % fine.
   - For the l = 2 part (r^-4) it is twice that. AC24's P1 residual (4.6 %) is the same effect.
   - This offset is grid-dependent and not monotone in refinement, so it creates false DIVERGENT and
     OSCILLATORY series wherever the true change between rungs is smaller than it.
2. CONV failed on 52 of 336 series.
   - 39 are DIVERGENT: 24 q_B and 15 q. The q_B ones are all at M234. 15 of the 39 are q series at both M,
     with rung changes of 1e-3 of the line or less.
   - 13 are PRE-ASYMPTOTIC (all q).
   - At M490 every q_B series is MONOTONE.
   - The ladder used only the final t = 1000 snapshot. AC24 had already reported q_B NOT STEADY on the
     medium t = 3000 runs, changing by 10-31 % over the last 20 % of t_end. So the final-snapshot rung
     difference mixes the grid error with the time phase.

## R1. Fixed-physical-radius readout (replaces the nearest-edge readout everywhere)

field_fixed() is AC15's field() with one change: the gates are evaluated at rp = rp0 exactly.

- The cell [lo, hi] containing rp0 is split by volume. Its inner part carries the fraction
  f_in = (rp0^3 - lo^3) / (hi^3 - lo^3) of the cell's charge, at radius r_a = 0.75 (rp0^4 - lo^4) / (rp0^3 - lo^3).
- The outer part carries 1 - f_in at r_b = 0.75 (hi^4 - rp0^4) / (hi^3 - rp0^3).
- Every other line of field() and grade_snap() is unchanged: Legendre l <= 24, core cap, Sun subtraction,
  per-cell M rescale, the G1/G2/G3 formulas, and the lines. G3 divides by rp0.
- This is exact for any charge lying wholly inside or outside rp0, the plants included. It is
  second-order in the cell width for the straddling cell.
- The plants are AC24's make_plant() unchanged. A plant shell (0.5-0.9 rp0) never straddles rp0.

## R2. Time handling of each rung

Each t = 1000 ladder run has five snapshots, t = 800, 850, 900, 950, 1000. For each series (M, reading,
gate, cell), each rung r gives:

- X_r = the mean over the five snapshots;
- s_r = max - min over the five snapshots (the time spread).

## R3. Ladders

- M490: (coarse, medium, fine), as in MS1.
- M234: (medium, fine, ultra). Ultra is a new fourth rung: dln r = 0.00625 and 640 theta cells, half of
  fine in both directions. Its run is TRANSMIT UNIFORM, t_end 1000, M_inf 234, with no other change to
  AC24's solver. The diff from hydro_ac24.py is committed.
- Ultra is run because all 24 DIVERGENT q_B series are at M234. One run covers every M234 series.
- Until ultra finishes, M234 is graded on (coarse, medium, fine) and the result is reported as INTERIM,
  not a label. The label is the grade with ultra.

## R4. Classification (per series; e1 = X_1 - X_2, e2 = X_2 - X_3, coarsest first; S = max s_r)

Applied in this order:

| Class | Condition | Bracket |
|---|---|---|
| TINY_ABS | max(abs(e1), abs(e2)) <= 1e-3 (ratio-to-line units). Convergence only matters at the line's scale. | [min X - 3D - S, max X + 3D + S], with D = max X - min X |
| TINY | abs(e2) <= 0.01 abs(X_3) | [X_3 - 3 abs(e2) - S, X_3 + 3 abs(e2) + S] |
| NOISE | abs(e1) <= s_1 + s_2 and abs(e2) <= s_2 + s_3 (both rung changes within the time spread) | [max(0, min X - D - S), max X + D + S] |
| MONOTONE | 0 < R = e2/e1 < 1 and p = log2(1/R) >= 0.5 | MS1's rule (p_u = min(p, 2), Fs 1.25), widened by S on both sides |
| PRE-ASYMPTOTIC | 0 < R < 1 and p < 0.5 | Computed as MONOTONE; fails CONV |
| OSCILLATORY | R <= 0 | MS1's rule, widened by S |
| DIVERGENT | R >= 1 | Unbounded above; fails CONV |

All lower ends are clipped at 0.

CONV passes when no series is DIVERGENT or PRE-ASYMPTOTIC.

## R5. Brackets graded

These are AC24's brackets.

- **TRANSMIT UNIFORM t = 1000, both M.** The ladder bracket is used directly.
- **Medium-only brackets at t_end 3000:**
  - TRANSMIT at both M, ABSORB at both M, REFLECT at both M, and the HEDGEHOG start at M234;
  - each is read with R1 and graded on AC24's rule: the final value if steady, else the per-cell envelope
    inflated by its change;
  - the bound is [G * L / X_med, G * U / X_med], from the same-M ladder's medium rung;
  - if X_med = 0, the bound is [0, G + U];
  - the transfer is a scope assumption, as in MS1.

## Known answers (each must pass)

- **KA1 (MS1 exactly).** With readout = nearest edge and final-snapshot X, the script must reproduce
  MS1.json's ladder rung values (xc, xm, xf of every worst-U entry) and AC24's medium-to-fine maxima
  0.4964 / 0.5721, to 1e-12 relative.
- **KA2 (readout).** Under R1, the planted-only field (field with plant minus without, AC24's P1
  construction) must equal k to within 1 % on every rung, gate, cell and k in {2, 0.1}. That is against
  4.6 % on the edge readout.
- **KA3 (procedure).** MS1's KA2 synthetic sequences must reproduce, with s_r = 0. AC24's gravity-off
  errors must classify MONOTONE with a bracket containing 0.
- **KA4 (ultra solver).** The ultra run's gravity-off check is not rerun; KA3 of AC24 covers the scheme.
  The ultra run's done.json must show t = 1000 reached, with no NaN in q, u or v.

## MUTATE (must both read right)

AC24's analytic plants are added through R1 on every snapshot of every rung of both ladders, for q and q_B,
and the planted series are classified and bracketed by R4.

- k = 2. L > 1 in every cell, gate, M and reading: reads FAIL.
- k = 0.1. U < 1 wherever the unplanted U + 0.1 < 1: reads PASS. Other cells are reported as
  near-failures, not counted.

If either fails, NO VERDICT.

## Diagnostic D (decides the M234 question; reported; does not move the label)

For M234 q_B, the dq_B charge of the finer of each pair of rungs is volume-averaged onto the coarser grid.
The grids nest by a factor of 2 in r and theta. The absolute difference |delta(dq_B dV)| is summed in
radius bands: [2, 5], [5, 20], [20, 100] and [100, 2000] R_A.

- **R_A-SCALE.** At least 50 % of the medium-to-fine difference lies at r < 20 R_A. Then the M234
  acceleration is called a pre-asymptotic resolution of the accretion / bow-shock scale.
- **TEMPORAL.** The MS1 DIVERGENT series become NOISE under R2.
- **DISTRIBUTED.** Neither.

The same sums for M490 are reported beside it.

## Labels

- **PASS (moving Sun, scoped).** KA1-KA4, CONV and both MUTATEs pass, and every U < 1 in every cell,
  gate, bracket and reading.
- **FAIL.** The same checks pass, and some cell has L > 1 in every bracket for some gate (worse reading
  governs). The line is named: the G1/G2 planet bound (Earth 8.7e-15, Mars 1.4e-15, Saturn 7.0e-15 m/s^2)
  or Cassini Q_eff 5.2e-27 s^-2.
- **UNDECIDED.** The same checks pass, some U >= 1, and no FAIL. The splitting bracket is named.
- **NO VERDICT.** A KA, CONV or a MUTATE fails. The bracket [min L, max U] per gate is reported.

Scope as AC15, AC24 and MS1. No PPN alpha_1 or alpha_2 is claimed. AC2q differs by s^2/rho0 ~ 4e-6.

## Compute

- **Ultra run.** One process, one thread, nice 15. It is checkpointed by hydro's own SIGTERM handler, and
  a killed run resumes from state.npz. It runs in the background. RSS is checked to stay under 1 GB; if
  it does not, the run is stopped and reported.
- **Grading.** One process, nice 15, with a row cache for resume.
- **Expected wall time.** Fine took 11 199 s to t = 1000; ultra is about 8 times that, more under the
  present load.
