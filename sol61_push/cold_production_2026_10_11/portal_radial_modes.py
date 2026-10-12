"""Radial Rayleigh-Ritz instability witnesses for the pressure-only portal fluid."""
import json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import eigh
from numpy.polynomial.legendre import leggauss
p=Path(__file__).parent
checks=[]
def check(n,b):checks.append(dict(name=n,passed=bool(b)))
def equilibrium(xc):
 yc=xc/math.hypot(1,xc);start=1e-8
 def rhs(r,z):
  y=max(0.,min(z[0],1-1e-15));rho=y/math.sqrt(1-y*y)
  return [-z[1]/r**2,r*r*rho]
 def surface(r,z):return z[0]
 surface.terminal=True;surface.direction=-1
 sol=solve_ivp(rhs,(start,10),[yc-xc*start**2/6,xc*start**3/3],events=surface,dense_output=True,rtol=2e-12,atol=2e-14,max_step=.01)
 assert sol.success and len(sol.t_events[0])==1
 return sol,sol.t_events[0][0]
def ritz(xc,N,Q):
 sol,R=equilibrium(xc)
 edges=np.r_[0.,R*np.geomspace(1e-7,1.,120)]
 z,w=leggauss(Q);r=(edges[:-1,None]+(edges[1:]-edges[:-1])[:,None]*(z+1)/2).ravel()
 weights=((edges[1:]-edges[:-1])[:,None]*w/2).ravel()
 y=np.maximum(sol.sol(np.maximum(r,1e-8))[0],0.);t=np.sqrt(1-y*y)
 rho=y/t;P=y*y/(1+t);rhocs=y*y*t;B=3*rhocs-4*P
 # Include uniform displacement plus Gaussian core/envelope profiles.
 core=min(.3,1/max(xc,1)**1.5)
 widths=R*np.geomspace(core,2.,N)
 basis=np.column_stack([np.ones_like(r)]+[np.exp(-(r/s)**2) for s in widths])
 deriv=np.column_stack([np.zeros_like(r)]+[-2*r/s**2*np.exp(-(r/s)**2) for s in widths])
 mass=basis.T@((weights*rho*r**4)[:,None]*basis)
 stiff=deriv.T@((weights*rhocs*r**4)[:,None]*deriv)
 stiff+=basis.T@((weights*3*B*r*r)[:,None]*basis)
 cross=basis.T@((weights*B*r**3)[:,None]*deriv)
 stiff+=cross+cross.T
 # Alternative manifestly-positive decomposition when Gamma>=4/3.
 div=3*basis+r[:,None]*deriv
 alt=deriv.T@((weights*(4/3)*P*r**4)[:,None]*deriv)
 alt+=div.T@((weights*(rhocs-(4/3)*P)*r*r)[:,None]*div)
 check('radial quadratic-form identity',np.max(abs(alt-stiff))<1e-10*max(1,np.max(abs(stiff))))
 scale=1/np.sqrt(np.diag(mass));Mn=mass*scale[:,None]*scale[None,:]
 Kn=stiff*scale[:,None]*scale[None,:]
 vals,vecs=eigh(Mn);keep=vals>1e-10
 transform=(vecs[:,keep]/np.sqrt(vals[keep]))
 reduced=transform.T@Kn@transform
 ev,vec=eigh((reduced+reduced.T)/2)
 coeff=scale*(transform@vec[:,0]);mode=basis@coeff;modep=deriv@coeff
 direct_num=float(np.sum(weights*(rhocs*r**4*modep**2+3*B*r*r*mode**2+2*B*r**3*mode*modep)))
 direct_den=float(np.sum(weights*rho*r**4*mode**2))
 check('direct witness Rayleigh quotient',abs(direct_num/direct_den-ev[0])<1e-6*max(1,abs(ev[0])))
 return dict(central_density_ratio=xc,basis_gaussians=N,angular_free_radial_quadrature_order=Q,
             retained_basis=int(sum(keep)),omega2_upper_bound_over_4piG_rho0=float(ev[0]),
             trial_energy_negative=bool(direct_num<0),direct_quotient=direct_num/direct_den)
rows=[ritz(x,N,8) for x in [.1,.8,1.,2.,3.,10.,30.] for N in [8,14]]
refined=[ritz(x,14,12) for x in [3.,10.,30.]]
for row in refined:
 base=next(r for r in rows if r['central_density_ratio']==row['central_density_ratio'] and r['basis_gaussians']==14)
 check('quadrature refinement',abs(row['direct_quotient']-base['direct_quotient'])<1e-6*max(1,abs(row['direct_quotient'])))
for x in [.1,.8]:
 check('analytically positive branch agrees with Ritz',all(r['direct_quotient']>0 for r in rows if r['central_density_ratio']==x))
tcrit=(math.sqrt(19/3)-1)/2;xcrit=math.sqrt(1/tcrit**2-1)
out=dict(all_pass=all(c['passed'] for c in checks),checks=checks,rows=rows,refined=refined,
 sufficient_radial_stability_central_density_ratio=xcrit,
 non_claims=['Ritz values are upper bounds, not fully converged eigenvalues',
 'Positive Ritz values alone do not prove stability',
 'Pressure-only barotropic fluid; no reacting field, kinetic stress or quantum gradients'])
(p/'portal_radial_modes_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2));print('Checks',len(checks));assert out['all_pass']
