# Self-audit: NS-20261022

Primary verdict for the original selection-and-preservation claim: **incomplete, with the smallest missing implication** being a converged nonlinear material partition into fragments, bound envelope and ejecta, coupled to field-energy export. No observational fit can be inferred without that partition and settled profiles.

Claim cards and dependency graph:
1. Exact logarithmic W -> Legendre conjugate -> nonlinear elliptic field equation -> source-conditioned scaling defect. Internally derived; numerical discretization and finite source grid checked. This is a fixed-χ quasistatic statement.
2. Field energy + analytic isolated Gaussian gravity -> restricted profile extrema -> radius support. Envelope forces checked by finite differences; separate grid/box checks. These are not general static Euler solutions.
3. Restricted affine matter kinetic energy + quasistatic nonlinear potential + fixed spin -> finite-time nonradial rebound. Time and space refinement support this in the implemented model. No fragments, ejecta, internal spin transfer, radiation or live baryons are represented.
4. Nonlinear passive stationary action -> virial/chemical identities -> decreasing E/M along a differentiable branch. Reviewed against the original derivation in core_formation_transport_2026_10_22/RESULT.md. Uniform dilation does not assume spherical symmetry. Excludes passive interior binding-energy mass selection, not dynamical fragmentation or a branch endpoint.
5. Quasistatic phase equation -> nonlocal quartic dual -> phase probes. Correct gradient check; boundary convergence of phase excess fails. Finite-inertia phase evolution is not supplied by this elimination.
6. Small-amplitude expansion about P=h=0, χ=1 -> unchanged linear kernel. Does not imply unchanged nonlinear cosmology or empirical fits.

Critical implementation checks:
- W*=s-ln(1+s), and P=-grad h/(1+s), are derived rather than guessed saturation prescriptions.
- Difference gradient and divergence are exact discrete adjoints. Quadratic Fourier control uses the same lattice Laplacian; continuum accuracy is separate.
- Force is an energy derivative. Isolated Gaussian gravity uses U=-M²/(4sqrt(pi)) integral_0^infinity dt/sqrt(product(t+ai²)); for equal widths this gives -M²/(2sqrt(pi)R).
- The removed constant h mode is restored exactly in fixed-χ isolated-energy calculations by2pi M²/box³. Periodic gravitational energies are not mixed across box sizes as if absolute isolated energies.
- Phase probes instead retain the positive source and its constant mode directly; finite boxes still contaminate the phase tail. The reported25.3% excess change is a failed boundary test, not an uncertainty hidden in a successful optimizer.
- Gaussian profile extrema are a variational restriction, not true minimum energies over all admissible fields and matter profiles. Restricted fission costs do not rule out more tightly bound differently shaped fragments.
- Fixed affine mass and spin are input constraints. Their conservation is not evidence of a mass attractor. No fragment count is possible in this ansatz.
- Grid40/48 rebound still occurs at only a few cells per narrow axis. Passing the stated bulk-axis repeat is not pointwise density convergence, proof of 3D stability, or a full continuum simulation.
- The matched force scaling defect has a dedicated compact-source grid repeat. The sole weak-source residual failure is retained.
- The global target remains open despite completed runs. False interpretation gates include unperformed tests, explicitly distinguished from falsified physics.

Provenance and failures:
- static_run failed during JSON serialization of NumPy bool after computation. Its stdout and manifest are preserved. run_v2.py changes only serialization; it does not discard the failing residual gate.
- static_v2_run completed; one residual gate remains false (1.25e-5 versus1e-5). Other finite checks and the stronger-source repeat are separate evidence.
- Initial affine runs stop at their resolution boundary, as recorded. The later heavy continuation resolves a bulk rebound in the restricted model; it does not supersede lower-mass missing endpoints.
- All actual runs have bounded manifests with input hashes, observed revisions and dirty-state information. The repo is shared, so observed revisions may differ from the starting checkpoint without changing pinned inputs.
- No independent reviewer or subagent was used. This is proof/computation self-review. No .mathbox ledger is present.

Proofreading self-review covers new DERIVATION.md, RESULT.md, AUDIT.md and HANDOFF.md. Definitions, signs, units, Gaussian-width versus core-radius distinction, source-conditioned force norm and claim limitations checked. No inherited mathematical text was edited. Plot is descriptive, not separate computational evidence.

Final verification:32 ordinary check records,31pass and1failed residual gate. Interpretation gates2pass,3false (phase-boundary precision failed; mass distribution and joint fits not established). Nine manifests validate against current input/output hashes:8completed,1preserved serialization failure. Rebound widths repeat within0.000186ell0 in time step and0.00264ell0 in grid; four restricted radius curvatures are positive. No active jobs remain.
