# Pre-run refinement extension

The initial cap17 run failed due to uncaught DOP853 dense-output stage error;
its exact source is planar_first_attempt.py.txt. The handler was moved to cover
those stages. Physics, tolerances and Newton rules were unchanged. Historical
manifests retain original hashes and are not silently relabeled current runs.

The corrected runs at33 and65 stop near t=.81 with small positive nodal cap
gap but near-saturated polarization. Dense interpolation at t=.8 already shows
more saturation than nodal values at33. This motivates cap129 and cap65tight,
with the same data, time target3 and original 300second bound. No new physical
parameters or relaxed success thresholds. Purpose: discriminate resolved
singularity from increasingly sharp polarization/lapse profiles and Fourier
ringing. These runs alone cannot establish singularity.

Continuum check: when F=1+gamma Dp stays nonzero, the exact polarization equation
is (log N)_x=(exp(A) W_P-gamma(Dp)_x)/F. A smooth bounded right side on the compact
circle has a strictly positive exponential solution if its period integral
vanishes. Thus a negative truncated Fourier lapse with bounded coefficients
is NOT by itself a continuum zero of N. Track dense polarization domain,
continuum equation residuals and grid convergence, not just algebraic discrete
constraint residuals.

The129 endpoint moves from .8115 to .8275, so stopping-time convergence has NOT
been established. Authorize one257-node run with the same parameters, tolerances,
target and300second cap to determine whether this drift continues. It is a
resolution diagnostic, not a new physical example. Preserve partial output.
