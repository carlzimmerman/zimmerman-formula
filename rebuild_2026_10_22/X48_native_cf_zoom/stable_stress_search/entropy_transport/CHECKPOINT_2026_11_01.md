# Phase synthesis: conserving entropy redistribution

Checkpoint X48-TRANSPORT-2026-11-01-B, descended from A at revision
`c4b97598e8b6b408dd75d724ea469a81a2bd4ea9` in the shared dirty workspace.
This is a bounded phase closeout and handoff; the original physical research
goal remains open. The live entry point is [STATUS.md](STATUS.md).

The initial discriminator rejected persistent thermal conduction as a settling
mechanism: it damps motion but continues cooling and contracting the center.
Damping without transfer retains adverse entropy ordering. These negative
controls remain recorded. An outward heat flux restricted to an adverse
entropy gradient and a hot-to-cold temperature gradient was then declared
with fixed physical diffusivity and gradient length. Shared fluxes conserve
energy; viscosity supplies exactly its own mechanical heat. No coefficient
was scaled with resolution and no entropy floor was inserted.

The selected route has finite success at 32--256 shells and t32, and radial
size/entropy relaxation through t64 at N64. Central entropy remains near the
mass/energy-selected regular endpoint K=0.3496240637Kstar. All tested late
criteria pass. Separate accepted-state and sampled energy diagnostics are
small; a tighter-time completion agrees closely. The expansion chain required
a genuine unchanged-RHS BDF continuation after two capped Radau attempts.
Their historical resource-limited statuses are retained.

The minimum principle preserves a seeded global floor. It does not guarantee
seeding from K=0 or establish a mesh-uniform protected central bound. Other
ordered cusp initial data remain counterexamples to a universal core theorem.
The stationary isentropic prediction is independent of observed final K but
conditional on a regular limiting branch. Global branch uniqueness, entropy
ordering preservation, and dynamical convergence remain open.

Current evidence: [README.md](README.md), [analysis_v2](analysis_v2/summary.json),
[NUMERICS.md](NUMERICS.md), [ISENTROPIC_LIMIT.md](ISENTROPIC_LIMIT.md).
Review freshness: [REVIEWS.md](REVIEWS.md). Complete run lineage and
interpretation history: [PROVENANCE.md](PROVENANCE.md). No external jobs from
this phase remain running; no production X48 mechanism or grade was changed.

Next decisive theoretical route: prove a fixed-duration heating lower bound
and guard control on a central material prefix, uniformly in resolution,
along with admissible geometry. Next independent physical route: evaluate
actual forest density/compression histories against the chosen material
scales. A cosmological exterior and responsive baryonic disc require their
own tests. The earlier static baryon results are not substituted for them.
