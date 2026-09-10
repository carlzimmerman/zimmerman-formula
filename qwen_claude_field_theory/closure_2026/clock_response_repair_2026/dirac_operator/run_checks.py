#!/usr/bin/env python3
"""Record exact commands and actual exits; an unbuilt Lean draft is NOT a pass."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
LEAN = HERE.parents[1] / 'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--result-file', type=Path, required=True)
    a = p.parse_args()
    out = a.result_file.parent
    cases = [
        ('canonical_operator', [sys.executable, '-B', str(HERE/'sample_operator.py'), '--result-file', str(out/'operator.json')], ROOT, 240),
        ('constraint_surface', [sys.executable, '-B', str(HERE/'constraint_data.py'), '--result-file', str(out/'constraints.json')], ROOT, 90),
        ('DiracKernel.lean', ['lake', 'env', 'lean', str(HERE/'DiracKernel.lean')], LEAN, 90),
        ('CoerciveInverse.lean_DRAFT', ['lake', 'env', 'lean', str(HERE/'CoerciveInverse.lean')], LEAN, 90),
        ('stationary_action_regression', [sys.executable, '-B', str(HERE.parent/'nonlinear_transport/stationary.py'), '--result-file', str(out/'stationary.json')], ROOT, 120),
        ('Stationarity.lean_regression', ['lake', 'env', 'lean', str(HERE.parent/'nonlinear_transport/Stationarity.lean')], LEAN, 90),
    ]
    records = []
    for name, argv, cwd, limit in cases:
        try:
            r = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=limit)
            row = dict(name=name, argv=argv, cwd=str(cwd.relative_to(ROOT)), exit_status=r.returncode, stdout=r.stdout, stderr=r.stderr)
        except subprocess.TimeoutExpired:
            row = dict(name=name, argv=argv, cwd=str(cwd.relative_to(ROOT)), exit_status=None, status='timeout')
        records.append(row)
        print(json.dumps(dict(name=name, exit_status=row['exit_status'])), flush=True)
    gates = {}
    if (out/'constraints.json').exists():
        rows = json.loads((out/'constraints.json').read_text())['cases']
        gates['all_eight_solved'] = len(rows) == 8 and all('lowest_eigenvalues' in r for r in rows)
        if gates['all_eight_solved']:
            gates['sampled_regular_positive_branch'] = all(
                min(r['min_X'], r['min_log_domain'], r['min_kinetic'], r['min_principal'], r['min_mass'], r['lowest_eigenvalues'][0]) > 0 for r in rows)
            gates['full_constraint_residuals'] = all(max(r['full_C_residual'], r['full_T_residual'], r['full_momentum_residual']) < (1e-9 if r['modes'] == 16 else 1e-7) for r in rows)
    incomplete = any(r['exit_status'] != 0 for r in records) or not gates or not all(gates.values())
    result = dict(cases=records, finite_gates=gates, full_theory_status='OPEN',
                  suite_status='INCOMPLETE' if incomplete else 'EXECUTION_COMPLETE_NOT_THEORY_CERTIFIED')
    a.result_file.write_text(json.dumps(result, indent=2)+'\n')
    return int(incomplete)


if __name__ == '__main__':
    raise SystemExit(main())
