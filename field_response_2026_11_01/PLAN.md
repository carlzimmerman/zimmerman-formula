# Field response implementation plan

**Goal:** Test radial stability and fixed-mass baryon response of the existing
PN28 finite-gradient halo, then publish a reviewed reproducible result.

**Architecture:** Immutable local input snapshots feed two independent small
calculations: a radial variational screen and a nonlinear static boundary-value
continuation. Independent review checks the variational completion, vacuum
scope, conservation identities and interpretation.

**Tech stack:** Existing Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4; mathbox v2
bounded runner. **Spec:** CONTRACT.md and CONTRACT_STATIC.md.

## Constraints and review focus

- Scope and non-claims follow CONTRACT.md. Do not modify earlier lanes.
- Fix dark mass when baryons change; central potential becomes an output.
- Keep scalar anisotropic stress and reciprocal energy terms.
- Distinguish fluid stability, kinetic stability and numerical convergence.
- Keep all failed attempts and independent source hashes.
- Use an isolated Git index/result branch so the shared checkout and its
  staged changes are not committed by this experiment.

## Tasks

- [x] Snapshot inputs and freeze both contracts before new scientific runs.
- [ ] Derive radial quadratic energy and a positive-inertia linear completion;
  document the vacuum prescription and the fluid-closure assumption.
- [ ] Write local-Hessian, gravity and source controls before the radial code;
  demonstrate missing implementation fails, then implement and run controls.
- [ ] Implement the radial energy screen, refined adverse witnesses, and
  finite-basis linear behavior where useful. No nonlinear-formation claim.
- [ ] Implement fixed-dark-mass static continuation with independent integral
  and stress/virial checks, zero-forcing controls and frozen refinements.
- [ ] Run the two experiments through bounded manifests and inspect every
  scientific result separately from implementation-control success.
- [ ] Independent review; fix any material numerical or interpretation defects,
  retaining previous runs. Write README, exact reproduction and handoff.
- [ ] Verify manifests/source dependencies and publish the result-only branch;
  report verified commit and remote branch with the physical outcome.

Execution ruling: the user approved the proposed experiment and publication;
no additional design-approval pause is required. This research package uses
the established per-experiment plan location rather than software-wide docs.
The static and radial implementations are independent; root coordinates the
latter, a collaborator the former, and a separate reviewer the mathematics.
