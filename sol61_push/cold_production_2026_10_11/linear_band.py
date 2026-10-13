"""Independent monodromy checks of the exact n=1 Lame reduction."""
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import ellipj, ellipk

u=0.001
checks=[]; rows=[]
def check(name,passed,value=None):
    checks.append(dict(name=name,passed=bool(passed),value=value))

def monodromy(eps,p2,scale=1.0,tol=2e-12):
    A=1+eps; am1=eps*(2+eps); modulus2=2*am1/(1+am1)
    T=4*ellipk(modulus2)/A
    w=math.sqrt((1+p2)/(4*(1+u*u)))
    def rhs(t,z):
        sn=ellipj(A*t/2,modulus2)[0]
        delta=scale*am1/2*(1-2*sn*sn)
        si,co=math.sin(w*t),math.cos(w*t)
        L=delta*np.array([[si*co/w,si*si/(w*w)],[-co*co,-co*si/w]])
        return (L@z.reshape(2,2)).ravel()
    sol=solve_ivp(rhs,(0,T),np.eye(2).ravel(),method='DOP853',
                  rtol=tol,atol=tol/100,max_step=T/80)
    si,co=math.sin(w*T),math.cos(w*T)
    R=np.array([[co,si/w],[-w*si,co]])
    F=R@sol.y[:,-1].reshape(2,2)
    determinant=float(np.linalg.det(F))
    # Avoid trace^2-4 cancellation near a multiplier +1 or -1.
    disc=float(((F[0,0]-F[1,1])/2)**2+F[0,1]*F[1,0])
    growth=math.asinh(math.sqrt(max(0,disc)/determinant))/T
    return growth,disc,abs(determinant-1),bool(sol.success)

for eps in [1e-7,1e-5,1e-3,0.1]:
    am1=eps*(2+eps); width=(1+u*u)*am1
    lo=u*u-width; hi=u*u+width
    points=[('band_offset_'+str(b),u*u+b*width) for b in [-1.5,-.5,0,.5,1.5]
            if u*u+b*width>=0]
    points += [('higher_p2_'+str(p),p) for p in [0.01,1.,3.,8.,15.]]
    for name,p2 in points:
        growth,disc,deterr,success=monodromy(eps,p2)
        expected=lo<p2<hi
        check(f'{eps} {name}: integration',success)
        check(f'{eps} {name}: symplectic determinant',deterr<2e-10,deterr)
        check(f'{eps} {name}: exact band sign',disc>0 if expected else disc<=0,disc)
        rows.append(dict(epsilon=eps,p2_over_m2=p2,band_lower=lo,band_upper=hi,
                         predicted_exponential_growth=expected,
                         growth_per_Mt=growth,discriminant=disc))
g,disc,err,ok=monodromy(1e-7,u*u,scale=0)
check('zero-modulation control',g==0 and ok)
g0=next(r['growth_per_Mt'] for r in rows if r['epsilon']==1e-7 and r['p2_over_m2']==u*u)
g1,_,_,_=monodromy(1e-7,u*u,tol=2e-13)
check('weak-band tighter integration',abs(g1-g0)<1e-10,abs(g1-g0))
out=dict(rows=rows,checks=checks,all_pass=all(c['passed'] for c in checks),
         conventions='tau=M t; physical p/m; elliptic parameter is modulus squared',
         non_claims=['No expansion','No source depletion or nonlinear rescattering',
                     'Numerical samples do not prove the complete band theorem'])
(Path(__file__).parent/'linear_band_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print('Checks:',len(checks),'all pass:',out['all_pass'])
for r in rows:
    if r['p2_over_m2']==u*u: print(json.dumps(r))
assert out['all_pass']
