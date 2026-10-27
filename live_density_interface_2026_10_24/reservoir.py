"""LD-5: reservoir entropy and resolved core, physical branch up to .9997."""
import argparse,json
from pathlib import Path
import numpy as np
import torch
from constrained import Constrained
from warm import Warm
from joint import RESERVOIR

class Reservoir(Warm):
    def __init__(self,*args,**kwargs):Constrained.__init__(self,*args,**kwargs)
    def functions(self,u):
        c=.9999;v=torch.clamp(u,max=c);d=u-v
        return (-torch.log1p(-v)-v+d*c/(1-c)+.5*d*d/(1-c)**2,
                v*v/(1-v)+d*c*(2-c)/(1-c)**2+d*d/(1-c)**3)
    def cap(self,v):return super().cap(v)+.0297
    def transfer(self,old):
        ro=np.array(old['r'])/self.rm;edges=np.r_[0,(ro[:-1]+ro[1:])/2,old['R_kpc']/self.rm]
        new=self.R*np.linspace(0,1,self.n+1)**2;cum=np.interp(new,edges,np.r_[0,np.cumsum(old['mass'])]);mass=np.maximum(np.diff(cum),1e-12);mass*=RESERVOIR/sum(mass)
        x=np.interp(self.r.numpy()*self.rm,old['r'],old['v'][old['n']:]);return np.r_[mass,x]

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();base=json.loads(Path(__file__).with_name('run_warm').joinpath('results.json').read_text())['runs'][1];out=dict(runs=[])
    for K in [3,10,30]:
        m=Reservoir(n=128,domain=4,beta=1000,k=120,tau=1,K=K);r=m.solve_scaled(m.transfer(base));out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['v','r','mass','q','g_total','g_law']},flush=True)
