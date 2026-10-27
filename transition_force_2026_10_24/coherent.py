import sys,json,argparse
from pathlib import Path
import numpy as np,torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'material_interface_2026_10_24'))
from mixed_carrier import Mixed,transfer_species
from polish import polish
from joint import RESERVOIR,T
class Coherent(Mixed):
 def __init__(self,*args,Fs=.03,**kw):super().__init__(*args,**kw);self.Fs=Fs
 def activation(self,x):
  q=torch.sin(torch.pi*x/2)**2;t=torch.clamp(q/.2,0,1);return t**3*(10-15*t+6*t*t)
 def energy(self,z,x):
  m=RESERVOIR*torch.softmax(z,dim=0);rho=m/self.vol;gd=self.A@m;S=self.activation(x);w,_=self.functions(gd);gb=self.r/(self.r*self.r+self.b*self.b)**1.5;M=m.sum()
  grav=-torch.sum(self.vol*(.5*gd**2+gb*gd))-.5*M*M/self.R-M/np.sqrt(self.R*self.R+self.b*self.b)
  bulk=torch.sum(self.vol*(S*w+1.5*self.K*(1-S)*rho**(5/3)))
  phase=self.beta*.95*self.Fs*torch.sum(self.vol*torch.sin(torch.pi*x)**2/torch.pi**2)+.5*self.ell2*self.Fs*torch.sum(self.rf**2/self.dr*(x[1:]-x[:-1])**2)
  return grav+bulk+phase
 def cap(self,v):return .9997-self.A.numpy()@v[:self.n]
 def capjac(self,v):return -np.c_[self.A.numpy(),np.zeros((self.n,self.n))]
 def report(self,v):
  r=super().report(v);r.update(Fs=self.Fs,activation_end=float(self.activation(T(v[self.n:]))[-1]));return r
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);out={'runs':[],'checks':[]};old=json.loads(Path('material_interface_2026_10_24/run_final_recovery/base_192.json').read_text())
 for Fs in [.01,.03,.1]:
  m=Coherent(n=96,domain=12,beta=.5,K=15,charge=0,Fs=Fs);m.ell2=(10/m.rm)**2;v,info=transfer_species(m,old);assert min(m.cap(v))>0
  E,g=m.direct(v);d=np.sin(np.arange(192));d[:96]*=1e-7;errors=[]
  for eps in [1e-5,3e-6,1e-6]:
   fd=(m.direct(v+eps*d)[0]-m.direct(v-eps*d)[0])/(2*eps);errors.append(abs(fd-g@d)/max(1,abs(fd)))
  assert max(errors)<1e-6;out['checks'].append(errors)
  r=polish(m,v,dest.with_name(f'checkpoint_{Fs}.json'),maxiter=1600);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['Fs','law_windows_dex','density_KKT_max','interpolated_crossings_kpc','activation_end','optimizer']},flush=True)
