# Accepted evidence and exact certification scope

Four Mathbox computation-audit manifests are accepted:

| Route | Checks | Additional controls | Evidence |
| --- | ---: | --- | --- |
| Reciprocal vacuum | 24 exact/control assertions | 90 finite sign regressions | [run](vacuum/run_001/results.json) |
| Occupied FRW | 25 exact identities | Full constraint block and UV limit | [run](occupied/run_001/results.json) |
| Joint auxiliaries | 26 exact/bounded checks | Three one-harmonic variational solves | [run](static/run1/results.json) |
| Expanding transport | 26 exact/finite checks | Two expansion rates and uncoupled controls | [run](transport/run_001/results.json) |

There are **101 recorded checks**, plus the vacuum's 90 finite regressions.
These counts mix assertion types and are not 101 independent physical tests.
All bounded runs completed with exit zero; the manifests pin their scripts
and results. Analytic theorems are stated separately from those computations.

Two Lean sources compiled in this checkpoint, **14 declarations total**:

- [ReciprocalVacuum20260926.lean](vacuum/ReciprocalVacuum20260926.lean): eight
  algebraic statements about inverse symmetry, positivity and factorizations.
  The curvature formula is checked algebraically; identifying it as a
  derivative and the elliptic theorem are not Lean-formalized.
- [OccupiedBridge20260926.lean](occupied/OccupiedBridge20260926.lean): six
  conditional algebraic/positivity statements for the kinetic and constraint
  reductions. The ADM derivation and full PDE theory are not Lean-formalized.

Accepted outputs use only `propext`, `Classical.choice`, and `Quot.sound`;
no admissions/custom axioms. The occupied compile has one harmless style
warning. Prior CD26-4 declarations remain separate historical evidence.

Independent reviews: [vacuum and fixed-data barrier audit](static/VACUUM_AUDIT.md),
and the [occupied derivation's vacuum cross-check](occupied/RESULT.md).
Root also read the dual argument and the exact transport energy/Lyapunov
identities. The source-specific reports preserve their limitations.

Run `python3 real_research/breakthrough_review_2026_09_26/verify.py` from the
repository root to validate all four manifests against current files, check
accepted Lean source/log hashes and axioms, and check local report links.
The [machine record](verification.json) records that verification. It does
not recompile Lean or re-run the numerical experiments; their accepted fresh
compiler/runner outputs are preserved and hash-checked.
