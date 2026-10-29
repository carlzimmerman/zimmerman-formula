# Next structural reduction: exact covariance dual bound

Avoid treating a nearly annihilating floating Q as an exact projector. For
positive-definite actual covariance C and any fixed vector a with a^T T=0,
Cauchy-Schwarz gives, for every nuisance vector b,

    (x-Tb)^T C^-1 (x-Tb) >= (a^T x)^2/(a^T C a).

Thus the original constrained minimum has the same lower bound. Exact dyadic
C,T,a and an outward bound on a^T(y-m) can remove the whitening/projector
rounding obligation without inverting C approximately. The witness a is a
mathematical inequality certificate, not a physical fitted parameter or a
changed observational score/cut.

Next freeze an executable contract: derive one witness from the saved failed
L=3.75 residual and nuisance amplitudes; fix its nonpivot coordinates as exact
binary64 rationals. Choose the largest-magnitude template coordinate in each
of four disjoint mass bins and solve the four pivot entries exactly so a^T T=0.
Prove actual saved C positive definite by exact rational LDL with positive
pivots, then evaluate a^T C a exactly. Bound the numerator over the already
published native prediction boxes, retaining anchored/fixed-projection and
continuum coefficient assumptions explicitly. Include exact orthogonality,
positive denominator, point-score upper checks and deliberate mutation controls.
Use bounded single-thread arithmetic; preserve bit-growth/time limits as
inconclusive rather than approximate proof. No new L values or changed cut.

This is a prospective route, not an executed certificate. It will not close
projection coefficient construction or column/branch/continuum obligations by
itself, nor establish a continuous covering obstruction from a local interval.
