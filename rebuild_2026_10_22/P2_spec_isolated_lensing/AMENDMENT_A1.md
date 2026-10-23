# P2_spec_isolated_lensing AMENDMENT A1 (POST-RESULT; append-only; no pass/fail line changed)

Written after a full development run (not committed) had printed the frozen verdict. Nothing in `FROZEN_CRITERIA.md`
is changed. Everything below is either an implementation fix that touches no frozen line, or a reported-only addition.

## 1. What the development run showed

- Frozen verdict on both footings: UNDECIDABLE (N too small). The committed run reproduces it.
- K2 failed numerically: the offset machinery at d → 0 matched the centred bin average to 1.7e-3 (line ≤ 1e-3).
  Cause, found by a separate test: log-log interpolation of the M_c(u, v) table at 30 points per decade (1.0e-3) plus
  the 6-point bin average of the centred profile (6e-4).
- Peak RSS (ru_maxrss) reached 1.33 GB in the neighbour-term step, above the brief's 1 GB, although the process
  footprint was 0.37 GB. macOS keeps freed multi-megabyte blocks in RSS. Repeated temporaries of about 6 MB caused it.

## 2. Implementation fixes after that run (no frozen line touched)

- Numerics: the M_c table is now 60 points per decade in u and v. Bin integrals use 17-point Simpson and the centred
  bin average uses 12 points. Tested on its own: 4.5e-4.
- Memory: every work array is kept to about 1 MB or less (pairs 8,000 per chunk in the neighbour term; 100–300
  centres per tree query). Sources are read box by box into reused buffers. No physics changed.
- A single-process run with these fixes still peaked at 1.01 GB (footprint 0.36 GB). The script therefore runs as two
  sequential processes:
  - Phase A: sources, K0a/K0b and the shear measurement, written to the scratch cache.
  - Phase B: rebuilds the same samples (same seeds and hash), reads the cache, replays A's K0 lines, then models and
    scores.
  Each phase stays below 1 GB, and the verdict numbers are identical to the single-process run.
- Earlier, before that run: K0b first failed at a ΣWW ratio of 1.0000014 against the frozen upper bound 1.000001.
  - The bound assumed F1's cache lacks the Z_B = 1.20 rows. It does not. F1's own estimator drops those rows through a
    float64 cut, which K0a now copies.
  - The 1.4e-6 excess came from distance numerics, not from data. Copying the record's per-lens 2048-point distance
    table and its stored lens χ made the reproduction exact (ratio 1.0000000). The line was not moved.
- Completeness limit M_lim95(z): a 0.01 z bin needs ≥ 50 valid-mass galaxies, otherwise it is interpolated (the frozen
  text says "empty bins"). The proxy zero-point c(z) needs ≥ 20. All lens bins (0.05 < z < 0.5) are well populated.

## 3. Reported-only additions (not verdict lines)

- **y_need:** the smallest grid y_e at which A_O1 and A_O2 ≥ 1 − 2σ, so the data do not sit below the model. The
  frozen y_allow ("A ≤ 1 + 2σ") reaches the top of the grid because the data are never short. So the field the data
  *allow* is unbounded above on this grid; y_need is the informative side.
- **S1's own decisiveness S,** and the significance of its 1.1–2.6 Mpc deficit against the zero-field model.
- **Boost against the iso-randoms I3** (same z and M★ draws as S3), beside the frozen comparison with the plain
  randoms R. R is drawn from S1's redshifts, so its source-weight ratio is not a clean boost.
