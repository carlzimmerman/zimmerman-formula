# FGF-028: response rows beyond two target radii

Change only the observation rows. The source is the same ZW1215 center,
fiducial angular diameter distance and 512-square CAR patch used in FGF019.
The same fifteen continuous linear pressure hats at the registered nodes
vanish at x=5 and outside. Pixel radii use spherical separation; the beam
uses the inherited tangent-plane FFT, source zero-padded to 1024 square,
cached isotropic transfer interpolated in ell, and cutoff ell>17000 zero.
The constant post-convolution offset is fixed at zero as in FGF024.

For each ring [2,3), [3,4), [4,5), use finite map/mask pixels with mask>0,
and normalized mask weights. A finite map value only selects valid pixels;
this task does not fit those values. For each pressure hat, analytically
project along the line of sight, convolve, then average with these weights.
This produces C with three rows and fifteen pressure columns. Repeat the
old twelve rings on the same patch, report exact/relative mismatches against
saved H and stop if relative Frobenius discrepancy exceeds 1e-12. No silent
replacement of saved H: residual rows always use the pinned original H.

The projector and convolution arithmetic are explicitly adapted from the
read FGF019 source, without importing its top-level code. This is a changed
execution/control, not an independently derived response model. LOS direct
quadrature and constant-weight checks are repeated. Geometry, ring statistics,
weight/radius hashes and saved compact operators support separate root review.

With pinned inner A, outer O, K=A^-1 O and missing row m from FGF024, form
D=C_outer-C_inner K. Apply its reviewed exact validator to all three single
rows, all three pairs and all three together. The coefficients are computed
in binary64 and then interpreted as exact rationals solely for finite row-space
statements. A rank increase is not an observational significance statement.

For any identifying subset, save exact reconstruction weights t on the old
plus added Compton-y bins so g=t d. Report singular values and condition
numbers of D and the full fifteen-column augmented response. Also report
row-normalized D conditioning separately: raw rows have y per normalized
pressure units, while normalization changes their scale and not their span.

Use a deterministic synthetic data perturbation delta d_j=epsilon sign(t_j),
epsilon=1e-8 y, which attains |delta g|=epsilon sum|t_j| exactly. This arbitrary
synthetic epsilon is not a measured uncertainty. It tests amplification and
reconstruction, not covariance, confidence or robust empirical inference.
Preserve numerical conditioning even if exact rational rank is full. Include
a duplicated outer-row negative control and a wrong-target witness check.

Exactly three new rings, no support/grid/beam sweep and no new data fit.
Physical response approximations and shared-map covariance remain unauthenticated.
The observed rows are not independent instruments. Any later MOND source
bridge needs density and total/electron-pressure conversion and preserves
both a0 normalizations, separate vacuum/H histories and Q/RAR/registered M.
No force, mass, metric coupling or theory closure is inferred here.

Bound each computation at 120 s wall/110 s CPU, cooperative one-library thread,
1 MiB logs, no claimed memory cap. Fixed deterministic inputs, no randomness.
