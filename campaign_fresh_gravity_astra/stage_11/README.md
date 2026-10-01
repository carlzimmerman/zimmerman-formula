# Checkpoint: the full slab remains stable at its first scale turn

2026-09-30, 05:24 UTC heartbeat pass. Parent: [stage ten](../stage_10/README.md).
This is another bounded analytic step in the diagnostic Q/R wall model.
The physical objective remains open; no spectrum, numerical continuation,
observed length or empirical calibration was computed in this pass.

## Exact new implication

Assume a smooth finite continuation with B,rho,g>0 has chi'=w>0 before its
first zero at the right endpoint D*. The background identity
Jw''=Mw-C R, with R=rho q/lambda>0, implies that zero is simple: w'(D*)<0.
A double zero would have w''(D*)<0 and make w negative just before D*,
contradicting the assumed first zero.

The weighted expression divides by w, but its singularity does not change
the physical domain. For eta in H1_0, with h=D*-x,

    |eta(x)|²/h <= integral_x^D* |eta'|² ->0,
    integral eta²/h² <=4 integral eta'².

These estimates make the weighted terms integrable and kill the extra
boundary contribution. The quotient eta/w need not have a finite trace or
belong to H1_0; imposing that would wrongly exclude admissible perturbations.
The four-square identity therefore extends to the full original domain and
proves strict positive energy at D*.

Strict positivity alone would not establish a spectral gap. The original
regular form has positive principal gradient coefficients and satisfies
Q>=A_G||u'||²-B_G||u||². Compactness on the finite interval then excludes a
unit-norm sequence with Q tending to zero. This supplies a fixed-background
positive gap and H1 coercivity, without a claimed numerical value.

Rescaling each full interval [0,D] to [0,1] makes the original nonsingular
forms continuous in D. The attained gap thus persists for some positive
extension beyond D*. This is the SAME continued full prefix, including its
original left boundary and all its mass, not a new tiny patch around the
turn. Right-wall fields, pressure and total equilibrium mass change with D
as induced by the same IVP; mass is fixed under perturbations at each D.
No moving-wall evolution or globally fixed-mass family is asserted.

The root also supplied an analytic nonemptiness construction: at fixed
B_i,rho_i>0 and chi_i=0, sufficiently small positive w_i has w'(0)=-T_i/J<0
and reaches a regular first zero within a uniform local existence neighborhood.
This has no computed domain length or example outside the old shortness bound.

## Verification and remaining limits

Root and FGF-026 author derived the endpoint argument independently. A
separate agent audited root's proof, including traces, compactness, continuation
and the local first-turn existence argument. Product norms use fixed reference
units or dimension-balancing weights, and the kinetic norm restores frequency
units. Gap and extension bounds are existential and background-dependent.

- [Root derivation](endpoint_audit/ROOT_DERIVATION.md).
- [Norm and family conventions](endpoint_audit/QUALIFICATIONS.md).
- [Independent proof audit](endpoint_audit/INDEPENDENT_AUDIT.md).
- [FGF-026 reconciliation](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-026_RECONCILIATION.md).
- [Coordinator receipt](COORDINATOR_VERIFICATION.json).

This settles the conditional first-turn stability question, not arbitrarily
far continuation beyond it. No extra field-flux condition is imposed, and
the positive Dirichlet rank-one term is retained under static elimination.
Mass/source balance uses Q/R MOND flux with both a0 normalizations and distinct
constant-vacuum versus frozen H reference families. No M action is invented.
The variable effective local scale still fails a literal pointwise constant-
vacuum interpretation; filtered-MONO, metric/photon, free-wall, nonlinear/3D
and observational closure remain open. Primary AS228 repair retains its owner.

Next prioritize the already-ready FGF-024 pressure information task rather
than repeating this now-settled endpoint proof. A quantitative gap or extension
for a declared full background would be a separate computation with error
controls, not an implicit consequence of an unquantified existence argument.

Live handoff: 27 scoped tasks; 14 reviewed and 13 ready, none running. FGF024 is next priority. FGF027 specifies quantitative gap/extension bounds and is unlaunched. All source, task and available review pins matched in queue_integrity_009.json. Checked scope/ownership sent to the authorized peer.
