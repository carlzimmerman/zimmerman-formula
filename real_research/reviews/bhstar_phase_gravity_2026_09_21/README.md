# A missed JWST test: weigh a black-hole star through its changing gravity

**Result: a derived, testable application missing from the inspected BH*
campaign—not an established new law of nature.** It turns the campaign's
unresolved dynamical-gravity correction into an observable consistency test.

For a spherical material photosphere with constant enclosed mass,

\[
\boxed{R(t)^2\,[g_{\rm spec}(t)-\ddot R(t)]=GM.}
\]

The fitted atmospheric gravity contains the acceleration of the gas. Treating
it as GM/R² at every epoch can mistake pulsation for mass. Write
R=R0 q, with q obtained from the *relative* bolometric flux and temperature:

\[
q=\sqrt{F/F_{\rm ref}}\,(T_{\rm ref}/T)^2,
\qquad g_{\rm spec}q^2=A+R_0q^2\ddot q,
\qquad M=A R_0^2/G.
\]

This gives one line across epochs. Its slope gives radius; its intercept gives
mass once the radius is known. Neither an assumed Eddington ratio nor a
pulsation-mode constant is needed. Common absolute flux calibration and
magnification cancel. Relative lens magnifications and atmosphere physics remain.

The practical advance is an **integral implementation**: for smooth weights
vanishing with their first derivatives at the observing window's ends,

\[
\int g_{\rm spec}w\,dt
=A\int q^{-2}w\,dt+R_0\int q\,\ddot w\,dt.
\]

Only the chosen weight is differentiated. The observations need no numerical
second derivative, no complete period and no assumed sinusoidal waveform.
Several independent weights test the same two constants. A full cycle also
predicts a k² acceleration scaling across harmonics, each returning the same
positive radius.

## A sharp prediction

At maximum radius, positive fitted gravity requires

\[
M\ge R_{\max}^2|\ddot R_{\max}|/G.
\]

For an assumed sinusoid with mean radius 941 au, a 32-year **rest-frame** period
and 10% radius amplitude, this requires **M >= 98,459 solar masses**. A 10,000
solar-mass object at that radius and period is limited to **1.20% radius
amplitude** under the same assumptions. These are forecasts, not measurements
of an object. The radius is a stack-scale illustration; the 32-year value in
the RX1 paper was model-adopted, and luminosity amplitude is not radius amplitude.

## What this changes in the repo

Wave U's Eddington cancellation becomes

\[
\Gamma_{\rm es}(t)=
\frac{\kappa_{\rm es}\sigma T(t)^4}{c[g_{\rm spec}(t)-\ddot R(t)]}.
\]

The existing value 56.6 is conditional on negligible acceleration. The new
inversion provides a route to measuring the missing term. It measures total
enclosed mass; it does not automatically isolate the black hole's mass.

A secondary result replaces the proposed exterior Balmer-layer radius test
with a mass-independent density ceiling. Under the static median gravity and
the local-density transition premise, an exterior layer must have
**n_H <= 1.13e6 cm^-3**. At n_H=1e10 the predicted radius is only 0.103 of the
photospheric radius. Applying this to real absorption requires the correct
emitting-region geometry and true gravity; it is not an observational exclusion.

## Standing and next decisive evidence

The photosphere must follow a material layer and the atmosphere model must
represent its support correctly. Winds, moving opacity fronts and shocks can
break that identification. Even a perfect fit can hide certain systematic
accelerations, explicitly demonstrated in the checks.

The stellar photometric-hydrodynamic idea is known (Barcza 2003). The addition
here is its application to the recent BH* campaign, the integral estimator,
and explicit ways to falsify the inference. **No observed detection yet.**

R2211-RX1 is a motivated target, but the checked paper lacks phase-resolved
atmosphere gravities. The next needed dataset is a joint time sequence of
host-corrected bolometric flux, temperature and gravity-sensitive spectra,
with rest-frame timing, lens ratios and radiation/velocity consistency checks.
Do not use the existing population substacks as successive times of one star.

## Evidence and reproduction

* [PROOF.md](PROOF.md): physical premises, derivation, integral estimator,
  cycle/harmonic identities, mass bound and failure cases.
* [LITERATURE.md](LITERATURE.md): exact primary versions, attribution and scope.
* [REVIEW.md](REVIEW.md): adversarial self-review, including an undetectable bias.
* [verify.py](verify.py): exact algebra plus deterministic mock recovery.
* [certified/result.json](certified/result.json): 153 passing checks, 18 inverse
  problems at three resolutions; maximum final relative recovery error 1.46e-8.
* [certified/manifest.json](certified/manifest.json): hashed execution provenance.

From the repository root:

```bash
python3 real_research/reviews/bhstar_phase_gravity_2026_09_21/verify.py /tmp/bhstar-phase-check
```

The checks establish the implemented conditional mathematics. They do not
establish a new force law, global literature novelty or empirical confirmation.
