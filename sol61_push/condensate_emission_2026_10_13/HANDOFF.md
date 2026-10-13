# Condensate-emission research handoff

2026-10-13. Read REPORT.md for equations, hypotheses and interpretation.

## Evidence

- run/manifest.json: baseline calculation; bdg_run/manifest.json: extended calculation with 24 numerical checks total and four exact symbolic identities.
- lean_run_v2/manifest.json: three Lean statements, clean main compilation, two deliberately false controls rejected.
- All three successful manifests validated against current files after execution.
- lean_run/ is a historical failed strict audit (unused-hypothesis warning). Its original source is retained as CondensateWindow_initial.lean; it is not current successful evidence.
- Actual execution checkout was dirty main at 560af1dffb99a2721f52e8b605a1138dbb779c84. Manifests pin individual input hashes. Publication uses a separate index atop codex/cold-energy-equations at 283fe7b46d1f62d8a2aff1376c14d9a9e932f86d; no shared checkout or index changes. Publication checks every contracted execution input against the staged tree.

## Scope and next calculation

Occupied condensate final states enhance a hypothetical radiative channel, while repulsive detuning closes it at sufficiently high density. The leading polynomial rate window is formally bounded. The actual homogeneous gapped mode agrees with the weak-mixing example to about 0.009% in projected rate. This is conditional theoretical evidence, not experimental evidence or a complete glow-plus-gravity mechanism.

Next calculate the same dressed mode's nonradiative decay into finite-momentum excitations, using the full coupled-field eigenvectors and cubic vertices, then compare its radiative branching fraction. Photon transport, finite-cloud stability, source preparation and confinement remain independently unresolved. Do not use the stationary coherent background as a supply of decaying excited particles. Do not promote the negative-Maxwell or uncontrolled large-field scan rows.
