# Verified run

`run_001` completed 2026-09-10 17:32 UTC, exit 0, runtime 2.895504 seconds. Execution HEAD was `9af1f5856527adbc148ee8c1fcaeec4e1937cf14` in the dirty shared worktree; the dispatched starting base was `5fcb04bb7`. Only the new `dhost_kinetic/` package was edited by this lane. No commits or dependency installations.

Results: four exact Python test groups pass (0.152 seconds); the executable algebra report prints 21 zero residuals; four Lean theorems compile with no warnings and only `propext`, `Classical.choice`, `Quot.sound` axioms (no `sorryAx`). The manifest verifies against current inputs. Manifest SHA-256: `a30c683a8ce1baaeb8b3494a67d733f1b73d3a6a8456d4fe83d0292e168ba12e`.

Reproduce from repository root:

```sh
python3 -B qwen_claude_field_theory/closure_2026/kgb_healthy_matching_2026/dhost_kinetic/test_kinetic.py
python3 -B qwen_claude_field_theory/closure_2026/kgb_healthy_matching_2026/dhost_kinetic/kinetic.py
```

From the existing `clock_constitutive_construction_2026/lean_formalization_2026` environment, run `lake env lean` with the absolute path to `dhost_kinetic/KineticDegeneracy.lean`. Exact arguments, full logs, before/after input hashes, 60-second timeout and log cap are recorded in `run_001/manifest.json`. Versions: child Python 3.9.6, SymPy 1.14.0, runner Python 3.11.13, Lean 4.34.0-rc2, Mathlib `85e3a25e006c35636f0e53b0e9296caca2685bc0`.

An independent read-only algebra check agreed on all contractions, the acceleration coefficient, square and kinetic primary relation. This is still a primary kinetic-block result: no full Dirac closure, scalar-health or common-mass solution is certified.
