# Frozen first group derivative enclosure

Use the validated[3.5,3.5001] analytic fixed-EPS/kernel group domain and its
published378root/189coefficient enclosures. Do not repeat source grades or
reconstruct EPS. ParentM,R,baryons are L-independent and all cells stay on the
compact halo branch. Audit the derivative identities in GROUP_DERIVATIVE_ROUTE.
For x=R/r0,q=r/R<1, differentiate the mass-match relation to obtain
 dlogx/dlogSigma=1/(2-h(x)),
 dlogMh/dlogSigma=[h(qx)-h(x)]/(2-h(x)).
For r>=R derivative is0. Use positive quadrature for v'(L) as stated there.

Enclose the full-L root, column, radius and h ranges. Evaluate B and h at
argument endpoints and use their proved monotonicity; naive interval B over
a varying small argument can lose cancellation and is not acceptable. Clamp
only the analytically nonnegative elasticity lower bound to0. Reuse existing
velocity boxes for the positive s2 denominator. Save all189v' enclosures.
Build full changing-statistic T,T',mu,mu',Z' intervals with actual delta=.02
and alpha=.10 binary64 constants. No monotonicZ assumption. Report a local
negative sign only if directed Z' upper<0; otherwise INCONCLUSIVE, never
choose another physical parameter, interval or cut to obtain a sign.

Check all parent/branch/root premises, finite/outward arrays, positive moments
and derivatives, derivative sign mutation and stable input hashes. Independently
validate nine cells (first/middle/last group times3mass offsets) at L3.5 via
70digit normalized-root velocity differences with steps1e-6 and5e-7 and
Richardson extrapolation. Diagnostic relative error<=1e-8; finite differences
are controls, not a uniform bound. Check a wrong-sign formula is rejected.
Independently recompose the entire statistic interval at70digits. One numerical
thread, wall600/CPU480. No globalL or original floating/libm/CLASS continuum
certificate. A regional sign/cover experiment requires a separate contract.
