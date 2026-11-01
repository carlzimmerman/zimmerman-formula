# X48 entropy redistribution target

Checkpoint X48-TRANSPORT-2026-11-01-A, base Git revision
`c4b97598e8b6b408dd75d724ea469a81a2bd4ea9` in a dirty shared checkout.
The previous phase is `../CHECKPOINT_2026_10_31.md`; its endpoint projection
is not a transport law. The user now explicitly requests derivation and tests
of energy-conserving redistribution, settled cold-collapse cores, quiet forest
material, and a central entropy floor persisting under refinement.

## Contract

Keep the previous material energy `e=K W(rho)`, pressure `P=K rho^2 h`, and
virgin collapse heater. Test a genuinely evolving heat flux and signed bulk
damping, preserving latent energy and the exact dormant phase. New physical
transport scales are allowed by the user's earlier authorization. No entropy
clipping, imposed K floor, accepted-state projection, sorting, energy reset,
or numerical coefficient scaled with shell count is permitted as evidence.

Track separately: exact semidiscrete conservation/entropy production;
actual time-integration errors; finite-time radial settling; late thermal
stability; fixed-resolution entropy positivity; a positive central lower bound
uniform in resolution; and the empirical identification of the quiet domain
with the observed forest. The latter is not implied by a gate definition.

## Routes and first discriminators

- Local Kirchhoff/Fourier conduction plus memory-activated damping. Check
  conservative pair exchange and the full cold collapse at fixed physical
  coefficients. Persistent uniform-temperature equilibration may soften the
  thermal response and must not inherit a frozen-entropy stability theorem.
- Instability-gated transport. If persistent conduction contracts secularly,
  suppress it only in stable entropy stratification using a nonnegative
  conductivity; retest conservation and formation. This changes the physics
  and must be labeled as a separate route.
- Positive nonlocal thermometric exchange. Symmetric physical-scale kernels
  provide a different mixing rate and explicit conditional lower bounds;
  they retain thermal gravitational-stability obligations.

An independently derived obstruction route tests whether finite energy,
entropy increase and positive conductivity imply a uniform floor. They do not
alone: a density/enthalpy bound or equivalent coercivity is additionally needed.
Specific cold initial data can still settle on a locally stable branch.

## Finite tests declared before execution

Use the prior uniform sphere: rho=0.25rho_q, radius=1, velocity=-0.25r,
K=0, normalized G=rho_q=Kstar=1, a0=sqrt(8pi), tau=0.5. Initial transport
parameters: D=0.1, damping strength=1, memory activation chi_d=0.01.
The face gate is h_i*h_j and therefore approximates continuum h^2, not h.
These coefficients remain fixed as N changes.

Start N32 through t=4 with bounded resources, compare D=0 damping-only and
the new D=0.1 route. Expand to longer times and N64/128/256 only when named
uncertainties warrant it. Every run records actual completion or resource
limits, source hashes, tolerances, and restart lineage.

Settling success requires both late kinetic energy below 1e-3 of binding
energy and a late relative density oscillation amplitude below 2%, with no
continuing density/entropy drift concealed by those criteria. Energy error
must be below 1e-6 or demonstrably decrease with tighter time tolerances.
Assess inner 1%, 5%, and 10% fixed-mass entropy/density diagnostics, first-cell
values, temperature variation, residual force, and entropy ordering. Finite
positivity is not labeled a continuum lower-bound proof.

Frozen X48/ZK1 production code and previous snapshots remain unchanged.
