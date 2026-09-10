#!/usr/bin/env python3
"""Read-only crossover diagnostic from the pinned sector-run output; no data fit."""
import hashlib
import json
import math
from pathlib import Path

source=Path(__file__).resolve().parent/'run_001/results.json'
record=json.loads(source.read_text())
case=next(c for c in record['cases'] if c['name']=='coupled_action')
if case['exit_status'] != 0:
    raise RuntimeError('The input action derivation did not succeed')
result=json.loads(case['stdout'])
rows=[]
for sample in result['tracking_cosh_background_samples']:
    if sample['a'] not in (1e-6,0.001,1.0):
        continue
    A=0.1/sample['a']**3
    Z=math.asinh(A/0.001)
    Q=1+0.001*Z
    B=math.cosh(Z)
    U=1e-5*Q*A
    f=B*Q*U/(2*sample['H2'])
    squared=-sample['e']*f/sample['D']
    if not squared>0:
        raise ArithmeticError('Not on the e<0,D>0 branch')
    rows.append(dict(a=sample['a'],q_mix_over_H=math.sqrt(squared),UV_cs2=sample['cs2']))
print(json.dumps(dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),rows=rows,
                     interpretation='UV speed is not the finite-k growth law or a CMB certificate'),indent=2))
