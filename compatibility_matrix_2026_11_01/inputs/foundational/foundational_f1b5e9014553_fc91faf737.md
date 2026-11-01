# X48 entropy transport: current state

Current checkpoint **X48-FLOOR-2026-11-01-B**:
[uniform-floor research state](floor_theorem/STATUS.md). The original goal
remains open at mesh-uniform startup seeding. The completed finite transport
phase below is **X48-TRANSPORT-2026-11-01-B**. Its base is
X48-TRANSPORT-2026-11-01-A, initial assessment revision
`c4b97598e8b6b408dd75d724ea469a81a2bd4ea9`. Artifacts remain uncommitted;
individual manifests identify their execution revisions and hashes.

**Computationally verified in the declared finite range:** one fixed-parameter,
energy-conserving entropy-gated heat law settles the virgin spherical collapse
at N=32,64,128,256 through t=32. Late central-5% minima approach
0.349624Kstar without an inserted floor. Positive all-material K is observed
after t=8. Radial size and energy-neutral entropy perturbations relax through
t=64 at N64. Quiet material remains exactly inactive under its stated gate.

**Proved for the semidiscrete law with valid geometry:** shared heat fluxes
conserve energy; physical entropy production is nonnegative; fixed-geometry
transport is cooperative; the global minimum K cannot decrease. This last
statement preserves a seeded floor and does not prove seeding from zero.
The new [preservation theorem](floor_theorem/preservation_route.md) is stronger:
a seed on a wider central mass prefix protects a smaller core uniformly in
resolution for all later times, without a permanent outer guard. Tail floors
and exact energy also prove global continuation for each fixed finite mesh.
These statements passed independent proof audit. Actual uniform seeding is
still a hypothesis, not a numerical conclusion.

**Conditional:** a stationary regular connected remnant retaining K'<=0 must
be isentropic. The independent mass/energy solve predicts
K=0.3496240637094284, rho_c=2.455533676765764 and R=0.5379206218348132.
Global branch uniqueness and convergence to it are not proved.

**Open:** a positive dynamical floor uniform in arbitrary resolution and
infinite time, uniform continuum geometry/PDE convergence, nonradial stability,
cosmological forest viability, and evolved baryonic-disc resistance.
Other admissible ordered cusp data refute a universal floor claim for this
law. Previous static baryon tests remain separate evidence.

Current interpretation: [README.md](README.md). Current numerical synthesis:
[analysis_v2/summary.json](analysis_v2/summary.json). Analysis v1 is retained
historically; v2 separates accepted-state energy bounds from dense-output
sample maxima. [NUMERICS.md](NUMERICS.md) records resource-limited attempts and
completed continuation lineage. [ISENTROPIC_LIMIT.md](ISENTROPIC_LIMIT.md)
states the conditional endpoint argument. [REVIEWS.md](REVIEWS.md) records
independent review; [PROVENANCE.md](PROVENANCE.md) indexes the bounded records.

The next load-bearing proof is mesh-uniform startup compression/heating on a
fixed wider central prefix. Preservation and fixed-N continuation are now
proved; a localized nonlinear startup estimate remains open. Six new
N32..1024 short runs support the sufficient compression hypothesis at 81
sample times each but do not prove it. Additional finite grids alone cannot
close that implication. For physical viability,
the next distinct experiment is an actual forest density/compression history
test against rho_q and tau, followed by responsive baryonic loading.
Neither frozen production engines nor acceptance grades have changed.
