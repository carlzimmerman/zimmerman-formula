# Microscopic capture: bounded candidate test

User authorization: derive a microscopic interaction and test population separation
with universal parameters and no object-type switches. This is a research candidate
test, not a declaration that a UV completion of the tether model exists.

Chosen candidate: distinguishable oppositely charged particles with masses mX=10mC
under a massless U(1), nonrelativistic Coulomb bound states and electric-dipole
ground-state recombination/photoionization. Alternatives: an unconstrained
two-level effective transition would leave the gap and matrix element as inputs;
baryon binding would require a new baryon coupling and observational constraints.
The atomic candidate is selected for calculability, not because it is known to
produce the required tether force. Charge conservation is a required compatibility
test, not something to bypass by assigning atoms a new charge.

Implementation plan (executed inline; no changes to previous solvers):
1. Test spectrum/threshold cross section against hydrogen, integrate forward and
   reverse rates independently and check Saha detailed balance including stimulated
   emission, and test energy accounting under recombination.
2. Implement natural-unit Coulomb formulas with explicit cm/s conversions in
   atomic.py. Document degeneracies and approximation domain.
3. Run bounded experiment.py: 61 universal alpha values 1e-4..0.1 and 31 mC values
   1keV..1GeV, mass ratio10, the four existing numeric mass/radius families; common
   10Gyr duration. Use uniform-volume mean densities and virial temperature as a
   deliberately specified one-zone screen. No morphology-dependent temperature,
   cross section or reaction switch. Fixed-temperature radiative-only abundances
   are subsystem diagnostics, not complete halo predictions.
4. Separately solve four variable-temperature, constant-volume, escaping-radiation
   parcels through dimensionless time10, then repeat with tighter tolerances.
5. Report microscopic derivation, missing processes, charge/field incompatibility,
   numerical evidence and whether the candidate can be identified with T.

Success screen, chosen in advance: ground-state bound fraction >=.8 for the
6e10Msun/3kpc family and <=.2 for each other family at10Gyr. These are engineering
targets, not observed confidence intervals. Report continuous rate ratios as well.
Compute conservative all-neutral photo-opacity and dilution diagnostics. Do not
claim a simulation invalidity screen excludes a physical model.

Primary formula source: Rosenberg & Fan, Phys.Rev.D96,123001 (2017), Eq27,
https://link.aps.org/accepted/10.1103/PhysRevD.96.123001 . Its ground-state
photoionization formula supplies the Coulomb continuum matrix element. Inverse
rates below follow from explicit phase-space balance, not independently fitted
normalizations. Atomic dark matter background: https://arxiv.org/abs/1209.5752 .
Neither source derives the existing tether field. The original Zenodo record
could not be retrieved in this turn; no attribution to its unseen contents is made.
