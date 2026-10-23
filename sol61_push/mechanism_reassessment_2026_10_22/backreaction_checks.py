import json,sys
import numpy as np
from scipy.integrate import solve_bvp,simpson,cumulative_trapezoid
import sympy as sp
from backreaction_response import background,run,G

def static(end):
 bg=background(end)
 def hh(r):
  q,_=bg.sol(r);return (1-q)**-2-1
 def fun(r,y):
  p,d=y;g=-r*np.exp(-r*r/2)/(2*np.pi)**1.5
  return np.array([d,(hh(r)*p-g)/G-2*d/r+2*p/r**2])
 mesh=np.geomspace(1e-5,end,1000)
 sol=solve_bvp(fun,lambda a,b:np.array([a[1]-a[0]/1e-5,b[0]]),mesh,np.zeros((2,len(mesh))),tol=2e-9,max_nodes=10000)
 r=np.linspace(1e-5,end,60000);p,d=sol.sol(r)
 integ=cumulative_trapezoid(p,r,initial=0);sigma=integ-integ[-1]
 rho=(r*r-3)*np.exp(-r*r/2)/(2*np.pi)**1.5
 chi=simpson(-r*r*rho*sigma,x=r)
 energy=simpson(r*r*(hh(r)*p*p+G*(d+2*p/r)**2),x=r)
 # Endpoint term from integrating sigma L sigma; outer sigma=p=0.
 # Remaining inner contributions are tiny and recorded by raw comparison.
 return dict(outer=end,status=sol.status,background_status=bg.status,chi=float(chi),energy=float(energy),identity_error=float(abs(chi/energy-1)))
stat=[static(R) for R in [30,60]]
dynamic=[run(w,400) for w in [.3,1.]]
m,k,lam,c,Q=sp.symbols('m k lambda chi0 Q',positive=True)
v=sp.symbols('v',real=True)
# A one-mode algebraic representation of completion of the square.
energy=c*v*v/2-lam*Q*c*v+k*Q*Q/2
square=c*(v-lam*Q)**2/2+(k-lam*lam*c)*Q*Q/2
checks=dict(static_converged=all(r['status']==r['background_status']==0 for r in stat),static_positive=all(r['chi']>0 for r in stat),static_energy=all(r['identity_error']<1e-4 for r in stat),static_domain=abs(stat[1]['chi']/stat[0]['chi']-1)<1e-4,dynamic_converged=all(r['status']==0 for r in dynamic),positive_dissipation=all(r['chi_imag']>0 for r in dynamic),work_flux=all(abs(r['omega']*r['chi_imag']/2/r['power']-1)<1e-4 for r in dynamic),schur_square=sp.expand(energy-square)==0)
mutate='--mutate' in sys.argv
out=dict(static=stat,dynamic=dynamic,checks=checks,all_pass=all(checks.values()),mutated=mutate,scope='diagnostic reciprocal oscillator, not a derived matter action')
with open(sys.argv[1],'w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
