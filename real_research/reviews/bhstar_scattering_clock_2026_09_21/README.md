# JWST follow-up: a scattering constraint, not a claimed breakthrough

**Stronger follow-up:** [the density-free lag–width theorem](density_free/THEOREM.md)
removes the electron density from the earlier bound for a central source in a
uniform spherical scattering cloud. Radius R, electron temperature T_e and the
added spectral variance predict an interval for an independently measured lag.
The lag is never used to choose or calibrate those inputs. The illustrative
941-AU, 10,000-K, 2,000-km/s case predicts **11.78–14.24 rest-frame days**.

The proof solves a stopped spatial-transport identity before combining it with
frequency broadening. A new 600,000-photon run tests optical depths 0.03–30;
deliberate density-gradient and distributed-source counterexamples demonstrate
why its hypotheses matter. See the [claim-by-claim audit](density_free/AUDIT.md).
This establishes a conditional mathematical result. It does not establish that
an observed LRD satisfies the model or that the theorem is globally new.

## First-pass result and data analysis

**The requested Kepler-grade discovery has not been established.** This pass
adds a conditional relation connecting electron-scattered line width to photon
residence time, plus a bound on how much the same transport can suppress
variability. It is ordinary Thomson physics. Its application to the campaign is
worth testing; neither global novelty nor observational confirmation is claimed.

The prior phase-gravity result was an application of known stellar dynamics and
did not meet the requested standard. This follow-up uses released observational
data for one route and independent photon-transport calculations for another.

## What survived

For static, conservative, leading-order Thomson transport, including all escaping
photons, the added velocity variance measures their mean electron-weighted
thermal exposure:

\[
\Delta\sigma_v^2=\frac{2k_B\sigma_Tc}{m_e}
\mathbb E\!\left[\int_0^{t_{\rm esc}}n_eT_e\,dt\right].
\]

If density and temperature are independently bounded below along the paths,
this bounds the mean time available for scattering to smooth variability.
The [proof](PROOF.md) does not assume a diffusion approximation or a shell
thickness. The observational use requires a complete line profile and either
spherical symmetry or a justified directional transfer model.

**Conditional example:** a full exponential line with FWHM 2,000 km/s passing
through gas with n_e >= 10^10 cm^-3 and T_e >= 10,000 K has mean residence time
<= 0.797 days. For a central source in a spherical cloud, it must retain at least
97.50% of an intrinsic sinusoidal amplitude at a 200-day rest-frame period.
That layer cannot suppress that signal tenfold merely by delaying its photons.

Conversely, allowing tenfold suppression requires n_e <= 2.78e8 cm^-3 for the
same temperature, width and central-source setup. This is a necessary condition,
not a sufficient explanation. At n_e=10^8 cm^-3 the bound permits 79.70 days and
gives no useful amplitude constraint at that period.

**No observed LRD is excluded here.** The numerical example does not combine
matched measurements of width, electron density and a measured transfer function
for one object. Balmer n_H cannot be substituted for n_e without an ionization
and spatial-association model. TWINKLE's absence of variability is not itself a
measurement of tenfold suppression at a 200-day period.

## Evidence

- Seven continuous-flight simulations, 60,000 photons each, cover radial optical
  depths 0.1–10 for uniform gas, central and distributed emission, and two
  radially varying density/temperature models. They sample 3D Maxwell electron
  velocities and the Thomson angular kernel. The identity agrees within 1.4%
  and 1.5 paired Monte Carlo standard errors; 420,000 photons escaped.
- Separate angular and path-integral checks test the stochastic reduction.
  Applying the formula only to photons selected for having scattered fails by
  a factor 7.8 in the thin case. This explicitly guards against treating a
  fitted broad wing as the full ensemble.
- The released de Graaff v2 catalogue contains 181 spectra and 146 unique
  objects. There are 47 unique z<4.5 objects with usable modified-blackbody and
  total H-alpha luminosities. Their median L_Halpha/L_MBB is 0.06777, with a
  descriptive bootstrap interval [0.05519, 0.08556] and 0.220 dex dispersion.
  This does not establish a 1/15 law. The published paper already reports the
  line–continuum correlation; the apparent rational constant has no unique
  physical derivation. The bootstrap ignores measurement covariance and
  selection effects and is not a likelihood for a universal law.

## Why the observational discovery remains open

The exact scaling n_e -> a n_e, R -> R/a leaves a static Thomson line profile
unchanged and divides all delays by a. A spectrum alone cannot supply the missing
clock. An independent density or length is essential. The stronger follow-up
uses an independently measured scattering radius as that length; the continuum
photospheric radius is not automatically the scattering radius. Absorption/re-emission,
different line and continuum birth regions, low-density gaps and intrinsically
quiet engines provide additional physical alternatives.

The available catalogue lacks line-profile second moments, scattering-region
electron densities and an observed input/output variability transfer function.
It therefore cannot close this test. Collecting more algebra checks cannot fix
that missing evidence. No specific source is promoted as a discovery.

See [route decisions and source checks](LITERATURE_AND_ROUTES.md),
[adversarial self-review](REVIEW.md), and [checkpoint](CHECKPOINT.md).

## Reproduction

Dependencies: Python 3.9.6, NumPy 1.26.4, SciPy 1.11.4, Astropy 6.0.1.
From the repository root, with those dependencies available:

```bash
python3 real_research/reviews/bhstar_scattering_clock_2026_09_21/analyze.py /tmp/bhstar-scattering-result.json
```

`certified/manifest.json` records the actual bounded run, hashes and command.
`certified/result.json` includes all selected catalogue rows, numerical examples
and per-simulation diagnostics. Success verifies these finite computations,
not the astrophysical assumptions or novelty.

The stronger transport extension requires only NumPy and SymPy (recorded run:
NumPy 1.26.2 and SymPy 1.14.0):

```bash
python3 real_research/reviews/bhstar_scattering_clock_2026_09_21/density_free/verify.py /tmp/bhstar-density-free-result.json
```

Its separate evidence record and results are under `density_free/certified/`.
