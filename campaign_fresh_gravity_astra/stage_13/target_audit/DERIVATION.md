# Independent full-response target and sensitivity audit

The candidate extends the inherited twelve pressure-response rows to fifteen
by three outer annuli. Offset is assumed fixed and subtracted, pressure at
x=5 fixed zero. The stored finite pressure matrix U has fifteen columns and
rows. This audit will not reconstruct a pressure profile from observed data.

Independently solve U^T r=L^T over the exact rationals represented by its
stored binary64 coefficients. Then r U=L is a direct target-reconstruction
certificate, independent of block Schur elimination. If U is invertible,
g=L p=r y for noiseless y=U p. For each proper subset of new rows, test rank
before/after appending L; nonmembership supplies a null direction that changes
g while preserving those rows. The strict inherited baseline makes small
both-sign null perturbations admissible. A full-rank operator is a finite
coefficient fact, not an instrument-calibration or continuum statement.

For perturbations of the fixed response data satisfying |delta y_i|<=epsilon,
|delta g|<=epsilon sum|r_i|. Equality is attained by the deterministic vector
delta y_i=epsilon sign(r_i). This is an exact worst-case deterministic bound
for independent componentwise error allowances; it is not a covariance,
noise model or confidence interval. Keep raw annular-y units, dp/dx target,
and no arbitrary row rescaling. Numerical condition numbers depend on that
choice and must be labeled separately from the exact certificate.

A common post-convolution offset error delta b produces delta g=(sum r_i)
delta b, because normalized annulus weights give offset column one. Thus
calibrating the offset remains a separate obligation even if fifteen pressure
columns are invertible. It is a sensitivity derivative around the declared
fixed-offset model, not evidence of an actual offset or a correction fit.
For actual response U+Delta U, the nominal estimate obeys
r y-Lp = r Delta U p + r e. No bound on these physical errors is invented.

The response reviewer must separately verify angular geometry, beam/mask
weighting, finite pressure support and convolution conventions. Exact algebra
cannot authenticate them. No pressure-to-force/source calculation is done;
a later bridge must retain both registered a0 normalizations, distinct constant-
vacuum and H histories and separate Q/RAR/registered M with density/composition.

Negative control with a deliberately changed premise: release the fixed offset.
If v=-U^-1 1, (delta p,delta b)=(v,1)t leaves all fifteen bins unchanged.
Its target shift is -sum(r)t. A nonzero sum therefore certifies ambiguity
when background calibration is removed. Scale t by half the minimum positive
pressure-difference margin to preserve strictly positive decreasing profiles
for both signs. This is a counterexample to dropping the offset premise, not
a measured offset, a refutation of fixed-offset identification, or a new fit.
