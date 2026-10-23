# Lapse-preservation continuation: contract before computation

Base repository remains 05a3bfdb73fd9194954dbcdb90602d2c2f979b83. Parent result: RESULT.md R1. Previous turn classified as progress: a new exact counterexample and saved checked calculation changed the next action.

Target: derive {H[N],H[M]} for the A33 action, retaining the full metric dependence of D.P, and obtain the actual lapse-preservation equation. Do not assume eight first-class constraints or a particular final mode count.

Analytic candidate: the bracket is an integral of a vector density V^i times (N partial_i M-M partial_i N). Derive each contribution separately. Independent check: reduce the action to a reflection-symmetric plane-dependent sector h=diag(A,B,C), P=(p,0,0), all fields functions of x; compute canonical functional Euler derivatives of the complete reduced Hamiltonian, including its three-curvature, and compare the resulting V^x to the general formula. This reduced test verifies one invariant sector, not all three-dimensional components.

Criteria: symbolic coefficient identities must vanish; test at nonconstant metric and nonconstant fields. Removing the metric variation of D.P must break the identity; deleting the clock must recover the parent result's vanishing witness. No parameter fit. W may be an arbitrary differentiable local potential because its antisymmetrized ultralocal contribution must cancel.

Continuation discriminator: is a smooth positive lapse automatically guaranteed? Construct explicit periodic constraint-satisfying P=0 data with varying pi_P where preservation requires div(N^2 V)=0. A regular positive-lapse obstruction on those data is a scoped result, not proof that every dynamical branch fails. Conversely a permitted positive lapse is not nonlinear well-posedness.

Scope: self-review, exact formal calculus with periodic boundary conditions, no observational claims, no inherited manuscript edits. Runs small, deterministic and single-threaded. Store scripts, raw logs, outcomes and hashes. No full completion or novelty presumed.

## Scope addition after the first symbolic probe
The general plane-dependent identity and the positive-lapse witness passed the first probe. Add a Christoffel reconstruction of the reduced scalar curvature and a full three-dimensional polarization-gradient derivative as orthogonal checks. Also complete the Dirac algorithm for the existing flat-vacuum scalar quadratic action: four scalar constraints must have nonzero determinant for k>0, and canonical reduction must reproduce the recorded dispersion. This extension is motivated by the first result, not an independent pre-registered empirical test. No success threshold was changed.
