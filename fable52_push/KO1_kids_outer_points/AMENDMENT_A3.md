# KO1 AMENDMENT A3 (post hoc; committed alone, before `ko1_neighbours.py` exists)

It changes no frozen statistic, cut, gate or label rule. It declares one more reported computation, before it is run.

## Why

Section 6 of RESULT.md reads the host-free outer signal against a two-phase exterior made of the lens's own baryons and its
swept share, and finds the record's share excluded at more than 5 sigma. That reading assumes the outer bins are not supplied
by lighter neighbours, which the veto leaves in place. The result file currently supports the assumption only by analogy with
CFG903. The assumption can be computed.

## E8, the neighbours' term in the two-phase reading (reported only)

- **Lenses.** Host-free at the frozen cut (40,667) and at the widest veto (1.6 R_h, 17,335).
- **Neighbours.** Every object of the lane's neighbour pool (r < 20, 0.02 <= z <= 0.8, finite log M* > 7, masked 0 or 1)
  other than the lens, at any mass, with projected physical separation inside the lens's measured range and
  |chi_j - chi_l| < 230 Mpc.
- **What a neighbour shows.** In the two-phase reading a neighbour is seen from outside its own wall as a point of
  (1 + X) M_b,j (SWT1 T1 plus its swept share), with M_b,j from the record's recipe. For a point of mass m at projected
  separation d the annulus average is exact: DeltaSigma = 2 m ln(R2 / R1) / A for d < R1, (2 m ln(R2 / d) - m) / A for
  R1 < d < R2 and zero beyond, with A = pi (R2^2 - R1^2); the annulus is each lens's own cell, capped at 3 Mpc.
- **Chance projections** are removed by subtracting the same sum around shuffled sky positions (each lens keeps its
  redshift, mass and cells; five shuffles, seed 52).
- **Statistic.** The stacked net term, with the lensing weights WW, against the law model with the data's bin weights:
  a_nb per unit (1 + X). Reported: a_nb with its patch jackknife error, the term at the record's share (X = 5.562) and at
  the census cap (X = 53.64), and the same in the calibration-free form (multiplied by the inner window's enclosed-mass
  factor k and divided by the inner amplitude).
- **What each outcome would say.** If the term at the record's share is small against the 0.5 to 0.7 the outer bins lack,
  exit B stays closed with the neighbours counted. If it is comparable, exit B is open and the result file's section 6
  must say so.
- **Limits, known before running.** The catalogue is flux-limited, so the term is a lower bound that weakens with redshift;
  it is reported for the two redshift halves. Neighbours' unseen baryons are not counted.
- **Hand estimate (mine, before running).** CFG903 found 0.2 to 0.5 Msun/pc^2 with ten shares per neighbour and hosts
  included. Without hosts and with one share I expect a few hundredths of the law's level: exit B stays closed.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
