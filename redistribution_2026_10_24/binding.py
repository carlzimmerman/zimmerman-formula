import argparse,json
from pathlib import Path
import numpy as np,torch
from redistribute import Capillary,transfer_species,polish,RESERVOIR
class Binding(Capillary):
 def __init__(self,*args,eps=0,**kw):super().__init__(*args,L=0,**kw);self.eps=eps
 def energy(self,z,x):
  E=super().energy(z,x);mass=RESERVOIR*torch.softmax(z,dim=0);q=torch.sin(torch.pi*x/2)**2
  return E-self.eps*torch.sum(mass*(4*q*(1-q))**2)
 def report(self,v):
  r=super().report(v);r['binding_epsilon']=self.eps;return r
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('material_interface_2026_10_24/run_final_recovery/base_192.json').read_text());out={'runs':[],'checks':[]}
 for eps in [.01,.03,.1,.3]:
  m=Binding(n=96,domain=12,beta=.5,K=15,charge=0,eps=eps);m.ell2=(10/m.rm)**2;v,info=transfer_species(m,old);E,g=m.direct(v);d=np.sin(np.arange(192));d[:96]*=1e-7;errors=[]
  for dt in [1e-5,3e-6,1e-6]:
   fd=(m.direct(v+dt*d)[0]-m.direct(v-dt*d)[0])/(2*dt);errors.append(abs(fd-g@d)/max(1,abs(fd)))
  assert max(errors)<1e-6;out['checks'].append(errors)
  r=polish(m,v,dest.with_name(f'checkpoint_{eps}.json'),maxiter=1400);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['binding_epsilon','law_endpoint_error_dex','density_KKT_max','explicit_exterior_mass','explicit_exterior_T_fraction','empty_transition_cells','interpolated_crossings_kpc','optimizer']},flush=True)
