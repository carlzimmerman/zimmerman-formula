# Moving-source inverse production is not kinematically excluded

2026-10-11. Adversarial check of the uniform coherent source used in
[ENVELOPE.md](ENVELOPE.md). This identifies a missing channel; it does not
calculate its rate or show that it ruins cold production.

## The same vertex opens another channel

The interaction is -(mu/2) h Y^2, with mu=M^2/f. It permits Y+Y -> h as
well as h -> Y+Y. The envelope retains the inverse process only for exactly
opposite momenta returning to the homogeneous source. In the field theory,
daughters from different pairs can instead form a moving radial quantum.

For physical incoming momentum magnitudes p and q and angle theta,

\[
 s=2m^2+2(\sqrt{m^2+p^2}\sqrt{m^2+q^2}-pq\cos\theta).
\]

The inverse process is on shell when s=M^2. Therefore

\[
 \cos\theta_*={\sqrt{m^2+p^2}\sqrt{m^2+q^2}+m^2-M^2/2\over pq}.
\]

It is allowed if this lies in [-1,1], with source momentum squared
K^2=(sqrt(m^2+p^2)+sqrt(m^2+q^2))^2-M^2. These follow directly from
four-momentum conservation; conventions match the
[PDG kinematics review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-kinematics.pdf).
No rate or cosmological result is imported from that reference.

For equal magnitudes and M=2m sqrt(1+u_*^2), the expressions simplify exactly:

\[
 \cos\theta_*=1-{2m^2u_*^2\over p^2},\qquad
 K^2=4(p^2-m^2u_*^2).
\]

At the band center p=m u_* only opposite momenta work and K=0. Above that
center, non-opposite momenta can create K>0. For p^2/m^2=1.2u_*^2,
cos(theta_*)=-2/3 and K/m=sqrt(0.8)u_*. The exact cold daughter band spans
both sides of the center, so the new channel cannot be discarded on
kinematic grounds. Below-center equal momenta fail this on-shell test.

## Diagnostic from the saved spectrum

[inverse_channel_v2.py](inverse_channel_v2.py) uses physical momenta at x=200
from the three resolved envelope quadratures. For independent draws from
its number-weighted *magnitude* distribution, about 0.276 of magnitude pairs
admit some resonant angle. Values are 0.27633, 0.27670 and 0.27607 for the
512-, 1024- and wider 768-cell grids. These are only approximate diagnostics;
the threshold indicator is discontinuous and has not been separately
converged to high precision. Between 36% and 37% of the sampled daughter
number lies above the equal-momentum threshold.

**These are not collision probabilities, angular fractions, conversion
fractions or rates.** An exactly on-shell angle is a surface, and a rate
requires the energy delta function or finite-time kernel, matrix element,
phase-space Jacobian, Bose factors and correlations. The product magnitude
weights omit those correlations. The maximum allowed source momentum in
the retained interval also depends on the interval endpoint, not only on
appreciably populated modes; it is not a spectral prediction.

Six finite checks pass, including exact equal-momentum cases and bounded
weights. [Results](inverse_channel_run_v2/results.json) and
[manifest](inverse_channel_run_v2/manifest.json) record them. The original
run failed while serializing a NumPy boolean, before saving scientific
results. The corrected version explicitly converts check flags to Python
booleans; original source and failed manifest are retained. Kinematic
formulas were not changed by that repair.

## Consequence for the candidate

The small direct Hartree shift in [HARTREE_BOUND.md](HARTREE_BOUND.md) does
not control this near-resonant trilinear process. Likewise, the n=2 radial
band calculation tests spontaneous radial growth about a daughter-free
background, not daughter-driven inverse production after amplification.
Neither result closes this omission.

Moving source particles formed this way are still nonrelativistic in the
examples above. Redistribution need not destroy a cold gravitating sector,
but it can alter the claimed daughter fraction, coherence, and subsequent
scattering. Thus the uniform-source envelope establishes a candidate
production process in its stated truncation; its endpoint fraction is not
currently a justified yield for the complete action.

Next discriminating calculation: retain nonzero radial momenta in a
momentum-conserving three-wave evolution, seeded by the existing daughter
covariances, and track both species' energy and pressure. A dilute collision
formula alone is not reliable at the enormous occupations of this benchmark.
A proof that the combined sector remains cold despite redistribution would
also advance the actual target without requiring a fixed daughter fraction.
