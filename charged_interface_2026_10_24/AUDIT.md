# Self-audit and interpretation

## Computation

The operative parameter coverage is each script's explicit iterator and
`mathematics.bounds`, not the inherited generic `inputs` label. CI-1 uses
small and large disks; CI-2 onward uses only the large disk. Some early
contracts retain the generic phrase “four parent numeric profiles” and
“beta20” under conventions. Those describe inherited definitions, not the
executed population: beta is explicitly varied in the bounds and code.
They do not support a four-profile or original-beta success claim. Historical
contracts and hashed evidence have not been retroactively edited.

Phase gradients, Hessian products and independent T mass variations are
checked against centered energy differences. CI-6 adds independent F mass
variation. All checked discrepancies are below 4e-9. Hessian includes both
mixed capacity terms and the rank-one fixed-Q contribution. Response charge
uses actual enclosed T mass and includes its density derivative in both
species' forces. Independent surface tension contributes to phase variation
even though it has no fixed-q density derivative.

CI-3 diagnostics are specific to Protected, whose mass potential they
explicitly reconstruct. They must not be reused for ResponseCharge. CI-7
onward instead calls both model species-potential methods; the added charge
mass term is retained. This is why a separate diagnostic implementation was
made rather than silently reusing CI-3.

Optimizer success is not the stationarity criterion. Polished metric speeds,
generalized Hessian eigenvalues and later displacements are reported
separately. Multiple crossings and tiny residual phases are not rounded into
a clean wall. Pressure checks are necessary, not sufficient for a positive
distribution function. CI-8's tiny trace populations are retained; negativity
where population is negligible is not treated as a resolved material defect.
Its original candidate's negative bound is at T fraction .983, well away
from that ambiguity.

## Derivation review

The fixed-charge energy and its first and second variations follow directly
from constrained quadratic minimization; they require a supplied Q. The
simple R^4=k/tau result constrains only one coordinate. The contrast/radius
degeneracy and disconnected-wall charge transport prevent treating it as a
complete stability or formation theorem.

The kinetic stress inequality follows by integrating the radial momentum
equation with nonnegative tangential stress and zero outer radial pressure.
The conclusion is limited to the given density and all forces in the tested
energy; extra external traction or different material stresses are excluded
assumptions, not refuted theories. Positive total virial is weaker than this
local condition. No appeal to an unverified external theorem is required.

## Prose and notation self-review

Applied the mathematical proofreading skill to the new derivation, contracts
and reports. Scope: this directory's new charged-interface writeup only.
Routine corrections: defined the pressure components and distinguished
surface-coordinate stiffness from the generalized phase Hessian.
Mathematical-token corrections: none during proofreading.
Unresolved scientific obligations are explicitly listed rather than repaired
as typography: continuum restoration, live mass equilibrium, charge origin,
local charge transport, distribution-function positivity and formation.

No independent human or agent review was performed. All verification is
self-review plus the orthogonal numerical checks and saved evidence.
