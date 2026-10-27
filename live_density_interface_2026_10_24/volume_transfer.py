"""LD-6: fix mesh-transfer density singularity before interpreting LD-5."""
import argparse,json
from pathlib import Path
import numpy as np
from reservoir import Reservoir
from joint import RESERVOIR

class VolumeTransfer(Reservoir):
    def transfer(self,old):
        ro=np.array(old['r'])/self.rm
        # Source LD-3 uses uniform cells; exact edges are known.
        edges=np.linspace(0,old['R_kpc']/self.rm,old['n']+1)
        new=self.R*np.linspace(0,1,self.n+1)**2
        cum=np.interp(new**3,edges**3,np.r_[0,np.cumsum(old['mass'])]);mass=np.maximum(np.diff(cum),1e-12);mass*=RESERVOIR/sum(mass)
        x=np.interp(self.r.numpy()*self.rm,old['r'],old['v'][old['n']:]);return np.r_[mass,x]

def checks():
    # An exactly constant density transfers to arbitrary radial cell volumes.
    oldedges=np.linspace(0,2,17);newedges=2*np.linspace(0,1,33)**2
    c=np.interp(newedges**3,oldedges**3,oldedges**3)
    error=max(abs(np.diff(c)-np.diff(newedges**3)));assert error<1e-14
    return dict(uniform_density_transfer_error=float(error))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();base=json.loads(Path(__file__).with_name('run_warm').joinpath('results.json').read_text())['runs'][1];out=dict(checks=checks(),runs=[])
    for K in [3,10,30]:
        m=VolumeTransfer(n=128,domain=4,beta=1000,k=120,tau=1,K=K);v=m.transfer(base);slack=float(min(m.cap(v)))
        assert slack>0,('infeasible transferred start',slack)
        r=m.solve_scaled(v);r['initial_cap_slack']=slack;out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['v','r','mass','q','g_total','g_law']},flush=True)
