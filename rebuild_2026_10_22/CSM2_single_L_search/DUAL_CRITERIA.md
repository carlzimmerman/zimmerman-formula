# Frozen covariance-dual experiment

Use actual saved60x60 covariance C and60x4 template T, interpreted as exact
binary64 rationals, and unchanged cached baseline/law profiles at L=3.75.
Require C exactly symmetric. Prove SPD through exact Fraction LDL with positive
pivots and full exact reconstruction C=L D L^T. Cap rational coefficient bit
length20000, wall240s, CPU180s, one numerical thread. A bound hit is inconclusive.

Derive a floating witness from C^-1(y-H-T b_H) using saved baseline constrained
amplitudes. Fix its nonpivot values as exact binary64 rationals. Choose the
largest absolute T coordinate in each disjoint bin; solve those four entries
exactly to obtain a^T T=0. Require exact orthogonality and positive a^T C a.
The witness is an inequality certificate, never a new physical fitted number.

Use already enclosed projected mass-difference boxes from signed_dot_002_cached.
Accumulate their weights, baseline and numerator interval a^T(y-m) with exact
Fractions. The inequality min_b chi2 >= distance(0,numerator_box)^2/(a^T C a)
holds for the stated native prediction boxes. Compute an exact law-score upper
bound using its saved nonnegative nuisance amplitudes and exact LDL solves;
compare dual lower against this conservative law upper+9. Do not relax any cut.

Check point dual bound <= exact baseline candidate score; exact law candidate
matches old cached score within1e-6 as a diagnostic. A pivot perturbation must
break orthogonality. Save full rational LDL/witness/box/candidate certificates
and verify all inputs stable. Record finite floating witness and all rational
signs exactly. Preserve failures and inconclusive results.

This removes approximate Q whitening/nuisance dependence for fixed C,T. It
retains fixed projection, anchor, column/branch and continuum box-coverage
obligations. It is not a real-L or global obstruction. Do not regrade new L
points, add a fitted parameter or change historical source inputs.
