#!/usr/bin/env python3
"""Reproduce all evidence; any failed check or Lean warning is fatal."""
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
for script in ['verify.py', 'verify_global_qumond.py']:
    subprocess.run([sys.executable, str(HERE/script), str(OUT)], check=True)
lean_cwd = ROOT/'fable_independent_2026/lean_2026'
proc = subprocess.run(['lake', 'env', 'lean', str(HERE/'TailAlgebra.lean')],
                      cwd=lean_cwd, text=True, capture_output=True)
(OUT/'lean.txt').write_text(proc.stdout+proc.stderr)
assert proc.returncode == 0, proc.stdout+proc.stderr
assert 'warning:' not in proc.stdout+proc.stderr, proc.stdout+proc.stderr
assert 'sorryAx' not in proc.stdout+proc.stderr
assert proc.stdout.count('depends on axioms:') == 8, proc.stdout
version = subprocess.run(['lake', 'env', 'lean', '--version'], cwd=lean_cwd,
                         text=True, capture_output=True, check=True).stdout.strip()
result = json.loads((OUT/'result.json').read_text())
global_result = json.loads((OUT/'global_qumond.json').read_text())
summary = {'status': 'passed', 'exact_symbolic_checks': result['exact_check_count'],
           'aqual_nonlinear_residual_cases': len(result['nonlinear_residual_cases']),
           'qumond_nonlinear_residual_cases': len(result['qumond_residual_cases']),
           'second_order_compact_source_cases': len(result['compact_source_cases']),
           'global_qumond_cases': global_result['case_count'],
           'global_qumond_largest_radius_max_error': global_result['largest_radius_max_error'],
           'lean_theorems': 8, 'lean_version': version,
           'qualification': 'conditional asymptotic coefficient; no general AQUAL existence theorem or observations'}
(OUT/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
print(json.dumps(summary, indent=2))
