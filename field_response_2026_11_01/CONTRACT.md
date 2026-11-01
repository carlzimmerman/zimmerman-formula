# FR01: finite-gradient halo stability and baryon response

User authorization, 1 November 2026: execute the proposed field-response test
and push verified results. This is a bounded experiment in the existing PN28
conditional parent, not adoption of that parent as the physical theory.
`INPUTS.json` pins copied inputs and the observed base revision. All writes
belong to this directory; other research and running jobs remain untouched.

## Question and model

Does the existing pressure-carrying field admit a viable radial response to
ordinary matter without an inserted contraction factor? Use precisely the
PN28 static energy and finite scalar gradients. The chosen potential, canonical
phase level, pressure coefficient and scalar stiffness remain assumptions.
No a0, kappa, measured galaxy scale or fitted response switch enters the test.

The first test is the radial second variation of that energy at fixed dark
mass. An explicitly declared isotropic fluid-plus-scalar *linear* completion
has positive inertia, including the material scalar velocity in the occupied
interior and ordinary free scalar motion outside. This supplies a necessary
stability test. It neither constructs nonlinear vacuum-crossing dynamics nor
proves the collisionless Vlasov hierarchy preserves the fluid closure.
If a negative energy direction is found, report instability of this reduced
completion; do not promote it to a theorem excluding all kinetic realizations.
If no negative direction is found in a finite basis, report a finite screen,
not a stability theorem.

## Frozen finite domains and interpretation

- Reconstruct all six existing equilibria: psi_c = .8,.95,.99 crossed with
  epsilon = .0001,.01. Preserve finite-gradient stress and the exterior scalar.
- Radial displacements xi = r P_j(2(r/R)^2-1), j = 0,...,11, with nested
  sizes 4,8,12. Solve the minimizing scalar perturbation for each displacement.
  Repeat the decisive witness with doubled quadrature and tighter scalar BVP
  tolerance. Negative curvature more than 1e-5 of the summed absolute energy
  terms is adverse; borderline or nonconverged signs are inconclusive.
- Use independent local-energy finite differences, radial gravity integrals,
  the scalar response identity, exact mass variation, and basis/mesh changes.
  A mutation that removes the reciprocal mixed term must fail its control.
- The static response branch is frozen separately in CONTRACT_STATIC.md:
  dark mass and field coefficients stay fixed while a Plummer baryon potential
  is introduced. The two imposed forcings are diagnostic, not observationally
  calibrated dwarf/spiral predictions. Failed continuations are retained.
- Only call a static response potentially viable after its stability status
  is disclosed. An endpoint equilibrium is not a formation trajectory.

Negative curvature is a result, not a software failure. Failed invariants or
changed inputs invalidate the affected numerical interpretation. No universal
mechanism, observed a0, kappa=1/2, cluster repair, mass mapping or cosmological
completion can be inferred from this experiment.

## Resources and evidence

One numerical thread per worker, measured RSS, short runs with 300-second wall
and 240-second CPU ceilings; no production N-body jobs, installations or
changes to existing queues. Preserve source, result, profile and manifest
hashes; create a new run directory on every execution. Freeze the contract
before producing new scientific numbers. Publish the isolated result branch
only after independent mathematical and implementation review.
