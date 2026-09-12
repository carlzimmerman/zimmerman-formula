# Nonlinear constrained response checkpoint

Base `1be42350b`. Shared main has an unrelated working modification of
`fable_independent_2026/FINDINGS.md`; preserve it. Target remains the unchanged
same-action gravity requirements, not a fitted effective fluid.

The previous bare quartic coefficient is not constraint-reduced. This work
executes the next uncertain implications in parallel:

1. `action/`: restore the full ADM cubic term, expand through quartic order,
   and derive the nonlinear lapse/shift source harmonics before averaging.
2. `clock/`: vary and eliminate the static spatial clock response in a local
   frozen-metric/frozen-coefficient diagnostic; compare bare versus eliminated
   quartic coefficients and exact implicit-branch roots.
3. `review/`: independently audit the full clock source terms and directional
   Hessian of this reduction; distinguish a restricted stationary point from
   an admissible nonlinear Einstein/clock solution.
4. `ClockElimination.lean`: formalize the conditional elimination and transverse
   degeneracy algebra. Do not call these full-action formalization.

All new files are confined to this directory. No old coefficient source,
background or archived evidence may be overwritten. A restricted positive
quartic energy coefficient is not a full stability pass. Immediately test
transverse response, clock invertibility, and omitted full field equations.

Completed: all four bounded routes above, plus the generated second-order
mean/2k initial-constraint response. The bare quartic sign reverses after
clock elimination, but the restricted stationary point has null transverse
stiffness and fails the affine Einstein-response stability gate. The full
nonaffine theory remains OPEN. See REPORT.md for the conditional Hessian
bound and why it must be computed from preserved equations, not assigned.

Next: preserve the nonlinear clock constraint and evolve the scalar/metric
initial data; compute lapse and the nonaffine principal, then reduced S4.
The observational question about DF2 is recorded separately with attribution
and primary sources; it is not used as a premise in the action calculations.
