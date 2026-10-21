# Harmonic compression normalization with backreaction

Base checkpoint: `f659e6d8e1ee4cf2b756f091aff56b018da1fb1e`.
New bounded route, fixed before execution. Scope is the conditional thermal
compression construction, not a proof about every scalar phase or an
acceleration dipole construction. Existing source/occupation failures stand.

Claim to audit: the fixed-host rational compression response can approach
`4 pi G chi/V = 1` while retaining negligible scalar self-gravity, when the
reference volume is the physical uniform core volume and the acceleration
coordinate is `E = delta(kappa) R_c` (`L=R_c`).

Exact test: independent Maxwell-Boltzmann particles conditioned to `r<R_c`
in a uniform core, with `x=m kappa R_c^2/(2T)`. Obtain their actual second
and fourth moments and `chi=beta Var(Q)`, including the boundary. Solve
algebraically for the scalar/core mass ratio at normalized susceptibility
one, then compare the central gravitational curvatures. Scalar gravity is
omitted only in the distribution under test, never in that diagnostic.

New continuation: solve the spherical self-consistent isothermal mean-field
equation with retained positive original contact, the same harmonic source,
and reflecting/conditioned radius. At `x=10`, preserve the mass selected by
the tracer normalization and compare contact parameters `eta=0.1,1,10`,
source values `s=1,1.1,2,5,10` and local derivative controls. These declared
states add no force; `eta`, temperature, loading, wall and thermal receiver
are hypotheses. Compute stationary profiles, not certified stable states.

Success: an exact implication or counterexample under the stated conventions,
plus mesh-converged stationary checks that discriminate normalization/shape.
Failure/inconclusive: failed residual, no root, or cap; retain that output.
No coefficient fit, no astrophysical exclusion, no microscopic abundance or
kappa selection, no theory closure, no new external theorem claim.

Resources: stdlib Python, one process, one core, 1 GB address-space cap,
45 CPU seconds and 60 wall seconds per recorded run. No existing outputs,
canonical statements, frozen criteria or shared status are edited.
