# SRF1R AMENDMENT A2 (2026-11-12): compute budget, second cut

Committed alone, after AMENDMENT A1 (696d184fbf) and before any flux-level number of this lane exists. A second timing
run of one halo chunk (no part written, no statistic) gave about 6 minutes per seed-0 part and 2.3 minutes per part without
f = 4, 6, inf: still about 2.9 h for the primary stage alone. The f >= 4 cases (whole-halo disks of the heaviest haloes)
take about 70 % of a seed-0 part.

Changes (stated before any number):

1. **f = 4, 6 and inf are computed at the three anchor bins only (seed 0).** Their twelve-bin flux Delta chi^2 is
   estimated as the anchor-block value (joint covariance of z 2.2, 3.0, 4.4) times the ratio twelve-bin / anchor-block of
   the flux Delta chi^2 at f = 3 (the largest f computed at every bin). This estimate is used for the graded value at those
   f and for known answer (b); it is labelled as an estimate wherever it appears. Their matter-level values stay exact
   (twelve bins).
2. Everything else as READING plus A1. Brackets keep their frozen order and are dropped from the end if time runs short.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
