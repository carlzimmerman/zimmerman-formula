import sys
from pathlib import Path
import numpy as np,torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'gradient_coupling_2026_10_24'))
from coupled_model import Coupled,solve,transfer_species
from joint import T,outer
class Surface(Coupled):
 def __init__(self,*args,sigma=.01,spacing=2,**kw):
  super().__init__(*args,**kw);self.sigma=sigma;self.spacing=spacing
  # Fixed physical interval resolved independently of the resulting wall radius.
  edges=np.r_[25*np.linspace(0,1,65)**2,np.arange(25+spacing,225+.1*spacing,spacing),np.geomspace(225,self.R*self.rm,33)[1:]]/self.rm
  self.n=len(edges)-1;r=(edges[1:]+edges[:-1])/2;self.r=T(r);self.vol=T(np.diff(edges**3)/3);self.dr=T(np.diff(r));self.rf=T((r[1:]+r[:-1])/2);self.B=T(np.tril(np.ones((self.n,self.n)),-1)+.5*np.eye(self.n));self.A=self.B/self.r[:,None]**2;self.grav=T(1/np.maximum(r[:,None],r[None,:]));self.phib=-1/torch.sqrt(self.r**2+self.b**2)
 def energy(self,z,x):
  E=super().energy(z,x);q=torch.sin(torch.pi*x/2)**2;dq=q[1:]-q[:-1];reg=self.delta*self.dr;D=dq*dq/(torch.sqrt(dq*dq+reg*reg)+reg)
  return E+self.sigma*torch.sum(self.rf**2*D)
 def report(self,v):
  r=super().report(v);rad=np.array(r['r']);mass=np.array(r['mass']);rho=mass/self.vol.numpy();R=r['interpolated_crossings_kpc'][-1] if r['interpolated_crossings_kpc'] else 0;sel=(rad>15)&(rad<1.2*R);rr=rho[sel];r.update(surface_tension=self.sigma,spacing_kpc=self.spacing,density_rebound_full=float(max(rr/np.minimum.accumulate(rr))) if len(rr) else None,phase_endpoint=float(v[-1]));return r
