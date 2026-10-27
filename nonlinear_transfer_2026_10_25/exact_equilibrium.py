"""Force-finish exact complex-edge equilibrium using the inherited 3n Newton."""
import argparse,json,sys
from pathlib import Path
import numpy as np,torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'physical_completion_2026_10_25'))
from two_field import TwoField
from free_formation import FreeVacuum
from joint import RESERVOIR,T
from three_field_solver import finish

class Exact(TwoField,FreeVacuum):
 def functions(self,u):
  c=.9999;v=torch.clamp(u,max=c);d=u-v;poly=torch.zeros_like(v)+1/16
  for n in range(15,1,-1):poly=1/n+v*poly
  W=torch.where(abs(v)<.05,v*v*poly,-torch.log1p(-v)-v)+d*c/(1-c)+.5*d*d/(1-c)**2;F=v*v/(1-v)+d*c*(2-c)/(1-c)**2+d*d/(1-c)**3;return W,F
 def energy(self,z,p):
  n=self.n;x=p[:n];y=p[n:];mass=RESERVOIR*torch.softmax(z,dim=0);rho=mass/self.vol;q=torch.sin(torch.pi*y/2)**2;qx=torch.sin(torch.pi*x/2)**2;u=self.A@(mass*q);w,F=self.functions(u);mt=(mass*q).sum();M=mass.sum();s=torch.sin(torch.pi*x)**2/torch.pi**2
  E=torch.sum(self.vol*(w+self.beta*.95*s*F))+torch.sum(self.tw*self.functions(mt*self.tt**2)[0]/self.tt**4);ff=self.functions((u[1:]+u[:-1])/2)[1];weight=self.rf**2/self.dr;dx=x[1:]-x[:-1];E+=.5*torch.sum(weight*(self.ell2*ff+(self.vacuum_length/self.rm)**2)*dx**2)
  a=torch.sqrt(rho);t=a*torch.sin(torch.pi*y/2);f=a*torch.cos(torch.pi*y/2);E+=.5*(self.material_length/self.rm)**2*torch.sum(weight*((t[1:]-t[:-1])**2+(f[1:]-f[:-1])**2))
  gd=self.A@mass;gb=self.r/(self.r**2+self.b**2)**1.5;E-=torch.sum(self.vol*(.5*gd**2+gb*gd))+.5*M*M/self.R+M/np.sqrt(self.R*self.R+self.b*self.b);E+=1.5*self.K*torch.sum(self.vol*rho**(5/3)*abs(torch.cos(torch.pi*y/2))**(10/3));E+=torch.sum(self.volume_cost*self.vol*qx-self.eps*mass*q+self.J*mass*torch.sin(torch.pi*(y-x)/2)**2);return E

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);m=Exact(J=30);old=np.load('nonlinear_transfer_2026_10_25/run_equilibrium_stable/state.npz');mass=np.sum(abs(old['a'])**2,axis=0);theta=np.arctan2(abs(old['a'][0]),abs(old['a'][1]));v=np.r_[mass,old['alpha']*2/np.pi,theta*2/np.pi];r=finish(m,v,dest.with_name('equilibrium.json'),initial_iterations=0,newton_iterations=30);n=m.n;mass=np.array(r['mass']);x=np.array(r['v'][n:2*n])*np.pi/2;th=np.array(r['v'][2*n:])*np.pi/2;aa=np.array([np.sqrt(mass)*np.sin(th),np.sqrt(mass)*np.cos(th)],complex);np.savez_compressed(dest.with_name('state.npz'),a=aa,alpha=x,chi=old['chi'],pi=old['pi']);out={k:r.get(k) for k in ['energy','density_KKT_max','gradient_max','optimizer','scaled_law_error_bound_percent','scaled_density_rebound','scaled_boundary_kpc','free_exterior_T_fraction','mass_constraint_error']};dest.write_text(json.dumps(out,indent=2)+'\n');print(out,flush=True)
