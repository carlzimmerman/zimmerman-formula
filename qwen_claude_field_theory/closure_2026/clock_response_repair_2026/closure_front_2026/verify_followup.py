#!/usr/bin/env python3
"""Bounded verification, not theory certification. No downloads/builds."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    front = Path(__file__).resolve().parent
    here = front/'disformal_cone'
    root = front.parents[3]
    lean = root/'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026'
    out = args.output.resolve()
    if root not in out.parents:
        raise ValueError('output must be inside repository')
    out.mkdir(exist_ok=False)
    paths = [front/'principal_gate/principal_gate.py', front/'principal_gate/test_principal.py', front/'principal_gate/first_derivative_variation.py',
             front/'metric_response/derive_static_metric.py', front/'spherical_branch/derive_spherical.py',
             front/'boosted/derive_boosted.py', front/'boosted/test_boosted.py',
             front.parent/'mond_braiding_completion/derive.py',
             front/'health/pressure/audit_pressure.py',
             front/'principal_gate/ResponseGate.lean', front/'spherical_branch/SphericalScaling.lean',
             here/'derive_cone.py', here/'test_cone.py', here/'DisformalCone.lean',
             front/'boosted/tensor_cone.py', front/'nonlinear_clock/derive_nonlinear_clock.py',
             front/'critical_radial/derive_critical.py', front/'critical_radial/CriticalRadial.lean']
    env = dict(os.environ, PYTHONOPTIMIZE='0', PYTHONDONTWRITEBYTECODE='1',
               OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    guard = subprocess.run([sys.executable, '-B', '-c',
                            "import sys; assert sys.flags.optimize == 0; assert False, 'negative control'"],
                           env=env, cwd=root, capture_output=True, text=True, timeout=10)
    if guard.returncode == 0 or 'negative control' not in guard.stderr:
        raise RuntimeError('assertion negative control did not fail as required')
    def execute(path):
        islean = path.suffix == '.lean'
        argv = ['/opt/homebrew/bin/lake','env','lean',str(path)] if islean else [sys.executable,'-B',str(path)]
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        start = time.monotonic()
        try:
            proc = subprocess.run(argv, cwd=lean if islean else root, env=env,
                                  capture_output=True, text=True, timeout=90)
            code, stdout, stderr = proc.returncode, proc.stdout, proc.stderr
        except subprocess.TimeoutExpired:
            code, stdout, stderr = 124, '', 'per-command timeout at 90 seconds'
        after = hashlib.sha256(path.read_bytes()).hexdigest()
        name = path.parent.name+'_'+path.stem
        (out/(name+'.stdout.txt')).write_text(stdout)
        (out/(name+'.stderr.txt')).write_text(stderr)
        axiom_sets = [set(x.strip() for x in row.split(',')) for row in
                      re.findall(r'depends on axioms: \[([^]]*)\]', stdout)] if islean else []
        proof_ok = bool(axiom_sets) and all(x <= {'propext','Classical.choice','Quot.sound'} for x in axiom_sets)
        ok = code == 0 and before == after and (not islean or proof_ok)
        print(name, 'exit', code, 'checked', ok, flush=True)
        return dict(argv=argv, cwd=str(lean if islean else root), exit_status=code, checked_ok=ok,
                    elapsed_seconds=time.monotonic()-start, sha256_before=before, sha256_after=after,
                    axioms=[sorted(x) for x in axiom_sets])
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(execute, paths))
    summary = dict(scope='Local nonlinear clock, critical radial, disformal cone, earlier regression, bounded Lean lemmas only',
                   full_theory_status='OPEN',
                   negative_control=dict(exit_status=guard.returncode, stderr=guard.stderr),
                   numerical_thread_cap=1, worker_cap=2, timeout_seconds_per_command=90,
                   results=results, all_checked=all(row['checked_ok'] for row in results))
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return 0 if summary['all_checked'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

