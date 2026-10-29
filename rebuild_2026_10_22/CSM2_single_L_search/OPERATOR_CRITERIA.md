# Structural route preflight: exact discrete projection operator

The source `f2_aqual.delta_sigma` is a linear map of the enclosed-mass grid:
finite differences, linear interpolation and fixed quadrature weights. Build
that map explicitly on the source's 3601-point radius grid and all four B21
radius-label arrays, for both constant and linear outer continuation. Verify
against the original routine on five fixed profiles, including a point mass,
SIS-like mass, a smooth compact profile and a fixed-seed nonmonotone vector.
Require max error relative to each source curve's max norm <1e-10. A 1% operator
corruption must fail. Save max errors and benchmark diagnostics, not dense maps.

This preflight does not evaluate any L or prove a continuous exclusion. If it
passes, an interval mass box can be propagated through signed coefficients
without assuming DeltaSigma is monotone. A later bound must use the actual
native radii/weights/covariance and account for every branch event. Profiling
unconstrained two-halo amplitudes gives a lower chi2 bound relative to the
original nonnegative fit; only a lower bound exceeding the unchanged cutoff
can exclude an interval. Every later error allowance and domain needs its own
contract. The current test establishes only the discrete operator identity.
