# Audit and outcome

## Electronic calculation

`run_surfaces`: completed. Fixed-nuclei spin-adapted FCI includes electron-electron
repulsion and exchange in finite Gaussian bases.46 R points from .4 to20 use
aug-cc-pVDZ. Four R values1.4,2,4,10 are additionally computed in aug-cc-pVTZ;
the two atomic/anion basis calculations set consistent approximate asymptotes.
One-electron eigenvalues use the orthonormal molecular orbital representation.
Spin-square checks distinguish singlet0 and triplet2. Nuclear J=0 mass50
reduced-mass kinetic energy uses Dirichlet boundaries at.4 and20, PCHIP
interpolation of the DZ curve and three mesh spacings.

The ground nuclear binding stabilizes under mesh refinement, but basis error is
much larger. At R1.4 the DZ-to-TZ singlet shift is about−.008025. The TZ result
is still about .001843 above the published high-accuracy BO result (SOURCES.md).
Thus no resonance-width or high-precision scattering claim is justified.
No continuum boundary, neutral resonant excited-state basis, autoionization
width, nonadiabatic coupling, R matrix or physical S matrix was calculated.
No finite-mass anion or full four-body bound calculation was done.

Outcome: **conditional finite-basis channel evidence**, not computed collision
rates. A known additional Coulomb bound channel is not a new physical interaction.

## Interface calculation

`run_audit`: completed. Tests check the independently integrated unit-loss
Maxwell formula, reject probabilities>1, verify both conservation identities
and equilibrium built from the prior Saha relations, and integrate finite
forward/reverse reactions. A separate manufactured DR+photon integration uses
a unit-loss single-block fixture; this is deliberately labeled physical_rate=false.
A zero-rate callback reproduces the prior radiation RHS exactly. Central
finite-difference derivatives independently check the coupled Jacobian.
Energy error6.94e−17, charge1.11e−16, directional Jacobian relative error1.60e−9.
These are numerical implementation checks, not accuracy estimates for nature.

Outcome: **implementation and finite assertion verified in stated tests**.
No true scattering dataset was passed to the interface. Physical finite-rate
halo trajectories:0. The previous radiative-only/rapid-collision results are
not recomputed or reclassified as finite-rate predictions.

## Applicability and parameters

The four original profiles enter only through masses/radii and the common
microscopic parameters. The Born diagnostic uses one representative energy
3T/2, not a rigorous Maxwell-averaged error bound. All four have eta>1 and are
not in the plane-wave weak-Coulomb regime. The point-Coulomb enhancement is
not used as a rate or as a universal bound for molecular scattering.
The unit-loss optical-depth numbers are per unit-weight incoming block with
unit reactant fraction, not actual reaction times or evidence for rapid LTE.

No rate normalization, density switch, morphology flag, formation energy fit
or cross-environment tuning was introduced. Removing a free normalization via
dimensional scaling does not remove the need to compute its dimensionless
scattering function. Charge conservation in the existing restricted network
must be extended when negative ions become dynamical.

## Dependency/provenance limits

Runner manifests pin all local code, imported previous-stage code and spectrum
data. PySCF and its basis library are version-pinned external dependencies,
not vendored/hash-pinned wheels. Surface results are conditional on that
library. OpenMP-unavailable warning is recorded; runner sets numerical thread
limits and PySCF uses one thread where supported. All supplied assertions passed.
No manuscript or earlier pinned scientific inputs were modified.
