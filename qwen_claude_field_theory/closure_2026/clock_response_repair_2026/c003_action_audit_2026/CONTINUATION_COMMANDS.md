# L191/L192 continuation: commands, exits, and evidence boundaries

Working directory unless specified:
`/Users/carlzimmerman/new_physics/zimmerman-formula`.
Exact bounded-run argv, source hashes, logs, resource limits and exit status
are recorded in the version-2 manifests linked below. Reproduction uses new
run-directory names, never overwriting the archived evidence.

## Main-agent unit suites

```bash
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026 -p test_gradient_transport.py -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026 -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/l192_principal_audit_2026 -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026 -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fixed_action_initial_data_2026 -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/l192_stress_audit_2026 -p 'test_*.py' -v
```

The first command initially exited 1 (expected missing-module failure before
implementation), then 0 with three tests. The five full suites above exited
0 with 8, 4, 35, 4 and 5 tests respectively. Repeated independent principal and
gradient tests also passed. These are scoped regression and algebra tests,
not a full-theory certification suite.

## Main-agent direct Lean checks

From
`qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026`:

```bash
/opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/PoissonFloor.lean
/opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/L192Discriminant.lean
```

Both final sources exit 0 and are independently reviewed. Five plus four
theorems report only propext, Classical.choice and Quot.sound, with no
custom axioms or sorryAx. The Poisson import failure is separately described
in POISSON_RUNS.md. Two developmental discriminant builds exited 1 while
correcting a noncomputable definition, a missing multiplied identity,
denominator handling and a section terminator. Those were unsuccessful
proof drafts, not accepted certificates. The final archived build below
supersedes the unarchived drafts and has no warnings.

## Archived runs

| Run | Execution / validation exit | Actual interpretation |
|---|---:|---|
| `poisson_001/manifest.json` | 0 / 0 | Five conditional mixture/exponential Lean lemmas |
| `l192_lean_001/manifest.json` | 0 / 0 | Four conditional discriminant Lean lemmas |
| `gradient_transport_001/manifest.json` | 0 / 0 | Two exact local jet identities and required tracking source |
| `l191_reconciliation/run_001/manifest.json` | 1 / 0 | Historical failed JSON serialization; not successful result |
| `l191_reconciliation/run_002/manifest.json` | 0 / 0 | Source mismatches and bounded orbit/control discriminator |
| `../l192_principal_audit_2026/run_001/manifest.json` | 0 / 0 | Exact varied Hessian and restricted instability counterexamples |
| `../fixed_action_initial_data_2026/hermes_objective_audit_2026/run_001/manifest.json` | 0 / 0 | Optimizer objective false positive; no optimizer run |
| `../l192_stress_audit_2026/run_002/manifest.json` | 0 / 0 | Ten metric variations, 20 frozen-root stress evaluations, 39 consistency checks |

The stress run_001 is retained as historical evidence after a verdict-output
correction; its original source snapshot is retained alongside it. It is not
claimed as current-input-fresh evidence. Run_002 reran the corrected source.

`../l192_principal_audit_2026/COMMANDS.md`, `POISSON_RUNS.md`, the stress
audit report, and the above manifests retain the subtask execution details.
The stress audit's run and tests are recorded separately with its results.

The two additional root-run commands were:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/gradient_transport_contract.json --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/gradient_transport.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/test_gradient_transport.py --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/gradient_transport_001 --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/gradient_transport_001/result.json --timeout 45 --max-output-bytes 1048576 --max-threads 1 -- python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/gradient_transport.py --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/gradient_transport_001/result.json
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/l192_lean_contract.json --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/L192Discriminant.lean --input qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lean-toolchain --input qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lake-manifest.json --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/l192_lean_001 --timeout 90 --max-output-bytes 1048576 --max-threads 1 -- /bin/bash -c 'cd /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026 && /opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/L192Discriminant.lean'
```

Manifest validation uses this exact command with each manifest path above:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py MANIFEST_PATH --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

## Git scope

Read-only checks included `git status --short`, `git status --short
--untracked-files=no`, `git log`, `git show --stat`, and `git diff --cached
--stat`. This is a shared main checkout. New results are staged by exact
path; unrelated untracked data and concurrent-agent work are preserved.
No old action or gate threshold was edited. The earlier checkpoint's main
files landed in concurrent commit `9b97161a6`; `056a4159e` was only its file
index cleanup. This continuation is a separate scoped commit, not a rewrite
of either shared commit.

The first staged whitespace check exited 2 only because the preserved raw
L191 run_002 stdout ends with an extra blank line. Its log and provenance
hash were not changed. The source/document/data-only staged check is used
before commit; raw experimental logs remain verbatim.
