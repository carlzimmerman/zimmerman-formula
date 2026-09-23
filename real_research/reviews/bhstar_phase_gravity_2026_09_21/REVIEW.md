# Adversarial self-review

Reviewer is the author, not an independent agent. Read the primary source's
gravity convention, reconstruct the momentum equation, then test alternative
physical interpretations before judging the numerical output.

1. **Sign and radiation:** subtracting the static from the accelerating momentum
   equation gives g_s=g_N+a, with outward a positive. Radiation cancels only when
   the atmosphere model and actual layer have the same radiative support. A
   gas-only pressure gravity would require a different formula. Scope is explicit.
2. **Pattern versus material surface:** optical-depth radii need not move with
   gas. This is the main astrophysical obstruction, not a small statistical
   correction. A radiation-hydrodynamic model or matched velocity tracers must
   justify the application. A residual is not automatically new gravity.
3. **Parameter independence:** relative photometry determines q, not R0. The
   time-dependent acceleration supplies the physical length scale. Rank two is
   necessary; a constant q cannot determine radius or mass. Three epochs test
   a direct line only if accelerations have independently been estimated.
4. **Weak formulation:** both endpoint conditions on w are required. They kill
   [w q'-w' q] exactly. The code differentiates polynomials, not the observed q.
   Correlation between the six moments is not ignored in a claimed likelihood:
   no observational likelihood is claimed or implemented.
5. **Cycle averages:** a population stack is not a phase average. The Fourier
   and cycle inversions require a full cycle with correct time weighting. The
   finite-window version needs neither periodicity nor an assumed mode constant.
6. **Undetectable errors:** an acceleration error in the two-column model space
   gives a perfect but biased fit. A specific injected example passes the null
   with A increased 20% and R0 increased 30%. Thus passing does not uniquely prove
   a single material photosphere, much less a new law of nature.
7. **Data boundary:** neither the four stacks nor the sparse RX1 light curve
   supply the needed g_s(t),F(t),T(t) record. In particular, the model-adopted
   32-year period is not independent evidence for a low mass. No observed source
   is excluded by the illustrative 10% amplitude calculation.
8. **Enclosed versus BH mass:** this method measures total enclosed gravity.
   It cannot separate a BH from a massive co-moving envelope by itself.
9. **Scope of density bound:** it applies to an exterior absorber around the
   same point-mass-dominated photosphere with known true gravity. It cannot
   transplant a broad-line-region covering factor onto a continuum disk or
   turn a CLOUDY slab thickness into a radius. No observed exclusion is claimed.
10. **Novelty:** the governing stellar method predates JWST. The useful addition
    is its explicit deployment against the campaign's net-gravity ambiguity,
    with a finite-window implementation and a harmonic consistency test.

## Computation review

The deterministic mocks exercise three masses/radii/periods, three smooth
waveforms, two observing spans and three integration grids. Analytic-acceleration
regression and two independent full-cycle inversions cross-check the integral
estimator. Frame errors, flux magnification, constant-radius degeneracy and
detectable/undetectable acceleration errors are separate tests.

During development, a guessed lower threshold of 0.003 for the deliberately
perturbed weak residual failed: the six smooth weights yield 0.0015226, while
the clean quadrature residual is 3.9e-12. Smooth integration attenuates the added
third harmonic. The assertion was replaced by a comparison to the actual clean
numerical floor, with a 1e-6 minimum. This is a code diagnostic, not an adjusted
observational significance threshold. The finite residual remains far above
quadrature error; no noise model or statistical detection claim follows.

The final certified run verifies algebra and deterministic recovery. It does
not validate an atmosphere code, a radiation-hydrodynamic simulation, or an LRD
measurement. The proof contains the universal conditional argument; repeated
mock success is not a proof of its physical premises.
