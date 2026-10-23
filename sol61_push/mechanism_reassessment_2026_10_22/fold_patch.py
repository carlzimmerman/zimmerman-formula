"""Local, single-counted resonance-curve integrals for a prescribed dilation potential."""
import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.special import roots_legendre
from scipy.optimize import brentq
p=Path(__file__).parent
# Execute only background and orbit definitions, never the prior experiment loop.
ns={'__file__':str(p/'direct_folds_v2.py'),'__name__':'background'}
exec((p/'direct_folds_v2.py').read_text().split('gx,_=roots_legendre(128)')[0],ns)
sol=ns['sol'];R=ns['R'];r0=ns['r0'];omega=ns['omega'];geometry=ns['geometry'];psi=ns['psi'];rhs=ns['rhs'];A=ns['A']
r=np.linspace(r0,R,80001);m,pp=sol.sol(r);rho=A*np.maximum(pp,0)**2.5/(1+r*r);dp=np.array([rhs(float(x),y)[1] for x,y in zip(r,sol.sol(r).T)]);drho=2.5*A*np.maximum(pp,0)**1.5*dp/(1+r*r)-2*r*rho/(1+r*r);q=m/r**2
integ=cumulative_trapezoid(q*(2-q)/(1-q)**2*r*rho,r,initial=0);phi=-(integ[-1]-integ)-.01*(3*rho+r*drho);phi/=max(abs(phi));F=15*A/(2**4.5*np.pi)
def coefficient(e,u,n,count):
 rc=geometry(u)[0]
 def v2(x):return 2*(e+psi(x))-u/x**2
 rp=brentq(v2,r0,rc,xtol=1e-14);ra=brentq(v2,rc,R,xtol=1e-14)
 theta=(np.arange(count)+.5)*np.pi/(2*count);x=rp+(ra-rp)*np.sin(theta)**2;w=(ra-rp)*np.sin(2*theta)/np.sqrt(v2(x));phase=np.pi*(np.cumsum(w)-w/2)/w.sum()
 return np.sum(w*np.interp(x,r,phi)*np.cos(n*phase))/w.sum()
refs=[x for x in json.load(open(p/'direct_folds_v2_run/results.json'))['rows'] if x['quadrature']==128];rows=[]
for ref in refs:
 n=ref['harmonic'];uc=ref['u'];ec=ref['energy'];halfwidth=1e-4
 for order,count,frac in [(16,1024,1e-4),(32,2048,5e-5),(64,2048,5e-5)]:
  gx,gw=roots_legendre(order);terms=[];unit=[];res=[];slopes=[];couplings=[];us=[]
  for e in ec+halfwidth*gx:
   u=brentq(lambda u:n*omega(e,u,geometry(u)[0],128)-.8228,.9*uc,1.1*uc,xtol=1e-13)
   h=u*frac;slope=(omega(e,u+h,geometry(u+h)[0],128)-omega(e,u-h,geometry(u-h)[0],128))/(2*h)
   c=coefficient(e,u,n,count);terms.append(c*c/abs(slope));unit.append(1/abs(slope));slopes.append(slope);couplings.append(c);us.append(u);res.append(abs(n*omega(e,u,geometry(u)[0],128)-.8228))
  B=float(2*np.pi**3*F*halfwidth*np.dot(gw,terms));unit_integral=float(halfwidth*np.dot(gw,unit))
  rows.append(dict(harmonic=n,energy_halfwidth=halfwidth,order=order,phase_points=count,derivative_fraction=frac,absorption_patch=B,unit_integral=unit_integral,max_residual=max(res),min_abs_slope=float(min(abs(np.array(slopes)))),coefficient_range=[float(min(couplings)),float(max(couplings))],u_range=[float(min(us)),float(max(us))]))
changes={str(n):abs([x['absorption_patch'] for x in rows if x['harmonic']==n][-1]/[x['absorption_patch'] for x in rows if x['harmonic']==n][-2]-1) for n in [5,6]}
checks=dict(resonance=all(x['max_residual']<1e-7 for x in rows),regular=all(x['min_abs_slope']>1 for x in rows),positive=all(x['absorption_patch']>0 for x in rows),integration_convergence=all(v<1e-3 for v in changes.values()))
out=dict(checks=checks,all_pass=all(checks.values()),rows=rows,relative_32_to_64_changes=changes,scope='two fixed energy patches of dilation-trial absorption only, no full matrix, full curve or pole')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
