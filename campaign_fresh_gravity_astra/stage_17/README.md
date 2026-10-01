# Checkpoint: a prescribed reference history requires explicit energy exchange

2026-09-30, 11:28 UTC pass. Parent: [stage sixteen](../stage_16/README.md).
FGF032 derives the exact energy accounting when the previously stationary
reference becomes a prescribed function a_ref(t)=a_c exp(lambda(t)). This is
a proof about the inherited diagnostic Q action, not a constructed cosmology
or a new physical reservoir. No numerical run was needed.

## The physical balance

Let C=4 pi G and T=-a W_a, which is positive for Q at nonzero field.
The fluid internal/kinetic energy, interaction rho phi, scalar field energy
and scale field energy combine into E. Their flux F includes fluid enthalpy,
interaction advection and both field fluxes. The exact identity is

    partial_t E + div F = -lambda_dot T/C.

All internal exchanges cancel. Explicit reference work remains. On a fixed
domain the integral includes both the outward boundary flux and the volume
integral of this work term. Thus a prescribed change in reference scale
cannot be treated as an unforced conserved evolution of this same action.
Under closed physical boundaries, an increasing reference removes energy
from the selected system when T is nonzero. No net-work claim for every
closed protocol is made.

The dynamic MOND source equation is div P=C rho+tau phi_tt. The static
source formula cannot be used in an evolving problem unless that time term
vanishes. No mass discrepancy, force fit or Newtonian source replacement
was calculated in this pass.

## Changing coordinates does not remove the work

The exact transformation theta=chi+lambda retains kinetic velocity
theta_t-lambda_dot and potential U(theta-lambda). With
pi_theta=sigma(theta_t-lambda_dot)/C, the transformed canonical quantities are

    H_theta = E + lambda_dot pi_theta,
    F_theta = F - J lambda_dot grad(theta)/C,
    partial_t H_theta + div F_theta
      = lambda_ddot pi_theta - lambda_dot U'(theta-lambda)/C.

These identities describe the same driven system. Subtracting the momentum
and flux corrections recovers the original physical balance exactly.
Replacing the transformed kinetic and potential terms by autonomous theta
terms changes the action; it is not an equivalent relabeling.

Walls also transform: a fixed chi wall becomes theta=chi_wall+lambda(t).
Its physical energy flux can vanish while the transformed canonical flux
does not. Imposing static walls in both coordinates would change the problem.
At an isolated zero-rate instant the two energies coincide in value, but
their time derivatives can still differ by lambda_ddot pi_theta. A constant
protocol on an interval is a stronger control.

## What was checked

Root and author derived the balances independently before reading each
other's new proof. A separate auditor froze its own derivation first, then
reviewed the author. A fourth agent independently audited root's proof,
including its full off-shell residual identity for arbitrary smooth fields.
All relevant source/result hashes are recorded. This is proof-only evidence:
there are no computation manifests, sampled trajectories or invented tests.

Controls retain the constant-reference limit, constant nonzero reference
shift, nonzero rate with zero acceleration, instantaneous zero rate with
nonzero acceleration, kinetic/potential mutations, and transformed boundary
conditions. Arbitrary manufactured fields are not asserted to solve the
equations; their equation residuals must be included in any balance check.

The exact missing obligation is a physical dynamical sector that exchanges
the opposite energy and derives its reference history, with equations,
energy, boundary data and stability. A formal uniform driver would require
its generalized force to equal integral T/C, but no such physical sector is
constructed or authenticated here. A spatially uniform driver is not
automatically a local covariant field.

- [Root proof and off-shell identity](energy_identity/ROOT_DERIVATION.md)
- [Root independent audit](energy_identity/INDEPENDENT_AUDIT.md)
- [Independent author audit](independent_audit/INDEPENDENT_AUDIT.md)
- [Scoped reconciliation](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-032_RECONCILIATION.md)
- [Coordinator receipt](COORDINATOR_VERIFICATION.json)

Both a0 normalizations remain separate choices; their constant shift changes
the constitutive response but not lambda_dot. Constant-vacuum and prescribed
H histories remain distinct. The earlier H-history obstruction, literal
constant-vacuum interpretation, metric/photon coupling, filtered-MONO action
and observational adequacy remain unresolved. No RAR/M action or stability
conclusion is transferred from this Q calculation.

FGF033 next tests a clearly labelled minimal autonomous global reference
coordinate: conservation alone must not be confused with an equilibrium or
stability proof. Any added inertia/potential and extra global canonical pair
must be counted. FGF031 remains ready for one conditional operator-error
certificate. AS228 repair stays with its primary owner.
