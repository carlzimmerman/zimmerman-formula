# Precision/radiation execution record

All repository-relative paths below are under `qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026` unless written in full.
Starting HEAD: `95e61fa4e68dba1bbfc0931fdc352600748a6d89`.
No pre-existing source implementation was edited. `REPORT.md` gained a checkpoint link.
Unrelated tracked/untracked work was preserved.

## Created files

- `transfer_precision.py`
- `test_transfer_precision.py`
- `integration_precision_probe.py`
- `test_integration_precision.py`
- `radiation_probe.py`
- `test_radiation_probe.py`
- `precision_contract.json`
- `integration_precision_contract.json`
- `radiation_contract.json`
- `PRECISION_RADIATION_REPORT.md`
- `PRECISION_RADIATION_COMMANDS.md`
- `precision_001/manifest.json`
- `precision_001/result.json`
- `precision_001/stdout.txt`
- `precision_001/stderr.txt`
- `integration_precision_001/manifest.json`
- `integration_precision_001/result.json`
- `integration_precision_001/stdout.txt`
- `integration_precision_001/stderr.txt`
- `radiation_001/manifest.json`
- `radiation_001/result.json`
- `radiation_001/stdout.txt`
- `radiation_001/stderr.txt`
- `radiation_002/manifest.json`
- `radiation_002/result.json`
- `radiation_002/stdout.txt`
- `radiation_002/stderr.txt`

## Important commands actually executed

Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula`.
Each archived execution and validation below returned exit **0**. The integration
step probe records a **non-monotonic residual**, not a scientific convergence PASS.
The manifests record actual executable argv, source hashes, software, limits and logs.

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/precision_contract.json --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/precision_001 --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_precision.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_jets.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/derive.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/background_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/precision_001/result.json --timeout 90 --max-output-bytes 1048576 --max-threads 1 -- python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_precision.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/precision_001/result.json

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/integration_precision_contract.json --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/integration_precision_001 --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/integration_precision_probe.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_precision.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_jets.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/derive.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/background_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/integration_precision_001/result.json --timeout 90 --max-output-bytes 1048576 --max-threads 1 -- python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/integration_precision_probe.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/integration_precision_001/result.json

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_contract.json --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_001 --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_probe.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_jets.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/derive.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/background_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_001/result.json --timeout 90 --max-output-bytes 1048576 --max-threads 1 -- python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_probe.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_001/result.json

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_contract.json --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_002 --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_probe.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_jets.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/derive.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/background_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_002/result.json --timeout 90 --max-output-bytes 1048576 --max-threads 1 -- python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_probe.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_002/result.json --step .0125 --rtol 2e-12
```

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/precision_001/manifest.json
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/integration_precision_001/manifest.json
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_001/manifest.json
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_002/manifest.json
```

Full regression: **24 tests, exit 0**.

```bash
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026 -p 'test_*.py' -v
```

New-module red/green checks used the same command with patterns
`test_transfer_precision.py`, `test_integration_precision.py`, and
`test_radiation_probe.py`. Each initially failed (exit 1) before its implementation
existed, then passed (exit 0; respectively 3, 1 and 3 tests).

Existing Lean verification: **exit 0**, four conditional algebra theorems,
using only the standard reported `propext`, `Classical.choice`, and `Quot.sound`
axioms. No new Lean certificate for numerical or physical validity was added.
Working directory for this command:
`/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026`.

```bash
/opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/ConstraintPropagation.lean
```

Read-only checks included current git status/log, relevant source/test/report files,
SciPy's actual DOP853 polynomial evaluation and segment-selection implementation,
and `numpy.finfo(numpy.longdouble)`. On this ARM Mac, longdouble has binary64
precision, which is why the independent evaluation uses mpmath rather than assuming
longdouble provides extra digits. An exploratory three-step integration check is
reproduced by the archived `integration_precision_probe.py` command above.

The tests and manifests establish bounded execution evidence only. See the
[interpretation and open gates](PRECISION_RADIATION_REPORT.md).
