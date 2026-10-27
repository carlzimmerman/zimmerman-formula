# AFG-004–006: from ideal moments to a measurement operator

Date: 2026-09-27. Base Git revision at resumption:
`eccd1c0e59459b5ec1acf2e916fb7a05a7f67971`.
Parent scientific checkpoint: AFG-003 in this campaign, not a different agent's
work. Owner: this chat. Write scope: `campaign_fresh_gravity_astra/stage_02/`
and a new status link in the campaign README. Earlier evidence is immutable.

Target remains a gravity explanation from Zimmerman's core; this stage attacks
the first unresolved implication in applying the derived measurement test.
No imported theoretical mechanism or literature search. Existing scales remain
9.3619e-11 and 1.1279e-10 m/s², with vacuum scale versus H(z) carried separately.
The study below uses dimensionless B/a_reference, radius/r_reference, and
velocity/sqrt(a_reference*r_reference); a is the scale ratio, not a new fit
normalization. The exact polynomial estimator applies only to the algebraic
Q branch. RAR is a distinct forward law and a negative control.

## Three executed questions

1. Can a fourth-moment identity survive varying radius and projection without
   dividing by a nearly zero projection? Derive the weighted identity, inject a
   disk tracer on an explicit radial baryonic field, and recover scale a=1 and
   a=E(3), with Gaussian and symmetric non-Gaussian broadening.
2. Can spatially varying broadening be removed after a known PSF mixes the
   pixels? Derive the required linear equation for observation weights. Test
   its residual, noise amplification and a rank-deficient counterexample.
   Nonexistence of this law-independent linear correction does not imply
   impossibility of fitting a fully specified gravity/velocity model.
3. Are a and unknown common Gaussian width identified by moments two and four?
   Derive the scalar inverse map and its curvature, construct two positive-width
   models with a=1 and E(3) sharing both moments, and test the sixth-moment
   separation. This is a counterexample to universal two-moment identifiability,
   not equality of full spectra.

## Finite experiment and failure rules

Binary64; no empirical spectra. The physical disk model is synthetic and its
emissivity, source field, inclination and response are known inputs. No
calibration or posterior is taken from real equipment. Grid, PSF widths,
noise seed, photon budget and replicate count are explicitly recorded in code
and manifest. Include exact moment expansion, independent line quadrature,
adjoint residuals and a Poisson-photon Monte Carlo with covariance included.

A noiseless identity must recover a to 1e-8 relative whenever the declared
linear equation has been solved to adequate precision. A singular or noisy
inverse is reported, not rescued by dropping inconvenient pixels. Finite Monte
Carlo is a check on an analytically derived variance, not an empirical forecast.
Both normalizations are used when quoting physical velocities/widths.

This stage cannot establish a relativistic action, lensing closure, a fit to
all evidence, historical novelty or a real-instrument detection threshold.
