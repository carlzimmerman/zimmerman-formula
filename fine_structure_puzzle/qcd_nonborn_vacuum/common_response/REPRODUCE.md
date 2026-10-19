# Bounded reproduction

The saved contract and scientific inputs preceded `run_001`. Do not
overwrite that run. The exact command is also recorded as argv in its v2
manifest. Python is bundled 3.12.14; no external package is imported.

For a new run, replace `run_002` below with a fresh directory. From the
repository root, launch the mathbox runner with an argv list rather than
shell interpolation:

```python
import json, subprocess
from pathlib import Path
root = Path('/Users/carlzimmerman/new_physics/zimmerman-formula')
lane = 'fine_structure_puzzle/qcd_nonborn_vacuum/common_response'
py = '/Users/carlzimmerman/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
skill = '/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit'
contract = json.loads((root/lane/'COMPUTATION_CONTRACT.json').read_text())
argv = [py, skill+'/scripts/run_experiment.py', '--root', str(root),
        '--contract', lane+'/COMPUTATION_CONTRACT.json']
for item in contract['execution_artifacts']:
    argv += ['--input', item]
argv += ['--output', lane+'/run_002', '--result', lane+'/run_002/result.json',
         '--timeout', '30', '--max-output-bytes', '1048576',
         '--max-cpu-seconds', '20', '--max-threads', '1', '--',
         py, lane+'/check_common.py', lane+'/run_002/result.json']
subprocess.run(argv, cwd=root, check=True)
subprocess.run([py, skill+'/scripts/validate_manifest.py',
                lane+'/run_002/manifest.json', '--root', str(root)],
               cwd=root, check=True)
```

No RLIMIT_AS or CPU affinity is requested on macOS. The run has a wall,
CPU and log bound. Success verifies the declared finite assertions only;
read RAW_DERIVATION and SELF_AUDIT for the physical and analytic limits.
