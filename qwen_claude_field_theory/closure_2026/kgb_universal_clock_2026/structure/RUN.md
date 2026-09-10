# Frozen independent structure run

`run_001` completed on 2026-09-10 at 16:10 UTC, exit 0, elapsed 2.800354 seconds. Its SHA-256 manifest is `7d8cdbbd28560262084dda372bec92db7636c65af283045f010bde9112e2098c`.

The task's starting base was `1e8f58095a44e27b9cff0a467737e30eef414601`; the shared repository HEAD at execution was `d0db626c4035117798922587fa5a9edc1e9fb40d`, with a dirty worktree. The old construction source directories used here have no committed difference between these revisions. The manifest hashes the exact listed files before and after execution, including this package's code/report/contract, imported old construction files, Lean environment descriptors, and the local primary IFT source. Unrelated user/root changes were not touched. No commits were made by this lane.

Observed results:

- All 11 Python tests passed (0.463 seconds): exact static inverse, determinant, preservation/cancellation identities, lower-map limiting Jacobian, and three bounded comparisons with the committed inverse and complex-step curvatures.
- All 8 Lean theorems compiled. Each printed only `propext`, `Classical.choice`, and `Quot.sound`; there were no `sorryAx` dependencies.
- The single supplied initial seed was independently refined/evaluated at 60 and 80 decimal digits. Maximum raw matching/first-preservation residuals were approximately `4.381e-48` and `1.754e-67`. Both runs agree on normalized next determinant `-0.00053882941384094395736...` and incompatible individually required controls, as detailed in `REPORT.md` and the full stdout log.
- Manifest validation against the current files returned `valid evidence record; mathematical interpretation requires review`.

Direct reproduction, from the repository root:

```sh
/usr/bin/python3 -B qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/structure/run_checks.py
```

The runner invokes the Python tests, the Lean file from the existing `clock_constitutive_construction_2026/lean_formalization_2026` environment, and both precision evaluations. Its exact subprocess arguments are retained in `run_001/stdout.txt`. A fresh provenance run uses the Mathbox computation-audit `run_experiment.py`, the `contract.json` here, a fresh output directory, and exactly the `execution_artifacts` entries as repeated `--input` arguments; the frozen execution used a 60-second timeout and 1,048,576-byte log cap. No scientific files are silently overwritten.

Manifest verification:

```sh
/opt/homebrew/bin/python3.11 -B /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/structure/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Versions: child Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4, SymPy 1.14.0, mpmath 1.3.0; runner Python 3.11.13; Lean 4.34.0-rc2, Mathlib `85e3a25e006c35636f0e53b0e9296caca2685bc0`.

`REPORT.md` SHA-256: `b304e97c4922da7206b2c4acddc5c9ea829078c39411ad914ebff3f8ad4df7c2`.
`SharedControlAlgebra.lean` SHA-256: `d6a026d58efc7b2c8f06c6c719297879b8eab15983b93c7615990b6cb0ddc4a1`.

The IFT application is prose with an exact checked limiting determinant, not a fully formalized analytic construction. The numerical result concerns one seed, not every mass pair or branch; the singular field map and zero-pivot control cases require their explicit separate conditions. None of this certifies source normalization, universal finite continuation, health, or the full no-dark-matter theory.
