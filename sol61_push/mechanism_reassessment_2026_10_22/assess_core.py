"""Frozen 5% finite-time enclosed-mass comparison; not asymptotic binding."""
import json,sys
from pathlib import Path
import numpy as np
p=Path(__file__).parent
names=['collapse_core_compiled_run','collapse_core_512_stream_run','collapse_core_cutoff_run','collapse_core_timecheck_run']
summaries=[]
for name in names:
    data=json.loads((p/name/'results.json').read_text());row=data['rows'][0]
    ss=[s for s in row['samples'] if 20-1e-9<=s['t']<=30+1e-9]
    t=np.array([s['t'] for s in ss])
    means={key:float(np.trapz([s[key] for s in ss],t)/(t[-1]-t[0])) for key in ['mass_inside_3','mass_inside_5']}
    summaries.append(dict(run=name,N=row['N'],epsilon=row['epsilon'],tolerance=row['tolerance'],
        means=means,completed=row['failure'] is None and row['final_time']==30,
        energy_error=row['max_energy_error'],source_checks=data['checks']))
reference=summaries[0]['means']
for r in summaries:
    r['relative_difference']={key:abs(r['means'][key]/reference[key]-1) for key in reference}
checks=dict(completed=all(r['completed'] for r in summaries),
    numerical_controls=all(all(r['source_checks'].values()) for r in summaries),
    finite_time_mass_stability=all(max(r['relative_difference'].values())<.05 for r in summaries[1:]))
out=dict(checks=checks,all_pass=all(checks.values()),rows=summaries,
    scope='Only time-averaged mass within radii3,5 during t20..30, under these numerical controls. No pointwise trajectory convergence, permanent-core mass or asymptotic equilibrium assertion.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
