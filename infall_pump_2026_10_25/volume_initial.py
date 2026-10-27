"""Conservative initial remap in enclosed volume, regular at a finite-density core.

No subsequent density trajectory is specified. M(s) with s=r^3/3 is linear for
a uniform core, unlike M(r). PCHIP preserves nonnegative cell species masses.
"""
import numpy as np
from scipy.interpolate import PchipInterpolator
from physical_branch import PhysicalFull

def fine_initial(m,case,equilibrium=None):
 assert equilibrium and case in ('formed','prepared','dilated')
 b=PhysicalFull(wave_R_kpc=10000.);old=np.load(equilibrium);aa=old['a'];edge=b.edges.copy()
 if case=='dilated':edge*=1+.2*np.exp(-(edge*b.rm/200)**4)
 assert np.min(np.diff(edge))>0
 a=[]
 for av in aa:
  mass=abs(av)**2;cs=np.r_[0.,np.cumsum(mass)]
  interp=PchipInterpolator(edge**3/3,cs)
  new=np.maximum(np.diff(interp(m.edges**3/3)),0.)
  new*=np.sum(mass)/np.sum(new)
  a.append(np.sqrt(new)*np.exp(1j*np.interp(m.r,b.r,np.unwrap(np.angle(av)))))
 a=np.array(a);x=np.arctan2(abs(a[0]),abs(a[1]));c=np.zeros(len(m.wr));x,res,it=m.minimize_alpha(a,c,x,maxit=400)
 return a,x,c,c.copy(),{'initial_data':'Species cumulative masses interpolated monotonically in enclosed volume; original mass mapped onto displaced original edges before evaluation on fine grid. Regular constant-density core reproduced exactly. No wave or fast-mode seed.','case':case,'initial_carrier_residual':res,'initial_carrier_iterations':it,'material_h_kpc':m.material_h_kpc,'mass':float(np.sum(abs(a)**2))}
