# CD26-4 evidence reconciliation

The final independent reconciliation command is

```sh
python3 real_research/common_action_2026_09_26/verify_checkpoint.py
```

It completed successfully: **25 accepted manifests validate; 55 Lean
declarations in seven current files match successful compiler records**.
The machine-readable [verification.json](verification.json) records every
accepted manifest, source/log hash, declaration count, axiom inventory and
lint count. Manifest validation includes the declared input and output hashes;
it does not assert that a physical model is correct.

## Formal evidence

| Current Lean file | Declarations | What is formalized |
|---|---:|---|
| assembly/AssemblyBridge20260926.lean | 6 | Zero-mode contradiction/projection, quartic bounds, energy and convexity algebra |
| assembly/CanonicalAuxiliary20260926.lean | 5 | Legendre identity, square completion, coercivity and Hessian inequalities |
| assembly/BarrierBridge20260926.lean | 3 | Exact positive-floor regularization identities |
| evolution/EvolutionBridge20260926.lean | 14 | Monotonicity, filter/gate identities, frozen signs and perspective Hessian |
| evolution/PQBridge20260926.lean | 6 | Conditional de Sitter rational bounds, kinetic/stiffness signs and infrared tuning |
| transport/CommonTransport20260926.lean | 13 | Bounded potential, current/exchange and transition algebra |
| transport/ConversionTransport20260926.lean | 8 | Conversion potential, charge cancellation, resonance and energy balances |

All current compiled declarations report only `propext`, `Classical.choice`
and `Quot.sound`. None uses `sorryAx`, an admitted proof or a new physical
axiom. Accepted lint warnings concern unused hypotheses or tactic style;
their counts and logs remain visible. Compilation was through the repository's
Lean 4.34.0-rc2 / mathlib
`85e3a25e006c35636f0e53b0e9296caca2685bc0` environment. This is **not** a
formal certification of the entire gravity theory.

In particular, the continuum compactness/elliptic arguments, global
fixed-background wave theorem, nonlinear homogeneous cosmology theorem,
complete action variation and observational interpretation are mathematical
arguments in the linked reports. The Lean files certify their explicitly
listed algebraic ingredients, not those larger conclusions.

## Accepted computational evidence

- [Action evidence](action/EVIDENCE.md): four original accepted runs; the
  separate [PQ evidence](action/PQ_EVIDENCE.md) adds its action-variation run.
- [Evolution evidence](evolution/EVIDENCE.md): six earlier accepted runs,
  supplemented by the actual-background de Sitter and PQ runs in
  [FRW_RESULT.md](evolution/FRW_RESULT.md).
- [Assembly](assembly/REPORT.md): energy/current identities and controlled
  ODEs, convex gate identities/Jensen controls, and exact projected variations.
- [Transport evidence](transport/EVIDENCE.md): eight original accepted runs,
  supplemented by the refined homogeneous FRW run. The nonlinear outgoing
  packet and homogeneous cosmology are distinct experiments.

The accepted count is five action, eight evolution, three assembly and nine
transport manifests. Scientific negative controls remain accepted evidence
when they correctly demonstrate a failed candidate. They are not converted
into physical passes by appearing in this count.

Earlier Lean attempts and source snapshots are retained. The first
homogeneous cosmology integration failed its final two-tolerance comparison
and is retained as `transport/run_homogeneous_frw_001`; it is excluded from
the accepted count. The refined run `run_homogeneous_frw_002` passes its
43 controls, including independently evolved Friedmann, energy and charge
ledgers. The failure and refinement do not change the analytic theorem.

## Independent review and scope

The [host review](transport/FINAL_HOST_REVIEW.md) checks the projected
variations and static/frozen scope. The
[quadratic extension review](transport/QUADRATIC_PERSPECTIVE_REVIEW.md)
checks the extended positive-floor proof. The action and evolution lanes
independently derive the de Sitter scalar reduction and all-wavelength sign
bounds; root reconciles their coefficients in
[VACUUM_STIFFNESS.md](assembly/VACUUM_STIFFNESS.md).

The checks deliberately do not certify exact global filtered MOND for the
new gate, full Dirac counting, general-background health, occupied-carrier
perturbations, nonlinear inhomogeneous continuation, full PPN or a fitted
evacuation history. These remain explicit obligations in the live report.

Final mathematical proofreading covers this checkpoint's current reports
and the newly inserted recipe/standing paragraphs. Changes include corrected
source/density distinctions, projection terms, action-version attribution,
the regularization minimizer step and the distinction between homogeneous,
fixed-background and fully coupled evolution. These substantive repairs are
documented as research revisions, not silently classified as typographical
edits. Prior repository history and unrelated dirty files were not rewritten.
