# The scattering exposure identity and a variability bound

Status: a derivation within ordinary, leading-order Thomson transport, not a
new fundamental law. The proof is author-reviewed, not independently refereed.

## Precise model

A photon is emitted at time zero, follows straight flights at speed c through
a static medium, scatters elastically off Maxwellian electrons in their rest
frames, and eventually escapes. At position x the electron density is n_e(x)
and temperature is T_e(x). The collision rate is n_e sigma_T c. The normalized
unpolarized angular kernel is p(mu)=3(1+mu^2)/8. Polarization is ignored.

Keep the leading thermal Doppler shift, neglecting recoil, stimulated scattering,
aberration and second-order Compton drift. Define the additive velocity shift
V=c Delta nu/nu_0. Each flight and scattering direction is independent of the
thermal electron velocity at this order. There is no absorption, photon
replacement, frequency-dependent selection or discarded direction. Include
unscattered photons. Initial line variance is finite and independent of the
thermal velocities. Assume finite expected integrated n_e T_e exposure until
escape; this permits localization and the L2 martingale limit below.

The primary theorem is for all escape directions together. Applying it to one
unresolved observer requires rotational symmetry of both the medium and source,
or an independently justified equivalence of that observer's photon ensemble.
Arbitrary clumpy geometry does not automatically satisfy the observer condition.

## Identity

For incoming and outgoing unit directions u and u', electron velocity w gives

    delta V = w dot (u'-u).

Maxwellian covariance is (k_B T_e/m_e) I. Consequently

    E[delta V | pre-collision state] = 0,
    E[(delta V)^2 | mu, pre-collision state]
        = (2 k_B T_e/m_e)(1-mu).

The phase function has E[mu]=0, so the angle-averaged variance per collision is
2 k_B T_e/m_e. Independent centered thermal increments have zero cross terms.
Applying the compensated collision-count identity, first at bounded stopping
times and then taking the integrable limit, gives

    Delta sigma_v^2 = (2 k_B sigma_T c/m_e)
                     E[integral_0^t_escape n_e(X_t) T_e(X_t) dt].       (1)

This does not assume N=tau^2, a diffusion limit, an exponential escape-time law,
a particular cloud thickness, or an exponential line shape. Finite Monte Carlo
checks of continuous flights supplement the argument; they do not prove it.

Equation (1) concerns the entire photon ensemble, not just a fitted wing.
Selecting N>0 after the trajectories finish invalidates the compensator step.
The supplied thin-sphere countercheck produces a factor ~7.8 error from exactly
that selection, despite otherwise perfect Thomson physics.

## Density and temperature lower bounds

If n_e T_e >= Q_min > 0 everywhere on the flights up to the chosen escape surface,

    E[t_escape] <= m_e Delta sigma_v^2 / (2 k_B sigma_T c Q_min).       (2)

For homogeneous gas this is equality. One may replace Delta sigma_v^2 by the
full intrinsic emergent variance sigma_line^2 for a conservative upper bound
when nonthermal birth widths add independently. Instrumental variance may be
left in for a weaker bound, but host-line dilution, line truncation, absorption
and component selection can make the measured variance underestimate the
needed full ensemble variance. They must be addressed explicitly in a fit.

Vacuum cavities or low-density channels invalidate a density lower bound
extended over the full residence interval. Equation (1) still measures weighted
exposure; it no longer bounds unweighted time. In particular n_H from Balmer
absorption is not automatically n_e in the scattering medium.

## From residence time to smoothing

For a point source at the centre of a spherical cloud of radius R, a photon
escaping at r with final outward direction u has excess observer delay

    D = t_escape - u dot r/c,  0 <= D <= t_escape.

Rotational symmetry makes this delay distribution representative of each
observer. For distributed emission at r_0, define delay relative to direct
emission from that same point. Then

    D = t_escape - u dot (r-r_0)/c,  0 <= D <= 2 t_escape.

The factor-two result bounds additional scattering delay. It does not bound
delays in the excitation of different source points by a central driver, or the
geometrical response of an extended emitting region to that driver.

Let H(omega)=E[exp(i omega D)] be the normalized, nonnegative photon impulse
response of a stationary linear transfer process, integrated over the whole
line. Since |exp(i x)-1| <= |x|,

    |H(omega)| >= max(0, 1-|omega| E[D]).                              (3)

Combining (2) and (3), at rest-frame period P and for a central source,

    |H(2 pi/P)| >= max(0, 1 - pi m_e sigma_line^2 /
                               (k_B sigma_T c P Q_min)).              (4)

For distributed emission's additional scattering response use twice the
subtracted term. No assumed shape for the time-response tail is needed.
Rare long paths cannot circumvent (3) while keeping its ensemble mean fixed.

Equation (4) is a necessary constraint on an attempted smoothing explanation.
A non-detection over a 200-day baseline does NOT establish |H(2pi/200d)|<0.1.
One also needs an intrinsic-driver model and the actual sampling, errors,
host dilution and response. A constant engine requires no smoothing at all.

## Numerical, explicitly conditional example

For a FULL Laplace line p(v)=exp(-|v|/b)/(2b), W_FWHM=2 b ln 2 and
sigma_line^2=2 b^2. Therefore at W=2000 km/s,

    E[t_escape] <= 0.796963 days * (W/2000 km/s)^2
                   * (1e10 cm^-3/n_e) * (1e4 K/T_e).

At those density and temperature lower bounds, equation (4) retains at least
97.50% of a 200-day input amplitude for the central-source sphere (94.99% for
the distributed-source additional-scattering bound). Such a layer cannot
provide tenfold suppression on that period under these assumptions.

For that tenfold-suppression hypothesis to remain possible in homogeneous gas,

    n_e <= 2.78193e8 cm^-3 * (W/2000 km/s)^2
                         * (1e4 K/T_e) * (200 days/P) * (.9/(1-A)),

where A is the desired output/input amplitude. This necessary condition is not
sufficient for suppression. If n_e=1e8 cm^-3 instead, the residence upper bound
is 79.70 days and the P=200-day amplitude bound is vacuous. A general LRD
exclusion cannot be inferred from the high-density example.

For an exponential component convolved with a Gaussian, use the FULL variance
sigma_G^2+2b^2 with its correct direct/scattered mixture weights, not its fitted
FWHM as if the entire line were a pure Laplace distribution.

## An exact identifiability obstruction

In homogeneous geometrically similar clouds, transform n_e -> a n_e and every
length -> length/a at fixed temperature and dimensionless source positions.
All optical depths, angular histories and emergent line shapes are unchanged,
while every flight time and delay scales as 1/a. Therefore a static line profile
alone cannot determine a residence time. An independent electron density or
length is mathematically necessary. The catalogue analyzed here does not
supply it. This is why the result is not yet an observed parameter-free law.
