"""Analyze only completed final-branch records; retain inner-region diagnostics."""
import json
import sys
from pathlib import Path
import numpy as np
from capture_v4 import Capture,local_moments

p=Path(__file__).resolve().parent
names=['scan_v4','seed_v4','packets_v4','controls_v4','followups_v4','radiative','radiative_seed','radiative_long','radiative_packets']
rows=[]
for name in names:
    source=p/('run_'+name)
    manifest=json.loads((source/'manifest.json').read_text())
    if manifest['run']['status']!='completed':raise RuntimeError('unfinished batch '+name)
    data=json.loads((source/'results.json').read_text())
    for row in data['runs']:
        if row['status']!='completed':
            rows.append(dict(source=name,status=row['status']));continue
        m=Capture(row['mass_msun'],row['b_kpc'],n=row['n'],f=row['f'],flat=row['flat'],
                  beta=row['beta'],seed=row['seed'],soft=row['soft'])
        x=np.array(row['final_positions']);v=np.array(row['final_velocities']);state=np.array(row['final_states'])
        S,_,rel,R=m.basis(x);radius=np.linalg.norm(rel,axis=1);half=np.median(radius[:m.n])
        inner={}
        for factor in (1,2):
            a=np.clip((factor*half/R-.75)/.5,0,1)
            kernel=a**3*(10+a*(-15+6*a))
            b=float(kernel[:m.n]@m.m[:m.n]);T=float(kernel@(m.m*state));D=float(kernel[m.n:]@m.m[m.n:])
            inner[str(factor)]=dict(tethered_fraction=T/max(D,1e-30),free_per_baryon=(D-T)/max(b,1e-30))
        clean={k:z for k,z in row.items() if k not in ('history','final_positions','final_velocities','final_states')}
        clean.update(source=name,inner=inner)
        hs=[local_moments(x[i],x[:m.n],v[:m.n],m.m[:m.n])['h']/half for i in range(m.n,2*m.n)]
        clean['neighborhood_h_over_half_median']=float(np.median(hs))
        rows.append(clean)
good=[r for r in rows if 'final'in r]
summary=dict(rows=rows,completed=len(good),
    max_energy_error=max(r['max_energy_error'] for r in good),
    max_angular_error=max(r['max_angular_momentum_error'] for r in good),
    max_reaction_energy_error=max(r['stats']['event_energy_error'] for r in good),
    max_global_T=max(r['final']['q'] for r in good),
    max_inner_T=max(r['inner']['1']['tethered_fraction'] for r in good),
    min_RAR_residual=min(r['final']['rar_max_dex'] for r in good))
Path(sys.argv[1]).write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='rows'},indent=2))
