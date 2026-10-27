"""Reproduce in a fresh, named bounded-run directory; no existing run overwritten."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--run-name', required=True)
args = parser.parse_args()
if not args.run_name.startswith('run_') or '/' in args.run_name or '..' in args.run_name:
    parser.error('Use a fresh single-component name beginning run_.')
base = Path(__file__).resolve().parent
root = base.parents[2]
relative = base.relative_to(root)
contract = json.loads((base/'contract.json').read_text())
runner = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py')
output = relative/args.run_name
result = output/'results.json'
command = [sys.executable,str(runner),'--root',str(root),'--contract',str(relative/'contract.json')]
for path in contract['execution_artifacts']:
    command += ['--input',path]
command += ['--output',str(output),'--result',str(result),'--timeout','45',
            '--max-cpu-seconds','30','--max-threads','1','--max-output-bytes','131072',
            '--',sys.executable,str(relative/'check_two_mode.py'),'--output',str(result)]
raise SystemExit(subprocess.call(command,cwd=root))
