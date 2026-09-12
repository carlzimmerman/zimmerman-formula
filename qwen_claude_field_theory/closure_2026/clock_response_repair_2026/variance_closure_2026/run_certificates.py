#!/usr/bin/env python3
"""Run immutable bounded vertex and Lean evidence; --tag chooses fresh paths."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = next(path for path in HERE.parents if (path/'.git').exists())
SKILL = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit')
LEAN = ROOT/'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026'


def bounded(contract, output, command, results=()):
    relative = lambda p: str(p.relative_to(ROOT))
    definition = json.loads(contract.read_text())
    cmd = [sys.executable, str(SKILL/'scripts/run_experiment.py'), '--root', str(ROOT),
        '--contract', relative(contract), '--output', relative(output),
        '--timeout', '90', '--max-output-bytes', '1048576', '--max-threads', '1']
    for path in definition['execution_artifacts']:
        cmd += ['--input', path]
    for path in results:
        cmd += ['--result', relative(path)]
    subprocess.run(cmd+['--']+command, cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(SKILL/'scripts/validate_manifest.py'),
                    str(output/'manifest.json'), '--root', str(ROOT)], cwd=ROOT, check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', default='001')
    args = parser.parse_args()
    if not args.tag.isalnum():
        raise ValueError('tag must be alphanumeric')
    vertex_output = HERE/'vertices'/('run_'+args.tag)
    bounded(HERE/'vertices/contract.json', vertex_output,
        [sys.executable, '-B', str(HERE/'vertices/vertices.py'), '--result-file',
         str(vertex_output/'result.json')], [vertex_output/'result.json'])
    import shlex
    bounded(HERE/'lean_contract.json', HERE/('lean_'+args.tag),
        ['/bin/bash', '-c', 'cd '+shlex.quote(str(LEAN))+
         ' && /opt/homebrew/bin/lake env lean '+shlex.quote(str(HERE/'VarianceClosure.lean'))])
