import argparse,json
from pathlib import Path
import numpy as np,torch
from two_field import TwoField
from three_field_solver import finish
from joint import T,RESERVOIR

def model(h):
 m=TwoField(J=30);ed=np.r_[35*np.linspace(0,1,81)**2,np.arange(35+h,65+.1*h,h),np.arange(65.25,80.01,.25),np.geomspace(80,m.R*m.rm,65)[1:]]/m.rm;m.n=len(ed)-1;r=(ed[1:]+ed[:-1])/2;m.r=T(r);m.vol=T(np.diff(ed**3)/3);m.dr=T(np.diff(r));m.rf=T((r[1:]+r[:-1])/2);m.B=T(np.tril(np.ones((m.n,m.n)),-1)+.5*np.eye(m.n));m.A=m.B/m.r[:,None]**2;m.grav=T(1/np.maximum(r[:,None],r[None,:]));m.phib=-1/torch.sqrt(m.r**2+m.b**2);return m

def transfer(m,old):
 rad=np.array(old['r']);ed=[0.]
 for rr in rad:ed.append(2*rr-ed[-1])
 new=[0.]
 for rr in m.r.numpy()*m.rm:new.append(2*rr-new[-1])
 mass=np.array(old['mass']);q=np.array(old['q']);parts=[np.maximum(np.diff(np.interp(np.array(new)**3,np.array(ed)**3,np.r_[0,np.cumsum(mass*f)])),0) for f in [q,1-q]];mm=parts[0]+parts[1];qq=np.divide(parts[0],mm,out=np.zeros_like(mm),where=mm>1e-14);mm=np.maximum(mm,1e-12);mm*=RESERVOIR/sum(mm);y=2/np.pi*np.arcsin(np.sqrt(np.clip(qq,0,1)));x=np.interp(m.r.numpy()*m.rm,rad,old['v'][len(mass):2*len(mass)]);return np.r_[mm,x,y]
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('physical_completion_2026_10_25/run_two_field/J_30.0.json').read_text());out={'runs':[]}
 for h in [.125,.0625]:
  m=model(h);v=transfer(m,old);assert min(m.cap(v))>0;r=finish(m,v,dest.with_name(f'h_{h}.json'),initial_iterations=0,newton_iterations=65);r.update(interface_spacing_kpc=h,refined_interval_kpc=[35,65]);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r.get(k) for k in ['n','interface_spacing_kpc','scaled_boundary_kpc','scaled_law_error_bound_percent','scaled_density_rebound','density_KKT_max','gradient_max','max_angle_lag','optimizer']},flush=True)
  if not r['optimizer']['success']:break
  old=r
