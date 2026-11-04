# LAM6: does the law's residual at r_half track orbit shape (integrated h4)?

Criteria `16e2226f95` (frozen first; script committed before any run). kappa = 1/2 FITTED; footings never pooled; not theory closed.

**LABEL: NO VERDICT on both footings.** A lean toward a positive trend, not a result.

| | canonical | alt |
|---|---|---|
| E = slope x IQR(h4_int), ln | **+0.040 [-0.008, +0.093]** | **+0.042 [-0.003, +0.096]** |
| M1 (h4 shuffled within groups) | +0.014 [-0.042, +0.061], PASS | -0.019 [-0.061, +0.026], PASS |
| C1 N in groups / C2 KU2 D reproduced | 963 / exact | 963 / exact |

Rows, ungraded: fibre h4 on the same galaxies +0.022 / +0.022; within slow +0.088 / +0.086; within fast +0.033 / +0.036.

## Reading
At fixed M*, sigma and spin class, galaxies with more peaked integrated profiles (higher h4_int) sit slightly
higher on the law, by about +0.04 ln per h4 interquartile range, but the 95 % interval touches zero and also
reaches past the 0.05 bar, so neither label is earned. The sample (963 in groups) is too small: the shuffle's
interval half-width is about 0.05, the same as the bar. If the lean is real, the likely reading is a JAM
anisotropy systematic (radial-orbit galaxies' masses), not a law dependence; nothing here separates the two.
KU2's UNIVERSAL is not overturned (that is a slow-fast offset; this is a within-class trend), but it is now
not shown robust to orbit shape either.

What would decide it: the same statistic on all of KU2's 6056 galaxies, which would need the remaining MaNGA
cubes summed as in LAM4 (about 6x LAM4's streaming; shrinks the interval by about 2.5x).

Files: `lam6.py`, `lam6.out/.json`, `lam6_MUTATE.out/.json`.
