# Local capture works mechanically; the astrophysical separation is not achieved

We built **local collision conversion with independently moving tethered and
free packets**, coupled to live gravity. Both reversible conversion and a
radiative capture channel conserve the modeled total energy. They produce
some T from an entirely F initial state, but the tested interactions do not
preferentially produce tethered rotating systems or preserve the acceleration
relation. The original scientific goal remains open.

These are synthetic, softened particle experiments, not observational fits
or a derived microscopic theory. Particles move in 3D; the tether field is
still a spherical average about the center of mass.

## What changed from the collective model

- Every medium packet has an individual T/F state, position and velocity.
  T feels its field force; F has no individual field charge. They can move
  apart. A direct equal-position comparison verifies their different forces.
- A nearby baryon encounter pays the **full finite field-energy change** from
  relative kinetic energy. A central impulse conserves pair momentum and
  angular momentum. Reverse conversion returns the field energy to motion.
- The activation barrier uses locally estimated baryon circulation, with
  noise controls. No galaxy name or global rotation flag enters a reaction.
- A second channel removes 91% of the remaining normal collision energy
  after F->T activation and puts it in an explicit radiation receiver. This
  tests trapping by cooling while preserving energy bookkeeping.

All numerical masses/scales are crossed with the same initial rotation and
shape families. The two states retain the same positive mass. No extra mass
is created to improve a residual.

## Results

The final evidence contains **63 completed trajectories** across reversible,
radiative, barrier-off, seed, particle-resolution, timestep, softening,
cooling-off and longer-time tests. Earlier estimator/rate experiments are
preserved separately and are not pooled into these results.

For the radiative channel, beta=4, flattened initial configurations, four
initial dynamical times, the two-seed ranges are:

| Initial baryon mass (solar masses) | Scale (kpc) | T fraction, unordered velocities | T fraction, strong initial rotation |
|---|---:|---:|---:|
| 300,000 | 0.3 | 6.25–9.38% | 9.38–15.63% |
| 100 million | 1 | 9.38–12.50% | 6.25–12.50% |
| 60 billion | 3 | 6.25–15.63% | 12.50–15.63% |
| 100 trillion | 300 | 15.63% | 12.50–15.63% |

Rotation does not consistently increase the T fraction. These two-seed spans
are not confidence intervals; one packet is 3.125% at this resolution.

Across all 63 final-branch tests:

- The largest final global T fraction is **28.13%**, versus the illustrative
  95% formation target. The largest T fraction enclosed by the current baryon
  half-mass radius is **33.33%**. An inner T-dominated component is not hidden
  by the global average in these saved endpoints.
- The smallest maximum monopole acceleration residual is **0.278 dex**, above
  the .05-dex target. No run passes the joint formation/acceleration test.
- **71.88–96.88%** of the initial reservoir remains snapshot-bound and free.
  That is approximately 3.9–5.2 initial baryon masses, given the assumed 5.364
  reservoir. It does not establish enough mass for measured dwarfs or clusters.
  Some cases fail even the illustrative 90%-retention gate.
- At eight dynamical times, the radiative 100-million-mass model has 12.5% T
  with either initial kinematics. The 60-billion-mass model has 21.88% T with
  unordered velocities and 12.5% with strong rotation. Longer runs do not
  rescue the proposed separation in these tested pairs.

Capture and release are both active. For example, the rotating 100-million-
mass radiative run makes 17 captures and 15 releases in four times. Removing
some outgoing energy does not ensure permanent capture after subsequent
gravitational motion and encounters.

## Conservation and numerical checks

The maximum relative total-energy error is **1.54e-5** across the final suite.
The maximum single-reaction energy discrepancy is **3.33e-17** in the chosen
normalization; angular-momentum drift stays below **8.36e-15**. Independent
force derivatives, inverse impulses/barriers, collision-flux measure,
translation, rotation and velocity-boost checks pass. Eleven final evidence
manifests cover the nine dynamical batches, invariant tests and final analysis.

The final circulation estimator passes fresh synthetic noise controls: mean
noise-only C=.007–.015, versus .740–.947 with imposed rotation plus noise.
That is a finite statistical calibration, not a proof for every velocity field.
See [estimator amendment](ESTIMATOR_AMENDMENT.md) and
[incoming-flux correction](FLUX_AMENDMENT.md) for the retained failed versions.

## Limits that matter

The local encounter kernel is coarse: its median radius ranges from .77 to
7.44 baryonic half-mass radii across final configurations. Thus **microscopic
locality and the continuum limit are not resolved**. The algorithm confines
reactions to its neighbor kernel; it does not yet establish a short-range
particle interaction in real galaxies. Particle refinement changes some
fractions appreciably, so quantitative phase fractions are not converged.

The tether-field monopole, its common center-reaction force, numerical
softening and packet self-energy remain approximations. The radiative receiver
is a cold, zero-net-momentum Newtonian closure, with no photon absorption or
relativistic completion. Binding is instantaneous in an evolving potential.
The RAR diagnostic is a mass-profile comparison, not a disk rotation-curve fit.
Flattened initial conditions are not evidence of cosmological disk formation.

The useful result is a conservation-consistent transport and reaction model
that can now test proposed capture laws. This candidate's barrier and
radiative loss do not supply the desired selective formation. That finite
failure is not a no-go theorem for all two-state interactions.

[Derivation](DERIVATION.md) · [Self-audit](AUDIT.md) · [Checkpoint](HANDOFF.md)
· [Figure](results.png) · [Final machine-readable analysis](run_analysis_final/results.json)

## Reproduce the principal runs

From this directory with Python, NumPy and SciPy:

```sh
OPENBLAS_NUM_THREADS=1 python3 capture_v4.py --betas 4 --duration 4 --output /tmp/capture-reversible.json
OPENBLAS_NUM_THREADS=1 python3 capture_radiative.py --betas 4 --flats .25 --duration 4 --output /tmp/capture-radiative.json
OPENBLAS_NUM_THREADS=1 python3 invariants_v4.py /tmp/capture-invariants.json
```

Exact commands, seeds, versions, source/result hashes and bounds for all
controls are in the final `run_*/manifest.json` files. Final reversible folders
end in `_v4`; radiative folders begin `run_radiative`. `run_analysis_final`
combines those records. Earlier unversioned/v3 folders are historical.
