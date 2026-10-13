# Compact handoff: Hamiltonian drift and sharp-edge selector

Publication parent: `33ec3085256a0a8993752fd0347c83bd96332236`, branch
`codex/cold-energy-equations`. Shared working main can advance independently;
the actual run bases and all execution-input hashes are pinned in the manifests.
No shared index or checkout is used for publication.

## Assumptions additional to the cold-carrier framework

Externally imposed Stratonovich white Hamiltonian noise of strength k>0;
regular one-dimensional integrable orbital motion; smooth periodic coupling;
weak-noise angle averaging; fixed cutoff ER and fixed L; finite positive orbital
period. Stationary zero-current target for the selector conclusion. Nonzero
limiting diffusion for divergent-power conclusion. Connected single well and
smooth position-only noise for the nested-orbit zero argument. Constant D,T and
finite reflecting interval only for the closed regularized power formula.
These are NOT consequences yet derived from the cold-carrier Lagrangian.
No Lambda-CDM or standard MOND premise enters these calculations.

## Exact new implication

The specified noise implies A_H=D'+D*(log T)' and J_H=-D*T*f'.
The target f proportional to q^(-1/2) requires extra drift b=-D/(2q), hence
positive extra energy gain D/(2q). Its integrated bulk input diverges if D*T
has a positive finite limit. For D proportional to q^beta and finite T, the
input is locally finite only for beta>1/2. Position-only white forcing cannot
create an isolated diffusion zero at a regular cutoff while stirring nested
interior orbits. Regularized constant-D,T target has mean input
P=D/[2*sqrt(epsilon*(Q+epsilon))]. See REPORT.md for derivations and caveats.

## Formal correspondence and evidence

HamiltonianDrift.lean: six exact-real algebra theorems. They check the transformed
drift, density-of-states current, cancellation and necessity of extra drift,
regularized normalization identity, and momentum anti-damping factor.
They do NOT certify stochastic calculus, averaging, integral divergence,
nested-orbit positivity argument, physical applicability, or global stability.
Axiom reports allow only propext, Classical.choice, Quot.sound. Three damaged
certificates (transformation sign, selector sign, power factor) are rejected.

Numerical checks: 46 passed. Quartic-well lambda={0,.1,1,10}, E={.01,.1,1,10};
relative central-difference step 1e-4; harmonic closed benchmarks; regularized
power epsilon={1,.1,.01,1e-4,1e-6}; missing-drift residual. Tolerances and exact
argv are in contract.json and run/manifest.json. This is numerical/analytic
model evidence, not empirical evidence. Self-review only.

## Remaining closure gates

Derive the actual bath and its reciprocal reservoir coupling from the framework;
resolve boundary work and finite energy supply; derive noise spectrum and
correlation time; demonstrate selector or finite-width alternative without
encoding the target by hand; test metric/lensing coupling and observed profiles.
No completion or new-physics discovery is asserted.

## Run bases and hashes

- run: execution base `8cef73ea7d01e20f1d08f435ad621b739f8eb3cc`, dirty shared workspace; manifest SHA256 `f4f93b67229533b9c4e192f7a7fa31b803fc1dc49bb9a1d0662717d190bf0338`.
- lean_run: execution base `8cef73ea7d01e20f1d08f435ad621b739f8eb3cc`, dirty shared workspace; manifest SHA256 `2821227705a38dbd7c2900d35092216de5eabfd16007b9ccb1a26d7e5f68c090`.
- HamiltonianDrift.lean: SHA256 `9c6bb112448d23791c84fcb7ad466a45288739103410de4a2cf63801e7a09bf3`.
- check.py: SHA256 `ebba10f392d5935aeae482bfc91ba2358dd0e45bd145f4ab620acf744991746f`.
- verify_lean.py: SHA256 `5dee506f72d4d9e622e6cc4ea0ea50a2fc1ba86e13fbeb0dde9ff3e5e4351798`.
