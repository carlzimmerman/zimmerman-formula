import argparse,json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'live_density_interface_2026_10_24'))
from joint import G,A0,outer
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();rm=np.sqrt(G*6e10/A0);ell=10/rm;beta=2;C=.95;M=4.4;r0=30/rm;box=12*outer(3/rm);gamma=np.sqrt(2*beta*C)/ell

def F(r):
 r=np.asarray(r);u=np.where(r<r0,M*r/r0**3,M/np.maximum(r,1e-30)**2);return u*u/(1-u)
def profile(r,R):return 2/np.pi*np.arctan(np.exp(-gamma*(r-R)))
def reference(R,sigma=0):
 def integrand(r):
  x=profile(r,R);xp=-gamma/(np.pi*np.cosh(gamma*(r-R)));qprime=np.pi/2*np.sin(np.pi*x)*xp
  return r*r*(F(r)*(beta*C*np.sin(np.pi*x)**2/np.pi**2+.5*ell*ell*xp*xp)+sigma*abs(qprime))
 return sum(quad(integrand,lo,hi,epsabs=1e-11,epsrel=1e-10)[0] for lo,hi in [(0,r0),(r0,R),(R,box)])
def discrete(edges,R):
 r=(edges[1:]+edges[:-1])/2;vol=np.diff(edges**3)/3;dr=np.diff(r);rf=(r[1:]+r[:-1])/2;x=profile(r,R);u=np.where(r<r0,M*r/r0**3,M/r**2);uf=(u[1:]+u[:-1])/2
 return float(sum(vol*beta*C*F(r)*np.sin(np.pi*x)**2/np.pi**2)+.5*ell*ell*sum(rf*rf/dr*(uf*uf/(1-uf))*np.diff(x)**2))
Radii=np.arange(90,191,1)/rm;step=.02/rm;force=np.array([-(reference(R+step)-reference(R-step))/(2*step) for R in Radii]);assert min(force)>0;out={'reference_outward_force_min':float(min(force)),'grids':[],'reference_R_kpc':(Radii*rm).tolist(),'reference_force_Eunit_per_rM':force.tolist()}
meshes=[('quadratic96',box*np.linspace(0,1,97)**2),('quadratic144',box*np.linspace(0,1,145)**2)]
for h in [2,1]:meshes.append((f'fixed_{h}kpc',np.r_[25*np.linspace(0,1,65)**2,np.arange(25+h,225+.1*h,h),np.geomspace(225,box*rm,33)[1:]]/rm))
for name,edges in meshes:
 ff=np.array([-(discrete(edges,R+step)-discrete(edges,R-step))/(2*step) for R in Radii]);out['grids'].append(dict(name=name,cells=len(edges)-1,spurious_inward_samples=int(sum(ff<0)),samples=len(ff),max_relative_force_error=float(max(abs(ff-force)/force)),forces=ff.tolist()))
sigma=.01;op=minimize_scalar(lambda R:reference(R,sigma),bounds=(35/rm,100/rm),method='bounded',options=dict(xatol=1e-9));A=2*ell*np.sqrt(2*beta*C)/np.pi**2;pred=np.sqrt(M*(1+np.sqrt(A/sigma)));out['empty_wall_with_surface_tension']=dict(reference_minimum_R_kpc=float(op.x*rm),thin_wall_R_kpc=float(pred*rm),qualification='Manufactured fixed-response force benchmark, not full mobile-density equilibrium.');Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['grids','reference_R_kpc','reference_force_Eunit_per_rM']},indent=2));print([{k:v for k,v in r.items() if k!='forces'} for r in out['grids']])
