"""LD-8: conserve both species during transfer and verify feasible starts."""
import argparse,json
from pathlib import Path
import numpy as np
from reservoir import Reservoir
from joint import RESERVOIR

def transfer_species(m,old):
    r=np.array(old['r'])/m.rm;edges=[0.]
    for ri in r:edges.append(2*ri-edges[-1])
    edges=np.array(edges);assert abs(edges[-1]-old['R_kpc']/m.rm)<1e-8
    source=np.array(old['mass']);q=np.array(old['q']);new=m.R*np.linspace(0,1,m.n+1)**2
    for dilation in [1.,1.05,1.1,1.2,1.4]:
        parts=[]
        for frac in [q,1-q]:
            c=np.interp(new**3,(edges*dilation)**3,np.r_[0,np.cumsum(source*frac)])
            parts.append(np.maximum(np.diff(c),0))
        total=parts[0]+parts[1]
        if abs(sum(total)-RESERVOIR)>1e-7:continue
        ratio=np.divide(parts[0],total,out=np.zeros_like(total),where=total>1e-14)
        total=np.maximum(total,1e-12);total*=RESERVOIR/sum(total)
        x=2/np.pi*np.arcsin(np.sqrt(np.clip(ratio,0,1)));v=np.r_[total,x]
        if min(m.cap(v))>1e-4:
            return v,dict(dilation=dilation,T_mass_error=float(abs(sum(total*ratio)-sum(source*q))),F_mass_error=float(abs(sum(total*(1-ratio))-sum(source*(1-q)))),initial_cap_slack=float(min(m.cap(v))))
    raise ValueError('no feasible conservative transferred start')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();old=json.loads(Path(__file__).with_name('run_warm').joinpath('results.json').read_text())['runs'];out=dict(runs=[])
    for tau in [.1,.03]:
        for source in [0,1]:
            m=Reservoir(n=128,domain=4,beta=1000,k=120,tau=tau,K=3);v,check=transfer_species(m,old[source]);r=m.solve_scaled(v);r.update(source_index=source,transfer=check);out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['v','r','mass','q','g_total','g_law']},flush=True)
