# Native score and stacking preflight (frozen before arithmetic)

Reconstruct the actual F2 catalogue interpolation weights at h=.679, four native
radius arrays, full covariance and fixed two-halo template. Require positive
weights summing to one, source interpolation reproduction <1e-12, native radius,
data and sigma reproduction <1e-10, and discrete projection reproduction <1e-10
on point/linear/compact profiles with both continuations at actual native radii.

At saved CSM1 L=3.75,3.9,4.0 and both footings, independently reproduce saved
law+two-halo and corrected+two-halo chi2 within 1e-6. Build W=chol(C)^-1 and
P projecting off the four whitened templates. Check rank four, symmetry,
idempotence, annihilation and agreement with independent least squares at
1e-9 relative tolerance. The unrestricted score must be no larger than the
saved constrained score (allow 1e-6). All arrays/errors must be explicitly finite.
A 1% covariance corruption must break saved score reproduction.

This establishes actual matrices, weights and nuisance reduction only. It is
not an L interval bound or a new model grade. Do not sample additional L here.
No fitted physical number changes. Save compact arrays and hashes; exclude
large dense mass operators. Bound execution to 180 seconds, CPU120 seconds,
one numerical thread. Following this preflight, separately freeze a branch-
fixed L interval and numerical mass enclosures before new interval arithmetic.
