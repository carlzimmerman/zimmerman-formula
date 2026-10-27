"""C4 positive continuum density, conservatively pushed forward before sampling.

Reference density comes from the force-finished energy equilibrium, not the
target law. Reflection enforces a regular even central density. The smooth
radial diffeomorphism and Gauss volume integration replace piecewise cumulative
mass interpolation, so a short-wave pump cannot hide in interpolation kinks.
"""
import numpy as np
from scipy.interpolate import make_interp_spline
from live_collocated import Collocated

def fine_initial(m,case,equilibrium=None):
 assert case=='dilated'
 ref=Collocated(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);s=np.load('infall_pump_2026_10_25/run_static_polish/state.npz');ar=s['a'];rho=np.sum(abs(ar)**2,axis=0)/ref.vol
 logprofile=make_interp_spline(np.r_[-ref.r[::-1],ref.r],np.r_[np.log(rho[::-1]),np.log(rho)],k=5)
 def inverse(r):
  old=r/1.2
  for _ in range(12):
   power=(old*m.rm/200)**4;ex=np.exp(-power);derivative=1+.2*ex*(1-4*power);old-=(old*(1+.2*ex)-r)/derivative
  return old,derivative
 nodes,weights=np.polynomial.legendre.leggauss(8);mid=(m.edges[1:]+m.edges[:-1])/2;half=np.diff(m.edges)/2;rq=mid[:,None]+half[:,None]*nodes[None,:];ro,der=inverse(rq);rn=np.exp(logprofile(ro))*(ro/rq)**2/der;mass=half*np.sum(weights*rn*rq*rq,axis=1);mass*=m.M/np.sum(mass)
 oldr,_=inverse(m.r);theta=np.interp(oldr,ref.r,np.arctan2(abs(ar[0]),abs(ar[1])));a=np.array([np.sqrt(mass)*np.sin(theta),np.sqrt(mass)*np.cos(theta)],complex);c=np.zeros(len(m.wr));x,res,it=m.minimize_alpha(a,c,theta,maxit=400)
 return a,x,c,c.copy(),{'initial_data':'Positive C4 log-density interpolant of force-finished reference, even at origin, exact smooth radial pushforward rnew=rold[1+.2 exp(-(rold/200kpc)^4)],8-point Gauss r^2dr cell integration, total mass normalized. Internal composition/carrier preparation follows separately. No target-law fit or supplied wave modes.','mass':float(np.sum(mass)),'minimum_mass':float(np.min(mass)),'material_h_kpc':m.material_h_kpc,'initial_carrier_residual':res}
