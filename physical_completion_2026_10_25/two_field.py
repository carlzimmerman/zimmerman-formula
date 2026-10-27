import argparse,json
from pathlib import Path
import numpy as np,torch
from vacuum_checked import Vacuum
from three_field_solver import finish
from joint import RESERVOIR,T,law
class TwoField(Vacuum):
 def __init__(self,*args,J=30,**kw):super().__init__(*args,**kw);self.J=J
 def energy(self,z,p):
  n=self.n;x=p[:n];y=p[n:];mass=RESERVOIR*torch.softmax(z,dim=0);rho=mass/self.vol;qx=torch.sin(torch.pi*x/2)**2;q=torch.sin(torch.pi*y/2)**2;u=self.A@(mass*q);w,F=self.functions(u);mt=(mass*q).sum();M=mass.sum();s=torch.sin(torch.pi*x)**2/torch.pi**2
  E=torch.sum(self.vol*(w+self.beta*.95*s*F))+torch.sum(self.tw*self.functions(mt*self.tt**2)[0]/self.tt**4);ff=self.functions((u[1:]+u[:-1])/2)[1];weight=self.rf**2/self.dr;dx=x[1:]-x[:-1];dy=y[1:]-y[:-1];E=E+.5*torch.sum(weight*(self.ell2*ff+(self.vacuum_length/self.rm)**2)*dx**2)
  k=(self.material_length/self.rm)**2;a=torch.sqrt(rho);E=E+.5*k*torch.sum(weight*((a[1:]-a[:-1])**2+(torch.pi/2)**2*(rho[1:]+rho[:-1])/2*dy**2))
  gd=self.A@mass;gb=self.r/(self.r**2+self.b**2)**1.5;E=E-torch.sum(self.vol*(.5*gd**2+gb*gd))-.5*M**2/self.R-M/np.sqrt(self.R**2+self.b**2);E=E+1.5*self.K*torch.sum(self.vol*rho**(5/3)*torch.abs(torch.cos(torch.pi*y/2))**(10/3))
  return E+torch.sum(self.volume_cost*self.vol*qx-self.eps*mass*q+self.J*mass*torch.sin(torch.pi*(y-x)/2)**2)
 def cap(self,v):return .9997-self.A.numpy()@(v[:self.n]*np.sin(np.pi*v[2*self.n:]/2)**2)
 def capjac(self,v):
  n=self.n;q=np.sin(np.pi*v[2*n:]/2)**2;hp=np.pi/2*np.sin(np.pi*v[2*n:]);return -np.c_[self.A.numpy()*q,np.zeros((n,n)),self.A.numpy()*(v[:n]*hp)]
 def report(self,v):
  n=self.n;E,g=self.fg(v);z=v[:n];x=v[n:2*n];y=v[2*n:];mass=np.exp(z-max(z));mass*=RESERVOIR/sum(mass);q=np.sin(np.pi*y/2)**2;qx=np.sin(np.pi*x/2)**2;rad=self.r.numpy()*self.rm;gb=self.r.numpy()/(self.r.numpy()**2+self.b**2)**1.5;gt=gb+self.A.numpy()@mass;ref=law(gb);err=np.log10(gt/ref);sel=(rad>=1.5)&(rad<=50);ee=max(max(abs(err[sel])),max(abs(np.interp([1.5,50],rad,err))));proj=g.copy();ph=v[n:];proj[n:][((ph<=1e-8)&(g[n:]>0))|((ph>=1-1e-8)&(g[n:]<0))]=0
  def cross(qq):
   ids=np.where((qq[:-1]-.5)*(qq[1:]-.5)<0)[0];return [float(rad[i]+(.5-qq[i])*(rad[i+1]-rad[i])/(qq[i+1]-qq[i])) for i in ids]
  cr=cross(q);cx=cross(qx);R=cr[-1] if cr else None;rho=mass/self.vol.numpy();out=dict(n=n,R_kpc=self.R*self.rm,energy=E,gradient_max=float(max(abs(proj))),mass=mass.tolist(),v=v.tolist(),r=rad.tolist(),q=q.tolist(),q_vacuum=qx.tolist(),g_total=gt.tolist(),g_law=ref.tolist(),interpolated_crossings_kpc=cr,vacuum_crossings_kpc=cx,max_u=float(max(self.A.numpy()@(mass*q))),scaled_law_error_bound_percent=float((10**ee-1)*100),physical_scale=self.scale,alignment_J=self.J,alignment_ratio=self.J/self.eps,max_angle_lag=float(np.pi/2*max(abs(y-x))),mass_weighted_angle_lag=float(np.pi/2*(mass@abs(y-x))/RESERVOIR),model='Independent vacuum phase and matter spin angle; finite alignment energy; all variables varied',beta=self.beta,K=self.K)
  if R:
   ss=(rad>15)&(rad<1.2*R);rr=rho[ss];outside=rad>1.2*R;out.update(scaled_density_rebound=float(max(rr/np.minimum.accumulate(rr))) if len(rr) else None,scaled_boundary_kpc=R,free_exterior_mass=float(sum(mass[outside])),free_exterior_T_fraction=float(mass[outside]@q[outside]/sum(mass[outside])))
  return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('physical_completion_2026_10_25/run_vacuum/prepared.json').read_text());out={'runs':[],'checks':[]}
 for J in [30.,300.,3.]:
  m=TwoField(J=J);n=m.n;v=np.r_[old['mass'],old['v'][n:],old['v'][n:]];z=np.r_[np.log(v[:n]),v[n:]];d=np.cos(np.arange(3*n));E,g=m.fg(z);errors=[]
  for dt in [1e-6,3e-7,1e-7]:
   fd=(m.fg(z+dt*d)[0]-m.fg(z-dt*d)[0])/(2*dt);errors.append(abs(fd-g@d)/max(1,abs(fd)))
  assert max(errors)<1e-6;out['checks'].append(errors);r=finish(m,v,dest.with_name(f'J_{J}.json'),initial_iterations=0,newton_iterations=70);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r.get(k) for k in ['alignment_J','scaled_law_error_bound_percent','scaled_density_rebound','scaled_boundary_kpc','max_angle_lag','density_KKT_max','gradient_max','free_exterior_T_fraction','optimizer']},flush=True)
