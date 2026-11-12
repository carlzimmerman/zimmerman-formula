# FRZ3 AMENDMENT A2 (2026-11-12): correction to A1's statement, and a code fix found before the first part

Committed alone. Seen before writing this: the first part file (z 2.2, seed 0), its per-mode R_F and gas ratio for that
one seed; no Delta chi^2, no label.

1. **A1 said the floor cannot act on the primary fields. That is wrong.** The primary fields are strictly positive (the
   frozen assertion holds), but the lognormal voids reach 1 + delta = 3.0e-4, below the floor of 1e-3: in the first part
   6.6e-5 of the pixels of BOTH the reference and the rule 5 field are floored (the same pixels in both). The flux there is
   1 to within A x (1e-3)^1.72 ~ 1e-6 of optical depth in either reading, so the effect on R_F is expected to be far below
   the seed scatter. Both readings will be reported: RESULT gives R_F and Delta chi^2 for one anchor part re-run with the
   floor at 1e-9 (reading "floor off", output `parts_check/`), beside the graded floored reading. The graded reading stays
   the floored one, as A1 fixed it.

2. **Code fix before any part was written (no design change).** The first launch stopped on the frozen positivity
   assertion at z 2.2 (minimum 1 + delta = -0.004). Cause: the halo profiles U(k) were looked up on the 3D grid by NEAREST
   index on a fine ln k grid, which puts a non-positive-definite error into each painted halo (single 1e12 Msun/h halo:
   minimum -1e-3 against a peak of 129). The lookup is now linear in ln k on that grid (single-halo minimum -1.4e-5, i.e.
   float32 round-off). The failed log is kept as `logs/fields_anchor_failed_nearest_k_index.log`; no part from that launch
   exists.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
