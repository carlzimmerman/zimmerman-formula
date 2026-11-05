"""Own-action radial equations and formal GR limit; no charged solution claim."""
import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
r=s.symbols('r',positive=True)
N=s.Function('N')(r);B=s.Function('B')(r);p=s.Function('p')(r)
m2,K,b,q,V,gam=s.symbols('M2 K b q V gamma',positive=True)
nn,pp=s.symbols('N0 p0',positive=True)
UF=s.Function('U');U=UF(N,p)
X=q*q/(2*N*N);d=s.diff(p,r)+2*p/r
Lg=m2*(N*B+N/B+2*r*s.diff(N,r)/B)
Lold=m2*N*(B-1/B+2*r*s.diff(B,r)/B**2)
L=Lg+N*B*r*r*(X-V-U)+r*r*p*s.diff(N,r)/K-gam*N*r*r*d*d/(2*K*K*B)
checks={}
def check(n,z):
 checks[n]=bool(z);print(('PASS ' if z else 'FAIL ')+n,flush=True)
check('radial Einstein integration by parts',s.simplify(Lold-Lg+s.diff(2*m2*N*r/B,r))==0)
def EL(f):return s.diff(L,f)-s.diff(s.diff(L,s.diff(f,r)),r)
Un=s.diff(U,N);Up=s.diff(U,p)
EN=m2*(B-1/B+2*r*s.diff(B,r)/B**2)-B*r*r*(X+V+U+(0 if args.mutate else N*Un))-s.diff(r*r*p,r)/K-gam*r*r*d*d/(2*K*K*B)
EB=m2*(N-(N+2*r*s.diff(N,r))/B**2)+N*r*r*(X-V-U)+gam*N*r*r*d*d/(2*K*K*B**2)
EP=r*r*s.diff(N,r)/K-N*B*r*r*Up+gam*r*r/K**2*s.diff(N*d/B,r)
check('lapse Euler-Lagrange equation',s.simplify(EL(N)-EN)==0)
check('radial metric Euler-Lagrange equation',s.simplify(EL(B)-EB)==0)
check('polarization Euler-Lagrange equation',s.simplify(EL(p)-EP)==0)
aval=s.sqrt(b*(q*q/(2*nn*nn)+V))
W=aval**2/K*(-pp/aval-s.log(1-pp/aval))
ss=s.symbols('s',positive=True)
h=ss+ss/(1+ss)-2*s.log(1+ss)
NWn=s.diff(W,nn)*nn
target=b*q*q/(2*nn*nn*K)*h
check('density-portal lapse contribution',s.simplify(s.expand_log(NWn.subs(pp,aval*ss/(1+ss)),force=True)-target)==0)
check('polarization conjugate derivative',s.simplify(K*s.diff(W,pp)-pp/(1-pp/aval))==0)
mass=s.symbols('mass',positive=True)
f=1-2*mass/r-V*r*r/(3*m2)
# Formal uncharged q->0 limit of equations, not a q=0 normalized-clock field.
Ng=s.sqrt(f);Bg=1/s.sqrt(f)
ENgr=m2*(B-1/B+2*r*s.diff(B,r)/B**2)-B*r*r*V
EBgr=m2*(N-(N+2*r*s.diff(N,r))/B**2)-N*r*r*V
check('Schwarzschild-de Sitter lapse constraint',s.simplify(ENgr.subs(B,Bg).doit())==0)
check('Schwarzschild-de Sitter radial metric constraint',s.simplify(EBgr.subs({N:Ng,B:Bg}).doit())==0)
out={'mode':'omit_portal_lapse_source' if args.mutate else 'main','checks':checks,'passed':all(checks.values()),'radial_lagrangian':str(L),'lapse_equation':str(EN),'radial_metric_equation':str(EB),'polarization_equation':str(EP),'scope':'Static V=constant radial equations; q->0 is a formal GR benchmark; no charged background solved.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(out,indent=2)+'\n');sys.exit(0 if out['passed'] else 1)
