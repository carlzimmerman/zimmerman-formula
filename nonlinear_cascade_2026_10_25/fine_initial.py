"""Positive conservative interpolation defines initial data only, not evolution."""
import numpy as np
from scipy.interpolate import PchipInterpolator
from initial import initial
from physical_branch import PhysicalFull

def fine_initial(m,case,equilibrium=None):
 b=PhysicalFull(wave_R_kpc=10000.)
 if equilibrium:
  s=np.load(equilibrium);aa=s['a'].copy();xx=s['alpha'].copy()
  if case=='dilated':
   shift=b.edges*(1+.2*np.exp(-(b.edges*b.rm/200)**4));aa=np.sqrt(np.maximum([np.diff(np.interp(b.edges,shift,np.r_[0,np.cumsum(abs(v)**2)])) for v in aa],0)).astype(complex);xx=b.minimize_alpha(aa,np.zeros(len(b.wr)),np.arctan2(abs(aa[0]),abs(aa[1])),maxit=300)[0]
 else:aa,xx,_,_,_=initial(b,case)
 aa2=[]
 for av in aa:
  old=abs(av)**2;cs=np.r_[0,np.cumsum(old)];interp=PchipInterpolator(b.edges,cs);new=np.maximum(np.diff(interp(m.edges)),0);new*=sum(old)/sum(new) if sum(new)>0 else 1;phase=np.interp(m.r,b.r,np.unwrap(np.angle(av)));aa2.append(np.sqrt(new)*np.exp(1j*phase))
 a=np.array(aa2);x=np.interp(m.r,b.r,xx);chi=np.zeros(len(m.wr));x,res,it=m.minimize_alpha(a,chi,x,maxit=300)
 return a,x,chi,chi.copy(),{'initial_data':'Positive PCHIP cumulative species mass from original initial state, normalized separately; phase/carrier interpolated. Subsequent density and phases free. Not a newly force-certified fine equilibrium.','case':case,'initial_carrier_residual':res,'initial_carrier_iterations':it,'reference_input_mass':float(np.sum(abs(aa)**2)),'new_mass':float(np.sum(abs(a)**2)),'material_h_kpc':m.material_h_kpc,'uniform_material_region_kpc':[.5,320.]}
