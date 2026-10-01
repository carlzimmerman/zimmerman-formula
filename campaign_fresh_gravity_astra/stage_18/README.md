# Checkpoint: conserved global scale dynamics still require an equilibrium and restoring force

2026-09-30, 12:29 UTC pass. Parent: [stage seventeen](../stage_17/README.md).
FGF033 adds one explicitly diagnostic spatially uniform coordinate lambda to
the inherited Q fluid/field action, with L_driver=I lambda_dot²/2-V(lambda),
I>0 and one fixed autonomous C2 potential. This is a conditional mathematical
extension, not an adopted element of the user's physical framework.

Its equation I lambda_ddot+V'=integral T/C exactly cancels the reference work
found in FGF032. Total energy is conserved with the original fixed field walls
and impermeable matter walls. This supplies global conservation only; it does
not construct local covariant stress or a metric/photon coupling.

A regular static nonzero-field Q slab must also satisfy V'=integral T/C>0.
An identically constant V therefore cannot support such a static equilibrium.
This is a no-equilibrium obstruction, not an unstable-mode calculation around
a nonexistent state. An older fixed-reference slab does not automatically
solve the new global equation. No potential has been fitted to make it do so.

At an actual equilibrium, let Q0 be the original full fixed-reference Hessian
on fixed-mass H1_0 fluid/phi/chi perturbations. Define

    ell[u]=-integral(q psi'+T_chi eta)/C,
    k=V''-integral T_chi/C,
    a0(z,v)=ell[v], beta=Q0[z], Delta=k-beta.

Assuming Q0 is continuous and coercive on the declared fixed-unit domain,

    Q_full[u,s]=Q0[u+s z]+Delta s².

Full coercivity is equivalent to Delta>0. Equality gives one zero direction;
Delta<0 gives negative index one. With the regular compact-domain operator
and positive kinetic assumptions, these give the corresponding longitudinal
spectral signs. Positive finite I changes rates, not this threshold. Matter
response remains inside Q0 inverse; dropping it or a wall compatibility term
would change the test. No numerical frequency or candidate Delta was computed.

The autonomous theta=chi+lambda point transformation retains one extra global
canonical pair. Its momentum is P_lambda=I lambda_dot-integral pi_theta; the
full Hamiltonian equals the same physical total energy. The perturbative theta
traces equal the global perturbation s at both walls. The transformed momentum
equation requires -J[theta_x]/C from these linked endpoint variations. Holding
theta independently fixed would change the problem. Root's explicit boundary
addendum credits the independent auditor's cue; author derived its own version.

Author and root fixed their main derivations independently. A third agent
froze its own derivation before reviewing author; another audited root only.
All accepted statements remain conditional proofs. There were zero numerical
or symbolic computation runs and no fabricated manifests or empirical tests.

- [Root derivation](global_reference/ROOT_DERIVATION.md)
- [Attributed boundary addendum](global_reference/BOUNDARY_ADDENDUM.md)
- [Root proof audit](global_reference/INDEPENDENT_AUDIT.md)
- [Independent author audit](independent_audit/INDEPENDENT_AUDIT.md)
- [Scoped review](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-033_RECONCILIATION.md)
- [Coordinator receipt](COORDINATOR_VERIFICATION.json)

Both a0 normalizations and separate constant-vacuum/frozen-H/evolving-H
hypotheses are preserved. The evolving MOND source includes tau phi_tt;
no Newtonian replacement, source mass or discrepancy estimate was made.
Q results do not automatically apply to RAR, registered M or filtered MONO.
Physical V,I, a simultaneous equilibrium, local stress, vacuum identification,
metric/photon coupling and the required gravitational DOF count remain open.
No physical theory closure or historical novelty claim follows.

Next execute FGF031's single conditional response-error certificate for the
cluster pressure ambiguity. FGF034 separately asks for a fixed-mass, fixed-wall
local equilibrium response branch: the older fixed-left-IVP family changes
its mass/right walls and cannot simply be differentiated for this purpose.
That branch and its proposed susceptibility identity are unproved task targets.
Do not launch a potential/spectral sweep without an independently specified V.
AS228 metric repair remains with its primary owner.
