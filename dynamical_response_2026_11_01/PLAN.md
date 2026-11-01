# DR01 implementation plan

**Goal:** Execute and publish the bounded kinetic response in CONTRACT.md.
**Architecture:** Immutable FR01 reconstruction; independent orbit library;
variational density/scalar/current interaction; causal spectral pulse solve.
**Stack:** Existing Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4.

- [x] Freeze inputs and analytical contract; independent derivation of signs,
  weights, current feedback, exterior conditions and work/torque normalization.
- [x] Implement background adapter, radial basis and shell spectral assembly.
  Check harmonic orbit and analytic shell/spatial Gram identities before
  interpreting FR01 output.
- [x] Execute baseline and compact endpoint at the frozen resolution ladder
  under the computation-audit bounded runner. Retain each result and failure.
- [x] Independently verify pulse response/energy and numerical convergence.
  Mark unresolved errors explicitly; no fitted damping or response multiplier.
- [x] Write reviewed results, reproduction instructions and handoff. Validate
  manifests. Prepare publication of only this directory using an isolated Git
  index on a dedicated codex/ branch based on the published FR01 commit.

Scientific computation and review are complete. Remote publication follows
content freezing; its verified commit is reported in the completion message.
The compact longer-pulse and late-time diagnostics remain explicitly
inconclusive; those are results of the bounded scope, not completed physical
claims. Primary short-pulse work meets the frozen one-percent target.

Review focus: canonical-current feedback; shell measure and orbit-zero modes;
finite scalar-limit scope; work versus retained heat; finite stability versus
continuum stability. The user already selected this calculation and authorized
execution and push. Directory/index isolation preserves concurrent shared work.
