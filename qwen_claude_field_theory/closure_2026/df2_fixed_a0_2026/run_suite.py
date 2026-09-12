#!/usr/bin/env python3
"""Run and archive the bounded DF2 checks; never overwrites an existing result."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'.git').exists())
OLD = HERE.parent/'exact_exponential_aqual_efe_kepler_2026'


def main(output):
    output.mkdir(parents=True, exist_ok=True)
    # The enclosing bounded runner creates an empty run directory first.
    labels = ('unit_static', 'unit_stellar', 'existing_efe', 'stellar_reference',
              'independent_audit', 'nonlinear_study')
    if any((output/(label+'.stdout.txt')).exists() for label in labels):
        raise FileExistsError('Use a fresh output directory')
    commands = [
        [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', str(HERE), '-p', 'test_*.py', '-v'],
        [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', str(HERE/'stellar'), '-p', 'test_profile.py', '-v'],
        [sys.executable, '-B', str(OLD/'test_exact_exponential_aqual_efe_kepler_2026.py')],
        [sys.executable, '-B', str(HERE/'stellar/run_checks.py')],
        [sys.executable, '-B', str(HERE/'bridge/audit_solver.py')],
        [sys.executable, '-B', str(HERE/'study.py'), '--output', str(output/'study.json')],
    ]
    records = []
    for label, command in zip(labels, commands):
        started = time.monotonic()
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=180)
        (output/(label+'.stdout.txt')).write_text(result.stdout)
        (output/(label+'.stderr.txt')).write_text(result.stderr)
        record = dict(label=label, argv=command, cwd=str(ROOT), exit_status=result.returncode,
                      runtime_seconds=time.monotonic()-started)
        records.append(record)
        print(json.dumps(record), flush=True)
    summary = dict(status='NUMERICAL_CHECKS_ONLY' if all(r['exit_status']==0 for r in records) else 'FAIL',
                   commands=records, empirical_pass=None, lean_certificate=None)
    (output/'suite.json').write_text(json.dumps(summary, indent=2, allow_nan=False)+'\n')
    return 0 if all(r['exit_status']==0 for r in records) else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(main(args.output.resolve()))
