# Fixed-common-state refinement appendix

The refined runner loads `--initial initial.npz` and the adjacent
`initial_metadata.json` through `refined_initial.load_initial`. It validates the
physical masses, particle/species counts, initial seed and saved state hash.
The saved velocities are retained at every softening, timestep, collision
choice and backend. The optional host case adds the same analytic orbital
translation only after loading that relative state.

`refined_core.py` is a versioned mechanical copy of `run_resolution.py`, whose
SHA256 is `e13233e8b73db3c401cbf000ab8f7bb708edc4ba38120a38ada8594b685bec30`.
Its differences are common-state loading, explicit force/collision callbacks,
and rejection of existing scientific output. The H4 map, positive-time end
collision step, full three-dimensional Plummer gravity law, analytic host,
retention of every original particle, remnant diagnostic, energy/vector
angular-momentum/host-work receipts and saved trajectory conventions remain.
The CTMC samples the same frozen-position central elastic generator; this
does not eliminate outer timestep or finite collision-support errors.

Native `cpu` uses binary64 direct forces. `metal` uses the separately tested
DS expansion implementation, whose same-state full-CPU checks use relative
force L2, potential L2 and energy errors below `1e-11`. CPU comparisons are
bounded to supplied total particle count at most 32768 and any skipped checks
are recorded explicitly.

The `mixed`, `tile` and versioned `tile2` candidates have a **separate empirical numerical
budget**: relative force L2 below `5e-7`, maximum per-particle relative force
error below `2e-6`, maximum relative potential error and relative total
potential-energy error below `5e-7`. They do not inherit the DS `1e-11` gate.
Both retain raw three-component coordinate encoding but round pair
interactions to FP32; `mixed` uses DS subtraction and accumulation, while
`tile` uses FP32 displacement and tile partial sums with DS merges. `tile2`
retains a separate implementation and library, using four FP32 partial chains
and balanced reduction before each DS tile merge; it does not overwrite tile v1.
Metadata
records the selected implementation and binary hash without relabeling this
arithmetic as native binary64 or DS interaction arithmetic.

At gravity calls 1, 2, 100, 1000, 6000, 30000, 60000, 120000 and 240000, candidates compare
against a full DS force evaluation and, for total N at most 32768, a full
native CPU evaluation. Calls made by instantaneous unbinding diagnostics also
count; each comparison records its particle count. The maximum absolute
particle-force error divided by the maximum reference force is recorded
alongside the per-particle relative maximum, so cancellation points are not
hidden. These sparse same-state checks do not certify accumulated trajectory
error. Long-run E/vector-J/momentum gates, timestep controls and matched
profiles remain necessary before physical interpretation.

The launcher requires a fresh case, freezes this appendix, selected backend
sources/binary, DS and CPU references where used, common initial bytes and
metadata, CTMC and old diagnostic sources, and the original cold master
equations. No core profile, spherical-force assumption, cooling sink,
thermostat, particle deletion, live host absorption or evolved-field claim is
introduced. A completed record is finite evidence, not a convergence result.

Implementation plan: first test fixed 512+64 arrays at eps10/20 against the
existing H4 map and test candidate rejection/provenance; then create the
mechanical core copy, accuracy wrapper and bounded launcher; finally run only
tiny CPU smoke controls and request parent review before production.
