import argparse,json
from pathlib import Path
import numpy as np
from tension_charge import TensionCharge
from tension_refine import diagnostic
from stress_test import stress_bound
from refine import polish

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();rows=json.loads(Path(__file__).with_name('run_traction').joinpath('results.json').read_text())['runs'];prev=next(r for r in rows if r['k']==120 and r['tau']==1);out=dict(runs=[],recovery=[])
    for n,delta in [(512,1e-5),(512,1e-6),(1024,1e-6)]:
        m=TensionCharge(6e10,3,n,120,delta,beta=1000,tau=1);x,op=polish(m,np.interp(m.r*m.rm,prev['r'],prev['x']));r=diagnostic(m,x);r['stress']=stress_bound(m,x);out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['x','r','force_T','force_F']},flush=True);prev=r
    for displacement in [-.2,.2]:
        xp,op=polish(m,np.interp(m.r*m.rm+displacement,m.r*m.rm,x));d=diagnostic(m,xp);d.update(displacement_kpc=displacement,max_phase_difference=float(max(abs(xp-x))),energy_difference=float(d['energy']-prev['energy']),stress=stress_bound(m,xp));out['recovery'].append(d);Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
