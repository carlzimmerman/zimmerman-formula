# KO2 AMENDMENT A2 (post hoc: written after a second model-only run; no lensing number has been computed)

Committed alone, before `ko2.py` is changed again or run on the lensing sums. It changes one tolerance of one known answer and
the order of the model-only stage. It changes no statistic, design, bracket, line or label rule.

## What happened

With A1 in place, the model-only stage (no WG, no WX) passed KA-2a, KA-2b (largest table error 8.7e-4 of a band's maximum) and
KA-2c. KA-2d passed in all 20 edge-adjacent cells (largest error 1.1e-3 of the band maximum) and failed in the non-adjacent
cells: largest deviation 1.45 % against the 0.5 % allowed.

## Why the check, not the table, is wrong

- The failing cell is the inner band in bin 10, where the band's own term crosses zero: 0.019 of the law's value in that cell.
  At separation 1e-3 l the off-centre truth (A1's reference) is 0.01858, the table 0.01870 and the concentric form 0.01898,
  all in units of the law's cell value. The table is within 0.0001 of the truth. The offset itself moves the value by 0.0004
  of the law's level. Relative to a value near zero, that reads as 1.5 %.
- Every other non-adjacent cell is within 0.06 % of the concentric form.

**Replacement.** In non-adjacent cells: |table - concentric| <= 0.005 times the law's value in that cell (the cell's own scale),
in place of 0.5 % of the band's term. The edge-adjacent part of KA-2d (A1) is unchanged.

## Order of the stages

KA-3a (2,000 planted neighbours, tree against brute force) reads no shear. It moves into the model-only stage, together with
the catalogue, the pool, the class thresholds and the class counts (weights only, as frozen). So every check that does not
need the shear is settled before WG or WX is read. The neighbour pass and everything after it stay in the full stage.

## What has been seen

Only the kernel checks' numbers above. No WG, no WX, no amplitude, no ratio and no label.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
