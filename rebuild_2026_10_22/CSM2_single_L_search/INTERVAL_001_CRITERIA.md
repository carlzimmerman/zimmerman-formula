# First L-interval experiment (frozen after native-matrix validation)

Domain: canonical footing, native X53 background h=.679, L in [3.75,3.751].
This local interval is chosen to validate machinery around a reproduced failed
point; success here cannot exclude the remaining continuous domain. Original
law score154.34346325076024 and unchanged delta<=9 cut apply. Both continuation
operators and equality-law convention remain unchanged.

Before evaluating its score bound, inventory all 127 positive-weight stellar
mass nodes and compute their switch thresholds from the pinned actual X53
columns using U(L)=U(3.75)*(L/3.75)^1.25. A threshold in or uncertainly touching
the interval requires subdivision with law-side equality or an inconclusive
result; never silently hold its branch fixed. Check copied inventory weights
against native_matrix_001. Do not edit a historical scorer or its pinned input.

For every active node, construct native spherical enclosed-mass vectors at both
endpoints with the unchanged corrected column, baryon inventory and truncation.
Independently bracket the compact Burkert root on its documented compact side;
report bracket/solver tolerances and saturation. Validate the monotonic-mass
argument and componentwise order for the actual domain before invoking it.
Numerical samples alone do not prove monotonicity. Enclose uncertain roots by
mass boxes, with an additional relative allowance1e-8 and absolute1e-6 Msun per
mass coordinate; if this cannot be justified as conservative, retain a
conditional numerical result rather than a certified cover.

Use signed native projection matrices, positive inventory weights, and saved
PW to propagate mass boxes to residual boxes. Direct projection of endpoint
mass profiles must reproduce the original source routine within1e-9 relative
max norm, and L=3.75 assembled stack must reproduce saved CSM1 H within1e-8
relative max norm. Inflate final residual intervals by1e-6 per whitened
coordinate and final score lower bound downward by1e-4. Explicitly check every
array/error finite. The coordinate distance-to-zero bound is compared with
163.34346325076024; no interpolated score or assumed chi2 monotonicity.

A valid bound above the cut excludes this declared interval only, conditional
on established enclosure arithmetic. A bound below the cut is inconclusive,
not a passing witness. Check deterministic endpoint and midpoint source scores
lie above the bound, and mutation of matrix/weight/branch must break controls.
Freeze implementation/resource contract and hash inputs before execution;
wall<=600s, CPU<=480s, one numerical thread. Preserve failures and numerical
uncertainty; no new fit, estimator or relaxed cut. This file is a prospective
contract, not evidence that the experiment has run.
