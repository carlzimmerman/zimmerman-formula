import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,cumulative_trapezoid
from scipy.optimize import brentq
from scipy.special import roots_legendre
from scipy.stats import qmc
p=Path(__file__).parent
refs=json.load(open(p/'cold_limit_run/results.json'))['rows'];omega=json.load(open(p/'cold_spectrum_run/results.json'))['spectra'][-1]['omega'][0]
rows=[]
for ref in refs:
 A=ref['A'];pc=ref['Psi_c'];r0=1e-6
 def fun(r,y):
  m,psi=y;q=m/r**2;rho=A*max(psi,0)**2.5/(1+r*r);chi=2.5*rho/psi if psi>0 else 0
  return [r*r*rho,(q*q/(1-q)-r/(1+r*r)**1.5+.02*r*rho/(1+r*r))/(1+.01*chi)]
 def edge(r,y):return y[1]
 edge.terminal=True;edge.direction=-1
 sol=solve_ivp(fun,[r0,100],[A*pc**2.5*r0**3/3,pc],rtol=2e-13,atol=2e-16,events=edge,dense_output=True,max_step=.05)
 R=sol.t[-1];rr=np.linspace(r0,R,80001);mm,psi=sol.sol(rr);rho=A*np.maximum(psi,0)**2.5/(1+rr*rr);cdf=cumulative_trapezoid(rr*rr*rho,rr,initial=0);cdf/=cdf[-1]
 u=qmc.Sobol(3,scramble=False).random_base2(10);u=(u*1023+.5)/1024
 r=np.interp(u[:,0],cdf,rr);pp=sol.sol(r)[1];ss=np.linspace(0,1,30001);speeds=np.sqrt(2*pp)*np.interp(u[:,1],(5*ss**3-3*ss**5)/2,ss)
 vr=speeds*u[:,2];vt=speeds*np.sqrt(1-u[:,2]**2)/np.sqrt(1+r*r);L=r*vt;E=.5*(vr*vr+vt*vt)-pp
 omegas=[];errors=[];turnerrs=[]
 for radius,l,e in zip(r,L,E):
  def v2(x):return 2*(e+sol.sol(x)[1])-l*l/x**2
  rp=brentq(v2,r0,radius,xtol=1e-13);ra=brentq(v2,radius,R,xtol=1e-13)
  vals=[]
  for order in [64,128]:
   nodes,w=roots_legendre(order);theta=(nodes+1)*np.pi/4;x=rp+(ra-rp)*np.sin(theta)**2
   speed2=v2(x)
   if min(speed2)<=0:raise RuntimeError('quadrature reached nonpositive speed')
   half=np.sum(w*(ra-rp)*np.sin(2*theta)/np.sqrt(speed2))*np.pi/4;vals.append(np.pi/half)
  omegas.append(vals[-1]);errors.append(abs(vals[0]/vals[1]-1));turnerrs.extend([abs(v2(rp)),abs(v2(ra))])
 o=np.array(omegas)
 rows.append(dict(A=A,mass=float(sol.y[0,-1]),edge=float(R),omega_quantiles=np.quantile(o,[0,.01,.1,.5,.9,.99,1]).tolist(),max_quadrature_error=max(errors),max_turning_residual=max(turnerrs),fraction_within_5pct_of_cold_mode={str(n):float(np.mean(abs(n*o/omega-1)<.05)) for n in range(1,9)},omega_samples=o.tolist()))
checks=dict(mass=all(abs(x['mass']-1)<1e-5 for x in rows),quadrature=all(x['max_quadrature_error']<1e-4 for x in rows),turning=all(x['max_turning_residual']<1e-8 for x in rows))
out=dict(cold_collective_omega=omega,quantile_levels=[0,.01,.1,.5,.9,.99,1],checks=checks,all_pass=all(checks.values()),rows=rows,scope='finite orbit sample and harmonic proximity; not spectral support proof or damping rate')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps({**out,'rows':[{k:v for k,v in r.items() if k!='omega_samples'} for r in rows]},indent=2));sys.exit(0 if out['all_pass'] else 1)
