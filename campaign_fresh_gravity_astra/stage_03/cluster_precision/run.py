"""Invoke provenance runner with the recorded contract; choose a fresh run name."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent.relative_to(ROOT)
RUN = BASE/(sys.argv[1] if len(sys.argv)>1 else 'run_002')
contract = json.loads((ROOT/BASE/'contract.json').read_text())
argv = [sys.executable,
        '/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/run_experiment.py',
        '--root', str(ROOT), '--contract', str(BASE/'contract.json'), '--output', str(RUN),
        '--timeout', '120', '--max-output-bytes', '1048576', '--max-cpu-seconds', '100', '--max-threads', '1']
for path in contract['execution_artifacts']:
    argv += ['--input', path]
for name in ['shell_constraints.csv', 'shared_nuisance.csv', 'flow_bounds.csv', 'continuity_intervals.csv', 'checks.json']:
    argv += ['--result', str(RUN/name)]
argv += ['--', sys.executable, str(BASE/'constraint.py'), '--out', str(RUN)]
raise SystemExit(subprocess.run(argv, cwd=ROOT).returncode)
