# Exact main-agent commands and important exits

Repository working directory for commands below:
`/Users/carlzimmerman/new_physics/zimmerman-formula`.
Sub-agent numerical commands and exact expanded argv are preserved in each
version-2 manifest, plus the recoil/medium and initial-data command indices.

## Unit tests

```bash
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026 -p 'test_trigger.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026 -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fixed_action_initial_data_2026 -p 'test_*.py' -v
```

Important exits: trigger tests first exited 1 with five expected missing-module
assertion failures, then exited 0 with five passes after implementation; the
existing cosmological-bridge suite exited 0 with 35 passes; initial-data tests
exited 0 with four passes. These do not certify the full theory.

## Exact trigger/action run

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/trigger_contract.json --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/trigger.py --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/trigger_001 --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/trigger_001/result.json --timeout 90 --max-output-bytes 1048576 --max-threads 1 -- python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/trigger.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/trigger_001/result.json
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/trigger_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Both exited 0. Reproduction requires replacing the result/run folder with a
new name; existing archived evidence is deliberately not overwritten.

## Lean

Executed from
`qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026`:

```bash
/opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/ClockMoments.lean
```

Exit 0, seven theorem axiom reports. Repeated under the bounded provenance
runner: `lean_001/manifest.json` contains the exact command including working
directory, source/toolchain/manifest hashes and exit 0. The two additional
Lean modules were compiled by their corresponding executed audit wrappers and
independently by the reviewer; commands and axiom reports are retained in
`recoil/lean_run_003` and `medium_emission/run_002`.

## Important scientific outcomes versus execution status

| Evidence | Important execution status | Scientific outcome |
|---|---|---|
| `trigger_001`, `lean_001` | 0 | Necessary pure-dust/clock constraints; no full-action certificate |
| `recoil/numeric_run_002`, `recoil/lean_run_003` | 0 | Quadratic rest-mass-loss claim incompatible with exact mass shells |
| `orbits/analytic_001`, `convergence_001`, `replication_001`, `verification_001` | 0 | Four hosts simulated; fixed-NFW cluster ceiling fails |
| `fixed_action_initial_data_2026` archived runs | 0 | No tested positive-q history passes both temporal directions |
| `medium_emission/run_002` | 0 | Emission-only passive medium cannot supply positive heating |

Historical failed recoil executions and their causes are retained in
`recoil/RUNS.md`. They are not silently promoted to successful or fresh-source
evidence. Source comment corrections similarly require a fresh manifest.

## Git inspection and scope

Executed read-only `git status --short`,
`git status --short --untracked-files=no`, `git log` with recent SHA/date/message
formats, `git show --stat --oneline HEAD`, `git branch --show-current`,
`git diff --cached --stat`, and targeted source reads. Shared branch is `main`.
No checkout, reset, cleaning, or existing source modification was performed.
Only these two new research directories are selected for the authorized
commit, excluding the exploratory JSON. Commit/push results are reported to
the user after the actual Git commands complete.

`git diff --cached --check` exited 2 solely because the preserved raw SciPy
quadrature-warning log contains trailing spaces. The log was not edited or
its hash invalidated. The source/document/data-only check
`git diff --cached --check -- '*.py' '*.lean' '*.md' '*.json'` exited 0.
See [the exact file index](FILES.md) for the selected paths.
