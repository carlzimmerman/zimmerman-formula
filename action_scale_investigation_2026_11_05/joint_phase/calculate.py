"""Joint phase-energy and force-response calculation, no target input."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
A,B,t,h,p,sigma,K,G,delta,L,m=s.symbols('A B t h p sigma K G delta L m',positive=True)
U0=s.symbols('U0',real=True)
checks={}
def check(name,expr):
 checks[name]=bool(expr);print(('PASS ' if expr else 'FAIL ')+name,flush=True)
cone=-((L*L+m*m)**s.Rational(3,2)-m**3)/3+L**3/3+L*m*m/2
check('subtracted two-dimensional cone energy',s.simplify(s.limit(cone,L,s.oo)-m**3/3)==0)
R=s.sqrt(sigma*sigma+h*h*p*p)
U=U0-t*R*R/2+A*R**3/3+B*h**3*p**3/3+delta*p*p/2
check('amplitude stationarity',s.simplify(s.diff(U,sigma)-sigma*(-t+A*R))==0)
m0=t/A;pc=m0/h;C=B*h**3
Ueff=U0-t**3/(6*A*A)+C*p**3/3+delta*p*p/2
# Evaluate on R=t/A without choosing a sign for sigma or taking a branch square root.
branch=s.simplify((U0-t*m0*m0/2+A*m0**3/3+B*h**3*p**3/3+delta*p*p/2)-Ueff)
check('relaxed potential on condensed branch',branch==0)
curv=s.diff(U,sigma,2)
curv_branch=s.simplify(curv.subs(sigma,s.sqrt(m0*m0-h*h*p*p)))
check('amplitude curvature and endpoint',s.simplify(curv_branch-t*(1-(p/pc)**2))==0)
vac=Ueff.subs(p,0);gap=U0-vac
check('phase energy difference',s.simplify(gap-t**3/(6*A*A))==0)
check('uncondensed origin is not metastable',s.simplify(s.limit(s.diff(U,sigma,2).subs(p,0),sigma,0,dir='+')+t)==0)
force=s.diff(Ueff,p)
used_force=C*p*p+(0 if args.mutate else delta*p)
g=p+K*used_force;gn=K*used_force
check('full force retains allowed quadratic',s.simplify(g-p-K*force)==0)
check('spherical Poisson flux',s.simplify(g-p-gn)==0)
a0=1/(K*C)
check('critical deep MOND response',s.simplify(s.limit((g*g/gn).subs(delta,0),p,0,dir='+')-a0)==0)
check('noncritical infrared has no MOND constant',s.limit(g*g/gn,p,0,dir='+')==0)
gtrue=p+K*force;gntrue=K*force
check('noncritical force is linear in Newtonian field',s.simplify(s.limit(gtrue/gntrue,p,0,dir='+')-(1+K*delta)/(K*delta))==0)
Uabove=U.subs(sigma,0)
check('endpoint energy continuity',s.simplify((Uabove-Ueff).subs(p,pc))==0)
check('endpoint force continuity',s.simplify((s.diff(Uabove,p)-force).subs(p,pc))==0)
check('endpoint amplitude curvature vanishes',s.simplify((t*(1-(p/pc)**2)).subs(p,pc))==0)
kap2=a0*a0/(G*vac)
check('vacuum offset remains physical input',s.simplify(s.diff(kap2,U0)+a0*a0/(G*vac*vac))==0 and s.diff(kap2,U0)!=0)
lam=s.symbols('lambda_phase',positive=True)
ratio_gap=s.simplify(a0*a0/(G*gap))
check('conditional phase-gap ratio',s.simplify(ratio_gap-6*K/G*(B/A)*(a0/pc)**3)==0)
check('critical force is Newton plus square-root term',s.simplify(gtrue.subs(delta,0)-(gntrue.subs(delta,0)+p))==0)
out={'passed':all(checks.values()),'mode':'drop_delta' if args.mutate else 'main','checks':checks,
 'results':{'sigma_squared':str(m0*m0-h*h*p*p),'p_endpoint':str(pc),'U_effective':str(Ueff),
 'vacuum_energy':str(vac),'phase_gap':str(gap),'C3':str(C),'a_MOND_critical':str(a0),
 'kappa_squared_if_vacuum_identified':str(s.factor(kap2)),
 'lambda_phase':str(s.simplify(pc/a0)),'phase_gap_ratio_conditional':'24*pi*(B/A)/lambda_phase^3'},
 'scope':'Conditional mean-field spectral parent and leading static force; not absolute vacuum matching or a covariant healthy theory.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(out,indent=2)+'\n')
raise SystemExit(0 if out['passed'] else 1)
