"""Conditional baryonic loading and thin-wall phase tests; no MOND target input."""
import argparse
import json
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s

ap=argparse.ArgumentParser()
ap.add_argument('--out',required=True)
ap.add_argument('--mutate',action='store_true')
a=ap.parse_args()
checks={}
def check(name,ok):
    checks[name]=bool(ok)
    print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def zero(expr):
    return s.simplify(expr)==0
phi,v,lam,D,V0=s.symbols('phi v lam D V0',positive=True)
z=s.symbols('z',real=True)
q=(2+3*z-z**3)/4
V=V0+lam*(phi**2-v**2)**2/4+D*q.subs(z,phi/v)
check('phase values',zero(V.subs(phi,v)-V.subs(phi,-v)-D))
check('both phase derivatives vanish',all(zero(s.diff(V,phi).subs(phi,e*v)) for e in [-1,1]))
check('phase curvatures',all(zero(s.diff(V,phi,2).subs(phi,e*v)-(2*lam*v**2-e*3*D/(2*v**2))) for e in [-1,1]))
R,Sigma,eps,c,rhob,P=s.symbols('R Sigma eps c rhob P',positive=True)
Mb=s.Function('Mb')(R)
E=4*s.pi*Sigma*R**2+4*s.pi*D*R**3/3+eps*c**2*Mb
wall=s.diff(E,R)/(4*s.pi*R**2)
claimed=( -D if a.mutate else D)+2*Sigma/R+eps*c**2*rhob
check('wall pressure sign and baryon surface term',zero(wall.subs(s.diff(Mb,R),4*s.pi*R**2*rhob)-claimed))
De=s.symbols('De',nonzero=True)
Eb=4*s.pi*Sigma*R**2+4*s.pi*De*R**3/3
check('critical bubble is a radial maximum',zero(s.diff(Eb,R,2).subs(R,-2*Sigma/De)+8*s.pi*Sigma))
check('vacuum additive offset cancels from phase splitting',zero(s.diff(V.subs(phi,v)-V.subs(phi,-v),V0)))
N,kT,Vs=s.symbols('N kT Vs',positive=True)
Vol=4*s.pi*R**3/3
F=N*kT*(s.log(N/Vol)-1)+D*Vol+4*s.pi*Sigma*R**2
check('fixed inventory variation yields pressure balance',zero(s.diff(F,R)/(4*s.pi*R**2)-(D+2*Sigma/R-N*kT/Vol)))
rr,G,M,b,cs=s.symbols('rr G M b cs',positive=True)
Phi=-G*M/s.sqrt(rr**2+b**2)
lnrho=-Phi/cs**2
check('baryon-only density hydrostatics',zero(cs**2*s.diff(lnrho,rr)+s.diff(Phi,rr)))

runs=[]
for dc in [.01,.03,.1]:
    pair=[]
    for tol in [1e-9,1e-11]:
        x0=1e-5; B=1.; ds=.001
        # central regular series: m=dc*x^3/3, ln d=ln dc-(B+dc/3)x^2/2
        y0=[dc*x0**3/3,np.log(dc)-(B+dc/3)*x0*x0/2]
        def ode(x,y):
            return [x*x*np.exp(y[1]),-(y[0]+B*x**3/(1+x*x)**1.5)/x**2]
        def edge(x,y):
            return y[1]-np.log(ds)
        edge.terminal=True;edge.direction=-1
        sol=solve_ivp(ode,(x0,300),y0,method='DOP853',rtol=tol,
                      atol=tol/100,max_step=.2,events=edge,dense_output=True)
        check(f'{dc} {tol} reaches pressure surface',sol.success and len(sol.t_events[0])==1)
        if not len(sol.t_events[0]):
            continue
        root=float(sol.t_events[0][0]); mass=float(sol.y_events[0][0][0])
        xs=np.linspace(x0,root,101); ys=sol.sol(xs)
        check(f'{dc} {tol} positive monotone mass and density',np.all(np.diff(ys[0])>0) and np.all(np.diff(ys[1])<0))
        pair.append({'central_density':dc,'rtol':tol,'radius':root,'pool_mass':mass,
                     'surface_total_v2_over_cs2':(mass+B*root**3/(1+root**2)**1.5)/root,
                     'x':xs.tolist(),'mass':ys[0].tolist(),'density':np.exp(ys[1]).tolist()})
    if len(pair)==2:
        for key in ['radius','pool_mass']:
            check(f'{dc} tolerance agreement {key}',abs(pair[0][key]/pair[1][key]-1)<1e-6)
    runs.extend(pair)
fine=[r for r in runs if r['rtol']==1e-11]
check('same baryons dispersion pressure allow distinct pool masses',len(fine)==3 and min(abs(a['pool_mass']/b['pool_mass']-1) for i,a in enumerate(fine) for b in fine[i+1:])>1e-3)
result={'checks':checks,'passed':all(checks.values()),'runs':runs,'mutated':a.mutate,
        'interpretation':'Equilibrium nonuniqueness and local phase/wall identities, not a formation or MOND prediction.'}
Path(a.out).write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['passed'] else 1)
