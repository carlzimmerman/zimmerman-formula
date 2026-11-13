# FRZ5 AMENDMENT A1 (2026-11-13): two twins redesigned, after the as-frozen run

Committed alone, after the as-frozen outputs (dcf2b304de) and before any A1 number exists. The as-frozen labels stand
first: cases A and C are **NO VERDICT (a twin does not bite)** on both footings. A1 is a post hoc reading.

## What failed and why (diagnosed before writing this)

- **T3 (nuisance-shaped change) was built wrongly.** It set r = (k/k_p)^0.1 x S(R0 + 0.02) / S(R0) and required the
  refit to remove it to 1e-4. The refit model always multiplies by S(R) / S(R0) with base R0. To cancel the twin it would
  need S(R) / S(R0) = S(R0) / S(R0 + 0.02). P1D smoothing ratios do not compose that way after the line-of-sight
  projection, so no R in the model does this exactly. The twin was not exactly absorbable, contrary to its own
  definition. A check (scratch, not committed) confirms: the model reaches 0 to 4e-26 on the inverse construction, and
  the minimiser leaves 0.093 on the frozen twin (fixed value 3895), with alpha -0.101 and R 0.033.
- **T4 (amplitude frozen on case A) did not reach its frozen factor 1.25.** It rose 23.04 -> 26.35 (canonical) and
  23.90 -> 27.37 (alt), factors 1.14 / 1.15: tilt and smoothing stand in for most of the amplitude. The 1.25 factor
  was a design guess, not physics.

## A1 changes (nothing else changes: same model, priors, honesty rule, brackets, gate)

- **T3-A1:** r = 1 / N(theta*) with theta* = (A = 1, alpha = 0.1, R = R0 + 0.02 Mpc/h) in every bin; this is exactly
  representable. The refit must be <= 1e-4 and the fixed value > 100.
- **T4-A1:** freeze every A_j at 1 and refit T2's constant twin r = 1.05. The refit must stay > 4: the machinery's
  amplitude freedom must be load-bearing where it should be. The as-frozen T4 numbers are reported beside it.
- Outputs: `frz5_<footing>_A1.json/.out` and `frz5_<footing>_A1_MUTATE.json/.out`, written by `frz5_refit.py <footing> --A1`.
  The as-frozen run is not changed (same code path without the flag).

## What A1 can and cannot change

The primary refit numbers are unchanged by A1: case A 23.04 / 23.90 and case C 118.3 / 107.4, all above the gate of 4.
A1 can only decide between NO VERDICT and the graded word; it cannot turn a FAILS into a HOLDS. It is still a
post hoc change, made after the numbers were seen, and it is reported as such.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
