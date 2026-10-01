# FGF028 independent response audit plan

Review scope: response construction from the cached finite map/mask/beam and inherited geometry, not the root-owned target rowspace/sensitivity audit. No FGF028 output is yet accepted. Do not import inherited project.py top-level.

- Projection: fifteen nodal pressure hats, p(5)=0, support at x<=5, LOS factor 2, analytic Abel primitives and behavior at t=0/t=node boundaries. Target derivative is electron-pressure model slope, not force.
- Geometry: center, inherited fiducial DA and target radius, theta=Rt/DA units, spherical angular radius, WCS map/mask alignment, complete [0,5) annular inclusion in source patch.
- Beam: angular pixel spacing in radians, x longitude*cos(dec), y latitude, FFT axes/frequencies, ell=2pi|f|, cached normalization at ell0, cutoff/interpolation, 512 source/1024 padded grid and centered crop. Finite periodic/padding approximation remains conditional, not an authenticated full response.
- Measurements: actual finite-map and finite positive mask selection, each annulus [a,b), sum(mask*map)/sum(mask), same weights applied to every convolved basis, positive denominator, coverage and empty-mask failure. Extra rows are bins of the same cached map, not independent observations.
- Offset/support: post-response additive constant background has unit column under normalized weights; source pressure zero outside5; known offset is conditional, not automatically measured.
- Changed implementation: exact/declared tolerance reproduction of old twelve response rows, with discrepancies preserved.

One proposed discriminating bounded independent computation, if candidate outputs permit: select only pressure basis index14 (node x=4). Independently integrate the two LOS segments [3,4] and [4,5] with 32-point Gauss-Legendre quadrature at actual pixel radii; derive angular radii using a vector/cross-product atan2 formula; independently apply the declared cached beam and masked annular weights to all15 bins. Compare the first12 with pinned old H and last3 with the candidate new response. Expected absolute/relative response tolerance 1e-10+2e-9*abs(reference). This is one basis/one fixed grid, not a duplicate full fifteen-basis run. Record coverage and constant-offset checks in the same run. No covariance, pressure fit or force inference. Preserve source/contract/runner provenance before execution.
