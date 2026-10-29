# Local group derivative verified; regional coverage remains open

The frozen group_derivative_001 encloses all189 velocity derivatives on
canonical L in[3.5,3.5001] using the reviewed analytic fixed-EPS/quadrature
coefficient and compact-root boxes. Its8 controls pass; runtime35.839seconds.
The changing group statistic has

    Z'(L) in[-0.302567149462260,-0.301119418216813].

This establishes a local negative derivative in the stated analytic model.
The earlier Z lower2.00347780276279 remains above the necessary absZ<2 cut.
Neither derivative extrapolation nor global monotonicity is justified.

Derivation: for x=R/r0 and q=r/R<1, mass matching gives
M=pi*Sigma*R^2*B(x)/x^2, so
 dlogx/dlogSigma=1/(2-h(x)),
 dlogMh/dlogSigma=[h(qx)-h(x)]/(2-h(x)).
The already recorded compact-Burkert monotonicity argument proves decreasing
h(x); its dependency hash is in group_derivative_review.json. The compact
root boxes satisfy h(x)<2. The truncated exterior mass is constant. Positive
quadrature then gives v'=5/(8*L*ln10)*sum(K*Mh*E)/sum(K*Meff).
All189 cells stay halo, and review finds no uncertain radial truncation node.
The full derivative of T=sampleVariance(d)/63+alpha^2*mean(s)^2 is propagated,
including both changing residual variance and systematic mass slope; actual
binary64 alpha=.10 and delta=.02 are retained. Z'=mu'/sqrt(T)-mu*T'/(2*T^1.5).

All8 independent review controls pass. Nine cells (first/middle/last groups,
all three mass offsets) use70-digit normalized-root full-quadrature velocities
and Richardson differentiation. These controls choose admissible midpoint
coefficients within the already certified coefficient boxes; they do not
independently reconstruct the original catalogue/EPS coefficients. The entire
statistic interval is independently recomposed at70digits, with a symbolic
Z derivative identity, sign mutation, outward/finite and source-hash controls.
No physical parameter or cut changed. An initial review serialization failure
on a NumPy boolean was repaired without changing the arithmetic; it is recorded.

The common scope is the analytic profile with fixed saved CLASS/EPS/kernel
primitives. Original floating optimizer/libm behavior and broader L coverage
remain unresolved. GROUP_REGIONAL_ROUTE.md freezes the next separate regional
attempt. A broad inconclusive interval must be retained, with all coverage
holes and switches explicit. Native finals remain7of9, seeds4and6 pending.
