# Initial data that propagate binding and the remaining radial problem

19 October 2026. Checkpoint ZAR-2026-10-19-07, continuing [the confinement criteria](../uniform_confinement_2026_10_19/README.md). The two-response force model and exact warm equilibrium are unchanged.

**An explicit nonstationary initial-data class now propagates its binding reserve, finite boundary and nonlinear stability exactly.** The class has spherical spatial density but orientation-dependent angular currents. It is a genuine full phase-space solution; its spherical average equals the old equilibrium. It does not close the harder problem of a nonstationary strictly radial distribution f(r,v_r,L).

The checkable initial condition is

\[
f_{i0}(x,u)=F_i(E_i^F,L)+L_z h_{i0}(r,v_r,L),
\qquad |L_z h_{i0}|\le\theta F_i,\quad0<\theta<1,
\]

with smooth compact h_i0 inside the occupied region and L_z D_i^F h_i0 not identically zero for at least one species. Tangential velocity reversal makes every radial moment of the added term vanish. Central transport preserves that structure, so the density and force stay exactly those of F while the full distribution changes with time.

Consequently the initial envelope (1-theta)F <= f <= (1+theta)F, negative particle-energy cap and original orbital support propagate for all time. The exact density law and centered radial dispersion remain unchanged, including the original positive dispersion floor on the law annulus. A direct full-phase-space Lyapunov bound holds within this invariant class. [ORIENTATION_ODD_INVARIANT.md](ORIENTATION_ODD_INVARIANT.md) proves all these assertions and the precise symmetry limitation. No future work budget or damping assumption is imposed.

There is also a new self-consistent strictly radial obstruction. A tiny smooth even free population can be placed outside the original warm core so that **every initial individual particle energy is negative, yet the population's collective Hamiltonian is positive**. An angular-momentum barrier keeps it outside the core, whose density law and dispersion remain exactly unchanged. The virial identity then forces the full outer support to grow without bound, while its mass-plus-kinetic deviation remains O(delta) for all time.

[INITIALLY_BOUND_EXPANDING_SHELL.md](INITIALLY_BOUND_EXPANDING_SHELL.md) gives the smooth construction. It requires a sufficiently broad allowed angular interval, adds free mass/Casimirs and an initially exterior population, and its initial binding gap shrinks with the added mass. It does not refute a sufficiently small canonical neighborhood with a fixed negative gap and unchanged initial support. Unlike the previous prescribed Kepler pump, this example solves the actual coupled kinetic equations.

[RADIAL_PROPAGATION_OBSTRUCTIONS.md](RADIAL_PROPAGATION_OBSTRUCTIONS.md) identifies the remaining strict-radial work estimate. It proves that matching initial density, zero current and radial pressure does not freeze the field, derives an exact linear work cancellation, finds nonzero diagonal resonances in the actual coupling, and excludes a nearby homologous breathing ansatz. These close specific shortcuts, not all routes to confinement.

The original target is therefore partially advanced: the initial-time propagation theorem is proved for the stated nonstationary angular-current sector; the strictly radial, fixed-gap, unchanged-support problem remains open. [AUDIT_AND_HANDOFF.md](AUDIT_AND_HANDOFF.md) and [CHECKPOINT.json](CHECKPOINT.json) record the hypotheses, audits and next implication.

Only this new directory was written. No scientific scripts, numerical integrations, simulations or process inspection/control were used. Claude's calculations and all previous artifacts were left untouched. The results are internal analytic statements in the specified model, without a global novelty or observational claim.
