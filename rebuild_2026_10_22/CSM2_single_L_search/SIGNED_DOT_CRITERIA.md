# Frozen signed-map arithmetic experiment

Propagate the completed directed mass boxes through signed native projection,
positive inventory stacking and the saved nuisance/whitening map. Scope is an
explicit anchored fixed-coefficient map: m(L)=saved_H(3.75)+sum w A (M(L)-M(3.75))
for62 active nodes. A are the binary64 matrices reconstructed by the validated
operator implementation and saved with this run; weights, data and saved_H are
fixed binary64 inputs. Q is the binary64 product of saved P,W, also saved here.
Other65 nodes are constant in this anchored map. The continuum assumption that
M(L) lies between the endpoint boxes remains an external obligation; this test
alone does not certify the original physical likelihood or a real-L exclusion.

Form outward delta boxes [mass_lower_at0-mass_upper_at0,
mass_upper_at1-mass_lower_at0]. Use nextafter outward for binary64 subtraction.
For each signed projection row, select delta endpoints according to coefficient
sign. Accumulate products/sums in NumPy longdouble with optimize=False einsum.
Require at least53-bit precision, finite intermediates and normal-range nonzero
products. Use conservative unit-roundoff bound u=2^-50, absolute error allowance
eta=2^-1000 per operation, gamma_(2n)=2nu/(1-2nu), and bound exact absolute sum
by (computed_abs_sum_upper+2n eta)/(1-gamma_(2n)). Enclose each rounded dot using
that bound, gamma and2n eta. Directed50-digit intervals perform the error-budget
calculation, stacking, residual mapping and sum of coordinate-distance squares.
No unexplained fixed tolerance may replace the derived arithmetic bounds.

Check outward cast coverage; elementary exact-dot cases; deliberate1% dot-result
mutation detected; native endpoint/midpoint source residuals contained by the
final boxes; exactly62 nodes x4 bins x15 rows x2 bounds visited. Save coefficients,
delta boxes and projection bounds for an independent exact-dyadic dot review.
All arrays and errors finite; source/input hashes stable. Bound wall600s,
CPU480s, one numerical thread. A score lower bound is only for this stated map;
certification of Q as the original covariance nuisance minimizer, projection
coefficient construction and column/branch/continuum bounds remains separate.
