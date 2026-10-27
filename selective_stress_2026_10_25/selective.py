"""Two material fluids with distinct spatial stresses, independent carrier.

No target density/law enters energy. delta=0 is cold incoherent T plus F
gradient stress, not a canonical coherent two-state spinor.
"""
import sys,json,argparse
from pathlib import Path
import numpy as np, torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'physical_completion_2026_10_25'))
from two_field import TwoField
from two_field_refine import transfer
from three_field_solver import finish
from joint import T,RESERVOIR

class Selective(TwoField):
 def __init__(self,scale=2.,delta=0.,h=.25,center=50.,thermal='virial_scaled',strength=1.):
  super().__init__(J=30/scale,scale=scale,thermal=thermal)
  self.delta=delta;self.strength=strength;self.beta=40
  self.ell2=(3*np.sqrt(2/40)/self.rm)**2
  self.h=h;self.band=(max(30,np.floor(center-12)),min(140,np.ceil(center+12)))
  lo,hi=self.band;rm0=self.rm/scale
  ed=np.r_[30*np.linspace(0,1,81)**2,np.arange(30.5,lo+.1,.5),np.arange(lo+h,hi+.1*h,h),np.arange(hi+.5,160.1,.5),np.geomspace(160,self.R*rm0,65)[1:]]/rm0
  self.n=len(ed)-1;r=(ed[1:]+ed[:-1])/2
  self.r=T(r);self.vol=T(np.diff(ed**3)/3);self.dr=T(np.diff(r));self.rf=T((r[1:]+r[:-1])/2)
  self.B=T(np.tril(np.ones((self.n,self.n)),-1)+.5*np.eye(self.n));self.A=self.B/self.r[:,None]**2
  self.grav=T(1/np.maximum(r[:,None],r[None,:]));self.phib=-1/torch.sqrt(self.r**2+self.b**2)
 def energy(self,z,p):
  n=self.n;x=p[:n];y=p[n:];mass=RESERVOIR*torch.softmax(z,dim=0);rho=mass/self.vol
  qx=torch.sin(torch.pi*x/2)**2;q=torch.sin(torch.pi*y/2)**2
  u=self.A@(mass*q);w,F=self.functions(u);mt=(mass*q).sum();M=mass.sum();s=torch.sin(torch.pi*x)**2/torch.pi**2
  E=torch.sum(self.vol*(w+self.beta*.95*s*F))+torch.sum(self.tw*self.functions(mt*self.tt**2)[0]/self.tt**4)
  ff=self.functions((u[1:]+u[:-1])/2)[1];weight=self.rf**2/self.dr;dx=x[1:]-x[:-1]
  E=E+.5*torch.sum(weight*(self.ell2*ff+(self.vacuum_length/self.rm)**2)*dx**2)
  k=self.strength*(self.material_length/self.rm)**2
  aF=torch.sqrt(rho)*torch.cos(torch.pi*y/2);aT=torch.sqrt(rho)*torch.sin(torch.pi*y/2)
  E=E+.5*k*torch.sum(weight*((aF[1:]-aF[:-1])**2+self.delta*(aT[1:]-aT[:-1])**2))
  gd=self.A@mass;gb=self.r/(self.r**2+self.b**2)**1.5
  E=E-torch.sum(self.vol*(.5*gd**2+gb*gd))-.5*M**2/self.R-M/np.sqrt(self.R**2+self.b**2)
  E=E+1.5*self.K*torch.sum(self.vol*rho**(5/3)*torch.abs(torch.cos(torch.pi*y/2))**(10/3))
  return E+torch.sum(self.volume_cost*self.vol*qx-self.eps*mass*q+self.J*mass*torch.sin(torch.pi*(y-x)/2)**2)
 def report(self,v):
  r=super().report(v);s=self.scale;rad=np.array(r['r']);err=np.array(r['g_total'])/r['g_law']-1
  sel=(rad>=1.5*s)&(rad<=50*s);ee=np.r_[err[sel],np.interp([1.5*s,50*s],rad,err)]
  rho=np.array(r['mass'])/self.vol.numpy();cross=r['interpolated_crossings_kpc'];R=cross[-1] if cross else None
  r.update(constitutive_model='F gradient stress, T cold fluid with optional stress ratio delta',stress_ratio_T_to_F=self.delta,stress_strength=self.strength,scaled_law_error_bound_percent=float((10**max(abs(np.log10(1+ee)))-1)*100),maximum_fractional_law_error_percent=float(max(abs(ee))*100),law_test_window_kpc=[1.5*s,50*s],physical_scale=s,thermal_policy=self.thermal,scaled_spacing_kpc=self.h,fine_band_scaled_kpc=list(self.band),rho=rho.tolist())
  if R:
   ss=(rad>15*s)&(rad<1.2*R);rr=rho[ss];outside=rad>1.2*R;mass=np.array(r['mass']);q=np.array(r['q'])
   r.update(scaled_density_rebound=float(max(rr/np.minimum.accumulate(rr))),scaled_boundary_kpc=R/s,boundary_physical_kpc=R,wall_inside_fine_band=bool(self.band[0]+1<R/s<self.band[1]-1),free_exterior_mass=float(sum(mass[outside])),free_exterior_T_fraction=float(mass[outside]@q[outside]/sum(mass[outside])),edge_mass_fraction=float(sum(mass[-4:])/RESERVOIR))
  return r

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--scale',type=float,default=2.);ap.add_argument('--delta',type=float,default=0.);ap.add_argument('--strength',type=float,default=1.);ap.add_argument('--h',type=float,default=.25);ap.add_argument('--source');a=ap.parse_args();dest=Path(a.output)
 source=a.source or f'physical_completion_2026_10_25/run_purification_{a.scale}/results.json'
 old=json.loads(Path(source).read_text());old=old['runs'][-1] if 'runs' in old else old
 out={'runs':[],'gradient_checks':[],'source':source,'non_claim':'Static energy relaxation, not dynamical formation.'}
 for attempt in range(3):
  m=Selective(scale=a.scale,delta=a.delta,h=a.h,center=old['scaled_boundary_kpc'],strength=a.strength);v=transfer(m,old);z=np.r_[np.log(v[:m.n]),v[m.n:]]
  d=np.r_[.01*np.sin(np.arange(m.n)),.01*np.sin(np.arange(2*m.n)+.2)];E,g=m.fg(z);errs=[]
  for dt in [1e-5,3e-6,1e-6]:
   fd=(m.fg(z+dt*d)[0]-m.fg(z-dt*d)[0])/(2*dt);errs.append(float(abs(fd-g@d)/max(1,abs(fd))))
  assert max(errs)<1e-7;out['gradient_checks'].append(errs);assert min(m.cap(v))>0
  r=finish(m,v,dest.with_name(f'attempt_{attempt}.json'),initial_iterations=0,newton_iterations=100);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n')
  print({k:r.get(k) for k in ['physical_scale','stress_ratio_T_to_F','stress_strength','n','scaled_boundary_kpc','maximum_fractional_law_error_percent','scaled_density_rebound','density_KKT_max','gradient_max','free_exterior_T_fraction','edge_mass_fraction','wall_inside_fine_band','optimizer']},flush=True)
  if r['optimizer']['success'] and r.get('wall_inside_fine_band'):break
  old=r
