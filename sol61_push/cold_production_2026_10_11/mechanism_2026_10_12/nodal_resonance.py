"""Second-sheet pole continuation of the isotropic gapless kernel."""
from pathlib import Path
import json, math, cmath
import numpy as np
from scipy.optimize import root
P=Path(__file__).parent
checks={};rows=[]
eta=math.pi**2/16;b=math.pi/12
def F(z):return math.pi*(1-z*z)/4-0.5j*(z-(1-z*z)*cmath.atanh(z))
def determinant(k,w):
    pi=math.pi*k/4*F(w/k)
    return -w*w+(k*k-w*w)*(pi-w*w)
for k in [.0001,.001,.01,.1,.3,1.]:
    scale=math.sqrt(eta)*k**1.5
    # Root unknown normalized by the expected soft frequency.
    def fun(t):
        d=determinant(k,scale*complex(t[0],t[1]))/scale**2
        return [d.real,d.imag]
    guess=[1.,-b*eta*k**3/(2*scale)]
    sol=root(fun,guess,tol=1e-10)
    w=scale*complex(*sol.x)
    residual=abs(determinant(k,w))/scale**2
    checks[f'residual_{k}']=residual<1e-10
    checks[f'converged_{k}']=bool(sol.success)
    checks[f'damped_pole_{k}']=w.real>0 and w.imag<0 and abs(w/k)<1
    rows.append(dict(k=k,real_frequency=w.real,damping=-w.imag,damping_over_frequency=-w.imag/w.real,relative_residual=residual))
result=dict(checks=checks,all_pass=all(checks.values()),rows=rows,scope='Analytic continuation of upper-rim retarded expression through 0<Re(omega)/k<1 to the resonance sheet. These are decaying resonances, not complex eigenvalues of the finite conservative bath or a global pole count.')
(P/'nodal_resonance_run'/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));assert result['all_pass']
