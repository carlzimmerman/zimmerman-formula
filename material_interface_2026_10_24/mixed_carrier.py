"""Capacity requires genuinely mixed material, not weak core phase ripples."""
import argparse,json
from pathlib import Path
import torch
from carrier_checked import Carrier,RESERVOIR,transfer_species
class Mixed(Carrier):
 def capacity(self,z,x):
  m=RESERVOIR*torch.softmax(z,dim=0);rho=m/self.vol;q=torch.sin(torch.pi*x/2)**2;u=self.A@(m*q)
  rhof=2*rho[1:]*rho[:-1]/(rho[1:]+rho[:-1]+1e-100);f=rhof/(rhof+self.rhos)
  qf=(q[1:]+q[:-1])/2;b=(4*qf*(1-qf))**2;ff=self.functions((u[1:]+u[:-1])/2)[1]
  dq=q[1:]-q[:-1];reg=self.delta*self.dr;D=dq*dq/(torch.sqrt(dq*dq+reg*reg)+reg)
  return torch.sum(self.rf**2*ff*f*b*D)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);out={'checks':{},'runs':[]}
 import numpy as np
 m=Mixed(n=32,domain=4,beta=2,K=3,charge=.003);v=m.start(scale=8);v[m.n:]=np.linspace(.8,.1,m.n);d=np.cos(np.arange(2*m.n));d[:m.n]*=1e-6;E,g=m.direct(v);err=[]
 for eps in [1e-5,3e-6,1e-6]:
  fd=(m.direct(v+eps*d)[0]-m.direct(v-eps*d)[0])/(2*eps);err.append(abs(fd-g@d)/max(1,abs(fd)))
 assert max(err)<1e-7;out['checks']['gradient_errors']=err
 sources=json.loads(Path('material_interface_2026_10_24/run_pressure/results.json').read_text())['runs'];low=json.loads(Path('material_interface_2026_10_24/run_thickness/results.json').read_text())['runs'][6]
 for K,k in [(3,.003),(10,.003),(30,.003),(30,.03)]:
  n=64 if K==3 else 96;domain=4 if K==3 else 12;m=Mixed(n=n,domain=domain,beta=2,K=K,charge=k);m.ell2=(10/m.rm)**2
  old=low if K==3 else sources[0 if K==10 else 1];v,info=transfer_species(m,old);assert min(m.cap(v))>0
  r=m.solve_checkpointed(v,dest.with_name(f'checkpoint_{K}_{k}.json'),maxiter=1600);r.update(ell_kpc=10,transfer=info,capacity_model='mixed_carrier');out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({a:r[a] for a in ['K','charge','law_windows_dex','qouter','density_KKT_max','interpolated_crossings_kpc','optimizer']},flush=True)
