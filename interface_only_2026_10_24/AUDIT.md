# IO self-audit

Primary verdict: computationally verified only in the stated range.
Claim reviewed: the explicit interface-only energies have zero added force
in occupied pure phases, but the recorded finite states do not establish
stable local confinement with a free exterior and preserved interior law.
Original goal remains open. No independent review was performed.

Dependencies: explicit energy -> phase variation -> mass variation -> radial
force and baryon reciprocal variations -> finite minima -> Hessian check ->
perturbed/continued evolution -> measured gate outcomes. The energy choices,
kinematic inputs and boundary support are assumptions, not results. The
computations and derivations do not depend on an external theorem or paper.

Passed within declared scope:

- Auxiliary compliance tensor is positive; alignment energy is a square.
- All added interactions vanish in pure phases, with no direct bulk gap.
- Phase gradients, Hessians and independent T-mass variations agree with
  finite differences at the documented test points.
- The purported aligned stable fronts have genuine energy-lowering modes:
  explicit second differences confirm the Hessian sign.
- The intact pure interior matches the parent force-control discretization;
  an exterior phase interface changes its potential only by a constant in
  the adopted spherical functional.
- Continued phase evolution integrates its own positive heat receiver and
  checks E+Q independently. Free mass remains in the gravitational source.
- Optimizer success flags are not treated as stationarity. Iteration caps,
  line-search failures and sizable gradient residuals are recorded.

Failed target gates: every IO-1 front loses T; IO-2/3 provide no verified
stationary stable joint pass; IO-4 negative modes invalidate the apparently
successful endpoints; IO-5 demonstrates inward drift and eventual force
contamination; IO-6 all-T states fail the free exterior, while unresolved
local states cannot count as successes; IO-7 resolves its local candidate by
decay of the phase contrast.

Limits and corrections important for interpretation:

- The n512 IO-5 run starts from the n256 endpoint and evolves further. Its
  different radius is not presented as a same-time resolution comparison.
- A positive instantaneous Hessian during drift is not a stationary state.
- An infinitesimal T chemical potential in cells with no T is not reported
  as an observed matter acceleration. Raw diagnostic values there can be
  ill-conditioned and are excluded from physical conclusions.
- Principal-box constrained minima are tested by unrestricted angle flow;
  h(x) remains a nonnegative fraction even when x leaves[0,1].
- The thin spherical unit-jump curvature estimate does not constrain the
  freely varying jump amplitude. Treating it as a proof of stable confinement
  would be an invalid inference, directly exposed by IO-7.
- Curvature is tested as an explicit regularized radial functional. Its
  3D normal-field regularization and shape stability are not established.
- Reciprocal baryon functional derivatives are derived, but fixed baryon
  moments are not a live Hamiltonian completion or a closed dispersion law.

Remaining obligations: independently justified interaction coefficients,
joint moving-mass/phase/baryon equilibrium and stability, finite-work
formation, noise, nonspherical geometry and observational tests. No universal
exclusion of interface-local physics follows from this finite portfolio.
