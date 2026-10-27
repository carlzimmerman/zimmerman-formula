# Density-dependent continuation, before its numerical checks

The first run found an empty constant-A interval by over a factor 300. Its growth-limit check failed because a manually entered decimal anchor was inaccurate by 4e-8. Replace that anchor with an independently evaluated 2x2 eigenvalue; no mathematical criterion or interval changed. Preserve the first run and its failed status.

Next candidate: A(rho)=A0(rho/rho0)^(-m), rho>0. The first script's exact Hessian gives local mismatch-energy convexity for 0<=m<=1, with a degenerate zero-mismatch surface. This is not full gravitational stability.

Three new checks, selected analytically before numerical execution:
1. Homogeneous matter expansion rho=rho0 a^-3 gives k_phys^2 ell(rho)^2=(k_com ell0)^2 a^(3m-2). Avoiding divergent early-time tether strength within this matter scaling requires m>=2/3. This limit is a model requirement, not a radiation-era calculation.
2. An admissible zero-polarization compact uniform-sphere trial at fixed cold mass has mismatch energy proportional to R^[-3(1-m)] and gravity -3GM^2/(5R). Thus m>2/3 has a Newtonian concentration instability on this trial. m=2/3 is the marginal exponent. Discontinuous uniform spheres are understood as smooth limiting profiles; it suffices for an energy-unboundedness witness, not a dynamical collapse proof. No claim that all stationary solutions are unstable.
3. At m=2/3 derive and compute the uniform-sphere critical mass using rho0=2.26e-27 kg/m^3 as a declared illustrative present cold density, and ell0 at the existing local growth upper bound. This is a diagnostic upper scale for this trial, not a predicted core mass, observed threshold, or fitted coupling. Test separately both a0 footings where they enter; this unpolarized trial contains no a0.

Any continuation must include the coefficient-derivative force, conservation, a positive density, finite inventory and boundaries. No rotation/pressure-support selector follows from this energy's density dependence alone. A new density-gradient term or internal phase may alter the concentration test, but it would be a new interaction and must be specified and varied, not silently appended.
