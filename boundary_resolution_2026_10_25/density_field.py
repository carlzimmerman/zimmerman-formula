import argparse,json
from pathlib import Path
import numpy as np,torch
from critical import Critical
from fast_active import finish
from joint import RESERVOIR
class DensityField(Critical):
 def __init__(self,*args,density_length=1,**kw):super().__init__(*args,**kw);self.density_length=density_length
 def energy(self,z,x):
  E=super().energy(z,x);mass=RESERVOIR*torch.softmax(z,dim=0);rho=mass/self.vol;t=torch.clamp((rho-.001)/.002,0,1);S=t**3*(10-15*t+6*t*t);coef=self.eps*.002*(self.density_length/self.rm)**2
  return E+.5*coef*torch.sum(self.rf**2/self.dr*(S[1:]-S[:-1])**2)
 def report(self,v):
  r=super().report(v);r['density_activation_length_kpc']=self.density_length;return r
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('boundary_resolution_2026_10_25/run_force_finish/results.json').read_text());h=.1
 control=Critical(domain=12,beta=2,K=30,charge=0,L=1,eta=0,sigma=.002,eps=.3,hcritical=h);control.ell2=(2/control.rm)**2;v=np.r_[old['mass'],old['v'][control.n:]];r=finish(control,v,dest.with_name('active_control.json'),initial_iterations=0,newton_iterations=30);out={'control':r}
 m=DensityField(domain=12,beta=2,K=30,charge=0,L=0,eta=0,sigma=.002,eps=.3,hcritical=h,density_length=1);m.ell2=(2/m.rm)**2;v=np.r_[r['mass'],r['v'][m.n:]];vv=np.r_[np.log(v[:m.n]),v[m.n:]];rad=m.r.numpy()*m.rm;x=v[m.n:];d=np.r_[np.sin(rad/10),.05*x*(1-x)];E,g=m.fg(vv);errs=[]
 for dt in [1e-5,3e-6,1e-6]:
  fd=(m.fg(vv+dt*d)[0]-m.fg(vv-dt*d)[0])/(2*dt);errs.append(abs(fd-g@d)/max(1,abs(fd)))
 assert max(errs)<1e-6;out['checks']=errs;r=finish(m,v,dest.with_name('density_field.json'));out['candidate']=r;dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['law_endpoint_error_dex','density_KKT_max','gradient_max','density_rebound_full','mass_outside50','explicit_exterior_mass','explicit_exterior_T_fraction','interpolated_crossings_kpc','optimizer']})
