# AZ47 lane13 — measure scatter before freezing the new G3 regrade

This protocol precedes scatter measurement. The measured quantities will
be frozen in FROZEN_CRITERIA before evaluating candidate formulas with
the new statistic. Do not change BK2 or reopen its grammar searches.
Kappa=1/2 FITTED; not theory closed. BK2's failure report is already known.

Use BK2's existing local X-COP mass tables and read-only interpolation
definitions at x=r/R500={0.1,0.2,0.3,0.5,0.7}. These are published
hydrostatic/profile inferences with their original calibration assumptions,
not raw photon observations or a new cosmological fit. No new Planck or
LambdaCDM inputs. Keep the original sorted-cluster split: even index
train, odd index holdout. Do not use holdout clusters to set scatter.

For every complete train cluster form y_c(x)=log10[Mhydro/(Mgas+Mstar)].
Compute the sample covariance S across CLUSTERS, after subtracting the
mean at each radius, with n-1 denominator. Report marginal standard
deviations, the complete5x5 covariance/correlation, and leave-one-cluster-
out covariances. Report missing coverage; do not impute any missing point.
Neither radial points nor repeated model fits are independent clusters.

BK2's per-point error variance D_c(x)=se^2+sm^2 combines quoted forward-
mass error and dispersion between hydrostatic mass models. Report these
components separately. A diagnostic intrinsic estimate is the positive-
semidefinite part of S-mean(diag(D_c)), clipping only negative eigenvalues
to zero. This PSD projection is an explicit ESTIMATION ASSUMPTION, not
measured truth; report eigenvalues before/after and clipping size. Its
diagonal alone discards important radial covariance. Unknown measurement
covariances prevent an exact intrinsic-scatter separation; do not invent
off-diagonal errors or pretend this estimates a calibrated chi-square law.

Also report the empirical covariance S with no noise subtraction. This
is directly reproducible total cluster scatter, not necessarily intrinsic
scatter. Subsequent criteria must distinguish an old-statistic bookkeeping
comparison from a new probabilistically calibrated test. A candidate's
systematic mean radial mismatch must not be absorbed as cluster scatter.

Known answers before using measured values: diagonal covariance of a
hand-built symmetric fixture; rank-one covariance of pure cluster-level
offsets; invariance under common radial trend addition; invariance under
cluster reordering; orthogonal-centering annihilates a constant vector;
PSD projection reconstructs a positive fixture and clips a known negative
eigenvalue. Compare direct centered sums and independently accumulated
outer products to1e-12 absolute. Compare40/80-digit arithmetic covariance
to1e-12 absolute, so numerical precision is separated from sampling error.

The measurement has no footing dependence because it uses mass ratios,
but document that fact rather than duplicating its sample. The later
formula regrade must evaluate both a0 footings separately. No candidate
is graded here. Save input/source hashes, cluster names, measured vectors,
covariances, leave-one-out influence, tests, numerical comparison and
explicit limitations. No downloads; missing covariance products, if
required for calibrated inference, are recorded in NEEDS_OWNER.
