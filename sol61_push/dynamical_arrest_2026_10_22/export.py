import json,argparse
from pathlib import Path
import numpy as np
from scipy.special import roots_legendre
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);a=pa.parse_args();checks=[]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=str(v)));print(n,b,v)
x,w=roots_legendre(80);angular=2*np.pi*np.dot(w,1-x*x)
ck('curl_angular_factor',abs(angular/(8*np.pi/3)-1)<1e-12,angular)
# Direct scalar outgoing real field X=A cos(kr-omega t)/r.
omega,k,D,A,r=2.,.7,3.,.4,11.;ph=np.linspace(0,2*np.pi,4096,endpoint=False)
Xt=A*omega*np.sin(ph)/r;Xr=-A*k*np.sin(ph)/r-A*np.cos(ph)/r**2
flux=4*np.pi*r*r*np.mean(-D*Xt*Xr);expected=2*np.pi*D*omega*k*A*A
ck('outgoing_flux_phase_average',abs(flux/expected-1)<1e-12,flux)
rows=[]
for rr in [.1,1,10]:
 for om in [.5,.99,1,1.01,2,10]:
  kk=np.sqrt(max(0,om*om-1));power=om*kk**3*rr**6*np.exp(-(kk*rr)**2)*(2*np.pi)**3/(12*np.pi)
  rows.append(dict(R=rr,omega_over_gap=om,kR=kk*rr,power_units_source_squared=float(power)))
ck('subgap_no_outgoing_flux',all(z['power_units_source_squared']==0 for z in rows if z['omega_over_gap']<=1),'evanescent or threshold')
ks=np.array([1e-4,2e-4]);pp=np.sqrt(1+ks**2)*ks**3*np.exp(-ks**2)
ck('curl_threshold_cubic',abs(pp[1]/pp[0]-8)<1e-6,pp[1]/pp[0])
limits=[]
for n in [1,2,3]:
 for eps in [.02,.05,.1]:
  c=((1-eps)**-2-1)/n;ymin=2/(3+c);qq=c*ymin
  limits.append(dict(n=n,speed_tolerance=eps,minimum_stable_y=ymin,q_at_boundary=qq))
ck('phase_curve_intersection',all(abs(3*z['minimum_stable_y']+z['q_at_boundary']-2)<1e-12 for z in limits),limits)
# Witness: a weak-coupling stable phase with a 10% chi shift and small local curve correction.
y,q=.9,.01;ratio=1/np.sqrt(1+2*q/y)
ck('surviving_weak_drive',3*y+q>2 and ratio>.95,dict(y=y,q=q,speed_ratio=ratio))
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(dict(checks=checks,radiation=rows,phase_curve_limits=limits),indent=2)+'\n');raise SystemExit(0 if all(z['passed'] for z in checks) else 1)
