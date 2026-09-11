# Lean constraint identity: proved as written, not full theory closure

2026-09-11, base commit 31e334cb3c20ff3a66032296942d3e7cc64d91b2.
One bounded formalization requested by Carl Zimmerman to conserve usage.
No new action, coefficient fit, simulation, or empirical claim is introduced.

[ConstraintPropagation.lean](ConstraintPropagation.lean) proves the exact
real-jet algebra of the metric constraint reduction already derived in
[FIRST_ORDER_HANDOFF.md](FIRST_ORDER_HANDOFF.md).

Write \(p_k=k^2/a^2\), \({\cal C}\) for the Hamiltonian residual, \({\cal M}\)
for the momentum residual, \({\cal R}\) for the trace residual, \({\cal E}\)
for the energy Ward residual, and \({\cal B},{\cal U}\) for background
Raychaudhuri and energy residuals. The 15 real variables and every residual
are defined explicitly in the Lean file; none is assigned an expected zero.
The physical derivative interpretation assumes constant \(M^2\) and
\(\dot p_k=-2Hp_k\).

The unconditional polynomial identity is

\[
\boxed{p_k{\cal M}=\dot{\cal C}+2H{\cal C}
-H{\cal R}+{\cal E}+\alpha{\cal U}
-{\cal B}(\delta K+3H\alpha).}
\]

The four machine-checked statements are:

1. This off-shell identity holds for every tuple of real jets.
2. If the background, trace and energy equations hold, and both
   \({\cal C}=\dot{\cal C}=0\), then \({\cal M}=0\) for \(p_k\ne0\).
3. If instead the background, trace, energy and momentum equations hold,
   the algebraic rate of \(a^2{\cal C}\) vanishes:
   \(2a(aH){\cal C}+a^2\dot{\cal C}=0\).
4. A concrete \(p_k=0,M^2=1\) jet satisfies every premise of item 2 except
   \(p_k\ne0\), while \({\cal M}=1\). Thus that premise cannot be dropped.
   At \(k=0\) this momentum amplitude has no physical spatial-gradient
   meaning: the witness is an algebraic counterexample, not a physical
   solution violating Einstein's equations.

The conservation-rate result does not assume the Hamiltonian residual is
zero. Conversely, the momentum-recovery result needs its derivative, not
just its instantaneous value. These distinctions matter for the pending
numerical constraint checks.

## Scope and verification

**Proved as written for real jets.** Their identification with derivatives
of smooth physical solutions and the preceding action variation are not
formalized here. Nor is a zero-derivative-to-constancy theorem on a time
interval, ODE/PDE existence, stability, a MOND law, CMB viability or a
law of nature. This is an Einstein-constraint compatibility certificate,
not a novel gravitational field equation. Full theory status remains OPEN.

An independent read-only algebra reviewer derived the identity from the
definitions without being supplied the proposed result and checked the
zero-mode restriction. Mathbox proof-audit and self-proofreading preserved
these domains and limitations.

Lean 4.34.0-rc2 compiled all four theorems, exit 0. Each printed dependency
set is exactly propext, Classical.choice, Quot.sound: no sorryAx or added
axiom. Proof development included deliberately unproved goals (exit 1)
before adding proofs; two separate Lean syntax errors were corrected without
changing theorem statements. The final bounded run is in
[constraint_lean_001](constraint_lean_001/manifest.json); its input/output
hash validation exited 0. The existing 10-test bridge suite also exited 0.

Exact child command, from the existing Lean project directory
qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026:

    /opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/ConstraintPropagation.lean

Regression command, from repository root:

    python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026 -p 'test_*.py' -v

Created: this note, ConstraintPropagation.lean, constraint_lean_contract.json,
and constraint_lean_001/{manifest.json,stdout.txt,stderr.txt}.
Modified: REPORT.md, adding the scoped proof link. Existing simulation code,
coefficient functions and previous evidence were not changed.
