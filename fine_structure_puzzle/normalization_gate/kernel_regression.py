#!/usr/bin/env python3
"""Exact regression for partial masslessness in three gauge fields."""
import argparse
import json
from pathlib import Path
import sympy as s

p = argparse.ArgumentParser()
p.add_argument('--output', required=True)
args = p.parse_args()
z = s.symbols('z', positive=True)
N = s.Matrix([[1, 0], [0, 1], [0, 0]])
M = s.diag(0, 0, 1)
q = s.Matrix([1, 1, 1])
rows = []
for name, K in [('identity', s.eye(3)), ('mixed', s.Matrix([[2, 1, 1], [1, 3, 0], [1, 0, 4]]))]:
    assert all(K[:i, :i].det() > 0 for i in (1, 2, 3))
    pole = (z*K+M).inv().applyfunc(lambda f: s.limit(z*f, z, 0, dir='+'))
    predicted = N*(N.T*K*N).inv()*N.T
    assert pole == predicted
    residue, wrong = (q.T*pole*q)[0], (q.T*K.inv()*q)[0]
    assert residue != wrong
    rows.append({'case': name, 'pole_norm': str(residue), 'all_massless_norm': str(wrong)})
assert rows[0]['pole_norm'] == '2' and rows[0]['all_massless_norm'] == '3'
assert rows[1]['pole_norm'] == '3/5'
Path(args.output).write_text(json.dumps({'claim_id': 'FSP-N-KERNEL', 'checks_passed': True,
    'assertion_tested': 'Two exact 3x3 cases, rank-two massless kernel; distinguishes all-massless inverse from projected inverse.',
    'non_claim': 'Finite checks do not replace the projection proof.', 'cases': rows}, indent=2)+'\n')
print(json.dumps(rows))
