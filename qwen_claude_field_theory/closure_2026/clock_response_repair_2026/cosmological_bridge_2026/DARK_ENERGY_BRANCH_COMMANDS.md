# Density and alternative-branch execution record

Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula`.
Starting commit: `cb8a5d98e`. All files below are relative to
`qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026`.

## Files created

- `dark_energy_branches.py`
- `test_dark_energy_branches.py`
- `branch_continuation.py`
- `test_branch_continuation.py`
- `branch_kinetic.py`
- `test_branch_kinetic.py`
- `dark_energy_branches_contract.json`
- `branch_continuation_contract.json`
- `branch_kinetic_contract.json`
- `DARK_ENERGY_BRANCH_REPORT.md`
- `DARK_ENERGY_BRANCH_COMMANDS.md`
- `dark_energy_branches_001/manifest.json`
- `dark_energy_branches_001/result.json`
- `dark_energy_branches_001/stdout.txt`
- `dark_energy_branches_001/stderr.txt`
- `dark_energy_branches_002/manifest.json`
- `dark_energy_branches_002/result.json`
- `dark_energy_branches_002/stdout.txt`
- `dark_energy_branches_002/stderr.txt`
- `branch_continuation_001/manifest.json`
- `branch_continuation_001/result.json`
- `branch_continuation_001/stdout.txt`
- `branch_continuation_001/stderr.txt`
- `branch_continuation_002/manifest.json`
- `branch_continuation_002/result.json`
- `branch_continuation_002/stdout.txt`
- `branch_continuation_002/stderr.txt`
- `branch_kinetic_001/manifest.json`
- `branch_kinetic_001/result.json`
- `branch_kinetic_001/stdout.txt`
- `branch_kinetic_001/stderr.txt`

Modified `REPORT.md` only to link the current result. No existing implementation,
coefficient, initial-data archive or Claude result was changed.

## Important commands actually executed

All five bounded experiment invocations below returned exit 0. Both backward
alternative-branch continuations recorded a physical gradient-gate failure,
not a working theory. Manifests record exact argv, source hashes and limits.

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/dark_energy_branches_contract.json --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/dark_energy_branches_001 --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/dark_energy_branches.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_probe.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_jets.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/derive.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/background_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_002/result.json --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/dark_energy_branches_001/result.json --timeout 90 --max-output-bytes 1048576 --max-threads 1 -- python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/dark_energy_branches.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/dark_energy_branches_001/result.json --grid 1601

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/dark_energy_branches_contract.json --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/dark_energy_branches_002 --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/dark_energy_branches.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_probe.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_jets.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/derive.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/background_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_002/result.json --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/dark_energy_branches_002/result.json --timeout 90 --max-output-bytes 1048576 --max-threads 1 -- python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/dark_energy_branches.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/dark_energy_branches_002/result.json --grid 3201

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_continuation_contract.json --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_continuation_001 --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_continuation.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_probe.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_jets.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/derive.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/background_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_continuation_001/result.json --timeout 90 --max-output-bytes 1048576 --max-threads 1 -- python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_continuation.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_continuation_001/result.json --step .025

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_continuation_contract.json --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_continuation_002 --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_continuation.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_probe.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_jets.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/derive.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/background_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_continuation_002/result.json --timeout 90 --max-output-bytes 1048576 --max-threads 1 -- python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_continuation.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_continuation_002/result.json --step .0125

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_kinetic_contract.json --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_kinetic_001 --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_kinetic.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_continuation.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/dark_energy_branches.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_probe.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_jets.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/derive.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/background_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_002/result.json --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_continuation_002/result.json --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_kinetic_001/result.json --timeout 90 --max-output-bytes 1048576 --max-threads 1 -- python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_kinetic.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_kinetic_001/result.json --continuation-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_continuation_002/result.json
```

All five provenance validations returned exit 0:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/dark_energy_branches_001/manifest.json
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/dark_energy_branches_002/manifest.json
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_continuation_001/manifest.json
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_continuation_002/manifest.json
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/branch_kinetic_001/manifest.json
```

Full regression returned exit 0, **35 tests passed**:

```bash
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026 -p 'test_*.py' -v
```

The three focused test files `test_dark_energy_branches.py`,
`test_branch_continuation.py` and `test_branch_kinetic.py` were each run
before implementation (missing-module failure, exit 1) and afterward
(three tests each, exit 0). The same discovery command selects them via
its `-p` argument. No threshold was relaxed to make them pass.

Read-only checks included current git status/recent commits, the original
constitutive/action/background/transfer implementation, Claude's current
stability work, independent stress/kinetic checks, and the observational
sources linked in [the report](DARK_ENERGY_BRANCH_REPORT.md).

No new Lean theorem or empirical likelihood fit was added. Process/test
successes are separate from the scientific branch failures.
