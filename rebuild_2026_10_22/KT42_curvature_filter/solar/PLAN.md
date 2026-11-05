# Pre-execution Solar contract

2026-11-04. Authorized changed law: p=9/8, ell=3kpc, original a0 footings,
Solar GM, uniform Newtonian external field and Cassini ceiling unchanged.
Curvature filter has multiplier exp(-a^2 k^2/2); g is unfiltered. Both the
inner H filter and outer adjoint on B are mandatory. No baryon parameter or
observational cut is fitted.

Physical a grid in kpc: 0, .0001, .001, .003, .01, .03, .1, .3, 1.
The exact zero branch is independently re-evaluated against KT39's accepted
p=9/8 ell=3kpc point-Sun diagnostic. Positive a uses a new adjoint-observable
Green reduction, avoiding a three-dimensional convolution.

Primary assertion: compute the exterior regular STF Solar coefficient under
the same point-source/constant-external-field convention, with a controlled
origin limit and complete B adjoint. This is not the Hessian at the center of
a resolved finite Sun. The latter can have a nonuniform shrinking-core limit
after curvature filtering; it is not silently equated with Cassini's exterior
quadrupole. The local high-field A cusp must be shown to have vanishing STF
Hessian at small exterior radius, apart from the sought regular l=2 term.

Use base4000x128 and fine8000x256 logarithmic-radial/Gauss-Legendre grids;
fine range1e-10 to1e7 rM, base1e-8 to1e6. Require absolute changes in
ceiling ratio <2e-4, with tighter relative checks where appropriate. Check
the a=0 benchmark, Newtonian and zero-external controls, softened-H central
limit and derivative identities, and a second radial integration strategy.
For finite source size, inspect exterior multipoles or shrinking Gaussian
source at a fixed nonzero observable radius; do not reuse KT39's old central
contact theorem. Any failed gate remains recorded and makes that row
unresolved until explained; it does not count as a physical exclusion.

The first bounded run is a diagnostic with the above finite grid. If a
resolution/regularization gate fails, a targeted second run may refine that
same row. No wider response-law/parameter family is authorized here.
