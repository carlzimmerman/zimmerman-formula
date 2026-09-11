# Same-action cosmological bridge implementation plan

Base: 4dc6e9c79133f9b71ea8835df20739cf5d26fb1e. User approved the preceding
four-step plan. This is a bounded extension of the existing quadratic ADM
calculation, in the live checkout as requested, not a new coefficient fit.

Goal: obtain finite-wavelength metric/clock/matter Euler equations and Ward
checks from the existing action, and run a separate genuine GR comparator.
Architecture: keep the longitudinal spatial shear until variation, add
minimally coupled radiation and irrotational dust, and compare stress against
an independent covariant derivation. SymPy exact algebra; existing CLASS for
the GR reference. The physical frozen clock coefficient functions remain those
in nonlinear_evolution_2026/constitutive.py. Their historical reconstruction
and missing exponential MOND law remain explicit limitations.

- [x] Write tests for the unrestricted-shear variation, matter sources,
  independent stress components and homogeneous versus finite-k sectors;
  run the missing-feature failure before implementation.
- [x] Derive and export the quadratic action and all scalar Euler equations,
  check finite-k Ward identities, lapse/momentum sources and shear equation.
- [x] Run a separate pure-GR comparator with no clock sector in CLASS in the
  existing Python 3.13 environment; this is not a physical GR-recovery proof.
- [x] Independently review, record exact commands/hashes/status, and run relevant
  existing tests.

An additional short homogeneous trajectory with baryons and radiation passed
both constraint/charge checks with the old coefficient functions fixed.
The next finite-k transfer reduction is recorded but not yet integrated.
Integration step: commit/push only this package and its parent checkpoint link;
git history and the final handoff record the resulting commit.

Distinct checks: (1) raw ADM expansion, (2) independently varied covariant
stress/current identities, (3) GR positive control. A disagreement stops the
downstream interpretation. No CMB inference precedes a same-action radiation
background and validated perturbation integration. No new Lean statement is
called a full-theory proof. Coefficient selection, full nonlinear DOFs, galaxy
asymptotics, exact MOND, caustics and empirical cosmology remain separate gates.
