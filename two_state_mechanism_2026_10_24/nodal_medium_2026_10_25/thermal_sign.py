import argparse,json
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar

def stable_integrand(k,m):
    if k==0:return -m*m
    z=(m/k)**2
    if z<1e-4:return k*k*(-z*z/2+z**3/3-z**4/4+z**5/5)
    return k*k*np.log1p(z)-m*m
rows=[]
for m in [1e-4,.001,.01,.1]:
    integral=quad(lambda k:stable_integrand(k,m),0,1,points=[m,min(10*m,.99)],epsabs=1e-20,epsrel=1e-10)[0]
    coeff=integral/(4*np.pi*np.pi*m**3)
    rows.append(dict(M=m,subtracted_free_energy_over_TM3=coeff,target=-1/(12*np.pi),relative_asymptotic_error=abs(coeff+1/(12*np.pi))/(1/(12*np.pi))))
r=minimize_scalar(lambda y:-y*y/2+y**6/6,bounds=(0,2),method='bounded',options={'xatol':1e-13})
assert r.success and abs(r.x-1)<1e-7 and abs(r.fun+1/3)<1e-12
assert all(x['subtracted_free_energy_over_TM3']<0 for x in rows)
assert rows[0]['relative_asymptotic_error']<1e-4
out=dict(gaussian=rows,tricritical_scaled_minimum=dict(phi_over_sqrt_field=float(r.x),F_over_field_cubed=float(r.fun)),required_cubic_sign='positive',tested_cubic_sign='negative')
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
with open(a.output,'w') as f:json.dump(out,f,indent=2,allow_nan=False)
print(json.dumps(out))
