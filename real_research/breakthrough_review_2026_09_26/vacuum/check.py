#!/usr/bin/env python3
"""Exact algebra for CA5-GNC-R; no complete field-theory certification."""
import argparse
import json
import math
from pathlib import Path
import sympy as sp

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
args = parser.parse_args()
checks = []
def zero(name, expr):
    value = sp.factor(expr)
    assert value == 0, (name, value)
    checks.append(name)

t, d = sp.symbols('t d', positive=True)
F = 1+(t+1/t-2)**2
zero('quartic_barrier', F-1-(t-1)**4/t**2)
zero('reciprocal_invariance', F-F.subs(t,1/t))
zero('first_derivative', sp.diff(F,t)-2*(t-1)**3*(t+1)/t**3)
zero('convexity_factor', sp.diff(F,t,2)-2*(t-1)**2*(t*t+2*t+3)/t**4)
zero('third_derivative', sp.diff(F,t,3)-24*(t-1)/t**5)
zero('vacuum_value', F.subs(t,1)-1)
for n in range(1,4):
    zero('flat_derivative_'+str(n), sp.diff(F,t,n).subs(t,1))
zero('fourth_derivative_24', sp.diff(F,t,4).subs(t,1)-24)
assert sp.limit(F,t,0,dir='+') == sp.oo
assert sp.limit(F,t,sp.oo) == sp.oo
checks.extend(['barrier_zero_limit','barrier_infinity_limit'])
Fd=F.subs(t,d)+sp.diff(F,t).subs(t,d)*(t-d)+sp.diff(F,t,2).subs(t,d)*(t-d)**2/2
zero('Taylor_remainder_factor', F-Fd-(t-d)**3*(4*d*t-d-3*t)/(d**4*t**2))
for n in range(3):
    zero('Taylor_join_'+str(n), (sp.diff(F,t,n)-sp.diff(Fd,t,n)).subs(t,d))
aa,bb,cc=sp.symbols('aa bb cc',real=True)
L=aa*(t*t+t**-2)+bb*(t+t**-1)+cc
sol=sp.solve([L.subs(t,1)-1,sp.diff(L,t,2).subs(t,1)], [bb,cc])
zero('minimal_Laurent_ansatz', L.subs(sol)-1-aa*(F-1))
p,v,W,V0=sp.symbols('p v W V0',real=True)
E=(p*p/2+W)/t+V0*F
dp,dt=sp.symbols('dp dt',real=True)
hessian=sp.diff(E,p,2)*dp**2+2*sp.diff(E,p,t)*dp*dt+sp.diff(E,t,2)*dt**2
zero('perspective_Hessian', hessian-((dp-p*dt/t)**2/t+(2*W/t**3+V0*sp.diff(F,t,2))*dt**2))
K,H,x,dd,ddx=sp.symbols('K H x dd ddx',positive=True)
D=x*dd
den=K*H*H+D
CI=2*x*D/den-4*x*x/den-4*K*H*H*x*x*(dd+x*ddx)/den**2
fact=-2*x*x/den**2*(K*H*H*(2+dd+2*x*ddx)+x*dd*(2-dd))
zero('integrated_stiffness_factor',CI-fact)
alpha,r0,S,xi=sp.symbols('alpha r0 S xi',positive=True)
r=r0*S
alphae=2-(2-alpha)*(1-r)**2
f1,f2=sp.symbols('f1 f2',real=True)
Dgeneral=alphae*x-6*H*H*r*(f1+f2*r/2)
zero('flat_vacuum_D',Dgeneral.subs({f1:0,f2:0})-alphae*x)
zero('PQ_comparison',Dgeneral.subs({f1:-1,f2:2/r0})-(alphae*x+6*H*H*r0*S*(1-S)))
zero('general_IR_condition',Dgeneral.subs({x:0,S:1,f2:-2*f1/r0}))
u=sp.symbols('u',positive=True)
du=alphae.subs(S,sp.exp(-u))
zero('logarithmic_derivative',2*u*sp.diff(du,u)+4*(2-alpha)*u*r0*sp.exp(-u)*(1-r0*sp.exp(-u)))
# A derivative-cancellation mutant is not silently accepted.
mutant=1/t
assert sp.diff(mutant,t).subs(t,1) == -1
assert sp.diff(mutant,t,2).subs(t,1) == 2
assert sp.simplify((-6*H*H*r0*(f1+f2*r0/2)).subs({f1:-1,f2:2})) != 0
checks.append('old_reciprocal_floor_fails_flatness_control')

# Deterministic finite regression across wide H xi, not the all-mode proof.
rows=[]
for av in (0.01,0.5,1.99):
 for ell in (0.1,1.0):
  rv=ell/4
  for hv,xiv in ((0.01,0.01),(1.0,1.0),(100.0,100.0)):
   for uv in (1e-5,0.01,0.5,2.,30.):
    sv=math.exp(-uv); rr=rv*sv; xv=2*uv/xiv**2
    dv=2-(2-av)*(1-rr)**2
    log_der=-4*(2-av)*uv*rr*(1-rr)
    kv=10.; ev=kv*hv*hv+xv*dv
    A=kv*xv*dv/ev
    C=-2*xv*xv/ev**2*(kv*hv*hv*(2+dv+log_der)+xv*dv*(2-dv))
    assert A>0 and C<0 and 2+dv+log_der>=1
    rows.append({'alpha':av,'ell':ell,'H':hv,'xi':xiv,'u':uv,'A':A,'CI':C})
out={'claim':'CD26_5_RECIPROCAL_VACUUM','exact_checks':checks,
     'exact_check_count':len(checks),'regression_count':len(rows),
     'regression_min_A':min(z['A'] for z in rows),
     'regression_max_CI':max(z['CI'] for z in rows),
     'regressions':rows,
     'scope':'Symbolic identities plus finite floating controls; analytic elliptic and all-q proofs are separate; no full gravity closure.'}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['claim','exact_check_count','regression_count','regression_min_A','regression_max_CI']}))
