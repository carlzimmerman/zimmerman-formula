#!/usr/bin/env python3
"""Summarize executed checks without promoting estimates to full claims."""
import hashlib
import json
from pathlib import Path
import platform
import numpy
import scipy
import sympy
HERE=Path(__file__).resolve().parent
def read(name):return json.loads((HERE/name).read_text())
bh=read('main/black_holes.json');coupling=read('main/coupling.json')
main=read('main/structural_results.json');mut=read('mutate/structural_results.json')
metrics={}
for foot,rows in bh['footings'].items():
    metrics[foot]=dict(bh_members=len(rows),
        bh_failed_checks={k:[n for n,v in r['checks'].items() if not v] for k,r in rows.items() if not all(r['checks'].values())},
        bh_max_relative_change=max(r['convergence_relative'] for r in rows.values()),
        bh_max_shift=max(v for r in rows.values() for v in r['fine']['shifts'].values()),
        bh_min_divergence=min(r['fine']['min_divergence'] for r in rows.values()),
        coupling_max_eps=max(r['eps_max'] for k,r in coupling['footings'][foot].items() if '|L90.0|' not in k),
        pulsar_max_leakage_estimate=max(r['energy_leakage_estimate'] for k,r in coupling['footings'][foot].items() if k.startswith('double pulsar') and '|L90.0|' not in k))
checks=dict(bh_complete_30_members_each=all(m['bh_members']==30 for m in metrics.values()),
    bh_known_answers=all(bh['checks'].values()),
    coupling_checks=all(coupling['checks'].values()),
    gr_control=all(read('main/gr_control.json')['checks'].values()),
    switch_inverted_control_bites=main['checks']['nonnegative_principal_sound_speed'] and not mut['checks']['nonnegative_principal_sound_speed'],
    penalty_control_bites=main['checks']['leaf_uniform_energy_bound'] and not mut['checks']['leaf_uniform_energy_bound'])
labels={'binary_pulsars':'NO VERDICT full radiation',
        'leaf':'UNDECIDED full well-posedness',
        'causality':'NO VERDICT gauge-invariant retarded response',
        'strong_coupling':coupling['label'],
        'G9':'PASS matter-shell identity; off-shell-zero wording false',
        'black_holes':bh['label']}
inputs={str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.rglob('*.json') if p.name!='results.json'}
result=dict(labels=labels,metrics=metrics,checks=checks,
    original_structural_failures=[k for k,v in main['checks'].items() if not v],
    inputs=inputs,software=dict(python=platform.python_version(),numpy=numpy.__version__,scipy=scipy.__version__,sympy=sympy.__version__),
    statement='kappa = 1/2 FITTED; not theory closed')
(HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(labels=labels,metrics=metrics,checks=checks),indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
