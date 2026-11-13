# Independent aperture-prior correction review

**Scoped pass: the fixed-shape posterior transport and reported numerical
weights are correct. This is not a full-theory or empirical pass certificate.**

Reviewed `reweight_for.py`, the geometric aperture calculation and
`reweighted_geometry_01/result.json` against the original gated chains and
mass prior. Both the aperture-audit and correction manifests validate against
their current declared inputs.

For fixed light geometry and constant stellar M/L, m_ap=m_total+log10(f_ap).
The Jacobian in these logarithmic coordinates is one. The correct weight is

    w proportional to p_SED(m_total+log10(f_ap) | mu+delta)
                      / p_original(m_total | mu).

The implementation has the correct sign, preserves the exact original
denominator and uses stable logsumexp normalization. It retains the original
two half-normal branches, each with probability1/2 and its own1/sigma density
factor; it does not silently substitute a continuous split-normal prior.
The lower-side scalar survival calculation and representative-scenario label
were corrected before the reviewed bounded run.

An independent calculation using normalized normal densities and a separate
max-log weight normalization agrees with saved normalized weights to
1.1e-19 in the nominal case and3.0e-19 in the optional distance case. The
recomputed importance ESS values are9993.3881 and9992.4428 out of10000.
These are raw importance ESS values, not autocorrelation-adjusted MCMC ESS
or a new guarantee of global posterior convergence.

For f_ap=.8038930178016896, the nominal median total mass is
1.0947472e12Msun and its aperture mass is8.8005963e11Msun. Multiplication byf
independently reproduces the reported aperture mass. It is1.29844867 times
the SED median, or1.313108 quoted upper-error units above it. Those are
correct conditional comparisons, not a goodness-of-fit significance or theory
probability. The total-mass posterior median moves only.00004267dex, as
expected when the image likelihood is much narrower than the mass prior.

The geometric fraction of the exact unit-total profile on the actual pixel
union is the appropriate primary mapping for the same fixed mass-profile
geometry. The .7984476 released-map/COOLEST ratio also reflects map/export
normalization differences; retaining it as a sensitivity case is appropriate.
The optional+.00653358dex case is distance-only sensitivity until the actual
SED input-redshift provenance is established, not a mandatory correction.

The bounded run reports five exactly reproduced original targets and a
representative association diameter .299931arcsec. The latter nearly
saturates the adopted .3arcsec gate: the gate must remain explicit in any
statement about the fit. The representative is the highest new-target value
among sampled points, not a freshly optimized global MAP.

The aperture correction resolves the previous normalization mismatch between
finite-mask SED mass and infinite-profile mass. Remaining conditions include
the fixed light shape/inclination, constant M/L extrapolation, assumed IMF,
Gaussian source model, diagonal released noise, environmental convergence,
and the unscreened smooth-galaxy approximation. No additional investigations
were undertaken for this review.
