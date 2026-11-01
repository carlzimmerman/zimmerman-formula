# DR5 AMENDMENT A1, written after the first run, committed before the second

**What failed.** K1 as frozen read 5.6e-6 against 1e-6, so the first run's verdict is NOT DECIDED. Only rms differs (5.3e-6, 5.6e-6); Υ, tilt, LITTLE THINGS read 0. One bin's Υ moved 1.18 to 1.17.

**Cause, tested.** The gated path interpolates M₀ on the response path's 300-point grid; NR3's off row uses the closed form. At 1200 points with f ≡ 0, K1 reads 3.9e-7, inside the frozen line, and the bin returns to 1.18 (`dr5_k1b_1200.json`).

**Change.** The line stays 1e-6. Rows f0, 10, RATIO3, 30 are rerun at 1200 points, and K1 and the label read from those. K2 (f ≡ 1, against NR3's 300-point Blumenthal row) stays at 300, where it reads 0: it tests the plumbing, not the grid. MUTATE stays at 300. Nothing else moves.

**Seen before this was written.** The first run's numbers, including SIG10 against off: dΥ 0.030, dtilt 0.060, past the frozen 0.05 by one Υ grid step. The label's line isn't moved. Also disclosed: index.lock blocked the criteria commit, which landed (17b9d33134) after the first run, with its text unchanged.
