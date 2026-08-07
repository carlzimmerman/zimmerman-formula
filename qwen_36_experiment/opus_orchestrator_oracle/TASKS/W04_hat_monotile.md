# W04 — The hat: an aperiodic monotile
COST: M | script: `wacky_hat_monotile.py`

> WACKY TASK. No framework rules apply. Two things still do: **every check must be able to fail**, and
> **refine once and report the shift**. `../03_NUMERIC_HAZARDS.md` applies to any float arithmetic.
> Put the script in `real_research/reviews/` like any other, prefixed `wacky_`.

## The idea
In March 2023 Smith, Myers, Kaplan and Goodman-Strauss found the first **einstein**: a single tile that tiles
the plane only aperiodically. The "hat" is a 13-sided polykite. Its substitution system has a specific
inflation factor, and the ratio of the two reflected forms tends to an irrational limit.

## Do
1. Build the hat from 8 kites on the hexagonal grid (standard vertex coordinates are published).
2. Implement the substitution: hats group into 4 metatiles (H, T, P, F) which inflate. Iterate 5–6
   generations, counting tiles of each type.
3. The counts satisfy a linear recurrence — build the substitution matrix and get its **largest eigenvalue**
   (the inflation factor). Compare against the golden-ratio-related constant reported in the paper.
4. Compute the limiting ratio of unreflected to reflected hats. It should converge to a specific irrational
   value (φ⁴ appears). Report the convergence rate.
5. Refinement check: one more generation must not move the eigenvalue.

## Why
A 50-year-old open problem closed in 2023, and the whole answer is one matrix eigenvalue.
