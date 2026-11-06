# AC5: AC3's slow roots on a rolling clock: NO VERDICT (no power)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (63b0c9ca2c),
frozen before any graded run. Integrator 143a792e25; streaming measurement, merge and grader 6289791d63.

## Result

- **Main run, 81/81 cases, all converged** (R agrees between rtol 1e-9 and 1e-11 to 1e-3), Omega
  conserved (drift <= 2.4e-8, line 1e-6), every integration ok.
- **Largest amplification R = 2.68** over the whole grid (witnesses: 2.53). It is flat in eps_phi:
  2.682 / 2.682 / 2.681 at eps_phi = 0.05 / 0.5 / 2. This is under the PASS line (R <= 10) and far from
  FAIL (R >= 1e3).
- **Power gate NOT met.** The M2 flipped-stiffness twin reaches only R = 1.5-8.6 on the 8 witnesses
  (largest 8.58 at eps_phi = 2), short of the frozen 1e3. A wrong-sign stiffness gives only Hubble-rate
  growth on these backgrounds, so this setup cannot tell a healthy stiffness from a broken one.
- Label, as frozen: **NO VERDICT (no power)**, whatever the main run shows.

## Known answers and controls

- lambda = 0 reproduces AC4's main R on its two cases to 3.3e-9 (line 1e-8).
- M1 (drop Kdot) bites: Omega drift reaches 1.76 (separate output evidence/m1_drop_kdot).
- M2 (flipped stiffness): runs cleanly, but has no power (above).
- The clock really rolls: eps at the end equals its input on every witness (evidence/GRADE.json).

## Bookkeeping

70 of the 81 streaming parts first crashed in their per-part summary line (`max()` of an empty
witness list on a part holding no witness). The integration had already finished, but no output was
written. The fix is one line in evolve.py, `default=None` on `witness_max_R`; it touches no number.
The 73 cases with no output were rerun unchanged. merge_main.py takes the witness maximum over all
rows, which is never empty.

## What it does not show

Linear modes on exponential rolling-clock FRW backgrounds only. Nothing sourced, nothing nonlinear, no
galaxy, Solar-System or lensing regrade. Settling AC3's 8 slow roots needs a background or a control
where a wrong stiffness grows by more than 1e3 inside the run. On these backgrounds no such control
exists, because growth is capped at the Hubble rate.
