# Meaning of stored radial diagnostics

`radial_run_003` stores generalized Rayleigh/Ritz values of a trial space whose
scalar perturbations minimize the static quadratic energy. The inertia in
that trial space uses a declared scalar speed squared equal to h_star.

- `lowest_omega2_ritz` and `refined_lowest_omega2_ritz` are finite-subspace
  generalized eigenvalues. Their negative sign supplies a negative-energy
  witness under the declared positive-inertia reduced-fluid completion.
- `reduced_mode_efolding_time` is the inverse square root of that trial value.
  It is only a Galerkin estimate, **not an actual measured or solved coupled
  halo growth time**. The calculation does not solve the frequency-dependent
  exterior scalar tail or include its exact kinetic inertia.
- No physical seconds/years or galaxy mass is inferred from those numbers.
- Scalar static-tail energy is included in the curvature matrix. All quoted
  adverse conclusions use the converged quadratic-energy sign, not a claimed
  continuum growth rate.

The original machine-readable output is retained unchanged for provenance.
The canonical kinetic screen uses explicit `rayleigh` terminology and does
not turn a negative energy saddle alone into a Vlasov instability theorem.
