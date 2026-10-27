"""Independent finite-difference Newton check; no import of BVP implementation."""
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

checks = []


def ck(name, value, detail=None):
    checks.append(dict(name=name,passed=bool(value),detail=detail))
    if not value:
        raise AssertionError((name,detail))


def finite_difference(R,d,n,manufactured=False,angular=True):
    lo,hi=1e-5,max(300.,30*d/R)
    t=np.linspace(math.log(lo),math.log(hi),n);h=t[1]-t[0];x=np.exp(t)
    if manufactured:
        exact=.4*x/(1+x*x)
        lap=-.8*x*(x*x+5)/(1+x*x)**3
        source=-d*lap+exact**2/(1-exact)
        left,right=exact[0],exact[-1]
    else:
        source=R*R*x/(1+x*x)**1.5
        left,right=0.,R/hi-(R*R/2+d)/hi**2
    v=2*source/(np.sqrt(source*source+4*source)+source)
    v*=np.sqrt(x/(x+min(1.,math.sqrt(d))))
    v[0],v[-1]=left,right
    lower=-d*(1/h**2-1/(2*h))
    upper=-d*(1/h**2+1/(2*h))
    central=d*(2/h**2+(2 if angular else 0))

    def residual(u):
        return lower*u[:-2]+central*u[1:-1]+upper*u[2:]+x[1:-1]**2*(u[1:-1]**2/(1-u[1:-1])-source[1:-1])

    for step in range(80):
        res=residual(v)
        scale=1+np.max(x[1:-1]**2*source[1:-1])
        if np.max(np.abs(res))/scale < 3e-10:
            break
        w=v[1:-1]
        derivative=w*(2-w)/(1-w)**2
        jac=diags([np.full(n-3,lower),central+x[1:-1]**2*derivative,np.full(n-3,upper)],[-1,0,1],format='csc')
        delta=spsolve(jac,-res)
        factor=1.
        for _ in range(40):
            trial=v.copy();trial[1:-1]+=factor*delta
            if np.all((trial[1:-1]>0)&(trial[1:-1]<1)) and np.max(np.abs(residual(trial))) < np.max(np.abs(res)):
                v=trial;break
            factor*=.5
        else:
            raise RuntimeError('Newton line search failed')
    else:
        raise RuntimeError('Newton iteration bound exceeded')
    ck('finite-difference residual',np.max(abs(residual(v)))/scale<3e-10)
    if manufactured:
        return float(np.max(abs(v-exact))),step
    return float(np.interp(math.log(4/3),t,v)),step


src=json.loads(Path('sol61_push/cold_advance_2026_10_18/extended_source/run_001/results.json').read_text())
rows=[]
for row in src['rows']:
    if row['name'] not in ['Fornax','Leo I'] or row['L_pc'] not in [100.,300.]:
        continue
    R=row['R_rM_over_a']
    obj=next(x for x in json.loads(Path('sol61_push/cold_final_mile_2026_10_13/run_077/results.json').read_text())['dwarfs'] if x['name']==row['name'])
    a=.75*obj['r12_pc'];d=row['L_pc']**2/(2*a*a)
    coarse,it=finite_difference(R,d,2401)
    fine,it2=finite_difference(R,d,4801)
    err=abs(fine/row['aperture_U']-1)
    ck('independent discretization versus BVP '+row['name']+row['footing']+str(row['L_pc']),err<5e-5,err)
    ck('mesh refinement',abs(fine-coarse)<5e-5*row['aperture_U'])
    rows.append(dict(name=row['name'],footing=row['footing'],L_pc=row['L_pc'],relative_error=err,newton_iterations=[it,it2]))
for d in [.01,1.,100.]:
    error,_=finite_difference(.3,d,4801,True)
    ck('manufactured exact vector solution d='+str(d),error<3e-6,error)
wrong,_=finite_difference(.3,1.,4801,True,False)
ck('missing vector angular term is detected',wrong>1e-3,wrong)
out=dict(checks=checks,n_checks=len(checks),independent_rows=rows,angular_mutation_max_error=wrong,
         scope='Independent finite-difference Newton solver, eight BVP comparisons, three manufactured solutions and one angular-term mutation; finite floating evidence only')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
