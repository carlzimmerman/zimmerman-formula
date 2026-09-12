#!/usr/bin/env python3
"""Archive bounded independent symbolic and Lean runs in fresh directories."""
import argparse
import json
from pathlib import Path
import shlex
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = next(path for path in HERE.parents if (path/'.git').exists())
AUDIT = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts')
LEAN = ROOT/'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026'


def bounded(contract, output, command, results=()):
    definition = json.loads(contract.read_text())
    argv = [sys.executable, str(AUDIT/'run_experiment.py'), '--root', str(ROOT),
            '--contract', str(contract.relative_to(ROOT)), '--output', str(output.relative_to(ROOT)),
            '--timeout', '90', '--max-output-bytes', '1048576', '--max-threads', '1']
    for path in definition['execution_artifacts']:
        argv += ['--input', path]
    for path in results:
        argv += ['--result', str(path.relative_to(ROOT))]
    subprocess.run(argv+['--']+command, cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(AUDIT/'validate_manifest.py'),
                    str(output/'manifest.json'), '--root', str(ROOT)], cwd=ROOT, check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', default='001')
    args = parser.parse_args()
    if not args.tag.isalnum():
        raise ValueError('tag must be alphanumeric')
    review = HERE/'review'/('run_'+args.tag)
    bounded(HERE/'review/contract.json', review,
            [sys.executable, '-B', str(HERE/'review/derive_audit.py'), '--output',
             str(review/'result.json')], [review/'result.json'])
    bounded(HERE/'lean_contract.json', HERE/('lean_'+args.tag),
            ['/bin/bash', '-c', 'cd '+shlex.quote(str(LEAN))+
             ' && /opt/homebrew/bin/lake env lean '+shlex.quote(str(HERE/'ClockElimination.lean'))])
