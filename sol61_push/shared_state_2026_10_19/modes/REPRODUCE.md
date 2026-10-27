# Bounded reproduction

Run from the repository root with the installed Python/NumPy/SciPy/mpmath
versions recorded in the two contracts. No installation or network access is
required. The original output directories are immutable evidence. This command
chooses fresh directories `repeat_modes_001` and `repeat_static_001`; change
those names if they already exist. It executes only the two declared scripts.

```bash
python3 - <<'PY'
import json
import subprocess
import sys
from pathlib import Path

root = Path.cwd()
base = Path('sol61_push/shared_state_2026_10_19/modes')
runner = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py')
validator = runner.with_name('validate_manifest.py')
tasks = [
    ('contract.json', 'repeat_modes_001', 'check_shared_modes.py', []),
    ('static_contract.json', 'repeat_static_001', 'check_static_source.py',
     ['--input', str(base / 'run_001/results.json')]),
]
for contract_name, run_name, script_name, extra in tasks:
    contract_path = base / contract_name
    contract = json.loads(contract_path.read_text())
    output = base / run_name
    result = output / 'results.json'
    argv = [sys.executable, str(runner), '--root', str(root),
            '--contract', str(contract_path)]
    for item in contract['execution_artifacts']:
        argv.extend(['--input', item])
    argv.extend(['--output', str(output), '--result', str(result),
                 '--timeout', '45', '--max-output-bytes', '1048576',
                 '--max-cpu-seconds', '30', '--max-threads', '1', '--',
                 sys.executable, str(base / script_name), *extra,
                 '--result', str(result)])
    subprocess.run(argv, check=True)
    subprocess.run([sys.executable, str(validator),
                    str(output / 'manifest.json'), '--root', str(root)], check=True)
PY
```

The static script compares against the *pinned original* radial result so its
contract remains unchanged. To link it to a new radial result, create a new
contract with the changed `execution_artifacts` and pass the same changed path
to both the runner `--input` and script `--input`; do not overwrite an old run.

Original observed executions: `run_001` took 0.453 seconds and
`run_static_001` took 0.564 seconds as recorded by the runner. Both completed
with wall limit 45 seconds, per-process CPU limit 30 seconds and conventional
numerical thread limit one. No hard memory or affinity limit was requested.
Validation authenticates the evidence bytes, not the mathematical theorem.
