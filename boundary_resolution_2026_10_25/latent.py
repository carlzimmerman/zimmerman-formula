import argparse,json
from pathlib import Path
import numpy as np,torch
from compact import Compact
from fast_complete import finish
from surface_checked import transfer_species
from mixed_carrier import Mixed
from joint import RESERVOIR
class Latent(Compact):
 def __init__(self,*args,volume_cost=.0003,**kw):
  super().__init__(*args,**kw);self.volume_cost=volume_cost
 def energy(self,z,x):
  # Bypass density gate and constant surface term: retain inherited response wall.
  E=Mixed.energy(self,z,x);mass=RESERVOIR*torch.softmax(z,dim=0);q=torch.sin(torch.pi*x/2)**2
  return E+torch.sum(q*(self.volume_cost*self.vol-self.eps*mass))
 def report(self,v):
  r=super().report(v);r.update(phase_volume_cost=self.volume_cost,model='constant phase volume cost and per-T-particle binding; no density gate or extra stiffness');return r
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('boundary_resolution_2026_10_25/run_compact/checkpoint_0_0.3.json').read_text());out={'runs':[],'checks':[]}
 for B in [.0001,.0003,.001]:
  m=Latent(domain=12,beta=2,K=30,charge=0,L=0,eta=0,sigma=0,eps=.3,h=.5,volume_cost=B);m.ell2=(3/m.rm)**2;v,info=transfer_species(m,old);vv=np.r_[np.log(v[:m.n]),v[m.n:]];d=np.cos(np.arange(2*m.n));E,g=m.fg(vv);err=[]
  for dt in [1e-6,3e-7,1e-7]:
   fd=(m.fg(vv+dt*d)[0]-m.fg(vv-dt*d)[0])/(2*dt);err.append(abs(fd-g@d)/max(1,abs(fd)))
  assert max(err)<1e-6;out['checks'].append(err);r=finish(m,v,dest.with_name(f'base_{B}.json'),initial_iterations=200,newton_iterations=70);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['phase_volume_cost','law_endpoint_error_dex','density_KKT_max','gradient_max','mass_outside50','density_rebound_full','explicit_exterior_mass','explicit_exterior_T_fraction','interpolated_crossings_kpc','optimizer']},flush=True)
