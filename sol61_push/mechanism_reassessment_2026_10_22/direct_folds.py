"""Direct orbit minima and transverse crossings; no field-response continuation."""
import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq,minimize_scalar
from scipy.special import roots_legendre
p=Path(__file__).parent
A=10000.;pc=json.load(open(p/'cold_limit_run/results.json'))['rows'][-1]['Psi_c'];r0=1e-6

def rhs(r,y):
 m,psi=y;q=m/r**2;rho=A*max(psi,0)**2.5/(1+r*r);chi=2.5*rho/psi if psi>0 else 0
 return [r*r*rho,(q*q/(1-q)-r/(1+r*r)**1.5+.02*r*rho/(1+r*r))/(1+.01*chi)]
def edge(r,y):return y[1]
edge.terminal=True;edge.direction=-1
sol=solve_ivp(rhs,[r0,100],[A*pc**2.5*r0**3/3,pc],rtol=2e-13,atol=2e-16,events=edge,dense_output=True,max_step=.05)
R=sol.t[-1]
def psi(r):return sol.sol(r)[1]
def dp(r):return rhs(r,sol.sol(r))[1]
def lc(r):return -r**3*dp(r)
rcmax=brentq(lambda r:psi(r)+(r+r**3)*dp(r)/2,r0,R);umax=lc(rcmax)
quad={k:roots_legendre(k) for k in [64,128,256]}
def geometry(u):
 rc=brentq(lambda r:lc(r)-u,r0,rcmax);return rc,-psi(rc)+u/(2*rc**2),-u/2

def omega(e,u,rc,order):
 def v2(r):return 2*(e+psi(r))-u/r**2
 rp=brentq(v2,r0,rc,xtol=1e-14);ra=brentq(v2,rc,R,xtol=1e-14)
 gx,gw=quad[order];theta=(gx+1)*np.pi/4;r=rp+(ra-rp)*np.sin(theta)**2
 speed=v2(r)
 if np.min(speed)<=0:raise ValueError('nonpositive quadrature speed')
 half=np.sum(gw*(ra-rp)*np.sin(2*theta)/np.sqrt(speed))*np.pi/4
 return np.pi/half

def minimum(u,order):
 rc,lo,hi=geometry(u);width=hi-lo
 # Uniform energy scan brackets an interior minimum; all selected crossings are away from circular limit.
 x=np.linspace(.0001,.9999,65);vals=np.array([omega(lo+t*width,u,rc,order) for t in x]);i=int(vals.argmin())
 if i in [0,len(x)-1]:raise ValueError('minimum not interior')
 opt=minimize_scalar(lambda t:omega(lo+t*width,u,rc,order),bounds=(x[i-1],x[i+1]),method='bounded',options={'xatol':1e-10})
 if not opt.success:raise ValueError('minimization failed')
 return float(opt.fun),float(lo+opt.x*width),float(width),rc

gx,_=roots_legendre(128);us=(gx+1)*umax/2;rows=[]
for n,left,right in [(5,12,14),(6,24,26)]:
 for order in [64,128,256]:
  u=brentq(lambda u:n*minimum(u,order)[0]-.8228,us[left],us[right],xtol=1e-11)
  om,e,width,rc=minimum(u,order);derivatives=[]
  for fraction in [1e-3,5e-4]:
   h=width*fraction;op=omega(e+h,u,rc,order);ominu=omega(e-h,u,rc,order)
   curvature=(op+ominu-2*om)/h**2;slope=(op-ominu)/(2*h)
   du=u*fraction;transverse=(minimum(u+du,order)[0]-minimum(u-du,order)[0])/(2*du)
   derivatives.append(dict(fraction=fraction,energy_slope=slope,energy_curvature=curvature,transverse_slope=transverse))
  rows.append(dict(harmonic=n,quadrature=order,u=u,energy=e,frequency=om,resonance_error=abs(n*om-.8228),energy_width=width,derivatives=derivatives))
checks=dict(resonance=all(r['resonance_error']<1e-7 for r in rows),positive_curvature=all(d['energy_curvature']>0 for r in rows for d in r['derivatives']),transverse=all(abs(d['transverse_slope'])>1 for r in rows for d in r['derivatives']),quadrature=all(np.ptp([r['u'] for r in rows if r['harmonic']==n])<1e-7 for n in [5,6]),curvature_steps=all(abs(r['derivatives'][0]['energy_curvature']/r['derivatives'][1]['energy_curvature']-1)<.05 for r in rows))
out=dict(checks=checks,all_pass=all(checks.values()),rows=rows,scope='two selected direct-orbit fold crossings, three quadrature orders, two derivative steps; no exhaustive branch search or pole')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
