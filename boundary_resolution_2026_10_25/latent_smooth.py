import argparse,json
from pathlib import Path
import numpy as np,torch
from latent import Latent
from fast_complete import finish
from surface_checked import transfer_species
from joint import RESERVOIR
class SmoothLatent(Latent):
 def energy(self,z,x):
  mass=RESERVOIR*torch.softmax(z,dim=0);q=torch.sin(torch.pi*x/2)**2;mt=mass*q;u=self.A@mt;w,F=self.functions(u);s=torch.sin(torch.pi*x)**2/torch.pi**2;M=mt.sum();total=mass.sum()
  E=torch.sum(self.vol*(w+self.beta*.95*s*F))+torch.sum(self.tw*self.functions(M*self.tt**2)[0]/self.tt**4)
  ff=self.functions((u[1:]+u[:-1])/2)[1];E=E+.5*self.ell2*torch.sum(self.rf**2/self.dr*ff*(x[1:]-x[:-1])**2)
  gd=self.A@mass;gb=self.r/(self.r**2+self.b**2)**1.5;E=E-torch.sum(self.vol*(.5*gd**2+gb*gd))-.5*total**2/self.R-total/np.sqrt(self.R**2+self.b**2)
  # cos^(10/3) is algebraically the same gas but has finite AD Hessian at x=1.
  E=E+1.5*self.K*torch.sum(self.vol*(mass/self.vol)**(5/3)*torch.abs(torch.cos(torch.pi*x/2))**(10/3))
  return E+torch.sum(q*(self.volume_cost*self.vol-self.eps*mass))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('boundary_resolution_2026_10_25/run_compact/checkpoint_0_0.3.json').read_text());out={'runs':[],'checks':[]}
 for B in [.0003,.001,.003]:
  m=SmoothLatent(domain=12,beta=2,K=30,charge=0,L=0,eta=0,sigma=0,eps=.3,h=.5,volume_cost=B);m.ell2=(3/m.rm)**2;v,info=transfer_species(m,old);vv=np.r_[np.log(v[:m.n]),v[m.n:]];d=np.cos(np.arange(2*m.n));E,g=m.fg(vv);err=[]
  same=Latent.energy(m,torch.tensor(vv[:m.n]),torch.tensor(vv[m.n:]));assert abs(float(same)-E)<1e-12
  for dt in [1e-6,3e-7,1e-7]:
   fd=(m.fg(vv+dt*d)[0]-m.fg(vv-dt*d)[0])/(2*dt);err.append(abs(fd-g@d)/max(1,abs(fd)))
  assert max(err)<1e-6;out['checks'].append(err);r=finish(m,v,dest.with_name(f'base_{B}.json'),initial_iterations=120,newton_iterations=70);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['phase_volume_cost','law_endpoint_error_dex','density_KKT_max','gradient_max','mass_outside50','density_rebound_full','explicit_exterior_mass','explicit_exterior_T_fraction','interpolated_crossings_kpc','optimizer']},flush=True)
