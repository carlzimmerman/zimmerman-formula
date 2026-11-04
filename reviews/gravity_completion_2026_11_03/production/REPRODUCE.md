# Reproduction

The preferred record is run_refresh/manifest.json. Its four outputs repeat
the physical stationary transport, corrected threshold controls and numerical
checks under a complete imported local-source hash closure. All earlier runs
are immutable; current interpretation is DERIVATION_CURRENT.md and STATUS.md.

From the repository root, select an output directory that does not exist:

```bash
python3 - <<'PY'
import json, subprocess
from pathlib import Path
root = Path.cwd()
production = Path('reviews/gravity_completion_2026_11_03/production')
contract = production / 'refresh_contract.json'
output = production / 'run_reproduction_001'
runner = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py')
command = ['python3', str(runner), '--root', str(root), '--contract', str(contract)]
for path in json.loads(contract.read_text())['execution_artifacts']:
    command += ['--input', path]
command += ['--output', str(output)]
for filename in ['controls.json', 'physical.json', 'checks.json', 'result.json']:
    command += ['--result', str(output / filename)]
command += ['--timeout', '240', '--max-cpu-seconds', '230', '--max-threads', '1',
            '--max-output-bytes', '1000000', '--', 'python3',
            str(production / 'refresh.py'), str(output)]
raise SystemExit(subprocess.call(command))
PY
```

The runner path is the installed mathbox4.0.0 computation-audit skill; adjust
only that installed-skill location on another host. No install is performed.
The bundled code requires existing Python3.9.6,numpy1.26.2,scipy1.11.4, as
recorded. Standard numerical-library thread variables are set to1. Peak RSS
is measured, not claimed as a macOS-enforced address-space cap.

Validate a record with:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py reviews/gravity_completion_2026_11_03/production/run_refresh/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

VERIFICATION.json records the current validation of all11 histories, including
the failed final_checks JSON serialization attempt. Its failure is preserved;
final_checks_v2.py is the separate fixed source. Pinned mathematical run inputs
may contain superseded interpretation prose. Consult DERIVATION_CURRENT.md for
the corrected vacuum-width, neutral-pole and finite-grid scope.
