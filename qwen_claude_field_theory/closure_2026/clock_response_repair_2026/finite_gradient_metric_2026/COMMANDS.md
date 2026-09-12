# Exact scientific commands and exits

Working directory unless specified: `/Users/carlzimmerman/new_physics/zimmerman-formula`.
Reviewed base HEAD: `706cd625f648079d318aa968b59fbd45850720f2`.

## Fresh final regression checks

```bash
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026 -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/cubic -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_background_2026 -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026 -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/l192_principal_audit_2026 -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/l192_stress_audit_2026 -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fixed_action_initial_data_2026 -p 'test_*.py' -v
```

All seven exited **0**, with respectively **4,6,6,35,4,5,4 tests** (64 total).
The initial metric-only test command used `-p test_metric_principal.py` before implementation and exited **1** with four expected missing-implementation assertion failures. After implementation the same four tests passed, and the fresh full-pattern run above passed. An independent reviewer also reran metric/cubic tests and Lean successfully.

## Metric bounded run

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/contract.json --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/metric_principal.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/test_metric_principal.py --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/run_001 --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/run_001/result.json --timeout 90 --max-output-bytes 1048576 --max-threads 1 -- python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/metric_principal.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/run_001/result.json
```

Runner and child exit **0**; exact matrix/rank/differential-order results and hashes are in `run_001/`. The cubic and homogeneous-background bounded commands are in [cubic/COMMANDS.md](cubic/COMMANDS.md) and [background/COMMANDS.md](../finite_gradient_background_2026/COMMANDS.md), with exact argv in their manifests. Both child/runner exits **0**. The wrappers/scripts created in this change were executed.

## Lean build

Direct check from the existing `clock_constitutive_construction_2026/lean_formalization_2026` project:

```bash
/opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/AffineCubic.lean
```

Exit **0**, four lemmas, only the reported standard logical axioms. The fresh archived repetition used:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/lean_contract.json --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/AffineCubic.lean --input qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lean-toolchain --input qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lake-manifest.json --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/lean_001 --timeout 90 --max-output-bytes 1048576 --max-threads 1 -- /bin/bash -c 'cd /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026 && /opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/AffineCubic.lean'
```

Runner and child exit **0**. Pinned toolchain/Mathlib declarations and axiom output are retained in `lean_001/`. Lean checks the displayed conditional algebra, not empirical truth or all geometric/physical premises.

## Current-input and result validation

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/lean_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/cubic/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_background_2026/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

All four exited **0**: hashes match and records validate; mathematical interpretation still requires review. Reproduction needs fresh output-directory names, not overwriting archives.

## Git and review scope

Read-only commands included `git status --short --untracked-files=no`, `git log -5 --format='%h %s'`, file discovery with `rg --files`, and source/report reads. This shared checkout remains on main. Only the exact files indexed in [FILES.md](FILES.md) belong to this change; other agents' untracked work is left untouched. The final user handoff records the actual commit and push outcome. No force push, history rewrite, coefficient reconstruction, or paper publication is authorized or performed by this package.
