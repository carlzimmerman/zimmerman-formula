"""Physical coefficient scaling and canonical spinor kinetic companion."""
import sys
from pathlib import Path
import numpy as np,torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'boundary_resolution_2026_10_25'))
from latent_stiff import LatentStiff
from joint import RESERVOIR
class Physical(LatentStiff):
 def __init__(self,scale=1.,thermal='fixed_entropy',canonical=True,h=.25):
  # scale = rM/rM_base = sqrt(Mb/Mb_base). Grid remains fixed in scaled coordinates.
  K=30*scale**(-5/3) if thermal=='fixed_entropy' else 30
  super().__init__(domain=12,beta=4,K=K,charge=0,L=0,eta=0,sigma=0,eps=.3/scale,h=h,volume_cost=.001,material_length=.25/np.sqrt(scale))
  self.scale=scale;self.thermal=thermal;self.canonical=canonical;self.rm*=scale;self.ell2=(3*np.sqrt(.5)/self.rm)**2
 def energy(self,z,x):
  E=super().energy(z,x)
  if self.canonical:
   rho=RESERVOIR*torch.softmax(z,dim=0)/self.vol;rf=(rho[1:]+rho[:-1])/2
   E=E+.5*(self.material_length/self.rm)**2*(torch.pi/2)**2*torch.sum(self.rf**2/self.dr*rf*(x[1:]-x[:-1])**2)
  return E
 def report(self,v):
  r=super().report(v);rad=np.array(r['r']);err=np.log10(np.array(r['g_total'])/r['g_law']);lo=1.5*self.scale;hi=50*self.scale;sel=(rad>=lo)&(rad<=hi);error=max(max(abs(err[sel])),max(abs(np.interp([lo,hi],rad,err))));R=r['interpolated_crossings_kpc'][-1] if r['interpolated_crossings_kpc'] else None;mass=np.array(r['mass']);q=np.array(r['q']);r.update(model='fixed physical coefficients, optional canonical spinor phase kinetic term',physical_scale=self.scale,Mb_Msun=6e10*self.scale**2,b_kpc=3*self.scale,thermal_policy=self.thermal,canonical_phase_kinetic=self.canonical,law_test_window_kpc=[lo,hi],scaled_law_error_dex=float(error),scaled_law_error_bound_percent=float((10**error-1)*100))
  if R:
   ss=(rad>15*self.scale)&(rad<1.2*R);rho=mass/self.vol.numpy();rr=rho[ss];outside=rad>1.2*R;r.update(scaled_density_rebound=float(max(rr/np.minimum.accumulate(rr))),free_exterior_mass=float(sum(mass[outside])),free_exterior_T_fraction=float(mass[outside]@q[outside]/sum(mass[outside])),scaled_boundary_kpc=R/self.scale)
  return r
