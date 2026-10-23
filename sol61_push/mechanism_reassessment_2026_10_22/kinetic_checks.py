import numpy as np
from scipy.special import wofz
from scipy.optimize import root
import sympy as sp
import json,sys

def R(z):return 1+z*1j*np.sqrt(np.pi)*wofz(z)
def det(z,z0,J,a=1/3):return (1-(z/z0)**2)*(1-J*R(z))-a*J*R(z)
rows=[]
for z0 in [.5,1,2,5]:
 guess=z0-.001j
 for J in [.1,.5,.74]:
  def f(y):
   z=y[0]+1j*y[1];v=det(z,z0,J);return [v.real,v.imag]
  sol=root(f,[guess.real,guess.imag],tol=1e-11);z=sol.x[0]+1j*sol.x[1];guess=z
  rows.append(dict(z0=z0,J=J,success=bool(sol.success),z_real=float(z.real),z_imag=float(z.imag),residual=float(abs(det(z,z0,J)))))
sol=root(lambda y:[det(y[0]+1j*y[1],1,.8).real,det(y[0]+1j*y[1],1,.8).imag],[0,.05],tol=1e-11)
z=sol.x[0]+1j*sol.x[1]
K,D,k,J,resp,rho,s=sp.symbols('K D k J R rho s',positive=True)
# delta_rho=-rho R Phi/s², Phi=-K delta_rho/k²-K² delta_rho/D.
expr=1-rho*resp*K/s**2*(1/k**2+K/D)
identity=sp.simplify((expr*D).subs(rho,J*k*k*s*s/K)-(D*(1-J*resp)-K*k*k*J*resp))==0
beta=.02798;b=(2+3*beta)/beta;c=299792.458;disp=8.33
speed=c*np.sqrt(3/b);zbare=speed/(np.sqrt(2)*disp);beta_match=2*(disp/c)**2/(3-3*(disp/c)**2)
checks=dict(elimination=identity,static_threshold=abs(det(0,1,.75))<1e-14,zero_density=all(abs(det(x,x,0))<1e-14 for x in [.5,1,2,5]),mode_residuals=all(r['residual']<1e-9 for r in rows),field_roots_damped=all(r['z_imag']<0 for r in rows),jeans_growth=abs(det(z,1,.8))<1e-9 and z.imag>0,maxwell_static_sign=abs(R(0)-1)<1e-15)
checks={k:bool(v) for k,v in checks.items()}
out=dict(checks=checks,all_pass=all(checks.values()),roots=rows,growing_root=[float(z.real),float(z.imag)],growing_residual=float(abs(det(z,1,.8))),phase_speed_km_s=speed,zbare=zbare,log10_resonant_exponential=-zbare*zbare/np.log(10),beta_speed_equals_dispersion=beta_match,scope='local Maxwellian patch; minimal coupling; not the unproved sourcing selector')
with open(sys.argv[1],'w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
