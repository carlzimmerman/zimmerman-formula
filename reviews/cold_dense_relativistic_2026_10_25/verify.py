import json,math,argparse
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
z,w=np.polynomial.legendre.leggauss(512);theta=(z+1)*math.pi/4

def eos(E):
 amp=2*math.acos(1/math.sqrt(1.2+math.sqrt(E/10)));q=amp*np.sin(theta);U=10*(1/np.cos(q/2)**2-1.2)**2;wt=w*amp*np.cos(theta)/np.sqrt(2*(E-U));return 2*np.sum(wt*(E-U))/np.sum(wt)-E
E0=brentq(eos,.41,1.)
slopes=[(eos(E0*(1+h))-eos(E0*(1-h)))/(2*E0*h) for h in [1e-3,1e-4,1e-5]]
assert min(slopes)>1.07 and max(slopes)-min(slopes)<2e-5
cross=brentq(lambda E:(eos(E*1.0001)-eos(E*.9999))/(.0002*E)-1,.51,.6)
controls=[]
for vac in [0.,1.6]:
 E=10.;R=.2;B=(E-2*vac)/3;aa=2*(E+vac)/3;fs=math.sqrt(1-aa*R*R)
 def analytic(x):
  ff=np.sqrt(1-aa*x*x);return B*E*(ff-fs)/(E*fs-B*ff)
 x0=1e-7
 def rhs(x,y):
  mu,pr=y;return [x*x*E,-(E+pr)*(mu+x**3*(pr-2*vac/3))/(x*x*(1-2*mu/x-2*vac*x*x/3))]
 grid=np.linspace(x0,R,501)
 sol=solve_ivp(rhs,[x0,R],[E*x0**3/3,float(analytic(x0))],t_eval=grid,rtol=2e-11,atol=1e-13,method='DOP853',max_step=.002)
 assert sol.success
 err=float(max(abs(sol.y[1]-analytic(grid))));masserr=float(max(abs(sol.y[0]-E*grid**3/3)))
 assert err<1e-8 and masserr<1e-10
 controls.append(dict(vacuum=vac,max_pressure_error=err,max_mass_error=masserr))
result=dict(surface_energy=E0,surface_derivative_checks=slopes,unit_slope_crossing_E=cross,pressure_at_unit_slope=eos(cross),constant_density_controls=controls)
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
