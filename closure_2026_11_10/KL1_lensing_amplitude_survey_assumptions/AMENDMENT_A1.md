# KL1 AMENDMENT A1 (POST HOC; committed alone, before the new arm is computed)

Criteria 99a42c78ef (Part A), d26939ed4f (Part B). TEST lane; adopts nothing. **kappa = 1/2 FITTED; not theory closed.**
Footings never pooled.

**Timing, disclosed: post hoc.** Every Part A and Part B row, label and MUTATE arm had been computed and seen when this was written.
As frozen, MA2 (KA2 rerun with every n_i halved must FAIL (ii)) bites on KiDS-1000 and **cannot bite on DES Y3**. Halving
DES's densities leaves only 3 / 4 DES points (canonical / alt) where the noise is below half of the Gaussian diagonal. Test (ii)
needs 5, so it reads NOT EVALUABLE and the arm cannot fail. Test (i) does fail under the same mutation on DES (16th to 84th
percentile 0.907 to 1.155 against the band [0.85, 1.15]), so KA2 as a whole fails, but narrowly, and the frozen wording names
(ii). **By the frozen rule the DES rows MA2 guards (A2, ALL and their variants) read NO VERDICT, so the frozen overall label is
NO VERDICT on both footings, in Part A and in Part B.** That reading stays in RESULT.md, first.

**The defect.** The arm was meant to show that the area fit absorbs an overall factor of the Gaussian covariance but not a change
of the noise share. Halving the densities is one direction of that test. On a survey whose points are mostly noise-dominated
(DES), it removes the very points test (ii) reads.

**Swing harder: MA2b (added).** KA2 rerun with every n_i **doubled** must FAIL (ii) (signal-dominated points then have a larger
share, so (ii) stays evaluable), on both surveys, written to `parts/ma2b_MUTATE.json`. The DES rows MA2 guards are read under A1
by MA2b. KiDS-1000 keeps MA2 as frozen; MA2b is reported for it too.

**Reported alongside, not graded:** the A1 reading of every label. Nothing else changes: no row, line, label rule, tolerance or
other arm. MB2 (Part B), which did not bite (0.46 / 0.47 width against 0.5), is not touched by this amendment.
