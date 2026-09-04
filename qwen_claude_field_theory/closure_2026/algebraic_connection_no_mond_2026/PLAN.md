# Algebraic connection falsifier and surviving-route calculation plan

Goal: advance FRIED_CHICKEN_SPEC.md without changing its mu_exp kernel or certifying a different theory.
The user explicitly requested autonomous live-repository calculations and commit/push.

Architecture: test EH plus an unrestricted torsion-free connection with arbitrary local,
differentiable algebraic distortion potential. Separate a general variational proof from
finite exact component checks. Then identify what a metric-derived elliptic projector must
still calculate. No full PPN or gravitational Dirac certificate is inferred from an auxiliary block.

## Execution

- [x] Inspect HEAD, dirt, canonical spec, existing vector Palatini work.
- [x] Independent metric worker: derive curvature from separate Phi/Psi; integrate Einstein
  exterior; implicitly differentiate mu_exp; test curved FLRW and exact Schwarzschild-de Sitter.
- [x] Root: write failing tests, then construct all torsion-free components in dimensions 1–4;
  compute the quadratic Palatini distortion form, Hessian, all GL frame identities,
  and the actual canonical auxiliary Poisson matrix. Test an exponential potential's null branch.
- [x] Independent spectral worker: preserve exact Lorentzian projector degeneracy and local
  curvature-source counterexamples with executable tests and scoped interpretations.
- [x] Root: write the general on-shell covariance proof, hypotheses/exceptions, Ward identity,
  and a dependency-ordered list of remaining full-theory calculations. Check primary sources.
- [x] Adversarial mathematical/code review; run every new script and relevant existing gates.
- [ ] Record commands, statuses, hashes, and non-claims; commit/push only this scoped folder.

## Binding boundaries

Signature (-+++), c=1 in action/curvature calculations, mu_exp(y)=1-exp(-y), y=g/a0.
F contains only g and C=Gamma-LC(g), no derivatives of C, no differentiated extra fields,
no matter coupling and no flatness restriction on Gamma. Parameters are constants.
Rank/determinant/PPN/DOF values are computed, not inserted into result generators.
The frozen regular auxiliary canonical block is not the full gravitational constraint algebra.
An irregular exponential branch is not certified healthy by a zero linearized Hessian.
Novelty is at most project-level until a broader literature audit establishes more.

## Files and ownership

Root: connection_checks.py, test_connection_checks.py, REPORT.md, computation_manifest.json,
and captured outputs. Metric worker: metric_branch_checks.py, test_metric_branch_checks.py.
Spectral worker: spectral_escape_checks.py, test_spectral_escape_checks.py.
Unrelated existing dirt is excluded from edits and staging.

## Computational contract

Exact SymPy arithmetic; symbolic general inverse metric and torsion-free C; no random sampling.
This no-randomness statement applies to the new computations. Two legacy regression gates
use fixed seeded rational metric samples; the aggregate manifest records those seeds.
Dimensions 1–4 are finite checks, while the arbitrary-potential theorem is proved in REPORT.md.
Run: python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/algebraic_connection_no_mond_2026 -v
and each sibling executable directly. Deliberate wrong contraction and omitted metric variation
must fail the corresponding independent vector and covariance tests.

## Review record

The mathematical reviewer found the scoped variational theorem proved as written.
The Poisson cross-block sign test and explicit p>0 source-jet domain were strengthened.
Integration review identified seeded randomness and the imported hunt_lib.py in legacy
regressions; both are now recorded, and executable-input hashes are checked before/after runs.
The final aggregate run is the post-review authoritative run. The previously untracked
local intrinsic-DW script was also rerun successfully, but is excluded from the published
runner so a fresh checkout does not depend on unrelated uncommitted inputs.
No full theory is certified.
