# Local-moment estimator amendment

The first 12-neighbor estimator subtracts the expected squared curl noise.
Clipping a noisy estimate at zero still leaves a substantial positive bias:
noise-only calibration mean C=.17–.32, with some 90th percentiles above .8.
These calculations remain valid records of that model, but are provisional
evidence for physical rotation selection. Do not silently pool them with v2.

Version 2 uses k=round(3 sqrt(Nb)), at least 12 and at most Nb, and subtracts
three times the estimated curl noise before taking the positive part. This
is a conservative resolved-circulation statistic, not an exact unbiased
estimator of microscopic vorticity. The growing neighbor count is intended
to reduce sampling error as packet resolution increases. Neighborhood size,
ridge regularization and the factor three are numerical modeling choices.

Calibration criterion fixed before the v2 check: noise-only mean C<.05 and
90th percentile C<.1 in all four tested size/shape cases; imposed solid-body
spin plus noise should retain mean C>.5. This addresses a statistical false
signal, not a failed phase-fraction target. It does not validate arbitrary
non-Gaussian flows. Dynamics, masses, energy rules and barrier beta are unchanged.

Inner-region diagnostics will supplement global fractions: report T/medium
inside one and two current baryonic half-mass radii, plus F/baryon enclosed
ratios and the actual mass-profile acceleration residual. They are descriptive
post-hoc diagnostics and do not redefine the predeclared joint success gate.

The v2 pilot missed the stated mean-null criterion in the flattened 32-packet
case (mean .06588). It is retained and is not accepted as passing calibration.
Version 3 increases the subtraction to four times the noise estimate. Before
testing its dynamics, repeat the same criteria on a fresh seed 991 with 400
samples per case. This is a post-pilot estimator choice with a fresh finite
validation sample, not an independently derived physical threshold.
