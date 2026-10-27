import argparse,json
from pathlib import Path
import numpy as np,torch
from redistribute import Capillary,transfer_species,polish,RESERVOIR
class Global(Capillary):
 def energy(self,z,x):
  old=self.L;self.L=0
  try:E=super().energy(z,x)
  finally:self.L=old
  amp=torch.sqrt(RESERVOIR*torch.softmax(z,dim=0)/self.vol)
  return E+.5*(old/self.rm)**3*torch.sum(self.rf**2/self.dr*(amp[1:]-amp[:-1])**2)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('material_interface_2026_10_24/run_continue/results.json').read_text())['runs'][2];out={'runs':[],'checks':[]}
 for L in [1,3,10]:
  m=Global(n=96,domain=12,beta=2,K=30,charge=0,L=L);m.ell2=(10/m.rm)**2;v,info=transfer_species(m,old);E,g=m.direct(v);d=np.sin(np.arange(192));d[:96]*=1e-14;err=[]
  for dt in [1e-5,3e-6,1e-6]:
   fd=(m.direct(v+dt*d)[0]-m.direct(v-dt*d)[0])/(2*dt);err.append(abs(fd-g@d)/max(1,abs(fd)))
  assert max(err)<1e-6;out['checks'].append(err)
  r=polish(m,v,dest.with_name(f'checkpoint_{L}.json'),maxiter=1600);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['density_stiffness_length_kpc','law_endpoint_error_dex','density_KKT_max','explicit_exterior_mass','explicit_exterior_T_fraction','empty_transition_cells','interpolated_crossings_kpc','optimizer']},flush=True)
