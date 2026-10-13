"""Leading isotropized gapped gradient energy and far-field correction."""
from pathlib import Path
import json
import sympy as s
import numpy as np
from scipy.integrate import quad
P=Path(__file__).parent
r,B,c=s.symbols('r B c',positive=True)
p=s.Function('p')(r);dp=s.diff(p,r)
L=r*r*c*(dp*dp/(18*p)+p/(6*r*r))
EL=s.simplify((s.diff(L,p)-s.diff(s.diff(L,dp),r))/(r*r))
on_profile=s.simplify(EL.subs({s.diff(p,r,2):2*B/r**3,dp:-B/r**2,p:B/r}))
checks={'radial_variation':s.simplify(on_profile-2*c/(9*r*r))==0}
# Cutoff-free closed patch response; verify low-q coefficients numerically.
for m in [.1,1.,10.]:
 q=1e-3*m
 par=(q*q+4*m*m)/(2*q)*np.arctan(q/(2*m))-m
 trans=q/2*np.arctan(q/(2*m))
 checks[f'longitudinal_gradient_{m}']=bool(abs(par/(q*q/(6*m))-1)<1e-6)
 checks[f'transverse_gradient_{m}']=bool(abs(trans/(q*q/(4*m))-1)<1e-6)
rows=[]
# Independent compact-support finite variation, c=1; endpoints and derivatives vanish.
def f(x):return np.sin(np.pi*(x-1)/4)**2
def fd(x):return np.pi/4*np.sin(np.pi*(x-1)/2)
predicted=quad(lambda x:2*f(x)/9,1,5,epsabs=1e-12)[0]
for b in [3.,10.,30.]:
 def energy(eps):
  return quad(lambda x:x*x*((-b/x**2+eps*fd(x))**2/(18*(b/x+eps*f(x)))+(b/x+eps*f(x))/(6*x*x)),1,5,epsabs=1e-12)[0]
 eps=1e-5
 numeric=(energy(eps)-energy(-eps))/(2*eps)
 checks[f'energy_variation_{b}']=bool(abs(numeric/predicted-1)<1e-7)
 rows.append(dict(hB_over_v=b,gradient_to_cubic=2/(9*b*b),higher_gradient_expansion_parameter=1/(b*b)))
checks={k:bool(v) for k,v in checks.items()}
result=dict(checks=checks,all_pass=all(checks.values()),Euler_Lagrange=str(EL),profile_force=str(on_profile),rows=rows,
scope='Leading two-spatial-derivative expansion, gapped zero-T/mu medium, isotropic ring orientation and equal speeds; large hB/v only, not central solution or global dynamics.')
(P/'nodal_gapped_run'/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));assert result['all_pass']
