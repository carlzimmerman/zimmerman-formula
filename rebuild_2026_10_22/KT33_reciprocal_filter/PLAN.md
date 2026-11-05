# Reciprocal filter implementation and fixed-parameter rerun

Date: 2026-11-04. User authorization: implement the corrected filter and rerun
the Milky Way and Cassini checks with existing parameters. This follows the
accepted recommendation in `reviews/repo_audit_2026_11_03/NEXT_STEP.md`.
This is a numerical implementation and controlled comparison, not a blind test.

## Specification

For each controlled source problem hold the normalized Gaussian width fixed:

    Phi[rho] = N rho + S* (Q[S rho] - N S rho).

Here Q uses the existing simple nu, N is the Newton potential, and S* is the
volume-weighted adjoint of S. The continuum isotropic Gaussian is self-adjoint.
Use epsilon=0.5, canonical a0=9.3603e-11 and alternate a0=1.1312e-10 m/s^2.
Preserve KT25's baryon parameter grid, prior selections, width quantization,
external field, data, and observational cuts. Do not fit new parameters.

The prior report already selected this construction. Reusing source-only
scores would not test it; changing to the later variable tidal widths would
test a different theory. Neither is part of this implementation.

## Work and ownership

- [x] `mw/`: implement the volume-aware Gaussian outer operation, reproduce
  original controls, rerun saved passing cells and the existing prior grid as
  resources permit. Check complete radial/vertical cuts and strict scale length.
- [x] `cassini/`: derive the Gaussian-convolved tidal Green kernel, reproduce
  source-only and plain controls, evaluate corrected Q2 on both footings with
  angular/radial/domain refinement.
- [x] Independent review: check the mathematical map, volume weights,
  boundaries, limiting cases, numerical accuracy and reported scope.
- [x] Integration: validate manifests and input hashes, report before/after
  scores and whether the fixed candidate window survives.

## Checks and interpretation

Use independently computable Gaussian and zero-width limits, nu=1, adjoint
pairings, and source-only mutation controls. Separate exact algebraic adjoint
identities from continuum approximation and from errors in inherited QUMOND
discretization. Check boundary/gauge treatment, full-space versus half-space
mass, and spatial refinement against observational margins. A spherical check
alone does not certify reciprocity for nonspherical sources.

Cassini retains g_ext=2.32e-10 m/s^2 and |Q2| ceiling=5.2e-27 s^-2. Milky Way
retains L1, L2a, L2b, L3 and reports Lh separately. No dwarf or SPARC score is
inherited by the corrected model, and no claim of global theory viability is
made from these two checks. Width is fixed per controlled problem; this does
not solve the common system-mass definition.

## Execution and evidence

Python with the repository's installed NumPy/SciPy; no dependency installation.
Each worker records an explicit contract and bounded command before runs, pins
code/data, saves structured outputs and convergence checks, and validates the
computation manifest. Numerical library threads are limited to one. Each code
module is import-safe and originals are read-only.

Ruling: work in this new experiment directory rather than change branches in
the shared dirty checkout. Existing untracked research dependencies and running
jobs remain accessible; no original file is rewritten, committed, or published.
This matches the repository's experiment-lane layout and the authorized scope.
