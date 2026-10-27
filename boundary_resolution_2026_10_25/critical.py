import argparse,json
from pathlib import Path
import numpy as np,torch
from compact import Compact
from surface_checked import transfer_species
from fast_solve import finish
from joint import T
from joint_recovery import moved
class Critical(Compact):
 def __init__(self,*args,hcritical=.1,**kw):
  super().__init__(*args,h=.25,**kw);self.h=hcritical
  ed=np.r_[35*np.linspace(0,1,81)**2,np.arange(35.25,50.001,.25),np.arange(50+hcritical,60+.01*hcritical,hcritical),np.arange(60.25,80.001,.25),np.geomspace(80,self.R*self.rm,65)[1:]]/self.rm;self.n=len(ed)-1;r=(ed[1:]+ed[:-1])/2;self.r=T(r);self.vol=T(np.diff(ed**3)/3);self.dr=T(np.diff(r));self.rf=T((r[1:]+r[:-1])/2);self.B=T(np.tril(np.ones((self.n,self.n)),-1)+.5*np.eye(self.n));self.A=self.B/self.r[:,None]**2;self.grav=T(1/np.maximum(r[:,None],r[None,:]));self.phib=-1/torch.sqrt(self.r**2+self.b**2)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);base=json.loads(Path('boundary_resolution_2026_10_25/run_regularized/base_0.25.json').read_text());out={'runs':[],'checks':[]}
 for h in [.1,.05]:
  m=Critical(domain=12,beta=2,K=30,charge=0,L=1,eta=0,sigma=.002,eps=.3,hcritical=h);m.ell2=(2/m.rm)**2;v,info=transfer_species(m,base);vv=np.r_[np.log(v[:m.n]),v[m.n:]];rad=m.r.numpy()*m.rm;x=v[m.n:];d=np.r_[np.sin(rad/10),.05*np.cos(rad/10)*x*(1-x)];E,g=m.fg(vv);err=[]
  for dt in [1e-5,3e-6,1e-6]:
   fd=(m.fg(vv+dt*d)[0]-m.fg(vv-dt*d)[0])/(2*dt);err.append(abs(fd-g@d)/max(1,abs(fd)))
  assert max(err)<1e-6;out['checks'].append(err);r=finish(m,v,dest.with_name(f'base_{h}.json'));r.update(stage='base',transfer=info);base=r;out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print('BASE',{k:r[k] for k in ['fine_spacing_kpc','n','law_endpoint_error_dex','density_KKT_max','density_rebound_full','mass_outside50','explicit_exterior_mass','explicit_exterior_T_fraction','interpolated_crossings_kpc','optimizer']},flush=True)
  for disp in [-1.,1.]:
   v=moved(m,base,disp);assert v is not None and min(m.cap(v))>0
   rr=finish(m,v,dest.with_name(f'recover_{h}_{disp}.json'));rr.update(stage='recovery',displacement_kpc=disp,energy_difference=rr['energy']-base['energy'],front_change_kpc=rr['interpolated_crossings_kpc'][-1]-base['interpolated_crossings_kpc'][-1]);out['runs'].append(rr);dest.write_text(json.dumps(out,indent=2)+'\n');print('RECOVER',h,disp,{k:rr[k] for k in ['front_change_kpc','energy_difference','law_endpoint_error_dex','density_KKT_max','density_rebound_full','optimizer']},flush=True)
