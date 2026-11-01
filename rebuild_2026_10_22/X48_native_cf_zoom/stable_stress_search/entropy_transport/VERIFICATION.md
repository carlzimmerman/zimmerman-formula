# Scoped verification, 2026-11-01

Fresh checks at assessment revision
`22174c23b476a1c1c0f0a3230995532cc140e387`, with task artifacts uncommitted in
a shared dirty worktree:

| Check | Observed result | Record |
| --- | --- | --- |
| New transport-area discovery | 52 tests passed in 6.861 s | [transport_tests.txt](verification/transport_tests.txt) |
| Inherited material/static/endpoint discovery | 41 tests passed in 6.152 s | [parent_tests.txt](verification/parent_tests.txt) |
| Bounded-record validation | All 24 phase manifests validate against current input/output hashes, including historical failed attempts | [manifest_validation.txt](verification/manifest_validation.txt) |
| Syntax compilation | All 19 top-level Python files compile in memory | [source_hashes.json](verification/source_hashes.json) |
| Final analysis | Completed; all eight declared finite checks true | [v2 summary](analysis_v2/summary.json), [manifest](analysis_v2/manifest.json) |

The two unittest commands are recorded in [README.md](README.md). They are
scoped area checks, not the full repository suite. Both use one numerical
library thread and a 50-second outer subprocess timeout. The initial explicit
`py_compile` invocation attempted an unwritable system cache; in-memory Python
compilation supplies the syntax check without external cache writes.

The eight automatic analysis criteria concern settling on four finite grids,
N64 relaxation chains, positivity in recorded post-t8 samples, accepted-state
and sampled energy accuracy, and tighter-time profile agreement. They do not
certify continuum or infinite-time behavior. Tight-chain energy values were
also directly reviewed: accepted-state bound `2.4486420163e-9` and sampled
maximum `2.6431251039e-9`; those two fields are not automatic exit gates.

The final plot was visually inspected. Independent numerical reviewers
recomputed selected metrics and checked restart hashes, source identity,
perturbation work, and conditional endpoint quadrature; their scopes and
limitations are in [REVIEWS.md](REVIEWS.md).

Mathematical self-proofreading covered the new README, NUMERICS,
ISENTROPIC_LIMIT, STATUS, checkpoint and review/provenance notes, plus updated
parent overview paragraphs. Definitions, display delimiters, units, entropy
signs, and local links were checked. Routine edits clarify post-warming
positivity and distinguish accepted-state from dense-output errors.
No pre-existing mathematical derivation was changed. The unresolved
mathematical obligations are explicit research gaps, not typographic repairs.

Final local-link, whitespace and tracked-diff checks are in
[document_checks.json](verification/document_checks.json). Tracked X48 changes
are confined to its README; experimental code/data are under the new research
area. No production solver, running job, criterion or grade was changed.
