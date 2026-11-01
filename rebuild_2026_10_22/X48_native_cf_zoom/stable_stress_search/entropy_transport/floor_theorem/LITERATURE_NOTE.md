# Bounded source check: no theorem transfer used

Checked 2026-11-01. These sources were inspected to test a possible external
shortcut for the startup/continuum estimate. None is a load-bearing leaf of
the new semidiscrete proofs. This is a hypothesis comparison, not a claim
that no applicable theorem exists anywhere.

Chen, Zhang and Zhu,
[arXiv:2601.06620v3](https://arxiv.org/html/2601.06620v3), revised 2026-10-28:
the inspected introduction, equations (1.1) and the immediately following
constitutive relation, concern barotropic pressure with constant entropy,
density-weighted symmetric-gradient viscosity, and density vanishing at the
moving boundary. The X48 experiment instead has independent evolving K,
pure bulk stresses with an activation threshold, heat redistribution,
self-gravity, and a positive-density initial edge. These differences are
already enough to prevent direct application. No assertion is made that its
methods cannot be adapted, and no later theorem was used to fill the gap.

Chen and Zhang,
[arXiv:math/0701150v7](https://arxiv.org/abs/math/0701150v7), revised 2008-04-16:
the inspected abstract concerns isentropic flow between a solid core and a
vacuum free boundary, with power-law density viscosities. It does not itself
supply the needed central, nonbarotropic, mesh-uniform startup statement.
No theorem-level transfer from this paper was attempted after that mismatch.

The remaining estimate is explicitly stated as (UC) in
[seed_route.md](seed_route.md), or as the sufficient nonlinear semigroup
bound (NE) in [startup_energy_route.md](startup_energy_route.md). It is not
silently attributed to either source. The directly derived finite-graph
barrier is separate from a continuum heat-kernel theorem.
