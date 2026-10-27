import argparse,json
from pathlib import Path
import numpy as np,torch
from surface_checked import Surface,solve,transfer_species
from joint import RESERVOIR
class Chemical(Surface):
 def __init__(self,*args,eps=.03,**kw):super().__init__(*args,**kw);self.eps=eps
 def energy(self,z,x):
  E=super().energy(z,x);mass=RESERVOIR*torch.softmax(z,dim=0);rho=mass/self.vol;q=torch.sin(torch.pi*x/2)**2;t=torch.clamp((rho-.001)/.002,0,1);S=t**3*(10-15*t+6*t*t)
  return E-self.eps*torch.sum(mass*q*S)
 def report(self,v):
  r=super().report(v);r['chemical_epsilon']=self.eps;return r
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('boundary_resolution_2026_10_25/run_resolved/checkpoint_1_0.01.json').read_text());out={'runs':[],'checks':[]}
 for eps in [.03,.1,.3]:
  m=Chemical(domain=12,beta=2,K=30,charge=0,L=1,eta=3,sigma=.01,spacing=2,eps=eps);m.ell2=(10/m.rm)**2;v,info=transfer_species(m,old);vv=np.r_[np.log(v[:m.n]),v[m.n:]];d=np.cos(np.arange(2*m.n));E,g=m.fg(vv);err=[]
  for dt in [1e-6,3e-7,1e-7]:
   fd=(m.fg(vv+dt*d)[0]-m.fg(vv-dt*d)[0])/(2*dt);err.append(abs(fd-g@d)/max(1,abs(fd)))
  assert max(err)<1e-6;out['checks'].append(err);r=solve(m,v,dest.with_name(f'checkpoint_{eps}.json'),maxiter=2200);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['chemical_epsilon','law_endpoint_error_dex','density_KKT_max','mass_outside50','min_transition_cell_mass','density_rebound_full','explicit_exterior_mass','explicit_exterior_T_fraction','interpolated_crossings_kpc','optimizer']},flush=True)
