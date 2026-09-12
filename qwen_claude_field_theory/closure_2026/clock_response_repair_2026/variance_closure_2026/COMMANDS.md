# Executed commands and statuses

Working directory unless stated otherwise:
`/Users/carlzimmerman/new_physics/zimmerman-formula`.
The short symbol B below expands to
`qwen_claude_field_theory/closure_2026/clock_response_repair_2026`;
V expands to `B/variance_closure_2026`. These are path abbreviations in this
document, not environment variables used by the scientific scripts.

## Current source inspection

`git status --short --untracked-files=no` and `git log -5 --oneline`:
exit 0. Initial tracked tree clean. Observed latest revisions progressed
from `48ab93de3` to concurrent `08281ae25`. Targeted `sed`, `rg --files`,
and `git show` reads inspected actual action, tests, PAPER20 and L195 sources;
the independent reviews contain source locations and hashes.

## Scientific execution and certificates

1. `python3 -B B/variance_closure_2026/run_certificates.py`: exit **0**.
   This executes `vertices/vertices.py --result-file .../vertices/run_001/result.json`
   and the Lean compiler under separate bounded v2 runs, then validates both
   manifests with `--root`. Exact expanded executable argv and timestamps are
   in `vertices/run_001/manifest.json` and `lean_001/manifest.json`.
2. `python3 -B B/variance_closure_2026/geometry/derive_geometry.py --result-file B/variance_closure_2026/geometry/result.json`:
   exit **0**. The subsequent canonical bounded run and validation also exit
   **0**; all expanded arguments are in `geometry/run_001/manifest.json` and
   `geometry/COMMANDS.md`. Canonical result: **23 exact symbolic assertions**.
3. `python3 -B B/variance_closure_2026/evolution/variance_evolve.py --result-file B/variance_closure_2026/evolution/run_001/result.json`:
   bounded run exit **0**, validator exit **0**. Full runner invocation and
   actual argv are in `evolution/README.md` and `evolution/run_001/manifest.json`.
4. Coordinator independently reran the entire scientific evolution after
   reviewing its source (exit **0**), with this exact shell command after
   expanding B in the script path:

   ```bash
   variance_check_dir=$(mktemp -d /private/tmp/variance-closure-check.XXXXXX)
   python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/evolution/variance_evolve.py --result-file "$variance_check_dir/result.json"
   ```

   Its three printed k summaries reproduce the archived scientific results.
   The archive, not the temporary recheck copy, is the committed evidence.
5. The exact Lean command, run from
   `qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026`:

   ```bash
   /opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/VarianceClosure.lean
   ```

   Final direct, bounded, and independent reviewer compiles: **0**.
   Seven theorems; axiom reports contain only `propext`, `Classical.choice`,
   `Quot.sound`, with no `sorryAx` or custom axiom. The theorem interpreting
   a scalar homogeneous rate is not a formal matrix covariance theorem.

Each of the four version-2 manifests was validated against current inputs by:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py PATH_TO_MANIFEST --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

All four final statuses are **0**. Manifest validity certifies provenance,
not the mathematical interpretation or completeness of gravity.

## Fresh coordinator tests and regressions

The exact command for each row was
`python3 -B -m unittest discover -s DIRECTORY -p 'test_*.py'`, with DIRECTORY
equal to B followed by the path below. Every final exit status was **0**.

| Directory under B | Tests |
|---|---:|
| `variance_closure_2026/geometry` | 8 |
| `variance_closure_2026/evolution` | 4 |
| `variance_closure_2026/vertices` | 5 |
| `cosmological_bridge_2026` | 35 |
| `inhomogeneous_charge_2026/exterior` | 5 |
| `inhomogeneous_charge_2026/current` | 9 |
| `inhomogeneous_charge_2026/constraints` | 5 |
| `inhomogeneous_charge_2026/tracking` | 5 |
| `finite_gradient_metric_2026` | 4 |
| `finite_gradient_metric_2026/cubic` | 6 |
| `finite_gradient_background_2026` | 6 |
| **Total** | **92** |

These regression counts include earlier certificates only as executable
regressions; they are not 92 newly solved physics gates.

## Development failures, retained transparently

- Initial vertex tests against explicit stubs: exit **1**, first four
  assertion failures and a missing-result-key error; after completing that
  stub's result shape, all five failed as intended. Implementing the actual
  expansion/flux calculation changed them to five passes, exit **0**.
- First Lean compile: exit **1**, because one `unfold` command attempted to
  unfold two different definitions in both branches of a conjunction.
  Separating the branch proofs fixed the tactic error; subsequent compiles
  have no `sorryAx`. This was not a failed physical theorem.
- First metric regression invocation incorrectly used the nonexistent
  directory `B/finite_gradient_metric_2026/metric`: exit **1** (discovery
  import error). The actual directory discovered with `rg --files` is
  `B/finite_gradient_metric_2026`; its four tests passed, exit **0**.
- Geometry's two in-memory normalization/sign mutations were rejected by
  the targeted tests. They were never saved to production source.
- One edit request used unsupported delete-plus-add operations for the same
  path and was rejected without changing it; the subsequent update succeeded.

No old source, coefficients, or archived evidence were edited. Mathematical
self-review and independent review explicitly distinguish component vertices,
linear covariance, formal algebra, and the still-uncomputed nonlinear reduction.

## Integration

Integration uses an exact-path-only commit of `V/`, preserving concurrent
work, followed by `git push origin HEAD:main`. The resulting commit identifies
the complete file set; no force push, reset, broad staging, or old-paper rewrite
is part of this checkpoint. See the final handoff for actual commit/push status.

At integration, `git show --stat --oneline 53b1869f5` (exit 0) revealed a
later L196 output-only commit. Its numerical claims were not audited or used
as premises here. Concurrent modification of `fable_independent_2026/FINDINGS.md`
was left untouched. The initial exact-path `git add -N -- V` and
`git diff --check -- V` both exited 0; all four current-input manifest
validations were rechecked immediately before integration.
