# Frozen root-sign certification subexperiment

Test all124 non-saturated compact-root brackets saved in interval_001 at both
Sigma endpoints. Interpret saved M,R,Sigma and r0 bounds as exact binary64
numbers; use mathematical pi. At50 decimal digits with mpmath1.3.0 interval
arithmetic, certify that F(R/r0_upper)-M/(pi Sigma R^2)>0 and the corresponding
r0_lower residual<0, where F(x)=B(x)/x^2. Interval evaluations use log and
atan2, never rounded point estimates to decide a sign. Verify each bracket
lies on compact side using h(R/r0_upper)<2. The established decreasing-h proof
then supplies a unique enclosed compact root. All endpoints must be finite;
an interval touching zero is inconclusive, never accepted by tolerance.

A shifted1% first bracket must fail. Independently compare residuals using
80-digit point arithmetic as a diagnostic and validate elementary interval
containment on exact rational identities. Wall120s, CPU90s, one thread.

This isolates root-comparison rounding. It does not certify the saved physical
coefficients, endpoint mass boxes, projection/quadrature coefficients, covariance
whitening, signed dot products, cutoff, or continuum-L monotonicity. Even all
root checks passing cannot promote interval_001 to a certified model exclusion.
No new fit or score calculation. Preserve negative/inconclusive outcomes and
input hashes before/after; use a fresh run directory.
