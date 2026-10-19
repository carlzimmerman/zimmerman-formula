# Reproduction

Existing independent record, without rerunning:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_nonborn_vacuum/reviews/vacuum/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Run the independent implementation with a fresh own output directory from the repository root, using this structured argv construction. Change `run_002` if it already exists.

```python
import json, subprocess, sys
from pathlib import Path
root = Path.cwd()
base = Path('fine_structure_puzzle/qcd_nonborn_vacuum/reviews/vacuum')
skill = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit')
contract = json.loads((base/'CONTRACT.json').read_text())
output = base/'run_002'
argv = [sys.executable, str(skill/'scripts/run_experiment.py'), '--root', str(root),
        '--contract', str(base/'CONTRACT.json')]
for path in contract['execution_artifacts']:
    argv += ['--input', path]
argv += ['--output', str(output), '--result', str(output/'RESULTS.json'),
         '--timeout', '55', '--max-output-bytes', '65536',
         '--max-cpu-seconds', '45', '--max-threads', '1', '--',
         sys.executable, str(base/'check_independent.py'), '--result', str(output/'RESULTS.json')]
subprocess.run(argv, check=True)
```

The code requires the three pinned public source files at their existing transient paths and checks their hashes. It does not fetch them or modify a cache. It checks all author pins before returning; if reviewed artifacts change, preserve this record and establish a new audit/contract instead of silently refreshing `INPUTS.json`.
