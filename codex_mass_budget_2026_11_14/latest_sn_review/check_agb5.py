"""Read-only independent plain WLS check on snapshots of the live AGB5 table."""
import json
import re
import sys
from pathlib import Path
import numpy as np

P=Path(__file__).resolve().parent/'inputs'
with (P/'sdsssn_master.dat2').open() as f:
    header=f.readline().split()
    k=max(j for j,x in enumerate(header) if x=='logMass_Ravi')
    mass={r[0]:float(r[k]) if r[k]!='\\N' else np.nan for r in (l.split() for l in f if l.strip())}
reference=json.loads((P/'agb5/agb5_results_boot.json').read_text())
out={'tables':{}}
for which in (1,2):
    rows=[]
    for line in (P/f'agb5/table{which}.dat').read_text().splitlines():
        values=[v.strip().rstrip('\\').strip() for v in line.split('&')]
        if len(values)!=5 or not values[0].isdigit(): continue
        rows.append((values[0],float(values[1]),float(re.match(r'^[-\d.]+',values[3])[0]),float(values[4])))
    ids=[r[0] for r in rows]
    age=np.array([r[1] for r in rows]); y=np.array([r[2] for r in rows]); err=np.array([r[3] for r in rows]); lm=np.array([mass[i] for i in ids])
    fits={}
    for step in (False,True):
        sel=np.isfinite(lm) if step else np.ones(len(rows),bool)
        x=np.column_stack([np.ones(sel.sum()),age[sel]]+[(lm[sel]<10)-0.5] if step else [np.ones(sel.sum()),age[sel]])
        sw=1/np.sqrt(err[sel]**2+.01); xx=x*sw[:,None]; yy=y[sel]*sw
        b=np.linalg.lstsq(xx,yy,rcond=None)[0]; _,r=np.linalg.qr(xx,mode='reduced'); ri=np.linalg.inv(r); cv=ri@ri.T
        result=dict(n=int(sel.sum()),beta=float(b[1]),sd_beta_formula=float(np.sqrt(cv[1,1])),A=float(-b[1]/.03))
        if step: result['g']=float(b[2])
        ref=reference['L1']['fit'][f'table{which}'] if step else reference['reported'][f'table{which}']['no_step']
        result['difference_beta_from_stored']=result['beta']-ref['beta']
        assert abs(result['difference_beta_from_stored'])<1e-10
        fits['step' if step else 'no_step']=result
    out['tables'][f'table{which}']=fits
out['combination_using_stored_bootstrap_errors']={}
weights=np.array([1/reference['L1']['fit'][f'table{i}']['sd_beta']**2 for i in (1,2)])
beta=np.array([out['tables'][f'table{i}']['step']['beta'] for i in (1,2)])
a=-np.average(beta,weights=weights)/.03; sd=1/np.sqrt(weights.sum())/.03
out['combination_using_stored_bootstrap_errors']=dict(A=float(a),sd_A=float(sd),D_A0=float((a/sd)**2),D_A1=float(((a-1)/sd)**2))
out['scope']='Independent parser and WLS slopes; combined arithmetic checked with stored bootstrap errors. Bootstrap and structural optimizations not rerun.'
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
