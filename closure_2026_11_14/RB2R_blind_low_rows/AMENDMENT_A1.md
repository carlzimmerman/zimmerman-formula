# RB2R amendment A1 (2026-11-14): one added twin pair, written after the frozen twin T3 did not bite

Written after the first run, which I have read. The as-frozen reading stands and is reported first: twin T3 (the
Newtonian twin, M* = 1e6 Msun, R_h = 500 pc, at d = 20 kpc from the Milky Way, no proper motions) reads TIDES CANNOT
REACH on both footings, so T3 does not bite as frozen. The cause is in the twin's design, not (as far as I can tell) in
the pipeline: at 20 kpc its primary r_J is 0.68 / 0.74 of r_1/2 (canonical / alt), not "well inside" r_1/2 as the
specification's twin requires, and the phantom mass the law keeps inside that r_J still lifts g_B well above Newton at
r_1/2 (strong edge r_J / r_1/2 0.33 / 0.36, residual + 2 s = -0.145 / -0.241).

This amendment adds, without removing T3:
- T3b: the same construction (stars exactly on Newton, 5 % errors, 0.05 mag) with R_h = 2000 pc and M* = 1e6 Msun, at
  d = 20 kpc from the Milky Way, no proper motions. Its r_J should then sit well inside r_1/2. It must read TIDES CAN
  REACH.
- T4b: the same dwarf in the field file. It must read TIDES CANNOT REACH.
Pass lines are those of the frozen T3 / T4. The real rows' words are not touched by this amendment. Committed alone,
before T3b / T4b are run.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
