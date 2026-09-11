# Joint precision commands and inventory

Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula`.
All listed files are under `qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026`.
Created:

- `coupled_precision.py`
- `test_coupled_precision.py`
- `coupled_precision_contract.json`
- `coupled_fine_contract.json`
- `COUPLED_PRECISION_REPORT.md`
- `COUPLED_PRECISION_COMMANDS.md`
- `coupled_precision_001/manifest.json`
- `coupled_precision_001/result.json`
- `coupled_precision_001/stdout.txt`
- `coupled_precision_001/stderr.txt`
- `coupled_precision_002/manifest.json`
- `coupled_precision_002/result.json`
- `coupled_precision_002/stdout.txt`
- `coupled_precision_002/stderr.txt`
- `coupled_fine_001/manifest.json`
- `coupled_fine_001/result.json`
- `coupled_fine_001/stdout.txt`
- `coupled_fine_001/stderr.txt`

Modified: `REPORT.md` (checkpoint link only). No previous implementation or
archived evidence changed. Unrelated work preserved.

## Executed computations — each exit 0

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_precision_contract.json --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_precision_001 --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_precision.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_precision.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_jets.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/derive.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/background_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_precision_001/result.json --timeout 90 --max-output-bytes 1048576 --max-threads 1 -- python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_precision.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_precision_001/result.json --digits 40

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_precision_contract.json --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_precision_002 --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_precision.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_precision.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_jets.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/derive.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/background_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_precision_002/result.json --timeout 90 --max-output-bytes 1048576 --max-threads 1 -- python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_precision.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_precision_002/result.json --digits 50

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_fine_contract.json --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_fine_001 --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_precision.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_precision.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_jets.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/derive.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/background_evolve.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_fine_001/result.json --timeout 90 --max-output-bytes 1048576 --max-threads 1 -- python3 -B -c 'import sys,json; from pathlib import Path; sys.path.insert(0,"qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026"); from coupled_precision import run; r=run(steps=(".00025",".000125",".0000625")); Path("qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_fine_001/result.json").write_text(json.dumps(r,indent=2)+"\n"); print(json.dumps([{k:v for k,v in x.items() if k!="transfer_end"} for x in r["rows"]],indent=2))'
```

## Provenance validations — each exit 0

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_precision_001/manifest.json
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_precision_002/manifest.json
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/coupled_fine_001/manifest.json
```

## Tests

```bash
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026 -p test_coupled_precision.py -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026 -p 'test_*.py' -v
```

The first command failed with exit 1 before the implementation existed, then
passed both new tests with exit 0. The full suite passed 26 tests with exit 0.
No new Lean theorem was claimed or added. Numerical interpretation and
limitations are in [COUPLED_PRECISION_REPORT.md](COUPLED_PRECISION_REPORT.md).
