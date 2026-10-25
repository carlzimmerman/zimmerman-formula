# Self-audit of the local capture construction

Primary verdict for the requested astrophysical mechanism: **incomplete**.
The code implements independent transport and conserved local reactions, but
the tested models do not establish the requested rotation-dependent formation
and mass-profile separation. This is self-review, not independent review.

## Exact narrower claims

For positive packet masses, valid field domain z<1, an incoming pair and
enough normal kinetic energy, the central reaction impulse conserves pair
momentum and angular momentum. Its kinetic change is exactly the negative
finite field-energy change, plus the explicit radiative loss when enabled.
The receiver takes that loss. Particle positions and all masses are unchanged
at an event, so Newtonian potential energy and total mass are unchanged.

The fixed-state Hamiltonian is translationally and rotationally invariant.
Its center derivative is included, so net field force and net torque vanish.
The numerical trajectory conserves energy only to integration error; no
post-step correction is used. A tested identical-position T/F pair has
different acceleration, confirming that shared transport was actually removed.

The reversible barrier condition maps exactly to its inverse. The final
encounter hazard includes the normal-speed Jacobian required for flux measure.
This supports the stated continuous-time central collision construction,
not a theorem of full microscopic detailed balance. The radiative branch is
explicitly a cold-reservoir approximation and makes no such reversibility claim.

## Source-to-evidence restrictions

Final reversible implementation: capture_v4.py. Final radiative implementation:
capture_radiative.py. The original capture.py and v3 transport records are
historical experiments, not pooled with the final samples. v2 was a local
estimator pilot, not a successful calibration. The amended noise statistic
was tested on a fresh seed and larger synthetic calibration sample before
interpreting final dynamics. Its numerical threshold remains a modeling choice.

Checks include force finite differences, net force/torque, translation/rotation/
boost invariance, finite field jump, inverse impulse and inverse barrier,
collision flux identity, separate T/F force response, and runtime energy,
momentum and angular-momentum accounting. Both reaction directions were
observed, not merely exercised through a one-way test fixture.

## Important remaining limits

- The field is a COM-centered spherical average even though particles move
  in 3D. The common center reaction is an assumption of this Hamiltonian;
  it prevents interpreting free-particle binding as an exact escape theorem.
- Particles are massive numerical packets, with discrete phase increments.
  Field self-energy, softening and the finite-neighbor encounter kernel need
  continuum study. At this resolution the neighbor kernel can span a large
  part of the baryonic system; microscopic locality has not been demonstrated.
- The rotation estimator is tested on finite Gaussian nulls and imposed spin,
  not all anisotropic flows. It is a resolved-circulation proxy, not a known
  fundamental coupling. Beta, rates and restitution coefficients are assumed.
- Initial mass reservoirs and profiles are supplied. Shape and rotation are
  crossed inputs for all masses, not observed galaxy-type labels. A flattened
  initial configuration is not evidence of disk formation from cosmological
  initial conditions.
- Two seeds and a packet refinement do not establish a probability law or
  convergence of phase fractions. Halving event interval changes the random
  event sequence. Differences of one or two packets cannot be read as a
  robust physical trend.
- The acceleration residual is a monopole mass-profile diagnostic. It is not
  a resolved disk rotation-curve fit, and no measured dwarf/cluster masses
  were supplied. The 95%, 90% and .05-dex gates are illustrative.
- A few initial dynamical times test early formation/retention, not cosmic
  survival. Snapshot-bound free mass remains distinct from asymptotic binding.

The conservation result is useful and survives these caveats. It does not
establish the missing implication: enough durable inner T forms preferentially
in rotating systems while F remains distributed appropriately elsewhere.
