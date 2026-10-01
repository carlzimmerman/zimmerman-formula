# Autoresearch checkpoint: robustness and observation identifiability

2026-09-27. The physical objective remains open. This pass reconciled the
completed independent audits, executed new bounded tests, and audited a new
derivation from the cluster density-shape gap.

| Result | What changed | Exact limitation |
|---|---|---|
| FGF-015 | 120 low eigenvalues across 12 inhomogeneous slab cases are positive; finest-grid change <=0.30%. Original-form and square-form operators agree. | Fixed impermeable/Dirichlet walls, unfiltered Q/R scalar model. No physical boundary selection or main filtered-MONO stability claim. |
| FGF-018 | All 189 gas-interval slope bounds and 252 original plus 2268 midpoint force/sign checks survive the declared knot-error boxes. | Error-box/interpolation and hydrostatic-force interpretation, not a confidence level or universal exclusion. |
| DM1 / FGF-020 | Exact conditions characterize positive density profiles with fixed integrated mass and idealized emission measure but a prescribed shell density. | Not real detector-count conservation, a resolved profile or global hydrostatic repair. |

## New derivation from the observation gap

Let normalized density have mean mu and variance V>0. A shell with volume
fraction epsilon and constant density L can coexist with the two prescribed
moments in a positive measurable profile if and only if

    epsilon <= V/[V+(L-mu)²],  epsilon L < mu,

with 0<epsilon<1 and L>0. The independent audit supplies the complete
positive construction and equality cases. The original [DM1 derivation](density_moments/DERIVATION.md)
proves a sufficient three-region construction; seven exact rational witnesses,
eight synthetic Q/R gravity conversions and three negative controls passed in
[the bounded run](density_moments/run_001/manifest.json).

Without an independently justified minimum physical feature volume, the two
moments allow arbitrarily large finite shell density. A minimum volume does
give a bound. Instrument resolution alone does not impose that physical
minimum. Density changes at fixed pressure also change temperature and hence
potentially emissivity; the actual observation response must be supplied.

## Reviewed evidence

* [Slab reconciliation](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-015_RECONCILIATION.md)
* [Profile-error robustness](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-018_RECONCILIATION.md)
* [Independent moment audit and precise acceptance scope](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-020_RECONCILIATION.md)

All accepted computation records validate against their actual current input
and output hashes. Failed attempts in earlier checkpoints remain preserved.
No new failure was suppressed. Scientific parentage comes from the pinned
stage-three/stage-four evidence; actual checkout HEAD changed concurrently
and is recorded separately by each run. No commit was made by this pass.

## Next decision

Prioritize FGF-019: determine which local pressure-gradient information the
cached SZ projection, beam and mask can identify when outer-profile modes are
allowed. Retain missing covariance and shared Planck provenance explicitly.
FGF-017 addresses common aperture/distance conventions; those observations
must constrain a candidate before more profile fitting can count as closure.
On dynamics, physical boundaries or the operative filtered-MONO quadratic
action are new questions; more fixed-wall sign grids are redundant.

The main AS001–AS2000 catalog now links the FGF namespace and records compatible
ownership/review rules. It installs no DeepSeek execution service. Actual work
in this pass used the coordinator and named Astra agents. Follow
[the shared index](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/INDEX.md)
for current claims and reviews; task count is not an evidence score.
