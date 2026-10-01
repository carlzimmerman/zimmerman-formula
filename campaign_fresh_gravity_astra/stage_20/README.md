# Checkpoint: constrained equilibria have a genuine local response branch

2026-09-30, 14:30 UTC pass. Parent: [stage nineteen](../stage_19/README.md).
FGF034 addresses the gap between the earlier left-IVP family and the response
needed by the full autonomous-driver stability test. Mass, both phi/chi wall
values, physical interval and coefficients are now held fixed.

At one smooth positive-density, positive-gradient diagnostic Q equilibrium,
assume the reviewed full fixed-reference form Q0 is continuous and coercive
on the original H1_0 fluid/field perturbations. Hydrostatic balance and fixed
mass determine the density exactly:

    rho[phi]=M exp(-phi/cs²)/integral exp(-phi/cs²).

Its derivative includes a weighted mean that keeps total mass fixed. Eliminating
this density in the static equations gives a nonlinear map from H2 Dirichlet
field pairs to L2 residual pairs. Exact minimization over mass-preserving
fluid variations yields a coercive reduced form. Its weak inverse upgrades
to an H2 inverse through the two field equations. A local contraction then
constructs a unique nearby C1 branch, with positive gradient and the SAME
mass and wall values. This is more than a formal derivative of an assumed branch.

Let R(lambda)=integral T/C along this branch. With ell and z defined by the
full quadratic form, a0(z,v)=ell[v], the actual branch tangent is u_lambda=-z.
Consequently

    R'=integral T_chi/C+beta, beta=Q0[z]>=0.

The matter response is retained. The explicit-reference derivative alone is
not R'; the sign of R' is not fixed by beta>=0. At an actual intersection
V'=R for a separately specified potential, the autonomous margin is
Delta=V''-R'. No physical potential or such intersection has been supplied.

The old IVP derivative generally changes total mass and right-wall values.
It lies outside this homogeneous perturbation domain. Its static energy
variation includes chemical-potential times mass change plus explicit wall
work; those terms explain why it cannot simply replace the constrained tangent.
Fixed mass requires the difference of endpoint MOND fluxes to be constant;
it does not impose separately fixed flux at both endpoints.

## Checked scope and limits

Author's proof and a separately frozen independent derivation agree. Another
agent audits root's proof alone. Root discloses that an author route preview
arrived after its reasoning but before its file freeze, so root is not counted
as fully isolated. This is proof-only evidence: no numerical experiment,
computation manifest, branch radius or stability eigenvalue was fabricated.

The conclusion is local around a qualifying seed. It does not connect the two
normalizations by one common constrained branch, quantify how far lambda can
change, cross a zero-gradient point, or prove global/nonlinear stability.
The existing short-slab seeds give examples satisfying the seed gate, each
with its own induced mass and wall data; those seeds are not silently joined.

Both a0 normalizations and distinct constant-vacuum, frozen-H and evolving-H
hypotheses remain separate. Static balance uses the Q MOND flux b, not a
Newtonian source replacement; evolving balance retains its time term. Q does
not supply an RAR/M action or operative filtered-MONO/metric completion.
No local covariant scale sector, physical V, two-gravitational-DOF construction,
empirical pressure calibration or theory closure follows.

- [Root proof](constrained_response/ROOT_DERIVATION.md)
- [Root-only audit](constrained_response/INDEPENDENT_AUDIT.md)
- [Independent author audit](independent_audit/INDEPENDENT_AUDIT.md)
- [Scoped reconciliation](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-034_RECONCILIATION.md)
- [Coordinator receipt](COORDINATOR_VERIFICATION.json)

The formal fixed-wall susceptibility obligation is now closed in this scope.
Do not invent or fit V, or repeat formal response calculations, to claim a
physical autonomous completion. The existing FGF007 task is the next candidate:
quantify the loss of the nonzero-background Hessian approximation approaching
zero field, keeping Q and RAR distinct. It must be deduplicated before launch;
it cannot itself extend this nonlinear branch through degeneracy. Reuse that
recorded task rather than create a duplicate zero-field child. FGF031's finite
pressure robustness route remains stopped pending actual calibration evidence.
AS228 metric repair stays with its primary owner.
