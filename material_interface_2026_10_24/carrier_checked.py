"""Material-supported interface capacity; all forces differentiated from energy."""
import sys,json,argparse
from pathlib import Path
import numpy as np
import torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'live_density_interface_2026_10_24'))
from stable_compatible import Stable
from joint import RESERVOIR
from conservative_radius import transfer_species
from pressure_refine import extended
from stable_recovery import cross
class Carrier(Stable):
    def __init__(self,*args,charge=0,rhos=.01,**kwargs):
        super().__init__(*args,k=0,tau=0,**kwargs);self.charge=charge;self.rhos=rhos
    def capacity(self,z,x):
        m=RESERVOIR*torch.softmax(z,dim=0);rho=m/self.vol;q=torch.sin(torch.pi*x/2)**2;u=self.A@(m*q)
        # Harmonic mean: a vacuum cell cannot borrow a neighbouring cell's carrier.
        rhoedge=2*rho[1:]*rho[:-1]/(rho[1:]+rho[:-1]+1e-100)
        f=rhoedge/(rhoedge+self.rhos);ff=self.functions((u[1:]+u[:-1])/2)[1]
        dq=q[1:]-q[:-1];reg=self.delta*self.dr
        soft=dq*dq/(torch.sqrt(dq*dq+reg*reg)+reg)
        return torch.sum(self.rf**2*ff*f*soft)
    def energy(self,z,x):
        E=super().energy(z,x)
        if self.charge: E=E+self.charge/(self.capacity(z,x)+1e-30)
        return E
    def report(self,v):
        r=super().report(v);r.update(charge=self.charge,rhos=self.rhos)
        rad=np.array(r['r']);mass=np.array(r['mass']);q=np.array(r['q']);gap=(rad>=17)&(rad<=43)
        r['gap_mass']=float(sum(mass[gap]));r['gap_T_mass']=float(mass[gap]@q[gap]);r['capacity']=float(self.capacity(torch.tensor(v[:self.n]),torch.tensor(v[self.n:])))
        return cross(extended(r))
def checks():
    m=Carrier(n=32,charge=.3,beta=20,K=3);v=m.start(scale=8);v[m.n:]=np.linspace(.85,.05,m.n);d=np.cos(np.arange(2*m.n));d[:m.n]*=1e-6
    E,g=m.direct(v);errors=[]
    for eps in [1e-5,3e-6,1e-6]:
        fd=(m.direct(v+eps*d)[0]-m.direct(v-eps*d)[0])/(2*eps);errors.append(abs(fd-g@d)/max(1,abs(fd)))
    assert max(errors)<1e-7
    return {'gradient_errors':errors}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();dest=Path(args.output)
    old=json.loads(Path('live_density_interface_2026_10_24/run_stable_recovery/results.json').read_text())['refinement'][0]
    out={'checks':checks(),'runs':[]}
    for charge in [0,.003,.03,.3,3]:
        model=Carrier(n=64,domain=4,beta=20,K=3,charge=charge);v,info=transfer_species(model,old);assert min(model.cap(v))>0
        r=model.solve_checkpointed(v,dest.with_name('checkpoint_'+str(charge)+'.json'),maxiter=1200);r['transfer']=info;out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n')
        print({k:r[k] for k in ['charge','gap_mass','gap_T_mass','law_windows_dex','qouter','density_KKT_max','interpolated_crossings_kpc','optimizer']},flush=True)
