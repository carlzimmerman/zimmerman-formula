# Self-audit: FI checkpoint

Primary verdict: computationally verified only in the stated range.
Normalized claim: the specified effective energy has a finite-grid phase
minimum with a finite interface, passing the mass-weighted phase fractions,
but its law-shaped density fails the actual static T force equation.
The original physical goal is not achieved.

Dependency chain: inherited energy -> explicit auxiliary coupling -> reduced
binding energy -> analytic gradient/Hessian -> stationary phase computation
-> front restoring mode -> separate mass variation -> force-balance failure.
Every leaf is an internal derivation, an identified model assumption, or a
recorded finite computation. No external theorem or observational inference
is load bearing. No novelty claim is made.

Passed within scope: complete-square sign and boundedness; energy-gradient
and Hessian directional checks; T-only and total-mass finite variations;
correct exterior W and gradient tails; positive phase Hessian; restoring-mode
energy curvature; two-grid comparison; displaced-front recovery and heat
bookkeeping; all24+6+2 declared runs complete.

Failed target: free exterior and interior law simultaneously. The FI-2 5b,.03
candidate passes fraction gates but fails force balance; the8b candidates
fail the outer fraction. The small-disk template fails the free exterior
throughout its tested binding set. Barrier-only controls decay.

Conditional: stationary minima are numerical, spectra float64, spatial
derivatives finite-grid approximations. Outer boundary is the inherited
finite environment2 assumption. Rj kinematics are prescribed, not observations.
Near endpoint x=0 the T chemical potential is not assigned by its singular
ratio. Reported T-force failure lies where T is present. mu_c alone would
be sufficient only at phase stationarity; the independent mu_T check removes
that possible error. Actual gravity is unchanged at frozen total density,
which is why force balance, rather than a plot of that imposed gravity, is
the relevant law test.

Not addressed: live density equilibrium/stability, baryon stress evolution,
formation work, microscopic mode/time scales, noise,3D geometry, cosmology,
observed data or continuum certified eigenvalue bounds. No population-wide
or all-parameter exclusion follows from these cases.
