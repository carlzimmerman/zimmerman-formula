"""Shared scalar interaction: phase identities and history-dependent mode yield."""
import argparse,json
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
checks={}
def check(name,ok):
    checks[name]=bool(ok);print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def zero(x):return s.simplify(x)==0
q,rho,alpha,ms2,lam,V0=s.symbols('q rho alpha ms2 lam V0',positive=True)
U=V0+ms2*q*q/2+lam*q**4/4
f=rho+U-alpha*rho*q*q/2
q2=(alpha*rho-ms2)/lam
check('nonzero stationary branch',zero((s.diff(f,q)/q).subs(q*q,q2)))
check('branch curvature',zero(s.diff(f,q,2).subs(q*q,q2)-2*(alpha*rho-ms2)))
fmin=rho+V0-(alpha*rho-ms2)**2/(4*lam)
check('minimized energy',zero(f.subs(q*q,q2)-fmin))
pressure=rho*s.diff(fmin,rho)-fmin
check('pressure includes density variation',zero(pressure-(-V0+(ms2**2-alpha**2*rho**2)/(4*lam))))
check('scalar-only excess energy',zero((U-V0).subs(q*q,q2)-(alpha**2*rho**2-ms2**2)/(4*lam)))
check('negative induced compressibility',zero(s.diff(pressure,rho)+alpha**2*rho/(2*lam)))
check('local phase independent of vacuum offset',zero(s.diff(q2,V0)))
wi,wf=s.symbols('wi wf',positive=True)
A=(s.sqrt(wf/wi)+s.sqrt(wi/wf))/2
B=(s.sqrt(wf/wi)-s.sqrt(wi/wf))/2
if args.mutate:B=-B
check('quench field continuity',zero((A+B)/s.sqrt(2*wf)-1/s.sqrt(2*wi)))
check('quench derivative continuity',zero(wf*(A-B)/s.sqrt(2*wf)-wi/s.sqrt(2*wi)))
check('Bogoliubov normalization',zero(A*A-B*B-1))
check('quench occupation',zero(B*B-(wf-wi)**2/(4*wi*wf)))
check('equal masses no quench production',zero(B.subs(wf,wi)))
r,ms,C=s.symbols('r ms C',positive=True)
tail=C*s.exp(-ms*r)/r
check('linear exterior field equation',zero(s.diff(tail,r,2)+2*s.diff(tail,r)/r-ms*ms*tail))
check('exterior fifth force',zero(alpha*tail*s.diff(tail,r)+alpha*C*C*s.exp(-2*ms*r)*(ms/r**2+1/r**3)))
runs=[]
for tau in [.05,.5,5.]:
    pair=[]
    for tol in [1e-9,1e-11]:
        def ode(t,y):
            w2=1+1.5*(1+np.tanh(t/tau))
            return np.array([y[1],-w2*y[0]])
        sol=solve_ivp(ode,(-12*tau,12*tau),np.array([1/np.sqrt(2),-1j/np.sqrt(2)]),method='DOP853',rtol=tol,atol=tol/100,max_step=min(tau/20,.1))
        u,du=sol.y[:,-1]
        N=(abs(du)**2+4*abs(u)**2)/4-.5
        W=u*du.conjugate()-u.conjugate()*du
        check(f'{tau} {tol} mode integration',sol.success)
        check(f'{tau} {tol} canonical Wronskian',abs(W-1j)<1e-7)
        pair.append({'tau':tau,'rtol':tol,'occupation':float(N),'wronskian_error':float(abs(W-1j))})
    check(f'{tau} occupation convergence',abs(pair[0]['occupation']-pair[1]['occupation'])<1e-7)
    runs.extend(pair)
fine=[r for r in runs if r['rtol']==1e-11]
check('same endpoints different production',fine[-1]['occupation']<fine[0]['occupation']/100)
Path(args.out).write_text(json.dumps({'checks':checks,'passed':all(checks.values()),'runs':runs,'instantaneous_occupation_wi1_wf2':.125,'mutated':args.mutate},indent=2)+'\n')
raise SystemExit(0 if all(checks.values()) else 1)
