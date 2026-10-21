#!/usr/bin/env python3
"""Replay the new computations without historical source trees or network.

Run: python3 core_open_problems_2026_10_20/verify_bundle.py
Only verification.json is written into the bundle; scratch results use a tempdir.
This checks implementation reproducibility, not the four physical-origin claims.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare(a, b, path='result'):
    """Compare mathematical output; tolerate only float rounding, never a zero.

    Original software metadata and numerical residual diagnostics are retained
    in the historical results. Check names and pass flags are compared instead
    of requiring diagnostics to be bit-identical across numeric libraries.
    """
    if isinstance(a, bool) or isinstance(b, bool):
        assert type(a) is type(b) and a == b, path
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if a == 0 or b == 0:
            assert a == b, (path, a, b)
        else:
            assert math.isclose(a, b, rel_tol=1e-10, abs_tol=0), (path, a, b)
    elif isinstance(a, dict) and isinstance(b, dict):
        assert set(a) == set(b), (path, set(a) ^ set(b))
        for key in a:
            compare(a[key], b[key], path + '.' + key)
    elif isinstance(a, list) and isinstance(b, list):
        assert len(a) == len(b), path
        for i, (aa, bb) in enumerate(zip(a, b)):
            compare(aa, bb, path + '[' + str(i) + ']')
    else:
        assert a == b, (path, a, b)


def mathematical_view(data):
    data = dict(data)
    data.pop('software', None)
    data.pop('sympy_version', None)
    if 'checks' in data:
        checks = data['checks']
        if isinstance(checks, dict):
            assert all(x['passed'] for x in checks.values())
            data['checks'] = {k: v['passed'] for k, v in checks.items()}
        elif checks and isinstance(checks[0], dict):
            assert all(x['passed'] for x in checks)
            data['checks'] = [{'name': x['name'], 'passed': x['passed']} for x in checks]
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', type=Path, default=ROOT / 'verification.json')
    args = parser.parse_args()
    receipt = {
        'started_at_utc': datetime.now(timezone.utc).isoformat(),
        'python': platform.python_version(),
        'packages': {n: importlib.metadata.version(n) for n in ['sympy', 'mpmath', 'numpy', 'scipy']},
        'scope': 'portable replay and comparison of new mathematical outputs',
        'comparison': 'same assertions; mathematical floats relative 1e-10, no absolute zero tolerance; original software metadata and residual diagnostics excluded',
        'runs': [],
    }
    specs = [
        ('horizon', '01_horizon/check_horizon.py', ['{tmp}/horizon.json'], 'horizon.json', '01_horizon/run_002/results.json'),
        ('medium', '02_medium/check_medium.py', ['{tmp}/medium'], 'medium/results.json', '02_medium/run_002/results.json'),
        ('medium_stiffness', '02_medium/stiffness_addendum.py', ['{tmp}/medium_stiffness'], 'medium_stiffness/results.json', '02_medium/run_stiffness/results.json'),
        ('relativity', '03_relativity/checks.py', ['--output', '{tmp}/relativity.json'], 'relativity.json', '03_relativity/run_001/results.json'),
        ('stiffness', '04_stiffness/scripts/run_checks.py', ['--output-dir', '{tmp}/stiffness'], 'stiffness/checks.json', '04_stiffness/results/checks.json'),
        ('independent_review', '05_independent_review/check_independent.py', ['{tmp}/independent.json'], 'independent.json', '05_independent_review/results.json'),
        ('coordinator', 'review_checks.py', ['--output', '{tmp}/coordinator.json'], 'coordinator.json', 'review_results.json'),
    ]
    with tempfile.TemporaryDirectory(prefix='core-theory-verification-') as td:
        for name, script_name, argv, output, expected in specs:
            script = ROOT / script_name
            expected_path = ROOT / expected
            before = sha(script)
            command = [sys.executable, str(script)] + [v.format(tmp=td) for v in argv]
            start = time.perf_counter()
            result = subprocess.run(command, capture_output=True, text=True, timeout=120)
            if result.returncode:
                raise RuntimeError(name + '\n' + result.stdout[-4000:] + '\n' + result.stderr[-4000:])
            actual = json.loads((Path(td) / output).read_text())
            saved = json.loads(expected_path.read_text())
            compare(mathematical_view(saved), mathematical_view(actual), name)
            assert before == sha(script), name + ': script changed during run'
            receipt['runs'].append({
                'name': name, 'script': script_name, 'script_sha256': before,
                'arguments': argv, 'exit_status': result.returncode,
                'runtime_seconds': round(time.perf_counter() - start, 6),
                'reference_result': expected, 'reference_result_sha256': sha(expected_path),
                'mathematical_outputs_match': True,
                'original_software': saved.get('software', saved.get('sympy_version')),
            })
            print(name + ': passed; mathematical outputs match', flush=True)
    receipt['status'] = 'completed'
    receipt['physical_origin_goals'] = 'remain open; see reports and REVIEW.md'
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + '\n')
    print('Verification receipt: ' + str(args.receipt), flush=True)


if __name__ == '__main__':
    main()
