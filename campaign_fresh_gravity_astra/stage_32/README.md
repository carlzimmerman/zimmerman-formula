# Checkpoint: actual pressure-inclusive momentum has a conditional lifespan bound

2026-10-06. Parent: [stage thirty-one](../stage_31/README.md).
FGF045 evolves both fluid equations in the fixed Q potential. For the same
concentrated initial velocity, no positive C1 solution covers the regular local
cone through a conservative time O(N^-4). Weighted characteristic gradients
control density and compression while retaining pressure and force derivatives.
The chosen characteristic travels O(N^-3), remaining away from crossing/walls.

This is an a priori lifespan bound, not a constructed solution or actual shock.
Root's original endpoint-classification overclaim and G notation collision were
caught by independent audit; original and correction preserved. Author already
had the narrower scope. Conditional energy accounting passes; gravity still has
its changed-density source residual. No physical theory closure.

- [Root original](fluid_momentum/ROOT_DERIVATION.md)
- [Required correction](fluid_momentum/CORRECTION.md)
- [Root-only audit](fluid_momentum/INDEPENDENT_AUDIT.md)
- [Author audit](independent_audit/INDEPENDENT_AUDIT.md)
- [Scoped review](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-045_RECONCILIATION.md)
- [Coordinator receipt](COORDINATOR_VERIFICATION.json)
- [Unlaunched existence/continuation task](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-046.md)

Proof-only, zero mathematical computations. All three roles completed. Both
normalizations and distinct scale/law branches remain; conserved physical scale
sector, metric/photon/DOF and instrument-calibrated constraints still open.
