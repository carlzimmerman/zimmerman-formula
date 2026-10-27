import argparse,json
from pathlib import Path
import numpy as np,torch
from latent_smooth import SmoothLatent
from fast_complete import finish
from surface_checked import transfer_species
from joint import RESERVOIR
class LatentStiff(SmoothLatent):
 def __init__(self,*args,material_length=.5,**kw):super().__init__(*args,**kw);self.material_length=material_length
 def energy(self,z,x):
  E=super().energy(z,x);rho=RESERVOIR*torch.softmax(z,dim=0)/self.vol;a=torch.sqrt(rho)
  return E+.5*(self.material_length/self.rm)**2*torch.sum(self.rf**2/self.dr*(a[1:]-a[:-1])**2)
 def report(self,v):
  r=super().report(v);r['material_length_kpc']=self.material_length;return r
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('boundary_resolution_2026_10_25/run_latent_smooth/base_0.001.json').read_text());out={'runs':[],'checks':[]}
 for L in [.25,.5,1.]:
  m=LatentStiff(domain=12,beta=2,K=30,charge=0,L=0,eta=0,sigma=0,eps=.3,h=.5,volume_cost=.001,material_length=L);m.ell2=(3/m.rm)**2;v,info=transfer_species(m,old);vv=np.r_[np.log(v[:m.n]),v[m.n:]];d=np.cos(np.arange(2*m.n));E,g=m.fg(vv);err=[]
  for dt in [1e-6,3e-7,1e-7]:
   fd=(m.fg(vv+dt*d)[0]-m.fg(vv-dt*d)[0])/(2*dt);err.append(abs(fd-g@d)/max(1,abs(fd)))
  assert max(err)<1e-6;out['checks'].append(err);r=finish(m,v,dest.with_name(f'base_{L}.json'),initial_iterations=80,newton_iterations=80);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['material_length_kpc','law_endpoint_error_dex','density_KKT_max','gradient_max','mass_outside50','density_rebound_full','explicit_exterior_mass','explicit_exterior_T_fraction','interpolated_crossings_kpc','optimizer']},flush=True)
