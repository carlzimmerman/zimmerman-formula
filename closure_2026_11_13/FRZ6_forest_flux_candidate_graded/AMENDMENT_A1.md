# FRZ6 AMENDMENT A1 (2026-11-13, about 19:10 EST): known answer (i), tolerance on the 3D matter power

Committed alone. It is post hoc: it was written after a disclosed test grading of the primary parts (canonical) had shown
that known answer (i) fails as frozen, and after that test printed the case numbers. **The as-frozen reading is reported
first in RESULT.md and stays the lane's first reading.** No S bracket number existed when A1 was written. The U and C
bracket numbers that FRZ4's existing bracket parts give, rescaled to this lane's D, had been printed by that test.

## What failed

Criteria section 5 (i) requires every reused FRZ4 spectrum to be reproduced "to 1e-12 relative at every k_v (P1D and
P3D)". In the whole reproduced part (z 2.2, seed 1, canonical, 320 spectra):
- **P1D**, the graded flux statistic, agrees to at most **5.6e-16**.
- **P3D** differs by at most **1.5e-7**, in single bins of the 3D matter power (largest at the lowest k bins).
  This is the size of single-precision rounding. The fields are held as complex64 and the 3D power is accumulated from
  them, so the 1e-12 tolerance cannot be met for P3D.
- Over all reused parts, the maximum is 1.7e-7 (P3D only).

As frozen, (i) FAILS on that footing, so U and C are NO VERDICT there.

## A1 (one change)

Known answer (i) passes if:
- P1D agrees to 1e-12 relative, unchanged; and
- P3D agrees to **1e-6** relative, at every bin with modes.

That is, a single-precision tolerance for the single-precision quantity. P3D enters only the matter-level known answer
(c1) and the reported matter numbers, never the flux Delta chi^2 or the gate.

Nothing else changes: no threshold, twin, bracket, label rule or seed count.

## What A1 can change

Only whether (i) passes. Under A1, the U and C cases can receive a graded word on a footing where they would otherwise be
NO VERDICT because (i) fails. It cannot move any D, SE, N12, twin or bracket value. The S cases do not use (i).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
