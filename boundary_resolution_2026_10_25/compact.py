import argparse,json
from pathlib import Path
import numpy as np,torch
from chemical import Chemical
from surface_checked import solve,transfer_species
from joint import T
class Compact(Chemical):
 def __init__(self,*args,h=.5,**kw):
  super().__init__(*args,**kw);self.h=h
  ed=np.r_[35*np.linspace(0,1,81)**2,np.arange(35+h,80+.1*h,h),np.geomspace(80,self.R*self.rm,65)[1:]]/self.rm;self.n=len(ed)-1;r=(ed[1:]+ed[:-1])/2;self.r=T(r);self.vol=T(np.diff(ed**3)/3);self.dr=T(np.diff(r));self.rf=T((r[1:]+r[:-1])/2);self.B=T(np.tril(np.ones((self.n,self.n)),-1)+.5*np.eye(self.n));self.A=self.B/self.r[:,None]**2;self.grav=T(1/np.maximum(r[:,None],r[None,:]));self.phib=-1/torch.sqrt(self.r**2+self.b**2)
 def report(self,v):
  r=super().report(v);r['fine_spacing_kpc']=self.h;return r
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('boundary_resolution_2026_10_25/run_chemical/results.json').read_text())['runs'][2];out={'runs':[],'checks':[]}
 for L,eps in [(0,.2),(0,.3),(1,.2),(1,.3)]:
  m=Compact(domain=12,beta=2,K=30,charge=0,L=L,eta=3,sigma=.003,eps=eps,h=.5);m.ell2=(3/m.rm)**2;v,info=transfer_species(m,old);vv=np.r_[np.log(v[:m.n]),v[m.n:]];d=np.cos(np.arange(2*m.n));E,g=m.fg(vv);err=[]
  for dt in [1e-6,3e-7,1e-7]:
   fd=(m.fg(vv+dt*d)[0]-m.fg(vv-dt*d)[0])/(2*dt);err.append(abs(fd-g@d)/max(1,abs(fd)))
  assert max(err)<1e-6;out['checks'].append(err);r=solve(m,v,dest.with_name(f'checkpoint_{L}_{eps}.json'),maxiter=2200);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['density_stiffness_length_kpc','chemical_epsilon','n','law_endpoint_error_dex','density_KKT_max','mass_outside50','min_transition_cell_mass','density_rebound_full','explicit_exterior_mass','explicit_exterior_T_fraction','interpolated_crossings_kpc','optimizer']},flush=True)
