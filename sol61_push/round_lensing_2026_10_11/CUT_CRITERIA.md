# Constraint-generation continuation, frozen before execution

The full spherical_run hit its 60 CPU-second cap (exit -24), with no
scientific outputs. Preserve it unchanged. No optimum from that run is known.
The sparse all-pairs formulation has up to 55074 shape rows; solving every
row at once is the working performance hypothesis, not an established cause.

Keep all mathematical cells, tolerances, controls and non-claims in
SPHERICAL_CRITERIA.md. Replace only the LP execution with deterministic
constraint generation. Begin with all monotonic rows. Solve the relaxation,
scan EVERY shape row, and add up to 400 most violated omitted rows each
iteration. Accept only if all original rows have absolute violation <=1e-7.
Cap each LP at 15 wall seconds and each phase at 40 iterations. Abort rather
than interpret an incomplete separation run. Include the active-row dual
lifted by zeros to all omitted rows, check dual signs, column feasibility,
objective gap, and full primal feasibility. Check a tiny synthetic problem
against the full-row solver and MUTATE omission of a necessary cut.

Run cells sequentially, emitting progress after each solve and checkpointing
completed cells. One numerical thread; <=300 MB expected; total CPU cap 180s,
wall cap 240s. This budget adjustment is declared before seeing results.
Both solver tolerances and all four cells are required for a complete result.
Any partial result stays explicitly partial. No change to theory parameters,
no statistical rejection or positive-3D existence claim.

Commit this criteria file ALONE before execution.
