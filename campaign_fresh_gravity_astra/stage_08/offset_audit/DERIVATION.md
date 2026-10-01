# Fixed-offset identifiability audit

For the inherited stored finite operator, let C stack H and the row selecting
the map offset. Exact fixed-offset observations identify the target L theta
on the affine family iff L is in row(C). Indeed, if L is not in row(C), a
null vector v exists with Cv=0 but Lv nonzero. A baseline with strictly
positive decreasing pressure nodes is an interior point of these finite
inequalities. Therefore theta0 +/- epsilon v are feasible for sufficiently
small epsilon>0 and give different gradients with identical observations
and identical offset. This is an exact finite-dimensional equivalence;
positivity cannot restore local identification at an interior baseline.

For a concrete certificate use binary64 stored H,L,baseline as exact rational
numbers. RREF(C) constructs its null basis. Select the first vector with Lv!=0.
Choose epsilon as half the minimum of each positive pressure-difference margin
divided by the absolute corresponding perturbation, including the last
pressure versus fixed zero at x=5. Directly verify both synthetic witnesses,
monotonicity, offset equality and differing gradients. Rank uses exact arithmetic;
no floating cutoff or random sampling. This is an ambiguity witness, not sharp
bounds. FGF022's independent worker computes constrained extrema separately.

No force or missing mass is calculated. A later physical bridge must use
both a0 normalizations, separate vacuum/H branches and Q/R/registered M.
No calibrated pressure interval or continuum point-gradient theorem follows.
