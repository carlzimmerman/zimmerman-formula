"""Self-scattering kinematics, evaporation moments and local source stability."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--mutate',action='store_true');args=p.parse_args()
checks={}
def eq(k,a,b):checks[k]=bool(s.simplify(a-b)==0)
m,Q,ls=s.symbols('m Q ls',positive=True)
mand=4*m*m+2*m*Q
sig=ls**2/(32*s.pi*mand)
eq('self cross section cold limit',sig.subs(Q,0),ls**2/(128*s.pi*m*m))
u,B=s.symbols('u B',positive=True)
eq('uniform partition energy',s.integrate(u+(Q-u),(u,0,Q))/Q,Q)
eq('bound energy fraction B less than Q',2*s.integrate(u/Q,(u,0,B))/Q,(B/Q)**2)
eq('mean leading fragment',2*s.integrate(u/Q,(u,Q/2,Q)),3*Q/4)
eq('mean logarithmic leading fraction',2*s.integrate(s.log(u),(u,s.Rational(1,2),1)),s.log(2)-1)
theta,x,y=s.symbols('theta x y',positive=True)
# Flux energy density is proportional e exp(-e/theta), truncated above B.
I1=s.integrate(y*s.exp(-y),(y,x,s.oo));I2=s.integrate(y*y*s.exp(-y),(y,x,s.oo))
eq('escape flux tail',I1,(1+x)*s.exp(-x))
eq('escape energy moment',I2/I1,(x*x+2*x+2)/(x+1))
a0=s.symbols('a0',positive=True)
a=a0*s.sqrt(theta)*(1+B/theta)*s.exp(-B/theta)
esc=B+theta+theta**2/(B+theta)
eq('evaporation logarithmic slope',s.diff(a,theta)/a,(s.Rational(1,2)+(B/theta)**2/(1+B/theta))/theta)
eq('escape energy slope',s.diff(esc,theta),1+theta/(B+theta)+B*theta/(B+theta)**2)
J,K,n,ein=s.symbols('J K n ein',positive=True);cv=s.Rational(3,2)
ndot=J-K*n*n-a*n
Tdot=(J*(ein-cv*theta)-a*n*(esc-cv*theta))/(cv*n)
if args.mutate:Tdot=(J*ein-cv*theta*K*n*n-a*n*esc)/(cv*n)
eq('kinetic energy conservation',cv*(n*Tdot+theta*ndot),J*ein-cv*theta*K*n*n-a*n*esc)
# Jacobian reconstructed independently from symbolic generic a(T), e(T).
z=s.symbols('z',positive=True);af=s.Function('a')(z);ef=s.Function('e')(z)
f=J-K*n*n-af*n;g=(J*(ein-cv*z)-af*n*(ef-cv*z))/(cv*n)
A,Ap,E,Ep=s.symbols('A Ap E Ep',positive=True)
sub={s.diff(af,z):Ap,s.diff(ef,z):Ep,af:A,ef:E}
mat=s.Matrix([f,g]).jacobian([n,z]).subs(sub)
js=n*(K*n+A);eins=(cv*z*K*n+A*E)/(K*n+A)
mat=s.simplify(mat.subs({J:js,ein:eins}))
b=E-cv*z
eq('local Jacobian trace',s.trace(mat),-3*K*n-A-(Ap*b+A*Ep)/cv)
eq('local Jacobian determinant',mat.det(),(2*K*n+A)*K*n+(2*K*n*Ap*b+(2*K*n+A)*A*Ep)/cv)
eq('escaping particles hotter than mean',((esc-cv*theta)/theta).subs(B,x*theta),(x*x+x/2+s.Rational(1,2))/(x+1))
r,R,rc,amp,G=s.symbols('r R rc amp G',positive=True)
loss=s.integrate(4*s.pi*r*r*K*(amp/r**2)**2,(r,rc,R))
eq('flat tail annihilation inventory loss',loss,4*s.pi*K*amp**2*(1/rc-1/R))
v=s.symbols('v',positive=True)
eq('flat tail rest energy power',s.simplify(m*loss.subs(amp,v*v/(4*s.pi*G*m))),K*v**4/(4*s.pi*G*G*m)*(1/rc-1/R))
result={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'mutation':args.mutate,'scope':'Tree contact model, Maxwell exobase, fixed-volume fixed-potential local stability, prescribed flat-tail source requirements.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if all(checks.values()) else 1)
